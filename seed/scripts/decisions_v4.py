"""SEED-v4 judgment calls (data only). Used by build_v4.py.

Author of record: Benjamin Life (@omniharmonic). Base: SEED-v3.json (read only) + raw/g7-online-subcultures*, raw/g8-holistic-sweep*.
"""
TODAY = '2026-10-31'
WINDOW = '2025-10-31'   # verified-active needs a dated item on/after this date (v2 rule, unchanged)
CAP = 5

GAP_FILES = ['g7-online-subcultures', 'g8-holistic-sweep']
ADD_FILES = ['g7-online-subcultures.additions', 'g8-holistic-sweep.additions']

# ---------------------------------------------------------------- placement of new niches (left_right, accel/restrain, inst/exit)
PLACEMENT = {
    'decentering-men-single-on-purpose': ('L', 'neutral/mixed', 'exit'),
    'wellness-girlies-hormone-health': ('X', 'neutral/mixed', 'neutral/mixed'),
    'minimalism-anti-consumerism': ('X', 'restrain', 'exit'),
    'sober-curious-alcohol-free': ('X', 'restrain', 'neutral/mixed'),
    'rural-progressives-new-appalachia': ('L', 'neutral/mixed', 'within-institutions'),
    'tribal-nations-native-politics': ('CL', 'neutral/mixed', 'within-institutions'),
    'black-agrarianism-rural-black-south': ('L', 'restrain', 'exit'),
    'secession-national-divorce': ('X', 'neutral/mixed', 'exit'),
    'farm-ranch-mainstream': ('CR', 'neutral/mixed', 'within-institutions'),
    'populist-ai-backlash': ('X', 'restrain', 'within-institutions'),
    'markets-investing-mainstream': ('C', 'accelerate', 'within-institutions'),
    'main-street-small-business': ('CR', 'neutral/mixed', 'within-institutions'),
    'sikh-american-voices': ('CL', 'neutral/mixed', 'within-institutions'),
    'covid-conscious-long-covid': ('L', 'restrain', 'within-institutions'),
}
PLACEMENT_NOTES = {
    'secession-national-divorce': 'Horseshoe (TEXIT right, Calexit/Cascadia left); placed X although filed in d1.',
    'populist-ai-backlash': 'Cross-party coalition (Hawley/Bannon right core; Carson, Sanders on the left); placed X.',
}
# atlas_match must be one of the 39 known Owocki names (v3 rule); raw partial labels are logged and replaced
ATLAS = {
    'markets-investing-mainstream': 'wall street / macro',
    'black-agrarianism-rural-black-south': None,      # raw: 'regens & solarpunks (partial)'
    'secession-national-divorce': None,                # raw: 'network-state builders (partial: exit as strategy)'
    'populist-ai-backlash': None,                      # raw: 'maga / populist right (anti-AI strand); mirror of e/acc'
    'main-street-small-business': None,                # raw: 'indie hackers (offline analogue)'
}

