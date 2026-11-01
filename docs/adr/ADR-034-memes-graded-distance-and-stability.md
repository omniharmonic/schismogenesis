# ADR-034: Memes, graded distance and stability

Status: accepted for the pilot. Date: 2026-11-01.

Positions show what people hold. Memes show what they use and how ideas travel.

**Memes.** A reader proposes concepts and cited figures with tested patterns. Code counts them
across full public texts, with no model and no length cap. A reader then judges each person's
stance from sampled passages: embraces, attacks, engages or mentions. A count alone cannot tell
adoption from attack, and quoting is not adopting.

**Distance.** Positions within a question have graded distance: shared, compatible, in tension or
opposed. Pair distance averages over shared questions only and is pulled toward an uninformative
prior when overlap is thin. Binary scoring wrongly made Yarvin an outlier.

**Map and stability.** Classical MDS places people from those distances, and the page states how
much structure two dimensions capture. Groupings use average linkage at a cut of 0.40, chosen by
inspection. A bootstrap over questions reports how often each pair stays together. A grouping
carries only the weight its stability supports.

These are not the S11 clusters of the spec: thirteen people chosen by hand are not a population.
