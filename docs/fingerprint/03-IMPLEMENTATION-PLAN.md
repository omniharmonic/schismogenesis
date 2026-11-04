# AI Futures Fingerprint: implementation plan

Owner: Benjamin Life. Drafted by Claude, 2026-11-02. Implements `01-PRD.md` and `02-ARCHITECTURE.md`.

**Goal:** a locally runnable app that Benjamin can test end to end: answer, reveal, share card, join room, vote, write, room report. Then a short path to a private beta link.

**Execution:** Claude builds natively in this session, test-first per stage. `make ci` stays green at every commit. No public deploy and no outreach without Benjamin's yes.

## Status (2026-11-02)
F1 to F6 are built and pass `make ci` (107 Python tests, 9 JS tests). Benjamin's test guide is `TESTING.md`. What testing changed from the first design:
- **Anchor selection gained a coverage bonus.** The balance test showed Exit founders could never be ranked without it.
- **Home school is now the school of your nearest thinker.** A mean over members put the large, mixed Builders school on top at 0.3× its fair share.
- **The bridge bar is neutral agreement ≥ 0.75, with a majority on each side.** The Community Notes intercept of 0.40 assumes a low baseline that rooms don't have.
- **Room groups are no longer placed as points on the map.** Their letters tag their three closest thinkers, and "You" is drawn with lines to its three.
- Nothing is committed yet; it waits for Benjamin's go-ahead.

## Global constraints
- Python 3.12, uv workspace; ruff line length 100; pyright standard.
- No paid APIs, no cloud spend, no LLM at runtime.
- Quotes ≤ 280 characters with links; only the 27 atlas thinkers; none of the 20 flagged ids.
- Attribute the work to Benjamin Life.
- Fingerprint answers never leave the browser before opt-in.

## Review focus (what is most likely to bite a real user, with the test that pins it)
1. **A user skips or answers "Unsure" to most statements.** The reveal must refuse to place them. Pinned by `fingerprint.test.mjs: too few answers → not enough`.
2. **A thinker has stances on only 1 or 2 answered anchors.** They must not top the list. Pinned by `ranked needs n ≥ 3` and by the Laplace score test.
3. **The room is small or one-sided** (everyone agrees, one group). The report must show the "not enough yet" states and no fake groups. Pinned by `test_report_small_room` and `test_single_cluster`.
4. **A participant writes a statement with a handle or link, or pastes a duplicate.** It's refused with a clear reason. Pinned by `test_text_rules`.
5. **Synthetic voters leak into a real room's report.** Pinned by `test_synthetic_excluded_outside_demo`.

## Stages

### F1. Bundle: anchors and stances (Python)
- Files: `packages/arena_fingerprint/…/anchors.py`, `bundle.py`, `agreement.py`, tests, `scripts/build_fingerprint.py`, `apps/arena/source/atlas-v1.json`.
- Interfaces:
  - `select_anchors(ideas: list[dict], camps: dict[str, list[str]], per_set: int = 8) -> tuple[list[dict], list[str]]` returns the anchors and the selection log.
  - `build_bundle(atlas: dict, flagged: set[str]) -> dict`
  - `agreement(answers: dict[str, int], stances: dict[str, dict[str, int]]) -> dict[str, tuple[int, int, float]]` maps each thinker to (k, n, s).
- Tests:
  - Determinism (same input gives the same output).
  - The family cap.
  - Only stated stances.
  - Quote length.
  - The flagged-id guard raises.
  - Shared vectors in `vectors.json`.
- Done when `fingerprint.json` exists with 24 anchors, 8 per set.

### F2. Fingerprint scoring (browser module)
- Files: `apps/arena/public/placement.js`, `apps/arena/tests/fingerprint.test.mjs`.
- Interface: `fingerprint(bundle, answers) -> {status: 'ok'|'not_enough', answered, ranked[], furthest[], schools[], position, signature[], camps[]}`. Each `ranked` item is `{id, name, k, n, s}`.
- Tests: the shared vectors; not enough answers; ranking needs n ≥ 3; signature found on a crafted case; camp deepest split; position inside the hull of the top 5. Plus the balance check (PRD S1): 1,000 random answer sheets, each school's top-match rate between 0.5× and 2× its fair share. If it fails, report it rather than tune it away.

