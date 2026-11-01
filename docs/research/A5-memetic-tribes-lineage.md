# A5 — The memetic-tribes lineage and Kevin Owocki's visualizer

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Superseded: "Belonging = social graph" as Layer 1** (community detection on endorsement edges, Barberá ideal points). The follow graph measures **attention, not belief**, and is demoted to an optional attention overlay; the terrain is built from **landmark content**, with edges from quotes, appearances and named arguments (SYNTHESIS §2 D10, D14; §6.1).
> - **Modified: the 9-slot Limberg–Barnes schema and the 33 tribes.** Still the cluster-card schema; the tribes are now also one of three **seed sources for the ~500-landmark list** (2–3 landmarks per niche), alongside Kevin Owocki's 58 ontologies and Benjamin's brainstorm (§2 D12).
> - **Superseded: Kevin's "Venn first" view and the feed-share membership score ("your feed is 34% A").** The entry view is the first-sixty-seconds flow: react → dot on existing terrain → three nearest landmarks → threshold reveal → twist card → invitation to describe the farthest cluster (§2 D18; SYNTHESIS §6.4).
> - **Superseded: X archive / Bluesky as fallbacks for Layer 1.** X is no longer the front door; X archive is optional enrichment and Bluesky is one channel (§2 D11, D14).
> - **Modified: "opt-in for anyone shown by name".** Public figures may be placed from their public output with a dispute / annotate affordance; private individuals remain opt-in only (SYNTHESIS §11.2 red line 1).
> - **Kept:** Limberg's "post-meta" warning now drives the decision that **threshold people are protagonists** and every view invites encounter (§2 D8). Kevin's daily "Attention Times" is the model for the daily pulse (SYNTHESIS §6.6).

Brief for Dialogos Arena (author of record: Benjamin Life). Wave 0, task A5. Prepared 2026-10-30.

## Summary (≤200 words)

The lineage Benjamin pointed to is mostly real, but some names and credits in his account are mixed up. **"Peter Lindenberger" is Peter N. Limberg**, founder of The Stoa (opened 2020-03-21). His Substack and Medium bylines read "Peter Limberger", which probably explains the mix-up. **Limberg & Conor Barnes**, not Joe Lightfoot, wrote "The Memetic Tribes of Culture War 2.0" (Medium, Sept 2018). Its spreadsheet profiles **33 tribes on 9 qualitative dimensions**: Telos, Sacred Values, Master Status, Existential Threats, Combatants, Campfire, Chieftains, Mental Models, Forebears. The tribes were chosen by expert judgement; no data or clustering was used. **Joe Lightfoot** wrote "The Liminal Web" (2021, updated 2023), an informal essay on sensemakers, meta-theorists and systems poets, which is a *scene* rather than a tribe. Lightfoot did not write on "memetic tribes". Kevin Owocki shared **daily-ontological-map.vercel.app** with Benjamin on 2026-07-28, but I could not open it, so whether it is the "memetic tribes on Twitter" visualizer is **UNVERIFIED**. Neither vault holds a repo, method or data source for a Twitter tribe-clustering tool. The academic precedents (Barberá ideal points, Conover retweet networks) and survey precedents (Hidden Tribes, Pew) together show what a tribe is in practice. Belonging comes from the social graph. Identity comes from a memeplex profile. Survey-style values give the deeper drivers.

## Findings

### 1. Name check: "Peter Lindenberger" is Peter N. Limberg
- The Stoa was founded on 2020-03-21 as a series of Zoom salons and has more than 700 recorded sessions. Its public phase ended 2023-06-28. Jordan Hall, whom Limberg calls the "sensemaking general", led the first session. Limberg calls The Stoa an art project or personal practice rather than a movement. (Less Foolish, "How not to build a Stoa")
- His Substack is *Less Foolish*. The byline reads "Peter Limberger" and the footer reads "© Peter N Limberg". Benjamin's vault holds a forwarded Less Foolish post, "We are post-meta now" (2026-09-07). In it Limberg criticises the "stanceless stance", meaning meta-commentary used as a status game. This bears directly on the SEE layer: a mapping tool can itself become a meta-status toy. (Parachute: `vault/messages/email/fwd-we-are-post-meta-now-72396552`)
- Limberg's later threads include memetic mediation (posts from Nov 2020 onward; paywalled), "intimacy without friendship", and "The Meta-Crisis of the Meta-Crisis". I could not reach an essay titled exactly **"Intimacy Crisis"**: **UNVERIFIED**. The term "memetic mediator" circulated around The Stoa and the Intellectual Explorers Club; Jason Snyder's podcast "Rise of the Memetic Mediators" is from about 2019–2020. The text I could reach does not show who coined the term: **UNVERIFIED**. I found no Stoa source for "conversational hygiene": **UNVERIFIED as a Stoa term**.

