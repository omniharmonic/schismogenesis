# The Adversarial and Commercial Narrative-Intelligence Field, and How It Maps the Narrative Landscape (as of 1 Nov 2026)

> Evidence labels used below. **[Vendor claim]**: stated by the seller, not independently tested. **[Observed]**: I looked at the artifact itself (a screenshot, patent or document). **[Independent]**: court record, journalism or peer-reviewed work. "Mockup" means the vendor's own marketing image, which may not be a live screen. The session's web-search budget ran out partway through, so items that could not be checked are listed under Gaps rather than filled from memory.

## 1. Blackbird.AI: what Constellation, Compass and the narrative visuals are, and how it defines its terms

### Takeaway
Blackbird sells a client-centred threat console: claims are grouped into "narrative objects", enriched with bot, anomaly, toxicity and cohort signals, and ranked into a priority scorecard. Its definition of a "narrative attack" does not require falsehood, and its own example screen rates a narrative with low bot, anomaly and toxicity signals as High priority. No published accuracy figures or scoring formula were found.

### Cited Findings

**Company and product line**
- Legal entity is Socialtrendly Inc, d/b/a BlackbirdAI — [Google Patents, US12639533B2](https://patents.google.com/patent/US12639533B2/en); the RAV3N RISK LLM trademark was filed by SocialTrendly in February 2024 — [Justia](https://trademarks.justia.com/984/18/rav3n-risk-98418003.html).
- Product family per its own site: Constellation Platform (Constellation Dashboard, Narrative Feed, Constellation API); Compass (Compass Context for claims, Compass Vision for deepfakes and AI images); RAV3N (Radar, Watch, Recon, Agent, plus a human research team) — [Blackbird platform page](https://blackbird.ai/platform).
- Customers named: large enterprises, public sector, national security and defense, critical infrastructure, financial institutions, executive protection, corporate communications and PR, legal and compliance — [Blackbird AI info page](https://blackbird.ai/ai-info/). A PR-channel partnership with Weber Shandwick ("Media Security Center") exists, but the fetched page held only the headline — [Blackbird news item](https://blackbird.ai/in-the-news/weber-shandwick-launches-media-security-center-via-partnership-with-blackbird-ai).

**Pricing category (the one hard number set)**
- AWS Marketplace lists 12-month SaaS packages: Starter $54,800; Enterprise $75,000; Strategic $175,000; Strategic Plus $299,000. These scale users (5 to 15), Compass queries (1,000 to 3,000 per month), artifacts per year (500,000 to 10 million), Recon reports and analyst support hours. Fees are non-cancellable — [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-7dyxpokn2tuhg). The vendor's own site says only that pricing comes through direct engagement — [Blackbird AI info page](https://blackbird.ai/ai-info/).

**Definitions, quoted from the vendor**
- Narrative: "any assertion that shapes perception about a person, place or thing in the information ecosystem" — [Blackbird glossary](https://blackbird.ai/glossary-of-terms/).
- Narrative attack: the glossary says an attack occurs "when misinformation and disinformation tactics enable these narratives to scale and become harmful" — [glossary](https://blackbird.ai/glossary-of-terms/). A different vendor page drops the tactics condition: "any assertion that can cause harm by shaping perceptions about a person, place, or thing" — [What is Narrative Risk?](https://blackbird.ai/narrative-attacks/). The AI info page uses that wider wording too, and also says narrative attacks are "coordinated, sustained efforts" — [AI info page](https://blackbird.ai/ai-info/). So the vendor's definitions conflict with each other.
- Cohort: "like-minded communities segmented to understand how online groups interact with key narratives" — [glossary](https://blackbird.ai/glossary-of-terms/). High-Risk Cohorts: "Percentage of involvement of high-risk cohorts, such as political partisan cohorts and foreign state actors" — [glossary](https://blackbird.ai/glossary-of-terms/).
- Bot-Like Activity: "activity not coming from a human, programmed to do harm and to accelerate the trajectory of harmful narratives". Anomalous Activity: "inorganic behavior and manipulation that amplify or dampen a narrative and its spread". Manipulation: "Percentage of manipulation coming from bots and trolls" — [glossary](https://blackbird.ai/glossary-of-terms/).
- Narrative Risk Score: no formula is published. Narrative Feed is said to rank narratives on "hundreds of risk signals", tailorable to each customer's risk profile — [Narrative Feed PDF](https://blackbird.ai/wp-content/uploads/2025/04/bb-narrativefeed.pdf); [engineering blog](https://blackbird.ai/blog/engineering-blackbird-ai-constellation-narrative-intelligence-platform/). The FAQ names toxicity, bot-like activity, anomalous behavior, polarization and manipulation, with no weights — [What is Narrative Risk?](https://blackbird.ai/narrative-attacks/).

**How it is built [Vendor claim]**
- Pipeline: identify "specific assertions", group "identical claims into what we call narrative objects", each holding one claim with a shared stance across languages and phrasing; enrich with bot, manipulation, cohort and timeline signals; combine scores into priority rankings; cross-reference with Compass Context. Analysts see "20 narratives ranked by danger" and pivot among content, actors and behavior lenses. It claims "roughly 95% noise reduction" with no baseline given — [Blackbird blog](https://blackbird.ai/blog/blackbird-ai-turns-millions-of-posts-into-actionable-narrative-intelligence/).
- The 2019 design used a graph database, and Constellation maps accounts, content and hashtags into graphs displayed as clusters — [engineering blog](https://blackbird.ai/blog/engineering-blackbird-ai-constellation-narrative-intelligence-platform/).
- Compass context checking adds sourced context rather than true/false labels. The article offers no accuracy metrics, benchmarks or error rates — [Compass blog](https://blackbird.ai/blog/compass-by-blackbird-ai-help-organizations-fight-narrative-attacks). "Known for high accuracy" appears on the AI info page with no measurement — [AI info page](https://blackbird.ai/ai-info/).
- Five framing signals: narratives, networks, cohorts, anomalous behavior, influence — [AWS listing](https://aws.amazon.com/marketplace/pp/prodview-7dyxpokn2tuhg); [platform page](https://blackbird.ai/platform). The January 2023 release also promises "heatmapping of narrative flow within information networks" — [Blackbird release](https://blackbird.ai/?p=1429).

**What the screens show [Observed; all are vendor mockups, so treat as illustrative]**
- **Constellation Dashboard** ([network-graph-mockup-2.jpg](https://blackbird.ai/wp-content/uploads/2024/10/network-graph-mockup-2.jpg)): a dark, green-on-black force-style graph. Hub nodes with person icons fan out into dense white hemispheres of leaf accounts, plus a background of faint edges and scattered points. It has no labels, legend, axes, time or scale. The filename itself says "mockup".
- **Narrative Feed** ([narrative-feed-3.jpg](https://blackbird.ai/wp-content/uploads/2024/12/narrative-feed-3.jpg)): project selector reading "Woke Airline Industry"; headline "Boeing rewards CEO and executives for hitting DEI targets instead of increasing profit and prioritizing safety"; an LLM summary saying the change was "revealed in SEC filings", was discussed by "right-wing influencers", and naming James A. Lindsay. Right-hand **Narrative Scorecard**: Priority High; Bot-Like Low; Anomalous Low; Toxicity Low; Compass risk High; Negative sentiment High. Overlays: a red speedometer gauge reading HIGH PRIORITY, and a Compass Context card (Claim, Context, "misleading" verdict text, COMPASS RISK: High).
- **Compass** ([compass.jpg](https://blackbird.ai/wp-content/uploads/2024/10/compass.jpg)): a "Check Any Claim" box prefilled with "What are the top narrative attacks targeting my company?", then claim examples.
- **RAV3N Recon** ([rav3n-recon-platform.jpg](https://blackbird.ai/wp-content/uploads/2026/03/rav3n-recon-platform.jpg)): a "Risk Assessment Report" form with a TARGET SUBJECT field ("J. Smith", marked Verified), category "Influencers", period, platform checkboxes including Dark Web and Forums, and tiers Quick Check, Deep Risk Scan, and Forensic Audit (enterprise only).
- **Narrative Feed PDF** cover also shows a list of narrative titles with a detail pane, and describes an "easy-to-view narrative scorecard" — [PDF](https://blackbird.ai/wp-content/uploads/2025/04/bb-narrativefeed.pdf). A third page lists five scorecard categories: Compass Risk, Bot-Like, Toxicity, Anomalous, Negativity — [Blackbird narrative pulse page](https://blackbird.ai/narrative-pulse).

**Patents**
- US12639533B2 (priority 2023-01-25, published 2026-05-26) covers multilingual training by machine translation with label projection. It is not about cohorts or bots; narrative attacks appear only as an example task — [Google Patents](https://patents.google.com/patent/US12639533B2/en). A third-party profile claims 3 full filings and 10 provisionals, unconfirmed — [AI Market Watch](https://www.ai-market-watch.com/company/blackbird-ai).

**Market recognition (not capability evidence)**
- Blackbird reports Gartner's December 2025 "Company to Beat" label and Market Shaper status in the June 2026 Emerging Market Quadrant; Cyabra reports Market Shaper too. Both are vendor-relayed — [Blackbird](https://blackbird.ai/blog/gartner-names-blackbird-ai-company-to-beat-for-narrative-intelligence/); [Cyabra](https://cyabra.com/reports/cyabra-named-market-shaper-in-2026-gartner-emq-narrative-intelligence/). Gartner's indexed abstract confirms the Quadrant report exists — [Gartner](https://www.gartner.com/en/documents/8060233).

**Activists and legitimate speech, in its own materials**
- A beverage case study describes "a cohort of politically leaning activists, existing customers, and hyper-driven influencer groups" who pushed "harmful" storylines against a brand. Customers appear inside the threat cohort — [case study](https://blackbird.ai/case-studies/food-beverage/).
- A nonprofit case study says the client's monitoring "cannot separate legitimate criticism from coordinated narrative attacks", and positions Constellation as the fix — [case study](https://blackbird.ai/case-studies/nonprofit-social-impact-organizations/).

### Inferences
- The Boeing mockup is the most revealing artifact found. All behavioral signals are Low, the source is SEC filings, and it is still High priority, driven by a "misleading" context check and negative sentiment. On Blackbird's own display, "priority" here tracks reputational harm to the client, not manipulation. Caution: this is one marketing mockup, not a measured distribution.
- The name "Compass" is doing rhetorical work: a context check supplies a risk grade, so "we don't issue true/false labels" coexists with a label called High risk.
- The "narrative object" (one assertion plus one stance, with variants attached) is structurally nearly identical to Dialogos's neutral proposition with stance. The difference is the governance around it, not the data type. That supports Turquoise Sound's observation: the two are close in form and opposite in purpose.
- The Constellation visual is built to impress more than to inform. Having no legend or scale means it cannot be disputed. A Dialogos map should treat that as the anti-pattern, even while borrowing the sense of hubs and audiences.

### Gaps
- No live product demo, API docs or logged-in screenshots were accessible. Every screen above is marketing.
- No filed patent covering narrative clustering, cohorts or bot detection was found. USPTO assignee search was not possible here.
- The cohort-assignment method (how an account joins a cohort, whether individuals are labelled) is unpublished.
- No independent evaluation or investigative critique of Blackbird was found; one search returned only vendor pages. This means "none found", not "none exists".
- Funding details: the release page was blocked (HTTP 403/429). A $28M figure and 118% ARR growth appear only in press-release titles.

## 2. Comparable systems: recurring visual forms and shared data structures

### Takeaway
The field converges on one data shape, a multilayer graph of actors, content and claim clusters over time with scores attached, and about six visual forms. The same maps are sold for defense, brand and targeting work. The strongest validity warnings come from cases where the method or account list stayed hidden.

### Cited Findings

**Graphika (the canonical network map)**
- US patent 8,635,281 "System and method for attentive clustering and analytics": inventor John W. Kelly, Morningside Analytics, now Graphika Technologies; granted 21 Jan 2014 — [Google Patents](https://patents.google.com/patent/US8635281B2/en).
- Method: a mixed-mode network of source nodes and outlink targets; sources with "similar linking history" form an *attentive cluster*; targets with similar citation patterns form *outlink bundles*; many clustering algorithms are allowed — [Google Patents](https://patents.google.com/patent/US8635281B2/en).
- Display: the "proximity cluster" map uses a spring embedder (Fruchterman-Reingold named as an option). Each node is a dot, size reflects centrality, color marks cluster, and a general force pushes dots toward a circular border. Event data (phrases, links) is overlaid on the map — [Google Patents](https://patents.google.com/patent/US8635281B2/en); [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8635281).
- Current marketing [Vendor claim]: "Maintain a live view of how communities form, shift, and interact over time". It promises to "Improve targeting and segmentation accuracy", align messaging to how audiences "interpret and amplify content", and also detect orchestrated behavior. "Government & Defense" is listed as a sector — [Graphika use case](https://graphika.com/use-cases/audience-and-influence-mapping).

**Others**

| System | What it is / shows | Evidence status |
|---|---|---|
| PeakMetrics | Bipartite network graph: storylines as central nodes, linked to authors or domains; edge strength by contribution volume; threshold sliders. New narrative created when mentions fit no existing one | [Docs](https://docs.peakmetrics.com/help/workflows/network-graphs-visualize-the-web-of-influence.md) (vendor docs); clustering description via [search of vendor docs](https://docs.peakmetrics.com/help/peakmetrics-faqs/how-to-build-great-narratives.md), page later returned 404 |
| Cyabra | Fake-profile percentages, reports | **Contradicted**: Norway report (10 Aug 2025) claimed 269 fake profiles; [Faktisk.no](https://www.faktisk.no/artikkel/israeli-ai-firm-claims-fake-profiles-targeted-norwegian-pm-investigation-finds-several-were-real/127272) found at least four belonged to real people; methods undisclosed, no response from Cyabra. Nepal 34% "inauthentic" figure had no reviewable dataset — [Kathmandu Post](https://kathmandupost.com/national/2025/10/12/cyabra-report-on-nepal-gen-z-protest-comes-under-scrutiny) |
| Logically | AI fact-checking and narrative tool | Entered administration July 2025 after losing TikTok and Meta contracts; sold pre-pack to Kreatur Ltd — [Sifted](https://sifted.eu/articles/logically-ai-fact-check-misinformation-trump-tiktok-meta); [BusinessCloud](https://businesscloud.co.uk/news/rise-fall-of-yorkshire-firm-sold-in-pre-pack-administration-deal/embed/) |
| Alethea Artemis | Multi-channel disinformation analysis | Directory listing only — [SourceForge](https://sourceforge.net/software/product/Alethea-Artemis) |
| Primer | Command monitors narratives on public data; Delta analyzes private documents. Pitched to military information support operations | [Primer](https://primer.ai/solutions/narrative-monitoring-and-analysis); [Military Embedded](https://militaryembedded.com/ai/big-data/helping-special-forces-filter-out-the-data-noise) (vendor-derived) |
| Zignal Labs | Claims 8 billion posts a day, "curated detection feeds". Founded 2011 for PR firms and campaigns, moved to defense and intelligence about 2021. ICE signed $5.7M over five years via Carahsoft | [The Lever](https://www.levernews.com/ice-just-bought-a-social-media-surveillance-botice-just-bought-a-social-media-surveillance-bot/) (procurement records) |
| Recorded Future | Threat intelligence; early In-Q-Tel and Google Ventures money; Mastercard paid $2.65B in Sept 2024 | [Wikipedia](https://en.wikipedia.org/wiki/Recorded_Future) (secondary). "Intelligence Graph" not confirmed there |
| Narrative Science | **False friend**: generates prose from structured data (Quill). Bought by Salesforce in 2021, folded into Tableau. Not narrative detection | [Wikipedia](https://en.wikipedia.org/wiki/Narrative_Science) |
| NewsGuard | False Claim Fingerprints: one record per false claim, 42K+ instances with URLs, dates, excerpts; human verified, machine-readable feed | [NewsGuard](https://www.newsguardtech.com/solutions/misinformation-fingerprints/) (vendor) |
| GDELT GKG | Entities and themes tagged per article; about 13,000 themes reported | [GDELT](https://blog.gdeltproject.org/?p=57); [arXiv 2009.14281](https://arxiv.org/pdf/2009.14281) |
| Media Cloud | Open-source: Search, Directory (25,000+ sources), 1B+ stories; run by MEAG, UMass Amherst, Northeastern | [Media Cloud](https://www.mediacloud.org/) |
| Hamilton 68 | Time-series dashboard of top themes from a tracked account list | See below |
| DARPA INCAS | Detect, characterize and track campaigns "with quantified confidence"; says static demographic segmentation lacks explanatory power; complete | [DARPA](https://www.darpa.mil/research/programs/influence-campaign-awareness-and-sensemaking); [Proposers' Day slides](https://www.darpa.mil/attachments/INCASProp%20DaySlides2020-10-30a.pdf) |
| DARPA SocialSim | High-fidelity simulation of how information spreads; top-down vs. bottom-up trade-off; complete | [DARPA](https://www.darpa.mil/research/programs/computational-simulation-of-online-social-behavior) |
| NATO StratCom COE | January 2024 report on AI for target audience analysis, audience segmentation and psychological operations | [StratCom PDF](https://stratcomcoe.org/publications/download/AI-in-Support-of-StratCom-Capabilities-DIGITAL.pdf) |
| CounterCloud | 2023 anonymous demo: scraped targets, LLM-written counter-articles under fake journalist profiles, about $400 | [The Debrief](https://thedebrief.org/countercloud-ai-disinformation/); developer self-report, not verified |
| GoLaxy | Leaked documents: profiles on at least 117 US lawmakers and 2,000+ political and thought leaders, and a "GoPro" distribution system; firm denies targeting US officials | [Nextgov](https://www.nextgov.com/cybersecurity/2025/08/researchers-detail-new-gray-zone-conflict-ai-driven-chinese-propaganda/407358/); [The Register](https://theregister.com/2025/08/08/golaxy_ai_influence) |

**Hamilton 68**
- Launched August 2017 tracking 600 accounts "linked to Russian influence", list undisclosed; ended late 2018; version 2.0 (2019) tracked about 600 attributable state accounts with the list public — [Wikipedia](https://en.wikipedia.org/wiki/Hamilton_68). ASD merged into ISD-US effective 1 Jan 2026 — [same](https://en.wikipedia.org/wiki/Hamilton_68).
- Twitter's Yoel Roth reverse-engineered the list; reported finding: 36 of 644 accounts registered in Russia; he called the method "bizarre, and seemingly quite arbitrary" — [Wikipedia](https://en.wikipedia.org/wiki/Hamilton_68); [KUTV/Sinclair](https://kutv.com/news/nation-world/twitter-files-15-furthers-the-misunderstanding-of-hamilton-68-russian-disinformation-the-daily-caller-right-wing-talking-points-social-media-mainstream-media-nuance-methodolgy-extremism-donald-trump-matt-taibbi-research-interference-trolls-bots).
- ASD's defense: it always said some genuine Americans were on the list, that it did not track bots as such, and that media and lawmakers misused the data. That same Sinclair piece treats both sides critically — [KUTV/Sinclair](https://kutv.com/news/nation-world/twitter-files-15-furthers-the-misunderstanding-of-hamilton-68-russian-disinformation-the-daily-caller-right-wing-talking-points-social-media-mainstream-media-nuance-methodolgy-extremism-donald-trump-matt-taibbi-research-interference-trolls-bots). The Washington Post reportedly issued corrections — [Fox News](https://www.foxnews.com/media/washington-post-forced-issue-several-corrections-russian-bot-stories-following-twitter-files.amp) (partisan source, not checked against the Post).

**Market framing**
- Gartner abstracts describe narrative intelligence as one of three disinformation-security clusters, alongside content authentication and impersonation prevention — [Gartner abstract](https://www.gartner.com/en/documents/7861081). Dates and clusters came through search summaries.

### Inferences

**Recurring visual forms** (my synthesis across the above)
1. Force-directed community map: color = cluster, size = centrality (Graphika, Constellation).
2. Bipartite storyline-to-source graph (PeakMetrics).
3. Ranked narrative feed with an LLM summary (Blackbird, likely others).
4. Scorecard or gauge: categorical risk (Blackbird).
5. Time-series of volume per narrative (Hamilton; implied elsewhere).
6. Report-style annotated map overlays (Graphika event overlays).

**Shared data structure** (inferred)
- Actor (account, outlet) — posts — Content item — instance-of — Claim or narrative cluster — carried-by — Community, all timestamped, with derived scores on edges and nodes. Dialogos's proposition, stance, landmark and cluster tables are a close relative. The main differences are consent and quote provenance, a viewpoint dimension instead of a client dimension, and no "risk" field.

**What the field shows about validity**
- Secrecy is the common failure. Hamilton's and Cyabra's lists could not be checked until outsiders did so, and the reputational damage came from that. A published selection method is thus a validity feature as well as an ethics feature.
- Graphika's "attentive cluster" treats clusters as patterns of attention, not belief. That matches the project's own decision that follows are attention (B4 design update) and suggests showing attention and belief as separate layers.
- Business fragility matters. Logically fell when platform contracts vanished, and Zignal moved from PR to defense. Who pays determines what the map becomes.

### Gaps
- Could not verify in this session: Brandwatch, Meltwater, Dataminr, DFRLab, EIP report methods, Alethea's real product. "Recorded Future Intelligence Graph" is unconfirmed.
- Actual reading keys from published Graphika reports (for example Spamouflage) were not retrieved.
- No independent accuracy benchmark across vendors was found.
- Media Cloud's older Topic Mapper and attention views are not described on the current homepage.

## 3. How researchers define narrative computationally

### Takeaway
"Narrative" has at least four computational meanings: a repeated claim, a labelled theme, an agent-action-patient structure, and an actant network or event sequence. Commercial tools mostly use the first and call it narrative. Dialogos should say which one it means, since its propositions are claims, and its cluster stories would need the third or fourth.

### Cited Findings
- **No settled definition.** Piper, So and Bamman (EMNLP 2021): "there is no consensus" on a minimal definition, and narrativity is scalar rather than binary. Their minimal model lists teller, mode of telling, recipient, situation, agent, sequential actions, potential object, spatial location, temporal specification and rationale. (The text says "eight features" though its letters run A to J.) — [Paper](https://par.nsf.gov/servlets/purl/10342552); [ACL](https://aclanthology.org/2021.emnlp-main.26).
- **Agent-verb-patient (relatio).** Ash, Gauthier and Widmer (Political Analysis 2024) start from semantic role labeling ("who is doing what to whom"), cluster entities, produce narrative statements, and combine them in a directed multigraph. Applied to the US Congressional Record — [arXiv](https://arxiv.org/pdf/2108.01720v3.pdf); [EconPapers](https://econpapers.repec.org/RePEc:cup:polals:v:32:y:2024:i:1:p:115-132_8).
- **Actant networks.** Tangherlini, Shahsavari et al. (PLOS ONE 2020) use a Greimas-based generative model: nodes are actants, with context-specific relationships in supernodes and subnodes. Pizzagate's framework links otherwise separate domains via "hidden knowledge", whereas Bridgegate stays in one domain; they predict conspiracy-theory frameworks stabilize quickly while real conspiracies develop slowly — [arXiv](https://arxiv.org/pdf/2008.09961).
- **Event sequences.** Norambuena et al. (ACM Computing Surveys 2023) screened 900+ articles to 54. A timeline of events is the most common representation; event graphs are the richer form — [ar5iv](https://ar5iv.labs.arxiv.org/html/2302.08351).
- **Extraction pipeline survey.** Santana et al. (AI Review 2023) organize work by pipeline task and stress how hard annotation is — [Springer](https://link.springer.com/doi/10.1007/s10462-022-10338-7).
- **Fixed taxonomy (SemEval-2025 Task 10).** Multi-label classification into hierarchical narratives and sub-narratives for Ukraine-Russia and climate. Participant papers give conflicting counts: 11 narratives and 38 sub-narratives, and 10 and 36, for the two domains in [one paper](https://preview.aclanthology.org/corrections-2025-08/2025.semeval-1.59.pdf); another describes 10 main and 46 sub. A narrative-explanation subtask reports best F1-macro 0.75040, with one team at 0.72464 — [team paper](https://preview.aclanthology.org/transition-to-people-yaml/2025.semeval-1.9.pdf).
- **LLM era.** Schmidt et al. (2025) compared GPT-4o to expert annotation: valid structured narratives, but below experts on complex documents — [EconPapers](https://econpapers.repec.org/paper/arxpapers/2506.15041.htm). A 2026 paper steers narrative path extraction toward a chosen agenda and reports that this does not produce unsupported narratives — [arXiv 2603.29661](https://arxiv.org/abs/2603.29661).
- **RAND.** The 2018 Eastern Europe report uses resonance analysis and a lexical appendix — [DTIC](https://apps.dtic.mil/sti/pdfs/AD1086152.pdf) (table of contents seen, methods not read). A later RAND experiment reportedly found source labeling and media-literacy advisories reduced propaganda's effect — [publisher listing](https://www.bookwire.com/book/USA/Russian-Propaganda-Hits-Its-Mark-9781977405944-Helmus-Todd-C-77769629).
- **Vendor contrast.** Blackbird's "any assertion" definition has none of Piper's structure — [glossary](https://blackbird.ai/glossary-of-terms/).

### Inferences
- By Piper's scale, most commercial "narratives" are low-narrativity claim clusters. Calling them narratives lends them a coherence and intent they may not have.
- Suggested ladder for SEE: proposition (quote-anchored claim) → statement (agent-action-patient) → storyline (sequence with time) → framework (actant network). Each rung is labelled, so the UI does not imply more structure than was extracted.
- Tangherlini's stability finding is a possible cluster-health signal, but it would need validating and carries a labelling hazard if it is ever presented as a "conspiracy detector".
- Agenda-steered extraction shows that a pipeline can be tilted while staying well supported, because selection is where bias enters. Quote checks alone do not catch it, so selection must be audited too.

### Gaps
- **"Sobre" and "NarrativeNLP"** could not be identified as named authors or projects; search budget ended first. Please confirm the intended references.
- Official SemEval overview (Piskorski et al.) and Subtask 2 leaderboard not retrieved.
- A published critique of "narrative" as an inflated term in disinformation studies was sought but not found. Hanley and Durumeric's tracking work was not found either.
- Later Tangherlini and Shahsavari papers not reviewed.

## 4. Joan Donovan and critical internet studies: what a map should adopt

### Takeaway
Donovan's central contribution is treating manipulation as a campaign with a life cycle moving through a whole sociotechnical system, including how journalists, platforms and researchers respond. Her work is qualitative and case-based, and it treats the observer as part of the system. A map should adopt that: track time, responses and its own amplification.

### Cited Findings
- **Life cycle stages:** (1) "Manipulation campaign planning and origins"; (2) "Seeding the campaign across social platforms and web"; (3) "Responses by industry, activists, politicians, and journalists"; (4) "Mitigation"; (5) "Adjustments by manipulators to new environment" — [Casebook methods](https://mediamanipulation.org/methods).
- The Casebook "combines social science and data science", sits in Critical Internet Studies, and names investigative digital ethnography. It was active 2019–2023 and is archived. Cases are chosen on novelty, scale and evidence, so it does not claim to be comprehensive; findings are triangulated — [Casebook methods](https://mediamanipulation.org/methods).
- Donovan's handbook chapter: campaigns are rarely found in stage order, so start wherever you see action and "trace the campaign backward and forward". Artifact intent may be unclear while distribution reveals tactics such as hiding identity, editing, or faked coordination. Manipulators "trade up the chain" to established outlets. Debunking has sometimes amplified campaigns. "Every perceived ending" may be a new beginning — [Verification Handbook](https://datajournalism.com/read/handbook/verification-3/investigating-disinformation-and-media-manipulation/the-lifecycle-of-media-manipulation).
- Stage 3 notes that outside reaction often determines whether a campaign gains traction — [Casebook methods](https://mediamanipulation.org/methods).
- Current position: assistant professor at Boston University since 2023, founder of the nonprofit Critical Internet Studies Institute (2024 per one bio), co-author of *Meme Wars* with Emily Dreyfuss and Brian Friedberg — [Whistleblower Aid bio](https://whistlebloweraid.org/wba-team-member/dr-joan-donovan/); [Chautauqua Daily](https://chqdaily.com/2025/07/joan-donovan-scholar-of-media-memes-untangles-internets-political-influence/); [Wikipedia](https://en.wikipedia.org/wiki/Joan_Donovan).
- Camille François's ABC framing separates manipulative Actors, deceptive Behavior and harmful Content, noting a benign message can still be spread deceptively; it was later extended with Degree and Effect — [Democracy Digest](https://www.demdigest.org/?p=53076); [ABCDE reference in arXiv 2301.04246](https://arxiv.org/pdf/2301.04246).

### Inferences (methods to adopt)
1. **Case files, not only clusters.** For each contested idea, keep a dated record of origin, seeding, responses, mitigation and adaptation.
2. **Trace in both directions** from any entry point. The "timestamped propositions and cluster lineages" already decided fit this.
3. **Treat the map as an actor at stage 3.** Log when the map's own publication changes what it measures, and watch for "trade up the chain" attempts to get onto the map.
4. **Keep a qualitative check.** Pair computational clusters with human ethnographic reading of a sample. Do not let the graph stand alone.
5. **Separate A, B and C.** Dialogos is about what clusters believe, not who is deceptive. It should not import behavior judgments into worldview labels.
6. **Publish selection criteria** as the Casebook does, and state non-comprehensiveness on the map.
7. Note a tension: Donovan's frame studies manipulation, whereas Dialogos studies sincere worldviews. Using a manipulation lens on sincere groups would itself be a harm.

### Gaps
- joandonovan.org returned 403, so her site was not read directly. Her site's current projects are unknown.
- *Meme Wars* was not read, and its specific methods are not cited here. The investigative digital ethnography primer and Casebook code book were not retrieved.

## 5. Lineage: Bernays to cognitive warfare

### Takeaway
The through-line is a shift from persuading publics to measuring and segmenting them, then to framing the mind as terrain. Evidence for the power of targeted persuasion is much weaker than vendors and critics both imply, but the belief in that power has itself had effects.

### Cited Findings
- **Bernays (1928):** "The conscious and intelligent manipulation of the organized habits and opinions of the masses"; "an invisible government which is the true ruling power of our country"; propaganda is "a consistent, enduring effort to create or shape events to influence the relations of the public" — [Propaganda, Gutenberg](https://www.gutenberg.org/ebooks/78634).
- **Lippmann vs. Bernays:** *Public Opinion* (1922) is the source of "pseudo-environments" and stereotypes (secondary summary) — [Audible listing](https://origin-www.audible.com/pd/Propaganda-Audiobook/B0DVN47XB6). One source says Lippmann shaped Bernays, who still argued the public is not "an amorphous mass" — [Wikipedia](https://en.wikipedia.org/wiki/Propaganda_(book)).
- **Lasswell:** *Propaganda in the World War* (1927) noted as a contemporary study — [Sánchez](https://papers.uab.cat/article/download/v91-sanchez/pdf-es).
- **Ellul:** treats propaganda sociologically, as "the air we breathe" in technological society — [McKenna essay](https://rbnmckenna86.substack.com/p/two-ways-of-thinking-about-propaganda) (secondary).
- **Psychographics:** Matz et al. (PNAS 2017) tested personality-matched Facebook ads on 3.5M+ people and found effects on clicks and purchases — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5715760). A search summary attributes to Matz the remark that this will not "suddenly turn a Hillary voter into a Trump voter"; the exact outlet was not confirmed, so check before quoting — [likely source, Vice](https://www.vice.com/en/article/this-is-how-much-marketers-know-about-you-based-on-one-facebook-like).
- **Cambridge Analytica:** experts told NBC the approach was neither novel nor measurably effective — [NBC](https://www.nbcnews.com/politics/politics-news/cambridge-analytica-s-effectiveness-called-question-despite-alleged-facebook-data-n858256); evidence for persuasion is thin — [The Conversation](https://theconversation.com/cambridge-analyticas-secret-psychographic-tool-is-a-ghost-from-the-past-94143). The FTC still found deception — [B5 source, FTC opinion](https://www.ftc.gov/system/files/documents/cases/d09389_comm_final_opinionpublic.pdf).
- **Military memetics:** Maj. Michael Prosser's 2006 Marine Corps study proposed a Meme Warfare Center; DARPA reportedly funded a "Military Memetics" study about five years later — [Vice](https://www.vice.com/en_us/article/xyvwdk/meme-warfare). Giesea, "It's time to embrace memetic warfare", NATO *Defence Strategic Communications* 1 (March 2016) — [StratCom COE](https://stratcomcoe.org/publications/its-time-to-embrace-memetic-warfare/164). DARPA SMISC built "a new science of social networks", tracked "cultural narratives", and ran closed experiments with 2,000–5,000 consenting participants; its page does not mention memes — [DARPA](https://www.darpa.mil/research/programs/social-media-in-strategic-communication).
- **Cognitive warfare:** NATO ACT's concept is the most developed; Deppe and Schaal flag vague definitions and conceptual stretching — [Frontiers in Big Data](https://www.frontiersin.org/articles/10.3389/fdata.2024.1452129/full). A 2026 European Journal of International Security article argues the concept lacks analytical utility — [Cambridge](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2D1C2A97BDA7BF09F9FFCC7238A82709).
- **Effect evidence:** Eady et al. (Nature Communications 2023) found no meaningful link between exposure to Russia's 2016 Twitter campaign and attitudes, polarization or voting; 1% of users took 70% of exposures; the authors suggest the biggest effect may have been convincing Americans it worked — [DOAJ record](https://doaj.org/article/ae23fc2e267d4fe7beeeb88109b0b65a); [phys.org](https://phys.org/news/2023-01-exposure-russian-twitter-campaigns-presidential.pdf).
- **Forward threat:** Schroeder et al. (Science, January 2026) warn of coordinated AI persona swarms that infiltrate communities and fabricate consensus; full-scale swarms are still largely hypothetical — [BI Norwegian Business School](https://www.bi.no/en/about-bi/news/2026/01/ai-swarms-threaten-democracy/); [UBC](https://science.ubc.ca/news/2026-01/ai-swarms-could-hijack-democracy-without-anyone-noticing).

### Inferences
- Dialogos sits in Lippmann's problem more than Bernays's: it tries to repair the pseudo-environment each group holds of the other. But the same instrument is exactly what Bernays's successors would buy.
- The inflated belief in persuasion is a double risk: buyers may use a map to justify suppression, and the public may fear it beyond what is warranted. Public language should be modest.
- A sourced, single-paragraph history is enough. "Memetic" carries military baggage (Prosser, Giesea). Benjamin should choose public vocabulary with that in mind.

### Gaps
- **No RAND report on memetics was found.** The likely referents are Prosser (Marine Corps) and the DARPA study. Finkelstein's "Info-PIP" definition appears only in a low-quality source (Grokipedia-class), so its venue is unconfirmed.
- Lasswell's "who says what" and Ellul's sociological or pre-propaganda categories need primary citation. They could not be checked before the search limit.

## 6. Unintended consequences and safeguards

### Takeaway
A public worldview map is a targeting list, a stereotype generator and a legal and political target all at once. Precedents show harm comes less from one bad output than from secrecy, score-like labels, naming individuals, contact with state enforcement, and the costs of defending the work. Safeguards exist, but most were designed for other domains and would need adapting.

### Cited Findings

**Misuse for targeting and persuasion**
- Same map, different buyer: Graphika sells "targeting and segmentation" and manipulation detection from one product family — [Graphika](https://graphika.com/use-cases/audience-and-influence-mapping). NATO StratCom treats audience segmentation as a psychological-operations input — [StratCom PDF](https://stratcomcoe.org/publications/download/AI-in-Support-of-StratCom-Capabilities-DIGITAL.pdf). GoLaxy's documents show profiling of thought leaders alongside a distribution system — [Nextgov](https://www.nextgov.com/cybersecurity/2025/08/researchers-detail-new-gray-zone-conflict-ai-driven-chinese-propaganda/407358/).
- Commercial-to-state drift: Zignal went from PR and campaigns to a $5.7M ICE contract for Homeland Security Investigations, with ACLU and Just Futures Law objections; EFF and Yale attorneys argue AI surveillance tools "exacerbate the chilling impact" — [The Lever](https://www.levernews.com/ice-just-bought-a-social-media-surveillance-botice-just-bought-a-social-media-surveillance-bot/). Reported alongside ShadowDragon and Babel X — [Jacobin](https://jacobin.com/2025/10/ice-zignal-surveillance-social-media).
- Lowered cost: CounterCloud's roughly $400 claim, and swarm warnings above, mean a good cluster map plus LLMs is an attack kit — [The Debrief](https://thedebrief.org/countercloud-ai-disinformation/).

**Labelling errors**
- Botometer scores were imprecise, especially outside English, and most studies likely count many humans as bots and vice versa — [Rauchfleisch & Kaiser, PLOS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC7580919).
- Real Norwegians were labelled fake by Cyabra's method, unrebutted — [Faktisk.no](https://www.faktisk.no/artikkel/israeli-ai-firm-claims-fake-profiles-targeted-norwegian-pm-investigation-finds-several-were-real/127272).
- Blackbird's cohort of "politically leaning activists, existing customers" shows lawful critics in a threat frame — [case study](https://blackbird.ai/case-studies/food-beverage/).

**Reification and performative effects**
- Franke draws on Hacking to argue that classifying people into political categories can solidify political identity by eliciting conformist responses, while personalization can also produce looping effects that sometimes reduce polarization — [PhilArchive](https://philarchive.org/archive/UWEAPB).
- Fixed identity categories in ML immobilize existing categories for lack of iterative feedback — [arXiv 2205.13740](https://ar5iv.labs.arxiv.org/html/2205.13740).
- Bail et al. (2018), cited in B4: exposure to opposing bots made Republicans more conservative — [Nieman Lab](https://www.niemanlab.org/2018/08/republicans-who-follow-liberal-twitter-bots-actually-become-more-conservative/).

**The Hamilton lesson**
- A hidden list, a "Russian bots" shorthand, and press uptake together produced a reputational failure and a lasting political weapon — sources in Section 2. ASD's "the media misused it" defense did not protect it.

**Murthy, SIO and the legal fight**
- *Murthy v. Missouri* (26 June 2024): plaintiffs lacked standing, having not shown a substantial risk of future injury traceable to the government defendants. The Court noted that a private entity, the Election Integrity Partnership, not CISA, alerted Twitter to a Gateway Pundit article, and that the evidence did not trace Hoft's injuries to the FBI or CISA — [Opinion](https://www.supremecourt.gov/opinions/23pdf/23-411_3dq3.pdf). It did not resolve the merits; one Wikipedia framing of it as a win for SIO overstates it — [SCOTUSblog](https://www.scotusblog.com/cases/murthy-v-missouri-3/).
- SIO: leaders left in June 2024, reports described dismantling, and Stanford denied closing "as a result of outside pressure", citing funding — [Wikipedia](https://en.wikipedia.org/wiki/Stanford_Internet_Observatory); [NYU Stern](https://bhr.stern.nyu.edu/quick-take/the-destruction-of-a-research-group-at-stanford-marks-a-dangerous-partisan-victory/). House Judiciary demands reached Stanford, Washington, Clemson and GMF — [ProPublica](https://www.propublica.org/article/jim-jordan-information-requests-universities-disinformation); FIRE called on the committee to withdraw — [FIRE](https://www.fire.org/news/statement-congressional-letters-and-subpoenas-researchers-studying-misinformation).
- *Hines v. Stamos*: dismissed 1 July 2026 for lack of standing and jurisdiction, after jurisdictional discovery, per defendant Renée DiResta, who quotes the opinion on "the absence of any factual basis". She reports three years of cost and says "the process is the punishment". This is an interested party's account — [DiResta](https://www.reneediresta.com/happy-july-4-we-beat-stephen-miller-in-court/). Earlier: Doughty denied dismissal in Dec 2024 — [Volokh](https://reason.com/volokh/2024/12/18/first-amendment-censorship-claims-against-stanford-internet-observatory-can-go-forward-to-discovery-as-to-jurisdiction-and-standing/).

**Labelling public figures and outlets**
- SPLC paid $3.375M and apologized to Maajid Nawaz and Quilliam after listing them in a "Field Guide to Anti-Muslim Extremists", and had to keep apologies up for two years; reports said about 60 groups considered action — [Religion Clause](https://religionclause.blogspot.com/2018/06/splc-pays-3375m-for-wrongful-inclusion.html); [Washington Times](https://m.washingtontimes.com/news/2018/jun/18/southern-poverty-pays-33m-quilliam-nawaz-labeling-/).
- Ratings attract government pressure and suits: Daily Wire, The Federalist and Texas sued the State Department over funding of GDI and NewsGuard (First Amendment and statutory claims, not defamation) — [Complaint-related coverage](https://www.dailywire.com/news/daily-wire-texas-ag-ask-court-to-block-state-departments-domestic-misinformation-efforts). GDI sued the FTC, and FTC civil investigative demands to NewsGuard and GDI were withdrawn on 17 and 21 April 2026, per a filing — [Court filing](https://storage.courtlistener.com/recap/gov.uscourts.txed.226532/gov.uscourts.txed.226532.75.0.pdf); [FTC–Media Matters settlement note](https://webiis10.mondaq.com/unitedstates/antitrust-eu-competition/1789998/ftc-settles-with-watchdog-journalism-non-profit-media-matters-for-america).
- GDPR and X inference limits remain as described in `docs/research/B5-platform-data-ethics.md`.

**Safeguards found in practice**
- Attention to false positives and threshold-sensitivity reporting — [Rauchfleisch & Kaiser](https://pmc.ncbi.nlm.nih.gov/articles/PMC7580919).
- Public account list (Hamilton 2.0) — [Wikipedia](https://en.wikipedia.org/wiki/Hamilton_68).
- Published case-selection criteria, triangulation — [Casebook](https://mediamanipulation.org/methods).
- Human verification with per-instance URLs and excerpts — [NewsGuard](https://www.newsguardtech.com/solutions/misinformation-fingerprints/).
- Avoiding binary true/false labels (Compass claims this; it then adds a risk grade) — [Compass blog](https://blackbird.ai/blog/compass-by-blackbird-ai-help-organizations-fight-narrative-attacks).
- Sensemaking-only scope: INCAS explicitly focused on sensemaking, not countering — [Proposers' Day slides](https://www.darpa.mil/attachments/INCASProp%20DaySlides2020-10-30a.pdf).
- Quantified confidence as a design requirement — [DARPA INCAS](https://www.darpa.mil/research/programs/influence-campaign-awareness-and-sensemaking).

### Inferences

**What to borrow vs. refuse (for the SEE visualization)**

| Borrow | Change | Refuse |
|---|---|---|
| Hub-and-audience map, zoom from cluster to source | Add legend, scale, method link, date, confidence; show attention and belief separately | Unlabelled spectacle |
| Assertion + stance objects with variants | Already quote-anchored; add dispute link | Risk as the organizing field |
| Ranked feed with summary | Rank by usefulness for understanding, for example biggest misperception between two clusters | "Top attacks targeting me" framing |
| Scorecard | Flip to a fidelity card: would the described side sign this? cross-cluster endorsement, disputes, confidence | Gauges and red alarm colors; single composite scores for people |
| Actor / content / behavior pivot | Keep content and cluster lenses | "Target subject" lookups of individuals; any behavior judgment on landmarks |
| Time-series lineage | Tie to life-cycle stages | Real-time "threat" alerts |

**Proposed safeguards to add** (on top of the rules in `CLAUDE.md`, and B5's red lines)
1. **Language rule:** clusters are "described", never "detected". No words such as threat, attack, risk, bot, extremist, or conspiracy on the public map.
2. **No client view.** Nobody can load "my brand" or "my opponent" as the map's centre. This is the strongest structural difference from the field.
3. **Fuzzy membership.** Show soft, multi-cluster, per-topic positions and a "last updated" date, to limit reification.
4. **Described-side sign-off** before a cluster description goes public. This turns the project's success metric into a publication gate.
5. **Publish the landmark list, selection method and model versions.** Hamilton shows a hidden list becomes the story.
6. **No bulk export of person-to-cluster,** rate-limited API, and a stated ban on campaign, law-enforcement and vetting use, backed by license terms and a governance body that a buyer cannot simply override. This is especially needed given the Zignal drift. Treat acquisition as a threat, since a purpose-trust structure may matter here.
7. **Adversarial red team before launch:** try to use the map to build a persuasion campaign and a harassment list, then publish what was learned.
8. **Measure the map's own effects:** track whether seeing it raises or lowers out-group perception gaps, and be ready to pull features. Bail et al. show exposure can backfire.
9. **Legal posture:** describe views with linked quotes; avoid factual-sounding accusations; keep a fast correction path, and get counsel and possibly media-liability insurance before public launch. SIO's experience suggests budgeting for defense even when one wins. Benjamin should decide on this before any public launch, since it has real cost and CLAUDE.md requires approval for paid services.
10. **Keep government and platforms at arm's length:** no flagging of content to platforms or agencies. *Murthy* records EIP alerting Twitter to a specific article, and flagging of this kind was central to the "censorship" allegations (my reading; EIP's own process was not reviewed).

### Gaps
- **Not verifiable before the search limit:** the December 2025 State Department visa actions against disinformation researchers; *Milkovich* and the opinion-vs-fact doctrine (the Justia page returned 403); *Coral Ridge v. SPLC* on "hate group" labels; chilling-effect studies such as Stoycheff and Penney; Whitney Phillips's *The Oxygen of Amplification*; Hacking's own texts; More in Common's perception-gap work; and EIP's *The Long Fuse*. These are all worth checking, and none should be cited from this note.
- No study was found that directly measures harm from a public worldview map. Reification effects here are argued by analogy from philosophy and adjacent experiments.
- *Hines* dismissal date and any appeal should be checked on the W.D. La. docket (No. 3:23-cv-571). Status of the Daily Wire case and the FTC dispute is also unconfirmed.
- This is research, not legal advice. Defamation exposure for AI-generated descriptions of public figures needs counsel.
- The Washington Post corrections and several Hamilton details come from partisan or secondary outlets. ASD's fact sheet page was down (HTTP 522) and was not read.
