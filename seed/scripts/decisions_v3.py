"""All human QA decisions for SEED-v3, kept as data so build_v3.py is reproducible.

Inputs: SEED-v2.json (base, unchanged) + raw/g1..g5 (new niches) + raw/g6 (edits to existing niches)
+ the small step-3 gap fill below (12 web searches, 2026-10-31).
Author of record: Benjamin Life (@omniharmonic).
"""
TODAY = '2026-10-31'
WINDOW = '2025-10-31'   # v2 rule: verified-active needs a dated item on/after this date
CAP = 5                 # max primary landmarks per niche (SEED-BRIEF)

GAP_FILES = ['g1-issue-arenas', 'g2-gen-z', 'g3-mainstream-culture', 'g4-political-subcultures', 'g5-gender-family']

# --------------------------------------------------------------------------------------------
# 1. Niche merges among gap files (gap niche_id -> surviving niche_id).  'base' supplies the text.
# --------------------------------------------------------------------------------------------
NICHE_MERGE = {
    'barstool-bro-culture': 'barstool-boys-culture',
    'streamer-irl-culture': 'streamer-creator-culture',
    'lgbt-conservatives-gay-right': 'gay-conservatives-lgb-dissenters',
    'disability-justice': 'disability-rights-justice',
    'military-veteran-culture': 'veteran-warrior-culture-media',
    'veteran-operator-sphere': 'veteran-warrior-culture-media',
}
MERGED_META = {  # surviving id -> (base gap niche_id, display name, home domain, cross_domains, decision)
    'barstool-boys-culture': ('barstool-boys-culture', "'The boys' culture: Barstool, Nelk & sports-betting bro media",
        'd9-mainstream-culture', [],
        "g2 'The boys' (Barstool/Nelk/gambling) and g3 Barstool/'Stoolies' are one scene with the same people (Portnoy core in both) "
        "and the same outlook (irreverent anti-gatekeeper fun, betting, loyalty to 'the boys'); merged. g3's Barstool landmarks "
        "(Big Cat, PFT Commenter) join g2's Nelk/Flagrant voices; capped at 5. Sports betting is a sub-niche here."),
    'streamer-creator-culture': ('streamer-irl-culture', 'Streamer & IRL creator culture',
        'd9-mainstream-culture', [],
        "g2 'Streamer & IRL creator culture' and g3 'Streamer & creator culture' describe the same scene (Kai Cenat core in both); "
        "merged under g2's text with g3's Pokimane and Ludwig Ahgren added. All five landmarks are adults by documented birth year."),
    'gay-conservatives-lgb-dissenters': ('gay-conservatives-lgb-dissenters', 'Gay conservatives & LGB dissenters (the gay right)',
        'd6-gender-lifestyle-subcultures', ['d1-right'],
        "g4 'LGBT conservatives / gay right' and g5 'Gay conservatives & LGB dissenters' share Sullivan and Polumbo and the same "
        "sacred values (gay equality achieved; scepticism of gender-identity politics); merged. Homed in D6 next to its mirror "
        "(LGBTQ+ & trans rights) with D1 cross-listed. Sullivan is the bridger (Dishcast hosts left and right)."),
    'disability-rights-justice': ('disability-rights-justice', 'Disability rights & disability justice',
        'd6-gender-lifestyle-subcultures', [],
        "g1 and g4 seeded the same niche with the same three people. Merged; the rights (ADA/inclusion, legal-liberal) vs. justice "
        "(intersectional, Sins Invalid lineage, anti-ableist/anti-capitalist) distinction is kept as sub-niches, since members "
        "debate it but share sacred values (access, self-representation, 'nothing about us without us')."),
    'veteran-warrior-culture-media': ('veteran-warrior-culture-media', 'Veteran & warrior-culture sphere',
        'd9-mainstream-culture', ['d6-gender-lifestyle-subcultures', 'd8-geopolitics-media'],
        "Three agents seeded veterans (g1 warrior-culture media, g3 military & veteran culture, g4 veteran & operator sphere) with "
        "Jocko Willink core in all three. Reconciled into ONE niche: the shared worldview is the warrior ethos (discipline, "
        "ownership, brotherhood, distrust of politicians who send others to war). A separate 'political veterans' niche failed "
        "the worldview bar: its voices (Hegseth, Kelly, Rieckhoff) share an identity, not values, and split along existing "
        "partisan niches. The political split is carried as sub-niches (America First vets / pro-constitution veterans / "
        "independent vets) with Hegseth and Rieckhoff as bridgers. Homed in d9 (mainstream culture) with D6 and D8 cross-listed."),
}
# gap niches dissolved into EXISTING v2 niches (their landmarks are re-homed below)
ABSORB = {
    'retail-trader-yolo': ('crypto-degens',
        "g3 retail-trader YOLO had one verified voice (Kevin Paffrath); Keith Gill is sporadic and unverified. Thin, so absorbed. "
        "Its outlook ('everything is a market', moonshot risk, anti-Wall-Street irony) is the degen worldview; the Atlas also "
        "places 'wallstreetbets' beside 'degens'. Paffrath joins crypto-degens as edge; sports betting goes to the Barstool niche.",
        ["WallStreetBets / retail-trader YOLO culture", "meme-stock apes"],
        ["retail-trader YOLO: WallStreetBets, meme stocks, options & betting apps (absorbed from g3 in v3)"]),
    'news-lite-exhausted-majority': ('bridging-depolarization-explainers',
        "g3 news-lite creators (Philip DeFranco, V Spehar) and the existing bridging/depolarization explainers share the same "
        "sacred values (calm, non-tribal information for the 'exhausted majority'); the difference is format and audience size. "
        "Merged into the existing niche, which also fixes its missing bridger (V Spehar) and thin landmark count (2 -> 4).",
        ["news-lite creators", "'exhausted majority' explainers (More in Common term)"],
        ["news-lite creators for the exhausted majority (DeFranco, Under the Desk News) — merged from g3 in v3"]),
}

# --------------------------------------------------------------------------------------------
# 2. Landmark identity and placement
# --------------------------------------------------------------------------------------------
ALIAS = {'red-scare': 'anna-khachiyan', 'dan-big-cat-katz': 'dan-katz'}
DISPLAY_NAME = {'dan-katz': "Dan 'Big Cat' Katz"}

