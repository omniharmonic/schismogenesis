# Gap-Filling Swarm Brief (Stage 1b)

Author of record: Benjamin Life (@omniharmonic). Never attribute to OpenCivics or OpenCivics Labs.

## Goal
The seed map (SEED-v2: 165 niches, 546 landmarks) must feel **thoroughly representative of as wide an array of US subcultures as possible**, each with public figures who can credibly speak for it. Your job is to find and fill what's missing in your assigned area.

## Before you start
1. Read `/home/claude/dialogos-arena/seed/SEED-BRIEF.md`. Its niche definition, landmark rules, **exclusions** (no minors, no private individuals, no designated-extremist spokespeople, no accounts whose primary output is harassment or incitement), neutral tone and JSON schema all apply.
2. Load the existing niche list so you **don't duplicate**: run
   `python3 -I -c "import json;d=json.load(open('/home/claude/dialogos-arena/seed/SEED-v2.json'));[print(n['niche_id'],'|',n['name'],'|',n['domain']) for n in d['niches']]"`
   and check landmark names against `d['landmarks']` before adding anyone. If a person is already a landmark elsewhere, you may list them as a *secondary* landmark for your new niche (note it) rather than a new record.

## Inclusion bar for a new niche (all three)
- A **distinct worldview or value system** (not just a hobby or aesthetic). A hobby/fandom qualifies only if it carries a recognizable shared outlook (e.g., what matters, who the enemies are, how to live).
- **At least 2 identifiable adult public voices** with real audiences who talk at length (podcasts, long-form video, streams, interviews). Prefer long-form talkers — the pipeline transcribes speech.
- Meaningful **size or cultural influence** in 2025–2026 US discourse.
If something fails the bar, list it as a `sub_niche` of the nearest niche (existing or new) or in a "considered but not added" list with the reason.

## Mirror rule
Where an existing niche is one side of an issue movement, check that the opposing or parallel side is represented, and name each side the way its own members describe it.

## Extra care
- Gen Z and youth spaces: many creators are minors. **Verify age ≥ 18 with a reliable source or exclude.**
- Extremes: descriptive mapping of legal movements is fine; exclude spokespeople of designated violent extremist organizations and accounts primarily devoted to harassment.
- No personal allegations, health or conduct claims in any field.

## Budget
Web searches are a shared, limited pool across six parallel agents: **use at most ~30 searches**. Lean on your own knowledge for candidate generation, then spend searches confirming activity (a dated 2025–26 item) for core landmarks first. Mark the rest `UNVERIFIED` rather than guessing.

## Output
- `/home/claude/dialogos-arena/seed/raw/<gap-id>.json` — array of new niche objects (SEED-BRIEF schema). Set `"domain"` to the closest existing domain id (d1-right, d2-left-center, d3-tech-futures, d4-heterodox-sensemaking, d5-religion-spirituality, d6-gender-lifestyle-subcultures, d7-economy-ecology-place, d8-geopolitics-media) **or** `"d9-mainstream-culture"` for apolitical/mainstream culture niches. Add `"gap_type"` (e.g., "mirror", "missing-arena", "gen-z", "mainstream", "subculture", "representation").
- `/home/claude/dialogos-arena/seed/raw/<gap-id>.md` — table of added niches and landmarks, the mirror pairs you closed, and a "considered but not added" list with reasons.
Final reply to the orchestrator ≤200 words: niches added, landmarks added, and the most important remaining gaps you noticed outside your area.