### F3. Room analysis (Python)
- Files: `packages/arena_rounds/…/matrix.py`, `polis.py`, `bridging.py`, `report.py`, `synthetic.py`, tests.
- Interfaces:
  - `VoteMatrix.from_rows(rows: list[tuple[str,str,int]]) -> VoteMatrix` with `.participants`, `.statements`, `.values` (nan for unseen).
  - `polis_groups(m: VoteMatrix, min_votes=7, seed=7) -> PolisResult` with `projection`, `labels`, `k`, `silhouette`, `included`.
  - `group_stats(m, labels) -> dict` giving pa, pd and seen per group and statement.
  - `representative(stats) -> dict[group, list]`, `consensus(stats) -> list`, `divisive(stats) -> list`.
  - `fit_bridging(m, init: dict[str,float] | None, lambda_i=0.15, lambda_f=0.03, sweeps=60) -> BridgeFit` with `mu`, `b_u`, `f_u`, `b_s`, `f_s`, `raters`.
  - `bridges(fit, threshold=0.40, max_factor=0.50) -> (bridges, leaning)`.
  - `room_report(rows, statements, bundle, demo: bool) -> dict`.
  - `synthetic_votes(bundle, statements, n=120, seed=7) -> list[rows]` uses planted groups (3 camps plus noise), so tests can check that groups are recovered.
- Tests:
  - Planted 3 groups are recovered (ARI ≥ 0.8).
  - A planted bridge statement (all groups agree) passes the bar, and a planted divider does not.
  - Determinism.
  - Small-room states.
  - Single cluster.
  - Synthetic rows are excluded outside demo.
  - The axis label finds the planted camp split.

### F4. Storage and API
- Files: `sql/0009_rooms.sql`, `versions/0009_rooms.py`, `services/api/src/arena_api/{app.py,store.py,text_rules.py,limits.py}`, `services/api/tests/test_api.py` (marker `db`).
- Dependencies: `fastapi`, `uvicorn` (open source, local).
- Tests:
  - Join stores only the key hash.
  - Answers become votes.
  - Re-vote updates the vote and adds an event.
  - `next` excludes statements already voted on and pending statements.
  - Statement text rules.
  - Admin needs the token, and is disabled when the token is unset.
  - The report endpoint returns aggregates only (no participant ids).
  - Disputes and fairness ratings are stored.

### F5. Web app
- Files: `apps/arena/public/{index.html,style.css,app.js,map.js,card.js,room.js,admin.html}`.
- Screens:
  - Landing.
  - Three sets of 8 cards, with a teaser after each set.
  - Reveal: nearest and furthest, map, signature, camps, quote mirror, share card, fairness, report.
  - Room: vote, write, report.
  - Admin.
- Checks:
  - Playwright run at 390px and 1280px, light and dark.
  - No network calls before join (PRD S3).
  - Keyboard path.

### F6. Local run and demo
- `make app`, `make demo-room`, `make test-js`. A `docs/fingerprint/TESTING.md` script tells Benjamin what to click and what to look for.
- **Testable milestone: Benjamin tests here.**

### F7. Beta hardening (after Benjamin's first test; each step needs his yes where marked)
1. Fixes from his test.
2. Blind slant review of the 24 anchor wordings (two readers, eval E-F1).
3. Self-tests with 2 or more people from different camps (PRD S2).
4. 3D atlas overlay of "you" (R15).
5. "Would they sign this?" notes on school descriptions (R16).
6. X sign-in (R17).
7. Hosting choice and private beta URL. **Benjamin's yes.**
8. Local-model bridge suggestions, labelled as agent-written (R18).
9. Weekly round cadence and a Record of Understanding (R19).

### F8. Map upgrades ("best in class")
- Add 3 to 5 TPOT-native voices (needs Benjamin's picks and the extraction run on the GB10 box).
- Fix the known map trust issues: silence handling in `person_space`, the 54% line, and the `fidelity` docstring.
- Show room groups as live regions on the 3D atlas.
- Track change over seasons.

## Order and why
- The bundle comes first because everything reads it.
- Browser scoring comes second because it is the hook and needs no server.
- Room maths comes before the API so the hardest logic is tested as plain functions.
- The UI comes last, on top of tested parts.
- The demo room exists so the report can be seen before any real people join.
