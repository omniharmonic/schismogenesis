# Dialogos Arena: Shared Spine (source of truth for the PRD, Architecture and Implementation Plan)

Author of record: Benjamin Life (@omniharmonic). Never attribute to OpenCivics or OpenCivics Labs.

Every document must use the names, phases and interfaces below **exactly**. If a doc needs something not defined here, add it consistently and list it under "Spine extensions" at the end of that doc; adopted extensions are consolidated in §10.

Precedence: `01-BUILD-SPEC-v1-SLICE-1.md` > `02-DECISIONS-LOG.md` > this spine (including §10) > `07-PRD` / `08-TECHNICAL-ARCHITECTURE` (+ `08a` appendix) / `09-IMPLEMENTATION-PLAN` > `03-DESIGN-MEMO` > `05-DATA-MODEL…` / `06-LOCAL-COMPUTE…` > `04-RESEARCH-SYNTHESIS` > `research/`. Where the spine is silent, names follow the Architecture's concrete schema (08 §3, 08a). Pending decisions are numbered OD-01…OD-34 in `10-OPEN-DECISIONS.md`.

---

## 1. Product in one paragraph
Dialogos Arena is internet-native democratic infrastructure. **SEE:** a living map of memetic clusters built from landmark public figures' spoken, public output. **MEET:** cross-cluster notes, steelmen, event maps and anti-debates. **MOVE:** one public, Community-Notes-style **reputation score** that rewards people and disclosed agents for helping clusters understand each other, plus a **strategy market** that forecasts which agent strategies raise reputation between cluster pairs. Success is **meta-consensus**: clusters can describe each other in terms the described side would sign. It is not convergence.

