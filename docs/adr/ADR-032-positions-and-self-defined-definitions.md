# ADR-032: Positions and self-defined definitions

Status: accepted (D-31.13, D-31.14). Date: 2026-11-01.

A live question holds any number of positions. A person holds a position through a specific claim,
with the reason recorded, so people who share a position for different reasons stay distinguishable.

Definitions belong to the people described. Models draft them only to bootstrap. Every wording is a
row in the append-only `position_definition`, recording who wrote it. Constraints enforce that a
model's wording can never be ratified and that human wording names its author. People placed in
the relevant niche or cluster later replace the drafts. `position.status` starts as `provisional`.
The ratification threshold and flow reuse the OD-14 machinery and are decided before the beta.

Placements are model judgments about public text. A person's holding of a position stays open to
the same dispute affordance as any stance.
