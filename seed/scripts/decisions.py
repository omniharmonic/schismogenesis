"""All human QA decisions for SEED-v1, kept as data so the build is reproducible."""

# old niche_id -> surviving niche_id (niches not listed survive under their own id)
NICHE_MERGE = {
  # MAHA (D1/D4/D7/Atlas)
  'maha-coalition': 'maha-coalition-wellness', 'maha-wellness-politics': 'maha-coalition-wellness',
  # America First restraint (D1/D8) + paleocons
  'tucker-sphere-america-first-restraint': 'america-first-restraint',
  'america-first-non-interventionists': 'america-first-restraint',
  'paleoconservatives': 'america-first-restraint',
  # hawks (D1/D8)
  'reagan-hawks-pro-israel': 'peace-through-strength-hawks',
  'neoconservative-pro-israel-hawks': 'peace-through-strength-hawks',
  # Bulwark / Never-Trump (D1/D2)
  'bulwark-ex-conservatives': 'never-trump-bulwark', 'never-trump-converted-center': 'never-trump-bulwark',
  # neoreaction/vitalist (D1/D3/D6)
  'vitalist-online-right': 'neoreaction-vitalist-right', 'vitalist-right-masculinity': 'neoreaction-vitalist-right',
  # Christian nationalism (D1/D5)
  'christian-nationalists': 'christian-nationalism', 'reformed-christian-nationalism': 'christian-nationalism',
  # postliberals/integralists (D1/D5)
  'catholic-integralists': 'christian-postliberals-integralists',
  'christian-postliberal-integralist': 'christian-postliberals-integralists',
  # regens (D3/D7)
  'regen-crypto': 'regens-refi', 'regenerative-finance-refi': 'regens-refi',
  # nuclear/ecomodernism (D3/D7)
  'energy-abundance-nuclear': 'ecomodernism-nuclear-abundance', 'ecomodernism-pro-nuclear': 'ecomodernism-nuclear-abundance',
  # free speech (D2/D4)
  'free-speech-anti-censorship': 'free-speech-civil-libertarians', 'civil-liberties-legal-left': 'free-speech-civil-libertarians',
  # D8 populist new media duplicated D4 niches
  'corporate-media-critics-populist-new-media': 'populist-horseshoe-anti-establishment',
  # Free Press (D4/D8)
  'free-press-institutional-heterodox': 'free-press-heterodox-institutional',
  'heterodox-institution-builders': 'free-press-heterodox-institutional',
  # anti-disinformation field (D2/D8/D4)
  'speech-skeptical-anti-disinfo-left': 'anti-disinformation-field',
  'disinformation-research-trust-safety': 'anti-disinformation-field',
  # class-first / heterodox left (D2/D4)
  'class-first-anti-woke-left': 'class-first-heterodox-left', 'heterodox-left': 'class-first-heterodox-left',
  # Palestine (D2/D8) - D2 niche dissolved
  'palestine-solidarity-left': 'pro-palestinian-movement',
  # anti-imperialist (D2/D8)
  'marxist-leninist-left': 'anti-imperialist-ml-left', 'anti-imperialist-left': 'anti-imperialist-ml-left',
  # moderate Dems
  'popularists-moderate-democrats': 'moderate-centrist-democrats', 'neoliberal-centrist-democrats': 'moderate-centrist-democrats',
  # anti-Trump liberal media
  'liberal-institutionalists-resistance': 'anti-trump-liberal-media', 'fight-mode-democratic-creators': 'anti-trump-liberal-media',
  # Black liberal commentariat
  'black-political-commentariat': 'black-liberal-commentariat', 'racial-justice-antiracist': 'black-liberal-commentariat',
  # LGBTQ (D2/D6)
  'lgbtq-political-organizing': 'lgbtq-trans-rights', 'trans-rights-advocacy': 'lgbtq-trans-rights',
  # meaning crisis (D4/D5)
  'meaning-crisis-wisdom': 'meaning-crisis-religious-turn', 'christianity-curious-meaning-crisis': 'meaning-crisis-religious-turn',
  # metacrisis (D4/D7)
  'metacrisis-sensemaking': 'metacrisis-great-simplification', 'collapse-aware-great-simplification': 'metacrisis-great-simplification',
  # sacred economics dissolved
  'sacred-economics-eco-spiritual': 'bioregionalism-regenerative-culture',
  # thin D6 niches
  'mens-rights-mgtow': 'mens-boys-advocacy', 'healthy-masculinity': 'mens-boys-advocacy',
  '4b-decentering-men': 'liberal-feminism',
  'anti-work-lying-flat': 'gen-z-disaffection', 'gen-z-irony-brainrot': 'gen-z-disaffection',
  # D7 consolidations
  'food-freedom-raw-milk': 'regen-ag-food-freedom', 'regenerative-agriculture': 'regen-ag-food-freedom',
  'strong-towns-urbanism': 'urbanism-strong-towns-car-free', 'car-free-urbanism-media': 'urbanism-strong-towns-car-free',
  # conspiracy media (D1/D4)
  'patriot-conspiracy-media': 'conspiracy-realist-truther', 'conspiracy-realist-dyor': 'conspiracy-realist-truther',
  # libertarians (D1/D8)
  'paleolibertarians-mises': 'paleolibertarian-antiwar', 'libertarian-anti-war': 'paleolibertarian-antiwar',
  # foreign-policy establishment
  'democratic-foreign-policy-establishment': 'foreign-policy-establishment',
  'national-security-establishment-centrists': 'foreign-policy-establishment',
  # religion D5
  'religious-nones-sbnr': 'post-religious-deconstruction-nones', 'post-religious-deconstruction': 'post-religious-deconstruction-nones',
  # tech critics D3
  'neo-luddites': 'neo-luddites-anti-ai-creatives', 'anti-ai-creatives': 'neo-luddites-anti-ai-creatives',
}

