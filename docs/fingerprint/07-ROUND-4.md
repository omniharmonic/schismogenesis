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

## Camps, schools and close circles (redrawn twice; D-31.21)
Benjamin, after the first redraw: "we vastly over-simplified the schools. its too homogenous now. we need to be able to drill down from wider camps into more and more specific clusters until we get to a new degree of really tight clusters."

The four flat schools were the most a single cut could support. A hierarchy reads more out of the same evidence.
- **Evidence:** the survey pool plus every atlas idea at least 4 people took a side on, in their own words, with both sides present (80 statements). People with at least 10 positions draw the groups (56).
- **Consensus clustering** (`consensus`, `hierarchy` in `arena_fingerprint/instrument.py`). The groups are redrawn 300 times. Each time the statements are resampled with replacement, weighted down by overlap, and the number of groups is drawn at random from 3 to 14. Ward groups are formed in a weighted-MDS embedding. Counting how often each pair lands together gives a consensus matrix. Average linkage on it is cut at four depths: camps 25%, schools 42%, branches 60%, close circles 78%. A level that doesn't split a group is skipped. Every group reports its own cohesion (the mean share of redrawings in which two members land together).
- **Others** go down the tree only while they clearly agree with one group more than its siblings (`attach`). A person between two camps is shown between them.
- **Survey statements** are scored by how well they separate groups at the camp level and at the finest level, so the survey covers both.

- **AI as a new kind of risk** (36%): Bernie Sanders, Chris Murphy, Daniel Kokotajlo, Dario Amodei, Demis Hassabis, Eliezer Yudkowsky, Elon Musk, Geoffrey Hinton, Holly Elmore, Jack Clark, Leopold Aschenbrenner, Max Tegmark, Mustafa Suleyman, Sam Altman, Samuel Hammond, Scott Alexander, Stuart Russell, Tristan Harris, Vitalik Buterin, William Macaskill, William Saunders, Yoshua Bengio, Zvi Mowshowitz
  - **Slow it down and govern it** (64%): Bernie Sanders, Chris Murphy, Daniel Kokotajlo, Holly Elmore, Max Tegmark, Stuart Russell, Tristan Harris, Yoshua Bengio
    - **Stop and regulate** (69%): Bernie Sanders, Daniel Kokotajlo, Holly Elmore, Max Tegmark, Stuart Russell, Yoshua Bengio
      - **Kokotajlo and Bengio** (84%): Daniel Kokotajlo, Yoshua Bengio
    - **Murphy and Harris** (77%): Chris Murphy, Tristan Harris
  - **Rationalists and long-termists** (53%): Eliezer Yudkowsky, Elon Musk, Geoffrey Hinton, Scott Alexander, William Macaskill
    - **Yudkowsky, Musk and Alexander** (66%): Eliezer Yudkowsky, Elon Musk, Scott Alexander
    - **Hinton and MacAskill** (65%): Geoffrey Hinton, William Macaskill
  - **Security realists** (51%): Demis Hassabis, Leopold Aschenbrenner, Samuel Hammond
  - **Lab stewards** (64%): Jack Clark, Mustafa Suleyman
  - **Hopeful builders** (48%): Sam Altman, Vitalik Buterin
  - **Safety insiders** (52%): William Saunders, Zvi Mowshowitz
- **Human-first critics** (49%): Audrey Tang, Barack Obama, Brian Merchant, Daron Acemoglu, E Glen Weyl, Ed Zitron, Gary Marcus, Jaron Lanier, Josh Hawley, Karen Hao, Meredith Whittaker, Paul Kingsnorth, Pope Leo Xiv, Timnit Gebru
  - **Democratic humanists** (65%): Audrey Tang, Barack Obama, Brian Merchant, Daron Acemoglu, E Glen Weyl, Jaron Lanier, Josh Hawley, Karen Hao, Pope Leo Xiv
    - **Power and labour critics** (83%): Brian Merchant, Daron Acemoglu, E Glen Weyl, Jaron Lanier, Josh Hawley, Karen Hao
      - **Merchant, Acemoglu, Weyl, Hawley and Hao** (87%): Brian Merchant, Daron Acemoglu, E Glen Weyl, Josh Hawley, Karen Hao
  - **Hype and harms critics** (69%): Ed Zitron, Gary Marcus, Meredith Whittaker, Timnit Gebru
    - **Whittaker and Gebru** (85%): Meredith Whittaker, Timnit Gebru
- **Free-market builders** (42%): Balaji Srinivasan, David Sacks, Dean Ball, Guillaume Verdon, Jason Crawford, Jd Vance, Marc Andreessen, Mark Zuckerberg, Michael Kratsios, Robin Hanson, Ted Cruz, Tyler Cowen, Venkatesh Rao, Yann Lecun
  - **Human-centred builders** (50%): David Sacks, Dean Ball, Jd Vance, Marc Andreessen, Mark Zuckerberg, Michael Kratsios, Tyler Cowen, Yann Lecun
    - **Sacks and Andreessen** (64%): David Sacks, Marc Andreessen
    - **Vance and Kratsios** (78%): Jd Vance, Michael Kratsios
    - **Zuckerberg and LeCun** (67%): Mark Zuckerberg, Yann Lecun
  - **Accelerationists** (58%): Guillaume Verdon, Robin Hanson, Ted Cruz, Venkatesh Rao
    - **Verdon and Cruz** (69%): Guillaume Verdon, Ted Cruz
    - **Hanson and Rao** (65%): Robin Hanson, Venkatesh Rao
  - **Progress optimists** (56%): Balaji Srinivasan, Jason Crawford
- **Skeptics of hype and of pausing** (42%): Arvind Narayanan, Curtis Yarvin, Peter Thiel

Result: 4 camps, 11 schools, 11 branches, 2 close circles. 10 more people are placed into the tree, 12 sit between camps, and 12 are not yet grouped.

**Recovery.** A grouped person answering as themselves finds their own camp first 89% of the time (top three: 96%). They find their own school first 70% of the time (top three: 75%). The finer the group, the more statements it takes to tell it apart.

**On the site.** The Thinkers page and your result open on the camps. Selecting a camp redraws the map with its schools as regions, and so on down to close circles. Every group card shows a breadcrumb, its note, its cohesion, the groups inside it, its members, and where they agree and argue. A person's card shows their full path.

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
