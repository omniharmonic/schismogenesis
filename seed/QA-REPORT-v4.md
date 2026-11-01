# QA and merge report: Dialogos Arena SEED-v4

Author of record: Benjamin Life (@omniharmonic). QA/merge pass over SEED-v3 and the g7 (online subcultures) and g8 (holistic sweep) gap fills, 2026-10-31. Every judgment call is data in `scripts/decisions_v4.py`; `scripts/build_v4.py` applies them as a delta over `SEED-v3.json` and renders all outputs. No v3 file was modified.

## 1. Result

- **234 niches, 817 landmarks** (v3: 220 / 771). Added 14 niches (g7 4, g8 9, QA 1) and 46 landmark records; 4 alternates unchanged.
- Structural validation: 4 g7/g8 files parsed; 0 schema problems. Build warnings: 0 (no thin, over-cap or core-less niches; no dangling references).
- Verification: 592 verified-active (72%), 222 pending, 3 stale.
- Women 30% of landmarks (v3 29%); 54% of v4 additions. Bridgers 27% (v3 26%).
- Mirror pairs: 53 (7 new). Unpaired issue niches: none.
- g8 coverage matrix: 154 external categories across 7 taxonomies; 150 covered (incl. 11 former gaps closed in v4: 7 by new niches, 4 by sub-niches or landmarks), 2 still gaps, 2 excluded or not needed (§8).

## 2. Decisions needing Benjamin

### 2.1 Conflict flags (`flags_for_benjamin.conflict_flags`)

| Landmark | Niche | Added | Reason |
|---|---|---|---|
| Brad Carson | Populist AI backlash (anti-transhumanist right & AI-accountability coalition) | v4 | Public First (his AI-policy group and super PAC) is reportedly funded mainly by Anthropic, the company whose model assembled this seed. Benjamin to decide whether to keep him (conflict-of-interest check). |
| Griff Green | Regens / ReFi & public-goods funding | v3 | In Benjamin's professional network; confirm inclusion (conflict-of-interest check). |
| Kevin Owocki | Regens / ReFi & public-goods funding | v3 | In Benjamin's professional network; confirm inclusion (conflict-of-interest check). |
| Monty Bryant | Regens / ReFi & public-goods funding | v3 | Benjamin's long-term collaborator; confirm inclusion (also pending verification). |
| Samantha Power (The BioFi Project) | Regens / ReFi & public-goods funding | v3 | Benjamin's collaborator (The BioFi Project); confirm inclusion. Not the former USAID administrator. |

Brad Carson is new: the funding claim is from g8's sources ("reportedly") and was not independently checked. Because the seed was assembled with an Anthropic model, keeping him is Benjamin's call, not the build's.

### 2.2 All landmark flags (v3 flags kept unchanged)

| Landmark | Niche | Type | Reason | Status |
|---|---|---|---|---|
| Brad Carson | Populist AI backlash (anti-transhumanist right & AI-accountability coalition) | conflict-of-interest | Public First (his AI-policy group and super PAC) is reportedly funded mainly by Anthropic, the company whose model assembled this seed. Benjamin to decide whether to keep him (conflict-of-interest check). | verified-active |
| Griff Green | Regens / ReFi & public-goods funding | conflict-of-interest | In Benjamin's professional network; confirm inclusion (conflict-of-interest check). | verified-active |
| Kevin Owocki | Regens / ReFi & public-goods funding | conflict-of-interest | In Benjamin's professional network; confirm inclusion (conflict-of-interest check). | verified-active |
| Monty Bryant | Regens / ReFi & public-goods funding | conflict-of-interest | Benjamin's long-term collaborator; confirm inclusion (also pending verification). | pending |
| Samantha Power (The BioFi Project) | Regens / ReFi & public-goods funding | conflict-of-interest | Benjamin's collaborator (The BioFi Project); confirm inclusion. Not the former USAID administrator. | verified-active |
| Alex Jones | Conspiracy-realist & patriot independent media | exclusion-review | Keep descriptively or exclude — review. | verified-active |
| Andrew Tate | Top G / alpha hustle masculinity | exclusion-review | Possible harassment/incitement bar — review. | pending |
| Haz Al-Din | Patriotic socialism / 'MAGA communism' (American Communist Party) | exclusion-review | Confirm inclusion under the designated-organization exclusion — review. | verified-active |
| Jackson Hinkle | Patriotic socialism / 'MAGA communism' (American Communist Party) | exclusion-review | Confirm inclusion under the designated-organization exclusion — review. | verified-active |
| Jared Taylor | Race-realist / 'HBD' dissident right | exclusion-review | Contested movement leader; confirm inclusion under the brief's exclusion bars — review. | verified-active |
| Joel Webbon | Christian nationalism (self-identified; Moscow-style Reformed) | exclusion-review | Possible harassment bar — review. | verified-active |
| Laura Loomer | MAGA media mainstream (pro-Trump America First media) | exclusion-review | Possible harassment bar — review. | verified-active |
| Mohammed Hijab | Muslim dawah & anti-liberal traditionalists | exclusion-review | Possible harassment bar — review; also UK-based (US-centrality check). | verified-active |
| Myron Gaines (Amrou Fudl) | Red Pill dating / sexual market value | exclusion-review | Possible harassment/incitement bar — review. | verified-active |
| Nick Fuentes | Groypers / America First (Fuentes) | exclusion-review | Possible harassment/incitement bar; keep descriptively or exclude — review. | verified-active |
| Sneako | Groypers / America First (Fuentes) | exclusion-review | Tied to the Fuentes decision; review alongside it. | verified-active |
| Timothy Gordon | Traditionalist Catholics (Latin Mass) | exclusion-review | Possible harassment bar — review. | pending |
| Tristan Tate | Top G / alpha hustle masculinity | exclusion-review | Possible harassment/incitement bar — review. | pending |
| Umar Johnson | Black nationalism & self-determination (Pan-Africanist / conscious community) | exclusion-review | Possible harassment bar — review; weak verification. | verified-active |
| Clavicular (Braden Peters) | Looksmaxxing & blackpill | minor-adjacent | Young adult creator in a scene with many minors; confirm comfort with inclusion. | verified-active |

