# First written-source run: "The Education of a Libertarian"

Source: Peter Thiel, Cato Unbound, 2009, plus his own later addendum (18 paragraphs, 1,463 words).
The editor's note and other authors' summaries on the page were removed by hand.

| Step | Result |
|---|---|
| Ingest and chunk, stored in Neon | 18 segments, 4 chunks |
| Extraction (`claude_code_batch`, `extract_claims_written` v1) | 32 claims |
| Quote anchoring | 32 of 32 exact |
| Entailment gate (local DeBERTa, default thresholds) | 24 accepted, 8 escalated, 0 rejected |

## Limits of this run
- One essay, extracted by the same Claude session that built the pipeline, is a demonstration, not
  an evaluation. The exact-anchor rate is unsurprising for that reason. There is no gold set yet.
- Only 3 of the 8 validators in 08 §4.8 are ported, the cross-family critic is absent, and the
  entailment threshold is uncalibrated.
- The addendum carries the essay's 2009-04-13 date, though it was written later. Its true date
  needs setting, or later text should be ingested as its own item.

## Negative control
Distorted rewrites of real quotes, run in memory: 3 of 3 reversals were rejected as contradictions,
and 4 of 4 invented, widened or hedge-dropped statements escalated. None was accepted. That includes
"Women should not have the right to vote" tested against the suffrage sentence.

## Finding: first-person belief statements
The gate escalated several central claims, such as "I no longer believe that freedom and democracy
are compatible". A statement of belief does not entail the bare proposition. Rewritten as "The
author believes that freedom and democracy are not compatible", the same quote scored 0.98
entailment. The hypothesis wording for committed claims should be tested in P2. Escalated items wait
for review, so nothing wrong was accepted, but central claims would be lost without this fix.