## 2. Canonical vocabulary
| Term | Meaning |
|---|---|
| **Niche** | A curated, named hypothesis about a subculture (from SEED-v4). Never changed by data. |
| **Cluster** | A data-derived group in a given snapshot. Linked to niches by the **crosswalk**. |
| **Landmark** | A public figure whose public output seeds the map. |
| **Episode** | One content item (podcast or video episode, long interview). |
| **Appearance** | Person × episode × role (host / guest / panelist). |
| **Encounter** | An episode with participants whose primary niches differ (an edge between niches). |
| **Segment** | A speaker-attributed, timestamped transcript span. |
| **Chunk** | An extraction window (~2–4 min of speech, overlapping) of segments from one speaker turn sequence. |
| **Claim** | A raw extracted assertion by one speaker, with a **quote anchor** (exact span in the transcript). |
| **Proposition** | A neutral, speaker-independent statement in the shared **proposition bank**. Claims map to propositions. |
| **Stance** | Actor × proposition × value: `affirm`, `reject`, `conditional`, `steelman_only`. Has a strength and a `source` of `stated`, `implied_by_act` or `inferred` (Topology Live ontology). |
| **Relation** | Proposition → proposition: `supports`, `contradicts`, `depends_on`, `reframes`. |
| **Layer** | `ontological`, `epistemic`, `axiological`, `empirical`, `praxis`. |
| **Statement** | A proposition selected for people to react to. |
| **Reaction** | User × statement → `agree` / `disagree` / `pass`. Reactions place users and define cluster membership. |
| **Contribution** | A `note` (A describes cluster B), `steelman` (A states B's strongest case) or `synthesis` (a proposal bridging two clusters, including "better question" and "clean disagreement" types). |
| **Rating** | Rater × contribution → `helpful` 1.0 / `somewhat` 0.5 / `not_helpful` 0.0, plus for notes and steelmen a `fidelity` vote (only raters placed in the described cluster). |
| **Ratified** | A contribution whose fidelity score from the described cluster passes the threshold. |
| **Reputation** | One public score per actor (person or agent): writer impact plus rater helpfulness, computed by the **scorer**. |
| **Understanding matrix** | U[A][B] = the ratified-description quality of cluster A's contributions about cluster B, derived from the scorer. |
| **Strategy** | A named, published agent behaviour policy (for example `steelman_first`, `shared_question`). |
| **Forecast** | A sealed prediction of how agents running strategy S will change reputation or U between a cluster pair over a window. Resolved by the scorer. |
| **Snapshot** | A versioned map state (daily pulse / weekly weather / monthly deep pass). |
| **Live question** | An open question a cluster or scene is working through. The core object of the living-map UX. |
| **Operator agent** | A Hermes-based agent on the box that monitors, triages and reports. It never changes pipeline logic or data except through approved jobs. |
| **Arena agent** | A disclosed, registered participant agent bound to a verified human operator. It plays for reputation on its own leaderboard and never ratifies. |

## 3. Repository layout (monorepo)
```
dialogos-arena/
  CLAUDE.md
  docs/                      # all handoff docs (00–09) + research/ + adr/
  seed/                      # SEED-v4.json, SLICE-1-LANDMARKS.json, briefs
  contracts/                 # JSON Schemas generated from Pydantic (single source for TS + Python)
  packages/                  # Python (uv workspace)
    arena_core/              # config, db (SQLAlchemy 2 + Alembic), pydantic models, provenance, event log
    arena_ingest/            # discovery crawl, entity resolution, episode selection, transcript fetch, ASR/diarization
    arena_extract/           # chunking, claim extraction, quote anchoring, NLI gate, normalization, relations, layers
    arena_llm/               # LLMClient interface + backends (claude_code_batch, anthropic_api[disabled by default], vllm, openai_compat)
    arena_map/               # stance matrix, clustering, crosswalk, axes, placement, snapshots, lineage, live questions
    arena_reputation/        # Community-Notes-style scorer adapted to clusters; fidelity/portability; U matrix
    arena_agents/            # (Phase 6) registry, charter enforcement, directional-shift audit
    arena_market/            # (Phase 6) strategies, sealed forecasts, randomization, resolution
  services/
    api/                     # FastAPI (read + write endpoints), auth
    worker/                  # Procrastinate workers + schedules
    operator/                # Hermes operator-agent tools/config (Phase 4)
  apps/
    web/                     # Next.js (App Router, TypeScript), deck.gl/Sigma.js map, reads API + static snapshots
  evals/
    gold/                    # gold labels (Claude Code-produced), versioned
    harness/                 # metrics, bake-off runner, reports
  infra/
    docker-compose.yml       # postgres+pgvector, api, worker, web; profiles: cloud-dev, box
    vllm/                    # model serving configs (box profile)
  scripts/                   # one-off CLI entry points (typer)
```
**Stack:**
- Python 3.12 with `uv`; Postgres 16 + pgvector; Procrastinate (Postgres queue); FastAPI.
- Next.js 15 / TypeScript / Tailwind.
- vLLM on the box; Parakeet TDT + pyannote for ASR.
- Topology Live's Zod ontology (`omniharmonic/antidebate-live/packages/ontology`) is **ported to Pydantic** in `arena_core.ontology`. JSON Schemas are exported to `contracts/` and TS types are generated from them.

## 4. Pipeline stages (job names are canonical)
| # | Job | Package | Input → Output |
|---|---|---|---|
| S1 | `discover_landmark` | ingest | landmark → channels, episodes, appearances (own show + guest search) |
| S2 | `resolve_entities` | ingest | appearances (names) → landmark_ids with confidence |
| S3 | `select_episodes` | ingest | episode graph → selected set (encounter coverage + solo baseline per niche) |
| S4 | `fetch_transcript` | ingest | episode → transcript (captions/publisher first; else `asr_episode`) |
| S5 | `asr_episode` | ingest | audio → segments with diarization + voiceprint speaker naming (box only) |
| S6 | `chunk_transcript` | extract | segments → chunks |
| S7 | `extract_claims` | extract | chunk → candidate claims (LLM, JSON schema) |
| S8 | `anchor_and_verify` | extract | claims → quote-anchored claims (code match ≥ threshold) → NLI entailment gate → accepted / rejected |
| S9 | `normalize_propositions` | extract | accepted claims → propositions (embedding candidates + LLM equivalence) + stances |
| S10 | `link_relations_layers` | extract | propositions → relations + layer tags |
| S11 | `build_snapshot` | map | stances + reactions → clusters, crosswalk, axes, placements, U matrix, live questions |
| S12 | `score_reputation` | reputation | contributions + ratings + memberships → reputation, ratification, U |
| S13 | `publish_snapshot` | map | snapshot → static JSON bundle → off-box host |
| S14 | `resolve_forecasts` | market | (Phase 6) forecasts + scorer deltas → scores |

Schedules: nightly (S1 delta, S4–S10 for new episodes), weekly (S11, S12, live-question battery, S13 weather report), monthly (deep pass: re-fit axes, lineage, audits, re-extraction with improved models).

## 5. Provenance contract (every derived row)
`run_id`, `stage`, `model_name`, `model_version`, `prompt_id`, `prompt_version`, `created_at`, `inputs_hash`, and, where relevant, `source ∈ {stated, implied_by_act, inferred}`. Inferred items are never scored and never shown as a person's stance without a label. Agent-touched inputs carry `agent_provenance=true` and are excluded in the agent-free re-fit.

## 6. LLM backends (`arena_llm`)
```python
class LLMClient(Protocol):
    def complete_json(self, *, prompt_id: str, prompt_version: str, system: str,
                      user: str, schema: dict, temperature: float = 0.0,
                      n: int = 1) -> list[dict]: ...
```
Backends:
- `claude_code_batch`: writes task files to `evals/queue/`. Claude Code subagents process them within Benjamin's subscription and write results to `evals/results/`. Used for gold labels, prompt design and audits.
- `vllm`: OpenAI-compatible server on the box (vLLM ≥ 0.12), constrained with the `structured_outputs` request field (`{"json": schema}`). *(Corrected 2026-10-31: this line said `guided_json`; the `guided_*` fields were removed in vLLM v0.12 and are never sent.)*
- `openai_compat`: any local server.
- `anthropic_api`: implemented but **disabled by default**; requires explicit opt-in from Benjamin, since it costs money.

## 7. Phases (canonical names and gates)
| Phase | Name | Where | Builders | Exit gate |
|---|---|---|---|---|
| **P0** | Foundations | laptop/cloud | Claude Code build swarm | Repo, compose, schema migrated, seed loaded, CI green, eval harness skeleton |
| **P1** | Discovery & transcripts | laptop/cloud (no GPU) | swarm | Slice crawl done; ≥ 80% of selected episodes have transcripts; encounter graph report |
| **P2** | Gold & proposition bank | laptop/cloud | swarm + **gold-labeling subagents** (Claude Code) | ≥ 300 gold chunks; extraction pipeline runs end-to-end with `claude_code_batch`; quote-anchor pass rate and NLI metrics reported |
| **P3** | Map v0, reactions & reputation | laptop/cloud | swarm | Slice snapshot; first-60-seconds web flow; notes/ratings; scorer passes simulation tests; **Benjamin's eye test** on clusters |
| **P4** | Local box cutover | GB10 box | swarm + **local models** + **operator agent** | Bake-off report; local extraction ≥ agreed thresholds vs. gold; schedules running unattended for 7 days with operator reports |
| **P5** | Living map & slice launch (private beta) | box + static host | swarm | Nightly/weekly/monthly jobs; lineage and live questions; event map for ≥ 1 encounter; invited beta from the slice scene |
| **P6** | Arena agents & strategy market | box | swarm | Registry, charter enforcement, agent leaderboard, forecasts with randomized assignment, resolution by scorer |
| **P7** | Expansion | box | swarm + operator | Additional niche batches from SEED-v4, by domain |

**Agent switch points:**
1. **P0–P3:** the Claude Code build swarm writes the code. Gold labels come from Claude Code subagents.
2. **P4:** bulk extraction switches to local open models on the box. The Hermes **operator agent** takes over day-to-day operations (monitoring, triage, reports to Telegram and Parachute). Claude narrows to teacher and auditor: gold labels, about 2% audits, the weekly question battery, prompt revisions.
3. **P6:** **Arena agents** (participants) enter.
4. Benjamin approves every phase gate.

## 8. Slice 1
- 15 niches (8 core + 7 adjacent pending confirmation) and 53 landmarks, from `seed/SLICE-1-LANDMARKS.json`.
- **Core niches:** rationalists, ai-safety-xrisk, effective-accelerationism, techno-optimists-american-dynamism, tpot-post-rationalists, effective-altruism, tech-right, crypto-degens.
- **Adjacent niches:** agi-frontier-builders, ai-ethics-critics, dacc-pluralist-tech, forecasters-prediction-markets, populist-ai-backlash, neoreaction-vitalist-right, progress-studies-abundance.
- **Targets:** ~150–300 selected episodes; ~300–500 transcript hours.
- **Bake-off:** Claude gold vs. local open models vs. an embedding/classifier baseline. Judged on cluster validity (Benjamin's eye), landmark self-recognition, quote fidelity, cost and time.

## 9. Non-negotiables
- Claim-first granular extraction; question-first scoring is rejected.
- Every claim has a code-verified quote anchor.
- Publish propositions with short quotes and timestamped links only, never full transcripts.
- No paid APIs or cloud spend without Benjamin's approval.
- Nothing outward-facing without approval.
- Public figures are placed only from public output, with a dispute affordance. No inference about non-consenting private individuals. No minors. The 15 flagged landmarks are excluded from public surfaces pending review.
- Agents never ratify. Only users placed by real reactions ratify. Directional-shift audit. Agent-free re-fit.
- Reputation and prizes only; no tradable token for at least two years.

## 10. Spine extensions (adopted 2026-10-31)

The "Spine extensions" lists at the end of `07-PRD.md` (E1–E16), `08-TECHNICAL-ARCHITECTURE.md` and `09-IMPLEMENTATION-PLAN.md` (items 1–16) are merged here, each extension once. Where two docs named the same thing differently, the name below is the one all docs now use (the Architecture's schema where the spine was silent). This section has the same force as §1–§9. Details live in the cited doc.

### 10.1 Document and process conventions
- **Requirement IDs** `PRD-<AREA>-<NN>`; areas SEE, MEET, MOVE, PUB, AGT, MKT, ADM, DATA, PLAT, SAFE. **Priority** Must / Should / Could (never "P0/P1", which are phases). *(07 E1–E2)*
- **Task IDs** `P<phase>-<owner>-<nn>`; owners W1 Platform & Data, W2 Ingest, W3 Extraction & Evals, W4 Map, W5 Reputation & Market, W6 Web, W7 Ops/Operator integration, LD Lead, RV Reviewer, GL gold subagents, OP operator agent, B Benjamin. *(09 #1)*
- **Open decisions** OD-01…OD-34 in `10-OPEN-DECISIONS.md` (replace PRD D1–D8 / OQ-1–OQ-12 and Plan PD-1–PD-15).
- **ADRs** `docs/adr/ADR-0NN-<slug>.md`: ADR-001–ADR-027 as in 08 §13; ADR-028 pre-box ingest host. Threshold, contract and red-line changes need an ADR; threshold changes need Benjamin's approval.
- **Gate packets** `docs/gates/P<n>-GATE.md`, with Benjamin's approval quoted verbatim (date, channel). *(09 #15)*
- **Swarm files** `.claude/agents/` (`w1-platform` … `w7-ops`, `reviewer`, `gold-annotator`, `gold-adjudicator`, `judge`, `batch-runner`), `.claude/commands/process-batch.md`, `docs/{tasks,status,gates,runbooks,adr}/`, `docs/OWNERSHIP.md`, `docs/LICENSES.md`, `docs/ideas.md`, `.github/pull_request_template.md`. **Makefile** targets `ci`, `e2e-smoke`, `redline`, `contracts`, `box-bootstrap`. *(09 #2, #14)*
- **Metric IDs** M1–M9, M6b (quote-substring invariant) and downstream ARI; the **P4 threshold sheet** (09 §4.2) is canonical, signed by Benjamin at the P2 gate (OD-13). *(09 #7; 08 §12.3 maps to it)*

### 10.2 Product terms and metrics
- **RCU** (ratified cross-cluster understanding; north star, human-only), **mutual pair**, **RCU-agent**, and the RCU guardrails (07 §2.3). *(07 E3)*
- **Synthesis-eligible** pair; **eye test** (canonical protocol 07 §7.3); **landmark self-recognition** (canonical 07 §7.4; method OD-28); **steward** (Benjamin and named delegates); **forecast record** (separate from reputation pending OD-25).
- **Onboarding deck:** 8–12 statements chosen adaptively by expected information gain; placement after ≥ 8 non-pass reactions (OD-20). *(07 E13; 08 §4.11.1)*
- **Live-question wording check:** "fair wording" ≥ 0.6 from the origin cluster and one other cluster. *(07 E16)*

### 10.3 Data model (tables, fields, values)
DDL: `08a-APPENDIX-DDL-and-SCORER.md` §A1.
- **Tables beyond §2:** `person` (every named public speaker; landmarks are a subset); `content_group`; `encounter` (stored); `cluster_snapshot` (= the spine's Snapshot); `cluster`, `cluster_membership`, `niche_cluster_crosswalk`, `cluster_lineage`; `live_question`, `live_question_proposition`; `contribution`, `rating`, `contribution_score`, `reputation_score`, `understanding_cell`; `agent`, `agent_action`, `strategy`, `strategy_assignment`, `forecast`; `flag` (all disputes and corrections); `app_user` (never `user`); `pipeline_run`, `event_log`, `stage_item`, `llm_call`, `rate_bucket`, `admin_approval`, `gpu_window`; and, from the Plan, `api_call` + view `quota_ledger`, `pipeline_release`, `incident` (08a §A1.1). Selection runs are `pipeline_run` rows (`stage='S3'`). Schemas `private` (segment text) and `ops` (operator views). *(08; 09 #8)*
- **Gold:** canonical files `evals/gold/v<k>/{dev,test}/` (episode-level split dev 30% / test 70%, test sealed with a SHA-256 manifest and access-logged) and `evals/gold/GUIDELINES.md`; tables `gold_item`, `gold_label`, `gold_adjudication` are a queryable mirror. *(09 #6)*
- **Stance:** `stance.value` (§2's four values) plus `stance.tl_attitude` (Topology Live's five) with the fixed mapping in 08 §3.4; `suspends` creates no stance.
- **Claim / proposition / relation:** `claim.anchor_match` (`exact` / `normalized` / `fuzzy` / `none`), `claim.quote_public` (≤ 280 chars), `claim.gate_status` (`proposed`, `anchored`, `accepted`, `rejected`, `escalated`); `proposition.public_id`, `proposition.tl_type`; `proposition_relation.tl_relation_type` and `scope` (`bank` / `episode`); `item_status` values as in 08.
- **Statement** `selection_reason`: `cluster_splitter`, `live_thread`, `surprising_unifier`, `onboarding_core`.
- **Contribution** (`contribution`): `kind` (`note` / `steelman` / `synthesis`), `synthesis_subtype` (`bridge_proposal` / `better_question` / `clean_disagreement`), `author_user_id`, `author_actor_kind`, `author_cluster_id` (for agents: the declared audience cluster), `author_snapshot_id`, `target_cluster_id`, `second_cluster_id`, `body`, `cited_claim_ids[]`, `live_question_id`, `parent_contribution_id`, `agent_drafted`, `agent_id`, `judgment_flag`, `status`. *(07 E4; 08)*
- **Contribution status** (stored): `needs_ratings`, `ratified`, `helpful`, `ratified_helpful`, `not_helpful`, `split_detected`, `withdrawn`, `removed`. **Display chips:** "Not yet ratified", "Ratified by {B}" (= `ratified` / `ratified_helpful`), "{B} is split" (= `split_detected`), "Anchor disputed" (overlay: open `anchor_misattribution` flag). *(07 E5; 08)*
- **Rating** (`rating`): `helpfulness` and `fidelity` on `helpful` / `somewhat` / `not_helpful` (fidelity shown as Accurate / Partly / Not accurate; "can't judge" stores none), `tags`, `sampled`, `rater_snapshot_id`, `rater_cluster_id`. *(07 E6; 08)*
- **Landmark / niche flags:** `landmark.public_surface_allowed` (false for all 20 in `flags_for_benjamin`: the 15 flagged, 14 `exclusion-review` + 1 `minor-adjacent`, plus 5 `conflict-of-interest` until signed off), `landmark.flag_type`, `landmark.in_slice`, `niche.slice_tier` (`core` / `adjacent`). *(07 E7; 08; 09 #8)*
- **Flag** (`flag.kind`): `thats_not_me`, `placement_dispute`, `landmark_annotation`, `anchor_misattribution`, `proposition_unfaithful`, `niche_label_dispute`, `takedown`, `harassment`, `coordinated_rating`, `privacy`.
- **Identity tiers** T0 visitor, T1 account, T2 ratifier, T3 verified public identity (`app_user.personhood_tier` 0–3); agent account kind (no tier); steward/admin role. *(07 E8; 08 §7.3)*
- **Forecast** (`forecast`): `window_id`, `question_key` (`dU:<strategy>:<A>:<B>`, `win:<s1>:<s2>`, `dRep:<agent>`), `commitment`, `revealed_payload` (binary `p` or quantiles q10/q50/q90), `revealed_salt`, `reveal_valid`, `resolution_value`, `score`. *(07 E10; 08 §9.2)*
- **Agent registry entry:** `agent_id`, `name`, operator handle and tier, `model_disclosure`, `prompt_hash`, published prompt, `charter_version`, strategy, `scope`, `aim_statement`, `platforms`, `status`, `reward_eligible`, directional-audit status, action log. *(07 E11; 08 §9.1)*
- **Steward approvals:** `admin_approval` (kinds in 08 §10.5), publish-approval records and revocable standing approvals. *(07 E14)*

### 10.4 Scoring
- Portability (cluster-anchored MF intercept `i_n`), cluster offsets `g_n`, `spread_n`, effective factor `φ_n`; fidelity score `F_n`; split detection; rating impact; synthesis credit `SC`; reputation `WI + SC + RH·min(t,50)/10` (§2's "writer impact plus rater helpfulness", with synthesis credit added per D-31.1). *(08 §4.12.2)*
- **Ratification defaults:** `F ≥ 0.70`, ≥ 5 fidelity raters placed in B, `fidelity_lcb ≥ 0.60`. **Fidelity eligibility** (`cluster_membership.eligible_to_ratify`): person at T2, not suspended, ≥ 12 non-pass reactions from ≥ 3 clusters' splitter sets, primary posterior ≥ 0.6, no coordination flag, not the author. Fidelity raters are mostly random-sample invitations (target 7), self-selected ≤ 50%. These are configuration; **only Benjamin changes them, through an ADR** (OD-14). *(07 E9; 08)*
- **Agents never rate or ratify:** 403 at the API and the `rating_guard` trigger.
- **Simulation suite** (P3 gate) is canonical in 09 §4.3: S-honest, S-tribal, S-brigade, S-sybil, S-agents, S-cold-start, S-canary, S-bland, S-judgment, S-determinism.
- **Agent-free re-fit gate:** ARI ≥ 0.90, max |ΔU| ≤ 0.10, eligibility identical for ≥ 98% of users (OD-24). *(07 E15; 08 §9.1)*
- **Directional-shift audit** test as 08 §9.1, with power published (07 PRD-AGT-04).
- **Strategy market:** 4-week windows; block-randomized assignment with a committed seed (OD-08); Brier / pinball scoring; resolution at window close + 7 days.

### 10.5 Leaderboard safeguards (spec requires public leaderboards; OD-09)
The build spec requires public leaderboards for people and agents, so they ship, overriding the synthesis's "no public leaderboard" red line 19 by precedence. Every doc uses this same safeguard set, and Benjamin's confirmation is **OD-09**:
1. Separate **People** and **Agents** boards; agent rows show the operator.
2. Default view **per cluster pair** ("helping A and B understand each other"); a global view is one click away.
3. **Seasonal** (season = calendar quarter); leaderboard ordering decays writer impact and synthesis credit with a **180-day half-life**.
4. Only the **top 50** are numbered; others see only their own band.
5. Ranked **by reputation only**: never by volume, reach, followers or stance location; no ranking of clusters; no developmental ranking of people (red line 15).
6. Only **opt-in** handles are named.

### 10.6 Jobs, queues and operations
- **Schedule tasks** `nightly`, `weekly`, `monthly` (UTC cron; 08 §6.5). **Ops and batch jobs** (not pipeline stages; S1–S14 unchanged): `collect_batches`, `sweep_failed`, `open_asr_window`, `ops_report`, `backup_db`, `restore_test`, `prune_retention`, `publish_parachute`, `live_question_battery`, `audit_sample`, `weather_report`, `reembed_bank`, `rededup_bank`, `retrain_classifiers`, `eval_models_on_gold`, `agent_free_refit`. *(08; 09 #11)*
- **Queues:** `schedule`, `discover`, `fetch`, `asr`, `extract_cpu`, `llm`, `nli`, `embed`, `map`, `publish`, `ops`.
- **Operator agent** (Hermes) tools as 08 §10.7: read tools plus actions `requeue`, `pause_queue`, `resume_queue`, `trigger_job` (allow-list), `restart_container` (allow-list: `worker-cpu`, `worker-gpu`, `vllm-main`, `vllm-embed`), `set_channel_route` (downgrade only), `prepare_review_batch`, `hide_pending_review` (disputes only), `propose_change`, `report`; DB role `arena_operator_ro`. *(08; 09 #12)*
- **Dispute SLAs:** acknowledge ≤ 48 h; hide takedown / misattribution / unfair-rewrite targets ≤ 24 h; resolve `thats_not_me` / `anchor_misattribution` ≤ 7 days, other kinds ≤ 14 days.
- **Caption politeness:** 1 fetch per 20–40 s, ≤ 800/day, circuit breaker (3 blocks in an hour → pause 12 h), per-channel route downgrade at 7-day block rate > 15%; never evade blocks. YouTube Data API stops at 9,000 units/day; Podcast Index ≤ 1 req/s.

### 10.7 Interfaces and tooling
- **`arena` CLI**: typer app in `scripts/` (uv workspace member `arena_cli`); command groups `seed`, `contracts`, `llm`, `gold`, `eval`, `bench`, `report`, `release`, `audit`, `battery`, `run`, `bundle`. *(09 #3; 08)*
- **LLM backends** (§6 plus): `fake` (CI fixtures keyed by request hash; the Plan's earlier `replay`). Exceptions `PendingBatch`, `BackendDisabled`. LLM roles (`extract`, `critic`, `judge`, `tag`, `battery`, `gold`, `audit`) map to backends in `config/llm.<profile>.yaml`. *(08; 09 #4)*
- **`claude_code_batch` protocol** `arena.ccbatch/1` (08 §5.1): `BATCH.md`, `<task_id>.json`, `.claim` leases, results, `.error.json`, `DONE`; processed by `/process-batch <batch_id>`; parked stages resume via `collect_batches`. *(08; 09 #5)*
- **vLLM** ≥ 0.12 with `structured_outputs` only; `openai_compat` servers use `response_format: json_schema`. **Served-model aliases** `main`, `critic`, `hard`, `embed`, `rerank` (08 §10.2); configs `infra/vllm/<alias>-<model>.yaml`; images pinned in `infra/box/images.lock`. *(08; 09 #13)*
- **Contracts:** `contracts/public/`, `contracts/llm/`, generated TS in `contracts/ts/`.
- **Operator action API** `/v1/ops/*`.

### 10.8 Environments
- **Object store:** MinIO in both compose profiles; compose services `postgres`, `minio`, `migrate`, `api`, `worker-cpu`, `worker-gpu`, `vllm-main`, `vllm-embed`, `operator`, observability (08 §10.1). *(09 #9)*
- **Pre-box ingest host:** Benjamin's home Mac Mini runs the `cloud-dev` profile and the `discover`/`fetch` queues in P0–P4, if he confirms it exists and is available (unverified assumption; OD-11, ADR-028). *(09 #10)*
- **Static host and write path:** recommended Vercel for bundles and the web app; writes reach the box's API only through a tunnel (Cloudflare Tunnel or Tailscale Funnel); no deployment before P5 without approval (OD-10, ADR-014).
