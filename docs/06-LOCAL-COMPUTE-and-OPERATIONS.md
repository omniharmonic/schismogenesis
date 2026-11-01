# B10: Running the Arena Pipeline on One Local Blackwell Box

*Research brief for the Dialogos Arena. Author of record: Benjamin Life (@omniharmonic). Prepared 2026-10-31 as design task B10. It builds on the Data Model and Encounter Plan (2026-10-31), Design Memo §7 (2026-10-30), B9 §4 (transcript pipeline) and Topology Live's extraction design (`antidebate-live/docs/ARCHITECTURE.md` §2–3, `packages/pipeline`, `packages/llm`).*

**How to read this.** Figures marked **MEASURED** come from a cited benchmark (vendor or community) on the named hardware. **ESTIMATE** means derived arithmetic or extrapolation, and it always comes with a range. **UNVERIFIED** means a claim could not be checked against a primary source in this session. Community benchmarks on DGX Spark vary by ±30% between runs and software builds (the authors say so), so treat every number as a planning number and replace it with day-1 measurements on the actual box.

---

## Summary

1. **The box.** The likely box is a DGX Spark or an OEM GB10 clone (ASUS Ascent GX10, Dell Pro Max GB10, HP ZGX Nano, Lenovo PGX). All of them have **128 GB of unified LPDDR5X at 273 GB/s**, up to 1 PFLOP of sparse FP4, a 20-core ARM CPU, DGX OS (Ubuntu 24.04) and CUDA 13. **Memory bandwidth, not compute, sets LLM decode speed.** Only mixture-of-experts (MoE) models with roughly 3–12B active parameters run well on it. Dense 70B models are impractical (2.7 tok/s MEASURED).
2. **Measured speeds.**
   - gpt-oss-120b: about 1,700 tok/s prefill and 50–60 tok/s decode for one stream. Batched, it reaches about 120–150 tok/s at 8 concurrent requests and a reported ~860 tok/s at 256 streams.
   - Small MoE models (Qwen3.6-35B-A3B, Gemma-4-26B-A4B): about 300 tok/s aggregate at 8 concurrent requests on stock vLLM, and 740–1,900 tok/s at 32–128 concurrent requests on tuned community builds.
3. **The backfill fits on the box.** About 6,000 transcript hours ≈ 75M transcript tokens. That becomes ≈ 0.3–0.6B fresh input tokens and ≈ 90–230M output tokens across extract, critic, tag and dedup (ESTIMATE). On the box that is about **3–16 days of extraction compute**. ASR, diarization, NLI, embedding and classification add roughly **2–8 days**. The total is **about 1–3 weeks of continuous running** (ESTIMATE). Caption-fetch pacing (3–6 weeks) remains the binding constraint, as before.
4. **A weekly refresh** of about 770 landmarks needs about **0.5–2.5 box-days per week** (ESTIMATE).
5. **Reliability comes from structure.** A smaller model is made reliable by the surrounding structure, not by the model itself:
   - schema-constrained decoding;
   - a decomposed extract→critic chain run on *different* models;
   - deterministic quote anchoring;
   - an NLI entailment gate;
   - agreement voting on high-stakes content;
   - confidence-routed escalation to Claude;
   - LoRA distillation from a Claude-labeled and human-checked gold set (feasible on the box).
6. **Orchestration.** A deterministic Postgres-backed job queue (Procrastinate) runs the pipeline. A Hermes-based operator agent watches it, triages failures and writes reports. It is never in the data path.

---

## Findings

### 1. Hardware facts and measured throughput

#### 1.1 GB10-class box (DGX Spark and OEM equivalents)

| Item | Value | Source |
|---|---|---|
| SoC | GB10 Grace Blackwell: Blackwell GPU (5th-gen Tensor Cores) + 20-core Arm CPU (10× Cortex-X925, 10× Cortex-A725) | NVIDIA product page; LMSYS |
| Memory | **128 GB LPDDR5X coherent unified memory** (CPU and GPU share it); ~119–121 GiB usable in practice | NVIDIA; NVIDIA forum (121 GiB reported) |
| Memory interface / **bandwidth** | 256-bit, **273 GB/s** | NVIDIA |
| AI compute | Up to **1 PFLOP FP4 with sparsity** | NVIDIA |
| Precisions | NVIDIA's spec names only FP4. Blackwell Tensor Cores also run FP8/FP6 and the NVFP4/MXFP4 block formats. Community recipes use NVFP4, MXFP4, INT4 (AutoRound/AWQ) and FP8 KV cache | NVIDIA; forum recipes |
| GPU compute capability | **sm_121**. This matters: some kernels and wheels need source builds or patches (§1.4) | Unsloth guide; transcribe-dgx |
| Storage | Up to 4 TB NVMe (Founders). ASUS ships 1 TB Gen4 standard (slow writes, about 0.72 GiB/s peak measured by StorageReview) or 4 TB Gen5 | NVIDIA; Spheron/StorageReview |
| Networking | ConnectX-7, 2× QSFP (200 Gbps; two units can be clustered), 10 GbE, Wi-Fi 7 | NVIDIA |
| Power | 240 W PSU; GB10 TDP 140 W | NVIDIA |
| OS / stack | **DGX OS** (Ubuntu 24.04 based), CUDA 13, NGC containers (e.g., `nvcr.io/nvidia/pytorch:25.xx-py3`), NeMo, RAPIDS, NIM, playbooks at build.nvidia.com/spark | NVIDIA; forum posts |
| OEM differences | Same silicon, same 128 GB and 273 GB/s. They differ in storage, chassis cooling and warranty. Community reports note unit-to-unit thermal variance under sustained load | Spheron comparison |
| Price | $3,999 at launch; $6,950 for 128 GB/4 TB as of 2026-10-03 (reported) | Spheron |

**Rule of thumb (bandwidth bound).** The single-stream decode ceiling is about 273 GB/s ÷ (bytes of weights read per token).

| Model class | Weights read per token | Decode ceiling | Measured |
|---|---|---|---|
| gpt-oss-120b (5.1B active, MXFP4) | ~3 GB | ~90 tok/s | 50–60 tok/s |
| A dense 32B at 4-bit | ~17 GB | ~16 tok/s | — |
| Dense 70B at FP8 | ~70 GB | ~4 tok/s | 2.7 tok/s (LMSYS) |

**Conclusion: use sparse MoE models with few active parameters, and win on batching.** Prefill is compute-bound and 30–70× faster than decode, so input tokens are cheap and output tokens are expensive.

#### 1.2 LLM serving: measured numbers on GB10

