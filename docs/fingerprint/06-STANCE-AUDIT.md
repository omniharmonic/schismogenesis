# The stance audit (2026-11-03)

Owner: Benjamin Life. Run by Claude on 2026-11-03, at Benjamin's direction (D-31.19): "we need the stances to be iron clad. please use a swarm to validate all of the claims and make sure the atlas is fully documented with rich, high quality statements from all of the figures. Kingsnorth is OBVIOUSLY not a builder."

## What was checked, and how

**1. Every stance on the 24 statements** (protocol `stance_audit_v1`, `scripts/stance_audit.py`)
- Two blind readers per thinker covered all 54 thinkers. Each read every text we have by that person, in full, and decided hold, reject or silent on each statement. Readers never saw the old stances or each other's answers.
- Code checks every quote verbatim against that person's own text. Quotes are 280 characters or fewer. A quote that isn't found invalidates the stance.
- A stance is published only if two independent readings support it. Either both blind readers found the same side, or one did and a third reader confirmed it after reading the source around the quote (protocol `stance_adjudicate_v1`).
- Readers were told to watch for the mistakes that misrepresent people:
  - a lament or warning read as endorsement;
  - an opponent's or a quoted person's view;
  - irony;
  - a hypothetical or a story;
  - scope drift;
  - a forecast read as a value.
- **Round 3.** Fourteen thinly read voices were read again from all their works. That included 52 new works in their own voice, found and byline-checked by source researchers (`seed/AI-FUTURES-SOURCES-v3.json`). The round-3 reading replaces round 1 for those voices.

**2. Every other quoted holding on the atlas** (protocol `holding_audit_v1`, `scripts/holding_audit.py`)
- These 1,073 holdings had already passed a verbatim quote check, an entailment model and a blind second reader.
- Validators now read each source in full, and kept a holding only if the thinker is the one speaking, in their own voice, and the passage in context shows the position.

**3. Signature positions.** Each thinker has 3 to 6 positions in neutral words, each with a verified quote (`seed/thinker-voices.json`). They are shown first on the thinker's card.

## Results
**Stances on the 24 statements:**
- **Round 1.** 30 readers covered 54 thinkers. Where both blind readers took a side, they never picked opposite sides.
- **Third reader.** 78 stances only one reader found went to a third reader, who confirmed 41, judged 37 silent and judged none wrong-side.
- **Round 3.** 18 more readers covered 14 thinly read voices, from 50 usable new works (52 found; 2 were later excluded as not the person's own words). The 19 new one-reader stances: 11 confirmed, 8 judged silent.
- **Final:**
  - **426 stances**: 381 found by both blind readers, 45 confirmed by a third reader;
  - zero opposite calls between blind readers;
  - zero wrong-side rulings across all 97 third readings;
  - 425 are shown (Karpathy's one stance isn't enough to show him).
- **Against the stances shown before the audit:**
  - 246 confirmed, 0 flipped;
  - 51 not re-confirmed and removed;
  - 180 new.
- **Every thinker shown now has at least three audited stances**, the minimum for comparison.

**Other holdings on the atlas:** 1,073 were checked in context.
- 890 kept;
- 182 dropped as not supported in context, typically a real quote that says something narrower or different;
- 1 dropped as the wrong speaker: an official White House document rather than Alondra Nelson's own words;
- none on the wrong side.

**Schools:**
- 27 core voices keep their season-1 schools.
- Of the 28 other voices:
  - 10 clearly hold a school's distinctive positions and join it;
  - 4 sit between two schools;
  - 14, including Kingsnorth, have too few distinctive positions yet to group.

**Signature positions:** all 55 thinkers have 3 to 6.

## Sources found not to be the person's own words
Each is excluded at the root with a reason (seed `exclude`), so none of its claims count for anyone:
- an essay by Andy Hall in the Roots of Progress Intelligence Age series, filed under Jason Crawford (32 claims);
- a third-party summary page of a Balaji Srinivasan podcast;
- "Pygmalion's Passion" on Kingsnorth's Substack, almost all by a guest author, Andrew Caspersen;
- a third-party summary of Karpathy's YC keynote.

## Source problems the readers flagged
These were handled in the audit: readers only quoted passages clearly in the thinker's own voice. They still matter for future reading.
- **Unlabelled interview transcripts:**
  - Aschenbrenner and Zuckerberg (Dwarkesh);
  - LeCun (Lex Fridman);
  - Musk (Neuralink episode);
  - Acemoglu (Jon Stewart);
  - Korinek (FLI, CAIP);
  - Nelson (Edge).
- **Long quotation of others:**
  - Zvi Mowshowitz's posts;
  - Land's Dark Enlightenment (quoting Thiel and Moldbug);
  - Yarvin (quoting Andreessen);
  - Marcus (quoting Hartzog and Silbey);
  - Siddarth's review of Scharre;
  - Kingsnorth (quoting Yudkowsky, Harris and Raskin);
  - Merchant (worker testimony).
- **Generated summaries:** the Sacks a16z page and the opening of Siddarth's TED file.
- **Duplicates:** two Tang lecture files, two Nelson files, two LeCun files and two Sanders op-eds are identical.
- **Truncated by the 4,000-word fetch limit or the source:**
  - Andreessen's "Why AI Will Save the World";
  - Alexander's "Meditations on Moloch";
  - Gebru's TESCREAL paper;
  - Hanson's "Reasonable AI Fears";
  - Weyl's two essays.
- **Co-authored:**
  - Narayanan (with Kapoor);
  - Gebru;
  - Weyl's Plurality chapters;
  - MacAskill's Forethought papers.
- **Off topic:** none of Thiel's first five texts addressed AI.

## Why Kingsnorth was placed among the Builders, and what changed
- **One lament counted three times.** "The rise of the Machine was never going to stop… it will consume and colonise everything" was read as three positions, including fatalism about technology. Both audit readers rejected those readings.
- **Forecasts counted as values.** His agreement with Altman was all forecasts: AI is transformative, unstoppable, risky. On values they disagree.
- **No place on the map for his view.** The atlas has no ideas or school for a religious and ecological critique of "the Machine". His signature positions now show it: *the sacred and the digital are fundamentally opposed; technology is not neutral; the digital revolution is a spiritual crisis.*

**What changed: schools are now decided by distinctive positions.**
- A voice outside the core joins a school only when it clearly holds the positions that set that school apart (`school_fit` in `scripts/build_atlas.py`). Positions nearly everyone holds count for nothing, and forecasts count half.
- **Close fit to two schools:** the voice is shown *between* them.
- **Too little evidence:** the voice is shown as *not yet grouped*.

## New categories
The data doesn't yet support a new school. On the 24 statements, the progressive critics (Gebru, Bender, Hao, Whittaker) and the faith-grounded critics (Hawley, Pope Leo XIV, Kingsnorth) agree on every statement they both speak to. The one exception is "AI is a new kind of mind".

What separates them is the sacred against the secular, meaning against justice, and that isn't measured this season. **Proposal for season 2:** add statements that measure it, then let the data say whether a "faith and the Machine" school forms.
