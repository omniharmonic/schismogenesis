# State of the art in visualizing a semantic, narrative or worldview landscape (late 2026)

Prepared for Dialogos Arena (owner: Benjamin Life). Date: 2026-11-01.

**How to read these notes.** Under each question, findings are split into **Tested** (a controlled study or measured result) and **Practice / opinion** (a project's design choice, a theoretical argument, or an author's stance). Everything under Inferences is mine and is design opinion unless stated otherwise.

**Limits of this research.**
- The session's web search budget ran out partway through. The temporal, uncertainty, critical cartography and layered-ontology sections therefore rest on direct fetches of known pages, and several of those are Wikipedia summaries rather than the original texts.
- Many academic findings come from abstracts or indexes, not full papers. Where that matters, the entry says so.
- Sources I could not reach are listed under Gaps. They are not cited from memory.

**Baseline already covered, not repeated here.** `docs/research/A1-ontography.md` sets the "no meaning in force distance" and "simple first, high resolution later" lessons. `A3-anti-debate-topology-live.md` sets the X = stance, Y = stratum, Z = time layout and the 0-5 detail dial. `B4-mapping-science.md` covers tooling and the five-layer SEE stack. This note goes further on evidence for and against specific forms.

**Atlas facts checked in the repo.** `apps/atlas/atlas.tpl.html` uses `3d-force-graph`, with `fy:HEIGHT[i.layer]` fixing height by layer and `ax:i.x, az:i.y` anchoring horizontal position. `packages/arena_map/src/arena_map/structure.py` imports `MDS` and `trustworthiness` from sklearn. I did not trace how the 54% figure is computed. See the first section's Gaps.

## Projection integrity: what is lost, which method, how to show the loss

### Takeaway
No projection of worldview data is honest on its own. The best current practice is to do the analysis in the full space, match the method to the task, and draw the loss on the map. For the Atlas, classical or metric MDS is the right family for reading distances between clusters. Moving to UMAP would improve cluster appearance and make distances between schools less trustworthy.

### Cited Findings