# surviving niche -> (base raw niche whose fields are copied, name, domain, cross_domains, decision text)
MERGED_META = {
 'maha-coalition-wellness': ('maha-wellness-politics', 'MAHA coalition (Make America Healthy Again)', 'd4-heterodox-sensemaking', ['d1-right','d7-economy-ecology-place'],
   'D1 political MAHA + D4 wellness MAHA describe one coalition with the same sacred values (children\'s health, food, distrust of captured regulators); the split was governing wing vs influencer wing (style). Medical freedom kept separate (consent/vaccines are a different sacred value; the two argue over priorities). Food freedom sits in regen-ag. Atlas: "MAHA & health freedom".'),
 'america-first-restraint': ('tucker-sphere-america-first-restraint', 'America First restraint right (Tucker-sphere)', 'd1-right', ['d8-geopolitics-media'],
   'D1 Tucker-sphere and D8 America First non-interventionists are the same people and worldview. Paleoconservatives (Gottfried, McCarthy; low longform) folded in as a sub-niche because in 2025-26 their public conversation runs through The American Conservative / restraint media. Split from hawks kept: the 2026 Iran war (VERIFIED) is a fight over fundamentals.'),
 'peace-through-strength-hawks': ('neoconservative-pro-israel-hawks', 'Peace-through-strength hawks / pro-Israel conservatives', 'd8-geopolitics-media', ['d1-right'],
   'D1 Reagan hawks and D8 neocon hawks are one niche (same sacred values: US primacy, Israel alliance); Levin core in both.'),
 'never-trump-bulwark': ('never-trump-converted-center', 'Never-Trump / Bulwark converted center', 'd2-left-center', ['d1-right'],
   'D1 and D2 both listed Bulwark with the same cores. Homed in D2 because its 2025-26 political role is inside the anti-Trump coalition; Dispatch center-right stays in D1 (it remains on the right - a sacred-value difference).'),
 'neoreaction-vitalist-right': ('vitalist-online-right', 'Neoreaction & vitalist dissident right', 'd1-right', ['d3-tech-futures','d6-gender-lifestyle-subcultures'],
   'D1 and D6 vitalist niches were duplicates. Neither D1 nor D3 had placed Curtis Yarvin/neoreaction (each deferred to the other) - gap filled here; the tech right (Thiel, Sacks) stays a separate D3 niche because its sacred value is building/markets, not post-democratic sovereignty. Atlas: "neoreaction & the new right".'),
 'christian-nationalism': ('christian-nationalists', 'Christian nationalism (self-identified; Moscow-style Reformed)', 'd1-right', ['d5-religion-spirituality'],
   'D1 and D5 described the same movement and people (Wilson, Wolfe, Webbon). One niche, homed D1 for its political telos, with postmillennial theology as sub-niche. NAR voices (Wallnau) homed in charismatic-pentecostal.'),
 'christian-postliberals-integralists': ('christian-postliberal-integralist', 'Christian postliberals & Catholic integralists', 'd5-religion-spirituality', ['d1-right'],
   'D1 integralists + D5 postliberals share sacred values (common good ordered to the Church/Christian tradition). National conservatism (Hazony, Cass, Vance) kept separate in D1: its sacred value is the nation, not the Church.'),
 'regens-refi': ('regenerative-finance-refi', 'Regens / ReFi & public-goods funding', 'd7-economy-ecology-place', ['d3-tech-futures'],
   'D3 regen crypto and D7 ReFi had identical cores (Owocki, Landua). Homed D7 for its ecological telos. Neutrality note: author-proximate scene; external review advised.'),
 'ecomodernism-nuclear-abundance': ('ecomodernism-pro-nuclear', 'Ecomodernists & nuclear energy abundance', 'd7-economy-ecology-place', ['d3-tech-futures'],
   'D3 energy-abundance/nuclear and D7 ecomodernism share sacred values (abundant clean energy, nuclear); Boemeke core in both. Energy dominance / climate-skeptic right kept separate (does not treat decarbonization as a goal).'),
 'free-speech-civil-libertarians': ('free-speech-anti-censorship', 'Free-speech civil libertarians (FIRE / ACLU tradition)', 'd4-heterodox-sensemaking', ['d2-left-center'],
   'D2 civil-liberties left and D4 free-speech niche differ only in partisan style; both hold viewpoint-neutral speech protection sacred. Censorship-industrial-complex critics kept separate: their frame is a state-NGO censorship apparatus and they align with the 2025-26 administration, a different threat model.'),
 'populist-horseshoe-anti-establishment': ('populist-horseshoe-anti-establishment', 'Left-right populist anti-establishment media (Breaking Points sphere)', 'd4-heterodox-sensemaking', ['d8-geopolitics-media'],
   'D8 corporate-media critics (Ball, Enjeti, Greenwald) was a duplicate of D4 horseshoe + independent journalism; absorbed.'),
 'free-press-heterodox-institutional': ('free-press-institutional-heterodox', 'The Free Press / heterodox institution-builders', 'd4-heterodox-sensemaking', ['d8-geopolitics-media'],
   'D4 and D8 described the same project. Kept separate from independent adversarial journalism (Greenwald/Taibbi): the camps now disagree on fundamentals (re-entering legacy institutions via CBS; Israel/war).'),
 'anti-disinformation-field': ('disinformation-research-trust-safety', 'Anti-disinformation / information-integrity field', 'd8-geopolitics-media', ['d2-left-center','d4-heterodox-sensemaking'],
   'D2 speech-skeptical left and D8 disinfo-research field share cores (Jankowicz, DiResta) and sacred values; merged, homed D8 (media axis).'),
 'class-first-heterodox-left': ('class-first-anti-woke-left', 'Class-first / heterodox left', 'd2-left-center', ['d4-heterodox-sensemaking'],
   'D2 class-first and D4 heterodox left shared deBoer as core and the same critique (class over identity); style difference only.'),
 'anti-imperialist-ml-left': ('anti-imperialist-left', 'Anti-imperialist & Marxist-Leninist left', 'd2-left-center', ['d8-geopolitics-media'],
   'D2 ML left (PSL) and D8 anti-imperialist left (CODEPINK, Grayzone) share the anti-imperialist, campist sacred value and overlapping personnel. Left restraint (Drop Site, American Prestige) kept separate: it rejects campism.'),
 'moderate-centrist-democrats': ('popularists-moderate-democrats', 'Moderate / centrist Democrats (popularists & neoliberals)', 'd2-left-center', [],
   'Popularists and pro-market neoliberals act as one faction in 2025-26 (WelcomeFest, Majority Democrats) and differ mainly in emphasis. Abundance liberals kept separate (state-capacity sacred value, distinct combatants).'),
 'anti-trump-liberal-media': ('liberal-institutionalists-resistance', 'Anti-Trump liberal media (institutionalists & fight-mode creators)', 'd2-left-center', [],
   'D2 itself flagged the institutionalist vs fight-mode split as possibly style only; merged with sub-niches.'),
 'black-liberal-commentariat': ('black-political-commentariat', 'Black liberal commentariat & racial-justice movement', 'd2-left-center', [],
   'Racial-justice/anti-racist intellectuals and the Black liberal media commentariat share sacred values; the racial-justice niche was declining institutionally and thin. ADOS kept separate (lineage vs coalition is a fundamental dispute).'),
 'lgbtq-trans-rights': ('trans-rights-advocacy', 'LGBTQ+ & trans rights advocacy', 'd6-gender-lifestyle-subcultures', ['d2-left-center'],
   'D2 organizing and D6 advocacy niches shared Erin Reed as core and the same sacred values.'),
 'meaning-crisis-religious-turn': ('christianity-curious-meaning-crisis', 'Meaning crisis & the religious turn', 'd5-religion-spirituality', ['d4-heterodox-sensemaking'],
   'D4 meaning-crisis (Vervaeke) and D5 Christianity-curious revival (Peterson, Douthat, Holland) are one conversational cluster - the same people appear on each other\'s shows. The theist vs non-theist dispute is kept as sub-niches rather than two niches. Pageau homed in Orthodox convert wave.'),
 'metacrisis-great-simplification': ('metacrisis-sensemaking', 'Metacrisis / Great Simplification (liminal web core)', 'd4-heterodox-sensemaking', ['d7-economy-ecology-place'],
   'D4 metacrisis and D7 collapse-aware niches had the same two cores (Schmachtenberger, Hagens). Author-proximate scene; external review advised.'),
 'bioregionalism-regenerative-culture': ('bioregionalism-regenerative-culture', 'Bioregionalism & regenerative culture', 'd7-economy-ecology-place', [],
   'D7 sacred-economics niche dissolved: Eisenstein homed in awakening/sovereignty spirituality (his 2024-26 output and RFK-adjacent audience), Akomolafe moved here. Author-proximate scene; external review advised.'),
 'mens-boys-advocacy': ('healthy-masculinity', "Men & boys' advocacy (healthy masculinity & men's issues)", 'd6-gender-lifestyle-subcultures', [],
   "MGTOW/men's-rights niche was thin (2 landmarks; Sandman unverified persona). Warren Farrell moved here - he and Reeves share the boys'-crisis frame. MGTOW kept as a sub-niche of red-pill dating."),
 'liberal-feminism': ('liberal-feminism', 'Mainstream liberal / intersectional feminism', 'd6-gender-lifestyle-subcultures', [],
   '4B / decentering men (2 landmarks, mostly anonymous TikTok, declining) folded in as a sub-niche; Hope Woodard kept as edge.'),
 'gen-z-disaffection': ('gen-z-irony-brainrot', 'Gen Z disaffection: irony, doomer & lying-flat culture', 'd6-gender-lifestyle-subcultures', [],
   'Anti-work / lying flat (2 landmarks) merged with Gen Z irony/doomer culture: both are withdrawal-from-the-system stances with shared audiences.'),
 'regen-ag-food-freedom': ('regenerative-agriculture', 'Regenerative agriculture & food freedom', 'd7-economy-ecology-place', ['d4-heterodox-sensemaking'],
   'Food freedom / raw milk overlapped regen ag (Salatin core in both) and MAHA; merged as a sub-niche.'),
 'urbanism-strong-towns-car-free': ('strong-towns-urbanism', 'Urbanism: Strong Towns & car-free media', 'd7-economy-ecology-place', [],
   'Strong Towns and car-free urbanism media share sacred values (walkable, fiscally resilient places) and cross-appear; difference is style/audience.'),
 'conspiracy-realist-truther': ('conspiracy-realist-dyor', 'Conspiracy-realist & patriot truther media', 'd4-heterodox-sensemaking', ['d1-right'],
   'D1 patriot/truther media and D4 conspiracy-realist ecosystem share Alex Jones and the same epistemics; with Infowars ended (VERIFIED, ~30 Apr 2026) the D1 niche was declining. Merged.'),
 'paleolibertarian-antiwar': ('paleolibertarians-mises', 'Paleolibertarians / Mises Caucus & libertarian anti-war', 'd1-right', ['d8-geopolitics-media'],
   'D1 Mises Caucus and D8 libertarian anti-war shared Dave Smith and Scott Horton; style difference only.'),
 'foreign-policy-establishment': ('democratic-foreign-policy-establishment', 'Foreign-policy establishment (Democratic & nonpartisan)', 'd8-geopolitics-media', ['d2-left-center'],
   'Democratic FP establishment and nonpartisan national-security centrists share sacred values (alliances, expertise, stability); difference is partisanship. Liberal-internationalist democracy defenders kept separate (moralized democracy-vs-autocracy frame, pro-Ukraine hawkishness).'),
 'post-religious-deconstruction-nones': ('post-religious-deconstruction', 'Deconstruction, nones & post-religious life', 'd5-religion-spirituality', [],
   'Religious nones/SBNR niche had 2 landmarks (one an analyst rather than a voice); merged with deconstruction.'),
 'neo-luddites-anti-ai-creatives': ('neo-luddites', 'Neo-Luddites & anti-AI creative labor', 'd3-tech-futures', [],
   'Neo-Luddite critics and anti-AI artists share the sacred value of labor/craft over automation and cross-appear (Merchant covers creative workers). AI-ethics academics and hype skeptics kept separate.'),
 'pro-palestinian-movement': ('pro-palestinian-movement', 'Pro-Palestinian movement', 'd8-geopolitics-media', ['d2-left-center'],
   'D2 Palestine-solidarity niche dissolved: its people were all also in D8 (Hasan -> pro-Palestinian; Grim, Scahill -> left restraint; Beinart -> Jewish non-Zionist).'),
}