### 2. "The Memetic Tribes of Culture War 2.0": the primary source
- **Authors and date:** Peter Limberg & Conor Barnes, Medium (World Wide WTF), 2018-09-14. The essay was paired with a public Google Sheet.
- **Definition:** a memetic tribe is a group of agents who share a meme complex (memeplex) and try to impose its map of reality and its moral imperatives on others. Two features matter: a *shared memeplex* and a *proselytising stance*. The authors frame the 2018 landscape as "Culture War 2.0", in which many tribes fight each other, as opposed to the older red-vs-blue two-tribe model.
- **The spreadsheet** (verified headers): MEMETIC TRIBE · TELOS · SACRED VALUES · MASTER STATUS · EXISTENTIAL THREATS · COMBATANTS · CAMPFIRE · CHIEFTAINS · MENTAL MODELS · FOREBEARS.
  - Telos is the end goal. For example, Tea Party: reduce debt and spending. SJAs: end social oppression.
  - Sacred Values are what the tribe will not trade off.
  - Master Status is the identity a member leads with. For example, "Patriot" or "Social Activist".
  - Existential Threats are what endangers the telos. For example, "Kyriarchy" or "Debt crisis".
  - Combatants are the opposing tribes. Together with Existential Threats, these are the *enemy* dimensions.
  - Campfire is where the tribe gathers (platforms and venues).
  - Chieftains are the leading figures.
  - Mental Models are the tribe's interpretive tools.
  - Forebears are its intellectual ancestors.
- **The 33 tribes:** SJAs, Black Lives Matter, #MeToo, Gender-Critical Feminists, Modern Neo-Marxists, Antifa, Occupy, Dirtbag Left, DSA, Establishment Left, Optimists, New Atheists, Street Epistemologists, Rationalist Diaspora, Post-Rationalists, Integral Theorists, Sorters, Intellectual Dark Web, Benedictines, Christian Right, Establishment Right, Tea Party, Trumpists, InfoWarriors, QAnoners, Alt-Lite, Alt-Right, Modern Neo-Nazis, Neoreactionaries, MRA, Manosphere, MGTOW, Incels.
- **Method:** qualitative and curated. No inclusion criteria are stated, and no network or quantitative method was used (Second Renaissance overview of mapping efforts). Some tribes are movements (BLM, Occupy), some are organisations (DSA), some are online scenes (Dirtbag Left), and some are intellectual "observer tribes" (Rationalist Diaspora). The unit of analysis is therefore inconsistent.
- **Later uses:**
  - OILab's "Political Space: Mapping Memetic Tribes" (Sal Hagen et al.) places tribes as planets on three unnamed axes. Planet size is the comment volume on related subreddits.
  - Brandon Nørgaard gave a Stoa talk and podcast, "Memetic Tribes of the Meta-Crisis".
  - Nørgaard's "Approaches to the Meta-Crisis" (2022) groups approaches by value-meme.

