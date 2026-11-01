# Lifeworld Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a private 3D atlas of the AI futures region where thinkers appear as structures rooted in shared ideas.

**Architecture:** Existing written pipeline yields gated claims. A structure pass turns them into ideas, stances and typed links in existing tables. Tested measures in `arena_map.structure` compute coordinates and comparisons. A generator writes one self-contained page.

**Tech Stack:** Python 3.12, numpy, scikit-learn, Neon Postgres, bge-large-en-v1.5 (local), 3d-force-graph 1.x.

**Spec:** `docs/superpowers/specs/2026-11-01-lifeworld-atlas-design.md`

## Global Constraints
- Quotes ≤280 characters with source links. Full texts stay in git-ignored `data/`.
- Flagged landmarks excluded; `public_surface_allowed` must be true for everyone on the page.
- No paid APIs; model work uses subscription agents and `evals/queue`, `evals/results`.
- Inferred stances: half weight in geometry, never scored, dashed on the page.
- Neutral pronouns. Attribution to Benjamin Life only.
- Commit only inside `if make ci`.

## Review Focus
- A person with no accepted claims in the region: dropped from coordinates and named on the page.
- A pair with no shared ideas: `fork_profile` returns `lowest_opposed=None`, shown as "no shared ground measured".
- An idea held by one person: stays in the graph, excluded from correspondence rows' fitting weight via zero-variance guard.
- WebGL unavailable: the page shows the text fallback, not a blank canvas.
- A term with too few uses in a school: `sense_fork` returns None, not a score.

---

### Task 1: Corpus for the 14 new people
**Files:** Create `seed/AI-FUTURES-SOURCES.json`; texts in `data/texts/<key>.txt`.
- [ ] Find 2–3 own-name public works per person, cleaned to at most 4,000 words.
- [ ] Run `arena written ingest-list --sources seed/AI-FUTURES-SOURCES.json`. Expected: one chunk line per work.
- [ ] Commit the source list.

### Task 2: Claims for new works
- [ ] `arena written extract-all --batch core-v3`; answer the queue with agents using prompt v2.
- [ ] `scripts/check_batch.py core-v3`. Expected: no SCHEMA or QUOTE problems.
- [ ] `arena written extract-all --batch core-v3` then `arena written gate-all`.
- [ ] Record accepted, rejected and escalated counts per person.

### Task 3: Measures library (TDD)
**Files:** Create `packages/arena_map/src/arena_map/structure.py`, `packages/arena_map/tests/test_structure.py`.

**Interfaces — Produces:**
- `LAYERS = ("ontology", "epistemology", "axiology", "empirical", "praxis")`
- `Holding(person: str, idea: str, accepts: bool, inferred: bool)`
- `correspondence(holdings: list[Holding], dims: int = 8) -> Coordinates` with `.people: dict[str, ndarray]`, `.ideas: dict[str, ndarray]`, `.inertia: ndarray`
- `fork_profile(a: str, b: str, holdings: list[Holding], layer: dict[str, str]) -> Fork` with `.by_layer: dict[str, tuple[int, int]]` (shared, opposed), `.lowest_opposed: str | None`, `.shared_roots: list[str]`
- `schools(coordinates: Coordinates, cut: float) -> list[list[str]]`
- `school_stability(holdings, cut, runs=500, seed=7) -> dict[frozenset[str], float]`
- `reasons_load(idea, holders: int, links: int) -> float` returns links / holders, 0 when no holders
- `sense_fork(vectors: dict[str, ndarray], min_uses=5, permutations=2000, seed=7) -> SenseFork | None` with `.distance`, `.p`
- `fidelity(full: ndarray, seed2d: ndarray, neighbours=5) -> float`

- [ ] Tests first: two opposing camps separate on axis 1; people and ideas of a camp fall on the same side; a shared root with opposed values gives `lowest_opposed == "axiology"` and the root in `shared_roots`; no overlap gives `None`; inferred stances move coordinates less than stated; `sense_fork` returns None under `min_uses`, and a low p for separated vectors, a high p for mixed ones.
- [ ] Run `uv run --no-sync pytest packages/arena_map -q`. Expected: fails on import.
- [ ] Implement.
- [ ] Run tests. Expected: pass. Commit.

### Task 4: Structure pass
**Files:** Create `packages/arena_extract/src/arena_extract/prompts/ideas_v1.md`, `links_v1.md`; `scripts/prepare_structure.py`, `scripts/load_structure.py`.
- [ ] `prepare_structure.py`: embed accepted claims in the region with bge-large, assign themes, write per-theme tasks with claim ids and quotes.
- [ ] Agents write ideas per theme: canonical, layer, tl_type, validity tag, holdings (claim id, accepts or rejects), inferred roots with necessity argument.
- [ ] Agents write typed links across ideas, each with evidence claim ids, or marked inferred.
- [ ] Second blind readers check all inferred roots and a sample of at least 200 holdings and 100 links. Drop disagreements; report rates.
- [ ] `load_structure.py` idempotently writes `proposition`, `stance`, `proposition_relation` with provenance and event log entries. Test on local Postgres. Commit.

### Task 5: Measured atlas
**Files:** Create `scripts/build_atlas.py`.
- [ ] Output `atlas.json`: nodes, links, coordinates, schools with stability, forks, reasons load, first years, honesty checks.
- [ ] Compute sense forks for at least 8 contested terms with bge-large.
- [ ] Run stated-only ablation and the embedding baseline; assert both are present in the output.

### Task 6: Page
**Files:** Create `apps/atlas/atlas.tpl.html`, `apps/atlas/build_page.py`.
- [ ] Load `Artifact` quickstart guidance, build per spec, generate one HTML file.
- [ ] Verify in a real browser with Playwright: nodes render, person select, two-person fork, idea select, search, layer toggles, time slider, phone width, no-WebGL fallback, no console errors, light and dark.

### Task 7: Finish
- [ ] Write ADR-035, `docs/status/2026-11-01-lifeworld-atlas.md`, D-31.15, and update CLAUDE.md repo layout if needed.
- [ ] `make ci` passes; commit and push; confirm GitHub CI green.
- [ ] Publish privately and review the final numbers against the database. Report to Benjamin with the hypothesis result stated plainly.