# landmark_id -> primary niche (for people seeded in more than one place)
PRIMARY = {
    'david-hogg': 'gen-z-democratic-creators',
    'mark-kelly': 'gun-violence-prevention-movement',
    'paul-rieckhoff': 'veteran-warrior-culture-media',
    'jocko-willink': 'veteran-warrior-culture-media',
    'andrew-sullivan': 'gay-conservatives-lgb-dissenters',
    'brad-polumbo': 'gay-conservatives-lgb-dissenters',
    'kristin-kobes-du-mez': 'evangelical-conscience-critics',
    'kate-anthony': 'midlife-women-second-act',
    'steven-pinker': 'heterodox-academy-open-inquiry',
    'melissa-murray': 'progressive-legal-court-reform',
    'mel-robbins': 'therapeutic-self-help-mainstream',
    'dave-portnoy': 'barstool-boys-culture',
    'kai-cenat': 'streamer-creator-culture',
    'imani-barbarin': 'disability-rights-justice', 'emily-ladau': 'disability-rights-justice',
    'rebecca-cokley': 'disability-rights-justice',
    'kevin-paffrath': 'crypto-degens',
}
# extra secondary listings (landmark_id -> niches), beyond those implied by multi-file seeding
EXTRA_SECONDARY = {
    'steven-pinker': ['higher-ed-defenders'],
    'melissa-murray': ['reproductive-rights-movement'],
    'mel-robbins': ['daytime-lifestyle-mainstream'],
    'andrew-schulz': ['rogan-verse-longform-commons'],
    'adin-ross': ['barstool-boys-culture'],
    'dave-portnoy': ['crypto-degens'],
    'shawn-ryan': ['veteran-warrior-culture-media'],
    'mark-kelly': ['veteran-warrior-culture-media'],
    'paul-rieckhoff': ['democracy-reform-independents'],
    'warren-farrell': ['mens-rights-fathers-rights'],
    'jay-shetty': ['therapeutic-self-help-mainstream'],
    'sean-o-brien': ['national-conservatives'],
    'lyla-june-johnston': ['land-back-indigenous-sovereignty'],
    'dax-shepard': ['therapeutic-self-help-mainstream'],
    # g1 .md 'secondary landmarks suggested' (existing v2 records)
    'paola-ramos': ['latino-mainstream-media', 'immigrant-rights-movement'],
    'julio-ricardo-varela': ['immigrant-rights-movement'],
    'dan-bongino': ['law-and-order-police-support'],
    'mariame-kaba': ['criminal-justice-reform-decarceration'],
    'christopher-rufo': ['parents-rights-school-choice'],
    'michael-shellenberger': ['recovery-first-public-order'],
}
# landmark_id -> role in its PRIMARY niche (after merges)
ROLE = {
    'andrew-sullivan': 'bridger', 'dave-rubin': 'core', 'brad-polumbo': 'core', 'blaire-white': 'edge', 'chad-felix-greene': 'edge',
    'imani-barbarin': 'core', 'rebecca-cokley': 'core', 'emily-ladau': 'bridger',
    'jocko-willink': 'core', 'andy-stumpf': 'core', 'tim-kennedy': 'core', 'paul-rieckhoff': 'bridger', 'pete-hegseth': 'bridger',
    'kai-cenat': 'core', 'ishowspeed': 'core', 'ludwig-ahgren': 'core', 'pokimane': 'bridger', 'adin-ross': 'bridger',
    'dave-portnoy': 'core', 'dan-katz': 'core', 'kyle-forgeard': 'core', 'andrew-schulz': 'bridger', 'pft-commenter': 'bridger',
    'david-hogg': 'core', 'mark-kelly': 'bridger', 'steven-pinker': 'bridger', 'kristin-kobes-du-mez': 'core',
    'kevin-paffrath': 'edge', 'philip-defranco': 'core', 'v-spehar': 'bridger', 'mel-robbins': 'core', 'melissa-murray': 'core',
}
# per-secondary-listing roles (landmark_id -> {niche: role}); v3 adds this field
SECONDARY_ROLE = {
    'matt-taibbi': {'censorship-industrial-complex-critics': 'bridger'},
}
# over-cap or weak records held as alternates (kept in SEED-v3.json 'alternates', not mapped)
ALTERNATES = {
    'mat-best': "Over cap in the merged veteran niche (5 stronger voices); 2026 activity UNVERIFIED. Promote if Tim Kennedy fails verification.",
    'keith-gill': "Retail-trader niche absorbed into crypto-degens; sporadic output and UNVERIFIED. Symbolic figure only.",
    'daniel-christian-wahl': "Bioregionalism would exceed the cap of 5 after g6 added two verified US voices (Lyla June Johnston, Kenny Ausubel). Wahl is pending and non-US (us_focus_flag), so he moves to alternates. External reviewer may reverse.",
    'susan-glasser': "Proposed by g6 as the first woman in foreign-policy-establishment, but the niche already has 5 verified-active high-longform voices. Held as an alternate: on verification, swap in for Tommy Vietor (who overlaps anti-Trump liberal media).",
}

# --------------------------------------------------------------------------------------------
# 3. g6 handling notes
# --------------------------------------------------------------------------------------------
# strip private-vault-derived statements (Parachute / Gitcoin Brain) from public seed fields
PRIVATE_SCRUB = [
    (" Gitcoin Brain shows him leading a new rebuild.how podcast (AI Livelihood/neolocalism) in 2026; watch for a show change.", ""),
]
RENAME_ALIAS_EXTRA = {  # extra alias housekeeping that goes with the g6 renames
    'conspirituality-sovereignty': {'mark_outsider': {'wellness-to-right pipeline': "'wellness-to-right pipeline' (outsider/critics' label)"}},
}

# --------------------------------------------------------------------------------------------
# 4. Step-3 gap fill (12 WebSearch calls + 9 WebFetch calls, 2026-10-31)
# --------------------------------------------------------------------------------------------
def _L(lid, name, role, why, plat, lf, ver, ev_url, ev_date, gender, src, note=None):
    return dict(landmark_id=lid, name=name, role=role, why=why, platforms=plat, longform_output=lf, verification=ver,
                evidence_url=ev_url, evidence_date=ev_date, gender=gender, sources=src, verification_notes=note)

