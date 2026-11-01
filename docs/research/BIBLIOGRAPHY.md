# Dialogos Arena: Consolidated Annotated Bibliography

Author of record: Benjamin Life (@omniharmonic). Compiled 2026-10-30 as section 17 of `SYNTHESIS.md` (formerly §16, §15 and §14 before that), consolidated and de-duplicated from research briefs A1–A5 and B1–B9. Section I (agents) was added with B6; sections J (Girard, hyperstition and the state machine) and K (open agents, registries, tokens and strategy markets) were added with B7 and B8. Section L (design-dialogue lineages: Vervaeke, Landry's EGP, the Society Library, Community Notes and vTaiwan, plus the transcript pipeline) was added on 2026-10-30 from the Design Dialogue Memo and filled from B9.

**Key.**
- **[P]** a primary source: an original paper, an official doc or terms, the primary text, code, or an author's own post.
- **[S]** secondary: a summary, news report, wiki or vendor summary.
- **[V]** internal: Benjamin's repos, his Parachute vault, or Gitcoin Brain.
- **UNVERIFIED**: carried forward from a brief.
- Brief codes in brackets show which brief cited the item.

Some fetches failed during research: GitHub repos, the SEP, docs.x.com pricing, the anti-debate.org pages and parts of docs.bsky.app. Where a brief relied on a summary instead, the entry says so.

### A. Benjamin Life's prior work and internal records [V]
- Ontography repo, main and `live-docs` branches: `/home/claude/auto-ontography-archive` (README, docs/PRD.md incl. NFR-3, docs/ARCHITECTURE.md, src/lib/*). The code is authoritative over the docs. [A1, B4, B5]
- Topology Live / antidebate-live: `/home/claude/omniharmonic/antidebate-live` (docs/ONTOLOGY.md v1.0, ARCHITECTURE.md, QUALITY.md, QA_AUDIT_2026-09-30.md, evals/results.md, docs/client/*, packages/core/src/formats.ts). The canonical schema source. [A1, A3]
- Dialectical Topology: `/home/claude/omniharmonic/dialecticaltopology` (pipeline/*.py, data/bundle/*, frontend/public/data/tree.json, META_ANALYSIS.md, docs/plans/*). The six lenses plus the silhouette test. [A2, B4]
- Dialectical.Claims: `/home/claude/omniharmonic/dialecticalclaims` (README, PRD §3.5, lib/dialectic-generator.ts, supabase-schema.sql, production logs). Thinkers modeled as methods; three synthesis slots. [A2]
- Essays in Parachute `wiki/writing/`:
  - *For Now We See Through a Glass, Darkly* (2026-03-03)
  - *Dialectical.Claims*
  - *Dialectics & Spontaneous Evolution*
  - *The Ancient Future at the End of History*
  - *Beyond Narrow Optimization*
  - *When Democracy Dies*
  - *Fork You*
  - *Out in the Bloodshed*
  - *When Integral Theory Faces Its Colonial Shadow*
  - *What Is Ethereum For*
  - *A Political Rise Manifesto* (2021)
  - *Leaderful Spaces*
  - *Protocols of Place*
  - *The Infrastructure of Belonging*
  - *Citizen*
  - *How and Why AI Will Accelerate Capitalism and Then Destroy It*
  - *Awakening the Earth Dharma II*
  - *Welcome to Omniharmonic*
  - *The Christ Meme*
  - *After the Black Pill*
  - *Transhumanism, Wetiko…*

  These are the source of the positions P1–P17 and the glossary in A4. [A2, A4]
- Parachute `wiki/concepts/*`: dialectics, memetic-evolution, pluralism, functional-pluralism, quadratic-voting/funding, integral-theory, metamodernism, basin-of-attraction, etc. [A4]
- Parachute meetings and records:
  - `2026-07-10_regen-hub-demo-ontography`: legibility failures, the overlap doubts, the twin-test idea.
  - `2026-04-09/high-dimensional-foraging`.
  - `united-independents/.../2026-06-02_deliberative-polling-tool`.
  - `united-independents/docs/Civic Tech Stack Research Draft`: Comhairle; not independently verified.
  - Polis Labs meeting notes, 2025-08-27 and 2026-04-17.

  [A1, A4, B2]
- Parachute research and tasks:
  - `thiel-karp-genealogy/synthesis/graph-topology-report`: bridges found by betweenness plus diversity of source traditions.
  - `final-constellation`.
  - Tasks `topology-live-antidebate-progress-conference` (status pending) and `simplify-ontography-visualization`.

  [A3, A4]
- Parachute messages:
  - `telegram/kevin-owocki`: 2026-07-04 Venn feedback; 2026-07-28 Atlas link.
  - `telegram/joe-lightfoot`.
  - `email/fwd-we-are-post-meta-now-72396552`.
  - `wiki/writing/the-liminal-web-ep_01`.

  [A1, A5]
- Gitcoin Brain [V]:
  - `meetings/2026-06-19_gitcoin-x-stephanie-research-interview`: Lepp's offer to run anti-debates.
  - `knowledge/gov-forum-learnings/qf-mechanics`: the GG22 $0-match case; CCN Climate.
  - `knowledge/gov-forum-learnings/sybil-identity`: includes Benjamin's GG21 retrospective.
  - `knowledge/gov-forum-learnings/measurement-impact`.
  - `knowledge/love-fund-survey-disbursement-plan`: costless QF subsidizes sybils.
  - `knowledge/local-qf-record-model`.
  - `telegram/gitcoin-viral-content/2026-05-25` and `2026-05-06`.
  - `meetings/2026-05-21_daniel-schmachtenberger-gitcoin` (not mined).

  [A3, A5, B3]
- Benjamin's Google Calendar: Anti-Debate sessions with Stephanie Lepp, 2022–2023. [A3]

### B. Anti-Debate and dialogue formats
- [P via repo summary] anti-debate.org: How-To Guide, Ground Rules, Discourse Matrix (https://www.anti-debate.org/how-to-guide.html; /ground-rules.html; /discourse-matrix.html). The format phases and rules, CC BY-SA 4.0. A direct fetch was blocked. [A3]
- [P via repo summary] Synthesis Media, "What is the Anti-Debate?" (Feb 2026): https://www.synthesismedia.org/p/what-is-the-anti-debate ; "Anti-Debate on AI Governance: Ball x Kokotajlo": https://www.synthesismedia.org/p/anti-debate-on-ai-governance-dean. [A3]
- [P] Heck & Lepp, TED (Aug 2025), "Why meeting in the middle isn't enough…": https://www.ted.com/talks/bill_heck_and_stephanie_lepp_why_meeting_in_the_middle_isn_t_enough_for_today_s_trickiest_debates. Higher ground, parallax, the three integration questions. [A3]
- [S] Partiful, "Anti-Debate on AI" (Lighthaven, 2026-03-09): https://partiful.com/e/Toy7N2AzrWOqNiBrYhqO. [A3]
- [S] Szeps, "A Better Way to Debate?" (preview only): https://uncomfortableconversations.substack.com/p/szeps-live-a-better-way-to-debate. [A3]
- [P] Roots of Progress, Progress Conference 2026 (no anti-debate session listed): https://rootsofprogress.org/conference/. [A3]
- [P] Anti-Debate YouTube playlist (not fetched): https://www.youtube.com/playlist?list=PLRN1pe0US2hS-mWZAiYJ8OMII8BcB6UXc. [A3]
- Outcome of the 2026-10-11 Topology Live event: **UNVERIFIED** (no record found). [A3]

### C. Memetic-tribes lineage and Kevin Owocki's Atlas
- [P] Limberg & Barnes, "The Memetic Tribes of Culture War 2.0" (Medium, 2018-09-14): https://medium.com/s/world-wide-wtf/memetic-tribes-and-culture-war-2-0-14705c43f6bb ; spreadsheet: https://docs.google.com/spreadsheets/d/11Ov1Y1xM-LCeYSSBYZ7yPXJah2ldgFX4oIlDtdd7-Qw/edit. 33 tribes × 9 columns, chosen qualitatively. [A5]
  - Name note: "Peter Lindenberger/Limberger" is Peter N. Limberg. A3's "Connor Barnes" is Conor Barnes. [A5]
- [S] Second Renaissance, "Memetic Tribes" and "Overview of mapping efforts": https://secondrenaissance.net/wiki/memetic-tribes ; https://secondrenaissance.net/wiki/overview-mapping-efforts. [A5]
- [S] EA Forum discussion: https://ea.greaterwrong.com/posts/pKgWQMjPki5bz7ehZ/memetic-tribes-and-culture-war-2-0-article-discussion. [A5]
- [P] Lightfoot, "The Liminal Web" (2021, updated 2023): https://stream.syscoi.com/2021/11/18/the-liminal-web-mapping-an-emergent-subculture-of-sensemakers-meta-theorists-systems-poets-joe-lightfoot. A scene, not a tribe; the ~30% consumption heuristic. [A5]
- [P] Dempsey, *Metamodern Meaning* ep. 17: https://brendangrahamdempsey.substack.com/p/17-the-liminal-web-and-communitas-c93. [A5]
- [P] Limberg, *Less Foolish*:
  - "How not to build a Stoa": https://lessfoolish.substack.com/p/how-not-to-build-a-stoa-a-very-online
  - "Memetic mediation during the liminal war": https://lessfoolish.substack.com/p/memetic-mediation-during-the-liminal
  - "Alt accounts, insight roles and memetic mediation": https://lessfoolish.substack.com/p/alt-accounts-insight-roles-and-memetic
  - The "Intimacy Crisis" essay is **UNVERIFIED**. Who coined "memetic mediator" is **UNVERIFIED**.

  [A5]
- [S] Beiner/Kainos interview with Limberg: https://beiner.substack.com/p/why-scene-making-beats-sensemaking. [A5]
- [S] P2P Foundation: Snyder, "Rise of the Memetic Mediators": https://wiki.p2pfoundation.net/Jason_Snyder_on_the_Rise_of_the_Memetic_Mediators ; Nørgaard, "Memetic Tribes of the Meta-Crisis": https://wiki.p2pfoundation.net/Brandon_N%C3%B8rgaard_on_the_Memetic_Tribes_of_the_Meta-Crisis. [A5]
- [P] OILab, "Political Space": https://oilab.eu/political-space. Tribes placed manually on 3 axes. [A5]
- [P] Schmachtenberger, "The War on Sensemaking": https://civilizationemerging.com/media/war-on-sensemaking-5/. [A5]
- [P] More in Common, *Hidden Tribes of America* (2018): https://hiddentribes.us/. Clustering on deep drivers; the "Exhausted Majority". [A5]
- [P] Pew, Political Typology 2021: https://www.pewresearch.org/politics/2021/11/09/beyond-red-vs-blue-the-political-typology-2021/ ; methodology appendix B. The names of the 9 groups are **UNVERIFIED**. [A5]
- [P] Owocki, "Atlas of Frontier Ontologies": https://daily-ontological-map.vercel.app/. 58 X ontologies, nightly, two axes. Method undisclosed. [A5 addendum]

### D. Philosophical and theoretical lineages
- [P, SEP pointers not re-fetched] SEP entries "Hegel's Dialectics", "Cultural Evolution", "Jürgen Habermas", "Martin Buber" and "Dewey's Political Philosophy" (plato.stanford.edu). [B1]
- [P] Mueller, "The Hegel Legend of 'Thesis-Antithesis-Synthesis'", *JHI* (1958). Bibliographic detail from memory. [B1]
- [P] Kojève's Hegel lectures (1930s); Fukuyama, "The End of History?" (1989): https://www.democraziapura.it/wp-content/uploads/2015/01/1989-Fukuyama.pdf. [B1, A4]
- [P] Mill, *On Liberty* (1859), ch. 2. The "marketplace of ideas" phrase dates to Holmes's dissent in *Abrams v. United States*; its first exact use is **UNVERIFIED**. [B1]
- Wu, "Is the First Amendment Obsolete?" (2017): **UNVERIFIED**. [B1]
- [P] Buber, *I and Thou* (1923); Bohm, *On Dialogue* (1996). [S] Are.na Bohm overview: https://www.are.na/editorial/bohm-dialogue. [B1]
- [P] Habermas, *Structural Transformation of the Public Sphere* (1962); *Theory of Communicative Action* (1981). [S] "Ideal speech situation": https://www.wikiwand.com/en/articles/Ideal_speech_situation. Habermas 2022, *A New Structural Transformation*: **UNVERIFIED**. [B1]
- [P] Fraser, "Rethinking the Public Sphere," *Social Text* 25/26 (1990). Counterpublics. [B1]
- [P] Mouffe, "Deliberative Democracy or Agonistic Pluralism?" (1999/2000): https://irihs.ihs.ac.at/id/eprint/1312/. [B1]
- [P] Gutmann & Thompson, *Democracy and Disagreement* (1996); Dryzek, *Discursive Democracy* (1990); Dryzek & Niemeyer, *Foundations and Frontiers of Deliberative Governance* (2010): https://academic.oup.com/book/11756. Meta-consensus. [B1]
- [P] Landemore, *Democratic Reason* (2013) and *Open Democracy* (2020): https://press.princeton.edu/node/59247. [B1]
- [P] Dewey, *The Public and Its Problems* (1927). [B1]
- [P] Boyd & Richerson (1985, 2005); Henrich, *The Secret of Our Success* (2016); Dawkins (1976); Blackmore (1999). [B1]
- [P] Sperber, *Explaining Culture* (1996): https://www.dan.sperber.fr/?p=29. Cultural attraction. [B1]
- [P] Aunger (ed.), *Darwinizing Culture* (2000): https://dc2.philarchive.org/rec/AUNDCT. [B1]
- [P] Ashby (1956); Bateson, *Naven* (1936) and *Steps to an Ecology of Mind* (1972). [P] Heylighen & Joslyn: https://CliffJoslyn.github.io/Docs/HeFJoC03.pdf. [B1]
- [P] Woolley et al., *Science* 330 (2010): https://pubmed.ncbi.nlm.nih.gov/20929725/. The *c* factor; replications are mixed (**UNVERIFIED** detail). [B1]
- [P] Page, *The Difference* (2007). [P] Hong & Page, *PNAS* 101(46) (2004): https://pmc.ncbi.nlm.nih.gov/articles/PMC528939/. [P] Romaniega, arXiv 2307.04709 (critique; also the source for Thompson, *Notices AMS* 2014): https://arxiv.org/pdf/2307.04709. [B1]
- [P] Freinacht, *The Listening Society* (2017): https://wiki.p2pfoundation.net/Listening_Society. Wilber; Beck & Cowan. Visser critique (not read): https://www.integralworld.net/visser236.html. [B1]
- [P] Girard (1961, 1972, 1978). [S] https://en.wikipedia.org/wiki/Mimetic_theory ; https://criticallegalthinking.com/2023/09/04/mimetic-desire-the-scapegoat-notes-on-the-thought-of-rene-girard/. [B1]
- Popper, *The Poverty of Historicism*: **UNVERIFIED** citation detail. [B1]
- [P] Koltko-Rivera, "The Psychology of Worldviews" (2004): https://lup.lub.lu.se/search/files/5733804/3738786.pdf. 42 dimensions in 7 groups. [B4]

### E. Computational democracy and deliberation technology
- [P] Small et al., "Polis: Scaling Deliberation…" (2021): https://www.e-revistes.uji.es/index.php/recerca/article/view/5516. [P] CompDem open source (AGPL-3.0): https://compdemocracy.org/open-source. [P] Group-informed consensus: https://compdemocracy.org/group-informed-consensus. [B2, B3]
- [S] Polis 2.0 reporting: https://news.hada.io/topic?id=26667 ; https://news.lavx.hu/article/polis-2-0-the-open-source-platform-scaling-deliberative-democracy-to-millions ; https://www.gigazine.net/gsc_news/en/20260216-polis/. Scale claims **UNVERIFIED**. [B2, B5]
- [P] Nishio, notes on Polis lumping and on kouchou-ai: https://scrapbox.io/nishio-en/Phenomenon_that_Polis_with_the_most_votes_are_lumped_together. ; https://scrapbox.io/nishio-en/public_information_AI. [B2]
- [S] Daily Beast on vTaiwan: https://www.thedailybeast.com/taiwan-tried-to-digitize-democracy-with-vtaiwan-it-was-a-huge-flop ; Noveck rejoinder: https://thelivinglib.org/?p=57365. [B2]
- [P] AI Objectives Institute, Talk to the City (archived): https://gwern.net/doc/www/ai.objectives.institute/fa46182a810da5bfde418b21016574027d1dd94f.html. Pipeline specifics **UNVERIFIED**. [S] IE CGC case studies: https://ie.edu/cgc/news-and-events/news/using-ai-to-inform-policymaking-what-we-can-learn-from-3-use-cases-of-talk-to-the-city. [B2]
- [S] Team Mirai: https://en.wikipedia.org/wiki/Team_Mirai. [B2]
- [P] Konya et al. (2023), arXiv 2311.02242: https://ar5iv.labs.arxiv.org/html/2311.02242 ; Konya et al. (2025), arXiv 2503.01769: https://arxiv.org/pdf/2503.01769. Remesh and max-min agreement. [B2]
- [P] CIP Global Dialogues: https://www.cip.org/global-dialogues. [B2]
- [P] Stanford Online Deliberation Platform: https://deliberation.stanford.edu/tools-resources/online-deliberation-platform ; Fishkin et al., APSR (2021); Meta Community Forum: https://fsi.stanford.edu/node/36099. [B2]
- [P] Goyal et al., "Beyond Polarization: Opinion Mixing…" arXiv 2601.14221. Deliberation reorders opinions. [B2]
- [P] Tessler, Bakker et al., *Science* (2024), Habermas Machine: https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf ; Tessler et al., arXiv 2601.05904. No public code found (**UNVERIFIED**). [S] Sætra, CACM: https://cacm.acm.org/blogcacm/computation-and-deliberation-the-ghost-in-the-habermas-machine. [B2, B3]
- [P] Wojcik et al., "Birdwatch", arXiv 2210.15723: https://arxiv.org/abs/2210.15723. The MF bridging model. [B2, B3, B4]
- [S] DeepWiki, Community Notes group scoring: https://deepwiki.com/twitter/communitynotes/2.2-group-based-scoring. The repo licence (Apache-2.0) is **UNVERIFIED**. [B2]
- [P] Andreou & Sirivianos, "Two Fault Lines," arXiv 2609.21496: https://arxiv.org/abs/2609.21496. Second axis (institutional trust). Existence re-confirmed for this synthesis. [B2, B4]
- [P] Razuvayevskaya et al., arXiv 2510.12559; Arjmandi-Lari, Mantzarlis & Stafford, arXiv 2510.00650; Li & Bakker, arXiv 2604.02592 (LLM note writers); Lloyd et al., arXiv 2509.15434. [B2]
- [P] Selvam, Baxter et al., "Gaming Consensus," arXiv 2607.01824. Read via the summary at https://tldr.takara.ai/p/2607.01824. [B5]
- [P] Ovadya & Thorburn, "Bridging Systems," arXiv 2301.09976. [P] Milli, Thorburn et al., NeurIPS 2024 Pluralistic Alignment Workshop poster (bridging censors controversial topics): https://neurips.cc/virtual/2024/99058. [P] Stray et al., Prosocial Ranking Challenge, arXiv 2603.19626. [B2, B3]
- [P] Jigsaw et al., "AI and the Future of Digital Public Squares," arXiv 2412.09988 ; Google.org Sensemaking AI: https://blog.google/company-news/outreach-and-initiatives/google-org/sensemaking-ai/. `Jigsaw-Code/sensemaking-tools` licence **UNVERIFIED**. [B2]
- [P] Weyl, Tang et al., *Plurality* (CC0): https://plurality.net/. Plurality Institute outputs **UNVERIFIED**. [B2]
- [P] Anthropic & CIP, Collective Constitutional AI: https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input. [B2]
- [P] Fish, Gölz, Parkes, Procaccia et al., "Generative Social Choice," arXiv 2309.01291. [B2, B3]
- [S] Kialo: https://en.wikipedia.org/wiki/Kialo ; Harmonica: https://metagov.org/delib-tools/harmonica ; Frankly: https://cyber.harvard.edu/story/2025-04/asml-invites-open-source-collaborators-to-frankly ; Loomio: https://en.wikipedia.org/wiki/Loomio ; [P] Decidim Barcelona: https://decidim.org/case-studies/barcelona-budgeting/. [B2]
- Bluesky/Blacksky `assembly.blacksky.community` deliberation work: **UNVERIFIED**. Taiwan's Join platform: **UNVERIFIED**. [B2]

### F. Mechanism design
- [P] Lalley & Weyl, AEA P&P 108 (2018): https://www.aeaweb.org/doi/10.1257/pandp.20181002. [B3]
- [P] Buterin, Hitzig & Weyl, *Management Science* 65(11) (2019): https://arxiv.org/abs/1809.06421. [B3]
- [P] Buterin, "Pairwise coordination subsidies" (2019): https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553. Full text not fetched. [B3]
- [P] Weyl, Ohlhaver & Buterin, "Decentralized Society" (2022): https://papers.ssrn.com/abstract=4105763. [B3]
- [P] Miller, Weyl & Erichsen, "Beyond Collusion Resistance": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4311507 (full paper not fetched) ; RadicalxChange blog. Code at github.com/Jmiller4/plural-qf (not fetched). [B3]
- [P] Miller, Weyl & Kanich, "Fair Decisions through Plurality," EAAMO '25, arXiv 2509.18343. The CO-QF formula; 32 of 38 rounds. [B3]
- [P] Gitcoin: Deep Funding: https://gitcoin.co/mechanisms/deep-funding ; Pairwise: https://gitcoin.co/mechanisms/pairwise ; cluster-matching ops: https://roundoperations.gitcoin.co/round-operations/post-round/cluster-matching-and-csv-upload ; COCM nerd post: https://gov.gitcoin.co/t/nerd-post-updates-to-cluster-mapping-matching/18705. [S] Kronosapiens jury analysis: https://kronosapiens.github.io/blog/2025/08/03/deepfunding-jury-analysis. [B3]
- [P] Optimism, "Lessons learned from two years of RetroPGF": https://gov.optimism.io/t/lessons-learned-from-two-years-of-retroactive-public-goods-funding/9239. [B3]
- [S] BlockScience, "A Brief History of Conviction Voting" (not read in full). [B3]
- [P] Miller, Resnick & Zeckhauser, peer prediction (2005); Prelec, BTS, *Science* 306 (2004); Prelec, Seung & McCoy, *Nature* (2017); Hanson, futarchy: https://mason.gmu.edu/~rhanson/futarchy.html. BTS validity across clusters with different priors is **UNVERIFIED**. [B3]
- [P] Manheim & Garrabrant, Goodhart variants, arXiv 1803.04585. [B3]
- [P] Borge et al., Proof-of-Personhood (2017): https://bford.info/pub/dec/pop-abs/ ; Yu et al., SybilGuard (2006). [P] Human Passport: https://human.tech/blog/defending-gitcoin-grants. [B3]
- Frey & Oberholzer-Gee, AER (1997), crowding-out: not re-verified. Campaign-finance exposure of cross-cluster matching: **UNVERIFIED**. [B3]

### G. Mapping science
- [P] Conover et al., ICWSM 2011: https://ojs.aaai.org/index.php/icwsm/article/view/14126. Partly **UNVERIFIED** (bot wall). [A5, B4]
- [P] Barberá, "Birds of the Same Feather," *Political Analysis* (2015); code https://github.com/pablobarbera/twitter_ideology. [P] Barberá et al., *Psych. Science* (2015). [A5, B4]
- [P] Cinelli et al., *PNAS* 118(9) (2021): https://pubmed.ncbi.nlm.nih.gov/33622786/. Method detail to re-verify. [B4]
- [P] Garimella et al., "Quantifying Controversy": https://arxiv.org/abs/1507.05224 ; Garimella, Weber & De Choudhury, quote-RTs: https://www.arxiv.org/abs/1603.07933. [B4]
- [P] Waller & Anderson, arXiv 2010.00590; https://github.com/CSSLab/social-dimensions. [B4]
- [P] Wu, Nagler, Tucker & Messing, arXiv 2303.12057. LLM pairwise comparisons plus Bradley–Terry. [B4]
- [P] Satuluri et al., SimClusters, KDD 2020. Specifics **UNVERIFIED**. [B4]
- [P] Traag, Waltman & van Eck, Leiden, arXiv 1810.08473 ; Peixoto, SBM, arXiv 1705.10225 ; Traag & Bruggeman, arXiv 0811.2329 ; signed-bipartite sensitivity, arXiv 2405.08203 ; Grover & Leskovec, node2vec, arXiv 1607.00653 ; Burt (2004) ; Mucha et al., arXiv 0911.1824 ; Kivelä et al. (2014). [B4]
- [P] Ghafouri et al., stance-aware sentence transformers, EMNLP 2024: https://aclanthology.org/2024.emnlp-main.1171.pdf. [B4]
- [P] Grootendorst, BERTopic, arXiv 2203.05794. The HDBSCAN noise share on tweets is **UNVERIFIED**. [B4]
- [P] Stance surveys, arXiv 2409.15690 and 2409.13594 ; Törnberg, arXiv 2304.06588. PMC12629487 not read (**UNVERIFIED**). [B4]
- [P] Metropolitansky & Larson, Claimify, arXiv 2502.10855. [B4]
- [P] Preniqi et al., MoralBERT, arXiv 2403.07678 ; Hopp et al., eMFD (2021) ; Kiesel et al., SemEval-2023 ValueEval. MFQ-2 attribution to Atari et al. 2023 is **UNVERIFIED**. [B4]
- [S/P] Jev (TypeSafe AI, launched 2026-09-15):
  - The Batch: https://www.deeplearning.ai/the-batch/models-built-to-do-one-thing-well
  - The New Stack: https://thenewstack.io/typesafe-jev-system-one/
  - LiteLLM benchmark: https://docs.litellm.ai/blog/jev-auto-router-benchmark
  - NanoGPT docs: https://docs.nano-gpt.com/api-reference/endpoint/jev-decisions.md
  - Low-confidence JevBench/imitators: https://www.modemguides.com/blogs/ai-news/jev-typesafe-reality-check-run-locally
  - Re-confirmed for this synthesis by search: https://www.datacamp.com/blog/system-one-models-jev ; https://letsdatascience.com/news/typesafe-ai-launches-jev-decision-model-889a38c0
  - Accuracy claims are vendor-internal. Availability is **UNVERIFIED** (checked 2026-10-30). Secondary sources conflict: the waitlist was removed 2026-09-21 (explainx.ai), signups were paused 2026-09-22 (B4), and the direct API is still waitlisted with gateway routes open (opentweet.io).

  [B4]
- [P] GLiClass, arXiv 2508.07662 ; SetFit, arXiv 2209.11055 ; [S] gzip+kNN critique: https://liorsinai.github.io/machine-learning/2023/08/13/gzip-knn.html. [B4]
- [P] Pew (2019), Twitter users' 10%/80% skew. [P] Rauchfleisch & Kaiser (2020), bot-detection errors; re-verify the specifics. [B4]
- [S] Bail et al., *PNAS* (2018), backfire from exposure to opposing views, via NiemanLab: https://www.niemanlab.org/2018/08/republicans-who-follow-liberal-twitter-bots-actually-become-more-conservative/. The primary is **UNVERIFIED** per B1. [B1, B4]
- [P] Community Archive: https://github.com/TheExGenesis/community-archive. Inclusion of follow data is **UNVERIFIED**. [P] Bluesky dataset paper, arXiv 2408.03146. [B4]
- [P/S] Visualization: Apple Embedding Atlas, arXiv 2505.06386 ; DataMapPlot: https://datamapplot.readthedocs.io ; Cosmograph (vendor): https://cosmograph.app/docs-lib/comparison/ ; Nomic: https://home.nomic.ai/blog/posts/data-mapping. [B4]

### H. Platforms, data law and weaponization
- [P] X Developer changelog (pay-per-use 2026-02-06; Owned Reads 2026-04-16; search changes 2026-05-04): https://docs.x.com/updates/changelog. [P] X restricted use cases (political-inference clause): https://docs.x.com/developer-terms/restricted-use-cases. [P] X OAuth 2.0 PKCE: https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code. [B5]
- [S] Upload-Post X API pricing (2026-09-28): https://www.upload-post.com/x-api-pricing/ ; OpenTweet summary: https://opentweet.io/x-api-pricing. Per-resource prices and the scope of Owned Reads are **UNVERIFIED** against docs.x.com. [B4, B5]
- [P] X Help, archive download: https://help.x.com/articles/20170320 ; Princeton Community Notes archive protocol: https://communitynotes.cs.princeton.edu/data_collection_details_prol.pdf. [B5]
- [S] Knight Institute on X ToS liquidated damages: https://knightcolumbia.org/content/knight-institute-says-xs-new-terms-of-service-will-stifle-independent-research. [B5]
- [P] Jetstream (Jaz, 2024): https://jazco.dev/2024/09/24/jetstream/ ; [S] https://apis.io/apis/bluesky/bluesky-jetstream/ ; [P] Bluesky moderation docs: https://www.docs.bsky.app/docs/advanced-guides/moderation ; AT Protocol 2026 Spring Roadmap: https://atproto.com/blog/2026-spring-roadmap ; rate-limit discussion: https://github.com/bluesky-social/atproto/discussions/697 (current figure **UNVERIFIED**) ; [S] Gigazine on Bluesky MAU: https://gigazine.net/gsc_news/en/20260812-blueskys-active-user/. [B5]
- [P] Neynar pricing: https://neynar.com/developer ; [S] Pulse on Neynar's acquisition of Farcaster. [P] Lisker & Mihaljević, "Data Ethics in the Fediverse," arXiv 2505.07606. [B5]
- [S] DLA Piper on CJEU C-252/21: https://privacymatters.dlapiper.com/2023/07/eu-cjeus-landmark-decision-in-meta-vs-bundeskartellamt/ ; Columbia GFoE on C-446/21: https://globalfreedomofexpression.columbia.edu/cases/maximilian-schrems-v-meta-platforms-ireland-limited-schrems-iii/. [B5]
- [P] EU TTPA, Reg. 2024/900: https://eur-lex.europa.eu/eli/reg/2024/900/oj ; [P] EC FAQ on DSA researcher data access: https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en. Eligibility is **UNVERIFIED**. [B5]
- [S] Bastion on CCPA sensitive personal information ; NatLawReview on Colorado sensitive data (detail **UNVERIFIED**). [B5]
- [S] ZwillGen on hiQ v. LinkedIn ; NatLawReview and Goldman blog on X v. Bright Data (final outcome **UNVERIFIED**) ; scraping legal wiki (Meta v. Bright Data; 2025–26 DMCA §1201 cases). [B5]
- [P] FTC opinion on Cambridge Analytica (2019): https://www.ftc.gov/system/files/documents/cases/d09389_comm_final_opinionpublic.pdf ; [P] Kosinski, Stillwell & Graepel, *PNAS* (2013) ; [P] Narayanan & Shmatikov (2009), arXiv 0903.3276 ; [P] Graphika: https://graphika.com/how-it-works. [B5]

### I. AI agents, influence operations and agent ethics
Added with B6. Tessler et al. (Habermas Machine), Li & Bakker (AI note writers), the Prosocial Ranking Challenge, the Bluesky moderation docs and Rauchfleisch & Kaiser are listed above (E, G, H) and are also cited by [B6].

**Adversarial operations**
- [P] OpenAI, "Disrupting deceptive uses of AI by covert influence operations" (May 2024): https://openai.com/index/disrupting-deceptive-uses-of-AI-by-covert-influence-operations/ ; "Disrupting malicious uses of AI" (June 2025): https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-june-2025. Breakout Category ratings. [B6]
- [S] OpenAI on Storm-2035 (Aug 2024), via Security Affairs: https://securityaffairs.com/167194/intelligence/openai-dismantled-iranian-influence-operation.html ; OpenAI June 2026 PRC-linked operation, via PC Gamer: https://pcgamer.com/software/ai/openai-says-it-busted-a-shadowy-chinese-operation-that-used-chatgpt-to-whip-up-data-centre-hate-and-that-achieved-basically-nothing/. [B6]
- [P] Anthropic, "Detecting and countering malicious uses of Claude" (2025): https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025. Influence-as-a-service. [B6]
- [P] Meta, Adversarial Threat Report Q3 2022: https://about.fb.com/news/2022/11/metas-adversarial-threat-report-q3-2022/ ; [S] Meta Spamouflage takedown (Aug 2023), via The Record: https://therecord.media/spamouflage-china-accused-largest-covert-influence-operation-meta. [B6]
- [S] STOIC: Times of Israel on the NYT Diaspora Ministry report: https://www.timesofisrael.com/diaspora-ministry-funded-fake-social-media-posts-to-spread-pro-israel-content-nyt/ ; NBC News (headline only): https://www.nbcnews.com/tech/security/meta-openai-say-disrupted-israeli-companys-influence-campaign-rcna154774. State funding reported, ministry denied. [B6]
- [S] Reuters Pentagon anti-Sinovac investigation, via Al Jazeera (June 2024): https://www.aljazeera.com/news/2024/6/14/pentagon-ran-secret-anti-vax-campaign-to-undermine-china-during-pandemic. [B6]
- [P] SIO & Graphika, *Unheard Voice* (2022): https://fsi.stanford.edu/node/22009 ; https://purl.stanford.edu/nj914nx9540. [S] The Intercept on CENTCOM accounts (Dec 2022): https://theintercept.com/2022/12/20/twitter-dod-us-military-accounts/. [B6]
- [P] Graphika, *The Americans* (Sept 2024): https://public-assets.graphika.com/reports/graphika-report-the-americans.pdf. [B6]
- [P] DOJ, Doppelganger domain seizure (Sept 2024): https://www.justice.gov/usao-edpa/pr/justice-department-disrupts-covert-russian-government-sponsored-foreign-malign ; [S] CyberScoop on Meliorator (July 2024): https://cyberscoop.com/us-international-authorities-seize-russian-ai-bot-farm/. [B6]
- [P] Microsoft MTAC (April 2024): https://blogs.microsoft.com/on-the-issues/2024/04/17/russia-us-election-interference-deepfakes-ai/ ; DFRLab 2025 year in review (Pravda network): https://dfrlab.org/2025/12/31/the-dfrlab-reflects-on-2025/. [B6]
- [P] Eady et al., *Nature Communications* (9 Jan 2023), Russian 2016 Twitter campaign; [S] TCD summary: https://www.tcd.ie/news_events/articles/voting-behaviour-in-2016-us-presidential-election-not-affected-by-foreign-disinformation-campaigns-on-twitter/. Re-confirmed for this synthesis. [B6]
- [P] Nimmo, The Breakout Scale (Brookings 2020): https://www.brookings.edu/articles/the-breakout-scale-measuring-the-impact-of-influence-operations/ ; Yang, "Towards a New Toolkit for Measuring AI-Enabled Influence Operations" (ICML 2026 workshop): https://icml.cc/virtual/2026/74732. [B6]

**AI persuasion**
- [P] Salvi, Horta Ribeiro, Gallotti & West, *Nature Human Behaviour* (2025), PDF mirror: https://www.rivista.ai/wp-content/uploads/2025/05/s41562-025-02194-6.pdf. [B6]
- [P] Costello, Pennycook & Rand, "Durably reducing conspiracy beliefs through dialogues with AI," *Science* (Sept 2024); [S] Cornell Chronicle: https://news.cornell.edu/node/329310. Re-confirmed for this synthesis. [S] Boissin, Costello et al., *PNAS Nexus* (2025), via PsyPost: https://www.psypost.org/ai-conversations-can-reduce-belief-in-conspiracies-whether-or-not-the-ai-is-recognized-as-ai. [B6]
- [S] Hackenburg & Margetts, *PNAS* (2024), via OII: https://www.oii.ox.ac.uk/does-political-microtargeting-with-large-language-models-offer-persuasive-returns-ask-kobi-hackenburg-and-professor-helen-margetts/. [B6]
- [P] Hackenburg et al., "Levers of political persuasion," *Science* (2025); arXiv: https://arxiv.org/html/2507.13919v1 ; [S] OII: https://www.oii.ox.ac.uk/oxford-researchers-reveal-how-conversational-ai-can-change-political-opinions/. [B6]
- [S] Zurich r/changemyview case: The Decoder: https://the-decoder.com/researchers-used-ai-to-manipulate-reddit-users-scrapped-study-after-backlash/ ; NBC News: https://www.nbcnews.com/news/rcna203597 ; Live Science: https://www.livescience.com/technology/artificial-intelligence/ai-researchers-ran-a-secret-experiment-on-reddit-users-to-see-if-they-could-change-their-minds-and-the-results-are-creepy ; 404 Media (headline): https://404media.co/reddit-issuing-formal-legal-demands-against-researchers-who-conducted-secret-ai-experiment-on-users. Re-confirmed for this synthesis. The claim that prompts told the model users had consented is **UNVERIFIED**. [B6]

**Prosocial precedents**
- [S] Munger, "Tweetment Effects," *Political Behavior* (2017), via CSMaP: https://csmapnyu.org/research/academic-research/tweetment-effects-on-the-tweeted-experimentally-reducing-racist-harassment. Account construction and consent details **UNVERIFIED**. [B6]
- [S] Bail et al., *PNAS* (2018), via Phys.org: https://phys.org/news/2018-09-caught-political-echo-chamber-opposition.pdf. [B6]
- [P] Combs, Bail et al., DiscussIt, *Nature Human Behaviour* (2023): https://www.nature.com/articles/s41562-023-01655-0. Effect sizes not re-fetched (**UNVERIFIED**). [B6]
- [P] Argyle, Bail, Busby et al., *PNAS* (2023): https://arxiv.org/pdf/2302.07268. [B6]
- [S] X AI Note Writer launch (July 2025), via BetaNews: https://betanews.com/2025/07/02/x-launches-ai-bot-pilot-to-write-community-notes-fact-checkers/ ; Twitter "Automated by" label, via TechCrunch: https://techcrunch.com/2022/02/16/twitter-officially-launches-labels-to-identify-the-good-bots. [B6]

**Rules, law and ethics**
- [P] X automation rules: https://help.x.com/en/rules-and-policies/x-automation ; X authenticity policy: https://help.x.com/en/rules-and-policies/authenticity ; Meta inauthentic behavior policy (did not render; wording **UNVERIFIED**): https://transparency.meta.com/policies/community-standards/inauthentic-behavior ; Bluesky community guidelines: https://bsky.social/about/support/community-guidelines. Whether any Bluesky labeler offers a "bot" label is **UNVERIFIED**. [B6]
- [P] European Commission, AI Act Article 50 FAQ: https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act ; [S] DSA Article 34: https://www.springlex.eu/en/packages/dsa/dsa-regulation/article-34/. [B6]
- [P] California B&P §17941 (BOT Act): https://california.public.law/codes/business_and_professions_code_section_17941. Platform threshold (§17940) **UNVERIFIED**. [P] AB 410 (2025) status: https://legiscan.com/CA/text/AB410/2025. [B6]
- [S] FTC fake-reviews rule (16 CFR Part 465), via Hunton: https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots. Wider FTC AI-impersonation rulemaking **UNVERIFIED**. [B6]
- [P] 45 CFR 46.116 (fetch blocked; re-verify): https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116 ; Menlo Report (DHS 2012): https://www.caida.org/publications/papers/2012/menlo_report/menlo_report.pdf ; APA Ethics Code 8.07 (not re-fetched). [B6]
- [P] Susser, Roessler & Nissenbaum, "Online Manipulation: Hidden Influences in a Digital World": https://philarchive.org/archive/SUSOMHv1. [B6]

### J. Girard, hyperstition, reflexivity and the mimetic state machine
Added with B7. Items already listed above and also cited by [B7]: Girard (D), Dryzek & Niemeyer and Landemore (D), Manheim & Garrabrant (F), vTaiwan (E), Bail et al. (G).

**Girard and Girardians**
- [S] Andrade, "René Girard (1923–2015)," *Internet Encyclopedia of Philosophy*: https://iep.utm.edu/girard/. Arc of mimetic theory; criticisms. [B7]
- [P] Girard, *Battling to the End: Conversations with Benoît Chantre* (MSU Press, 2009; *Achever Clausewitz*, 2007), publisher page: https://msupress.org/9780870138775/battling-to-the-end/ ; [S] Haven, NBCC review (2010): https://www.bookcritics.org/2010/01/12/nbcc-featured-review-cynthia-l-haven-on-rene-girard/ ; [S] Frieze review: https://frieze.com/article/battling-end-conversations-beno%C3%AEt-chantre. Escalation to extremes. [B7]
- [S] Megoran, review of *I See Satan Fall Like Lightning* (2003): https://www.staff.ncl.ac.uk/nick.megoran/iFrame/iSatanFall.html ; Girard's "other totalitarianism" passage as quoted in *The American Conservative*: https://www.theamericanconservative.com/rene-girard-covington-catholic-boys/. [B7]
- [P] Shullenberger, "The Scapegoating Machine," *The New Inquiry* (30 Nov 2016): https://thenewinquiry.com/the-scapegoating-machine ; Thiel–Girard essay, *Cyborgology* (9 Aug 2016): https://thesocietypages.org/cyborgology/?p=21451. [B7]
- [P] Thiel, "The Straussian Moment," in Hamerton-Kelly (ed.), *Politics and Apocalypse* (MSU Press, 2007; from a 2004 symposium): https://muse.jhu.edu/books/9781609170417 ; https://archive.org/details/the-straussian-moment. Date per secondary sources and catalog record. [B7]
- [S] Dupuy, *The Mark of the Sacred* (Stanford UP, 2013), description: https://ingramacademic.com/products/the-mark-of-the-sacred-9780804776899 ; Childs, review of Dupuy, *How to Think About Catastrophe* (2023): https://journals.ub.uni-giessen.de/kult-online/article/download/1510/1719/4164?inline=1 ; Dupuy, *Economy and the Future* (2014): https://mitpressbookstore.mit.edu/book/9781611861464. Dupuy's fixed-point formalism is **UNVERIFIED**. [B7]
- [S] Dumouchel, *The Ambivalence of Scarcity and Other Essays* (MSU Press, 2014): https://msupress.org/9781628960006/the-ambivalence-of-scarcity-and-other-essays. [B7]
- [S] Burgis, *Wanting* (2021), summary: https://www.artofmanliness.com/character/self-improvement/thick-desires-anti-mimetic-life/. Framing, not evidence. [B7]
- [V] Parachute `vault/research/thiel-karp-genealogy/texts/girard-apocalyptic-turn`. [B7]

**Hyperstition, performativity, reflexivity**
- [P] Carstens, "Hyperstition: An Introduction" (interview with Nick Land, 2009): https://www.orphandriftarchive.com/articles/hyperstition-an-introduction/ ; [S] Nick Land: https://en.wikipedia.org/wiki/Nick_Land. [B7]
- [V] Parachute `wiki/concepts/hyperstition`. [B7]
- [P] GreenPill S10E8, "Hyperstitions: How Beliefs Become Reality in Networked Systems, with Jake Hartnell" (30 Dec 2025): https://sites.libsyn.com/400481/s10-ep8-hyperstitions-how-beliefs-become-reality-in-networked-systems-with-jake-hartnell ; Owocki, "Hyperstitions: how shared beliefs shape onchain realities" (Gitcoin, 5 Mar 2026): https://gitcoin.co/research/hyperstitions-how-shared-beliefs-shape-onchain-realities ; [S] Hartnell profile: https://cryptoslate.com/people/jake-hartnell/ ; https://www.ischool.berkeley.edu/events/2022/dao-first-world. [B7]
- [V] Parachute: `vault/messages/telegram/jake-hartnell` (2025-10-24); `vault/meetings/2025-12/2025-12-01_collaboration-monster-immersion-jam` (Hyperstition Markets → Incentives Markets); `vault/people/jake-hartnell`; `vault/projects/local-alternatives/reports/2026-09-04_sensor-networks-prediction-markets-dialogue-report` (prediction markets as hyperstition; pro-social gameability). The speaker identity of "Michael" and the Paris-thermometer anecdote are **UNVERIFIED**. Hartnell's preferred characterization is to be confirmed (Q23). [B7, B8]
- [P] Yu et al., "Memes, Markets, and Machines… through Hyperstition," arXiv 2410.23794: https://arxiv.org/pdf/2410.23794. [B7]
- [P] Biggs, "Self-Fulfilling Prophecies," *Oxford Handbook of Analytical Sociology* (2009), incl. Merton 1948: https://users.ox.ac.uk/~sfos0060/prophecies.shtml. [B7]
- [P] Soros, "Fallibility, Reflexivity, and the Human Uncertainty Principle," *J. Economic Methodology* (2014): https://www.georgesoros.com/2014/01/13/fallibility-reflexivity-and-the-human-uncertainty-principle-2/. [B7]
- [P] MacKenzie, *An Engine, Not a Camera* (MIT Press, 2006); [S] discussion: https://organizationsandmarkets.com/2006/11/14/pomo-periscope-vi-performativity/. The typology is **UNVERIFIED** here. Callon, *The Laws of the Markets* (1998): **UNVERIFIED** (not fetched). [B7]
- [P] Perdomo, Zrnic, Mendler-Dünner & Hardt, "Performative Prediction," ICML 2020: https://proceedings.mlr.press/v119/perdomo20a.html. [B7, B8]
- [S] Campbell's law (1979): https://en.wikipedia.org/wiki/Campbell%27s_law. [B7]
- [P] Deci, Koestner & Ryan, *Psychological Bulletin* (1999), meta-analysis: https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf ; Gneezy & Rustichini, "A Fine is a Price" (2000): https://Rady.ucsd.edu/_files/faculty-research/uri-gneezy/fine.pdf. [B7]

**State machine and opinion dynamics**
- [P] Rossetti & Cazabet, "Community Discovery in Dynamic Networks: a Survey," arXiv 1707.03186 / ACM CSUR 2018: https://arxiv.org/abs/1707.03186v3. Taxonomy details **UNVERIFIED** (abstract only). [B7]
- [P] Noorazar et al., "From classical to modern opinion dynamics," arXiv 1909.12089: https://arxiv.org/abs/1909.12089. DeGroot, Friedkin–Johnsen, Hegselmann–Krause, Deffuant–Weisbuch. [B7]
- [P] Hegselmann & Krause, *JASSS* 5(3) (2002): https://www.jasss.org/5/3/2.html ; Deffuant et al., "Mixing beliefs among interacting agents" (2000): https://next.sciencegate.app/document/10.1142/s0219525900000078. [B7]
- [P] Ye, Qin, Govaert, Anderson & Cao, expressed-vs-private opinion (EPO) model: https://arxiv.org/pdf/1806.11236. [B7]
- [P] Axelrod, Daymude & Forrest, "Preventing extreme polarization of political attitudes," *PNAS* (2021): https://pmc.ncbi.nlm.nih.gov/articles/PMC8685667. [B7]
- [P] Flache et al., "Models of Social Influence: Towards the Next Frontiers," *JASSS* (2017), title and venue only: https://econpapers.repec.org/RePEc:jas:jasssj:2017-90-1. Abstract **UNVERIFIED**. Esteban–Ray polarization index: **UNVERIFIED** (not fetched). [B7]

**Democracy and deliberation**
- [P] Fishkin, Siu, Diamond & Bradburn, "Is Deliberation an Antidote to Extreme Partisan Polarization?" *APSR* (2021): https://deliberation.stanford.edu/publications/journal-articles/deliberation-antidote-extreme-partisan-polarization-reflections. [B7]
- [P] Voelkel et al., "Megastudy testing 25 treatments to reduce antidemocratic attitudes and partisan animosity," *Science* (2024): https://sociology.stanford.edu/scalable-interventions-reduce-polarization-support-partisan-violence-and-anti-democratic-attitudes ; HKS abstract page: https://www.hks.harvard.edu/publications/megastudy-testing-25-treatments-reduce-antidemocratic-attitudes-and-partisan-animosity ; Kellogg summary: https://www.kellogg.northwestern.edu/academics-research/research/detail/2024/megastudy-testing-25-treatments-to-reduce-anti-democratic-attitudes/?p=1. Checked for this synthesis (VERIFICATION §E). [B7]
- [P] Broockman, Kalla & Westwood, "Does Affective Polarization Undermine Democratic Norms or Accountability? Maybe Not," *AJPS* (2022): https://isps.yale.edu/node/25356. Checked for this synthesis (VERIFICATION §E). [B7]
- [P] Nature Human Behaviour (2021) 26-country replication of Lees & Cikara on group meta-perceptions: https://www.nature.com/articles/s41562-021-01092-x. Author list **UNVERIFIED** (not captured). [B7]
- [P] Veri & Niemeyer, "Deliberative reason and the effect of minipublic configurations," *EPSR* (2025): https://www.cambridge.org/core/product/F19135A60561D8925735B44C236E673A/core-reader. The Deliberative Reason Index; R package `deliberr` noted, not evaluated. [B7]
- [S] Irish Citizens' Assembly, Eighth Amendment (Participedia): https://participedia.net/case/5317. The ~66% referendum figure is **UNVERIFIED**. [B7]

### K. Open agents, registries, token incentives and strategy markets
Added with B8. Items already listed above and also cited by [B8]: X automation rules and Bluesky guidelines and moderation docs (H, I), Perdomo et al. (J), Hanson futarchy and BTS (F), Gneezy & Rustichini (J).

**Platform rules**
- [P] X automated account labels: https://help.x.com/en/using-x/automated-account-labels. Universal availability **UNVERIFIED**. X automation rules re-checked for this synthesis (VERIFICATION §E). [B8]
- [S] Astral (AI-agent author), "agent governance on ATProto" (Feb 2026; secondhand): https://astral100.leaflet.pub/3mearallcqi2w. Community `ai-agent` self-labels, labelers and lexicons **UNVERIFIED**. [B8]
- [P] Neynar, autonomous Farcaster agent guide: https://docs.neynar.com/docs/autonomous-farcaster-agent ; [S] The Block, Network School acquires Farcaster (2026-10-15): https://www.theblock.co/news/ecosystems/2026-10-15-network-school-acquires-farcaster-from-neynar-418720. Post-acquisition agent policy **UNVERIFIED**. [B8]

**Registries, identity, attestations**
- [P] ERC-8004 "Trustless Agents" (Draft ERC, created 2025-08-13): https://eips.ethereum.org/EIPS/eip-8004. Status re-checked for this synthesis (VERIFICATION §E). [S] QuickNode explorer: https://erc-8004.quicknode.com/agents/ethereum-mainnet/23034. Mainnet date and counts **UNVERIFIED**. [B8]
- [P] Ethereum Attestation Service: https://attest.org/ ; Hypercerts v0.2, "Why AT Protocol": https://hypercerts-v02-documentation.vercel.app/getting-started/why-atproto ; MACI v3 docs: https://maci.pse.dev/docs/introduction. [B8]
- [P] Olas staking: https://olas.network/staking. Slashing semantics **UNVERIFIED**. [B8]
- [P] Taostats, weight copying: https://docs2.taostats.io/concepts/weight-copying/ ; Lui & Sun, Bittensor critical analysis, arXiv 2507.02951: https://arxiv.org/pdf/2507.02951. [B8]
- [S] Cointelegraph, Virtuals agent-token launches and drawdowns (2025-02-07): https://cointelegraph.com/news/new-ai-agent-launches-virtuals-plummet-token-drawdowns ; The Defiant, World AgentKit (2026-03-17): https://thedefiant.io/news/infrastructure/world-launches-agentkit-to-let-ai-agents-carry-proof-of-human-backing. [B8]

**Prediction markets**
- [P] Berg, Nelson & Rietz, "Prediction Market Accuracy in the Long Run," *IJF* (2008): https://iemweb.biz.uiowa.edu/about-iem/research/prediction-market-accuracy-in-the-long-run/ ; Rothschild & Sethi: https://papers.ssrn.com/abstract=2322420 ; Hanson & Oprea, *Economica* (2009): https://ideas.repec.org/a/bla/econom/v76y2009i302p304-314.html. [B8]
- [P] Chen, Kash, Ruberry & Shnayder, decision markets with good incentives: https://projects.iq.harvard.edu/sites/projects.iq.harvard.edu/files/yiling/files/a6-chen.pdf. Full-support randomized decision rule. [B8]
- [S] Blockworks, futarchy and MetaDAO: https://blockworks.co/news/understanding-futarchy-on-solana ; EA Forum, Metaculus vs Manifold (2023): https://forum.effectivealtruism.org/posts/PGqu4MD3AKHun7kaF/predictive-performance-on-metaculus-vs-manifold-markets. [B8]
- [S] Cases: The Block, French whale: https://www.theblock.co/post/324996/french-polymarket-whale-us-election-profit-france-ban ; Decrypt, Columbia wash-trading study (Sirolly et al., Nov 2025): https://decrypt.co/347842/columbia-study-25-polymarket-volume-wash-trading ; The Block, UMA governance attack: https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented ; Decrypt, Zelensky suit market: https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyys ; The Block, Nobel probe: https://www.theblock.co/post/374199/officials-probe-polymarket-over-suspicious-trades-predicting-nobel-peace-prize-winner-reports ; WGBH/NPR, Kalshi insider cases (2026-02-25): https://www.wgbh.org/news/2026-02-25/kalshi-reveals-insider-trading-case-against-editor-for-mrbeast ; Finance Magnates, *US v. Van Dyke*: https://www.financemagnates.com/trending/us-charges-soldier-in-first-insider-trading-case-linked-to-prediction-markets/ ; Bloomberg (excerpt only): https://www.bloomberg.com/news/articles/2026-04-25/insider-trading-cases-threaten-reckoning-for-prediction-markets ; Euronews, Paris weather-sensor tampering: https://www.euronews.com/2026/04/23/hair-dryer-trick-behind-25000-win-france-probes-potential-weather-data-scam-linked-to-poly. The hair-dryer detail is **UNVERIFIED**. [B8]
- [P] CRS Legal Sidebar LSB11441, CFTC proposed event-contract rule (June 2026): https://www.everycrsreport.com/files/2026-06-24_LSB11441_b1797929d9c973e7d2962416b42af20eddfea3e4.html ; Federal Register 2026-05105 (not read; **UNVERIFIED**): https://www.govinfo.gov/content/pkg/FR-2026-03-16/pdf/2026-05105.pdf. [B8]

**Measurement and elicitation**
- [P] Mastroianni, Dana & Nichols, ideological Turing test (2024): https://www.experimental-history.com/p/ideological-turing-test. ITT discrimination for distant clusters **UNVERIFIED**. [B8]
- [P] Shnayder, Agarwal, Frongillo & Parkes, "Informed Truthfulness in Multi-Task Peer Prediction," EC 2016: https://arxiv.org/abs/1603.03151v2. [B8]
- [P] Yu, Gao, Bennett & Joseph, "Evaluating Voting Design Vulnerabilities for Retroactive Funding," arXiv 2505.16068: https://arxiv.org/html/2505.16068v1. [B8]

**Funding, tokens, law**
- [P] Optimism, RetroPGF 3 learnings: https://www.optimism.io/blog/retropgf-3-learnings-reflections ; "Evolution of Retro Funding in Season 8": https://gov.optimism.io/t/evolution-of-retro-funding-in-season-8/10024 ; Season 7 early evidence: https://gov.optimism.io/t/season-7-retro-funding-early-evidence-on-onchain-builders-impact/10163. [B8]
- [S] Debevoise, SEC interpretive release (2026-03-17): https://www.debevoise.com/insights/publications/2026/03/crypto-unchained-the-secs-pivotal-interpretive-rel. Not legal advice; prize-tournament and state gambling status **UNVERIFIED**. [B8]
- [P] Gneezy & Rustichini, "Pay Enough or Don't Pay at All," *QJE* (2000): https://econpapers.repec.org/RePEc:oup:qjecon:v:115:y:2000:i:3:p:791-810. [B8]

### L. Design-dialogue lineages and the transcript pipeline (B9)
Added 2026-10-30 from the Design Dialogue Memo; filled from brief B9 (`wave-1/B9-reciprocal-opening-landry-society-library-transcripts.md`). B9's transcript conclusion was corrected by Benjamin the same day: YouTube transcripts remain the primary source (a ToS gray area, not a blocker).
- [V] *Dialogos Arena — Design Dialogue Memo*, Benjamin Life (@omniharmonic) with Claude, 2026-10-30: `/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md`; Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`; artifact https://claude.ai/artifact/Vm3DUhXucW2ZKjjtMEyoi8. The decision record behind §2. [memo]

**Reciprocal narrowing and reciprocal opening (feed rule, §2 D9, §8.6)**
- [S] Olshonsky, A. "Addiction Is Between You and the World," *Deep Fix*, 2022-12-23: https://deepfix.substack.com/p/addiction-is-between-you-and-the. Lewis's reciprocal narrowing and Vervaeke's reciprocal opening glossed. [B9]
- [P] John Vervaeke on *This Past Weekend w/ Theo Von* #462 (transcript): https://rosetta.to/u/theovon/john-vervaeke-this-past-weekend-w-theo-von-462. Credits a colleague's theory; reciprocal opening tied to love. [B9]
- [P] Jim Rutt Show EP 143, John Vervaeke Part 1 (transcript): https://jimruttshow.blubrry.net/?p=3299. Reciprocal opening; social media and the meaning crisis. [B9]
- [S] Petersonsphere glossary, "Reciprocal Narrowing": https://petersonsphere.github.io/Petersonsphere/Glossary-of-Terms/Reciprocal-Narrowing. Aliases: parasitic processing, addiction-forming process. [B9]
- [S] *Awakening from the Meaning Crisis* Ep. 13, "Buddhism and Parasitic Processing" (listing): https://metacast.app/podcast/dr-john-vervaeke/0YbNdI5Y/ep-13---awakening-from-the-meaning-crisis---buddhism-and-parasitic-processing/rIcFQ22k. The episode that first states reciprocal narrowing is **UNVERIFIED**. [B9]
- Marc Lewis, *The Biology of Desire* (origin of reciprocal narrowing): cited via the sources above, not read directly. No Vervaeke text applying the idea to ranking algorithms was found (**UNVERIFIED / likely absent**); "algorithm in reverse" is Benjamin's extension. [B9]

**Forrest Landry's Ephemeral Group Process (§2 D22, §6.5)**
- [P] EGP site: https://egp.community/ and https://egp.community/what-is-egp/. Inquiry first; base and branch questions; Inquiry Coach; archive. Names no creator, events or archive. [B9]
- [S] Life Itself wiki, "Ephemeral Group Process": https://notes.lifeitself.org/ephemeral-group-process. Steps and scale (~30–300 people). [B9]
- [P] Jim Rutt Show EP 153, Forrest Landry on the Small Group Method (transcript): https://jimruttshow.blubrry.net/?p=3679. EGP as a later "level two" stage of a larger body of work. [B9]
- The Stoa session (2020): recording **not located (UNVERIFIED)**. No published EGP outputs or case studies found. [B9]

**Jamie Joyce and the Society Library (§7.5)**
- [P] Jim Rutt Show Currents 076, Jamie Joyce on The Society Library (transcript): https://jimruttshow.blubrry.net/?p=4187. Topic flyover; claim IDs with all source quotes; steelmanning; status labels, not true/false. [B9]
- [P] Joyce, J. "Your Attempt To Refute Argument Maps Will Not Work," 2026-05-06: https://justjamiejoyce.substack.com/p/your-attempt-to-refute-argument-maps. 20+ relation types; Diablo Canyon map scale (~8,000 research hours); AI-assisted future. [B9]
- [S] Deep Tech Week, Society Library profile: https://www.deep-tech-week.com/organizations/the-society-library. [B9]
- [S] *You Are Not So Smart* 292, the Society Library (2024-07-22): https://youarenotsosmart.com/2024/07/22/yanss-292-how-one-organization-is-attempting-to-end-analysis-paralysis-by-creating-a-library-of-our-collective-arguing/. [B9]
- societylibrary.org was not fetched. "Papers of record" as Society Library terminology and any crowd- or Community-Notes-like ratification work are **UNVERIFIED**. [B9]
- [V] Parachute `vault/messages/twitter/jamie-joyce-twitter` (friendly DM thread, 2021–2024; basis for Q38); `vault/meetings/2024-02/2024-02-14_civic-innovation-summit` (not reviewed). [B9]

**Community Notes, Polis and vTaiwan (portability lineage, §7.5)**
- [P] Wojcik, Coleman et al., "Birdwatch: Crowd Wisdom and Bridging Algorithms…" (2022), arXiv 2210.15723: https://arxiv.org/abs/2210.15723. Bridging intercept = portability. See also sections E and H. [B9, B2, B5]
- [P] "Scaling human judgment in Community Notes" (2025), arXiv 2506.24118: https://arxiv.org/abs/2506.24118. LLM-drafted notes, human-rated. Not fetched; authors **UNVERIFIED**. [B9]
- [P] Polis / Computational Democracy Project: https://compdemocracy.org/ ; vTaiwan: https://info.vtaiwan.tw/. Not fetched in B9 (prior knowledge); vTaiwan's stalling when non-binding is in section E [B2, B7]. [B9]

**Transcript pipeline (§6.2, §11.1, R49, spec 4)**
- [P] YouTube Data API error reference: https://developers.google.com/youtube/data/reference/rest/v3/errors ; [S] Stack Overflow Q41087864 (Kiwix mirror), third-party caption download: https://kaweah.freedombox.rocks/kiwix/content/stackoverflow.com_en_all_2023-11/questions/41087864/youtube-api-v3-download-captions-from-third-party-videos-without-asking-for-au. Official `captions.download` is owner-only (docs page not fetched). [B9]
- [P] YouTube Terms of Service: https://www.youtube.com/terms. Prohibits automated access outside the official API. **Corrected reading (2026-10-30):** transcript libraries (e.g., `youtube-transcript-api`) and paid transcript services are routine and feasible; a ToS gray area tracked as R49, not a blocker. [B9]
- [S] "Speech-to-Text API Pricing 2026" (vendor-adjacent): https://convertaudiototext.com/blog/speech-to-text-api-pricing-2026. Source of the STT prices behind B9's cost ESTIMATES (verify on vendor pages). Commercial YouTube-transcript service pricing **UNVERIFIED**; podcast transcript APIs (Podscan, Listen Notes, Taddy) **UNVERIFIED**. [B9]
- [P] 17 U.S.C. §102(b); *Authors Guild v. Google*, 804 F.3d 202 (2d Cir. 2015); *Bartz v. Anthropic* (N.D. Cal., June 2025). Cited from prior knowledge; not legal advice. [B9]

- Kevin Owocki, "Attention Times" daily paper (companion to the Atlas): model for the daily pulse (§6.6). See section C. [memo §9]
