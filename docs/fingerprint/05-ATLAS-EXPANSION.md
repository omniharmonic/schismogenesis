# Widening and deepening the Lifeworld Atlas

Owner: Benjamin Life. Drafted by Claude, 2026-11-03, from Benjamin's direction of the same day: "make sure we also do a widening and deepening of the lifeworld atlas. there are plenty of important voices we are missing and many we need more from."

## Status (2026-11-03)
- **Done.** Steps E1–E6, plus E8, have run:
  - all 29 voices approved (D-31.18) and added to the seed;
  - 131 works fetched by a deterministic extractor, including 20 readable replacements for pages that failed;
  - 807 extraction tasks done by agents, giving 5,589 claims (every quote checked in code), then quote anchoring and the local entailment gate;
  - two blind readers per person on the 24 statements, for all 56 people. 206 stances were agreed, 101 of them new. There were no opposite calls and no contradictions with the atlas.
- **On the map.** 37 thinkers, of whom 10 are new voices placed provisionally from the statements alone (dotted on the map). Every school is now well enough covered to be checked by the balance test, and all eight are within the fair-share band.
- **Still thin.** 20 voices have fewer than 3 statements in common with the existing thinkers, so they aren't shown yet: Zvi Mowshowitz, Helen Toner, Leopold Aschenbrenner, Holly Elmore, Jack Clark, Alondra Nelson, Demis Hassabis, Mark Zuckerberg, Yann LeCun, Meredith Whittaker, Brian Merchant, Ed Zitron, Anton Korinek, Arvind Narayanan, Gary Marcus, Andrej Karpathy, Dwarkesh Patel, Venkatesh Rao, Noah Smith and David Sacks. Their first works talked around these statements, so round 2 looks for works where they take sides.
- **Not yet done.** E7, the structure pass that gives new voices real atlas positions and schools.

## 1. What's wrong now
- **Too few voices.** There are 27 thinkers. Many people the TPOT scene argues with or about are missing: lab leaders, forecasters, AI-ethics and labour voices, policy people, economists, "normal technology" sceptics, and the posters at the centre of the conversation on X.
- **Too thin on some.** Six thinkers have fewer than three stated positions on the 24 statements, so the fingerprint can't compare anyone with them: Sacks (0), Weyl (1), Balaji, Musk and Scott Alexander (2 each), and Crawford (3). The fix is reading more of their work. MacAskill and Tang are borderline.
- Each person is read from about 3 works. More works per person makes every measure steadier.

## 2. Principles
1. **The statements stay fixed for a season.** The 24 statements are the shared instrument. Results, profiles and comparisons over time all depend on them. Season 1 keeps them. A new statement set (season 2) can be chosen from the widened atlas later, with a clear break in the results.
2. **More stances on the same statements.** Deepening and widening mostly mean finding stated positions on the 24 statements, plus new ideas for the map. Same rules as before:
   - the exact quote is checked in code;
   - an entailment check;
   - a blind second reader;
   - silence counts as missing.
3. **Public figures, own voice, public work only.** Quotes stay at 280 characters or fewer, with links. Full texts stay in the git-ignored `data/`.
4. **Balance is measured, not asserted.** After widening, each camp's coverage on the statements is reported. The balance test in `apps/arena/tests` must still pass, and should then include Exit founders and Pluralists.
5. **Benjamin approves every new name.** Adding someone to a public map is an editorial act. Conflicts of interest are flagged, not hidden.

## 3. Steps

| Step | What happens | Who |
|---|---|---|
| E1 | Candidate voices and sources: 20–30 proposed people, plus 3 more works for each thin thinker → `seed/drafts/` | Claude (running) |
| E2 | **Benjamin approves the list** (add, cut, or reorder by priority) | Benjamin |
| E3 | New people enter the seed as landmarks (`seed/SEED-v5`), with niches and flags | Claude |
| E4 | Fetch and clean texts (own voice, at most 4,000 words each) into `data/texts/`, then `arena written ingest-list --sources seed/AI-FUTURES-SOURCES-v2.json` | Claude |
| E5 | Claims: `arena written extract-all --batch core-v4`, answered by subscription agents with prompt v2; then `check_batch.py`, then `gate-all` | Claude + agents |
| E6 | **Stances on the 24 statements (new, focused pass):** for each new or deepened person, readers decide from their accepted claims whether they hold, reject, or are silent on each statement, with a claim id and quote. A blind second reader has to agree. | Claude + agents |
| E7 | Structure extension: new claims either join existing ideas or form new ones, with blind second readings, then merge. Atlas v2 is rebuilt, with schools and stability rerun. | Claude + agents |
| E8 | Rebuild the bundle as `fp-…2`. The statements are unchanged; there are more thinkers and stances. Balance test, quote checks, and the flagged-name guard. | Claude |
| E9 | Benjamin reviews the new placements before launch, starting with the people most likely to object | Benjamin |

Step E6 is new, and it's what makes the fingerprint better quickly. Even without the full structure pass, it gives every thinker enough stated positions to be compared.

## 4. What changes for people who already took it
- **Old answers stay valid,** because the statements are the same.
- **Matches can change.** With more thinkers and stances, someone's nearest thinker may change. Published profiles keep the bundle version they were made with, and the page says so. A "see your updated result" link recomputes in the browser.
- **The results page** keeps working across the change, because it counts answers to the same statements.

## 5. Cost and time
- **No paid API.** The model work runs on the Claude subscription through agents, as before, and the entailment check runs locally.
- **Rough size:** 25 new people and 8 deepened people at 3 works each is about 100 works. That's roughly 1,500 to 2,500 claims to extract and check. In the earlier run, 93 works took several agent-hours across extraction, checks and the structure pass.
- **E6 is much smaller:** about 33 people × 24 statements.

## 6. Decisions for Benjamin
1. Approve, cut and prioritise the candidate list in `seed/drafts/ATLAS-EXPANSION-CANDIDATES.md` (once E1 finishes).
2. Confirm that the statements stay fixed for season 1 (Claude's recommendation).
3. Choose whether launch waits for widening, or launches with the deepened 27 and adds the new voices in a visible "new voices added" update. That update could be a news moment of its own.