STEP3_NICHES = [
    dict(niche_id='therapeutic-self-help-mainstream', name='Therapeutic & self-help mainstream (therapy culture)',
         domain='d9-mainstream-culture', cross_domains=['d6-gender-lifestyle-subcultures'],
         aliases=['therapy culture', 'self-help podcasts', "'therapy-speak' (critics' label)", 'personal-growth mainstream'],
         description="The mass-audience culture of therapists, relationship experts and self-help hosts who translate psychology into everyday life: boundaries, attachment, self-worth, emotional honesty and 'doing the work'. Largely apolitical in tone, it shapes how tens of millions talk about relationships, family and mental health.",
         telos='A culture where people understand their emotions and relationships, heal old patterns and live with agency and honesty.',
         sacred_values=['emotional honesty', 'self-worth and boundaries', 'healing and growth', 'relational repair'],
         existential_threats=['loneliness and disconnection', 'shame and silence about mental health', 'burnout'],
         combatants=["critics of 'therapy-speak' and therapeutic culture (reactionary feminism, red-pill dating)", 'Red Pill dating / sexual market value'],
         adjacent_niches=['Daytime & lifestyle mainstream (Oprah-sphere & morning shows)', 'New Age, manifestation & wellness spirituality', 'Modern dating & relationships mainstream', 'Celebrity-chat & comedy podcast mainstream'],
         sub_niches=['relationship & couples therapy media (Esther Perel)', "women's self-actualization memoir culture (Glennon Doyle)", 'science-flavored motivation (Mel Robbins)', 'attachment-theory TikTok (see modern-dating-mainstream)'],
         size_estimate='very large (Mel Robbins and Glennon Doyle are top-chart podcasts; Perel is a global brand)',
         cultural_influence='high (sets the vocabulary of everyday relationship talk)', trajectory='stable',
         atlas_match=None, limberg_barnes_match=None,
         sources=['https://www.estherperel.com/podcast', 'https://podstatus.com/podcasts/we-can-do-hard-things-1329'],
         notes="Added at v3 QA (step 3). g3 had placed Mel Robbins in daytime-lifestyle as a bridger and g5 flagged therapy/self-help as a gap. Split from daytime TV because its unit is the therapeutic frame, not the talk-show format; Mel Robbins moves here as core (secondary in daytime).",
         gap_type='mainstream', placement=('X', 'neutral', 'within')),
    dict(niche_id='latino-mainstream-media', name='Spanish-language & Latino mainstream media',
         domain='d9-mainstream-culture', cross_domains=['d2-left-center', 'd1-right'],
         aliases=['Spanish-language media', 'Univision/Telemundo sphere', 'Latino mainstream'],
         description="The mainstream Spanish-language and bilingual media culture of US Latinos: network anchors and talk, radio morning shows, YouTube shows and public-radio journalism. It centers family, faith, work, immigrant dignity and Latin American homelands, and its politics range from the anchor tradition of advocacy for immigrants to the Cuban-exile anti-communist right in Miami.",
         telos='Inform and represent Latino families in their own language and on their own terms, and hold power accountable to them.',
         sacred_values=['familia', 'immigrant dignity', 'Spanish-language identity', 'hard work and upward mobility'],
         existential_threats=['mass deportation and fear in mixed-status families', 'being ignored or caricatured by English-language media', 'communism and authoritarianism in homelands (exile right)'],
         combatants=['Immigration restrictionists / border hawks', 'Hispanic realignment conservatives (for the anchor tradition)', 'Latino progressives (for the exile right)'],
         adjacent_niches=['Latino progressives and Latino-vote politics', 'Hispanic realignment conservatives', 'Latino Christianity (evangelical & Brown Church)', 'Immigrant-rights movement'],
         sub_niches=['network anchor tradition (Jorge Ramos)', 'Spanish-language radio morning shows (Enrique Santos)', 'Miami Cuban-exile YouTube talk (Alex Otaola)', 'bilingual public-radio journalism (Latino USA)', 'regional Mexican music culture (TODO)'],
         size_estimate='large (tens of millions of Spanish-dominant and bilingual viewers and listeners)',
         cultural_influence='medium-high (agenda-setting for Latino voters; declining network reach, rising digital)',
         trajectory='splitting (network decline; anchors go independent on YouTube; exile right grows online)',
         atlas_match=None, limberg_barnes_match=None,
         sources=['https://www.latintimes.com/jorge-ramos-makes-digital-journalism-history-news-emmys-i-veo-las-cosas-597643', 'https://en.wikipedia.org/wiki/Alexander_Otaola'],
         notes="Added at v3 QA (step 3) to close a gap flagged in v1 and by g3. Thin: two of four voices are pending. Still TODO: Univision/Telemundo talk-show hosts, regional Mexican music culture, Puerto Rican and Dominican media voices.",
         gap_type='representation', placement=('X', 'neutral', 'within')),
    dict(niche_id='progressive-legal-court-reform', name='Progressive legal academia & court reformers',
         domain='d2-left-center', cross_domains=['d8-geopolitics-media'],
         aliases=['court reform movement', 'Strict Scrutiny sphere', "'court packers' (critics' label)"],
         description="Liberal and progressive law professors, legal journalists and advocates who argue that the conservative Supreme Court majority is reshaping the country beyond what law requires. They explain cases to mass audiences, criticize originalism, and debate structural reform (term limits, ethics rules, expansion).",
         telos='A judiciary that protects rights and democratic self-government, constrained by ethics rules and structural reform.',
         sacred_values=['equal protection and reproductive rights', 'democratic accountability of courts', 'rule of law against executive overreach'],
         existential_threats=['an unaccountable 6-3 Court', 'executive defiance of courts', 'originalism as a cover for policy'],
         combatants=['Originalist / constitutional legal conservatives', 'Religious-liberty legal movement'],
         adjacent_niches=['Reproductive rights / reproductive freedom movement', 'Democracy-Protection and Voting-Rights Advocates', 'Anti-Trump liberal media (institutionalists & fight-mode creators)'],
         sub_niches=['court-expansion and term-limit advocates', 'legal-explainer podcasts (Strict Scrutiny, Amicus)', 'judicial-ethics reform'],
         size_estimate='medium (Strict Scrutiny and Amicus are top legal podcasts)', cultural_influence='medium-high (frames Democratic thinking about courts)',
         trajectory='rising', atlas_match=None, limberg_barnes_match='Social Justice Activists (partial)',
         sources=['https://crooked.com/podcast-series/strict-scrutiny/page/2', 'https://shows.acast.com/amicus-with-dahlia-lithwick-law-justice-and-the-courts/episodes'],
         notes="Added at v3 QA (step 3) as the mirror of originalist-legal-conservatives (flagged by g4). Melissa Murray moves here as core from reproductive rights (secondary there).",
         gap_type='mirror', placement=('L', 'neutral', 'within')),
]
STEP3_LANDMARKS = {  # niche -> landmarks (new records)
    'therapeutic-self-help-mainstream': [
        _L('esther-perel', 'Esther Perel', 'core', "Psychotherapist; 'Where Should We Begin?' (real couples' sessions) and 'Mating in Captivity'; the global voice of relationship therapy.",
           {'podcast': "Where Should We Begin? https://www.estherperel.com/podcast", 'x': '@EstherPerel'}, 'high', 'verified-active',
           'https://www.estherperel.com/podcast', '2026-09-28', 'female', ['https://www.estherperel.com/podcast'], 'Belgian-born, New York-based.'),
        _L('glennon-doyle', 'Glennon Doyle', 'core', "Author of 'Untamed'; co-hosts 'We Can Do Hard Things' with Abby Wambach and Amanda Doyle, a top self-help podcast of women's self-actualization.",
           {'podcast': 'We Can Do Hard Things https://podcasts.apple.com/us/podcast/id1564530722'}, 'high', 'verified-active',
           'https://podstatus.com/podcasts/we-can-do-hard-things-1329', '2026-10-22', 'female', ['https://podstatus.com/podcasts/we-can-do-hard-things-1329'],
           'Evidence is an aggregator "published" date (2026-10-22); confirm on the feed.'),
    ],
    'latino-mainstream-media': [
        _L('jorge-ramos', 'Jorge Ramos', 'core', "Univision's anchor for nearly four decades; since 2025 runs the independent YouTube show 'Así Veo las Cosas' (News Emmy, May 2026); the anchor tradition of advocacy for immigrants.",
           {'youtube': 'Jorge Ramos: Así Veo las Cosas (YouTube)', 'x': '@jorgeramosnews', 'podcast': 'The Moment (with Paola Ramos)'}, 'high', 'verified-active',
           'https://www.latintimes.com/jorge-ramos-makes-digital-journalism-history-news-emmys-i-veo-las-cosas-597643', '2026-05-28', 'male',
           ['https://www.latintimes.com/jorge-ramos-makes-digital-journalism-history-news-emmys-i-veo-las-cosas-597643', 'https://remezcla.com/culture/jorge-ramos-launches-news-podcast-with-his-daughter-paola-ramos/']),
        _L('enrique-santos', 'Enrique Santos', 'core', "iHeartLatino chairman and host of the daily Spanish-language Enrique Santos Show (Miami, syndicated); the voice of Latino morning radio.",
           {'other': 'The Enrique Santos Show (Tu 94.9 Miami, iHeartRadio)'}, 'high', 'pending', None, None, 'male',
           ['https://radioinsight.com/headlines/207574/iheartmedia-extends-enrique-santos/'], 'Latest dated source found is 2021; confirm 2025-26 activity.'),
        _L('maria-hinojosa', 'Maria Hinojosa', 'bridger', "Founder of Futuro Media and host of 'Latino USA', the long-running bilingual public-radio show; bridges Latino mainstream and progressive politics.",
           {'podcast': 'Latino USA https://www.iheart.com/podcast/1119-latino-usa-28457181/'}, 'high', 'verified-active',
           'https://www.audible.com/podcast/Latino-USA/episodes/B08K55MTLC', '≈2025-11 (episode on post-election Democratic wins; listing undated)', 'female',
           ['https://www.iheart.com/podcast/1119-latino-usa-28457181/'], 'Episode-level date inferred from content (Nov 2025 elections); confirm host credit on a dated episode.'),
        _L('alex-otaola', 'Alexander Otaola', 'edge', "Cuban-American host of the YouTube show 'Hola! Ota-Ola'; the Miami exile right's most-watched Spanish-language commentator; 2024 Miami-Dade mayoral candidate.",
           {'youtube': 'Hola! Ota-Ola (Cubanos por el Mundo)'}, 'high', 'pending', None, None, 'male',
           ['https://en.wikipedia.org/wiki/Alexander_Otaola'], 'No dated 2025-26 item confirmed within budget.'),
    ],
    'progressive-legal-court-reform': [
        _L('leah-litman', 'Leah Litman', 'core', "University of Michigan law professor and Strict Scrutiny co-host; author of 'Lawless' (2025) on the Supreme Court's conservative majority.",
           {'podcast': 'Strict Scrutiny https://crooked.com/podcast-series/strict-scrutiny/', 'bluesky': 'leahlitman.bsky.social'}, 'high', 'verified-active',
           'https://crooked.com/podcast-series/strict-scrutiny/page/2', '2026-10-26', 'female', ['https://crooked.com/podcast-series/strict-scrutiny/page/2']),
        _L('kate-shaw', 'Kate Shaw', 'core', 'Penn law professor and Strict Scrutiny co-host; former White House associate counsel; writes on the Court and executive power.',
           {'podcast': 'Strict Scrutiny https://crooked.com/podcast-series/strict-scrutiny/'}, 'high', 'verified-active',
           'https://crooked.com/podcast-series/strict-scrutiny/page/2', '2026-10-26', 'female', ['https://crooked.com/podcast-series/strict-scrutiny/page/2']),
        _L('dahlia-lithwick', 'Dahlia Lithwick', 'bridger', "Slate legal correspondent and host of 'Amicus'; long-form interviews with judges, scholars and litigators across the spectrum.",
           {'podcast': 'Amicus https://shows.acast.com/amicus-with-dahlia-lithwick-law-justice-and-the-courts'}, 'high', 'verified-active',
           'https://shows.acast.com/amicus-with-dahlia-lithwick-law-justice-and-the-courts/episodes/69a20a5fe1cf48c7c1b7244f', '≈2026-02-27 (from the Acast episode-id timestamp)', 'female',
           ['https://shows.acast.com/amicus-with-dahlia-lithwick-law-justice-and-the-courts/episodes'], 'Date inferred from the episode identifier; confirm on the episode page.'),
    ],
}
STEP3_EXISTING_NICHE_ADDS = {  # new records added to existing v2 niches
    'labor-movement-left': [
        _L('sean-o-brien', "Sean O'Brien", 'bridger', "Teamsters general president (re-elected June 2026); spoke at the 2024 RNC and leads labor's opening to Republicans while calling himself a Democrat; the face of labor's right flank.",
           {'x': '@TeamsterSOB', 'other': 'Teamsters (speeches, interviews)'}, 'low', 'verified-active',
           'https://news.bloomberglaw.com/daily-labor-report/teamsters-reelected-obrien-sees-path-to-bipartisan-labor-deals', '2026-06-29', 'male',
           ['https://news.bloomberglaw.com/daily-labor-report/teamsters-reelected-obrien-sees-path-to-bipartisan-labor-deals', 'https://politicalwire.com/2026/09/02/teamsters-union-leaders-support-republicans/'],
           'Trimmed in v1 for low longform; restored in v3 as the bridger to the populist right (no other voice holds that slot).'),
    ],
    'land-back-indigenous-sovereignty': [
        _L('deb-haaland', 'Deb Haaland', 'bridger', 'Former Interior Secretary (Laguna Pueblo) and 2026 Democratic nominee for New Mexico governor; the leading voice of Native electoral and tribal-government politics.',
           {'x': '@DebHaaland'}, 'low', 'verified-active', 'https://gvwire.com/2026/06/02/deb-haaland-wins-nomination-in-new-mexico-governors-race/', '2026-06-02', 'female',
           ['https://gvwire.com/2026/06/02/deb-haaland-wins-nomination-in-new-mexico-governors-race/', 'https://nativenewsonline.net/currents/nm-governor-candidates-officially-file-deb-haaland-to-face-district-attorney-sam-bregman-in-democratic-primary/'],
           'Low long-form output (candidate). Added so Native politics is not represented only by Land Back activists.'),
    ],
}
STEP3_EXISTING_UPDATES = {  # landmark_id -> field updates (records created from gap files)
    'melissa-murray': dict(verification='verified-active', evidence_url='https://crooked.com/podcast-series/strict-scrutiny/page/2', evidence_date='2026-10-26',
                           verification_notes='Named as Strict Scrutiny co-host on the 2026-10-26 episode listing (v3 step-3 fetch).'),
    'clay-travis': dict(verification='verified-active', evidence_url='https://thedesk.net/2026/06/clay-travis-departs-outkick/', evidence_date='2026-06 (URL path)',
                        verification_notes='Left OutKick (which he founded) in June 2026; remains a Fox News Media contributor and hosts his own FS1 show.',
                        platforms_other='Fox News contributor; FS1 show (left OutKick June 2026)'),
    'umar-johnson': dict(verification='verified-active', evidence_url='https://briefread.pages.dev/en/summary/dr-umar-calls-out-bad-bunny',
                         evidence_date='≈2026-02 (podcast interview reacting to the Feb 2026 Super Bowl halftime show)',
                         verification_notes='Evidence is a summary of a 2026 podcast appearance (Its Up There Pod); weak source, confirm on the original video.'),
}
STEP3_SUBNICHES = {
    'sports-talk-culture': ["anti-woke sports media / sports-talk right (OutKick, Clay Travis)"],
    'labor-movement-left': ["labor's right flank: Teamsters–GOP rapprochement (Sean O'Brien)"],
    'land-back-indigenous-sovereignty': ["tribal-government & Native electoral politics (Deb Haaland, Sharice Davids; Native Republicans such as Markwayne Mullin) — needs more long-form voices"],
    'rogan-verse-longform-commons': ["Austin comedy circuit (Kill Tony / Tony Hinchcliffe, Segura & Kreischer, Bill Burr; Andrew Schulz's Flagrant) — per g3, a sub-niche not a niche"],
    'mens-boys-advocacy': ["men's rights & fathers' rights split out in v3 (see mens-rights-fathers-rights)"],
    'anti-sexual-exploitation': ['age-verification laws (Free Speech Coalition v. Paxton, 2025)'],
}

