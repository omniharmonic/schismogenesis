# Worldview core pilot

Private page: https://claude.ai/artifact/Xj38hmkuZVQi7XAbXh1k9s

14 public works by 12 authors (`seed/WORLDVIEW-CORE-SOURCES.json`), about 30,000 words, 85 chunks. All
results are in Neon. Full texts stay out of git.

| Step | Result |
|---|---|
| Extraction by 4 independent agents | 576 claims |
| Quote anchoring, M6b | 576 of 576 exact, 100% |
| Validators and entailment gate | 414 accepted, then 4 moved to review by the audit: 410 |
| Blind audit, 108 claims, one reader | M5 0.875; 1 wrong meaning; voice own 97% |
| Negative controls | 0 of 15 distortions accepted |
| Cross-author comparison | 1,188 pairs: 0 equivalent, 0 contradictory |
| Live questions | 21 drafted, 14 survived a blind second reader, 12 after review |
| Placements | 216 drafted, 144 agreed, 93 published; 94% agreement where both readers placed a claim |

## Main finding
Claim-first extraction alone gives almost no overlap. Nobody said the same sentence, and no pair
flatly contradicted. A map needs a shared frame, so live questions drawn from the claims become the
comparison layer. This differs from the rejected question-first design: questions come after
extraction, and every placement cites a verified quote. This needs Benjamin's review before P3,
because S11 clustering on the stance matrix alone would have nothing to work with.

## Known weaknesses
- The audit's main fault is lost scope: a limit stated elsewhere in the paragraph is dropped. The
  next prompt version should carry such limits into the proposition.
- Unresolved references ("this country") hurt comparison.
- The Vance transcript has source labels mixed into the text. None reached a proposition.
- The sample is one or two works per person. Karp appears on no question.
- All extraction, judging and auditing used Claude, so shared blind spots remain possible. No gold
  set exists yet, and neither the human eye test nor author review has happened.
- The Anthropic disclosure applies: Claude built and read this, and Dario Amodei is one of the twelve.
