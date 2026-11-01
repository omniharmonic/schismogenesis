# Worldview graph from public works

Private page: https://claude.ai/artifact/Xj38hmkuZVQi7XAbXh1k9s

Sources are 51 public works by 13 people (`seed/WORLDVIEW-CORE-SOURCES.json`). Results are in Neon.

| Step | Result |
|---|---|
| Claims proposed | 1,562 (576 prompt v1, 986 prompt v2) |
| Quote anchoring, M6b | 1,562 of 1,562 exact, 100% |
| Accepted after validators, entailment and audits | 908 |
| Blind audits | v1 M5 0.875 (n=108); v2 M5 0.865 (n=104) |
| Questions | 26 drafted, 25 kept |
| Positions | 85 kept, 27 of 88 drafted flagged as bundled |
| Links | 299 drafted, 246 agreed, 2 differ, 51 unplaced, 237 after final review |

## Findings
- Prompt v2 did not raise fidelity, though it ran on harder texts. The main flaw is lost
  argumentative role: a concession or a reconstruction of someone else's view reads as assertion.
  Limit-carrying rules do not fix this, and neither do quote or entailment checks. The next step is
  to give extraction the argument around a sentence, or add a role check as a separate stage.
- `new_entity` rejected good claims once prompt v2 resolved references, because it only looked at the
  paragraph. It now checks the chunk, title and author, and has aliases. 117 claims were restored
  with logged events; 26 stayed rejected.
- Pair overlap suggests two groupings: Altman, Amodei, Musk and Buterin; and Vance and Andreessen.
  Yarvin sits far from most people. Thirteen people are too few for real clusters.

## Open
- v1 claims have not been re-extracted with v2.
- Land's "Meltdown" was dropped for lack of a verifiable date. National Review's "The End of the
  Future" was dropped because an archive copy may bypass a metered paywall.
- The Parachute note dates "The Straussian Moment" to 2004; the book was published in 2007. The vault
  note should be corrected.
- Spoken and written works are mixed, and Vance's speeches are likely staff-drafted.
- Lineage to deceased thinkers is still not in the graph.
