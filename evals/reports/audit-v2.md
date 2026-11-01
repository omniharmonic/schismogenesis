# Audit v2: blind fidelity audit of accepted claims

Auditor: independent agent, blind to the pipeline. Sample: 104 accepted claims, 8 from each of 13 authors. Date: 2026-10-31.

## Result

- **M5: 0.865** (yes=1, partly=0.5, no=0). Rough 95% interval: 0.819 to 0.912.
- Fidelity: yes 78 (75.0%), partly 24 (23.1%), no 2 (1.9%).
- Voice: own 102, unclear 1, other 1. **Share `other`: 1.0%.**

No threshold was given to this audit, so none is applied here. The interval is wide because the sample is small. Per-author figures rest on 8 items each and are not a ranking of how fairly anyone was treated.

## Counts per author

| Author | yes | partly | no | own | unclear | other | M5 |
|---|---|---|---|---|---|---|---|
| Dario Amodei | 5 | 2 | 1 | 8 | 0 | 0 | 0.750 |
| Alex Karp | 5 | 3 | 0 | 8 | 0 | 0 | 0.812 |
| David Sacks | 5 | 3 | 0 | 8 | 0 | 0 | 0.812 |
| Elon Musk | 5 | 3 | 0 | 8 | 0 | 0 | 0.812 |
| JD Vance | 5 | 3 | 0 | 8 | 0 | 0 | 0.812 |
| Nick Land | 5 | 3 | 0 | 8 | 0 | 0 | 0.812 |
| Balaji Srinivasan | 6 | 2 | 0 | 8 | 0 | 0 | 0.875 |
| Peter Thiel | 7 | 0 | 1 | 7 | 0 | 1 | 0.875 |
| Curtis Yarvin | 7 | 1 | 0 | 7 | 1 | 0 | 0.938 |
| Eliezer Yudkowsky | 7 | 1 | 0 | 8 | 0 | 0 | 0.938 |
| Marc Andreessen | 7 | 1 | 0 | 8 | 0 | 0 | 0.938 |
| Sam Altman | 7 | 1 | 0 | 8 | 0 | 0 | 0.938 |
| Vitalik Buterin | 7 | 1 | 0 | 8 | 0 | 0 | 0.938 |

## Every no or other item

1. **Peter Thiel, The Straussian Moment** (`62dfd42f`), no / other. The claim that violent debates about truth interfere with commerce was accepted as Thiel's own. In the source it opens a reconstruction of the Hobbes/Locke rationale: the next sentence says such questions are "best" eliminated, then "Thus, in Hobbes". This is a voice failure the pipeline's checks would not catch, since the quote is exact and the sentence is flatly declarative. It is the one judgment call among the no items; the paragraph alone leaves some room to read the first sentence as his own observation.
2. **Dario Amodei, The Adolescence of Technology** (`257c714a`), no / own. One bullet from a multi-part list was turned into "Powerful AI is defined as" an AI that does long tasks autonomously. The full definition also requires intelligence beyond Nobel winners across fields and full virtual interfaces. The rewrite describes something close to existing agents, so it distorts his timeline claims too.

## Worst partly items

- **David Sacks** (`0f268619`): a concession inside an argument for diplomacy was extracted as "The West cannot cower before Putin's threats". The passage's turn is dropped and "we" was changed to "The West". This is the item closest to a no.
- **Alex Karp** (`e9be209c`): "must be willing to expose" became "must be exposed". The claim got stronger.
- **Sam Altman** (`15622f58`): "some regulation", "I think" and his stated view that technology is often over-regulated all disappear.
- **Marc Andreessen** (`a63154a8`): "we've failed you" became "a failure of society", and helping people find work became the worker "should be moved".
- **JD Vance** (`09aa09be`): a report of an endorsement became a "should" claim, labelled as stated.

## Patterns

1. **Sentence-level extraction loses argumentative function.** The serious errors are not misquotes. Each sentence is accurate, but its role (concession, premise of someone else's reasoning, sardonic set-up, conclusion from a premise) is lost. See Thiel, Sacks, Yarvin `3e4d2d3f`, Land `9a8b1d3f`. The exact-quote gate cannot catch this, and it matters most for authors who write in layered or ironic styles.
2. **Rewrites strengthen more often than they weaken.** Limits, quantifiers and "I think" get dropped: Altman, Musk `62305fd5`, Karp `654e2d09` and `e9be209c`, Vitalik `f95ecf39`, Land `c4f77645`.
3. **'We' is resolved by guesswork.** Resolved 'we' and 'our' are often wrong or too broad (Sacks, Karp `ac33430b`, Andreessen), or are left unresolved (Vance `44ddbc6f`, Land).
4. **Context is imported without marking, and references are left unresolved.** The subject can come from outside the paragraph (Amodei, Musk). Elsewhere a reference stays unresolved (Balaji `4de88909`, Land `196cf7b2`, Yudkowsky `f6fc01e9`).
5. **Scare quotes added around charged terms.** The source has no such marks for Sacks's "demented", "invade" and "Border Czar", or Balaji's "virtue signalers". The sneer reads as the pipeline's, or as the author distancing himself. Where the author's own evaluative words are simply kept, this audit did not penalize them, because the evaluation is the claim. Mild cases that target nobody (Andreessen's "smashmouth", `86348523`; Land's "paper-clippers") were also not penalized.
6. **Forecasts have no anchor date.** 'In 36 months' and '1-2 years away' are unresolved references (Musk `2e440d0c`, Amodei `214fa4f5`, `23cc5101`). This is mechanical and cheap to fix. Without these 3 items' penalties, M5 would be 0.880.
7. **Low-value claims pass.** Ceremonial lines (Vance `44ddbc6f`, `a12032fa`) are accepted as propositions. The second was scored yes because it is accurate, but neither is much of a position.

## What the pipeline does well

Negation handling held up (Amodei `ef47cda4`). Rhetorical questions were resolved correctly (Sacks `820a39bf`, `a22aa82b`). Hedges such as "may" and "could" usually survive, and Altman's self-correction on the ring of power (`98cf3ee7`) was captured correctly. No item reversed an author's meaning.

## Method and limits

- Judged against the paragraph in each sample item, as instructed. Local source texts in `data/texts/` were read where the paragraph could not settle voice or scope: Thiel `62dfd42f`, the Moloch's Toolbox passages behind Yudkowsky's four items (the surrounding text shows narrator voice, not a dialogue speaker), Yarvin `3e4d2d3f` and Amodei `257c714a`. Andreessen `dbf04b71` was also checked and stood. No pipeline output, prior audit or code was read.
- The sample shares paragraphs across items (for example Land, Musk and Yudkowsky), so items are not fully independent and the true interval is somewhat wider.
- Attitude values include `accepts_conditionally`, which was not in the audit brief. Where it appears (`bb8b6657`, `a22aa82b`, `2e66d6af`) the proposition already contains the 'if', so the condition is stated twice. Scored on meaning, not penalized.
- The Little Tech Agenda items are listed under Andreessen alone. The work's byline should be confirmed against the source.