# --------------------------------------------------------------------------------------------
# 5. Placement for new niches: (left_right, accelerate<->restrain, within-institutions<->exit)
# --------------------------------------------------------------------------------------------
PLACEMENT = {
    'reproductive-rights-movement': ('L', 'neutral', 'within'), 'gun-violence-prevention-movement': ('CL', 'restrain', 'within'),
    'public-health-evidence-based-medicine': ('CL', 'neutral', 'within'), 'immigration-restrictionists': ('R', 'restrain', 'within'),
    'immigrant-rights-movement': ('L', 'neutral', 'within'), 'pro-immigration-liberty-growth': ('CR', 'accelerate', 'within'),
    'law-and-order-police-support': ('R', 'restrain', 'within'), 'criminal-justice-reform-decarceration': ('L', 'neutral', 'within'),
    'parents-rights-school-choice': ('R', 'neutral', 'exit'), 'public-school-advocates-teachers-unions': ('L', 'restrain', 'within'),
    'higher-ed-defenders': ('CL', 'restrain', 'within'), 'harm-reduction-drug-policy-reform': ('L', 'neutral', 'within'),
    'recovery-first-public-order': ('C', 'restrain', 'within'), 'disability-rights-justice': ('L', 'neutral', 'within'),
    'veteran-warrior-culture-media': ('X', 'neutral', 'mixed'), 'religious-liberty-legal-movement': ('R', 'restrain', 'within'),
    'gen-z-conservative-creators': ('R', 'neutral', 'mixed'), 'gen-z-democratic-creators': ('CL', 'neutral', 'mixed'),
    'streamer-creator-culture': ('X', 'accelerate', 'exit'), 'barstool-boys-culture': ('X', 'neutral', 'exit'),
    'gen-z-faith-revival': ('X', 'restrain', 'within'),
    'sports-talk-culture': ('X', 'neutral', 'within'), 'pop-culture-stan': ('X', 'neutral', 'within'), 'bravo-reality-tv': ('X', 'neutral', 'within'),
    'celebrity-chat-comedy-podcasts': ('X', 'neutral', 'within'), 'true-crime-community': ('X', 'neutral', 'within'),
    'hip-hop-culture-commentary': ('X', 'neutral', 'mixed'), 'country-heartland-culture': ('X', 'restrain', 'within'),
    'daytime-lifestyle-mainstream': ('X', 'neutral', 'within'), 'skilled-trades-dignity-of-work': ('X', 'neutral', 'within'),
    'car-truck-motorsports': ('X', 'neutral', 'mixed'), 'mainstream-gaming-community': ('X', 'neutral', 'within'),
    'astrology-mainstream': ('X', 'neutral', 'exit'), 'black-family-faith-mainstream': ('X', 'restrain', 'within'),
    'democracy-reform-independents': ('C', 'neutral', 'within'), 'deliberative-democracy-civic-tech': ('C', 'neutral', 'within'),
    'patriotic-socialism-maga-communism': ('X', 'neutral', 'exit'), 'arab-muslim-american-political-bloc': ('X', 'neutral', 'within'),
    'gay-conservatives-lgb-dissenters': ('CR', 'neutral', 'mixed'), 'asian-american-conservatives': ('R', 'accelerate', 'within'),
    'black-nationalism-self-determination': ('X', 'neutral', 'exit'),
    'mens-rights-fathers-rights': ('CR', 'neutral', 'within'), 'protective-parents-family-court-reform': ('CL', 'neutral', 'within'),
    'childfree-by-choice': ('L', 'neutral', 'exit'), 'ethical-non-monogamy': ('L', 'neutral', 'exit'),
    'sex-positivity-sex-worker-rights': ('L', 'neutral', 'mixed'), 'anti-sexual-exploitation': ('X', 'restrain', 'within'),
    'queer-theory-abolitionist-left': ('L', 'neutral', 'exit'), 'biblical-womanhood-marriage-revival': ('R', 'restrain', 'within'),
    'evangelical-egalitarians-purity-culture-critics': ('CL', 'neutral', 'within'), 'midlife-women-second-act': ('X', 'neutral', 'within'),
    'homeschool-self-directed-education': ('X', 'restrain', 'exit'),
}
DOMAIN_OVERRIDE = {  # gap niche -> domain (placement decisions)
    'astrology-mainstream': ('d5-religion-spirituality', ['d9-mainstream-culture'],
        "Moved from d9 to D5: astrology is a meaning and divination system (a worldview), not a hobby, and D5 already holds "
        "New Age; kept as its own niche (Atlas lists 'astrology twitter' as a separate tribe) and the duplicate "
        "'astrology/tarot TikTok' sub-niche in new-age-manifestation-wellness now points here."),
    'black-family-faith-mainstream': ('d9-mainstream-culture', ['d5-religion-spirituality'],
        "Kept in d9: its unit is the mainstream Black entertainment-and-family culture (Steve Harvey, Tyler Perry, T.D. Jakes's "
        "media brand), whose politics are kept at arm's length. D5's black-church-prophetic is the justice/prophetic tradition "
        "and is not duplicated; T.D. Jakes is not seeded in any D5 niche."),
}
ATLAS_NEW = {'sports-talk-culture': 'sports twitter', 'pop-culture-stan': 'stan / pop culture', 'astrology-mainstream': 'astrology twitter',
             'pro-immigration-liberty-growth': None}
