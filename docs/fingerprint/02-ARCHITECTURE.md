# AI Futures Fingerprint: technical architecture

Owner: Benjamin Life. Drafted by Claude, 2026-11-02. Implements `01-PRD.md`. Decision record: ADR-036.

## 1. Shape of the system

```
 atlas-v1.json (checked structure: 27 thinkers, 360 ideas, quotes ≤280 chars)
        │  scripts/build_fingerprint.py  (arena_fingerprint: choose anchors, export)
        ▼
 apps/arena/public/fingerprint.json  ── static bundle, versioned, committed
        │
        ▼
 Browser (apps/arena, plain ES modules, no build step)
   fingerprint.js  — all fingerprint scoring, on device (PRD R3)
   map.js / card.js — 2D map and share card (SVG, canvas → PNG)
   room.js         — voting, writing, room report (only after opt-in)
        │  HTTPS JSON, only after "Add my answers to the live room"
        ▼
 services/api (FastAPI)  ── arena_api.app:create_app
   store.py   — SQL against Postgres (rooms, statements, participants, votes)
   routes     — /api/rooms/…, /api/admin/…
   report     — arena_rounds.report.room_report (numpy, cached per vote version)
        │
        ▼
 Postgres (existing dev database; new migration 0009_rooms)
```

What stays the same: Python 3.12, uv workspace, Postgres, Alembic with SQL files, `make ci`. What's new: a FastAPI app, two pure-Python packages, and one static web app. It needs no paid services and no LLM at runtime.

## 2. Packages and files

| Path | Responsibility |
|---|---|
| `packages/arena_fingerprint/src/arena_fingerprint/anchors.py` | Choose the anchor statements from the atlas (rule in §4). |
| `packages/arena_fingerprint/src/arena_fingerprint/bundle.py` | Build the browser bundle: anchors, thinkers, schools, camps, stances, quotes. |
| `packages/arena_fingerprint/src/arena_fingerprint/agreement.py` | The agreement formula in Python (server use: mapping room groups to thinkers). |
| `packages/arena_fingerprint/tests/vectors.json` | Shared test vectors. The Python and JS tests both check them, so the two implementations can't drift. |
| `packages/arena_rounds/src/arena_rounds/matrix.py` | Build the vote matrix from rows. |
| `packages/arena_rounds/src/arena_rounds/polis.py` | PCA, k-means groups, representativeness, group-informed consensus, divisiveness. |
| `packages/arena_rounds/src/arena_rounds/bridging.py` | Community Notes-style matrix factorisation and bridge labels. |
| `packages/arena_rounds/src/arena_rounds/report.py` | Assemble the room report with minimum-data rules. |
| `packages/arena_rounds/src/arena_rounds/synthetic.py` | Labelled fake voters for demo rooms only. |
| `services/api/src/arena_api/app.py` | FastAPI app, static files, routes. |
| `services/api/src/arena_api/store.py` | SQL. |
| `services/api/src/arena_api/text_rules.py` | Participant statement checks (length, no handles, links or emails). |
| `packages/arena_core/src/arena_core/migrations/versions/0009_rooms.py` + `sql/0009_rooms.sql` | Schema. |
| `scripts/build_fingerprint.py` | CLI: atlas → bundle. |
| `scripts/demo_room.py` | CLI: create the demo room and fill it with synthetic voters. |
| `apps/arena/public/` | `index.html`, `style.css`, `app.js`, `fingerprint.js`, `map.js`, `card.js`, `room.js`, `admin.html`, `fingerprint.json`, `atlas.html`. |
| `apps/arena/tests/*.test.mjs` | `node --test` for the browser modules. |
| `apps/arena/source/atlas-v1.json` | The frozen atlas input (public-figure data; quotes ≤280 chars with links). |

## 3. The bundle (`fingerprint.json`)