### 2.3 Niches that need an outside reviewer

| Niche | Added | Why |
|---|---|---|
| Tribal nations & Native politics (sovereignty within the federal system) | v4 | Outside reviewer recommended (near Benjamin's Treaty Land Atlas work). |
| Deliberative democracy & civic tech | v3 | Benjamin's own field (civic tech); written neutrally by g4 with Benjamin and his organizations excluded; needs an outside reviewer. |
| Metacrisis / Great Simplification (liminal web core) | v3 | Near Benjamin's own field; needs an outside reviewer. |
| Metamodernism / political metamodernism | v3 | Near Benjamin's own field; needs an outside reviewer. |
| Bioregionalism & regenerative culture | v3 | Benjamin's own field (Spirit of the Front Range); needs an outside reviewer. |
| Land Back / Indigenous sovereignty | v4 | Outside reviewer recommended (near Benjamin's Treaty Land Atlas work). |
| Regens / ReFi & public-goods funding | v3 | Near Benjamin's own field and network; needs an outside reviewer. |

### 2.4 Open calls

1. **Haaland and Woodard moved** (§4.2). Reverse if Benjamin prefers g8's minimal change for Haaland. Side effect: liberal feminism's remaining primaries (Valenti, Filipovic) are both pending, so it now has no verified-active primary; verifying either (both publish weekly newsletters) fixes this cheaply.
2. **Taylor Lorenz and William Costello** are outside interpreters (edge) in looksmaxxing, not adherents; move Lorenz to streamer-creator-culture if landmarks must be adherents (that niche is at the cap).
3. **Thin new niches** to demote if verification fails: Sober-curious (both primaries pending), Sikh American voices (Singh pending), Main Street small business (2 primaries), State sovereignty/secession (Evans pending).
4. **Secession** maps the sovereign-citizen movement only as a sub-niche, with no landmarks (exclusion rule).
5. v3 open calls (edge as bridger; scale; Tate/Fuentes decisions) are unchanged.

## 3. New niches

| Niche | Dom | gap_type | L/R | Landmarks |
|---|---|---|---|---|
| **State sovereignty, secession & 'national divorce' movements** (`secession-national-divorce`) | d1 | political-edge | X | Daniel Miller (c), Marcus Ruiz Evans (c)*; also: Marjorie Taylor Greene |
| **Rural progressives & New Appalachia ('dirt-road' Democrats)** (`rural-progressives-new-appalachia`) | d2 | representation (regional) | L | Matt Hildreth (c), Silas House (c), Sarah Smarsh (c), Chloe Maxmin (b); also: Dan Osborn |
| **Tribal nations & Native politics (sovereignty within the federal system)** (`tribal-nations-native-politics`) | d2 | representation | CL | Rebecca Nagle (c), Mark Trahant (c), Peggy Flanagan (b), Deb Haaland (b), Markwayne Mullin (e) |
| **Populist AI backlash (anti-transhumanist right & AI-accountability coalition)** (`populist-ai-backlash`) | d3 | mirror | X | Joe Allen (c)*, Josh Hawley (c), Brad Carson (b)⚑; also: Bernie Sanders, Steve Bannon |
| **COVID-conscious & long-COVID community** (`covid-conscious-long-covid`) | d4 | mirror | L | Betsy Ladyzhets (c), Julia Doubleday (c)*, Beatrice Adler-Bolton & Artie Vierkant (Death Panel) (b) |
| **Sikh American voices** (`sikh-american-voices`) | d5 | representation | CL | Valarie Kaur (c), Simran Jeet Singh (c)*; also: Harmeet Dhillon |
| **Decentering men & single-on-purpose women** (`decentering-men-single-on-purpose`) | d6 | mirror | L | Hope Woodard (c), Shani Silver (c), Amanda Montei & Tracy Clark-Flory (Dire Straights) (c)*, Bella DePaulo (e)* |
| **Sober-curious & alcohol-free movement** (`sober-curious-alcohol-free`) | d6 | subculture | X | Annie Grace (c)*, Holly Whitaker (c)*; also: Ruby Warrington |
| **Wellness girlies: 'that girl' self-optimization & hormone health** (`wellness-girlies-hormone-health`) | d6 | subculture | X | Alisa Vitti (c), Lauryn & Michael Bosstick (The Skinny Confidential) (c), Liz Moody (b)* |
| **Black agrarianism & the rural Black South (land, food sovereignty, environmental justice)** (`black-agrarianism-rural-black-south`) | d7 | representation | L | Catherine Coleman Flowers (c), Leah Penniman (c), Karen Washington (b)*; also: John Boyd Jr. |
| **Farm-and-ranch mainstream (ag media & farm YouTube)** (`farm-ranch-mainstream`) | d7 | mainstream | CR | Chip Flory (c), Zach Johnson (Millennial Farmer) (c), Tyne Morgan (b)* |
| **Main Street small-business owners (owner-operator & 'buy a boring business' culture)** (`main-street-small-business`) | d7 | representation (occupational) | CR | Codie Sanchez (c), Rick Woldenberg (b); also: Dave Ramsey |
| **Markets & investing mainstream (Wall Street, FinTwit macro & retail trading)** (`markets-investing-mainstream`) | d7 | atlas-gap | C | Jim Cramer (c), Joe Weisenthal & Tracy Alloway (Odd Lots) (c); also: Kevin Paffrath (Meet Kevin), Scott Galloway |
| **Minimalism & anti-consumerism (no-buy, deinfluencing)** (`minimalism-anti-consumerism`) | d7 | subculture | X | The Minimalists (Joshua Fields Millburn & Ryan Nicodemus) (c), Matt D'Avella (c)*, Dawn Madsen (The Minimal Mom) (b); also: Cal Newport, Juliet Schor |

Atlas matches normalized to the 39 known Owocki names (raw partial labels replaced): `black-agrarianism-rural-black-south`: 'regens & solarpunks (partial)' → None; `secession-national-divorce`: 'network-state builders (partial: exit as strategy)' → None; `populist-ai-backlash`: 'maga / populist right (anti-AI strand); mirror of effective accelerationists' → None; `markets-investing-mainstream`: 'wall street / macro; wallstreetbets' → wall street / macro; `main-street-small-business`: 'indie hackers (offline analogue)' → None.

Boundary calls accepted from the agents: incel/blackpill stays a sub-niche of looksmaxxing (mapped only through adult researchers and journalists); 4B / decentering men promoted out of liberal feminism; wellness girlies kept apart from MAHA and fitness-biohacking; sober-curious kept apart from harm reduction and recovery-first; Sikh voices kept apart from Hindu American voices; farm-and-ranch mainstream kept apart from the rural populist farmer movement (now mirrored); tribal-nations split out of Land Back. g8 suggested minimalism as a degrowth sub-niche while g7 made it a niche: the niche wins, and degrowth's sub-niche now points to it.

## 4. Additions to existing niches, dedupe and moves

### 4.1 New records in existing niches

| Landmark | Niche | Role | Status | Reason |
|---|---|---|---|---|
| Kareem Shami | Looksmaxxing & blackpill | core | verified-active | Second verified adult, US-based core voice with long-form interview output. Lowers the niche's reliance on Clavicular (flagged) and Mike Mew (UK, pending). |
| Taylor Lorenz | Looksmaxxing & blackpill | edge | verified-active | Adult long-form commentator on the scene, as Benjamin asked. |
| William Costello | Looksmaxxing & blackpill | edge | pending | Maps incel/blackpill discourse only through adult researchers, as the task specified. |
| Mina Le | Gen Z disaffection: irony, doomer & lying-flat culture | bridger | verified-active | Gives the new 'girl rot / femcel / girlhood' sub-niche an adult long-form voice without promoting it to a niche. |
| Shane Claiborne | Progressive / mainline Christianity | bridger | pending | The Christian left (Red Letter Christians, already a sub-niche here) had no landmark. Not promoted to its own niche: it shares progressive-christianity's sacred values and differs mainly in activist tactics. |
| Guerline Jozef | Immigrant-rights movement | bridger | verified-active | Caribbean/Haitian/African immigrants fail the bar as a separate niche (few long-form voices with a shared distinct worldview); adding a Black-immigrant voice and sub-niche here represents them. |

### 4.2 Primary moves

| Landmark | From | To | New role | Reason |
|---|---|---|---|---|
| Hope Woodard | Mainstream liberal / intersectional feminism | Decentering men & single-on-purpose women | core | Originator of 'boysober'; g7 recommends this as her home. Kept as a secondary (bridger) in liberal feminism. Her current show still needs a re-check. |
| Deb Haaland | Land Back / Indigenous sovereignty | Tribal nations & Native politics (sovereignty within the federal system) | bridger | Her v3 slot represented the tribal-government / Native electoral sub-niche, which moved to the new niche. Kept as a secondary (bridger) in Land Back. |

Not moved: Ruby Warrington. g7 suggests making sober-curious her primary; kept in childfree-by-choice (moving her would leave that niche with one landmark). Secondary (core) in sober-curious.

### 4.3 Dedupe and secondary listings

All 46 new names were checked against the 775 v3 landmark and alternate ids (by id and by normalized name); none duplicates a v3 record. 17 secondary listings of existing people were applied (roles in `secondary_roles`):

| Landmark | Primary | Secondary in | Role |
|---|---|---|---|
| Cal Newport | Humane tech / attention critics | Minimalism & anti-consumerism (no-buy, deinfluencing) | bridger |
| Juliet Schor | Degrowth / post-growth | Minimalism & anti-consumerism (no-buy, deinfluencing) | bridger |
| Ruby Warrington | Childfree by choice | Sober-curious & alcohol-free movement | core |
| Dan Osborn | Structural democracy reformers & anti-duopoly independents | Rural progressives & New Appalachia ('dirt-road' Democrats) | bridger |
| John Boyd Jr. | Rural populist / independent farmer movement | Black agrarianism & the rural Black South (land, food sovereignty, environmental justice) | core |
| Marjorie Taylor Greene | America First restraint right (Tucker-sphere) | State sovereignty, secession & 'national divorce' movements | edge |
| Steve Bannon | War Room populist nationalism | Populist AI backlash (anti-transhumanist right & AI-accountability coalition) | core |
| Bernie Sanders | Fight-the-oligarchy economic populist left | Populist AI backlash (anti-transhumanist right & AI-accountability coalition) | edge |
| Kevin Paffrath (Meet Kevin) | Degens / memecoin culture | Markets & investing mainstream (Wall Street, FinTwit macro & retail trading) | bridger |
| Scott Galloway | Men & boys' advocacy (healthy masculinity & men's issues) | Markets & investing mainstream (Wall Street, FinTwit macro & retail trading) | bridger |
| Dave Ramsey | Personal finance & FIRE | Main Street small-business owners (owner-operator & 'buy a boring business' culture) | edge |
| Harmeet Dhillon | Asian American conservatives & merit advocates | Sikh American voices | bridger |
| Shane Claiborne | Progressive / mainline Christianity | Evangelical conscience / 'post-Trump' evangelical critics | bridger |
| Riley Gaines | Gender-critical feminism | Sports talk culture (debate shows & sports podcasts) | edge |
| Riley Gaines | Gender-critical feminism | Gender-medicine skeptics & detransitioner voices | bridger |
| Taylor Lorenz | Looksmaxxing & blackpill | Gen Z disaffection: irony, doomer & lying-flat culture | edge |
| Taylor Lorenz | Looksmaxxing & blackpill | Streamer & IRL creator culture | edge |

## 5. Cheap gaps (QA step 2)

| Gap | Result |
|---|---|
| Riley Gaines / 'Save women's sports' | Added to **Gender-critical feminism** as bridger (verified 2025-12-17, new OutKick multi-year podcast deal). That niche already holds the anti-self-ID-in-sports position and has its mirror (LGBTQ+ & trans rights). Secondary in sports-talk culture (edge) and gender-medicine skeptics (bridger). Sub-niches added in both gender-critical feminism and sports-talk culture. No new niche (one voice checked). |
| COVID-conscious community (mirror of medical freedom) | **Added** `covid-conscious-long-covid` (D4, cross D6/D2): Betsy Ladyzhets (core, The Sick Times / Still Here, verified 2026-03-27), Beatrice Adler-Bolton & Artie Vierkant (Death Panel; bridger, verified Oct 2026), Julia Doubleday (core, pending). Bar met (2 verified adult long-form voices). Mirror pair recorded; disability sub-niche re-pointed. |
| A woman voice in minimalism | Added **Dawn Madsen (The Minimal Mom)** as bridger (YouTube upload about 2026-10-02 via aggregator; approximate, in spot-check). Juliet Schor (secondary) is also a woman. |

Considered and not added: 'Save women's sports' as its own niche: Not created: Gaines fits gender-critical feminism's existing position on sex-based sports; only one voice checked. Mirror (lgbtq-trans-rights) already exists.; Courtney Carver (Be More with Less / Project 333): No dated 2025-26 first-person item found; not seeded.; Elysia Berman (no-buy year): Guest appearances only (Jan 2025); no own long-form show found; not seeded.

## 6. Sub-niche changes

- `looksmaxxing-blackpill`: replaced 'incel forums (looksmax.org)' → 'incel / blackpill discourse (mapped only through adult researchers and journalists; forum figures not seeded)'
- `liberal-feminism`: replaced '4B / decentering men (merged niche)' → '4B / decentering men (now its own niche: decentering-men-single-on-purpose)'
- `land-back-indigenous-sovereignty`: replaced 'tribal-government & Native electoral politics (Deb Haaland, Sharice Davids; Nati' → 'tribal-government & Native electoral politics (moved in v4 to its own niche: tribal-nations-native-politics)'
- `disability-rights-justice`: replaced 'COVID-conscious / 'still coviding' community' → 'COVID-conscious / 'still coviding' community (now its own niche: covid-conscious-long-covid)'
- `crypto-degens`: replaced 'retail-trader YOLO: WallStreetBets, meme stocks, options & betting apps (absorbe' → 'retail-trader YOLO: WallStreetBets, meme stocks, options & betting apps (absorbed from g3 in v3; also listed under markets-investing-mainstream)'
- `gen-z-disaffection`: added 'girl rot / femcel / girlhood internet'
- `gen-z-disaffection`: added 'soft life (anti-hustle femininity)'
- `new-age-manifestation-wellness`: added 'divine-feminine / feminine-energy coaching (cross-reference tradwife 'feminine-energy coaching')'
- `humane-tech-attention-critics`: added 'AI-companion users (r/MyBoyfriendIsAI, #keep4o), described from the users' own perspective, not only as harm'
- `immigrant-rights-movement`: added 'Haitian, Caribbean and African (Black immigrant) advocates (Haitian Bridge Alliance, UndocuBlack)'
- `skilled-trades-dignity-of-work`: added 'truckers and owner-operator drivers (OOIDA, trucker YouTube; English-proficiency and freight-fraud fights)'
- `public-health-evidence-based-medicine`: added 'nurses and frontline healthcare workers (National Nurses United; nurse creators)'
- `christian-postliberals-integralists`: added 'Anabaptist and plain-church voices (Bruderhof / Plough Quarterly) as a small adjacent current'
- `new-atheist-secular-humanist`: added 'The Satanic Temple (religious-liberty litigation by nontheists)'
- `progressive-christianity`: added 'Unitarian Universalists'
- `meaning-crisis-religious-turn`: added 'Girardians (mimetic theory; Owocki Atlas tribe)'
- `asian-american-voices`: added 'Filipino American, Korean American and Vietnamese American currents'
- `classical-liberal-libertarians`: added 'Western public-lands transfer / 'sagebrush' property-rights advocates (mirror side of hunter-conservationists on federal land sales)'
- `degrowth-post-growth`: added 'minimalism / voluntary simplicity (now its own niche: minimalism-anti-consumerism; Juliet Schor secondary there)'
- `gender-critical-feminism`: added ''Save women's sports' / sex-based sports categories (Riley Gaines; Title IX fights)'
- `sports-talk-culture`: added 'women's sports fandom (WNBA; A Touch More) and its 'Save women's sports' counter-current (Riley Gaines, OutKick)'
- `progress-studies-abundance`: added 'Georgists / land-value tax (Owocki Atlas tribe; one checked voice, Lars Doucet; kept as sub-niche)'
- `crypto-degens`: 'Remilia / Milady' kept as a sub-niche (g7: not promoted).

## 7. Balance audit

### 7.1 By domain (incl. D9)

| Domain | Niches | new in v4 | Landmarks | new in v4 | Verified-active | Female | Bridgers |
|---|---|---|---|---|---|---|---|
| D1 Right | 29 | 1 | 101 | 2 | 71 (70%) | 24% | 27% |
| D2 Left & center | 31 | 2 | 111 | 9 | 89 (80%) | 39% | 30% |
| D3 Tech & futures | 24 | 1 | 81 | 3 | 69 (85%) | 19% | 30% |
| D4 Heterodox & sensemaking | 22 | 1 | 79 | 3 | 64 (81%) | 20% | 28% |
| D5 Religion & spirituality | 30 | 1 | 111 | 3 | 76 (68%) | 23% | 24% |
| D6 Gender, lifestyle & subcultures | 35 | 3 | 109 | 13 | 64 (59%) | 62% | 23% |
| D7 Economy, ecology & place | 27 | 5 | 92 | 13 | 56 (61%) | 30% | 27% |
| D8 Geopolitics & media | 19 | 0 | 70 | 0 | 60 (86%) | 21% | 26% |
| D9 Mainstream culture | 17 | 0 | 63 | 0 | 43 (68%) | 21% | 25% |
| **Total** | 234 | 14 | 817 | 46 | 592 (72%) | 30% | 27% |

### 7.2 Left / right / other (rough QA placement)

| Placement | Niches v3 | Niches v4 | new in v4 | Landmarks v4 |
|---|---|---|---|---|
| Left | 47 | 51 | 4 | 185 |
| Center-left | 22 | 24 | 2 | 87 |
| Center | 9 | 10 | 1 | 35 |
| Center-right | 14 | 16 | 2 | 56 |
| Right | 47 | 47 | 0 | 166 |
| Cross-cutting / off-axis | 81 | 86 | 5 | 288 |

Left + center-left niches: 75; right + center-right: 63; cross-cutting 86; center 10. v4 adds 6 left-leaning, 2 right-leaning, 1 center and 5 cross-cutting niches (the AI backlash and secession niches are cross-party).

### 7.3 Verification, roles and gender

| Status | Landmarks v4 | Share | of which new in v4 | v3 |
|---|---|---|---|---|
| verified-active | 592 | 72% | 32 | 560 |
| pending | 222 | 27% | 14 | 208 |
| stale | 3 | 0% | 0 | 3 |

| Role (primary) | Landmarks | Share | new in v4 |
|---|---|---|---|
| core | 520 | 64% | 29 |
| bridger | 217 | 27% | 13 |
| edge | 80 | 10% | 4 |

| Gender | Landmarks | Share | new in v4 |
|---|---|---|---|
| male | 559 | 68% | 19 |
| female | 247 | 30% | 25 |
| nonbinary | 4 | 0% | 0 |
| mixed | 6 | 1% | 2 |
| unknown | 1 | 0% | 0 |

Women: 30% of landmarks (31% counting mixed-gender duo records). Bridgers: 27% by primary role. Niches whose primary landmarks include no woman: 84 (v3: 83).

### 7.4 Coverage gaps

**Niches with no verified-active primary landmark (11; v3: 9):** Religious-liberty legal movement (`religious-liberty-legal-movement`), ADOS / lineage-based Black politics (`ados-lineage-politics`), Criminal-justice reform & decarceration movement (`criminal-justice-reform-decarceration`), Childfree by choice (`childfree-by-choice`), Mainstream liberal / intersectional feminism (`liberal-feminism`), Men's rights & fathers' rights (shared parenting / family-court reform) (`mens-rights-fathers-rights`), Polyamory, ethical non-monogamy & relationship anarchy (`ethical-non-monogamy`), Sober-curious & alcohol-free movement (`sober-curious-alcohol-free`), Top G / alpha hustle masculinity (`alpha-hustle-masculinity`), Tradwife / traditional femininity (`tradwife-trad-femininity`), Degrowth / post-growth (`degrowth-post-growth`).

**Niches without a verified-active core: 13** (field `has_verified_active_core`); new in v4: Sober-curious & alcohol-free movement.

**Niches lacking a bridger (35; v3: 34)**, counting bridger roles in secondary listings: Daily Wire culture-war conservatives, Immigration restrictionists / border hawks, Pro-immigration libertarians & growth advocates, State sovereignty, secession & 'national divorce' movements, ADOS / lineage-based Black politics, Arab & Muslim American political bloc (Uncommitted to Dearborn), Class-first / heterodox left, Higher-education defenders (academic freedom vs. federal pressure), Reproductive rights / reproductive freedom movement, MAHA coalition (Make America Healthy Again), Astrology mainstream ('astrology twitter'), Esotericism, occultism & Perennialist Traditionalism, Gen Z faith revival (young-adult Christian resurgence), New Age, manifestation & wellness spirituality, New Atheists & secular humanists, Anti-pornography & anti-sexual-exploitation movement, Anti-woke gamer culture, Childfree by choice, Decentering men & single-on-purpose women, Evangelical egalitarians & purity-culture critics, Looksmaxxing & blackpill, Modern dating & relationships mainstream, Neurodivergence & mental-health identity, Protective parents & family-court reform (domestic-violence / child-safety), Sober-curious & alcohol-free movement, Animal rights / vegan, Ecomodernists & nuclear energy abundance, Sound money / Austrian economics / gold & dedollarization, Dissident Military-Analysis Circuit, Pro-Palestinian movement, Black faith-and-family mainstream, Bravo & reality-TV culture, Daytime & lifestyle mainstream (Oprah-sphere & morning shows), Pop culture, celebrity & stan culture, Therapeutic & self-help mainstream (therapy culture).
If edge may count as bridger, 19 remain: Daily Wire culture-war conservatives, State sovereignty, secession & 'national divorce' movements, ADOS / lineage-based Black politics, Higher-education defenders (academic freedom vs. federal pressure), Reproductive rights / reproductive freedom movement, MAHA coalition (Make America Healthy Again), Gen Z faith revival (young-adult Christian resurgence), Anti-pornography & anti-sexual-exploitation movement, Anti-woke gamer culture, Childfree by choice, Evangelical egalitarians & purity-culture critics, Modern dating & relationships mainstream, Neurodivergence & mental-health identity, Protective parents & family-court reform (domestic-violence / child-safety), Sober-curious & alcohol-free movement, Ecomodernists & nuclear energy abundance, Dissident Military-Analysis Circuit, Daytime & lifestyle mainstream (Oprah-sphere & morning shows), Therapeutic & self-help mainstream (therapy culture).

### 7.5 Mirror pairs

53 pairs (46 from v3, 7 new). New pairs:

| Side A | Side B | Arena |
|---|---|---|
| Red Pill dating / sexual market value | Decentering men & single-on-purpose women | opting out of the other sex (MGTOW vs. decentering men) |
| Looksmaxxing & blackpill | Wellness girlies: 'that girl' self-optimization & hormone health | self-optimization (men's vs. women's parallel; not opponents) |
| Hustle culture / finfluencer grindset | Minimalism & anti-consumerism (no-buy, deinfluencing) | consumption & status |
| 'The boys' culture: Barstool, Nelk & sports-betting bro media | Sober-curious & alcohol-free movement | drinking culture |
| Tech right / Silicon Valley New Right | Populist AI backlash (anti-transhumanist right & AI-accountability coalition) | AI regulation, preemption & data centers |
| Rural populist / independent farmer movement | Farm-and-ranch mainstream (ag media & farm YouTube) | farm policy & agribusiness consolidation |
| Medical freedom / vaccine-injury movement | COVID-conscious & long-COVID community | COVID precautions & long COVID |

New issue exceptions: State sovereignty, secession & 'national divorce' movements: Horseshoe niche (TEXIT right, Calexit/Cascadia left); its foil is national unity carried by both party niches.; Tribal nations & Native politics (sovereignty within the federal system): Constituency niche; its argument with Land Back (within vs. outside the federal system) is an internal split, not a mirror. Unpaired after the check: none.

### 7.6 Landmarks per niche

| Primary landmarks per niche | Niches |
|---|---|
| 2 | 23 |
| 3 | 111 |
| 4 | 62 |
| 5 | 38 |

## 8. g8 coverage matrix summary

g8 mapped SEED-v3 (plus its own new niches) against 7 outside taxonomies. Counts parsed from `raw/g8-holistic-sweep.md` §1; 'still a gap' is any row marked GAP without a v4 fix.

| Outside taxonomy | Categories | mapped to niche(s) | gap closed by v4 niche | gap closed by v4 sub-niche/landmark | sub-niche only | covered by g7 | no niche needed (fails bar) | excluded by design | still a gap |
|---|---|---|---|---|---|---|---|---|---|
| 1a. Limberg & Barnes 2018, all 33 tribes (from their public spreadsheet) | 33 | 31 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1b. Owocki Atlas (39 of 58 names known) | 39 | 29 | 1 | 1 | 8 | 0 | 0 | 0 | 0 |
| 1c. Pew political typology (2021; the latest typology, per Pew) | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1d. More in Common "Hidden Tribes" (2018) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1e. Pew Religious Landscape categories | 15 | 12 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1f. US social movements (Wikipedia list, main entries) | 19 | 14 | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| 1g. Identity communities | 32 | 19 | 4 | 1 | 5 | 0 | 1 | 0 | 2 |
| **Total** | 154 | 121 | 7 | 4 | 17 | 1 | 1 | 1 | 2 |

**154 external categories: 150 covered (of which 11 were gaps closed in v4), 2 still gaps, 2 excluded or not needed.** Remaining gaps: older Americans / boomers (fails the bar), Iranian American diaspora (unchecked); the 19 unknown Owocki Atlas names are outside the matrix. Neo-Nazis are excluded by design.

## 9. Content hygiene

- Gap-file flag texts on landmarks: 0 found (none carried; flags set only from decisions_v4).
- Private-vault citations removed: 0.
- Residual keyword scan of new niches/records (6 hits), all reviewed: `sober-curious-alcohol-free`.notes 'addiction'; `covid-conscious-long-covid`.description 'illness'; `covid-conscious-long-covid`.notes 'Death'; `covid-conscious-long-covid`.notes 'Death'; `shane-claiborne`.why 'death'; `beatrice-adler-bolton-artie-vierkant`.why 'Death'. They are topic words (addiction as a policy frame, chronic illness as the niche's subject, the Death Panel show name, the death penalty as a campaign issue); none is a personal allegation, health or conduct claim about a seeded person. The secession niche's sovereign-citizen sub-niche label notes the FBI's public view of that movement (descriptive, no person named).
- Ages: Kareem Shami adult per the Guardian (2024, aged 22). No minors, private individuals or designated-organization spokespeople added.

## 10. Remaining TODO gaps

- **Older Americans / retirees** (fails the bar; v3 and g8 agree).
- **Iranian American diaspora** (regime-change vs. anti-war split; D8): unchecked.
- **Jewish secular / cultural voices** (Tablet's Unorthodox): unchecked.
- **Public-lands transfer side**: sub-niche only; needs a long-form voice before it can mirror hunter-conservationists.
- **Occupational cultures**: nurses/healthcare workers, truckers, first responders (sub-niches only).
- **Black women's 'leveling up' / divestment** (Christelyn Karazin): re-check; may meet the bar.
- **AI-companion users**: strong candidate for promotion once adult public voices from the user side exist.
- **'Save women's sports'**: if a second verified voice is found (Paula Scanlan, Payton McNabb), consider a small niche.
- **Woman core voices** for markets-investing (CNBC/macro) and a Southern Black farmer with long-form output for Black agrarianism.
- **g7 unverified candidates**: Eric Garcia, Ari Ne'eman (neurodivergence), Emmeline Clein, Christy Harrison (fat liberation), Christelyn Karazin (in VERIFICATION-QUEUE-v4.json).
- **Pending in v4**: Amanda Montei & Tracy Clark-Flory (Dire Straights), Annie Grace, Bella DePaulo, Holly Whitaker, Joe Allen, Julia Doubleday, Karen Washington, Liz Moody, Marcus Ruiz Evans, Matt D'Avella, Shane Claiborne, Simran Jeet Singh, Tyne Morgan, William Costello.
- Unchanged v3 TODOs: 19 unknown Atlas names; Puerto Rico statehood; Black Hebrew Israelites; Korean and Vietnamese evangelicals; Spanish-language media depth; WNBA fandom niche.

## 11. Verification queue

`VERIFICATION-QUEUE-v4.json` holds **225 landmarks** (pending or stale; 14 new in v4), grouped by domain, cores first: D1 Right 30, D2 Left & center 22, D3 Tech & futures 12, D4 Heterodox & sensemaking 15, D5 Religion & spirituality 35, D6 Gender, lifestyle & subcultures 45, D7 Economy, ecology & place 36, D8 Geopolitics & media 10, D9 Mainstream culture 20. By role: {'core': 108, 'bridger': 72, 'edge': 45}. Spot-checks: 98 (8 new in v4: Brad Carson, Chip Flory, Daniel Miller, Guerline Jozef, Leah Penniman, Mark Trahant, Matt Hildreth, Silas House). Also lists alternates, the held-out record and g7's unverified candidates.

## Searches used

7 WebSearch and 4 WebFetch calls (budget ≤10 searches): WebSearch: Riley Gaines podcast OutKick 2026; WebSearch: Death Panel podcast 2026; WebSearch: COVID-conscious community 2026 (masking, long COVID); WebSearch: Julia Doubleday The Gauntlet 2026; WebSearch: Courtney Carver Project 333 2026; WebSearch: no-buy / deinfluencing women creators 2026; WebSearch: The Minimal Mom Dawn Madsen 2026; WebFetch: Apple Podcasts: Death Panel; WebFetch: Zeno: Still Here (The Sick Times) episode; WebFetch: Apple Podcasts: The Minimal Mom; WebFetch: creatordb: The Minimal Mom.