# ---------------------------------------------------------------- QA-added niche (step 2, cheap gaps)
STEP2_NICHES = [dict(
    niche_id='covid-conscious-long-covid', name="COVID-conscious & long-COVID community", domain='d4-heterodox-sensemaking',
    cross_domains=['d6-gender-lifestyle-subcultures', 'd2-left-center'],
    aliases=["COVID-cautious", "'still coviding'", "COVID is not over", "long-COVID advocacy", "covid zero (outsider label)"],
    description=("People who continue to take COVID-19 precautions (masking, clean air, testing) and long-COVID patients and journalists who argue the "
                 "pandemic's chronic-illness toll is being ignored. They organize through mutual aid, mask blocs, clean-air campaigns and independent "
                 "health journalism, and frame precaution as community care and disability solidarity."),
    telos="Public recognition of long COVID and airborne transmission; clean indoor air, research and care for the chronically ill; precautions treated as normal community care.",
    sacred_values=['community care and solidarity with the immunocompromised', 'disability inclusion', 'scientific evidence on airborne transmission', 'collective rather than individual risk'],
    existential_threats=['mass disabling events normalized', 'the end of public-health data and research', 'mask bans and stigma', 'minimization by health institutions'],
    combatants=['Medical freedom / vaccine-sceptic', 'MAHA coalition & wellness', 'Public-health & evidence-based medicine defenders (on "COVID is over" messaging)'],
    adjacent_niches=['Disability justice & disability rights', 'Public-health & evidence-based medicine defenders', 'Democratic socialists (DSA / Jacobin left)'],
    sub_niches=['mask blocs and clean-air mutual aid', 'long-COVID patient advocacy and patient-led research', 'independent long-COVID journalism (The Sick Times)',
                'health-communism / disability-left podcasting (Death Panel)', 'ME/CFS overlap'],
    size_estimate="small (+ active online communities; a few long-form shows and newsletters)",
    cultural_influence="low-medium (+ shapes disability-left and clean-air advocacy; marginal in mainstream politics)",
    trajectory="stable (+ organizing shifted from mandates to clean-air and long-COVID recognition)",
    atlas_match=None, limberg_barnes_match=None,
    sources=['https://thesicktimes.org/2026/06/05/indie-bookstores-promoting-masking-and-covid-19-consciousness-in-2026/',
             'https://zeno.fm/podcast/still-here-a-podcast-from-the-sick-times/episodes/long-covid-awareness-day-2026-inside-the-growing-organizing-efforts-to-recognize-the-disease',
             'https://podcasts.apple.com/us/podcast/death-panel/id1444679141'],
    notes=("Added at v4 QA as the mirror of medical-freedom-vaccine-sceptic (gap noted by g7). Promoted from the disability-rights-justice sub-niche "
           "\"COVID-conscious / 'still coviding' community\". Bar met: two adult long-form voices verified active (Ladyzhets, Mar 2026; Death Panel, Oct 2026). "
           "Death Panel's current co-hosts include Jules Gill-Peterson (already seeded in queer-theory-abolitionist-left)."),
    gap_type='mirror', mirror_of='medical-freedom-vaccine-sceptic')]

