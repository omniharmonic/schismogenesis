# Placing the public and key voices in one space, and tracking a few voices and questions (November 2026)

Evidence tags: **[F]** = read in extracted full text. **[A]** = abstract or publisher summary only. **[S]** = search snippet or secondary description only, not opened. Cambridge full text returned 403 errors, so several core political science papers are [A] or [S]. All "Inferences" are mine, not findings from the sources. All numbers in the design section are my starting proposals unless a source is given.

## Joint scaling of elites and masses: bridges, anchors, and how many are needed

### Takeaway
A common scale is buildable with few bridges, but it rests on the assumption that elites and the public read each item the same way, and that assumption fails for a sizeable share of people. No source gives a validated minimum bridge count: the best guidance is more than 20% of items under misfit, and one working political example used 7.

### Cited Findings
- Jessee shows the standard strategy of fitting ideal point models to citizens and elites together can suffer "potentially problematic pathologies". He offers a technique to test how assumptions and data choices affect estimates, and a way to constrain the dimension being estimated. [A] — [Jessee 2016 via IDEAS](https://ideas.repec.org/a/wly/amposc/v60y2016i4p1108-1124.html)
- A later article describes Jessee's check: use legislator item parameters to scale voters in "legislator space", and voter item parameters to scale legislators in "voter space". [S] — [Shiraito, Lo and Olivella, Cambridge](https://www.cambridge.org/core/product/4BF1AABAEA9A55F1CE488FD2F31F97EB/core-reader)
- Shiraito, Lo and Olivella re-analysed a survey where respondents voted on roll calls legislators had already voted on. Some voters can be compared safely with legislators, but a sizeable share read the items differently, and ignoring this can give wrong conclusions about representation. No percentage was in the abstract. [A] — [arXiv 2205.05934](https://arxiv.org/abs/2205.05934)
- Bafumi and Herron built bridges by asking mass respondents about the same items candidates took positions on. [S] — [Battista, Peress and Richman](https://www-cambridge-org.ezproxyberklee.flo.org/core/services/aop-cambridge-core/content/view/FE71BBF7A5EBA52AF909F31DEADC35B6/S204984702100042Xa.pdf/estimating-the-locations-of-voters-politicians-policy-outcomes-and-status-quos-on-a-common-scale.pdf)
- Walder placed Swiss voters and elites together using elite questions in a Bayesian item response model. Real data used 7 bridge questions out of 51 voting-advice questions, with 1,905 candidates and 7,375 people analysed in total. [F] — [Walder 2024](https://frontiersin.org/articles/10.3389/fpos.2024.1425406/full)
- Limits of Walder: it argues "a handful" suffices but does not test a minimum, does not discuss differential item functioning, and does not cite Jessee. Its reported simulation errors look internally inconsistent (root mean square error 14.9 with 7 items against 6.3 with 51), so I would not reuse those numbers. [F] — [Walder 2024](https://frontiersin.org/articles/10.3389/fpos.2024.1425406/full)
- In psychometric linking, a simulation of Rasch linking concludes anchors should exceed 20% of the test when misfit is present, at small to medium samples. [A] — [Fischer et al. 2021](https://doaj.org/article/53599c6075af4f7daeadbd0b5c7e8e86)
- A 2025 simulation varying anchors from 5% to 25% and tests from 20 to 80 items found recovery improves logarithmically, and highly discriminating anchors help. [S] — [Frontiers 2025](https://public-pages-files-2025.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1652341/pdf)
- Anchoring vignettes are an alternative bridge: fixed stimuli treat differences in placement as differences in interpretation. The attribution to Bakker, Jolly, Polk and Poole comes from a search summary and is unconfirmed. [S] — [Political Analysis article](https://www-cambridge-org.ezproxyberklee.flo.org/core/journals/political-analysis/article/capturing-rationalization-bias-and-differential-item-functioning-a-unified-bayesian-scaling-approach/B5EA395887034A9E555BE78B1974CEF9)
- Behavioural bridges exist. Barberá's Twitter model puts elites and ordinary users together from who follows whom, reproduces conventional legislator measures, and sorts registered partisans in Ohio as expected. [A] — [Barberá 2015](https://ideas.repec.org/a/cup/polals/v23y2015i01p76-91_01.html)
- Group-level alternatives avoid scoring individuals. Caughey and Warshaw estimate opinion for demographic or geographic groups, borrowing strength across groups and time. [A] — [Caughey and Warshaw 2015](https://dspace.mit.edu/handle/1721.1/106583)
- Tausanovitch and Warshaw scaled 275,000 Americans from surveys. [S] — [Measuring Constituent Policy Preferences](https://core.ac.uk/download/78052354.pdf)
- Machine-coded stances have already been used as survey-like responses. Burnham's Semantic Scaling classifies stance with a language model, then runs item response theory. It reports correlation 0.95 with DW-NOMINATE in Congress. Among the public it correlates 0.9 with Tweetscores. Where the two disagree, it matches human labels at 0.75 versus 0.18. It is a preprint. [F] — [Burnham 2024](https://arxiv.org/pdf/2405.02472)

### Inferences
- **Yes, machine-coded elite stances can act as anchor responses**, because Burnham's pipeline does exactly this in form. But nobody I found has tested text-coded elite stances against answers by the same public on the same items, so this exact link is unvalidated.
- Do not fit one joint model. With 27 thinkers, elites cannot calibrate items: 27 respondents is far too few for that. Calibrate items on the public alone, then score thinkers as respondents under those fixed parameters. Run Jessee's check in reverse where possible.
- Text-derived stances add a second source of mismatch beyond the elite-public gap: a written position and a survey answer are different acts.
- Current data can't support many bridges. About 10% fill over 27 by 360 gives about 2.7 stances per idea (my arithmetic from [structure.py](/Users/benjaminlife/dev/schismogenesis/packages/arena_map/src/arena_map/structure.py)). Bridges need targeted reading for each chosen statement, which supports the prior report's battery idea, but with thinkers scored on public-tested wording.

### Gaps
- No validated minimum bridge count for the elite-public case.
- Shor and McCarty, and Bonica's CFscores: not read directly.
- I could not find a Hill and Tausanovitch joint-scaling paper in search; that citation is unconfirmed.
- Boussalis: nothing found. I did not search it separately.

## Do elites and the public share a dimensional structure?

### Takeaway
Probably not in the same strength. Elite structure is constrained; much of the public is weakly structured, cue-driven or cross-pressured. So "near a thinker" can only mean "answers these items similarly", never "follows or belongs to this thinker's worldview".

### Cited Findings
- Kinder and Kalmoe argue ideological innocence still describes much of the public, that elite ideological battles appear in the public as scattered skirmishes, and that preferences arise more from group attachments. [S] — [publisher synopsis](https://blackwells.co.uk/bookshop/product/Neither-Liberal-nor-Conservative-by-Donald-R-Kinder-Nathan-P-Kalmoe/9780226452319)
- A recent reappraisal argues many people seen as moderates are conflicted, holding extreme views across issues that one dimension describes poorly. [S] — [Moderates, APSR](https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/4C8917D91FCFD7ECA74E5D2DB5C741FE/S0003055424001333a.pdf/moderates.pdf)
- Barber and Pope used real liberal and conservative Trump positions as cues. Low-knowledge respondents, strong Republicans, Trump approvers and self-described conservatives moved most, in either ideological direction. They conclude group loyalty motivates opinion more than ideology. [S] — [APSR 2019](https://www.cambridge.org/core/journals/american-political-science-review/article/abs/does-party-trump-ideology-disentangling-party-and-ideology-in-america/B5BAD0AE947BD3CF18D51D399263C8D3)
- Follow-up work finds personally important issues can resist cues that run against one's ideology. [S] — [PSRM note](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/556415944D298A98E9BE01C22800423C/S2049847023000286a.pdf/does_issue_importance_attenuate_partisan_cuetaking.pdf)
- Lenz argues people often choose a politician first and then adopt that politician's stances. [S] — [Follow the Leader?, publisher listing](https://chicagoreference.com/ucp/books/book/chicago/F/bo11644533.html)
- Watts and Dodds's simulations found large changes are mostly driven by easily influenced people influencing each other, not by opinion leaders, outside special cases. [A] — [Watts and Dodds 2007](https://pdodds.w3.uvm.edu/research/papers/years/2007/watts2007a.pdf)
- The two-step flow model has long been criticised as too simple; a test found a sizeable group influenced by media alone. [S] — [van den Ban](https://edepot.wur.nl/21986)

### Inferences
- A person who has never heard of Nick Land can still sit near him on items. That is a statement about responses, not lineage or influence. Language should say "you answered like" and show the items.
- Hide all names while people answer. Barber and Pope imply names would measure loyalty. Naming should come after answers are locked, and a randomised group could see names, to measure the cue effect directly.
- Thinkers are unknown to most people, so cue effects may be smaller than for Trump, but outrage-famous names (Musk, Altman) will carry group meaning. This is untested.
- The AI-focused map's axes may simply not exist for many people yet, so expect item non-response and "don't know". Treat those as data.

### Gaps
- Zaller's receive-accept-sample model and Broockman and Butler on elite persuasion: searches returned nothing usable.
- Ahler and Broockman: I could not open the paper; only secondary description, which I have left out as a cited claim.
- No direct study on proximity to figures unknown to the respondent.

## Voter proximity: how good are voting advice applications?

### Takeaway
They are the closest working analogue and are useful for rough sorting, but the single answer they produce is fragile. The choice of statements alone can swing recommendations several-fold, and top-match output should not be trusted to fine precision.

### Cited Findings
- Across 500,000 configurations of 36 statements from a list of 50, with 1,000 Belgian voters, some configurations favoured certain parties and others different ones. [F] — [Walgrave et al. 2009](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20et%20al%202009%20-%20voting%20aid%20applications.pdf)
- In that simulation CD&V-N-VA received between 5% and 32% of advice; VLD-Vivant 0.3% to 23%; Vlaams Blok 4% to 26%. [F] — [Walgrave et al. 2009](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20et%20al%202009%20-%20voting%20aid%20applications.pdf)
- Only 43% of Dutch respondents using both Kieskompas and Stemwijzer got identical advice (Kleinnijenhuis and Krouwel, quoted). Stemwijzer sent 28% to SP against 12% from Kieskompas. [F] — [Walgrave et al. 2009](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20et%20al%202009%20-%20voting%20aid%20applications.pdf)
- An audit of a Danish application found it "not robust enough for users to trust the agreement percentages", and 45% of surveyed voters reported following its recommendations. Preprint. [A] — [arXiv 2603.03532 listing](https://www.alphaxiv.org/abs/2603.03532)
- Wieland analysed 63 Wahl-O-Mat editions against expert and manifesto data, concluding it roughly represents party relations but design changes distort comparison across editions. [S] — [Wieland 2024](https://ideas.repec.org/a/bpj/statpp/v15y2024i3p245-271n1003.html)
- Kieskompas combines expert judgement, manifesto coding and party self-placement. [S] — [Quality & Quantity 2014 listing](https://ideas.repec.org/a/spr/qualqt/v48y2014i3p1455-1472.html)
- Vote Compass reconciles party self-placement with coder calibrations, and parties can contest with public statements. [S] — [Vote Compass methodology](https://www.voxpoplabs.com/votecompass/methodology.pdf)
- Early-user data can check spatial maps defined in advance, and this changed the implicit advice in smartvote. [S] — [Germann et al.](https://michagermann.github.io/publication/germannmendezwheatleyserduelt2015)
- A side effect: early and later users with identical answers can get different advice under such updating. [S] — [Bruinsma 2020](https://publikationen.ub.uni-frankfurt.de/files/81295/s11135-020-00986-8.pdf)
- Ireland's application under-identified supporters of the two main centre-right parties and drew unrepresentative users. [S] — [Wall et al. 2009](https://dare.uva.nl/id/b9bd2b5c-1df2-487f-bb26-d1d00c1d3da0)
- Self-selected data can still be useful. In a study of over 50,000 BSW-O-Mat users, effects correlated r = 0.65 with a probability sample (0.87 excluding non-converging effects), effect sizes were overestimated, and AfD voters were 5.5% against 19.8%. [A] — [Thomeczek 2026](https://www.cogitatiopress.com/politicsandgovernance/article/view/11241)
- These tools change people: a UK study found durable shifts in perceived closeness to parties and in party preference. [S] — [Bath research portal](https://researchportal.bath.ac.uk/en/publications/do-voting-advice-applications-have-durable-causal-effects-evidenc/)

### Inferences
- Walgrave's method transfers directly: resample the statement set many times and publish how often a person's nearest school changes. This should be a required test.
- The Vote Compass contest step is a ready model for the map's dispute right, and it fits "terms the described side would sign".
- Dynamic validation by early users would mean the map changes under people. Freeze a versioned map, and rescore on a release.
- A fingerprint is a light intervention. Telling people who they resemble may move them, which matters for a project valuing non-convergence.

### Gaps
- No general accuracy figure for matching (no benchmark exists for a person's "true" nearest party). I found no study comparing Wahl-O-Mat and Kieskompas head to head on accuracy.
- A secondary summary claimed about 40 items give satisfactory reliability of party positions, but I could not confirm the source, so do not cite it.

## Text-derived and language-model positions: accuracy for individual people

### Takeaway
Language models recover broad camps very well (correlations above 0.9) and do markedly worse inside a camp. The 27 thinkers are mostly a within-camp problem, so the headline numbers overstate what to expect.

### Cited Findings
- Wu, Nagler, Tucker and Messing (not Poole or Tausanovitch) used pairwise model comparisons on 116th Congress senators. Correlation with DW-NOMINATE dimension 1 is 0.967 overall, but 0.838 among Democrats and 0.649 among Republicans. CFscores 0.933; perceived ideology 0.941. [F] — [Wu et al.](https://ar5iv.labs.arxiv.org/html/2303.12057)
- Same study: ranks differ from DW-NOMINATE by 8.31 of 100 positions on average, with the largest gaps about 40 places (Grassley 48th vs 8th). No overall individual error rate is given. It drew on model knowledge, not supplied text. [F] — [Wu et al.](https://ar5iv.labs.arxiv.org/html/2303.12057)
- Le Mens and Gallego report best-model correlations above .90 with experts, crowds or roll calls. For senators, correlation with DW-NOMINATE stays high within party, while correlation with CF scores is weaker within party. [F; exact figures lost in extraction] — [Le Mens and Gallego](https://arxiv.org/html/2311.16639v3)
- For single tweets the best models predict one human rater as well as the average of about 5 to 7 raters. They advise against use in new domains without validation. [F] — [Le Mens and Gallego](https://arxiv.org/html/2311.16639v3)
- Sentence-level averaging beat placing a whole manifesto in one prompt. [F] — [Le Mens and Gallego](https://arxiv.org/html/2311.16639v3)
- Burnham's public scale loads more on affect than on policy (0.9 vs 0.82 with Tweetscores). [F] — [Burnham 2024](https://arxiv.org/pdf/2405.02472)

### Inferences
- These benchmarks are mostly Congress on a known left-right scale. Our axes have no external benchmark, so correlations don't transfer.
- The project's own experience agrees: only 80 of 734 machine-proposed holdings survived blind reading ([ADR-035](/Users/benjaminlife/dev/schismogenesis/docs/adr/ADR-035-idea-families-and-two-reader-structure.md)). Keep the blind reader as the gate on anchors.
- Sentence-level stance with quotes, which the project already does, is the better-supported form. Model recall of what someone "believes" should not be used as an anchor.
- Text-only methods may pick up tribal tone. Keep the stance question tied to specific propositions.

### Gaps
- No study found validating language-model stances of public intellectuals against those people's own answers. That test is cheap if a few thinkers ever agree, but contacting them requires Benjamin's approval.

## Sentinel monitoring: can a small watchlist detect new questions?

### Takeaway
There is good evidence a well-chosen small sample gives early warning of spread, but the sample that works is network-central people, not famous voices. Evidence that a watchlist anticipates opinion is thin, and in the best US study politicians followed the public.

### Cited Findings
- Garcia-Herranz and colleagues monitored followees of random users. Over six months and nearly half a billion tweets, sensors used 32 widespread hashtags a mean 7.1 days (SEM 1.1) before controls, in all but two cases. [F] — [Friends as Sensors](https://arxiv.org/pdf/1211.6512)
- Their sensors led controls 79.9% of the time for 24 newly born hashtags, with lead ranging from 20 days to a few hours or none. Lead times beat a shuffled null for 65.4%. [F] — [Friends as Sensors](https://arxiv.org/pdf/1211.6512)
- Barberá and colleagues found legislators are more likely to follow than lead discussion of issues in the 113th Congress, controlling for media, and respond more to supporters than the general public. [A] — [Who Leads? Who Follows?](https://csmapnyu.org/research/who-leads-who-follows-measuring-issue-attention-and-agenda-setting-by-legislators-and-the-mass-public-using-social-media-data)
- Their Twitter public agenda correlated only .32 to .4 with Gallup's Most Important Problem. [S] — [APSR reader](https://www.cambridge.org/core/product/D855849CE288A241529E9EC2E4FBD3A8/core-reader)
- Downs described a systematic issue-attention cycle starting from a pre-problem stage where few are concerned. [S] — [The Public Interest 1972](https://nationalaffairs.com/public_interest/detail/up-and-down-with-ecologythe-issue-attention-cycle)
- Hogwood criticised Downs's model as based on perception, not quantitative salience analysis. [S] — [Hogwood 1985](https://fbaum.unc.edu/teaching/articles/Hogwood_JOP_1985.pdf)
- Google search has been tested against Gallup's problem question in the US for 2004 to 2010. [A] — [Mellon 2014](https://bibbase.org/network/publication/mellon-internetsearchdataandissuesaliencethepropertiesofgoogletrendsasameasureofissuesalience-2014)
- Mellon warns the searching population is unknown. [S] — [Mellon 2013](https://www.cambridge.org/core/journals/ps-political-science-and-politics/article/abs/where-and-when-can-we-use-google-trends-to-measure-issue-salience/A5B3FE4B866C97E55C9CD6564BDE9C0D)
- An Australian paper reports search failing to predict survey salience. [S] — [ECPR](https://ecpr.eu/Events/Event/PaperDetails/34421)
- First story detection has been shown on Twitter in constant time and space, with effectiveness comparable to pairwise systems. [S] — [Petrović et al. 2010 summary](https://awesomepapers.io/learning-to-hash/publications/petrovic2010streaming)
- LLM agents can draft forecasting questions from web research, with deduplication and verifier agents for quality and resolvability. [S] — [Bosse et al. 2026](https://arxiv.org/abs/2601.22444)
- Question generation on Metaculus, Polymarket and Good Judgment Open was described as still manual editorial work. [S] — [Hillebrandt](https://haukehillebrandt.github.io/forecasting-reports/paper/main.pdf)

### Inferences
- Benjamin's approach is sound for **elite forks**: a watchlist detects new disagreements among those voices by construction. It is unproven as a detector of **wider public questions**. Treat those as two products.
- Add a sensor layer of ordinary-but-central accounts or newsletters chosen by the friends method, so selection is not only fame. Note hashtags measure adoption, not opinion. Platform terms need checking, and individuals must not be profiled: count at topic level only.
- Trigger design: a candidate question fires when a new proposition draws stance from two or more clusters within a short window, with opposed stances. This is cheaper than burst detection on the whole web, and matches the existing pipeline.
- Backtest before trusting: replay past months of works, freeze the system date, and measure lead time and false alarms against later surveys or search.

### Gaps
- Kleinberg burst detection, Media Cloud, GDELT and Pew tracking: searches returned nothing usable, so no reliability claims.
- No source used Polymarket or Metaculus as an issue-attention measure.
- No study found testing whether pundits or intellectuals, as opposed to legislators, lead opinion.

## Item selection from elite disagreement, and letting the public add axes

### Takeaway
Drawing items only from elite disagreement builds the agenda problem into the instrument. Elite items are good for placing thinkers and poor for discovering what the public cares about, so the instrument needs a protected public-origin share and a test for what elites miss.

### Cited Findings
- Bachrach and Baratz's second face of power concerns how some issues are organised into politics and others out. Barriers to airing conflict are themselves power. [S] — [Sage entry](https://sk.sagepub.com/ency/edvol/embed/power/chpt/second-face)
- Lukes extends this to power operating without visible conflict. [S] — [Sage entry](https://sk.sagepub.com/ency/edvol/embed/power/chpt/three-faces-power)
- Walgrave's list of statement criteria includes relevance, diversity and discriminating between parties. [F] — [Walgrave et al. 2009](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20et%20al%202009%20-%20voting%20aid%20applications.pdf)
- Montgomery and Cutler show reduced batteries can cut precision and bias estimates, especially for people at the extremes, and offer adaptive testing instead. [A] — [Political Analysis 2013](https://ideas.repec.org/a/cup/polals/v21y2013i02p172-192_01.html)
- Crowdsourced Adaptive Surveys exists as a relevant method; I read only the title. [S] — [arXiv 2401.12986](https://arxiv.org/pdf/2401.12986)

### Inferences
- Discrimination between elites is exactly VAA's third criterion, so this bias is inherited. Discriminating items favour what the elites fight about.
- Run a Polis-style open round first: the public writes statements, votes, and clusters form with no thinker involved. Thinkers come in only after.
- **Elite-blind axis test:** fit public space, then measure how much public variance lies outside the directions the thinkers span. Report it as a headline number. A high share means the map's voices are missing what people are divided about.
- Reserve at least a quarter of the item bank for public-origin statements (a judgement, no source). Then ask which thinkers have spoken to them. Silence stays missing, and that gap is itself a finding worth showing.
- Third-face limits remain: public statements are shaped by the same media, so no input is neutral. State this.
- Benjamin's cross-cutting statements should be sought in public data first. Statements that bridge public clusters may not be those that bridge thinkers.

### Gaps
- No study found measuring elite-agenda bias in Polis-style tools.

## Concrete design: projecting a person's fingerprint, measuring error, minimum sample and bridges

### Takeaway
Treat the public space as the reference, score thinkers into it, and report a person as a band with a set of possible neighbours. Proposed starting point: 40 to 60 tested bridge statements, 20 to 25 answered per person, about 1,000 opted-in calibrators, and pass or fail tests before any public use. These numbers are proposals.

### Cited Findings
- `person_space` scores people over 40 families and centres by the mean of the 27 thinkers, and `layout` uses MDS `fit_transform`, which positions only those fitted. [F] — [structure.py](/Users/benjaminlife/dev/schismogenesis/packages/arena_map/src/arena_map/structure.py)
- Silence becomes zero then is shifted by centring, and only people near the average remain at zero. [F] — [structure.py](/Users/benjaminlife/dev/schismogenesis/packages/arena_map/src/arena_map/structure.py)
- Anchors above 20% are advised under misfit. [A] — [Fischer et al. 2021](https://doaj.org/article/53599c6075af4f7daeadbd0b5c7e8e86)
- Project rules forbid inference on private individuals who have not opted in, minors, and public use of the 15 flagged landmarks. Paid panels need Benjamin's approval. [F] — [CLAUDE.md](/Users/benjaminlife/dev/schismogenesis/CLAUDE.md)

### Inferences

**Why the current code can't project a person as is:** four changes are needed.
1. Treat unanswered families as missing, not zero. Cosine over the shared answered families only, and show how many.
2. Centre on a public reference, not the thinkers' mean, or everyone will read as one-sided.
3. Add out-of-sample placement, such as landmark MDS or item-model scoring, because the current layout cannot place a new point without refitting.
4. Pin the layout per release so positions stay comparable.

**Pipeline**
1. Open public round, then a bank of 60 to 80 plain statements: at least a quarter public-origin, the rest drawn from families with opposed thinkers.
2. Require each bridge to have about 6 or more blind-read thinker stances with at least 2 on each side. Run targeted reading to reach that. Current data will fail this on most ideas.
3. Calibrate on about 1,000 opted-in adults, names hidden, plus benchmark weights.
4. Drop items that behave differently for thinkers and the public, as far as 27 anchors can show. Use text position against item direction as a sign check.
5. Fit dimensions from public data. Score thinkers under fixed item parameters, with intervals.
6. People answer 20 to 25 items chosen adaptively, and get a band, the top few schools, and the items that drove it.

**How precise, in best case (my calculation):** using two-parameter item information at most a²/4 per item, a normal prior, and one dimension.

| Items | Discrimination 1.0: reliability, posterior SD | Discrimination 1.5: reliability, posterior SD |
|---|---|---|
| 7 | 0.64, 0.60 | 0.80, 0.45 |
| 20 | 0.83, 0.41 | 0.92, 0.29 |
| 40 | 0.91, 0.30 | 0.96, 0.21 |

These are ceilings, since items aren't all peaked at the person. Two dimensions split the items between them. So 7 items gives a rough region, and 20 to 25 gives about one useful dimension or two coarse ones. I assume weak public structure pushes real numbers toward the left column or worse.

**Error tests, with proposed pass marks**
- Statement sensitivity (Walgrave style): resample bank 10,000 times. Target: the top-three schools hold for 80% of people.
- Test-retest at two weeks: position correlation at least 0.7.
- Held-out items: predict a person's unseen answers better than majority and party-only baselines. This is the key test of whether the map adds anything.
- Thinker recovery: remove a thinker's stances from fitting and check recovery from the rest, and compare two independent item sets.
- Cue arm: randomise name display, and estimate shift.
- Interval coverage: do stated bands contain the retest position about 90% of the time.
- Elite-blind share: report it.

**Sample rationale:** 1,000 is a judgement, and no source sets a minimum for this design. Simulate on synthetic respondents before fielding, because [linking results depend on design details](https://public-pages-files-2025.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1652341/pdf).

**Display:** "You answered most like this school on these items, and differ on these." No single dot, no percentage match at false precision, and a route to dispute. Show thinkers as hollow where few bridges cover them.

### Gaps
- No precedent found for this exact setup: small elite anchor set, text-derived stances, multidimensional public space.
- Actual count of ideas meeting the bridge rule is unknown. Stored stance data was not located in `data/`, so I did not compute it.
- Item discriminations for AI-era propositions in the US public are unknown until a pilot.