KEEP_DECISIONS = {
    'gen-z-faith-revival': "KEPT as a niche (not demoted). Its defining unit is a cross-denominational generational convergence "
        "(evangelical creators, Catholic and Orthodox converts, Bible-in-a-year culture) with its own creator-native voices "
        "(Girls Gone Bible, Sadie Robertson Huff, Ruslan KD). Demoting it would force a single denominational home and erase the "
        "convergence that defines it; it is also the mirror of deconstruction/nones. Trajectory is marked contested (survey "
        "evidence for a revival is mixed).",
    'homeschool-self-directed-education': "KEPT separate from parents-rights-school-choice. Different sacred values: homeschooling "
        "and unschooling are exit from schooling (child-led learning, family formation, including a secular-libertarian "
        "unschooling wing), while parents' rights / school choice is a political movement to control and fund-port public "
        "education (school boards, vouchers, curriculum). Both mirror public-school-advocates-teachers-unions.",
    'mens-rights-fathers-rights': "ACCEPTED g5's re-split from mens-boys-advocacy: the camps disagree on a fundamental "
        "(feminism compatible vs. feminism as cause). Weakest new niche — all three primaries pending; verify first, and "
        "fold back into mens-boys-advocacy as a sub-niche if verification fails.",
    'black-nationalism-self-determination': "KEPT, flagged as a weak entry: Pan-Africanist self-determination has different "
        "sacred values from ADOS (diaspora unity vs. US lineage claims). Umar Johnson verified only via a weak 2026 source; "
        "Kali Akuno pending. Demote to an ADOS sub-niche if both fail verification.",
    'biblical-womanhood-marriage-revival': "KEPT separate from tradwife-trad-femininity per g5: theological and empirical "
        "(Wilcox, Kearney) rather than aesthetic-lifestyle; revisit if Stage 2 extraction finds identical sacred values.",
    'public-health-evidence-based-medicine': "KEPT separate from skeptics-debunkers: institutions and clinical science "
        "(vaccine policy, ACIP) vs. a debunking media genre; they cross-appear but defend different things.",
}