# landmark_id -> surviving niche (primary). Used for cross-domain duplicates and deliberate moves.
PRIMARY = {
 'abigail-shrier':'gender-medicine-skeptics','albert-mohler':'reformed-tgc','alex-clark':'turning-point-movement',
 'alex-epstein':'energy-dominance-climate-skeptic','alex-jones':'conspiracy-realist-truther','alex-o-connor':'apologetics-debate-culture',
 'aubrey-marcus':'conspirituality-sovereignty','bari-weiss':'free-press-heterodox-institutional','ben-norton':'multipolarity-global-south',
 'bill-kristol':'liberal-internationalist-democracy-defenders','brendan-graham-dempsey':'metamodernism','brian-atlas':'red-pill-dating',
 'bronze-age-pervert':'neoreaction-vitalist-right','bryan-johnson':'longevity-transhumanists','calley-means':'maha-coalition-wellness',
 'candace-owens':'conspiracy-realist-truther','chad-pecknold':'christian-postliberals-integralists','charles-eisenstein':'conspirituality-sovereignty',
 'cory-doctorow':'open-source-digital-rights','curt-mills':'america-first-restraint','daniel-schmachtenberger':'metacrisis-great-simplification',
 'dave-smith':'paleolibertarian-antiwar','david-french':'dispatch-center-right','del-bigtree':'medical-freedom-vaccine-sceptic',
 'derek-thompson':'abundance-liberals','douglas-murray':'free-press-heterodox-institutional','eli-lake':'peace-through-strength-hawks',
 'erin-reed':'lgbtq-trans-rights','freddie-deboer':'class-first-heterodox-left','freya-india':'reactionary-feminism',
 'glenn-greenwald':'independent-anti-establishment-journalism','gregory-landua':'regens-refi','hannah-neeleman':'tradwife-trad-femininity',
 'isabelle-boemeke':'ecomodernism-nuclear-abundance','jay-shetty':'new-age-manifestation-wellness','jeremy-scahill':'left-restraint-foreign-policy',
 'jesse-singal':'gender-medicine-skeptics','joel-salatin':'regen-ag-food-freedom','joel-webbon':'christian-nationalism',
 'john-vervaeke':'meaning-crisis-religious-turn','jonathan-haidt':'humane-tech-attention-critics','jonathan-pageau':'orthodox-convert-wave',
 'kevin-owocki':'regens-refi','krystal-ball':'populist-horseshoe-anti-establishment','lance-wallnau':'charismatic-pentecostal',
 'laura-loomer':'maga-loyalist-media','lyn-alden':'bitcoin-maximalists','marc-elias':'democracy-protection-voting-rights',
 'marjorie-taylor-greene':'america-first-restraint','mark-levin':'peace-through-strength-hawks','matt-stoller':'anti-monopoly-neo-brandeisian',
 'matt-taibbi':'independent-anti-establishment-journalism','megyn-kelly':'america-first-restraint','mehdi-hasan':'pro-palestinian-movement',
 'michael-shellenberger':'censorship-industrial-complex-critics','mike-lindell':'election-integrity-fraud-concern',
 'nate-hagens':'metacrisis-great-simplification','nina-jankowicz':'anti-disinformation-field','patrick-deneen':'christian-postliberals-integralists',
 'paul-kingsnorth':'orthodox-convert-wave','peter-attia':'fitness-biohacking','peter-beinart':'jewish-anti-zionist-non-zionist-left',
 'peter-singer':'animal-rights-vegan','raw-egg-nationalist':'neoreaction-vitalist-right','renee-diresta':'anti-disinformation-field',
 'robert-f-kennedy-jr':'maha-coalition-wellness','robin-hanson':'forecasters-prediction-markets','ryan-grim':'left-restraint-foreign-policy',
 'saagar-enjeti':'populist-horseshoe-anti-establishment','sam-harris':'new-atheist-secular-humanist','sarah-longwell':'never-trump-bulwark',
 'scott-horton':'paleolibertarian-antiwar','sneako':'groypers-america-first','sohrab-ahmari':'christian-postliberals-integralists',
 'stephen-wolfe':'christian-nationalism','steve-bannon':'war-room-populist-nationalists','tim-miller':'never-trump-bulwark',
 'tucker-carlson':'america-first-restraint',
 # deliberate single-occurrence moves
 'lars-doucet':'progress-studies-abundance','alex-cooper':'modern-dating-mainstream','bayo-akomolafe':'bioregionalism-regenerative-culture',
 'warren-farrell':'mens-boys-advocacy','red-scare':'dirtbag-left',
}
EXTRA_SECONDARY = {'lars-doucet':['urbanism-strong-towns-car-free'],'alex-cooper':['liberal-feminism'],
  'charles-eisenstein':['bioregionalism-regenerative-culture'],'red-scare':['gen-z-disaffection','class-first-heterodox-left'],
  'swami-sarvapriyananda':['hindu-american-voices'],'curt-mills':[],'jonathan-pageau':['meaning-crisis-religious-turn']}