STEP2_LANDMARKS = {
    'covid-conscious-long-covid': [
        dict(landmark_id='betsy-ladyzhets', name='Betsy Ladyzhets', role='core', gender='female', longform_output='medium',
             why="Founder and editor of The Sick Times, the main independent newsroom covering long COVID; co-hosts its podcast Still Here.",
             platforms={'podcast': 'Still Here: A Podcast from The Sick Times', 'substack': None, 'other': 'https://thesicktimes.org'},
             verification='verified-active', evidence_url='https://zeno.fm/podcast/still-here-a-podcast-from-the-sick-times/episodes/long-covid-awareness-day-2026-inside-the-growing-organizing-efforts-to-recognize-the-disease',
             evidence_date='2026-03-27', verification_notes='Still Here episode (Long COVID Awareness Day 2026) dated 2026-03-27; co-host Miles Griffis.',
             sources=['https://zeno.fm/podcast/still-here-a-podcast-from-the-sick-times/episodes/long-covid-awareness-day-2026-inside-the-growing-organizing-efforts-to-recognize-the-disease',
                      'https://thesicktimes.org/2026/06/05/indie-bookstores-promoting-masking-and-covid-19-consciousness-in-2026/']),
        dict(landmark_id='beatrice-adler-bolton-artie-vierkant', name='Beatrice Adler-Bolton & Artie Vierkant (Death Panel)', role='bridger', gender='mixed',
             longform_output='high', record_type='multi-person',
             why="Hosts of Death Panel, a weekly health-politics podcast and the best-known long-form voice of 'COVID is not over' disability-left politics; authors of Health Communism. Bridges to the socialist and disability-justice left.",
             platforms={'podcast': 'Death Panel https://podcasts.apple.com/us/podcast/death-panel/id1444679141', 'other': 'https://www.deathpanel.net'},
             verification='verified-active', evidence_url='https://podcasts.apple.com/us/podcast/death-panel/id1444679141', evidence_date='2026-10-23',
             verification_notes="Episodes dated Oct 2026 on Apple Podcasts (e.g., 'How to Close a Camp', Oct 23). Current co-hosts also include Phil Rocco and Jules Gill-Peterson. COVID focus is from knowledge of the show's archive; recent episodes range across health politics.",
             sources=['https://podcasts.apple.com/us/podcast/death-panel/id1444679141', 'https://muckrack.com/podcast/death-panel/']),
        dict(landmark_id='julia-doubleday', name='Julia Doubleday', role='core', gender='female', longform_output='medium',
             why="Writer of The Gauntlet newsletter and long-COVID patient; one of the most-shared voices arguing that COVID minimization is a public-health failure.",
             platforms={'substack': 'https://www.thegauntlet.news', 'bluesky': 'juliadoubleday.bsky.social'},
             verification='pending', evidence_url='https://oyvayblog.blogspot.com/2025/10/the-nightmare-of-living-with-long-covid.html', evidence_date='2025-10-16',
             verification_notes='Latest dated item found is a repost from Oct 16, 2025 (before the window). Needs a dated 2025-11+ item.',
             sources=['https://rss-parrot.net/web/feeds/www.thegauntlet.news']),
    ],
}
STEP2_EXISTING_ADDS = {
    'gender-critical-feminism': [
        dict(landmark_id='riley-gaines', name='Riley Gaines', role='bridger', gender='female', longform_output='high',
             why="Former NCAA swimmer and the leading 'Save women's sports' voice; hosts an OutKick podcast. Carries the sex-based sports argument from gender-critical feminism to the conservative right.",
             platforms={'podcast': "OutKick podcast (launched as 'Gaines for Girls'; confirm current title)", 'x': '@Riley_Gaines_ (UNVERIFIED)',
                        'other': 'OutKick / Fox News appearances'},
             verification='verified-active', evidence_url='https://tools.prnewswire.com/en-us/live/20772/release/20251217NY50031', evidence_date='2025-12-17',
             verification_notes='OutKick announced a new multi-year podcast deal with her on 2025-12-17 (PR Newswire). Placed in gender-critical-feminism because that niche already holds the anti-self-ID-in-sports position; her mirror (lgbtq-trans-rights) exists. Not a separate niche: her allies (Paula Scanlan, Payton McNabb) were not checked.',
             sources=['https://tools.prnewswire.com/en-us/live/20772/release/20251217NY50031',
                      'https://www.mediaite.com/sports/outkick-announces-upcoming-gaines-for-girls-podcast-hosted-by-riley-gaines/'],
             secondary={'sports-talk-culture': 'edge', 'gender-medicine-skeptics': 'bridger'}),
    ],
    'minimalism-anti-consumerism': [
        dict(landmark_id='dawn-madsen', name='Dawn Madsen (The Minimal Mom)', role='bridger', gender='female', longform_output='medium',
             why="Decluttering and family-minimalism YouTuber (about 880K subscribers); carries 'own less' to a mostly female, faith-friendly homemaking audience.",
             platforms={'youtube': 'https://www.youtube.com/@TheMinimalMom', 'podcast': 'The Minimal Mom (podcast; last episode Nov 2024)'},
             verification='verified-active', evidence_url='https://creatordb.app/creatorstats/theminimalmom/', evidence_date='2026-10-02',
             verification_notes='Aggregator (creatordb, refreshed 2026-10-06) shows a YouTube upload about 2026-10-02 and others in Sept 2026; approximate date. Her podcast feed stopped in Nov 2024. YouTube URL from knowledge; confirm.',
             sources=['https://creatordb.app/creatorstats/theminimalmom/', 'https://podcasts.apple.com/gb/podcast/the-minimal-mom/id1579074055']),
    ],
}