# --------------------------------------------------------------------------------------------
# 6. Flags for Benjamin (neutral reasons; never repeat allegations)
# --------------------------------------------------------------------------------------------
_HB = "Possible harassment/incitement bar — review."
FLAGS = {
    'nick-fuentes': ('exclusion-review', "Possible harassment/incitement bar; keep descriptively or exclude — review."),
    'sneako': ('exclusion-review', "Tied to the Fuentes decision; review alongside it."),
    'andrew-tate': ('exclusion-review', _HB), 'tristan-tate': ('exclusion-review', _HB),
    'myron-gaines': ('exclusion-review', _HB),
    'alex-jones': ('exclusion-review', "Keep descriptively or exclude — review."),
    'laura-loomer': ('exclusion-review', "Possible harassment bar — review."),
    'joel-webbon': ('exclusion-review', "Possible harassment bar — review."),
    'timothy-gordon': ('exclusion-review', "Possible harassment bar — review."),
    'mohammed-hijab': ('exclusion-review', "Possible harassment bar — review; also UK-based (US-centrality check)."),
    'jared-taylor': ('exclusion-review', "Contested movement leader; confirm inclusion under the brief's exclusion bars — review."),
    'clavicular': ('minor-adjacent', "Young adult creator in a scene with many minors; confirm comfort with inclusion."),
    'jackson-hinkle': ('exclusion-review', "Confirm inclusion under the designated-organization exclusion — review."),
    'haz-al-din': ('exclusion-review', "Confirm inclusion under the designated-organization exclusion — review."),
    'umar-johnson': ('exclusion-review', "Possible harassment bar — review; weak verification."),
    'samantha-power-biofi': ('conflict-of-interest', "Benjamin's collaborator (The BioFi Project); confirm inclusion. Not the former USAID administrator."),
    'monty-bryant': ('conflict-of-interest', "Benjamin's long-term collaborator; confirm inclusion (also pending verification)."),
    'kevin-owocki': ('conflict-of-interest', "In Benjamin's professional network; confirm inclusion (conflict-of-interest check)."),
    'griff-green': ('conflict-of-interest', "In Benjamin's professional network; confirm inclusion (conflict-of-interest check)."),
}
OUTSIDE_REVIEW_NICHES = {
    'regens-refi': "Near Benjamin's own field and network; needs an outside reviewer.",
    'metacrisis-great-simplification': "Near Benjamin's own field; needs an outside reviewer.",
    'bioregionalism-regenerative-culture': "Benjamin's own field (Spirit of the Front Range); needs an outside reviewer.",
    'metamodernism': "Near Benjamin's own field; needs an outside reviewer.",
    'deliberative-democracy-civic-tech': "Benjamin's own field (civic tech); written neutrally by g4 with Benjamin and his organizations excluded; needs an outside reviewer.",
}

