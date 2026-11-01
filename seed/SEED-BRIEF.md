# Seed Swarm Brief: Niches & Landmarks (Stage 1)

Author of record: Benjamin Life (@omniharmonic). Never attribute to OpenCivics or OpenCivics Labs.

## Purpose
Build the seed dataset for the Dialogos Arena map: the cultural niches (memetic clusters) of US public discourse, and the landmark public figures whose public output (podcasts, YouTube, Substack, posts) will be transcribed and run through quote-anchored proposition extraction. Read `/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md` §7 for how landmarks are used.

Scope target across the whole swarm: roughly **120–180 niches** and **~450–550 landmarks** (about 3 per niche; 2 minimum; up to 5 for large or internally divided niches). Your domain should yield roughly **15–25 niches** — fewer if the domain is genuinely smaller; more only with good reason.

## What counts as a niche
A recognizable cluster of people who share an interpretive framework (Limberg & Barnes: a shared memeplex with its own telos, sacred values, threats and chieftains), with a **visible public conversation** in 2025–2026 (podcasts, channels, Substacks, accounts with real audiences). Balance plurality against scope:
- Include a niche if it has a distinct worldview (not just a hobby), at least 2 identifiable public voices, and an audience that is meaningful in size or in cultural influence.
- Split a niche when its members argue about fundamentals (e.g., two camps with different sacred values). Merge when the differences are of style only.
- Note deeper sub-niches as `sub_niches` rather than as separate entries, unless they meet the bar on their own.
- US-focused; include non-US voices only where they are central to a US niche.

## Who counts as a landmark
- A **public figure** with substantial public output in 2025–2026 that is representative of the niche's worldview. Prefer people who **talk at length** (podcasts, long-form video, interviews), because the pipeline extracts from transcripts.
- Include, per niche where possible: a **core** voice (the centre of gravity), and a **bridger/edge** voice (sits near a neighbouring niche, appears on other camps' shows). Mark the role.
- **Exclude:** private individuals; anyone under 18; anonymous accounts unless the anon persona is itself a major public figure; people whose output is primarily harassment or incitement to violence; spokespeople for designated violent extremist organizations. Fringe and extreme-but-legal movements that have a real public conversation may be mapped descriptively.
- Verify each landmark is **currently active** (output in the last ~12 months). Mark `UNVERIFIED` where you couldn't confirm.

## Tone
Descriptive and neutral, in terms a niche's own members would recognize. Describe worldviews; never score or judge people. Use the niche's own self-description where possible and note outsider labels separately.

## Sources
Use WebSearch/WebFetch. Useful starting points: Limberg & Barnes, "The Memetic Tribes of Culture War 2.0" (2018); Kevin Owocki's Atlas of Frontier Ontologies (https://daily-ontological-map.vercel.app/ — 58 ontologies; fetch it to align names where possible); More in Common "Hidden Tribes"; Pew Political Typology; podcast charts; Substack leaderboards; credible profiles and journalism about each scene. Cite a source for each niche and for each landmark's platforms.

## Output (write both files)
1. `/home/claude/dialogos-arena/seed/raw/<domain-id>.json` — a JSON array of niche objects with this provisional schema:

```json
{
  "niche_id": "kebab-case-unique",
  "name": "Self-recognized name",
  "aliases": ["outsider labels", "other names"],
  "domain": "<domain-id>",
  "description": "2–3 neutral sentences",
  "telos": "what it is trying to bring about",
  "sacred_values": ["..."],
  "existential_threats": ["what it fears"],
  "combatants": ["niches it most argues with (niche names)"],
  "adjacent_niches": ["niches it overlaps or bridges to"],
  "sub_niches": ["deeper rabbit holes, if any"],
  "size_estimate": "small | medium | large | very large (+ basis)",
  "cultural_influence": "low | medium | high (+ basis)",
  "trajectory": "rising | stable | declining | splitting (+ note)",
  "atlas_match": "nearest Owocki Atlas ontology name, or null",
  "limberg_barnes_match": "nearest 2018 tribe, or null",
  "landmarks": [
    {
      "name": "Full public name",
      "role": "core | bridger | edge",
      "why": "one line: why they represent this niche",
      "platforms": {"youtube": "channel URL or null", "podcast": "show name + URL or null", "substack": "URL or null", "x": "@handle or null", "bluesky": "handle or null", "other": "..."},
      "longform_output": "high | medium | low (how much transcribable talk exists)",
      "active_2025_2026": true,
      "verification": "verified | UNVERIFIED",
      "sources": ["URL", "..."]
    }
  ],
  "sources": ["URL", "..."],
  "notes": "uncertainties, boundary questions, overlaps with other domains"
}
```

2. `/home/claude/dialogos-arena/seed/raw/<domain-id>.md` — a readable summary: a table of niches (name · landmarks · size · trajectory) and a short note on boundary calls and gaps.

Final reply to the orchestrator: ≤200 words — niche count, landmark count, notable boundary calls, and niches you suspect belong to another domain.