### 3. Joe Lightfoot: what he actually wrote
- "The Liminal Web: Mapping An Emergent Subculture Of Sensemakers, Meta-Theorists & Systems Poets" was posted on joelightfoot.org in Nov 2021 and updated in Apr 2023. He discussed it with Brendan Graham Dempsey on *Metamodern Meaning* ep. 17 (2021-12-30), with a focus on communitas.
- **Definition:** an international constellation with no hard edges. His working membership heuristic is that a person is in if roughly 30% of the intellectual media they consume comes from it. He calls it a memetic ecosystem and a "noospheric relay".
- **Method:** none. It is an informal essay, infographic and list. The pages I could reach for the Liminal Web essay do not mention memetic tribes, The Stoa or Limberg.
- **Correction for Benjamin:** "Joe Lightfoot's original writing on memetic tribes" conflates two works. The *memetic tribes* essay is Limberg & Barnes (2018). Lightfoot's piece is the Liminal Web (2021). Lightfoot's consumption-share heuristic is still useful as a feed-based membership test.
- **Ties to Benjamin (from his vault):**
  - Benjamin's podcast EP_01 was titled "The Liminal Web" and featured Joe (Parachute: `wiki/writing/the-liminal-web-ep_01`).
  - Joe messaged Benjamin on 2026-05-27 after lunch with Michel Bauwens (Parachute: `vault/messages/telegram/joe-lightfoot`). He is reachable for a conversation.

### 4. Sensemaking discourse (Schmachtenberger, Hall, Game B)
- Schmachtenberger's "The War on Sensemaking" (Rebel Wisdom, 2019, plus later parts) frames the problem as an information ecology degraded by narrative warfare and incentives. It is about epistemics and does not offer a tribe taxonomy.
- Life Itself's "Mapping Metamodern / State of Sensemaking" (2020) is a curated directory and graph of organisations, using the criteria paradigmatic, integrated and pragmatic.
- Kevin Owocki recorded a call with Schmachtenberger on 2026-05-21 (Gitcoin Brain: `meetings/2026-05-21_daniel-schmachtenberger-gitcoin/transcript`). I did not mine it.
- Relevance: these sources supply the *why* (we need sense across tribes) more than the *how* (method).

### 5. Kevin Owocki's visualizer: what I found
- **Lead:** on 2026-07-28 Kevin sent Benjamin https://daily-ontological-map.vercel.app/ with the note "ud enjoy this". Benjamin replied "Omg wow". (Parachute: `vault/messages/telegram/kevin-owocki`, around the 2026-07-28 entries.)
  - **I could not open the page.** WebFetch was blocked by a permission timeout, and the session's egress proxy refuses the host.
  - A web search for the app name returned nothing, and GitHub access to `owocki/*` is not enabled in this session.
  - **It is UNVERIFIED whether this is the "memetic tribes on Twitter" tool.** The name suggests a map of ontologies that updates daily, perhaps generated by an LLM from a news or X feed. It does not necessarily cluster accounts.
- **Related context in the same thread:**
  - **2026-07-04:** Benjamin shared Ontography maps. Kevin asked whether closeness in the graph means distance on some vector. He proposed overlaying Daniel Schmachtenberger, Nate Hagens and Greenpill/Gitcoin to see where they overlap or differ. He then forwarded outputs from his second-brain agent ("mirror mirror (owocki)"):
    - an ontology visualization of Nate Hagens
    - a **Venn-diagram** comparison
    - a linear problem→solution layout

    His design note: Ontography is "good at looking in high resolution" while Venns are easier at a glance, so start simple and let the user drill into the high-resolution view. This is direct design input for SEE: a progressive-disclosure view that moves from Venn to cluster to claim graph.
  - **2026-06-25:** Kevin used the coinage "ontologymog" and said the movement needs a meme as potent as the woke mind virus, but for localism and relationality.
  - **2026-07-09:** Kevin shared capital-allocation-heatmap.surge.sh, a separate heatmap prototype.
  - **2026-05-25:** Kevin "sync'd my twitter history to my external brain" and posted an LLM-written arc of his tweets from 2016 to 2026. This shows he has a pipeline from X archive to LLM, applied to *his own* timeline (Gitcoin Brain: `telegram/gitcoin-viral-content/2026-05-25`).
- **What I searched without finding a tool:**
  - Parachute: searches for "owocki" combined with tribes, memetic, visualizer, twitter graph, followers, cluster, map; queries limited to items since 2026-06; and the `owocki-ag-lucian-benjamin` thread.
  - Gitcoin Brain: "tribes", "memetic", "twitter map", "clusters", and a twitter+graph/follower/cluster/tribe/map search inside `kevin/`.
  - Web: "owocki memetic tribes twitter".
  - None of these returned a repo, method, data source or stack for a Twitter tribe-clustering visualizer. Semantic search is not configured on either vault.
