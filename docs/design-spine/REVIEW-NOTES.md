# Cross-document consistency review: fixes made

*Review of 2026-10-31 · author of record for the package: Benjamin Life (@omniharmonic) · reviewer: independent Claude Code agent*

Scope: `design-spine/SPINE.md`, `01`, `02`, `CLAUDE.md`, `00-README.md`, `07-PRD.md`, `08-TECHNICAL-ARCHITECTURE.md`, `09-IMPLEMENTATION-PLAN.md`. Rule applied: align to the spine; where the spine is silent, align 07 and 09 to 08's concrete schema. A pre-review copy of every file was kept outside the package for diffing.

## A. Structure (tasks 2, 4, 5, 6)
1. **SPINE §10 added** ("Spine extensions (adopted 2026-10-31)"): the 07 (E1–E16), 08 and 09 (1–16) extension lists merged once each, with the reconciled names.
2. A "consolidated in SPINE §10" note added at the top of the extensions section in 07, 08 and 09; the 07 and 09 lists were rewritten to the reconciled names (each change noted per row).
3. **`10-OPEN-DECISIONS.md` created**: 34 decisions (OD-01 … OD-34) with question, options, recommendation, blocks and needed-by date, plus an old-ID cross-reference.
4. `02-DECISIONS-LOG.md` "Pending decisions" now points to `10`, with the old 1–7 → OD-01…07 mapping; D-31.2's open item tagged OD-08.
5. PRD §9.4/§9.5 (D1–D8, OQ-1–OQ-12) replaced by an OD table and cross-reference; "pending decision 2/6" and "Pending decisions 1, 2 and 5" replaced by OD-IDs.
6. Plan §8 (PD-1–PD-15, OPEN-n) replaced by an OD table and cross-reference; all 29 in-text `PD-n` references rewritten to OD-IDs; OPEN-1/2/3/6/9 references annotated with OD-29…33.
7. Architecture: OD cross-references added (OD-08, 09, 10, 11, 13, 14, 16, 24, 25, 28, 32, 34) in the conflict list, §1–§4, §7, §9, §12 and ADRs.
8. **`08a-APPENDIX-DDL-and-SCORER.md` created**: full DDL (786 lines) and full scorer code (`cluster_mf.py`, `scorer.py`), `coordination.py` and `test_scorer_sim.py`, moved verbatim (verified by exact-substring check). 08 keeps a tables-by-group index, the enums, `contribution`, `rating_guard` and `combined_status` excerpts, with links. 08 fell from ~31.8k to ~25.9k words.
9. `CLAUDE.md` read order now: 01, 02, SPINE, 10, 07, 08 (+08a), 09, seed; precedence stated.
10. `00-README.md` file table adds SPINE, 07, 08, 08a, 09, 10 and this file, and states precedence.
11. Precedence line made identical in SPINE, 02, 07, 08, 09, CLAUDE.md and README: spec > decisions log > spine > PRD/architecture/plan > design memo > data model/local compute > synthesis > research.

## B. vLLM structured outputs (task 1)
12. SPINE §6 corrected: `vllm` uses the `structured_outputs` request field (vLLM ≥ 0.12); `guided_json` was removed in v0.12.
13. 08: the `legacy_guided` → `guided_json` fallback removed from text and from the `VLLMClient` code; conflict note, §5.2, ADR-016 and extensions now say "never sent".
14. 09 §2.5 and §4.4 say `structured_outputs` only (with `response_format: json_schema` only for `openai_compat` laptop servers); CLAUDE.md build step 7 says the same.

## C. Leaderboard conflict (task 3)
15. One safeguard set (SPINE §10.5) stated identically in 07 MOVE-03 (AC7 opt-in handles and "no cluster/developmental ranking" added), 08 (conflict note, §4.12.2 reputation, `/v1/leaderboards` changed from top 100 to top 50 per pair), and 09 (P5-W6-01, P6-W5-03). Open question **OD-09** (merges PRD OQ-8 and OQ-12).