ROLE_OVERRIDE = {  # landmark_id -> role in primary niche
 'curt-mills':'core','megyn-kelly':'bridger','marjorie-taylor-greene':'bridger','candace-owens':'core','alex-jones':'core',
 'mark-levin':'core','eli-lake':'bridger','douglas-murray':'bridger','renee-diresta':'core','robert-f-kennedy-jr':'core',
 'charles-eisenstein':'core','warren-farrell':'bridger','alex-cooper':'core','lars-doucet':'bridger','bayo-akomolafe':'bridger',
 'jesse-singal':'bridger','sneako':'bridger','michael-shellenberger':'core','freddie-deboer':'core','red-scare':'edge',
 'hope-woodard':'edge','gabrielle-judge':'edge','anne-helen-petersen':'bridger','sally-fallon-morell':'core','paul-saladino':'edge',
 'chad-pecknold':'core','sohrab-ahmari':'bridger','robin-hanson':'edge','joel-webbon':'edge','nate-hagens':'core',
}

# name alias normalisation (raw name key -> landmark_id)
ALIAS = {'anna-khachiyan':'red-scare','dasha-nekrasova-anna-khachiyan':'red-scare','douglas-wilson':'doug-wilson',
         'bronze-age-pervert-costin-alamariu':'bronze-age-pervert'}