```json
{
  "version": "fp-2026-11-02.1",
  "atlas_version": "atlas-v1",
  "sets": [{"id": "being", "title": "What AI is and where it's going", "layers": ["ontological","empirical"]}, …],
  "anchors": [{"id": "ai-extinction-risk", "set": "being", "layer": "empirical", "text": "…", "family": 12}],
  "thinkers": [{"id": "vitalik-buterin", "name": "Vitalik Buterin", "initials": "VB", "school": "Long-term stewards", "x": 12.3, "y": -40.1}],
  "schools": [{"label": "Builders", "members": ["…"]}],
  "camps": [{"id": "eacc", "label": "e/acc", "members": [...]}, {"id": "safety", "label": "AI safety / EA", …}, {"id": "dacc", "label": "d/acc & pluralists", …}],
  "stances": {"<anchor id>": {"<thinker id>": {"a": 1, "q": "quote ≤280", "url": "…", "work": "…"}}},
  "layers": ["ontological","epistemic","axiological","empirical","praxis"],
  "notes": ["Thinkers are read by machine from about 3 public works each. …"]
}
```

Only **stated** stances go into `stances`. Inferred holdings are left out (PRD R4).

## 4. Choosing anchors (deterministic)

Candidates are atlas ideas with at least 3 stated holders, at least 1 on each side, and a neutral proposition of 200 characters or fewer.

- Each candidate's **split score** is `accepts × rejects` (thinker pairs it separates), plus a camp bonus of 2 when the e/acc, AI safety and d/acc camp majorities aren't all on the same side.
- **Sets** (8 each):
  - `being` = ontological and empirical.
  - `values` = epistemic and axiological.
  - `action` = praxis.
- **Coverage:** each pick also gains 4 points for every holder who still has fewer than 3 stated stances among the anchors chosen so far. Without this, Exit founders could never be ranked; the balance test found it.
- **Greedy fill per set:** take the remaining candidate with the highest split score plus coverage gain. Skip it if its family already has one anchor in this set or two anchors overall. Ties go to the idea id.
- If a set can't reach 8 under the family rule, relax both caps by one for that set only, and record the relaxation in the bundle's `selection_log`. The log also names every thinker left with fewer than 3 stated stances; the reveal lists them as "not enough to compare". On atlas-v1 these are Sacks (0), Weyl (1), Balaji, Musk and Alexander (2 each). Reading more of their work is in plan F8.
- The run is reproducible: the same atlas gives the same bundle. A test pins this.

## 5. Fingerprint maths (browser, mirrored in Python)

Answers are `+1` (agree), `-1` (disagree), `0` (unsure), or missing (skip). For a thinker `j`, take the anchors where the answer is ±1 and `j` has a stated stance:

- `n_j` = number of such anchors, `k_j` = number where the answer equals the stance.
- **Score** `s_j = (k_j + 1) / (n_j + 2)`. This is a Laplace-smoothed agreement rate, so 1 of 1 doesn't beat 9 of 11.
- **Ranked** only if `n_j ≥ 3`. Sort by `s_j`, then `n_j`, then id. Show `k_j of n_j`.
- **Not enough answers:** fewer than 6 answers that are ±1, or fewer than 5 ranked thinkers. The reveal then asks for more answers and places no one (PRD S4).
- **School affinity:** a school is as close as its closest ranked member, so the home school is the school of your nearest thinker who has one. Alex Karp has no school. A mean over members was rejected: on 1,000 random sheets it put the large, mixed Builders school on top at 0.3× its fair share.
- **Position:** take the top 3 ranked thinkers, weight each `w_j = exp(14 (s_j − 0.5))`, and set `xy = Σ w_j xy_j / Σ w_j`. It's labelled "approximate". A broad average over 5 put room groups in empty space between schools, because the layout is non-linear. Room groups are not placed as points; their letters tag their three closest thinkers instead, and "You" is drawn with lines to its three.
- **Signature** (cross-cutting lines): for each answered anchor, compare the user's answer to the majority stance of the nearest school `S` (members with stances; it needs at least 1) and of every other school `T`. The anchor is a candidate when `S` opposes the user and `T` agrees. Strength = (share of `S` opposed) × (share of `T` agreeing) × (number of `T` members with stances, capped at 3). Keep the best per anchor and show the top 3. If nothing qualifies, show "You're consistent with your neighbourhood on every statement we could check" together with the user's weakest agreement.
- **Camp splits:** for each camp and each layer, count anchors where the camp majority agrees or disagrees with the user. A tied majority doesn't count. The **deepest split** is the first layer, in the order ontological, epistemic, axiological, empirical, praxis, where disagreements outnumber agreements.

## 6. Room analysis (`arena_rounds`)

Input: the latest votes, as `(participant, statement, vote ∈ {−1, 0, +1})`. Synthetic participants count only in rooms with `config.demo = true`.

