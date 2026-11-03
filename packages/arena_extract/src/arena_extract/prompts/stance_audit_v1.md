# Stance audit from full texts (stance_audit_v1)

You are one of two blind readers. For each thinker in your pack, read **every one of their texts in full** (the `path` files), then decide for each of the 24 statements whether the thinker, **in their own voice**, holds it, rejects it, or is silent. A second reader does the same without seeing your answers; only stances you both reach independently are published. People will see these as "what X thinks", next to the quote, so a wrong stance misrepresents a real person.

## What counts
- **Hold**: the thinker asserts the statement, or something that plainly entails it, as their own view.
- **Reject**: the thinker asserts its negation, or something that plainly entails the negation.
- **Silent**: everything else. On the same topic is not enough. Silence is never disagreement. When in doubt, silent.

## Traps that have already misplaced people. Check every stance against these
1. **Lament or warning versus endorsement.** "The Machine will consume everything" from a critic is a fear, not a forecast they welcome. It can support "AI is hard to stop" as their empirical view, but it never supports values or policies they oppose. Ask: would this person sign the statement as written, in the sense a quiz taker reads it?
2. **Reported, quoted or ventriloquised views.** Text describing what opponents, "the industry", "accelerationists" or "some people" believe is not the author's view. Neither is a steelman, a hypothetical, or a question.
3. **Irony, sarcasm and rhetorical framing.** Read the paragraph around the quote.
4. **Scope drift.** "Social media has been a disaster" does not reject "market-driven technological development is good for people" unless they generalise it. Match the statement's actual scope.
5. **Facts versus values.** Agreeing that AI is powerful or transformative is not agreeing that it is good. Keep empirical and value statements separate.
6. **Statement wording.** Judge the `statement` text as people see it; `meaning` clarifies it. "Advanced AI poses a real risk of human extinction" is held by anyone who says the risk is real, even if small, and rejected by anyone who calls it negligible or incoherent.

## Quotes
- Every hold or reject cites a `work` key from that thinker's works and a `quote`: a **verbatim** passage from that file, 280 characters or fewer. Copy it exactly, but you may drop markdown asterisks. Code checks it, and a quote that isn't found invalidates the stance.
- Choose the passage that carries the stance most clearly and that a fair reader would accept as showing it on its own. Prefer complete sentences.
- `why`: one sentence on why this passage shows the stance, mentioning context if it matters ("in a section arguing against X, the author says...").

## Signature positions
For each thinker, also write 3 to 6 **signature positions**: the views most central to how they think about AI and society, in neutral words they would sign. Include positions the 24 statements don't cover. Each has a `position` (one plain sentence, 25 words or fewer, no loaded words), a `work` and a verbatim `quote` that shows it. These describe the person on the map, so fairness matters more than coverage.

## Output
Write JSON only to the answer path you were given:

```json
{"pack": 0, "reader": "A", "thinkers": [
  {"id": "<thinker id>",
   "stances": [{"statement": "<statement id>", "stance": "hold" | "reject", "work": "<work key>",
                "quote": "<verbatim>", "why": "<one sentence>"}],
   "signature": [{"position": "<one sentence>", "work": "<work key>", "quote": "<verbatim>"}],
   "note": "<optional: anything a reviewer should know, e.g. a text that looks mis-attributed>"}
]}
```

Leave silent statements out. Cover every thinker in the pack. Use only the given texts: no outside knowledge of the person, their reputation or their camp.