# --------------------------------------------------------------------------------------------
# 7. Content hygiene: exact-text rewrites (target id, field, old substring, new substring)
# --------------------------------------------------------------------------------------------
SCRUB = [
    ('fitness-biohacking', 'trajectory', 'stable (credibility hits: Attia resigned CBS Feb 2026 over Epstein emails)', 'stable'),
    ('christian-nationalism', 'notes', "Webbon's output includes statements critics call inflammatory (e.g., on Samuel Sey's ICE detention) — included descriptively; reviewers should check the brief's harassment exclusion.",
     "Webbon is included descriptively; his inclusion is flagged for Benjamin."),
    ('red-pill-dating', 'notes', ' (critics describe some of it as antisemitic)', ''),
    ('crypto-degens', 'notes', ' The 2025 SPX controversy around Murad is noted descriptively.', ''),
    ('hasan-piker', 'why', 'Largest left streamer; February 2026 Twitch ban and Democratic-party controversy.',
     'Largest left streamer; a recurring reference point in 2025-26 Democratic-party debates about online media.'),
    ('nick-fuentes', 'verification_notes', None, 'Mapped descriptively per the brief; inclusion decision pending (see flag_for_benjamin).'),
    ('mark-kelly', 'why', None, "Navy combat veteran, astronaut and Arizona senator; co-founded Giffords with Gabby Giffords and frames gun safety in gun-owner terms; also the leading voice of the pro-constitution veteran wing."),
    ('disability-rights-justice', 'notes', 'Alice Wong, the movement\'s best-known voice, died in November 2025 (obituaries, e.g. https://www.lewistownsentinel.com/obituaries/2025/11/disability-rights-activist-alice-wong-dies-at-51/), so she is not a landmark;',
     'Alice Wong is not seeded as a landmark;'),
    ('black-nationalism-self-determination', 'notes', None,
     "Weak entry: both landmarks need verification. Louis Farrakhan and Tariq Nasheed were considered and not seeded pending Benjamin's exclusion review. If verification fails, demote this niche to sub-niches of ADOS / lineage politics."),
    ('metacrisis-great-simplification', 'notes', 'Jim Rutt (Jim Rutt Show, Game B) died on 27 May 2026 (VERIFIED at QA: Wikipedia citing the Obaugh Funeral Home obituary), so he is excluded as a landmark;',
     'Jim Rutt (Jim Rutt Show, Game B) is not a landmark (see v1 QA-REPORT section 8);'),
    ('gay-conservatives-lgb-dissenters', 'notes', 'because of the harassment exclusion review', 'pending an exclusion review'),
    ('pete-hegseth', 'why', "the 'warrior ethos' purge of DEI", "the 'warrior ethos' campaign against DEI in the military"),
]

