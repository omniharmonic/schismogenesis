# Third reading of a disputed stance (stance_adjudicate_v1)

Two blind readers read a thinker's full texts. One of them found a stance on a statement and the other found the thinker silent. You are the third reader. For each item, decide whether the stance holds up.

For each item:
1. Open the source file at `path` and find the `quote`. Read at least the whole section around it, and enough of the piece to know what the author is arguing.
2. Decide what the passage, in context, shows about the thinker's **own** view on the `statement` (as people read it; `meaning` clarifies):
   - `confirm`: the passage is the author asserting, in their own voice, the `proposed` side (hold = they agree with the statement, reject = they disagree). A fair reader would accept the quote as showing it.
   - `wrong_side`: the passage shows the opposite side.
   - `silent`: everything else. That includes a related topic but not this statement; a lament or warning read as endorsement; someone else's view being reported, quoted or steelmanned; irony; a hypothetical or scenario; a narrower or broader claim than the statement; facts read as values; or a quote that only works with outside knowledge.
3. When in doubt, `silent`. A wrong stance misrepresents a real person to everyone who takes the quiz; a missing one costs little.

Write JSON only to the answer path you were given:

```json
{"rulings": [{"key": "<item key>", "ruling": "confirm" | "wrong_side" | "silent", "reason": "<one sentence>"}]}
```

Cover every item. Use only the source texts, never what you know of the person's reputation.
