# ADR-036: AI Futures Fingerprint and rooms

Status: accepted by the builder 2026-11-02, under Benjamin's direction of the same day (D-31.16).

## Context
Benjamin scoped the next build to the AI-and-society conversation (EA, e/acc, d/acc, the wider TPOT
scene): a fingerprint that makes people want to see where they sit, the best map we can make, and
real Polis-style rooms with Community Notes bridging. Citizen-assembly-scale deliberation is out of
scope for now. Design: `docs/fingerprint/01-PRD.md`, `02-ARCHITECTURE.md`, `03-IMPLEMENTATION-PLAN.md`.

## Decision
1. **Fingerprint on device.** 24 anchor statements chosen by a fixed rule from atlas ideas that
   thinkers hold on both sides. Scoring runs in the browser. Nothing leaves it before the user opts in.
2. **Agreement over stated positions only**, Laplace-smoothed, ranked at three or more shared
   statements, with counts always shown. The reveal always shows splits and cross-cutting lines.
3. **Rooms are new tables** (`room`, `room_participant`, `room_statement`, `room_vote`, plus an
   append-only vote event log). They don't reuse the Slice 1 `statement` and `reaction` tables,
   which require pipeline claims and accounts.
4. **Room analysis joins two methods.** Polis-style groups (PCA, k-means, representativeness,
   group-informed consensus) and Community Notes-style bridges (matrix factorisation; neutral
   agreement μ + intercept of 0.75 or more, factor under 0.50, a majority on each side; the
   Community Notes intercept bar of 0.40 assumes a low baseline that rooms don't have). The factor is initialised from Polis PC1. Minimum-data rules
   show "not enough yet" instead of guessing.
5. **The anchors join the three spaces.** Room groups map to thinkers through their votes on the
   anchor statements, which are the same items the fingerprint uses.
6. **No LLM at runtime, no paid services.** The app is FastAPI plus static ES modules, with no build
   step.

## Tension recorded
The vision draft (§3, §7) had placement waiting on calibration. Benjamin's direction puts a placing
fingerprint first for an early-adopter audience. We keep it honest: counts are always shown, the
honesty notes are always visible, a fairness rating and dispute path come with every reveal, and a
blind slant review of the wording comes before any shared link (plan F7.2).

## Consequences
Pseudonymous browser identity allows repeat voting. That's acceptable for a private beta, and X
sign-in comes before a public one. The 27 thinkers are coarse, and TPOT-native voices are a
planned addition.