# --------------------------------------------------------------------------------------------
# 8. Mirror pairs (issue-movement niches must each appear in >= 1 pair; exceptions listed)
# --------------------------------------------------------------------------------------------
MIRRORS = [
    ('pro-life-movement', 'reproductive-rights-movement', 'abortion'),
    ('second-amendment-movement', 'gun-violence-prevention-movement', 'guns'),
    ('medical-freedom-vaccine-sceptic', 'public-health-evidence-based-medicine', 'vaccines & medical authority'),
    ('maha-coalition-wellness', 'public-health-evidence-based-medicine', 'health authority (HHS under RFK Jr.)'),
    ('immigration-restrictionists', 'immigrant-rights-movement', 'immigration (justice frame)'),
    ('immigration-restrictionists', 'pro-immigration-liberty-growth', 'immigration (liberty/growth frame)'),
    ('law-and-order-police-support', 'criminal-justice-reform-decarceration', 'policing & incarceration'),
    ('parents-rights-school-choice', 'public-school-advocates-teachers-unions', 'K-12 governance & vouchers'),
    ('homeschool-self-directed-education', 'public-school-advocates-teachers-unions', 'exit from schooling'),
    ('claremont-new-right', 'higher-ed-defenders', 'universities, DEI & federal pressure'),
    ('harm-reduction-drug-policy-reform', 'recovery-first-public-order', 'drugs & homelessness'),
    ('religious-liberty-legal-movement', 'lgbtq-trans-rights', 'religious exemptions vs. LGBTQ protections'),
    ('gay-conservatives-lgb-dissenters', 'lgbtq-trans-rights', 'LGB politics & gender identity'),
    ('gender-medicine-skeptics', 'lgbtq-trans-rights', 'youth gender medicine'),
    ('originalist-legal-conservatives', 'progressive-legal-court-reform', 'the Supreme Court'),
    ('gen-z-conservative-creators', 'gen-z-democratic-creators', 'youth political media'),
    ('gen-z-faith-revival', 'post-religious-deconstruction-nones', 'youth religiosity'),
    ('barstool-boys-culture', 'modern-dating-mainstream', "young men's vs. young women's media (Call Her Daddy)"),
    ('car-truck-motorsports', 'urbanism-strong-towns-car-free', 'cars'),
    ('mainstream-gaming-community', 'anti-woke-gamer', 'games culture'),
    ('asian-american-voices', 'asian-american-conservatives', 'Asian American politics (affirmative action, H-1B)'),
    ('democracy-protection-voting-rights', 'election-integrity-fraud-concern', 'elections'),
    ('mens-rights-fathers-rights', 'protective-parents-family-court-reform', 'family courts & custody'),
    ('pronatalism', 'childfree-by-choice', 'having children'),
    ('sex-positivity-sex-worker-rights', 'anti-sexual-exploitation', 'pornography, sex work & age verification'),
    ('biblical-womanhood-marriage-revival', 'evangelical-egalitarians-purity-culture-critics', 'complementarian vs. egalitarian'),
    ('tradwife-trad-femininity', 'queer-theory-abolitionist-left', 'the family (traditional vs. abolitionist poles)'),
    ('hispanic-realignment-conservatives', 'latino-progressive-politics', 'Latino partisanship'),
    ('black-conservatives', 'black-liberal-commentariat', 'Black politics'),
    ('peace-through-strength-hawks', 'america-first-restraint', 'war & Israel on the right'),
    ('china-hawks', 'china-engagers-detente', 'China'),
    ('pro-israel-zionist-commentators', 'pro-palestinian-movement', 'Israel–Palestine'),
    ('liberal-zionists', 'jewish-anti-zionist-non-zionist-left', 'Zionism among US Jews'),
    ('anti-disinformation-field', 'censorship-industrial-complex-critics', 'content moderation'),
    ('clean-energy-electrification', 'energy-dominance-climate-skeptic', 'energy & climate'),
    ('effective-accelerationism', 'ai-safety-xrisk', 'AI risk'),
    ('new-atheist-secular-humanist', 'apologetics-debate-culture', 'God'),
    ('skeptics-debunkers', 'conspiracy-realist-truther', 'epistemics of conspiracy'),
    ('housing-justice-tenant-movement', 'abundance-liberals', 'housing (tenant power vs. supply)'),
    ('evangelical-conscience-critics', 'evangelical-christian-right', 'evangelicals & Trump'),
    ('progressive-catholic', 'catholic-traditionalist', 'the Catholic Church'),
    ('never-trump-bulwark', 'maga-loyalist-media', 'Trump on the right'),
    ('degrowth-post-growth', 'progress-studies-abundance', 'growth'),
    ('gender-critical-feminism', 'lgbtq-trans-rights', 'sex & gender identity'),
    ('climate-justice-movement', 'energy-dominance-climate-skeptic', 'climate'),
    ('animal-rights-vegan', 'hunter-conservationists', 'animals, meat & hunting'),
]
ISSUE_EXCEPTIONS = {  # issue-type niches with no single opposing niche, and why
    'disability-rights-justice': "No organized opposing movement; internal fault lines (medical aid in dying, cure vs. identity) are sub-niches.",
    'veteran-warrior-culture-media': "Identity-based; the political split is internal (sub-niches).",
    'democracy-reform-independents': "Its foil is the two-party status quo, carried by both party niches, not one niche.",
    'deliberative-democracy-civic-tech': "Its foil is representative-politics-as-usual; no organized counter-movement.",
    'arab-muslim-american-political-bloc': "Constituency niche; internal Trump-voting vs. Uncommitted split is carried inside it.",
    'midlife-women-second-act': "Its contested ground (HRT, divorce) is argued with several niches, none a direct mirror.",
    'black-nationalism-self-determination': "Constituency niche; its argument partner is ADOS (a split within Black politics, not a mirror).",
    'patriotic-socialism-maga-communism': "A horseshoe niche; its antagonists are both the mainstream left and right.",
    'latino-mainstream-media': "Representation niche; its internal poles (anchor tradition vs. exile right) are carried inside it.",
}

# --------------------------------------------------------------------------------------------
# 9. Gender of new records (default male). From public self-description; duos as noted.
# --------------------------------------------------------------------------------------------
GENDER_NEW = {
 'female': """alexis-mcgill-johnson renee-bracey-sherman melissa-murray shannon-watts katelyn-jetelina ann-coulter greisa-martinez-rosas
  heather-mac-donald josie-duffy-rice helen-prejean tiffany-justice randi-weingarten becky-pringle diane-ravitch jennifer-berkshire
  emily-hanford kassandra-frederique maia-szalavitz imani-barbarin emily-ladau rebecca-cokley kristen-waggoner brett-cooper
  olivia-julianna sadie-robertson-huff angela-halili pokimane chani-nicholas susan-miller oprah-winfrey mel-robbins drew-barrymore
  kelly-clarkson bethenny-frankel ashley-flowers karen-kilgariff-georgia-hardstark bailey-sarian rissi-palmer katherine-gehl
  helene-landemore jennifer-pahlka blaire-white janice-fiamengo tina-swithin joan-meier ruby-warrington amy-blackstone jessica-fern
  emily-morse kaytlin-bailey aella laila-mickelwait haley-mcnamara sophie-lewis m-e-o-brien jules-gill-peterson
  kristen-clark-bethany-beal melissa-kearney beth-allison-barr sheila-wray-gregoire kristin-kobes-du-mez mary-claire-haver
  tamsen-fadal sharon-malone kate-anthony ginny-yurich kerry-mcdonald yvette-hampton harmeet-dhillon""".split(),
 'nonbinary': ['v-spehar', 'judith-butler'],
 'mixed': ['bobby-finger-lindsey-weber', 'dedeker-winston-jase-lindgren'],
 'unknown': ['deuxmoi'],
}