**Polis part (`polis.py`):**
- Use participants with at least 7 votes. Build the matrix and centre each column on its observed mean. Missing cells become 0 after centring, which is mean imputation. Scale each row by `sqrt(S / votes_p)`, as Polis does for sparse voters.
- Take the top 2 principal components by SVD, for the 2D view.
- Run k-means on the 2D projection for k = 2 to 5, with k ≤ n/5. Choose by silhouette. Use 10 fixed seeds (deterministic). If the best silhouette is below 0.15, report one group ("no clear groups yet").
- **Representativeness** per group `g` and statement: `pa_g = (1 + agrees_g) / (2 + seen_g)`, where `seen` counts agree, disagree and pass. `ra = pa_g / pa_rest`, and the same for disagree. A statement is representative if `ra > 1` and a one-sided two-proportion z-test passes with z > 1.2816 (90%). Show the top 5 by `ra × pa_g`.
- **Group-informed consensus:** `Π_g pa_g`. It counts as common ground when every group has `pa_g > 0.5`.
- **Divisiveness:** `max_g pa_g − min_g pa_g`.

**Community Notes part (`bridging.py`):**
- Ratings: agree = 1, disagree = 0. Passes are left out. Use statements with at least 5 raters and participants with at least 3 ratings.
- Model: `r̂ = μ + b_u + b_s + f_u f_s`. Loss = Σ(r − r̂)² + λ_i (Σb_u² + Σb_s²) + λ_f (Σf_u² + Σf_s²), with λ_i = 0.15 and λ_f = 0.03 by default. Intercepts are penalised more than factors, so a statement's base score has to be earned across sides.
- Fit by alternating ridge solves: each statement's `(b_s, f_s)` given the participants, then each participant's `(b_u, f_u)`, then μ. Run 60 sweeps. Initialise `f_u` from the standardised Polis PC1, which also fixes the sign. Deterministic.
- **Bridge:** neutral agreement `μ + b_s ≥ 0.75`, `|f_s| < 0.50`, and a majority agreeing on each side. Community Notes uses intercept ≥ 0.40, but its baseline is low while a room's sits near 0.5, so the same intercept would need over 90% agreement; the demo test showed it. The factor bar is the Community Notes value. **Leaning bridge:** the top 5 by `b_s` with `|f_s| < 0.5` that didn't reach the bar. Sides seen are reported: the statement must have raters with `f_u > 0` and `f_u < 0`, at least 2 each.
- **Axis label:** correlate `f_u` with each participant's (camp A affinity − camp B affinity) on anchor votes, for every camp pair. If |r| ≥ 0.4, say "The room's main split lines up with A ↔ B (r = …)".

**Minimum-data rules (`report.py`):**

| Section | Shown when | Otherwise |
|---|---|---|
| Groups | at least 10 participants with 7 or more votes | "Groups appear after 10 people have cast 7+ votes (now: n)." |
| Bridges | the MF fit has at least 8 participants and at least 1 statement with 5+ raters | "Bridges need more votes." |
| Thinker map of groups | groups are shown | none |

**Groups to thinkers:** each group's stance on an anchor is +1 if `pa_g > pd_g + 0.1`, −1 if the reverse, and otherwise none. Then use the §5 formula to get the group's nearest 3 thinkers.

The report is cached in memory, keyed by `(room_id, vote_version)`. `vote_version` is the count plus the max timestamp of vote events.

## 7. Schema (migration `0009_rooms`)