**Tested**
- In 2D t-SNE and UMAP, the 30 nearest neighbours overlapped poorly with the original space (average Jaccard distance above 0.7, so about 30% or less shared). Cluster-rank correlations were 0.4 or lower, and max/min distance ratios were 4- to 200-fold larger than in the original space. The authors recommend treating 2D embeddings as illustrations and using dendrograms, trees or network diagrams at cluster level — [Chari and Pachter, PLOS Comp Biol 2023](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011288).
- Counter-evidence: Lause, Berens and Kobak argue that conclusion rested on inadequate metrics. t-SNE and UMAP strongly beat 2D PCA and an arbitrary "elephant" embedding on kNN classification, silhouette and AMI measures. This came from an abstract and excerpts — [Lause et al., PLOS Comp Biol 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11446450). The two papers conflict on framing. The reading I find most defensible is that distances are not preserved, but class and neighbourhood information partly is.
- The supposed global-structure advantage of UMAP over t-SNE comes from initialization. With informative initialization both perform about equally, and random initialization should be avoided — [Kobak and Linderman preprint](https://www.biorxiv.org/content/10.1101/2019.12.19.877522v1.full).
- A review of 136 visual analytics papers found t-SNE in 75 and UMAP in 31, and 44% gave no justification for their DR choice. Suitable tasks for t-SNE/UMAP: neighbourhood, outlier and cluster identification. Unsuitable tasks, which belong to global methods such as PCA and MDS: point distance, class separability, cluster distance and cluster density. The authors attribute misuse to limited DR literacy and say earlier fixes failed. UMAP had the highest misuse-to-usage ratio among the four major techniques — [Jeon et al., accepted for IEEE VIS 2026 and TVCG](https://arxiv.org/html/2506.08725v2).
- The same review points to UMATO, TriMap, PaCMAP and Global t-SNE for better global structure, and den-SNE and densMAP for density — [Jeon et al.](https://arxiv.org/html/2506.08725v2).
- PaCMAP's analysis finds that most methods lose global structure because they omit forces on farther points, and TriMap's global strength comes largely from PCA initialization rather than its triplets. PaCMAP uses mid-near pairs early, then refines local structure. Benchmarks are the authors' own and were not checked — [Wang et al., JMLR 2021](https://jmlr.org/papers/v22/20-1061.html); summary via [AITopics](https://aitopics.org/doc/arxivorg:D3CA0188).
- Purely random data can produce convincing clumps, and cluster sizes and inter-cluster gaps in t-SNE may mean nothing — [Wattenberg et al., Distill](https://distill.pub/2016/misread-tsne/).
- densMAP uses local density estimates as a regularizer, so spread stays visible, at roughly double runtime in the documented examples. High `dens_lambda` values push outliers into a halo — [UMAP docs](https://umap-learn.readthedocs.io/en/latest/densmap_demo.html).
- Parametric UMAP trains a network for fast online embedding of new points and adjustable global structure, performing comparably to standard UMAP. The abstract does not establish inverse mapping — [Sainburg et al.](https://arxiv.org/abs/2009.12981).
- Aligned UMAP optimizes time slices jointly with a regularizer rather than running UMAP per slice and applying Procrustes, and supports appending new slices — [UMAP docs](https://umap-learn.readthedocs.io/en/latest/aligned_umap_basic_usage.html); [method description](https://www.biorxiv.org/content/10.1101/2022.12.12.518225.full.pdf).
- Trustworthiness asks whether points that look close really are close, and continuity asks whether true neighbours stayed close. Both range from 0 to 1 — [checkatlas metric notes](https://checkatlas.readthedocs.io/en/latest/metrics/dimred/trust_continuity/). This pair matters for reading: false neighbours and torn neighbours are different errors.
- ZADU provides 17 or more distortion measures with per-point contributions, and ZADUVis draws CheckViz and Reliability Maps — [ZADU paper](https://arxiv.org/pdf/2308.00282v2.pdf); [PyPI](https://pypi.org/project/zadu/0.0.7).
- Aupetit colours each point's Voronoi cell by a distortion measure, showing where a manifold was torn or glued. Keywords also include recovering topology through the Delaunay graph — [Neurocomputing 2007 listing](https://elmi.hbku.edu.qa/en/publications/visualizing-distortions-and-recovering-topology-in-continuous-pro/).
- Nonato and Aupetit survey distortion types, their effect on tasks, and "layout enrichment" schemes that debunk distortions or show what the scatterplot cannot — [TVCG 2019 listing](https://qcai.qcri.org/publications/multidimensional-projection-for-visual-analytics-linking-techniques-with-distortions-tasks-and-layout-enrichment).

**Topological and hyperbolic methods (mostly proof of concept)**
- Mapper builds a graph summary through filtering, covering and clustering. Its output depends on the lens, the cover resolution and overlap, and the clustering method — [Mapper on text embeddings, 2025](https://arxiv.org/pdf/2510.17548). It has been applied to [UK Commons debates with time as the filter](https://arxiv.org/pdf/1510.03797), [US House roll calls](https://arxiv.org/abs/1906.01726?context=cs), [voting and racial polarization](https://mggg.org/MapperVote) and the [Brexit vote via Ball Mapper](https://arxiv.org/pdf/1909.03490).
- Poincaré embeddings capture hierarchy and similarity compactly and can significantly outperform Euclidean embeddings on data with latent hierarchies — [Nickel and Kiela, NeurIPS 2017](https://arxiv.org/pdf/1705.08039). CO-SNE adapts t-SNE to hyperbolic data and preserves each point's distance to the origin, because hyperbolic space holds far more volume away from the origin — [Guo et al., CVPR 2022](https://arxiv.org/abs/2111.15037).

**Practice / opinion**
- Fair 2D representation of partially elicited attitudes is treated as an open problem in deliberation research — [Computational Challenges in Scaling Democratic Deliberation](https://arxiv.org/pdf/2605.01525).

### Inferences
- **Keep MDS, or at least a global method, for the horizontal plane.** The questions the Atlas invites ("how far is school A from school B?") are the tasks Jeon et al. reserve for global methods. The 54% figure is not by itself a reason to change method. It is a reason to stop implying the plane is the whole truth.
- **Show the 46% rather than hide it.** The strongest low-effort move is a "false neighbour" layer: select a thinker or idea, and redraw its true nearest neighbours in full space as links, so viewers can see which close pairs are artifacts of the projection. Colour Voronoi cells by per-point error (Aupetit, CheckViz) as a toggle.
- **Do cluster statistics in full dimension, never on the plane.** Report school membership, nearest school and overlap from the full-space computation.
- **Consider a tree alongside the map.** Chari and Pachter's fallback and hyperbolic methods both point to hierarchy as a more honest overview. A dendrogram of schools needs no projection at all.
- **Hyperbolic layout is not a first prototype.** Worldview layers are ordered, but I found no evidence that worldview data is tree-like, and no user study of a hyperbolic worldview map.

### Gaps
- Benjamin's figure of 54% over three axes: `structure.py` calls `MDS(2, ...)`, and `space.py` has a classical MDS function returning variance share. Height is fixed by layer, so it is not a third fitted axis. I did not establish which three axes produce 54%. Someone should confirm before that number appears publicly.
- Persistent homology on text: the search that was meant to cover it returned nothing on point. I found no evidence that it has produced a legible public visual.
- No study found that compares DR methods on worldview or proposition-stance data specifically.
- Etemadpour et al. found subjects prefer projections with good segregation, but only an abstract-level account was reached — [record](https://repositorio.usp.br/item/002499570).

## 3D vs 2D, force-directed graphs, and terrain

### Takeaway
On a flat screen, 3D rarely earns its cost for reading point layouts, and terrain performed worse than points for finding specific items. The evidence that favours 3D is narrow: immersive displays, or depth driven by motion and stereo. Terrain's real case is a different task, recalling and reasoning about the space itself, and that case was explicitly left open by the main study.

### Cited Findings

**Tested**
- Across 816 scatterplots from 75 datasets and 4 DR techniques, two coders found 2D usually sufficient. Interactive 3D seldom helped and often reduced separation and usability. Advice: if 2D fails, try another DR technique in 2D first. Abstract only — [Sedlmair, Munzner and Tory, InfoVis 2013](https://www.tableau.com/research/publications/empirical-guidance-scatterplot-and-dimension-reduction-technique-choices).
- For a search and point-estimation task, points beat landscapes and 2D landscapes beat 3D ones. Coloured points were fastest, and height-only 3D landscapes slowest. Adding colour on top of height gave little or no benefit. The authors limit the conclusion to tasks about the points themselves, "rather than derived information about the data space". Abstract and listings only — [Tory et al., TVCG 2007](https://manuscript.isc.ac/Inventory/49/964290.htm); [record](https://search.isc.ac/inventory/10/402132.htm).
- Spatial memory showed no significant difference between 2D and 3D computer interfaces, and physical card layouts beat both — [Cockburn and McKenzie, CHI 2002](https://courses.washington.edu/hcde511/a14/readings/cockburn-chi02.pdf). Perspective effects did not change spatial memory in monocular static displays — [Cockburn 2004](https://crpit.scem.westernsydney.edu.au/abstracts/CRPITV28Cockburn.html).
- Non-experts judged document similarity largely from metric distance along network links, not node counts or distance across links. Link width, value and hue also shift judgments — [Fabrikant et al., 2004 record](https://www.bohrium.com/paper-details/the-distance-similarity-metaphor-in-network-display-spatializations/812313131953946626-144).
- Viewers do read near as similar, but when Montello et al. wrote, empirical support in information displays was scarce — [Montello et al., COSIT 2003](https://user.geo.uzh.ch/sfabri/pubs/montello_etal_cosit03.pdf). Similarity ratings in 3D network displays were close to the earlier 2D results, and the authors weigh that against the added perceptual and technical cost — [Fabrikant, Maggi and Montello 2014](https://user.geo.uzh.ch/sfabri/pubs/fabs_etal_gisci14.pdf).
- The information landscape metaphor "is not self-evident to lay users, as the landscape designers had claimed". Deep geomorphology knowledge is probably not needed, but a coherent theory of how people use space is — [Fabrikant, Montello and Mark, JASIST 2010](https://www.zora.uzh.ch/entities/publication/327fbcdd-5bc3-4378-8c44-20e8a05f1518). Later work adds that a landscape needs to be geomorphologically plausible — [AutoCarto 2022 abstract](https://cartogis.org/docs/autocarto/2022/docs/abstracts/Session11_Moore_2360.pdf).
- Counter-evidence for immersion: 18 participants, within-subjects, compared a 2D scatterplot matrix, 3D on screen, a VR miniature and full VR. 2D did worse on the measured variables and the authors find higher immersion can substantially benefit cluster detection in 3D data. Abstract-level only, and this is a small study on data that is natively 3D — [Kraus et al., TVCG 2020](https://bib.dbvis.de/publications/view/823).
- A 2011 paper found 3D projections beat 2D on neighbourhood precision, and users benefited from better class separation, but noted bare 3D point clouds impair orientation and interaction — [CGF 2011](https://pub-0ba4292bf23b48ceaee7d83b310f091c.r2.dev/files/papers/2011-3DProjections-CGF.pdf). Conflict with Sedlmair et al.: computed precision and human perception are different measures.
- For 3D node-link graphs, stereo and kinetic depth matter while perspective, shading and occlusion matter less (secondary summary). Motion plus stereo substantially increases the graph size people can perceive — [Ware and Mitchell 2005 record](https://www.bohrium.com/paper-details/visualizing-graphs-in-three-dimensions/811938941451108353-2747); [Ware and Franck 1996](https://scholars.unh.edu/ccom/939). 3D can also make labels illegible — [Alper et al., InfoVis 2011](https://sites.cs.ucsb.edu/~holl/pubs/Alper-2011-Infovis.pdf). A 2025 eye-tracking study still reports depth, occlusion and perspective challenges — [Zhang et al., GD 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol357-gd2025/LIPIcs.GD.2025.11/LIPIcs.GD.2025.11.pdf).

**Practice / opinion**
- GMap draws clusters as countries and argues maps reveal cluster structure that point clouds and graph drawings hide. This is the authors' case-study claim — [Gansner, Hu and Kobourov](https://yifanhu.net/GMap/index.html). Later work fixes fragmented regions — [Kobourov et al., via project list](https://ulp.cs.arizona.edu/~kobourov/PROJECTS).
- Spatialization of science at scale: a SOM of 2M+ medical publications avoids computing similarity matrices — [Skupin, Biberstine and Börner, PLOS ONE 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3595294). Boyack et al. warn an inferior map can misallocate funding — [Mapping the Backbone of Science](https://cns.iu.edu/docs/publications/2005-boyack-mapbckbn.pdf).

### Inferences
- **The Atlas's 3D is partly a good idea wrongly encoded.** Fixed height is honest because it is a labelled, ordered category, unlike a fitted axis. That avoids the ordinary 3D failure of depth carrying continuous data. Its costs remain: occlusion and unreadable labels on a monitor, as Alper et al. note, and orbit-only viewing without stereo.
- **Force simulation contradicts the spatial reading.** The links pull nodes from their MDS anchors, so distance becomes a mix of two meanings, yet Fabrikant's result implies people will read distance as similarity. Keep anchored positions fixed, or show displacement.
- **Terrain must be tested on the task it claims to serve.** Tory et al. warn against landscapes for finding points. No study I found tests terrain for "what is the shape of this cultural field?" or for memory of a recurring map. That is the gap this project could fill.
- **If terrain is used, height needs one simple meaning, plausible landforms and a points layer on top.** Otherwise lay readers will invent their own geology. A hill will imply "bigger" or "better", and a basin will imply "bad".

### Gaps
- Munzner's "no unjustified 3D" rule could not be sourced directly. Her evidence appears here through the Sedlmair and Tory co-authored studies.
- I found no study of depth-of-belief height encodings, and no study of map-metaphor comprehension with lay political audiences. The Saket study named in my search was not found.

## Exemplars: what each gets right

### Takeaway
The best maps of meaning share five things: density as background, hierarchical labels placed directly on the map, a link from every mark to source text, a small number of named views, and restraint about what distance means. None of them I reached handles stance, depth of belief and dispute together. That combination appears to be the open space, which supports Benjamin's sense that it has not been cracked.

### Cited Findings

**Practice / opinion (nearly all exemplars are unevaluated)**

| Exemplar | What it gets right | Limit or note | Source |
|---|---|---|---|
| Blackbird.AI Constellation | Treats a narrative as a cluster of related content, and adds risk signals, actor coalitions, cohort and platform distributions, and a "narrative threat matrix". It began as a 3D graph of users, hashtags and posts, and the 2.0 dashboard caption describes stats, platform volume and high-risk posts | Vendor marketing. No public screenshot reached, and the page does not say why 3D was dropped, only that scale was the 2.0 driver | [Engineering post](https://blackbird.ai/blog/engineering-blackbird-ai-constellation-narrative-intelligence-platform/); [API post](https://blackbird.ai/blog/blackbird-ai-rav3n-recon-constellation-api/); [Narrative Feed](https://blackbird.ai/blog/narrative-feed-help-organizations-combat-narrative-attacks-blackbird-ai/) |
| DataMapPlot | Publication-quality labelled maps, multi-level labels, about 500k points interactive, standalone | Aesthetic, not a truth guarantee | [Docs](https://datamapplot.readthedocs.io/en/latest/intro_splash.html) |
| Embedding Atlas (Apple) | Density clustering, automated labels, coordinated metadata views, millions of points in real time | Abstract only | [Paper](https://arxiv.org/abs/2505.06386) |
| Latent Scope | Open local pipeline: embed, project, cluster, LLM label, with flat-file provenance, plus named experiments | Licence unclear by one secondary report | [Repo](https://github.com/enjalot/latent-scope); [v1.0](https://github.com/enjalot/latent-scope/releases/tag/v1.0.0); [licence note](https://www.sourcepulse.org/projects/1844455) |
| Map of Reddit (anvaka) | Geographic metaphor, "Show Related" for first- and second-degree links, and data editable through a repo. The README warns proximity may be "just an artifact" | Co-commenting from 176M comments, so it maps attention rather than belief | [README](https://github.com/anvaka/map-of-reddit) |
| RedditMap.Social | Clusters by users, built as public infrastructure for research | Same attention caveat | [Media Cloud](https://www.mediacloud.org/research/redditmap-social-a-novel-map-of-reddit-based-on-user-clustering) |
| Map of Philosophy (Noichl) | UMAP and HDBSCAN on citations produced a real finding: the analytic/continental split is overstated, and analytic philosophy is not one coherent group | Corpus size differs between sources (1.78M articles vs 60k+ papers) | [Synthese](https://link.springer.com/10.1007/s11229-019-02390-8); [profile](https://www.uni-bamberg.de/en/bagss/members/doctoral-postdoctoral/doctoral/maximilian-noichl) |
| Science maps (Börner, Boyack, Klavans) | Compared 8 similarity measures before publishing, and a later consensus map drew on 20 existing maps. This is validation as a design step | Citation data, not stance | [Backbone paper](https://cns.iu.edu/docs/publications/2005-boyack-mapbckbn.pdf); [NIH tutorial](https://cns.iu.edu/docs/presentations/10-NIH-Tutorial-12.pdf) |
| Graphika | Pairs a force map with a density matrix of attentive clusters against outlink bundles, so patterns of attention can be read without spatial guessing | Known from patents, current practice unconfirmed | [US 8635281](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8635281); [application](https://uspto.report/patent/app/20160048556) |
| Polis | Shows the ecosystem of perspectives while it forms, and participants use it to write new statements. Axes are PCA of the vote matrix and represent no comment | Critics question whether groups are real; those critiques are informal | [CompDem](https://compdemocracy.org/polis/); [Melbourne explainer](https://mspgh.unimelb.edu.au/centres-institutes/centre-for-health-equity/research-group/beyond-disasters/projects/climate-change/polis/the-polis-visualisation); [replication note](https://scrapbox.io/nishio-en/pPolis2024-05-27) |
| Talk to the City | Connects high-level themes to each person's claims, presented as a way to mitigate LLM inaccuracies. Drill-down through subclusters | Visual layout not detailed on the page | [AOI](https://ai.objectives.institute/talk-to-the-city) |
| Kialo | Claim tree with pro and con branches, plus a colour-coded sunburst overview | Sunburst description comes from a forum user | [Kialo guide](https://ecocommunity.notion.site/Kialo-Guide-db8d334007e047d5b0b7a425edd0f20a); [Argdown forum](https://forum.obsidian.md/t/43299) |
| Argdown | Text is the source of truth and maps are generated from it, so arguments can be edited and versioned | Trees suit small debates | [Guide](https://argdown.org/guide/creating-argument-maps.html) |
| Society Library | "Civilization-scale" debate-map databases that compare reasoning behind views. It says it is still exploring visualization | No public form confirmed | [Site](https://www.societylibrary.org/) |
| Atlas of Emotions (Stamen with Ekman) | Metaphor as an explicit authored argument: emotions as continents, states as peaks on an intensity scale, a set of maps rather than one. Its basis is a survey of 248 scientists | Critics note Ekman's methods have been challenged, so it shows how a beautiful map can outrun its evidence | [Stamen](https://stamen.com/work/atlas-of-emotions/); [Stamen press](https://stamen.com/press/stamens-atlas-of-emotions/); [Bloomberg](https://www.bloomberg.com/news/articles/2016-05-06/stamen-s-atlas-of-emotions-was-inspired-by-the-dalai-lama) |
| Inglehart-Welzel cultural map | Two named axes, a stated variance share (over 70% of cross-national variance), and re-issue with each survey wave | Two-factor split weakly supported by some analysis, and rotation disputed. Criticized for essentialism | [Summary](https://en.wikipedia.org/wiki/Inglehart%E2%80%93Welzel_cultural_map_of_the_world) |
| Nolan chart | Moved past one line in 1969 | Critics say economic and personal issues cannot be cleanly split, as migration shows | [Summary](https://en.wikipedia.org/wiki/Nolan_Chart) |
| Red/blue electoral maps | Pew finds red/blue far from adequate for the spectrum of views. Brookings notes the maps simplify divergence within states | Both are old | [Pew 2006](https://www.pewresearch.org/politics/2006/04/10/in-search-of-ideologues-in-america/markdown); [Brookings](https://www.brookings.edu/wp-content/uploads/2016/06/20050429_rpa.pdf) |
| Grandjean | Network history with a beginner series on visual analysis and centrality, tying the picture to a method of reading it | Page-level summary only | [Site](https://www.martingrandjean.ch/) |

### Inferences
- **What Blackbird probably gets right.** Benjamin's preference fits a shift from graph-of-entities to narrative-as-object: named units with a size, trend, risk, actors and a card. That reading is inferred from the text, because I could not see the visuals. Ask Benjamin for the specific screen he means.
- **Its frame is the thing not to copy.** Blackbird scores narratives as threats to an organization. The Arena's purpose is that clusters can describe each other in terms they would sign. "Attack" and "risk" framing would work against meta-consensus even if the visual form is borrowed.
- **The Atlas's cards are closer to best in class than its scene.** Polis, Talk to the City and Blackbird all put the understanding in linked summaries rather than in geometry.
- **Publish the variance share.** The Inglehart-Welzel habit of stating it next to the map, plus Noichl's habit of treating a map as an argument, is a low-cost credibility move.

### Gaps
- Could not identify or reach: "Thematic Mapper", "MoDA", "Cartography of Culture" as a named project, "Atlas of Ideas", "Worldview Atlas". Nomic's blog failed twice with connection errors. Santiago Ortiz's portfolio loaded only as a canvas stub, so no project could be assessed ([page](https://moebio.com)).
- Not reached: The Pudding, Observable, Manuel Lima, Bellingcat network maps, Barberá's visual work (B4 covers his methods), the NYT political map beyond a [listing](https://ifp.nyu.edu/?p=1390603), and Political Compass critiques. I found no peer-reviewed study of how participants read Polis maps.
- Very few of these exemplars have been evaluated with users. Treat "gets right" as design judgment.

## Temporal and metabolic views: showing narratives move

### Takeaway
For showing that clusters split and merged, the alluvial diagram with significance testing is the strongest method found, because it refuses to draw changes that do not survive resampling. Animation works for presenting and fails for analysis, so the map should animate for a story and offer static small multiples for checking.

### Cited Findings

**Tested**
- Rosvall and Bergstrom cluster each time slice, draw about 1,000 bootstrap networks, and mark the core of each cluster that holds together in at least 95% of bootstraps. In the alluvial diagram, block height is flow, darker shading is the significant core, and ribbons show moves. Merges and splits failing thresholds are shown as nonsignificant — [PLOS ONE 2010](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0008694).
- Animation is fast and enjoyable for presentation, but led to many errors and was the weakest option for analysis. Small multiples were more accurate and static displays were faster — [Robertson et al.](https://www.microsoft.com/en-us/research/publication/effectiveness-of-animation-in-trend-visualization/).

**Practice / opinion**
- BERTopic's dynamic mode fixes topics globally and only re-words them per timestep. It recommends under about 50 timestamps — [Docs](https://maartengr.github.io/BERTopic/getting_started/topicsovertime/topicsovertime.html). So a topic cannot truly split or merge in this method.
- AlignedUMAP keeps positions comparable across slices and supports online appending — [Docs](https://umap-learn.readthedocs.io/en/latest/aligned_umap_basic_usage.html).
- Narrative Maps represent a story as a route map, with the most coherent path as the main storyline and events as landmarks, shown on three successive COVID maps. A follow-up suggests analysts can use them as a representation of their mental model — [Keith Norambuena and Mitra, CSCW 2020](https://arxiv.org/pdf/2009.04508); [follow-up](https://ar5iv.labs.arxiv.org/html/2112.12205).

### Inferences
- **Do not use dynamic topic models for lineage.** Their fixed-topic design rules out the splits and merges the Arena wants to see. Use per-slice clustering linked by alluvial matching, in line with the existing decision on cluster lineages (D19, cited in the B4 header note).
- **Adopt the darker-core idea directly.** Mark which part of a school is stable under bootstrap. It also gives an honest answer to "are the 9 schools real?"
- **Small data warning.** Bootstrap stability in a corpus of landmark transcripts may show few significant moves. An empty result is a valid result to show.

### Gaps
- Could not reach ThemeRiver, TextFlow, StoryFlow, dynamic topic models (Blei and Lafferty) or the Archambault and Purchase work on mental-map preservation. No claims are made about them here.
- Segel and Heer's *Narrative Visualization* could not be fetched. The two URLs tried returned 404 and a connection error, so its genres are not characterized here.
- I found no evidence on flows drawn over terrain.

## Uncertainty and accountability: the map as a contested claim

### Takeaway
Showing uncertainty is rare in practice, partly because it limits the conclusions a reader can draw, which is the reason to do it here. Critical cartography's main demand is that a map should show its authors and its choices. The most concrete working model for dispute comes from borders: publish a default plus alternative points of view.

### Cited Findings

**Tested**
- Hypothetical outcome plots (animated draws) beat error bars and violin plots for two- and three-variable probability judgments (288 Mechanical Turk subjects), where static displays had errors of at least 36 points on bivariate tasks. They were worse on some one-variable tasks — [Hullman, Resnick and Adar 2015](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444).
- A survey of 90 visualization creators and interviews with 13 designers found authors say uncertainty is valuable yet follow a norm of omitting it. The paper argues that showing uncertainty necessarily limits the conclusions viewers can draw — [Hullman, 2019](https://arxiv.org/abs/1908.01697).

**Practice / opinion**
- Harley: maps are social documents and "never value-free images"; he discouraged placing them above the politics of knowledge — [Critical cartography summary](https://en.wikipedia.org/wiki/Critical_cartography). This is a secondary summary, and the page cites a 1992 essay for his "hidden agendas of cartography" phrase.
- Counter-mapping was coined by Peluso in 1995 from Kalimantan, where NGOs adopted state conventions to make Dayak claims legible. Risks: mapping can fix boundaries it contests, treat community as bounded, overlook women and minorities, and work only when paired with legal or political strategies — [Summary](https://en.wikipedia.org/wiki/Counter-mapping).
- Natural Earth publishes a de facto default plus point-of-view variants for several dozen countries, so users can assemble borders matching their own view — [Natural Earth](https://www.naturalearthdata.com/blog/admin-0-countries-point-of-views/).
- Talk to the City treats the link from summary to individual claim as a safeguard against LLM errors — [AOI](https://ai.objectives.institute/talk-to-the-city). Argdown and the Map of Reddit keep the underlying data editable — [Argdown](https://argdown.org/guide/creating-argument-maps.html); [Map of Reddit](https://github.com/anvaka/map-of-reddit).
- A1 records that rendering opacity by status is already part of the project's own lineage — `docs/research/A1-ontography.md` §1.4.

### Inferences
- **Treat each boundary as a claim with an author.** Each school boundary or placement gets: who or what drew it, on what evidence, when, how stable, and who disputes it.
- **"Point of view" variants are the most distinctive idea to borrow.** Let a mapped cluster or landmark's representatives publish their own view of the map, for example "how we would draw this", next to the default, as with Natural Earth. It fits meta-consensus better than a correction queue, because the gap between the views is itself the finding: the map is scored by whether the described side would sign it. Ratified descriptions then become the visible geography, with unratified areas drawn differently.
- **Show dispute in the visual vocabulary.** Dashed boundaries, hatching for contested placement, and a mark for disputed items, all visible at the overview level instead of hidden in a panel. The dashed-border idea is a design proposal, not a tested result.
- **Two kinds of uncertainty need separate marks.** Model uncertainty (stability under bootstrap, projection error) differs from social contest (someone disputes this). Mixing them would make a disputed placement look like a statistical accident.
- **Use draws for placement.** Hypothetical outcome plots suggest an option to jitter a placement across bootstrap draws, showing that a position is a distribution. Note the mixed one-variable results.
- **Counter-mapping's warning applies to the Arena.** Representatives of a cluster may silence internal dissent, and a dispute mechanism favours people with time and standing. Flagged landmarks stay out of public views as `CLAUDE.md` requires, and any dispute feature is outward-facing, so it needs Benjamin's sign-off.

### Gaps
- Primary texts of Harley, Wood and *Data Feminism* could not be read. The Data Feminism page returned HTTP 403, so its "god trick" and pluralism arguments are not cited here despite their relevance.
- Value-suppressing uncertainty palettes (Correll et al.) could not be reached, though they are a likely fit for colour. Check them before choosing an uncertainty encoding.
- No evaluation was found of a dispute affordance on any public map, and no study of participatory worldview mapping.

## Layered ontology of meaning: does anything show depth of belief?

### Takeaway
I found no existing visualization that plots depth of belief as a measured axis from data. The depth frameworks exist mainly as diagrams of a theory. That makes the Atlas's layer axis potentially novel, and also unvalidated.

### Cited Findings

**Practice / opinion**
- Causal Layered Analysis has four layers: litany, social and structural, worldview, myth and metaphor. The summary I read describes no visualization — [Summary](https://en.wikipedia.org/wiki/Causal_layered_analysis).
- Spiral Dynamics represents Graves's value systems through colour-coded stages. It is reported to lack mainstream academic validity, and critics call its colour codes arbitrary. Its visual presents development as stages, which invites ranking even though the model says no stage is inherently better — [Summary](https://en.wikipedia.org/wiki/Spiral_Dynamics).
- The project's own stratum order comes from Ontography and Topology Live (ontology, epistemology, axiology, praxis, plus empirical), with a crux drawn as a fault plane — `docs/research/A1-ontography.md` §1.2, §1.7; `docs/research/A3-anti-debate-topology-live.md` §1.2, §1.3.
- Atlas of Emotions shows intensity in peaks across continents, the closest formal parallel found to a vertical meaning axis — [Stamen](https://stamen.com/work/atlas-of-emotions/).

### Inferences
- **The novel object is the fork.** Instead of a stack of nodes, show where two clusters that agree at the surface split further down, or agree on praxis for different reasons. That maps onto the incompletely theorized agreement already in the Topology Live ontology. A geologic cross-section between two clusters is the natural form: a slice along the line joining them, with shared strata continuous and faults where they diverge.
- **Avoid implying depth equals more advanced or more true.** The Spiral Dynamics reception shows the risk. Bottom-to-top layering already suggests ground and superstructure. Label it as "what this rests on", and test whether readers infer a ranking.
- **Respect that layers are assigned claims.** The evidence that a proposition's layer is reliable is the project's own gold-set work, so the layer boundary itself should carry uncertainty.

### Gaps
- Iceberg model: the page tried returned 404, so no source. Worldview Atlas: not identified.
- Search for visualized CLA ran out of budget. A CLA data visualization may exist. My "none found" is weaker than a real absence.

## Ranked forms worth prototyping

### Takeaway
Prototype a 2D-first "layered map with fault cross-sections" as the core, with distortion and dispute drawn on the map, and treat terrain and 3D as experiments that must beat it in a test. Ranking below is my design opinion, weighted by evidence, fit with meta-consensus, and cost for a near-zero budget.

### Cited Findings
- The evidence for each item is cited in the sections above. No study directly tests any of these forms on worldview data.

### Inferences

| Rank | Form | What it is | Why this rank | Main risk | Test that would settle it |
|---|---|---|---|---|---|
| 1 | **Fixed-position 2D map with honest layers** | MDS plane, positions locked, density underlay, hierarchical labels, narrative cards as primary objects, and a Layer selector instead of height | Supported by Sedlmair, Tory (points first), Jeon (global method), and exemplars' cards. Lowest cost | Less wow than current 3D | Readers answer "who is close to whom?" and "what does school X hold?" against the current Atlas |
| 2 | **Distortion lens** | Select any mark to see true full-space neighbours as links; toggle for error-coloured cells; published variance share | Directly answers "show what the projection lost". ZADU and `sklearn` trustworthiness are available | Too technical unless written plainly ("these two only look close") | Do readers stop over-trusting false neighbours? |
| 3 | **Fault cross-section between two clusters** | Pick two schools; see a slice by layer with shared ground, forks and cruxes | The new object nobody has. Serves SEE and MEET. Uses data already built | Geologic metaphor may imply depth is truth, and may lack enough deep-layer stated claims | Would both sides sign the slice? Use signability as the measure |
| 4 | **Signed map: points of view and ratified geography** | Default map, cluster-authored alternative views, ratified descriptions drawn solid, unratified and disputed hatched | Best fit with the success definition. Borrowed from Natural Earth and critical cartography | Needs real participants, outward-facing, and subject to privacy rules. Prototype with fictional or internal review first | Rate of "that's not me" corrections, and member-check agreement |
| 5 | **Significance-tested alluvial of schools** | Time columns, dark stable cores, ribbons for splits and merges, linked to the map | Strongest method found for lineage. Fits D19 | Too little time depth now. Bootstrap may show few moves | Do reported shifts survive resampling? |
| 6 | **Comparison small multiples** | One small map per layer or issue, same positions, colour by stance | Robertson favours static multiples for analysis. Also handles more than three dimensions, as the 46% lives elsewhere. Very cheap | Many panels on phones | Accuracy on "where do these two split?" |
| 7 | **Tree or sunburst overview** | Dendrogram of schools from full-space clusters | Needs no projection, per Chari and Pachter and Kialo. Good companion and phone view | Hides cross-links | Compare comprehension with the map |
| 8 | **Scrollytelling tour** | Short authored path through the map, ending in free exploration | Animation suits presentation (Robertson). Good for first-time public readers | Authored story becomes the map's voice, which is a neutrality risk | Recall and perceived fairness, across clusters |
| 9 | **Terrain view** | Contours and wells, height with one meaning such as density of adherents | Wanted by Benjamin and memorable, but Tory and Fabrikant caution against it. Keep as an experiment on a task it might win | Readers invent meaning. Basins and peaks imply value | Head-to-head with rank 1: memory of the map after one week, and "shape of the field" questions |
| 10 | **Current 3D Atlas as "explorer mode"** | Keep the layered 3D with positions locked, and remove force displacement | Retains the striking image and fixed categorical height. Depth still needs motion to read | Labels and occlusion | Does it add anything over rank 1 and 3? |
| 11 | **Hyperbolic or Mapper views** | Research lenses | Mapper is useful for analysts, and hyperbolic needs evidence of tree structure | Parameter sensitivity, and hard for lay readers | Internal analysis only |

**Suggested order.** Build 1, 2 and 7 as one page, then 3. Run a small comparison against the current Atlas before spending effort on 9 or VR. Item 4 requires Benjamin's approval before anything is shown to mapped people. Any tool choice that costs money also needs his approval, though everything above can be done with open-source libraries already named in B4.

**A testing idea for the wider field.** Since almost none of these forms have been evaluated on worldview data, a small published comparison of points, terrain and 3D with cross-cluster readers would be original work.

### Gaps
- Rankings have no direct user evidence from this project's audience.
- The Blackbird comparison is limited by not seeing the specific visuals Benjamin has in mind.
- Phone and accessibility performance of each form was not researched.
