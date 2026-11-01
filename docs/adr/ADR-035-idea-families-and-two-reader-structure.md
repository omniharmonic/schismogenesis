# ADR-035: Idea families and two-reader structure

Status: accepted by the builder 2026-11-01, for Benjamin's review.

## Context
Benjamin asked for a 3D map where thinkers read as structures built from clusters of ideas. Exact
claim matching found nothing across authors (0 of 1,188 pairs). Raw text embeddings measure topic.

## Decision
1. **An idea** is an assertion a holder would accept as a fair statement of part of their view.
2. **Two readers.** A holding enters the map only if a blind second reader agrees. Rejection requires
   the person's words. Silence is missing data.
3. **Inferred roots** need a written necessity argument and a blind "needed" verdict. They carry half
   weight, are drawn as wire spheres, and never count as shared ground in a fork's stated roots.
4. **People are compared over 40 idea families**, signed, damped and centred, by cosine distance.
   Families come from embeddings plus argument links, with attacks keeping poles apart. Embeddings
   group ideas and never decide what anyone believes.
5. **Height is the layer.** It is fixed, and horizontal force is anchored to measured positions.
6. **Everything is provisional.** No agent ratifies, and no person has seen it.

## Why not the alternatives
- Correspondence analysis on single ideas put 26 of 27 people in one group.
- Propagating stance through links improved the score only slightly.
- Machine-proposed holdings: 80 of 734 survived blind reading, so entailment alone cannot fill gaps.

## Consequences
The number of families (40) was chosen by comparing options against an outside check, and nine
schools is the top of the tested range. Both are open. Sparse coverage comes from reading about three
works per person, so more works should improve every measure.
