# Audit v1: blind fidelity audit of accepted claims

Auditor: independent blind review of `evals/queue/audit-v1/sample.json`. Item ratings are in `evals/results/audit-v1.json`.

Basis: each proposition was judged against its supplied paragraph only. The auditor did not read the pipeline, its other outputs, or the full source works.

## Overall

- Items: 108 (9 each from 12 authors)
- **M5 (yes=1, partly=0.5, no=0): 0.875**
- Fidelity: yes 82 (75.9%), partly 25 (23.1%), no 1 (0.9%)
- Voice: own 105 (97.2%), unclear 2 (1.9%), other 1 (0.9%)
- Sensitivity: strictly faithful share (yes only) is 0.759. Counting unresolved-reference items as yes would give M5 0.912.

## Counts per author

| Author | yes | partly | no | own | unclear | other | M5 |
|---|---|---|---|---|---|---|---|
| Alex Karp | 8 | 1 | 0 | 9 | 0 | 0 | 0.944 |
| Balaji Srinivasan | 7 | 2 | 0 | 9 | 0 | 0 | 0.889 |
| Curtis Yarvin | 8 | 0 | 1 | 9 | 0 | 0 | 0.889 |
| Dario Amodei | 6 | 3 | 0 | 9 | 0 | 0 | 0.833 |
| Eliezer Yudkowsky | 7 | 2 | 0 | 9 | 0 | 0 | 0.889 |
| Elon Musk | 6 | 3 | 0 | 9 | 0 | 0 | 0.833 |
| JD Vance | 6 | 3 | 0 | 9 | 0 | 0 | 0.833 |
| Marc Andreessen | 8 | 1 | 0 | 9 | 0 | 0 | 0.944 |
| Nick Land | 5 | 4 | 0 | 6 | 2 | 1 | 0.778 |
| Peter Thiel | 7 | 2 | 0 | 9 | 0 | 0 | 0.889 |
| Sam Altman | 7 | 2 | 0 | 9 | 0 | 0 | 0.889 |
| Vitalik Buterin | 7 | 2 | 0 | 9 | 0 | 0 | 0.889 |

## Items rated no or other

- **Curtis Yarvin**, A Formalist Manifesto (`01a0d5d9-fc3f-4940-ba2e-577ab8048f98`), fidelity no, voice own. Misreads 'the same thing'. Yarvin means your 2007 beliefs would stay the same if carried to 1907, where they would be radical, so moderation is relative and not a position. The rest of the paragraph (the list of 2007 views voiced in Vienna) shows this. The proposition instead has him say one should find Vienna 1907's status quo righteous, which is a different claim.
- **Nick Land**, The Dark Enlightenment, Part 1 (`10e6c303-cfbf-4fda-af4e-ce373801c14e`), fidelity partly, voice other. Land reports what Lind and the neo-reactionaries seem to agree on. The proposition drops 'seem' and 'or even'. Its content is a description of others' view, so it should not be used as evidence of Land's own stance, though he may share it.

## Items rated unclear on voice

- **Nick Land** (`7261393a-8be8-48ea-9000-289d5726c115`), fidelity yes. Fidelity is fine. Voice: same doubt as the companion item from this paragraph; the paragraph alone cannot show whether this is Land's thesis or exposition of the neo-reactionary case.
- **Nick Land** (`24ca00e3-102a-4674-b9e8-7817376d05f9`), fidelity partly. Drops the qualifier 'short of instantaneous social collapse ...'. Voice: unattributed and strongly stated, but other Part 1 paragraphs in this sample report neo-reactionary positions, and the paragraph alone cannot show whether this is Land's thesis or free-indirect exposition.

## Patterns in the partly ratings

- **Scope or context lost (11 items).** The sentence is restated accurately, but what limited it sits elsewhere in the paragraph: a scenario, a comparison set, a stated exception, or a we/our that gets widened or moved. This is the most serious pattern, because the quote gate passes these by design: the words really are in the source.
- **Unresolved reference (8 items).** 'This', 'current' and 'under discussion' are carried over, or a subject is dropped, so the proposition cannot stand alone. These hurt comparison between authors more than they hurt fairness.
- **Dropped hedges (5 items).** 'I suspect', 'seems' and 'I have no fear' get removed or turned into impersonal facts. First-person stance is treated as removable framing, and sometimes it is the commitment itself.
- **Unneutralised wording (1 item).** The author's loaded metaphor is carried over unquoted.
- **Rejected items.** Of 3 `rejects` items, the two plain negations are sound. The third embeds premises in the rejected content, which is the failure mode to watch for this attitude.

## Fairness flags and data issues

- **Thiel on suffrage** (`2143be46-8e1c-4e09-80ef-ba2a41e599ea`) is rated yes, but it should not surface without his addendum. That rests on the auditor's memory of the addendum's content, which is not verified here. The sample's only addendum paragraph does not cover it.
- **Yudkowsky on GPUs** (`6ff7f2fa-dda9-4adf-98b7-a1ad31368680`): the disclaimer that he does not actually advocate this is in a different paragraph of the same work, so a paragraph-level check cannot see it.
- **Land's voice** cannot be settled from single paragraphs. Part 1 moves between reporting neo-reactionaries and speaking for himself. Any map placement of Land should get a check against the full work.
- **Attitude values:** 3 items use `accepts_conditionally`, outside the two values in the audit brief. They were audited as commitments to the conditional.
- **Source contamination:** 8 JD Vance paragraphs contain news-taxonomy labels (for example 'Society > Values > Ethics') mixed into the transcript text. None reached a proposition, but they are not Vance's words and should be stripped upstream.

## Limits

- This measures precision on accepted claims only. It says nothing about what the pipeline missed or wrongly discarded.
- 108 items across 12 authors gives per-author M5 very little resolution: one rating moves an author's score by about 0.06.
- The rater is a single judge, and the yes/partly boundary for unresolved references is a judgment call, as the sensitivity figure above shows.