- **Questions for Kevin:**
  1. Is daily-ontological-map.vercel.app the tribes visualizer, or is that a different artifact? Repo URL?
  2. Data source: X API follows, likes, RTs, or quotes? Your own archive export? Lists? Scraped timelines? How many accounts, and how were seeds chosen?
  3. Representation: graph community detection (Louvain/Leiden), embeddings of tweets or bios plus clustering (UMAP/HDBSCAN), or LLM-assigned labels?
  4. How were clusters named, and by whom or what? How did you validate them (did people recognise themselves)?
  5. Stack: Vercel/Next plus which visualization library? Is it refreshed daily (as "daily" implies), and how?
  6. Would you share data, code or the pipeline for a Dialogos SEE prototype?

### 6. Adjacent mapping precedents

| Precedent | Unit / data | Method | How it defines a group |
|---|---|---|---|
| More in Common, *Hidden Tribes of America* (2018) | Survey of more than 8,000 US adults, plus focus groups and interviews | Hierarchical clustering on core beliefs | 7 tribes: Progressive Activists 8%, Traditional Liberals 11%, Passive Liberals 15%, Politically Disengaged 26%, Moderates 15%, Traditional Conservatives 19%, Devoted Conservatives 6%. The four middle tribes form the "Exhausted Majority". Inputs: group identity, perceived threat, parenting style/authoritarianism, moral foundations, personal agency. |
| Pew Research Center, *Political Typology* (2021) | More than 10,000 American Trends Panel registered voters | Weighted k-medoids on 27 standardized value items plus party thermometers | 9 groups. Group names are from memory and UNVERIFIED: Faith & Flag Conservatives, Committed Conservatives, Populist Right, Ambivalent Right, Stressed Sideliners, Outsider Left, Democratic Mainstays, Establishment Liberals, Progressive Left. |
| Barberá, "Birds of the Same Feather Tweet Together" (*Political Analysis*, 2015) | X follow edges to elite accounts | Bayesian spatial-following (ideal-point) model | A continuous latent position, inferred from homophily in whom you follow. Validated against legislator ideology, users' stated preferences and party registration records. |
| Conover et al., "Political Polarization on Twitter" (ICWSM 2011) | Retweet and mention networks around 2010 US midterm hashtags | Community detection / label propagation | The retweet network is strongly partisan-segregated. The mention network is far more cross-cutting. Partly UNVERIFIED: the paper page was bot-blocked, and these details are from the abstract outline plus known results. |
| OILab, *Political Space* | Memetic-tribe list, with subreddit comment volume for planet size | Manual classification on 3 axes | Tribes taken from the Limberg & Barnes list, positioned by coders. |
| Life Itself (2020), Lightfoot (2021), Kowalski Meta-Crisis Meta-Resource (2022) | Curated organisations and people | Directory, Kumu graph, essay | Expert judgement only. |

## How this answers the governing question (layering + validation)

**What a tribe is in practice (for clustering):** a set of accounts that **(a) attend to and amplify one another** and **(b) share a recognisable memeplex profile**. The profile covers telos, sacred values, enemies and canon. The precedents divide these jobs as follows:

1. **Belonging = social graph.** Conover shows that endorsement-type edges (retweets, and probably follows and likes) sort people into groups, while conversation edges (mentions, and probably replies and quotes) cross between groups. Barberá shows that follows support ideal-point estimates that hold up under validation. **Layer 1:** community detection on endorsement edges, plus a continuous ideal-point or latent-space position. Treat quote and reply edges separately, as *contact* edges; these are the bridges SEE wants to highlight.
2. **Identity = memeplex profile.** The 9 Limberg/Barnes columns are a ready-made schema for **labelling** clusters after detection, not for finding them. **Layer 2:** an LLM or claims-extraction pass over a cluster's top posts fills in each slot (Telos, Sacred Values, Master Status, Existential Threats, Combatants, Campfire, Chieftains, Mental Models, Forebears). Each slot can then be mapped to an Ontography layer:
   - Mental Models and Forebears map to the epistemological layer.
   - Sacred Values and Telos map to axiological.
   - Existential Threats map to ontological.
   - Campfire, Combatants and Master Status map to the praxis/social layer.