## D. Names, enums and fields aligned to 08's schema
16. Landmark visibility: 07 `public_visibility` (public/excluded_pending_review/withheld) and 09 `public_exclusion` → 08 `landmark.public_surface_allowed`; `flag_type` values hyphenated (`exclusion-review`).
17. Excluded set made consistent: all **20** `flags_for_benjamin` entries (15 flagged + 5 COI) start with `public_surface_allowed = false` (08 DDL comment, §11.1, §12.1, extensions and sources previously said 15).
18. Slice marks: 09 `landmark.slice_tier` → `niche.slice_tier` + `landmark.in_slice`.
19. Contribution: 07 `contribution_type`, `author_actor_id/type`, `cited_anchor_ids`, `text` → `kind`, `author_user_id`, `author_actor_kind`, `cited_claim_ids`, `body`.
20. Synthesis subtype `third_position` → `bridge_proposal`.
21. Contribution status: 07 stored values (`not_yet_ratified`, `ratified_by_B`, `B_split`, `anchor_disputed`) → 08 statuses; the 07 labels kept as display chips (MEET-05 AC1); RCU and writer-impact text updated.
22. Agent audience: 07 `audience_cluster_id` → `author_cluster_id` holds the declared audience for agents (comment added to 08 DDL).
23. `judgment_flag` column added to 08 `contribution` (PRD-MEET-01 AC3 required it).
24. Rating: 07 `channel`, four-value fidelity scale, `value`, `sealed_until` → 08 `helpfulness`/`fidelity` (same three values, displayed Accurate/Partly/Not accurate), `tags`, `sampled`; sealing "until status decided".
25. Identity tiers: 07 `anonymous/account/personhood_verified/landmark_verified/steward` → 08 T0–T3 + agent + steward/admin; sign-in = magic link + passkey (atproto OAuth → OD-26).
26. Forecast: 07 5-bin RPS format → 08 question keys (`dU`/`win`/`dRep`), binary/quantile payloads, Brier/pinball; PRD JSON, UX mock and E10 updated.
27. Randomization: 07 "probability ≥ 0.1, IPW" → 08 block randomization per 4-week window with a committed seed (OD-08).
28. Agent registry fields in 07 aligned to 08 §9.1; 08 registry gained prompt hash + published prompt (PRD-AGT-01).
29. Disputes: 09/07 `correction` rows → 08 `flag` rows; `thats_not_me` is a `flag.kind`.
30. Tables: 09 `cluster_lineage_link` → `cluster_lineage`; `niche_cluster_alignment` → `niche_cluster_crosswalk`; `crawl_request` → `api_call`; `api_quota_ledger` → `quota_ledger` view; `selection_run` → `pipeline_run` (stage S3); `job_run` dropped. `api_call`, `quota_ledger`, `pipeline_release` and `incident` DDL added in 08a §A1.1.
31. `event_log` columns in 09 aligned to 08.
32. DB role `arena_ops_ro` → `arena_operator_ro`.
33. Stance: 09 gold annotators label TL's five attitudes (as the extraction schema does); spine values derived by 08 §3.4. 07 and 09 use only the four spine values for stances.

## E. Jobs, tools, CLI and infrastructure
34. LLM test backend `replay` (09) → `fake` (08).
35. `claude_code_batch` protocol in 09 (manifest.json, `_rejected/`, `waiting_external`, `arena llm wait/ingest`) → 08's `arena.ccbatch/1` (`BATCH.md`, `.claim`, `.error.json`, `DONE`, `PendingBatch` + `collect_batches`, `/process-batch`).
36. `arena` CLI: 08 now names it (`scripts/`, workspace member `arena_cli`, `scripts` added to workspace members); command groups unified in SPINE §10.7.
37. Contracts paths: 09 `apps/web/src/contracts`, `gen:types` → 08 `contracts/{public,llm}/`, `contracts/ts/`, `pnpm contracts`.
38. Procrastinate/ops task names in 09: `operator_report` → `ops_report`; `prepare_batch(audit|battery)` → `audit_sample` / `live_question_battery`; weekly schedule aligned to 08's Sunday `weekly` task; task registration location aligned to 08 §6.
39. Operator allow-list: 09 container names → 08 service names; `prepare_batch` → `prepare_review_batch`; `trigger_job` added to 09; `set_channel_route` and `hide_pending_review` added to 08 §10.7.
40. Compose: 09 `db`/`worker-ingest`/filesystem object store → 08 `postgres`/`worker-cpu`/MinIO in both profiles; worker queues `discover,fetch` (not `ingest`).
41. vLLM aliases/ports in 09 (`extract-qwen36` on port 8000, which collided with the API) → 08 `main` on 8001 etc.; LLM roles `config/pipeline.yaml` (`dedup`) → `config/llm.box.yaml` (`judge`).
42. ADR numbering: 09 ADR-0001…0006 → 08's ADR-001…027 plus new **ADR-028** (pre-box host); `docs/adr/ADR-0NN-<slug>.md`.
43. Clustering, S2 and S9 parameters in 09 aligned to 08 (Leiden resolution sweep with 30 bootstrap runs; rapidfuzz ≥ 88; top-20 → rerank top-5).