# ---------------------------------------------------------------- primary moves and secondary roles
PRIMARY_MOVES = {  # landmark -> (new primary, new role, secondary role in old primary, reason)
    'hope-woodard': ('decentering-men-single-on-purpose', 'core', 'bridger',
                     "Originator of 'boysober'; g7 recommends this as her home. Kept as a secondary (bridger) in liberal feminism. Her current show still needs a re-check."),
    'deb-haaland': ('tribal-nations-native-politics', 'bridger', 'bridger',
                    "Her v3 slot represented the tribal-government / Native electoral sub-niche, which moved to the new niche. Kept as a secondary (bridger) in Land Back."),
}
NOT_MOVED = {
    'ruby-warrington': "g7 suggests making sober-curious her primary; kept in childfree-by-choice (moving her would leave that niche with one landmark). Secondary (core) in sober-curious.",
}
SECONDARY_EXTRA = {  # landmark -> {niche: role}
    'taylor-lorenz': {'gen-z-disaffection': 'edge', 'streamer-creator-culture': 'edge'},
    'ruby-warrington': {'sober-curious-alcohol-free': 'core'},
}

# ---------------------------------------------------------------- sub-niche changes (g7, g8, QA)
SUBNICHE_REPLACE = {  # niche -> {old: new}
    'looksmaxxing-blackpill': {'incel forums (looksmax.org)': 'incel / blackpill discourse (mapped only through adult researchers and journalists; forum figures not seeded)'},
    'liberal-feminism': {'4B / decentering men (merged niche)': '4B / decentering men (now its own niche: decentering-men-single-on-purpose)'},
    'land-back-indigenous-sovereignty': {"tribal-government & Native electoral politics (Deb Haaland, Sharice Davids; Native Republicans such as Markwayne Mullin) — needs more long-form voices":
                                         "tribal-government & Native electoral politics (moved in v4 to its own niche: tribal-nations-native-politics)"},
    'disability-rights-justice': {"COVID-conscious / 'still coviding' community": "COVID-conscious / 'still coviding' community (now its own niche: covid-conscious-long-covid)"},
    'crypto-degens': {'retail-trader YOLO: WallStreetBets, meme stocks, options & betting apps (absorbed from g3 in v3)':
                      'retail-trader YOLO: WallStreetBets, meme stocks, options & betting apps (absorbed from g3 in v3; also listed under markets-investing-mainstream)'},
}
SUBNICHE_ADD = {
    'gen-z-disaffection': ['girl rot / femcel / girlhood internet', 'soft life (anti-hustle femininity)'],
    'new-age-manifestation-wellness': ["divine-feminine / feminine-energy coaching (cross-reference tradwife 'feminine-energy coaching')"],
    'humane-tech-attention-critics': ['AI-companion users (r/MyBoyfriendIsAI, #keep4o), described from the users\' own perspective, not only as harm'],
    'immigrant-rights-movement': ['Haitian, Caribbean and African (Black immigrant) advocates (Haitian Bridge Alliance, UndocuBlack)'],
    'skilled-trades-dignity-of-work': ['truckers and owner-operator drivers (OOIDA, trucker YouTube; English-proficiency and freight-fraud fights)'],
    'public-health-evidence-based-medicine': ['nurses and frontline healthcare workers (National Nurses United; nurse creators)'],
    'christian-postliberals-integralists': ['Anabaptist and plain-church voices (Bruderhof / Plough Quarterly) as a small adjacent current'],
    'new-atheist-secular-humanist': ['The Satanic Temple (religious-liberty litigation by nontheists)'],
    'progressive-christianity': ['Unitarian Universalists'],
    'meaning-crisis-religious-turn': ['Girardians (mimetic theory; Owocki Atlas tribe)'],
    'asian-american-voices': ['Filipino American, Korean American and Vietnamese American currents'],
    'classical-liberal-libertarians': ["Western public-lands transfer / 'sagebrush' property-rights advocates (mirror side of hunter-conservationists on federal land sales)"],
    'degrowth-post-growth': ['minimalism / voluntary simplicity (now its own niche: minimalism-anti-consumerism; Juliet Schor secondary there)'],
    'gender-critical-feminism': ["'Save women's sports' / sex-based sports categories (Riley Gaines; Title IX fights)"],
    'sports-talk-culture': ["women's sports fandom (WNBA; A Touch More) and its 'Save women's sports' counter-current (Riley Gaines, OutKick)"],
    'progress-studies-abundance': ['Georgists / land-value tax (Owocki Atlas tribe; one checked voice, Lars Doucet; kept as sub-niche)'],
}
SUBNICHE_NOOP = {'crypto-degens': "'Remilia / Milady' kept as a sub-niche (g7: not promoted)."}

