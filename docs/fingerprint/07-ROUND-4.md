# Round 4: beyond tech voices (2026-11-03)

Owner: Benjamin Life. Run by Claude at Benjamin's direction (D-31.20): widen the map to the people who argue about AI and the social contract, make the survey represent them, redraw the schools, and check how the statements overlap and cluster.

## What was done
1. **New voices, own words only.** Ten source researchers looked for 4–6 own-voice works per person, each checked by fetching it: op-eds, speeches, testimony, letters, labelled transcripts (`seed/AI-FUTURES-SOURCES-v4.json`). A gap round then looked for people on the under-recorded side of each new statement (`seed/AI-FUTURES-SOURCES-v5.json`).
   - Politics: Elizabeth Warren, Chris Murphy, Ro Khanna, Alexandria Ocasio-Cortez, Richard Blumenthal, Lina Khan, Ted Cruz, Marsha Blackburn, Michael Kratsios, Ron DeSantis, Gavin Newsom, Scott Wiener, Andrew Yang, Pete Buttigieg, Barack Obama, Chuck Grassley; deeper reading of Bernie Sanders.
   - Whistleblowers and insiders: William Saunders, Frances Haugen, Miles Brundage, Steven Adler, Jan Leike.
   - Attention and public intellectuals: Tristan Harris, Jonathan Haidt, Yuval Noah Harari, Shoshana Zuboff, Jaron Lanier, Stuart Russell.
   - Labour and economics: Liz Shuler, Sean O'Brien, Duncan Crabtree-Ireland, Erik Brynjolfsson, David Autor, plus the gap round's economists.
   - Civil rights: Joy Buolamwini, Safiya Noble, Ruha Benjamin, Kate Crawford, Rumman Chowdhury, Cory Doctorow.
   - Faith and business: Russell Moore, Reid Hoffman, Fei-Fei Li, Jensen Huang, Ezra Klein.
   - Not sourced to the standard: Steve Bannon and Tucker Carlson (no own-voice text that loads), Sara Nelson (nothing on AI in her own voice).
2. **Fixes from the last pass.** Texts cut off at 4,000 words were fetched again at up to 10,000 (105 grew, 835k to 1.2M words). Five duplicate files are marked `duplicate_of`. Excluded as not the person's own public words: two machine-written Sacks summary pages, four transcripts with no speaker labels (Acemoglu with Autor, Korinek ×2, Nelson at Edge), an official White House document under Nelson, a Hassabis summary page, a Neuralink transcript, a possibly misattributed e/acc post, an AI-written Karpathy summary, two empty DeSantis pages and a leaked private Zuckerberg meeting. Thiel, Karpathy, Zuckerberg, LeCun, Hassabis, Aschenbrenner, Karp and the 14 previously ungrouped voices got new works.
3. **A pool of 51 statements.** The 24 season-1 statements plus 27 new ones on AI and the social contract. Two blind reviewers checked the new drafts. They agreed on slant in 10 (rewritten from their suggestions) and both proposed four missing questions (liability, a tax on replacing workers, local power over data centres, bias audits), which were added with four more (`seed/drafts/round4-pool.json`).
4. **Every person read on all 51 statements.** Two blind readers each read everything we have by each person (34 packs, 68 readings, `stance_audit_v2`). Then a gap round: 4 packs, 8 readings. Third readers ruled on every stance only one reader found (`stance_adjudicate_v1`) and on conflicts (`stance_conflict_v1`).

## Results
- **1,039 audited stances** on 51 statements for 125 people.
  - 886 found by both blind readers, 78 confirmed by a third reader, 35 matching the earlier audit, 40 carried from the earlier audit where the new readers were silent.
  - Blind readers never picked opposite sides.
  - Third readers judged 63 single-reader stances silent and none wrong-side.
