# Widening and deepening the Lifeworld Atlas

Owner: Benjamin Life. Drafted by Claude, 2026-11-03, from Benjamin's direction of the same day: "make sure we also do a widening and deepening of the lifeworld atlas. there are plenty of important voices we are missing and many we need more from."

## Status (2026-11-03, end of day)
- **Done.** Steps E1–E6 and E8, in two rounds:
  - **Fetched and extracted:**
    - 179 works fetched by a deterministic extractor, with failures replaced;
    - 1,197 extraction tasks done by agents, every quote checked in code;
    - 6,316 accepted claims after quote anchoring and the local entailment gate.
  - **Two-reader stance passes:**
    - 281 stances agreed in total;
    - no opposite calls, and no contradictions with the atlas.
- **On the map.** 50 thinkers: 27 from the original atlas and 23 new voices, placed provisionally from the statements (dotted on the map). All eight schools are well covered and inside the fair-share band.
- **Still not shown.** Six voices whose public writing mostly doesn't take sides on these statements: Demis Hassabis, Helen Toner, Meredith Whittaker, Yann LeCun, Andrej Karpathy and Alondra Nelson. David Sacks has 2 stances.
- **E7 done (atlas-v2, bundle fp-2026-11-03.5).**
  - Two blind readers checked 1,648 proposed holdings (235 agreed) and 61 holdings on 22 candidate new ideas. 11 ideas were kept, each with two confirmed holders; the off-topic candidates all fell out.
  - **Schools are frozen for season 1**, like the statements. Clustering everyone together made a false school out of thinly read voices: centring treats silence as a view. With the new evidence, even the core 27 would regroup a lot (agreement with the frozen schools, adjusted Rand 0.36), so schools are a season-2 question.
  - The core 27 keep their schools and positions. The 27 other voices are placed by the fingerprint's own agreement rule, take their school by weighted vote of their three closest, and stay marked provisional.
  - 54 thinkers are shown. Still too thin to show: Karpathy and Hassabis.
  - **For Benjamin's review (E9):** placements that may draw objections are Zuckerberg and LeCun (Human-first critics), Kingsnorth and Toner (Builders), and Sacks, Toner, LeCun, Nelson and Whittaker, who have fewer than three stances on the statements.

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