```sql
CREATE TABLE room (room_id uuid PK default gen_random_uuid(), slug text UNIQUE NOT NULL, title text NOT NULL,
  description text NOT NULL DEFAULT '', status text NOT NULL DEFAULT 'open' CHECK (status IN ('open','closed')),
  bundle_version text NOT NULL, config jsonb NOT NULL DEFAULT '{}', created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE room_participant (participant_id uuid PK default gen_random_uuid(), room_id uuid NOT NULL REFERENCES room,
  key_hash bytea NOT NULL, handle text, is_synthetic boolean NOT NULL DEFAULT false, consent_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE room_statement (statement_id uuid PK default gen_random_uuid(), room_id uuid NOT NULL REFERENCES room,
  text text NOT NULL, origin text NOT NULL CHECK (origin IN ('anchor','participant','agent')), anchor_id text,
  author_id uuid REFERENCES room_participant, status text NOT NULL DEFAULT 'pending'
  CHECK (status IN ('pending','approved','rejected')), reject_reason text, created_at …, moderated_at timestamptz,
  UNIQUE (room_id, anchor_id));
CREATE TABLE room_vote (participant_id uuid REFERENCES room_participant, statement_id uuid REFERENCES room_statement,
  vote smallint NOT NULL CHECK (vote IN (-1,0,1)), updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (participant_id, statement_id));
CREATE TABLE room_vote_event (event_id bigint GENERATED ALWAYS AS IDENTITY PK, participant_id uuid, statement_id uuid,
  vote smallint, created_at timestamptz NOT NULL DEFAULT now());           -- append-only
CREATE TABLE placement_dispute (dispute_id uuid PK, person_id text NOT NULL, anchor_id text, body text NOT NULL,
  contact text, status text NOT NULL DEFAULT 'open', created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE fairness_rating (rating_id bigint identity PK, bundle_version text NOT NULL,
  rating smallint NOT NULL CHECK (rating BETWEEN 1 AND 5), created_at timestamptz NOT NULL DEFAULT now());
```

These are separate from the Slice 1 `statement`, `reaction` and `app_user` tables. Those are tied to pipeline claims and to account-based users, and the room needs neither yet (ADR-036).

## 8. API

| Method and path | Body / result | Notes |
|---|---|---|
| `GET /api/rooms/{slug}` | room, counts | |
| `POST /api/rooms/{slug}/join` | `{key, handle?, consent_version, answers?: {anchor_id: vote}}` → `{participant_id}` | `key` is a random 32-byte secret made in the browser; the server stores sha256 only. Any answers given become votes on the anchor statements. |
| `GET /api/rooms/{slug}/next?limit=5` | statements the participant hasn't voted on, least-voted first, then random | header `X-Participant`, `X-Key` |
| `POST /api/rooms/{slug}/votes` | `{statement_id, vote}` | upsert into `room_vote` plus an event row |
| `POST /api/rooms/{slug}/statements` | `{text}` → pending | text rules, 5 per day per participant |
| `GET /api/rooms/{slug}/report` | report JSON | public: aggregates only |
| `GET /api/rooms/{slug}/me` | the participant's group and the bridges they backed | auth headers |
| `POST /api/disputes` · `POST /api/fairness` | | anonymous |
| `GET/POST /api/admin/…` | pending statements, approve and reject, disputes | `Authorization: Bearer $ARENA_ADMIN_TOKEN`; disabled if unset |

Static files: `/` serves `apps/arena/public`, and `/atlas` serves `atlas.html`.

There's a simple in-memory rate limit per IP and per participant, with a 429 on excess. That's enough for a beta on one process; a public launch needs a real limiter (open point).

## 9. Privacy and red lines in the code

- No answer leaves the browser before opt-in. Before joining, `room.js` is not even loaded, and `fingerprint.js` doesn't use the network.
- Anonymous participants are pseudonymous by random key, with no email. The participant's key lives in `localStorage`, and "Leave the room" deletes it locally.
- The public report shows aggregates only. Groups under 3 people aren't described.
- Only the 27 atlas thinkers appear. The bundle builder fails if any of the flagged landmark ids appear (`seed/SEED-v4.json` `flags_for_benjamin`).
- Quotes over 280 characters fail the build.
- Participant text rules: 10 to 140 characters, no `@handle`, no URL, no email, and not a duplicate (case- and space-insensitive) of an existing room statement.

## 10. Local run

```
make app          # migrate, build the bundle and atlas page, serve on http://localhost:8800
make demo-room    # create room "demo" with 120 labelled synthetic voters
make test-js      # node --test apps/arena/tests
```

`make ci` adds `test-js`.

## 11. Known limits (said plainly)

- Anyone can vote many times by clearing their browser. That's fine for a private beta and not fine for a public one. X sign-in is in the plan (F7).
- 27 thinkers and 24 anchors are coarse. Agreement on 9 of 11 is a small sample, so the reveal shows the counts.
- Matrix factorisation on fewer than about 50 participants is noisy. Bridges are labelled with their rater counts, and the bar stays at the Community Notes values instead of being lowered to produce results.
- The atlas schools are machine-made working labels (atlas copy says so).