DISPLAY_NAME = {'red-scare':'Red Scare (Dasha Nekrasova & Anna Khachiyan)','doug-wilson':'Douglas Wilson'}

# landmark drops: id -> reason
DROP = {
 'androgenic': 'HELD OUT: age unconfirmed in a niche dense with minors (brief excludes under-18s). Re-add only after age >=18 is verified.',
 'sandman': 'MGTOW persona, unverified and thin; MGTOW reduced to a sub-niche.',
 'gladden-pappin': 'Low longform; niche has stronger talkers (Pecknold, Deneen, Ahmari).',
 'paul-gottfried': 'Low longform; paleocon niche merged into America First restraint (cap 5).',
 'daniel-mccarthy': 'Paleocon niche merged; cap 5 reached by higher-output voices.',
 'joyce-vance': 'Merged anti-Trump liberal media niche over cap; legal commentary well covered by Elias/Hasen.',
 'gavin-newsom': 'Merged niche over cap; elected official - kept as alternate (high podcast output; re-add if a Democratic 2028-field niche is created).',
 'david-shor': 'Merged moderate-Dem niche over cap; medium output, unverified.',
 'liam-kerr': 'Low longform; merged niche over cap.',
 'deray-mckesson': 'Merged Black commentariat niche over cap.',
 'angela-rye': 'Merged Black commentariat niche over cap (alternate).',
 'jordan-hall': 'Merged metacrisis niche over cap; unverified.',
 'rachel-donald': 'Merged metacrisis niche over cap (alternate).',
 'mark-mcafee': 'Low longform; food freedom folded into regen ag.',
 'blake-chastain': 'Merged deconstruction/nones niche over cap; unverified.',
 'alexander-mercouris': 'Non-US, unverified; dissident circuit retains Macgregor, Davis, Johnson.',
 'richard-haass': 'Merged FP establishment niche over cap; unverified.',
 'alexa-vargas': '4B niche folded into liberal feminism; low output, unverified.',
 'ross-barkan': 'Low longform (text-heavy); merged class-first niche over cap.',
 'alejandra-caraballo': 'Low longform; merged LGBTQ niche over cap.',
 'daniel-herriges': 'Merged urbanism niche over cap.',
 'jeff-emmett': 'Low longform; merged regens niche (author-proximate) kept lean.',
 'harleen-kaur': 'Low longform, unverified; niche keeps two verified high-output cores. (Alternate.)',
}

# NEW niches (gap fills) and NEW landmarks are in gapfill.py
