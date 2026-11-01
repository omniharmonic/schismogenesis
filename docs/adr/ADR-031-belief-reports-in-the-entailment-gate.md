# ADR-031: Belief reports in the entailment gate

Status: accepted for the pilot. Thresholds are unchanged. Calibration against gold happens in P2.
Date: 2026-10-31.

"I no longer believe that X" does not entail "not X", so the gate sent central first-person claims
to review. When a quote is a first-person belief report, the hypothesis now says what the author
believes: "The author does not believe that X." Other claims keep 08 §4.8's wording.

This matches what the pipeline claims. A stance records what a person holds, not whether it is
true. The trigger is a code pattern on the source quote, so a model cannot choose it.

The negative control must keep passing after this change: no distorted rewrite may be accepted.