- **Against the earlier audit:** 423 of 426 stances confirmed, none flipped. The other three were lost because their source texts changed when fetched again.
- **The survey: 27 statements, 9 per set** (`seed/season-2.json`). 17 come from season 1. The 10 new ones are about jobs, concentration of power, shared truth, AI companionship, work and dignity, whether AI leaders are honest about risk, paying creators, state AI laws, income not tied to work, and autonomous weapons.
  - Dropped: statements nearly everyone on record agrees on (binding rules for frontier AI 52 to 3, planning control early 31 to 1, technology's direction is chosen 45 to 6), plus three with too few people on record.
  - Liability, whistleblower protection, workers' say, antitrust and public AI were left out for the opposite reason: no one on the record yet takes the other side.
- **Shown: 88 people, 659 stances on the 27 statements.** People with fewer than 5 audited stances are not shown yet (41, mostly from the gap round, plus Khan, DeSantis, Newsom, Haugen, Leike and Klein).

## Schools (redrawn)
Drawn among the 36 people with 12 or more stances (`scripts/draw_schools.py`, `seed/drafts/round4-instrument.json`). Method:
- agreement over shared statements only;
- each statement weighted by 1 / its total |correlation| with the others, so one axis asked five ways gets about one vote;
- Ward groups in a 5-axis weighted MDS embedding;
- the count chosen by survival when the statements are resampled.

Four is the largest count that stays above 0.6 (adjusted Rand 0.62; five falls to 0.54).

| School | Drew it | Joined |
|---|---|---|
| Human-first critics | Obama, Merchant, Acemoglu, Weyl, Lanier, Hawley, Hao, Whittaker, Kingsnorth, Pope Leo XIV, Gebru | Narayanan, Tang, Autor, Siddarth, Zitron, Bender, Shuler, Benjamin, Chowdhury, Zuboff |
| Free-market builders | Sacks, Ball, Verdon, Vance, Andreessen, Kratsios, Hanson, Cruz, LeCun | Thierer, Srinivasan, Jeffries, Zuckerberg, Hoffman, Cowen |
| Public-interest safety | Sanders, Murphy, Hassabis, Elmore, Tegmark, Russell, Harris, Bengio, Mowshowitz | Toner, Clark, Suleyman, Khanna, Buterin, MacAskill, Saunders, Harari |
| AGI is near | Kokotajlo, Yudkowsky, Musk, Aschenbrenner, Noah Smith, Altman, Scott Alexander | Korinek, Faggella, Amodei |

- **Between two schools (16):** Ocasio-Cortez, Nelson, Yang, Patel, Warren, Marcus, Hinton, Haidt, Buolamwini, Blackburn, Brundage, Buttigieg, Blumenthal, Noble, Hammond, Wiener.
- **Not yet grouped (9):** Doctorow, Yarvin, Brynjolfsson, Li, Crawford, Huang, Land, Thiel, Rao.

**Why Sanders is no longer with Altman.** Unweighted, the strongest split is extinction risk, and Sanders, Harris, Altman and Yudkowsky agree on all of the 5 to 10 statements each pair shares. Weighting down the many overlapping risk statements lets the social-contract statements count, and the risk camp separates. Public-interest safety wants AI slowed and governed, and rejects racing China. AGI is near expects a new kind of mind to arrive regardless, trusts lab leaders on risk, and favours sharing wealth directly. Kingsnorth now sits with the human-first critics, as the faith-and-progressive overlap found in the last audit suggested.

## How the statements intersect (the checks)
- **Effective dimensions:**

  | | Participation ratio | Axes beyond shuffled data |
  |---|---|---|
  | 51-statement pool | 24.5 | 4 |
  | 27-statement survey | 11.3 | 2 |
  | Old 24 | 10.2 | 3 |

  The new survey spreads its information more evenly than the old one. The top eigenvalue is 5.9 of 27, against 5.5 of 24.
- **Near-duplicates:** none above the threshold (shrunk |phi| 0.75). Both reviewers flagged guaranteed income and direct distribution of wealth as overlapping; the data separates them enough to keep both.
- **Recovery.** A grouped person answering as themselves finds a member of their own school first 86% of the time, and one in their top three 94%. The old 24 statements give 83% and 94% on the same people.
- **Placement.** The map position and the school come from the same agreement measure, so a dot no longer sits inside a school it doesn't belong to. This is the fix for the Kingsnorth case.

## For Benjamin's review (E9)
- **Every new name** is Claude's proposal at your direction.
- **Anthropic ties**, disclosed on the About page: Amodei, Clark, Leike, Korinek, Siddarth, Huang (Nvidia invested), Newsom (state partnership), Wiener (Anthropic backed SB 53).
- **Other industry ties:** Lanier and Crawford (Microsoft), Ball (OpenAI), Kratsios (Scale AI), Hoffman and Huang (commercial interests).
- **Thinly sourced:** Ocasio-Cortez and Blumenthal (committee remarks only), Klein (0 stances), Crabtree-Ireland and O'Brien (1–2 works).
- **The school names** are working labels: Human-first critics, Free-market builders, Public-interest safety, AGI is near.