3. **Drivers = values.** Hidden Tribes and Pew show that stable groups appear when you cluster on *deep* items: moral foundations, threat perception, authority, agency. **Layer 3, optional and opt-in:** a short questionnaire or inferred values profile. It explains *why* a cluster coheres, and it is also the layer where bridging is most likely, because the "Exhausted Majority" lies between the wings on these drivers.
4. **Scene vs tribe.** Lightfoot's Liminal Web is a *scene*: overlapping consumption with no shared enemy. Tribe-ness should be a measured property rather than assumed. Measure it by the share of **Combatants/Existential Threats** in a cluster's discourse, out-group hostility, and cross-cutting edges. Lightfoot's rule that a person belongs once about 30% of their media diet comes from the scene gives a simple **membership score** to show the user ("your feed is 34% cluster A, 21% B…").

**Avoiding overload:** follow Kevin's own suggestion. The default view is a Venn or overlap view of the user against 2–3 nearest clusters. The next level is the cluster map with bridges. The deepest level is the Ontography claim graph for any one cluster or person.

**Validation:**
- **Convergent:** graph communities and memeplex labels should agree. Test with mutual information between graph partitions and LLM-labelled stance clusters on a held-out sample.
- **External:** Barberá-style checks against known anchors such as self-declared affiliations and public org membership.
- **Recognition:** users and cluster "chieftains" rate whether the profile represents them. This is a steelman test: they should endorse the description as fair.
- **Stability:** clusters should persist across time slices and resampling (bootstrap ARI).
- **Predictive:** cluster membership should predict future engagement or quote-tweet direction better than topic embeddings alone. This guards against the "clusters by topic, not stance" risk.

## Reusable assets / design implications
- **The Limberg/Barnes 9-slot schema** (public sheet `docs.google.com/spreadsheets/d/11Ov1Y1xM-LCeYSSBYZ7yPXJah2ldgFX4oIlDtdd7-Qw`):
  - adopt it as the cluster-profile card;
  - use the 33 tribes as a 2018 seed and test set for labelling, noting they are US/Anglo and dated.
- **Hidden Tribes drivers** (moral foundations, threat, authority, agency, group identity) can be an optional "deep values" panel.
- **Edge typing:** endorsement edges (follow, RT, like) feed *belonging*. Contact edges (quote, reply, mention) feed *bridges and contact*.
- **Kevin's progressive-disclosure idea** (Venn first, high-resolution later) and his three-way overlay request (Schmachtenberger × Hagens × Greenpill) give a concrete first demo.
- **Limberg's "post-meta" warning** is a design constraint: the map should invite encounter (MEET), not spectator status. Pair every "where you sit" view with a "who across the gap to talk to" prompt.

