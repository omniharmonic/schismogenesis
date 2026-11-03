# Holdings in context (holding_audit_v1)

The atlas shows, for each thinker, ideas they hold or reject, each with a short quote from their own work. Earlier checks confirmed every quote is verbatim, that an entailment model links it to the idea, and that a second reader agreed. None of those checks read the source **around** the quote. You do.

For each work in your pack:
1. Read the source file at `path` in full (use the Read tool, in parts for long files).
2. For each holding drawn from it, find the `quote` and rule:
   - `keep`: the `thinker` is the one speaking, in their own voice, and in context the passage shows they `accepts` (or `rejects`) the `idea`. A fair reader would accept the quote as showing it.
   - `wrong_speaker`: someone else is speaking. That includes an interviewer or host, another panelist, a narrator, a co-author's clearly separate section, an auto-generated summary, or a passage the thinker is quoting (another writer, a press release, a tweet, a manifesto).
   - `not_supported`: it is the thinker's voice, but in context the passage doesn't show this position. That covers a hypothetical, a scenario or story, a steelman of the other side, irony, a lament read as endorsement, a forecast read as a value, a much narrower or broader claim, or a view they say they have abandoned.
   - `wrong_side`: in context the passage shows the opposite side.
3. When in doubt, don't keep. A wrong quote puts words in a real person's mouth.

Write JSON only, to the answer path you were given:

```json
{"pack": 0, "rulings": [{"key": "<holding key>", "work": "<work key>", "ruling": "keep" | "wrong_speaker" | "not_supported" | "wrong_side", "reason": "<one short sentence; required unless keep>"}]}
```

Cover every holding in the pack. Use only the source texts.