## F. Thresholds and protocols
44. Ratification: 07 gained `fidelity_lcb ≥ 0.60`; "only Benjamin changes them, via an ADR" stated in 07, 08, 09 and SPINE (OD-14). 08 code gained `Thresholds.fid_lcb_min` with a TODO (see G).
45. Fidelity eligibility: 07 (≥ 20 reactions, membership ≥ 0.5) → 08 (≥ 12 non-pass from ≥ 3 clusters, posterior ≥ 0.6, T2); 07 "raters cannot volunteer" → 08 "self-selected ≤ 50%"; portability from raters outside B.
46. Onboarding deck: 07 fixed 10 (4/3/3) → adaptive 8–12 (08 §4.11.1), OD-20.
47. Lineage credit: 07 "≥ 30% agree" → 08 uptake ≥ 0.5 in both parents, `SC = 3·min(…)`.
48. Agent-free re-fit: 07 ΔU ≤ 0.05 and "publish agent-free" → 08 max ΔU ≤ 0.10, eligibility ≥ 98%, block + incident, steward may publish agent-free (OD-24).
49. Agents and ratings: 09 "ratings stored but excluded" → cannot rate at all (403 + trigger), in §3.4, P3-W5-03, S-agents and G6.2.
50. Simulation suite unified (09 §4.3 canonical): S-honest uses 08's implemented metric (≥ 75% ratified, 0 strawmen) instead of AUC ≥ 0.85/0.90; brigade 15; 07's canary/bland/judgment added as S-canary/S-bland/S-judgment; 08 test assertion changed from 0.8 to 0.75 to match its own text and 20-seed sweep.
51. Extraction metrics: 08 §12.3 table remapped to the Plan's M1–M9 sheet and values (OD-13); 07 P2 row points to the same sheet.
52. Gold splits: 08 "held-out 20%" and `gold-vN/heldout.jsonl` → 09 dev 30% / sealed test 70% in `evals/gold/v<k>/`; tables are a mirror of the files.
53. Dispute SLAs unified (ack ≤ 48 h; hide ≤ 24 h; resolve 7 / 14 days) in 07 SEE-13 / ADM-04, 08 §11.3 and 09 §5.5.
54. Caption pacing and quotas in 09 aligned to 08 (20–40 s, ≤ 800/day, circuit breaker; YouTube stop at 9,000 units); 08's Podcast Index limit tightened to ≤ 1 req/s to match 09's conservative value.
55. Eye test: one canonical protocol (07 §7.3, merging 07's claim spot check with 09's blind/reveal/placement rounds); 09 and 08 §12.4 point to it.
56. Self-recognition: 07 insider proxy (≥ 70%) vs 09 judge check (≥ 85%) reconciled as stage A1 (judge, gating) + A2 (insiders, optional) in 07 §7.4, with **OD-28**.
57. P3 first-60 test: 07 "≥ 20 testers, ≥ 70%" → 09's "≥ 5 internal runs, median < 90 s".
58. P5 gate and beta size: 07's week-8 health targets moved out of the gate (tracked after); beta 40–80 for the gate, 150–300 later (**OD-27**); L4, L5, L8, A1 updated.
59. Static host and deploys: 07 "to choose" and 08 "P3 private preview" → Vercel recommended, no deploy before P5 without approval (OD-10).
60. Mac Mini: flagged as an unconfirmed assumption in 09 §1.1 (only 05 Q15 mentions it), made **OD-11** with ADR-028; 08 §1.3 now names the pre-box host; other 09 operational mentions say "pre-box host".

## G. Not reconciled (left for Benjamin or the swarm)
- The scorer code (`combined_status`) does not yet apply the `fidelity_lcb ≥ 0.60` rule that 08 §4.12.2 requires; `Thresholds.fid_lcb_min` was added with a TODO for W5 rather than rewriting tested code.
- The new S-canary, S-bland, S-judgment and S-sybil/S-cold-start tests are specified but not implemented in 08a.
- Docs 03, 05 and 06 were out of scope and were not edited; they may still use older names (e.g. 05's Neon recommendation, `CrossClusterNote`, `B_split`). The precedence order makes 07/08/09 win.
- Whether the Mac Mini exists (OD-11) and the leaderboard override of red line 19 (OD-09) need Benjamin's answer; the docs only state defaults.