## Risks & open questions
- **Not resolved:** whether daily-ontological-map.vercel.app is the visualizer. Someone must open it in a browser or ask Kevin (see the questions in §5).
- **Reification:** naming tribes can harden them. The 2018 list already mixes movements, organisations and scenes. Let clusters stay fuzzy (soft membership) and versioned.
- **Ethics:** clustering private individuals from X data raises profiling, doxxing and targeting risks. The tool should require opt-in for anyone shown by name. A related warning comes from Kevin's own 2026-05-06 message, which speaks of producing "memetic propaganda" week over week (Gitcoin Brain: `telegram/gitcoin-viral-content/2026-05-06`). The same map can serve propaganda as easily as dialogos, and governance should address this.
- **X API cost and access** constrain Layer 1. Fallbacks: user-uploaded archive exports (Kevin's 2026-05-25 pipeline shows this works for one person), Bluesky/AT Protocol (open graph), and lists.
- **Not verified:**
  - Limberg's "Intimacy Crisis" essay
  - the origin of "memetic mediator" and "conversational hygiene"
  - the exact names of Pew's nine groups
  - full Conover results

## Sources
- Limberg & Barnes, "The Memetic Tribes of Culture War 2.0" (2018): https://medium.com/s/world-wide-wtf/memetic-tribes-and-culture-war-2-0-14705c43f6bb ; summary: https://secondrenaissance.net/wiki/memetic-tribes ; spreadsheet: https://docs.google.com/spreadsheets/d/11Ov1Y1xM-LCeYSSBYZ7yPXJah2ldgFX4oIlDtdd7-Qw/edit ; PDF mirror (blocked, not read): https://seedsofrenaissance.org/assets/The.Memetic.Tribes.Of.Culture.War.2.0.pdf
- Second Renaissance, overview of mapping efforts: https://secondrenaissance.net/wiki/overview-mapping-efforts
- EA Forum discussion of Memetic Tribes: https://ea.greaterwrong.com/posts/pKgWQMjPki5bz7ehZ/memetic-tribes-and-culture-war-2-0-article-discussion
- Joe Lightfoot, The Liminal Web: https://stream.syscoi.com/2021/11/18/the-liminal-web-mapping-an-emergent-subculture-of-sensemakers-meta-theorists-systems-poets-joe-lightfoot ; https://secondrenaissance.net/wiki/liminal-web ; Dempsey interview: https://brendangrahamdempsey.substack.com/p/17-the-liminal-web-and-communitas-c93
- Limberg, "How not to build a Stoa": https://lessfoolish.substack.com/p/how-not-to-build-a-stoa-a-very-online ; "Memetic mediation during the liminal war": https://lessfoolish.substack.com/p/memetic-mediation-during-the-liminal ; "Alt accounts, insight roles and memetic mediation" (2020-11-13): https://lessfoolish.substack.com/p/alt-accounts-insight-roles-and-memetic ; Beiner/Kainos interview (2023-12-08): https://beiner.substack.com/p/why-scene-making-beats-sensemaking
- Jason Snyder, "Rise of the Memetic Mediators": https://wiki.p2pfoundation.net/Jason_Snyder_on_the_Rise_of_the_Memetic_Mediators
- Nørgaard, "Memetic Tribes of the Meta-Crisis": https://wiki.p2pfoundation.net/Brandon_N%C3%B8rgaard_on_the_Memetic_Tribes_of_the_Meta-Crisis
- OILab, Political Space: https://oilab.eu/political-space
- Schmachtenberger, "The War on Sensemaking": https://civilizationemerging.com/media/war-on-sensemaking-5/
- More in Common, Hidden Tribes: https://hiddentribes.us/ (report PDF: https://hiddentribes.us/media/qfpekz4g/hidden_tribes_report.pdf)
- Pew 2021 Political Typology, methodology: https://www.pewresearch.org/politics/2021/11/09/political-typology-appendix-b/ ; report: https://www.pewresearch.org/politics/2021/11/09/beyond-red-vs-blue-the-political-typology-2021/
- Barberá 2015: https://csmapnyu.org/research/academic-research/birds-of-the-same-feather-tweet-together-bayesian-ideal-point-estimation-using-twitter-data
- Conover et al. 2011: https://ojs.aaai.org/index.php/icwsm/article/view/14126
- Kevin Owocki's app (not reachable): https://daily-ontological-map.vercel.app/
- Parachute vault: `vault/messages/telegram/kevin-owocki` (2026-06-25, 07-04, 07-09, 07-28) · `vault/messages/telegram/joe-lightfoot` · `wiki/writing/the-liminal-web-ep_01` · `vault/messages/email/fwd-we-are-post-meta-now-72396552`
- Gitcoin Brain: `telegram/gitcoin-viral-content/2026-05-25` · `telegram/gitcoin-viral-content/2026-05-06` · `meetings/2026-05-21_daniel-schmachtenberger-gitcoin/transcript`

## Addendum (orchestrator, 2026-10-30): Kevin's visualizer identified

Fetched https://daily-ontological-map.vercel.app/ directly. It is **"Atlas of Frontier Ontologies"** by @owocki — a nightly-updated, cartographic map of **58 "ontologies" (belief systems / tribes on X)**. Each ontology is rendered as a continent or island; daily arguments are cities, top stories are mountains. Two organizing axes: **accelerate ↔ restrain** and **within institutions ↔ exit to build parallel systems**. Also published as a daily newspaper ("The Attention Times") ranking tribes by real-world size rather than feed volume, each described in its own voice. The page does not disclose its data collection or classification method — ask Kevin (questions in §5 above). Design note: this is a population-scale, tribe-level SEE layer with editorial framing, but no individual placement, no claim graph and no consent flow — which is exactly the gap Benjamin's layers fill.
