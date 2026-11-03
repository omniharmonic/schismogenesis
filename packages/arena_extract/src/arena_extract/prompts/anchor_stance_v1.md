# Stances on the fingerprint statements (anchor_stance_v1)

You read one public thinker's accepted claims and decide, for each of 24 statements, whether their own words show they **hold** it, **reject** it, or are **silent** on it.

Rules:
- **Hold** only if one of their claims states the statement or directly entails it. **Reject** only if a claim states or directly entails its negation. A claim that is merely on the same topic means silent.
- Every hold or reject cites exactly one `claim_id` from the list, plus a `quote`. The quote is a verbatim substring of that claim's `quote` field, 280 characters or fewer, and is the shortest passage that carries the stance.
- Don't infer from their reputation, their camp, or what people like them usually think. Use only the claims given. When in doubt, silent.
- Read the statement exactly. "Advanced AI poses a real risk of human extinction" is held by someone who says extinction risk is real even if small. It is rejected by someone who says the risk is negligible or the idea is incoherent.
- Give a one-sentence `why` for each hold or reject.

Output JSON only, with this shape:

```json
{"person": "<id>", "reader": "<A or B>", "stances": [
  {"statement": "<statement id>", "stance": "hold" | "reject", "claim_id": "<uuid>",
   "quote": "<verbatim substring>", "why": "<one sentence>"}
]}
```

Leave silent statements out of the list.
