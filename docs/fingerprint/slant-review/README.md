# Blind slant review of the season-1 statements (2026-11-03)

Under D-31.18 (Benjamin: "blind slant review is needed").
- `statements.json`: what reviewers R1 and R2 saw. Statement text only: no thinkers, no camps, no stances.
- `R1.json`, `R2.json`: two independent slant reviews of all 24 statements.
- `meaning.json` → `M3.json`, `M4.json`: round 1. Two blind checks that each proposed rewrite means exactly the same as the original proposition, plus a slant read of two candidate replacements.
- `meaning2.json` → `M5.json`, `M6.json`: round 2, for the fixes and final replacements.

**Rule:** a rewrite is shown to quiz takers only when both meaning reviewers judged it equivalent. The outcome is in `seed/season-1.json`:
- 14 statements reworded;
- 10 kept as written;
- 2 replaced.

Each statement records which review applies.