# ---------------------------------------------------------------- mirrors added in v4 (each side named as its members describe it)
MIRRORS_V4 = [
    ('red-pill-dating', 'decentering-men-single-on-purpose', 'opting out of the other sex (MGTOW vs. decentering men)'),
    ('looksmaxxing-blackpill', 'wellness-girlies-hormone-health', "self-optimization (men's vs. women's parallel; not opponents)"),
    ('hustle-finfluencer', 'minimalism-anti-consumerism', 'consumption & status'),
    ('barstool-boys-culture', 'sober-curious-alcohol-free', 'drinking culture'),
    ('tech-right', 'populist-ai-backlash', 'AI regulation, preemption & data centers'),
    ('rural-populist-farmers', 'farm-ranch-mainstream', 'farm policy & agribusiness consolidation'),
    ('medical-freedom-vaccine-sceptic', 'covid-conscious-long-covid', 'COVID precautions & long COVID'),
]
ISSUE_EXCEPTIONS_V4 = {
    'secession-national-divorce': "Horseshoe niche (TEXIT right, Calexit/Cascadia left); its foil is national unity carried by both party niches.",
    'tribal-nations-native-politics': "Constituency niche; its argument with Land Back (within vs. outside the federal system) is an internal split, not a mirror.",
}

# ---------------------------------------------------------------- flags
CONFLICT_NEW = {
    'brad-carson': "Public First (his AI-policy group and super PAC) is reportedly funded mainly by Anthropic, the company whose model assembled this seed. Benjamin to decide whether to keep him (conflict-of-interest check).",
}
OUTSIDE_REVIEW_NEW = {
    'tribal-nations-native-politics': "Outside reviewer recommended (near Benjamin's Treaty Land Atlas work).",
    'land-back-indigenous-sovereignty': "Outside reviewer recommended (near Benjamin's Treaty Land Atlas work).",
}

# ---------------------------------------------------------------- searches used in v4 QA (step 2)
SEARCHES = [
    ('WebSearch', 'Riley Gaines podcast OutKick 2026'), ('WebSearch', 'Death Panel podcast 2026'),
    ('WebSearch', 'COVID-conscious community 2026 (masking, long COVID)'), ('WebSearch', 'Julia Doubleday The Gauntlet 2026'),
    ('WebSearch', 'Courtney Carver Project 333 2026'), ('WebSearch', 'no-buy / deinfluencing women creators 2026'),
    ('WebSearch', 'The Minimal Mom Dawn Madsen 2026'),
    ('WebFetch', 'Apple Podcasts: Death Panel'), ('WebFetch', 'Zeno: Still Here (The Sick Times) episode'),
    ('WebFetch', 'Apple Podcasts: The Minimal Mom'), ('WebFetch', 'creatordb: The Minimal Mom'),
]
CONSIDERED_STEP2 = [
    ("'Save women's sports' as its own niche", "Not created: Gaines fits gender-critical feminism's existing position on sex-based sports; only one voice checked. Mirror (lgbtq-trans-rights) already exists."),
    ('Courtney Carver (Be More with Less / Project 333)', 'No dated 2025-26 first-person item found; not seeded.'),
    ('Elysia Berman (no-buy year)', 'Guest appearances only (Jan 2025); no own long-form show found; not seeded.'),
]