| Model (license) | Engine / quant | Prefill tok/s | Decode, 1 stream | Batched aggregate decode | Source (date) |
|---|---|---|---|---|---|
| **gpt-oss-120b** (Apache 2.0; 117B total, 5.1B active) | llama.cpp MXFP4 | 1,689 (pp2048); 1,221 at 32k depth | 52.9; 38.8 at 32k depth | — | ggml/jetsonhacks llama-bench (Oct 2025) |
| | llama.cpp MXFP4 | 1,725 | 55.4 | — | NVIDIA blog (Oct 2025) |
| | vLLM 4-bit (v0.26 dev) | — | 60.7 | **116–153 @ c=8** | NVIDIA forum, ss121 (Aug 2026) |
| | vLLM MXFP4 | — | 33.5 | **862.8 @ 256 streams** | Dendro Logic (Apr 2026), via a secondary summary; UNVERIFIED at source |
| | Ollama | — | 42.1 | 42.5 @ c=8 (no batching gain) | ss121 (Aug 2026) |
| **gpt-oss-20b** (Apache 2.0; 21B, 3.6B active) | llama.cpp MXFP4 | 3,611 | 79.7 | — | ggml (Oct 2025) |
| | SGLang | — | ~70 | — | LMSYS (Nov 2025) |
| | Ollama | 2,053 | 49.7 | — | LMSYS (Oct 2025) |
| **Qwen3-30B-A3B** | vLLM 4-bit | — | 77.1 | **313 @ c=8** | ss121 (Aug 2026) |
| Qwen3-Coder-30B-A3B | llama.cpp Q8_0 | 2,933 | 60.0 | — | ggml (Oct 2025) |
| **Qwen3.6-35B-A3B** (Apache 2.0; released 2026-04-16; 3B active; 256K ctx) | vLLM NVFP4 + DFlash speculative decoding (community build) | ~230–510 (short prompts) | 75–124 (by task; 80 on extraction/JSON) | **~740 @ c=64** | AEON-7 vllm-ultimate-dgx-spark wiki (Jun–Jul 2026) |
| **Gemma-4-26B-A4B** (Apache 2.0) | vLLM 4-bit + MTP | — | 54.9 | **304 @ c=8** | ss121 (Aug 2026) |
| | vLLM NVFP4 + DFlash (tuned) | ~320–600 | 50–200 by task | **746–1,151 @ c=32–128; 1,937 peak @ c=64** | AEON-7 wiki (Jul 2026) |
| Qwen3.6-27B (dense) | vLLM NVFP4 + MTP/DFlash | ~180–320 | 34–56 (stock ~10.5) | ~344 @ c=64 | AEON-7 wiki |
| **Qwen3.5-122B-A10B** (Apache 2.0) | vLLM INT4 AutoRound (+FP8 shared experts, MTP-1) | — | 28.3 → **38.4** with MTP; NVFP4 only 16.6 | not reported | NVIDIA forum (Apr 2026) |
| Nemotron-3-Super-120B-A12B | vLLM NVFP4 | 1,636–1,884 | 22.7–23.7 | — | secondary summary (Jun 2026) |
| GLM-4.5-Air | llama.cpp Q4_K | 841 | 22.6 | — | ggml (Oct 2025) |
| Llama 3.1 70B | SGLang FP8 | 803 | **2.7** | — | LMSYS (Oct 2025) |
| Llama 3.1 8B | SGLang | 7,991 | 20.5 | 368 @ b=32 | LMSYS (Oct 2025) |
| Qwen3 14B | TRT-LLM NVFP4 | 5,929 | 22.7 | — | NVIDIA blog |
| Qwen3-235B | TRT-LLM NVFP4, **two Sparks** | 23,477 | 11.7 | — | NVIDIA blog |
| A small MoE (ss121's long-prompt test) | vLLM | ~6,000 (a 27k-token prompt in 3.6–4.5 s) | — | — | ss121 (Aug 2026) |

**What the table says:**

- **Ollama does not batch.** Its 8-concurrent aggregate equals single-stream. Use **vLLM** (or SGLang) for the pipeline, and llama.cpp/Ollama only for quick interactive tests.
- **Kernel path matters more than format.** One NVFP4 checkpoint ran at about 1.1 tok/s on a vanilla build (emulation fallback) and about 77 tok/s with FlashInfer CUTLASS kernels. INT4 AutoRound beat NVFP4 on Qwen3.5-122B. **Use the community's Spark-specific recipes and containers**, and benchmark on day 1.
- **Speculative decoding (MTP/EAGLE/DFlash)** gives the biggest single-stream gain (+30–80%), but matters less at high batch.
- **Qwen3-235B and larger models do not fit usefully on one box.** Late-2026 frontier open models (DeepSeek-V4, Kimi K2.7, GLM-5.x, Mistral Large 3) need multi-GPU nodes. The 120B-class MoEs (gpt-oss-120b, Qwen3.5-122B-A10B, Nemotron-3-Super, Mistral Small 4 119B-A6.5B at 4-bit, which is UNVERIFIED on Spark) are the upper bound for one GB10.
- The "Llama" line has no current open model worth running here. Dense Llama 3.x is bandwidth-starved, and the Llama 4 MoEs were not benchmarked on Spark in sources found (UNVERIFIED).

#### 1.3 If the box is instead an RTX PRO 6000 Blackwell (96 GB) workstation

| | DGX Spark (GB10) | RTX PRO 6000 Blackwell WS |
|---|---|---|
| Memory | 128 GB unified LPDDR5X | **96 GB GDDR7 ECC** (plus separate host RAM) |
| Bandwidth | 273 GB/s | **1,792 GB/s (≈ 6.6×)** |
| FP4 (sparse) | ~1 PFLOP | 4,000 TOPS (≈ 4×) |
| Power | 240 W system | 600 W card alone |
| gpt-oss-20b, Ollama (LMSYS) | 2,053 prefill / 49.7 decode | **10,108 / 215 (≈ 4–5×)** |
| Host | ARM64, sm_121, DGX OS | x86-64 host; mainstream wheels (fewer source builds) |

**How the conclusions change:**

- **LLM stages run about 3–5× faster** (ESTIMATE from the bandwidth ratio and LMSYS's 4× on gpt-oss-20b). Backfill extraction drops from about 3–16 days to about **1–4 days**, and the weekly refresh to a few hours.
- **Capacity is tighter.** gpt-oss-120b (~61 GB) still fits with about 25–30 GB left for KV cache. Qwen3.5-122B-A10B at 4-bit (about 65–75 GB) leaves little KV room, and you cannot co-host ASR, embedding and NLI models alongside it as comfortably. On a PRO 6000 the natural choice is gpt-oss-120b or a 30–35B MoE.
- **Larger fine-tunes get harder.** 120B QLoRA (~68 GB on Spark per Unsloth) is marginal in 96 GB. 20–35B LoRA is easy.
- **Software is easier.** x86 + sm_120 has broader prebuilt support for CTranslate2, pyannote and torchaudio. The ARM/sm_121 friction in §1.4 mostly disappears.
- **Everything else in this brief is the same:** pipeline design, reliability methods, orchestration and pre-arrival plan.

#### 1.4 Software-stack cautions on GB10 (ARM64, sm_121)

- **Run everything in NGC-based containers.** Do not pip-install CUDA stacks on the host. The working community recipes are:
  - Parakeet: `nvcr.io/nvidia/pytorch:25.11-py3` + `nemo_toolkit[asr]`, with `lhotse` pinned below 1.30.
  - Unsloth: `pytorch:25.09-py3`, with Triton and xformers built for compute capability 12.1.
- **WhisperX / faster-whisper needed patches on Spark:** compute-capability spoofing, a torchaudio FFT workaround, and CTranslate2 and torchaudio built from source (rappdw/transcribe-dgx). This is another reason to prefer NeMo Parakeet on this box.
- vLLM on Spark moves fast (v0.19 → v0.26 between April and August 2026). Pin a known-good container image per model, and record `engine_version` in every `LlmCall` row.

### 2. ASR and diarization locally

| Model | License | English avg WER (Open ASR Leaderboard) | RTFx (A100, batch 64) | Word timestamps | Notes |
|---|---|---|---|---|---|
| **Parakeet TDT 0.6B v3** | CC-BY-4.0 | 6.32 | **3,333** | Yes (word, segment, char) | 25 European languages, auto language detection, punctuation and casing. Up to 24 min per pass with full attention; up to **3 h with local attention**. NeMo route; community Spark container exists |
| Parakeet TDT 0.6B v2 | CC-BY-4.0 | 6.05 | 3,386 | Yes | English-only; slightly better English WER |
| **Canary-Qwen-2.5B** | (check card) | **5.63 (best)** | 418 | Via NeMo (verify) | LLM-decoder; about 8× slower than Parakeet |
| Canary-1B-Flash | — | 6.35 | 1,046 | Yes | Middle option |
| Whisper large-v3 | MIT | 7.44 | 146 | Needs alignment (WhisperX wav2vec2) | Slowest. faster-whisper batched large-v2 did 13 min of audio in 17 s on an RTX 3070 Ti (≈ 46× real time) |

*Source: Open ASR Leaderboard paper (arXiv 2510.06961 v3), Table 3; Parakeet model card.*

**GB10 speed (ESTIMATE).** No credible long-form Parakeet benchmark on GB10 was found; a forum post only timed clips of a few seconds. GB10's dense tensor throughput is a fraction of an A100's and its bandwidth is about 1/7. So plan for Parakeet at **RTFx ≈ 300–1,000** (1 h of audio in about 4–12 s). The low end of that range allows for CPU-side MP3 decoding and VAD chunking. Whisper large-v3 through faster-whisper would run at about 30–60× real time and turbo at about 100–200× (ESTIMATE), after the CTranslate2 source build.

**Diarization.** pyannote **speaker-diarization-community-1** (CC-BY-4.0):

- DER improves on 3.1 on most benchmarks (e.g., AMI-SDM 19.9 vs 22.7; VoxConverse 11.2, the same as 3.1).
- It adds an **exclusive diarization** output designed for reconciling with STT word timestamps.
- On CPU (Apple M2) it ran at RTF 0.82, versus 1.74 for 3.1 (diarize benchmarks).
- On GPU, pyannote 3.1's card reported about 2.5% RTF on a V100 (about 1.5 min per audio hour). That figure is recalled and was not re-fetched this session (UNVERIFIED).
- Plan for **RTF 0.02–0.05 on GB10** (ESTIMATE). The clustering step is CPU-bound, so it can overlap with GPU work.

Alternatives:

- **NVIDIA Streaming Sortformer 4spk v2.1** (NeMo; limited to 4 speakers, which fits most podcasts).
- **`diarize`** (Apache 2.0; CPU RTF 0.12, VoxConverse DER about 10.8).
- pyannote's hosted precision-2 is better again (VoxConverse 8.5) but is a paid API, so it is out of scope.

**Word timestamps.** Parakeet emits word timestamps natively, so no wav2vec2 alignment pass is needed. YouTube captions give cue-level timing (seconds). That is enough for `?t=` deep links but not for word-precise anchors.

**Speaker naming (highest-harm failure; B9 and the Data Model's OPEN-6).** Fuse four signals:

1. Episode metadata (host and guest list).
2. Voiceprint similarity (pyannote or TitaNet embeddings enrolled from each landmark's solo content).
3. Topology Live's `speaker_id` LLM pass (self-identification in the transcript).
4. Diarizer agreement.

Publish only above the threshold, as Topology Live does. Below it, hold the item for operator confirmation.

**Acquisition caveat.** Local ASR removes the STT bill but not the sourcing question.

- Podcast RSS enclosures are published for download, so they are fine.
- YouTube-only multi-speaker content needs audio for diarization. Pulling audio (e.g., with yt-dlp) is a *stronger* ToS exposure than pulling captions.
- Keep it in the risk register (R49). Prefer RSS audio or landmark opt-in for encounter episodes, and use captions alone for solo monologues, where speaker = channel owner (still verify).

### 3. Local replacements for closed services

**Jev (TypeSafe's closed "decision" model, per B4).** It returns calibrated probabilities over choices you define. Local equivalents, in rising order of investment:

1. **LLM constrained choice + logprobs.**
   - vLLM `structured_outputs.choice` (or single-token labels A–E) with `logprobs` yields a probability distribution over labels from any local model.
   - Calibrate with temperature scaling against gold labels.
   - This is the closest drop-in. It costs about 300–500 prefill tokens and about 1–5 output tokens per item, which is cheap on this box because prefill is fast.
2. **GLiClass** (Knowledgator; Apache 2.0; ModernBERT base 151M / large 399M):
   - Zero-shot multi-label classification in one forward pass.
   - Average F1 over 11 datasets: 0.556 (base) and 0.605 (large). It beats BART-MNLI and DeBERTa-NLI zero-shot on most of them.
   - Good for a first pass at thousands of items per second.
3. **SetFit** (contrastive fine-tuning of a sentence encoder plus a logistic head) with 8–64 examples per class. Use it once a few hundred Claude- or human-labeled items exist.
4. **A fine-tuned ModernBERT/DeBERTa classifier** per task (stratum, speech act, stance attitude, question relevance), once ≥ 1–2k labels per task exist. Calibrate it and report ECE.

**Layering.** Use (1) to produce silver labels, check a sample with Claude and Benjamin, then distill into (3) or (4) for the daily pulse. Keep (1) as the fallback for low-confidence items.

**GLiNER / GLiNER2** (from knowledge; UNVERIFIED this session) handle the entity side: person and organization mentions for `ContentEdge` "names_to_rebut / names_to_endorse", and entity-diff validation.

**Embeddings for proposition dedup:**

| Model | License | Notes |
|---|---|---|
| **Qwen3-Embedding 0.6B / 4B / 8B** | Apache 2.0 | Dims 1024 / 2560 / 4096; **MRL** (8B supports 32–4096 dims); 32K context; instruction-aware (+1–5%); MTEB multilingual 70.58 and English v2 75.22 (8B); served by vLLM (`task="embed"`); companion **Qwen3-Reranker** (0.6B / 4B / 8B) |
| BGE-M3 | MIT (from knowledge) | 568M; dense + sparse + multi-vector; 8K context; good hybrid fallback |
| nomic-embed-text v1.5/v2 | Apache 2.0 (from knowledge) | Small, MRL; CPU-friendly |

Recommendation:

- Use **Qwen3-Embedding-4B truncated to 1024 dims** in pgvector (`halfvec`), with an instruction like "represent this claim to find claims with the same truth conditions".
- Use **Qwen3-Reranker-0.6B/4B** as a second filter.
- Use an **LLM adjudicator** for the final strict equivalence test (Topology Live §3.4: same truth conditions, same scope, polarity-normalized).
- Embeddings alone confuse "X" with "not X", so they are for candidate retrieval only.

**NLI as a "quote entails claim" check:**

- **Model:** `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (MIT; MNLI 0.91, ANLI 0.70; about 500–1,000 pairs/s on an A100).
- **Premise:** the anchor quote plus one sentence of context.
- **Hypothesis:** the speaker-committed form of the proposition. Use the proposition itself for `accepts`, and its negation for `rejects`, because the bank is polarity-normalized.
- **Decision rule:**
  - contradiction → reject;
  - neutral → critic or escalation;
  - entailment ≥ threshold → pass.
- Mind the 512-token limit.
- **Alternatives:** MiniCheck-DeBERTa-v3-Large / RoBERTa-Large / Flan-T5-Large (0.4–0.8B; check licenses). **Bespoke-MiniCheck-7B is CC BY-NC 4.0, so avoid it** unless licensed.

**Expected GB10 speed** (ESTIMATE): about 100–300 pairs/s, so the full backfill takes 0.5–2 h.

### 4. Making weaker models reliable

Topology Live's design already separates *proposal* from *acceptance* (every pass writes proposals; validators and the critic gate them). Offline on open models, the same design should be tightened as follows.

1. **Decompose L1 into narrower calls.**
   1. Segment into ADUs and **select verbatim quotes** (extractive, which small models do well).
   2. Write a neutral proposition per ADU (generative, the hardest step).
   3. Assign attributes (speech act from 13, type from 10, stratum from 5, attitude, strength, source) through **constrained-choice** fields.
   4. Run the critic (L2) as a separate call.

   Narrow calls with short outputs suit MoE models and batch well.
2. **Schema-constrained decoding.**
   - vLLM `structured_outputs` (`json`, `choice`, `regex`, `grammar`, `structural_tag`) or OpenAI-style `response_format: json_schema`.
   - The backend is `auto` (xgrammar/guidance). The old `guided_*` fields were **removed in vLLM 0.12**.
   - With reasoning models (gpt-oss harmony, Qwen thinking), let the model reason first and constrain only the final JSON. Use `--reasoning-parser` and, for some models, `structured_outputs_config.enable_in_reasoning`.
   - Generate the JSON Schemas **from the Zod ontology** (`packages/ontology`), so Claude and the local models share one contract.
   - Constraint guarantees syntax, not truth.
3. **Deterministic code gates** (reuse `packages/ontology/validate.ts` and `pipeline/quotes.ts`):
   - **Quote anchoring.** Topology Live's `locateQuote` is exact `indexOf` with no repair. For ASR and caption text, add a *normalized* matcher: NFC, collapsed whitespace, lowercase, stripped punctuation and normalized apostrophes, with an offset map back to the original. Add a *fuzzy locator* as a last resort (e.g., rapidfuzz `partial_ratio_alignment` ≥ 95 with ≤ 2 token edits). It may only **locate**. The stored quote is always the **source substring**, never the model's text. Fuzzy anchors carry `anchor_match = fuzzy` and must pass NLI and the critic. This keeps Topology Live's invariant that nothing is repaired into a span.
   - Entity/number diff, hedge lexicon, quantifier lexicon, speech-act guard, attribution guard: as in Topology Live §3.3.
4. **NLI gate** (§3) on every stated stance.
5. **Cross-model critic.** The critic should be a *different* model family from the extractor, with no access to the extractor's reasoning (Topology Live's independence rule). For example, a Qwen3.6 extractor with a gpt-oss-120b critic.
6. **Self-consistency voting, used selectively.**
   - On the encounter/coverage set (about 450–700 h, highest stakes) and on chunks flagged as uncertain, run extraction k = 2–3 times, either across two models or at temperature 0.7.
   - Keep propositions found in ≥ 2 runs. Match runs by anchor overlap ≥ 50% plus embedding similarity.
   - Disagreement escalates.
   - This roughly doubles to triples the extraction cost for that slice only.
7. **Confidence-routed escalation.** Score each item by validator flags, critic verdict, NLI margin, logprob margins on choice fields, voting agreement and speaker confidence. Route it to one of four outcomes:
   - auto-accept (`live_provisional` → `approved_auto`);
   - local re-critic;
   - **Claude audit**;
   - human.

   Also send a fixed **2% random sample** to Claude regardless of score, so drift is measured rather than assumed.
8. **Claude as teacher and auditor, not as pipeline.**
   - **Gold:** about 300 chunks (10–15 h from the pilot niches), labeled by Claude and *checked by Benjamin* (Topology Live's QUALITY §4 gold-set method), plus 2–3k Claude-labeled silver chunks.
   - **Audit:** 2% random plus all escalations.
   - **Weekly battery:** Claude reads a sample and proposes live questions (memo §7.4).
   - **Volume (ESTIMATE):** gold and silver ≈ 3,300 chunks × ~9k tokens ≈ 30M tokens once; audits ≈ 800–1,500 chunk-audits × ~8k ≈ 6–12M tokens over the backfill; weekly battery ≈ 0.2–0.5M tokens.
   - **Plan terms:** per Anthropic's support page (updated 2026-10-07), the Agent SDK and `claude -p` signed in with a plan draw from subscription limits, and Max/Team plans now include monthly API credits (amount not stated on the page). Size the teacher role against the actual remaining limits, and run labeling as batched Claude Code sessions rather than a background service.
9. **Distillation / LoRA on the box.**
   - Unsloth runs on Spark (NVIDIA playbook). gpt-oss-120b QLoRA uses about 68 GB. A gpt-oss-20b RL run did 1,000 steps in about 4 h.
   - NVIDIA's table reports peak LoRA throughput of about 7,000 tok/s (Llama 3.1 8B) and QLoRA of about 760 tok/s (Llama 3.3 70B). The same post's prose gives higher figures, so the source is internally inconsistent.
   - For a 20–35B model, assume **about 1,000–3,000 training tok/s** (ESTIMATE). A 3,000-example set at about 6k tokens is 18M tokens per epoch, which takes **about 2–5 h per epoch**, or overnight for 2–3 epochs.
   - **Targets:**
     - gpt-oss-20b, a proven Unsloth path on Spark;
     - Qwen3-30B-A3B or Qwen3.6-35B-A3B (MoE LoRA support on Spark is UNVERIFIED);
     - Qwen3.6-27B dense (slower to serve).
   - Gate each adapter on held-out gold: anchor precision, stance-source accuracy and neutral-rewrite fidelity. **Nothing is promoted on feel** (Topology Live `models.ts` rule).

### 5. Throughput math for this project (all ESTIMATES)

**Inputs:**

- 5,500–6,500 transcript hours (Data Model §2.9); mid case 6,000 h.
- Speech is 9–10k words/h × ~1.3 tokens/word ≈ **12–13.5k tokens per hour** (mid 12.5k).
- Corpus = 66–88M transcript tokens (mid **75M**).
- Chunks of about 2k fresh tokens + 0.5k overlap give about **7 chunks/h**, or **33k–44k chunks** in total.
- About 100 anchored claims per hour (range 60–150) gives about **600k anchors** for the backfill.
- The frozen system prompt, schema and examples (about 4k tokens) are **prefix-cached** in vLLM, so cached prefill is near-free. Count only fresh input.

**Per transcript hour:**

| Pass | Fresh input | Output (incl. reasoning) | Notes |
|---|---|---|---|
| P1 Extract (decomposed L1) | 7 × 3.5k = 24.5k (chunk + ~1k retrieved neighbor propositions; replaces Topology Live's full index) | 7 × 2k = 14k (range 10–21k) | Biggest output cost |
| P2 Critic (L2) | 7 × 3k = 21k | 7 × 0.8k = 5.6k | |
| P3 LLM tagging fallback | 20 items × 400 = 8k | 0.4k | Classifiers do the other 80% |
| P4 Dedup adjudication | 30 pairs × 500 = 15k | 30 × 60 = 1.8k | After embedding + rerank filter |
| Speaker-ID pass | ~3k per episode | 0.3k | ≈ per hour |
| **Total** | **≈ 70k (range 55–95k)** | **≈ 22k (range 16–36k; high = voting on part)** | ≈ 5.5× transcript tokens in |

**Backfill totals:**

- Fresh input ≈ 6,000 × 70k ≈ **0.42B tokens** (range 0.30–0.62B).
- Output ≈ 6,000 × 22k ≈ **132M tokens** (range 88–234M).

**Box throughput assumptions (sustained, ~7k-token contexts):**

| Model | Prefill | Aggregate decode |
|---|---|---|
| gpt-oss-120b | 1,500–3,000 tok/s | 250–600 tok/s at c ≈ 32–64 |
| 30–35B MoE | 3,000–6,000 tok/s | 500–1,200 tok/s |

KV fits: gpt-oss-120b's KV is about 40 KB/token, so 64 × 7k tokens ≈ 18 GB, within the room left after about 61 GB of weights. Prefill and decode share the GPU, so the times below are added together, which is conservative.

**Extraction wall-clock:**

| Model | Mid case | Range |
|---|---|---|
| gpt-oss-120b everywhere | 0.42B / 2,000 + 132M / 400 = 210k s + 330k s = 540k s ≈ **6.3 days** | ~2.9 days (low volume, fast) to ~15.6 days (high volume, slow) |
| 30–35B MoE extractor + 120b critic only | ≈ **3–4 days** | ~1.5–8 days |

These figures apply a ×1.0 operational factor. Add ×1.3–1.5 for retries, re-runs and maintenance windows.

**Per-hour unit cost:** about **90 s of box time per transcript hour** on gpt-oss-120b (70k / 2,000 + 22k / 400), or about **45 s** on a small MoE.

**Other backfill stages:**

| Stage | Volume | Rate (ESTIMATE) | Box time |
|---|---|---|---|
| Caption/publisher fetch | ~5,000+ h of items | Network- and rate-limit-bound | **3–6 weeks paced** (not box-bound; Data Model Phase 4) |
| ASR (Parakeet v3) | 1,500–6,000 h (captions primary → low end; all-audio → high end) | RTFx 300–1,000 | **2–20 h** |
| Diarization (community-1) | Multi-speaker items, ~1,500–3,000 h | RTF 0.02–0.05 | **30–150 h (1.3–6 days)**; CPU clustering overlaps LLM work |
| Speaker embeddings / enrollment | 542–770 landmarks × a few clips + per-episode segments | Fast | < 2 h |
| NLI gate | ~600k pairs (×1.5 with retries) | 100–300 pairs/s | **0.5–2.5 h** |
| Embeddings (Qwen3-Emb-4B) | 600k propositions + anchors + titles ≈ 20–40M tokens | 5–20k tok/s | **0.5–2 h** |
| Classification (GLiClass/SetFit, 5 tasks) | 3M item-task pairs | ≥ 1k/s | **< 1 h**, plus LLM fallback (counted in P3) |
| Fine-tuning (optional, between phases) | 2–3 epochs × 18M tokens | 1–3k tok/s | **5–15 h** |
| **Total box time** | | | **≈ 1–3 weeks continuous**, comfortably inside the 3–6 week paced acquisition window |

**Weekly refresh** (about 770 landmarks; the new-output hours sampled per landmark is a policy choice, OPEN-3):

| Sampled new hours/landmark/week | Hours/week | Extraction (90 s/h on 120b) | ASR + diarization (half multi-speaker) | Box time/week |
|---|---|---|---|---|
| 0.25 | ~190 | 4.8 h | ~0.2 + 2–5 h | **≈ 0.3–0.5 day** |
| 0.5 | ~385 | 9.6 h | ~0.4 + 4–10 h | **≈ 0.6–0.9 day** |
| 1 | ~770 | 19 h | ~0.8 + 8–19 h | **≈ 1.2–1.7 days** |
| 3 (B9's unverified figure) | ~2,310 | 58 h | ~2.3 + 23–58 h | **≈ 3.5–5 days**, so niche budgets are needed |

**Additional weekly work:**

- Daily pulse tagging: new anchors × live questions. Prefilter by embedding to the top 5 questions per anchor, then constrained choice. 20k anchors × 5 × 400 tokens ≈ 40M prefill ≈ **3–7 h/week**.
- Weekly re-clustering and snapshot: under 1 h.

**Electricity** (ESTIMATE): about 150–200 W average × 24 h ≈ 3.6–4.8 kWh/day, or about $0.5–0.7/day at $0.14/kWh. The backfill costs about $10–20 in power.

### 6. Orchestration and operations

**Pipeline = deterministic jobs, not an agent.** Every stage is an idempotent job keyed by `(item_id, stage, model_version, prompt_version)`. Its output is written as events and proposals, which fits the Data Model's event log and `LlmCall` table. Re-running a stage with a new model version creates a new version and never overwrites (Topology Live's `canonical.supersedes` pattern).

| Option | Fit | Verdict |
|---|---|---|
| **Procrastinate** (Python, MIT, Postgres 13+) | Periodic tasks, retries, task locks, queueing locks, priorities, async workers; lives in the *same* Postgres+pgvector the Data Model already chose; the ML stack (NeMo, pyannote, vLLM clients) is Python | **Recommended** for box-side stages |
| pg-boss (Node) | Same idea for the TypeScript app side (Topology Live is TS) | Use only if the worker stays in TS. Do not run two queues for one pipeline |
| Dagster | Asset lineage UI, partitions, backfills | Good but heavier; consider later if lineage views become a need |
| Prefect | Flows plus UI | Middle ground; needs its own server |
| Temporal | Durable workflows | Overkill at one box and one operator |

**GPU scheduling.** Hold one large model resident in vLLM. Swapping a 60 GB model costs minutes. Run in **phases**:

1. ASR + diarization phase: NeMo and pyannote containers.
2. LLM phase: vLLM with `--gpu-memory-utilization` ≈ 0.65–0.75, sharing the GPU with small resident models (embedder, reranker, NLI, classifiers, about 5–10 GB).

Leave about 15–20 GB for the OS, Postgres and page cache. A 30–35B MoE leaves room to run ASR alongside it.

**Recommended role for an open-source operator agent (Hermes Agent, Nous Research, MIT, v0.19 Jul 2026).** It has a cron scheduler, a Telegram/Slack/Signal gateway, skills, persistent memory, Docker/SSH sandboxes, and works with any OpenAI-compatible endpoint, so it can point at the box's own vLLM (gpt-oss-20b or the resident model).

- **Does:**
  - reads queue depth, failure rates, throughput, quality KPIs and disk/thermal status;
  - triages failed jobs (classifies the error, proposes a fix);
  - performs only allow-listed actions (re-queue job ids, pause or resume a queue, restart a container);
  - writes the daily and weekly operations report to Telegram and Parachute;
  - prepares Claude-audit and gold-review batches for Benjamin;
  - *proposes* threshold or config changes as diffs for approval.
- **Does not:**
  - decide what is extracted, accepted or published;
  - write to content tables;
  - hold credentials beyond a read-only DB role and the narrow action API.

This keeps the agent's errors out of the map.

**Scheduling horizons:**

| Horizon | Jobs |
|---|---|
| Daily (night window) | Poll RSS/playlists; paced caption fetch; ASR and diarization of new audio; extraction → critic → gates; daily pulse tagging; build the static snapshot; push; operations report |
| Weekly | Claude-led live-question battery from a sample (teacher role); coverage re-selection; 2% audit batch to Claude; clustering snapshot and lineage; weekly report |
| Monthly | Re-run dedup over the whole bank with the current embedder; re-evaluate models on gold (bake-off for new open releases); retrain classifiers on accumulated corrections and "that's not me" labels; backup **restore test**; prune transcripts past `retention_until` |

**Observability:**

- Prometheus + Grafana with node exporter.
- GPU metrics via `nvidia-smi`-based exporter. DCGM support on GB10 is UNVERIFIED.
- vLLM `/metrics` (queue time, TTFT, tokens/s, KV usage) and Postgres stats.
- A **quality dashboard** per model version: anchor exact/normalized/fuzzy match rates, NLI pass rate, critic reject rate, escalation rate, Claude-audit disagreement rate, and speaker-confidence distribution.
- Alerts go through the operator agent.

**Backups.**

- Postgres: WAL archiving plus nightly base backups (pgBackRest), encrypted, to off-box object storage (any S3-compatible bucket, or restic to a second disk plus cloud).
- Transcripts live in a private object store (MinIO on the box) with an off-box replica.
- Raw audio is deleted after ASR (B9). Word timestamps for anchored spans are kept permanently.
- Model weights and container images are pinned by digest.
- A monthly restore test is mandatory.
- Use a UPS. Remote admin goes over Tailscale/WireGuard only.

**Public site.** The box never serves the public. Each snapshot exports static JSON and HTML: propositions, ≤ 1-sentence quotes, deep links. The export is pushed to a static host (GitHub Pages, Cloudflare Pages or Vercel), which matches the publication rule (no full transcripts). Corrections and takedowns enter through the app, become jobs, and appear in the next snapshot.

### 7. Recommended stack

| Stage | Primary | Why | Fallback |
|---|---|---|---|
| Acquire | `youtube-transcript-api` paced + publisher transcripts + RSS enclosures (httpx) | Captions primary (B9 decision); RSS audio is download-intended | Paid transcript service for blocked channels; yt-dlp audio only where needed (risk register R49); landmark opt-in |
| Audio prep | ffmpeg → 16 kHz mono; Silero VAD | Standard; CPU (20 ARM cores) | — |
| ASR | **Parakeet TDT 0.6B v3** (NeMo, NGC container) | CC-BY-4.0; native word timestamps; RTFx 3,333 (A100); 3 h long-form mode; Spark container exists | **Canary-Qwen-2.5B** for hard audio (best WER 5.63); Whisper large-v3-turbo via faster-whisper (needs CTranslate2 build on sm_121) for non-European languages |
| Diarization | **pyannote community-1** | Better than 3.1; exclusive diarization for STT alignment; CC-BY-4.0 | NeMo Streaming Sortformer 4spk (≤ 4 speakers); `diarize` (Apache, CPU) |
| Speaker naming | Metadata + voiceprint (enrolled from solo content) + Topology Live `speaker_id` LLM pass + diarizer agreement | Highest-harm failure; reuse Topology Live's fusion and threshold | Operator confirmation queue |
| LLM serving | **vLLM** (Spark recipe container), prefix caching, structured outputs, MTP where available | Batching (Ollama does not batch); xgrammar JSON | SGLang; TensorRT-LLM for NVFP4 peak; llama.cpp for interactive tests |
| Extract (P1) | Bake-off: **Qwen3.6-35B-A3B** vs **gpt-oss-120b**; later a **LoRA-distilled** 20–35B | Small-active MoE = best tokens/s per quality on 273 GB/s; Apache 2.0 | Gemma-4-26B-A4B; Qwen3.5-122B-A10B (INT4, ~38 tok/s) for the hardest slice |
| Critic (P2) | A **different family** from the extractor (e.g., gpt-oss-120b) | Topology Live independence rule | Claude for escalations |
| Code gates | Topology Live validators + normalized/fuzzy-*locate* anchoring | Deterministic; no repair into spans | — |
| Entailment gate | **DeBERTa-v3-large mnli-fever-anli-ling-wanli** (MIT) | Fast, strong NLI | MiniCheck-DeBERTa/Flan-T5 (check license); LLM judge |
| Layer / stance / question tags | LLM constrained-choice + logprobs → distilled **GLiClass / SetFit / ModernBERT** | Local Jev equivalent with calibration | LLM fallback for low-confidence items |
| Embeddings | **Qwen3-Embedding-4B** (MRL → 1024-d, pgvector halfvec) | Apache 2.0; top MTEB; vLLM-served | BGE-M3; Qwen3-Embedding-0.6B for bulk |
| Dedup | ANN → **Qwen3-Reranker** → LLM equivalence adjudication | Polarity-safe | Claude adjudication on contested merges |
| Frontier | **Claude** (Max plan): gold labels, 2% audit + escalations, weekly battery | Teacher/auditor only | — |
| Fine-tuning | **Unsloth** in NGC PyTorch container (Spark playbook) | Proven on Spark (gpt-oss-20b/120b) | NeMo / PEFT + TRL |
| Queue | **Procrastinate** on Postgres + pgvector | Same DB as the data model; retries, cron, locks | pg-boss (if worker stays TS); Dagster later |
| Operator | **Hermes Agent** on local gpt-oss-20b | Cron, gateways, skills; kept out of the data path | Plain cron + email reports |
| Observability | Prometheus + Grafana + vLLM metrics + quality dashboard | Throughput *and* fidelity | — |
| Backups | pgBackRest/WAL + restic to off-box storage; monthly restore test | — | — |
| Public | Static snapshot export → static host | Box never public; publication rule | — |

### 7a. 30-day pre-arrival plan (no paid compute)

**Week 1: gold set and contracts.**

- Pick 10–15 h from the pilot niches (AI safety, e/acc, regen-ag). Fetch captions, publisher transcripts and RSS audio.
- In Claude Code sessions (subscription), label about 300 chunks with the Topology Live ontology. Benjamin checks them to make **gold v0**.
- Fix metrics per QUALITY.md: anchor precision, stance-source accuracy, neutral-rewrite fidelity, dedup precision and recall.
- Generate JSON Schemas from the Zod ontology.
- Port the L1 and L2 prompts to an **offline chunk mode**: local episode index plus retrieved neighbors instead of the full live index. Split L1 into the decomposed calls.

**Week 2: the deterministic skeleton.**

- Postgres + pgvector schema for Episode, Transcript, Segment, Anchor, Proposition, Stance, LlmCall and JobRun.
- Procrastinate tasks with idempotency keys and version stamps.
- An **OpenAI-compatible adapter** in `packages/llm`. It currently wraps only the Anthropic SDK, so add `base_url`-switchable local endpoints.
- A normalized and fuzzy-locate quote matcher, with property tests against ASR-style noise.
- Port the validators.

**Week 3: test on hardware already owned.**

- If the current Mac is Apple Silicon (Topology Live's capture uses `parakeet-mlx`):
  - run Parakeet (MLX) and pyannote community-1 on pilot audio to validate word timestamps, diarization reconciliation and speaker naming;
  - run gpt-oss-20b and Qwen3.6-35B-A3B through llama.cpp, MLX or Ollama for **prompt iteration on 10–15 min gold segments**. It is slow but adequate.
- Measure the first quality numbers against gold.

**Week 4: the cheap layers and operations.**

- Build and test the NLI gate, GLiClass zero-shot, a SetFit baseline and Qwen3-Embedding-0.6B dedup on CPU or the Mac.
- Write the box bring-up as code: compose files for the vLLM Spark recipe, the NeMo container, Postgres, MinIO, Prometheus and Grafana, plus a bootstrap script.
- Write a **day-1 benchmark script** (llama-benchy style: prefill, single-stream and c = 1/8/32/64 decode with real pilot prompts).
- Write the Hermes operator skeleton (read-only views, report template), backup scripts and the static export.
- Pre-download about 200–300 GB of weights to an external SSD.

**Arrival:**

- **Days 1–3:** bring-up and benchmarks. Replace every ESTIMATE in §5.
- **Days 4–10:** model bake-off on gold.
- **Week 2:** pilot run of 50–100 h, end to end.
- **Then:** the paced backfill.

---

## How this answers the governing question (layering + validation)

- **Layering.** The cheap, fast layers run on the box at full corpus scale: classifiers, embeddings and NLI handle the high-volume decisions. Generative extraction runs once per chunk, and Claude touches only a small, *measured* slice. Each layer's output carries its labeler and version, so the map can show "stated, gated and audited" separately from "inferred".
- **Validation.**
  1. A held-out, human-checked gold set scores every model and adapter before promotion.
  2. Deterministic anchor and NLI gates make a fabricated claim structurally hard to publish.
  3. A 2% random Claude audit measures drift continuously, with the disagreement rate shown on the quality dashboard.
  4. Landmark disputes and "that's not me" corrections feed back as labels.
  5. Cross-model agreement on the encounter set quantifies extraction uncertainty where it matters most.

## Reusable assets / design implications

- **Topology Live assets:**
  - `packages/ontology` (Zod → JSON Schema; validators, lexicons) is the shared contract between Claude and local models.
  - `pipeline/quotes.ts` gains a normalized/fuzzy *locator* that keeps the source substring as the quote.
  - `packages/llm/models.ts` already supports per-pass model overrides, so extend it with `base_url` and engine/version fields.
- **Data model additions:**
  - `LlmCall.engine`, `engine_version`, `quant`, `adapter_id`;
  - `Anchor.anchor_match` (exact / normalized / fuzzy);
  - `Proposition.gates` {validators, nli, critic, votes};
  - `QuestionLabel.calibration_version`.
- **The project no longer depends on a closed classifier.** Jev becomes optional: benchmark it against the local stack on the same gold set if it is ever used.

## Risks & open questions

- **Benchmarks are young and noisy.** Spark software changed fast through 2026, and kernel paths swing results by 10×. Day-1 measurement replaces the planning numbers.
- **Quality gap.** Open 30–120B MoE models may underperform Claude on neutral rewrite and stance-source nuance. Measure the gap on gold before scaling. If it is large, spend Claude on rewrite only, and keep local models for anchoring and tagging.
- **ARM/sm_121 friction:** source builds and pinned containers. An RTX PRO 6000 avoids most of it.
- **Sustained thermals** on small-form-factor GB10 units vary. Monitor clocks during multi-day runs.
- **Audio sourcing for diarization** of YouTube-only multi-speaker content raises the ToS exposure (R49).
- **Claude plan limits.** The teacher and audit volumes in §4 must fit the actual plan; the credit amounts are not stated on the page found.
- **Licenses.** Parakeet and pyannote are CC-BY-4.0, so attribution is required. Avoid Bespoke-MiniCheck-7B (non-commercial). Check Canary-Qwen and Gemma licenses before production use.
- **UNVERIFIED:** Dendro Logic's 256-stream figures (seen only via a secondary summary); pyannote GPU RTF; MoE LoRA on Spark for Qwen3.6; DCGM on GB10; GLiNER2 and BGE-M3 details (from knowledge).

## Sources

- NVIDIA DGX Spark product page and specs — https://www.nvidia.com/en-us/products/workstations/dgx-spark/
- LMSYS, "NVIDIA DGX Spark In-Depth Review" (2025-10-13) — https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark
- LMSYS, "Optimizing GPT-OSS on NVIDIA DGX Spark" (2025-11-03) — https://lmsys.org/blog/2025-11-03-gpt-oss-on-nvidia-dgx-spark
- ggml-org/llama.cpp discussion #16578, "Performance of llama.cpp on NVIDIA DGX Spark" — https://github.com/ggml-org/llama.cpp/discussions/16578 ; benchmark table — https://jetsonhacks.com/wp-content/uploads/2025/10/spark-llamacpp-bench.html
- NVIDIA Technical Blog, "How NVIDIA DGX Spark's Performance Enables Intensive AI Tasks" (2025-10-24) — https://developer.nvidia.com/blog/how-nvidia-dgx-sparks-performance-enables-intensive-ai-tasks
- NVIDIA Developer Forums, "Measured inference benchmarks on a single DGX Spark… Ollama, llama.cpp and vLLM" (2026-08-10) — https://forums.developer.nvidia.com/t/measured-inference-benchmarks-on-a-single-dgx-spark-same-harness-across-ollama-llama-cpp-and-vllm-notes-data-published/379766
- NVIDIA Developer Forums, "Qwen3.5-122B-A10B on single Spark: up to 51 tok/s" (2026-04-05) — https://forums.developer.nvidia.com/t/qwen3-5-122b-a10b-on-single-spark-up-to-51-tok-s-v2-1-patches-quick-start-benchmark/365639
- AEON-7, vllm-ultimate-dgx-spark wiki (2026) — https://github.com/AEON-7/vllm-ultimate-dgx-spark/wiki
- "DGX Spark GB10 decode/prefill bandwidth budget" (2026-06-08; secondary, cites Dendro Logic) — https://site-one-liart-13.vercel.app/en/dgx/dgx-spark-gb10-decode-prefill-bandwidth-budget-vllm-nemotron-nvfp4
- Spark Arena (community leaderboard) — https://sparkarena-readme.static.hf.space/README.md
- Spheron, "DGX Spark alternatives: Dell, ASUS, HP, Lenovo GB10 compared (2026)" — https://www.spheron.network/blog/dgx-spark-alternatives-dell-asus-hp-lenovo-gb10-compared-2026/
- NVIDIA RTX PRO 6000 Blackwell Workstation Edition — https://www.nvidia.com/en-gb/products/workstations/professional-desktop-gpus/rtx-pro-6000/
- Qwen3.6-35B-A3B summary (LLM Reference) — https://www.llmreference.com/model/qwen3.6-35b-a3b
- Context Studios, "Best open-weight LLMs 2026" — https://www.contextstudios.ai/guides/best-open-weight-llms-2026.md
- NVIDIA Parakeet TDT 0.6B v3 model card — https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
- Open ASR Leaderboard paper (arXiv 2510.06961 v3) — https://arxiv.org/html/2510.06961v3
- NVIDIA forum, Parakeet TDT v3 for DGX Spark (2026-04) — https://forums.developer.nvidia.com/t/multilingual-speech-to-text-stt-asr-with-nvidia-parakeet-tdt-0-6b-v3-for-the-dgx-spark/365554
- rappdw/transcribe-dgx (WhisperX on DGX Spark; build patches) — https://github.com/rappdw/transcribe-dgx
- pyannote speaker-diarization-community-1 — https://huggingface.co/pyannote/speaker-diarization-community-1
- diarize benchmarks — https://foxnosetech.github.io/diarize/benchmarks/
- NVIDIA Streaming Sortformer 4spk v2.1 — https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1
- WhisperX — https://github.com/m-bain/whisperx ; faster-whisper — https://github.com/SYSTRAN/faster-whisper
- Qwen3-Embedding-8B model card — https://huggingface.co/Qwen/Qwen3-Embedding-8B
- GLiClass modern-base v2.0 — https://huggingface.co/knowledgator/gliclass-modern-base-v2.0
- DeBERTa-v3-large-mnli-fever-anli-ling-wanli — https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli
- Bespoke-MiniCheck-7B (license CC BY-NC 4.0) — https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
- vLLM structured outputs (stable docs) — https://docs.vllm.ai/en/stable/features/structured_outputs.html
- Unsloth, "Fine-tuning LLMs with NVIDIA DGX Spark and Unsloth" — https://unsloth.ai/docs/blog/fine-tuning-llms-with-nvidia-dgx-spark-and-unsloth ; NVIDIA playbook — https://build.nvidia.com/spark/unsloth
- Procrastinate docs — https://procrastinate.readthedocs.io/en/stable/
- Hermes Agent (Nous Research) on PyPI — https://pypi.org/project/hermes-agent
- Anthropic support, "Use the Claude Agent SDK with your Claude plan" — https://support.claude.com/en/articles/15036540
- Internal: `design/DATA-MODEL-and-ENCOUNTER-PLAN.md` §1.2, §2.7–2.10; `design/DESIGN-MEMO-2026-10-30.md` §7; `wave-1/B9-…transcripts.md` §4; `wave-1/B4-mapping-science.md` §3 (Jev); `antidebate-live/docs/ARCHITECTURE.md` §2–3, §10; `packages/pipeline/src/quotes.ts`; `packages/llm/src/models.ts`
