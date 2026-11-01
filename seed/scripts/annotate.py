"""Atlas alignment, rough placements, gender, flags, and trim list."""
# Partial Atlas (39 of 58 names; atlas-2026-07-28-partial.md). Only exact/near-exact correspondences are recorded.
ATLAS = {
 'effective-accelerationism':'effective accelerationists','progress-studies-abundance':'progress & abundance movement',
 'techno-optimists-american-dynamism':'hard-tech & space frontier','space-mars-expansionists':'hard-tech & space frontier',
 'rationalists':'rationalists','ai-safety-xrisk':'AI-safety doomers','effective-altruism':'effective altruists',
 'tpot-post-rationalists':'tpot / post-rationalists','psychedelic-spirituality':'consciousness & psychedelic twitter',
 'bitcoin-maximalists':'bitcoin maxis','ethereum-builders':'ethereum builders','defi-stablecoin-institutionalists':'DeFi & stablecoin builders',
 'crypto-degens':'degens & memecoin culture','regens-refi':'regens & solarpunks','degrowth-post-growth':'degrowthers & climate realists',
 'longevity-transhumanists':'longevity & biohackers','fitness-biohacking':'longevity & biohackers','maha-coalition-wellness':'MAHA & health freedom',
 'medical-freedom-vaccine-sceptic':'MAHA & health freedom','neoreaction-vitalist-right':'neoreaction & the new right',
 'network-state-charter-cities':'network-state builders','maga-loyalist-media':'maga / populist right','war-room-populist-nationalists':'maga / populist right',
 'progressive-squad-left':'progressive left','anti-trump-liberal-media':'liberal establishment','sound-money-austrian-gold':'wall street / macro',
 'evangelical-christian-right':'christian twitter','metamodernism':'metamodernists','forecasters-prediction-markets':'forecasters',
 'pronatalism':'pronatalists','metacrisis-great-simplification':'doomer optimists','catholic-traditionalist':'trad catholics',
 'new-age-manifestation-wellness':'astrology twitter','hustle-finfluencer':'indie hackers',
}
# niche -> (placement, accelerate<->restrain, within-institutions<->exit)
# placement: L, CL, C, CR, R, X (cross-cutting/other). axes: A/R/- and W/E/-
P = {
 'war-room-populist-nationalists':('R','-','E'),'maga-loyalist-media':('R','-','W'),'turning-point-movement':('R','-','W'),
 'america-first-restraint':('R','R','E'),'groypers-america-first':('R','-','E'),'national-conservatives':('R','R','W'),
 'evangelical-christian-right':('R','R','W'),'christian-nationalism':('R','R','E'),'pro-life-movement':('R','R','W'),
 'paleolibertarian-antiwar':('R','-','E'),'classical-liberal-libertarians':('CR','A','W'),'fiscal-business-conservatives':('CR','A','W'),
 'daily-wire-culture-conservatives':('R','R','W'),'dispatch-center-right':('CR','-','W'),'claremont-new-right':('R','-','W'),
 'neoreaction-vitalist-right':('R','A','E'),'race-realist-dissident-right':('R','-','E'),'originalist-legal-conservatives':('R','-','W'),
 'hispanic-realignment-conservatives':('R','-','W'),'black-conservatives':('R','-','W'),'second-amendment-movement':('R','-','E'),
 'never-trump-bulwark':('C','-','W'),'progressive-squad-left':('L','-','W'),'fight-oligarchy-populist-left':('L','-','W'),
 'democratic-socialists-dsa':('L','-','W'),'abundance-liberals':('CL','A','W'),'moderate-centrist-democrats':('CL','A','W'),
 'anti-trump-liberal-media':('CL','-','W'),'black-liberal-commentariat':('CL','-','W'),'ados-lineage-politics':('X','-','E'),
 'latino-progressive-politics':('L','-','W'),'labor-movement-left':('L','R','W'),'dirtbag-left':('L','-','E'),
 'class-first-heterodox-left':('L','-','E'),'anti-imperialist-ml-left':('L','-','E'),'anarchist-mutual-aid-left':('L','R','E'),
 'gen-z-online-left-streamers':('L','-','E'),'asian-american-voices':('CL','-','W'),
 'effective-accelerationism':('X','A','E'),'techno-optimists-american-dynamism':('CR','A','E'),'tech-right':('R','A','E'),
 'network-state-charter-cities':('X','A','E'),'rationalists':('X','-','E'),'effective-altruism':('X','R','W'),
 'ai-safety-xrisk':('X','R','W'),'agi-frontier-builders':('X','A','W'),'ai-ethics-critics':('L','R','W'),
 'tech-hype-skeptics':('CL','R','-'),'neo-luddites-anti-ai-creatives':('L','R','-'),'humane-tech-attention-critics':('X','R','W'),
 'dacc-pluralist-tech':('X','A','E'),'bitcoin-maximalists':('X','A','E'),'ethereum-builders':('X','A','E'),
 'defi-stablecoin-institutionalists':('X','A','W'),'crypto-degens':('X','A','E'),'longevity-transhumanists':('X','A','E'),
 'progress-studies-abundance':('X','A','W'),'space-mars-expansionists':('X','A','E'),'open-source-digital-rights':('L','-','E'),
 'forecasters-prediction-markets':('X','A','-'),'tpot-post-rationalists':('X','-','E'),
 'maha-coalition-wellness':('R','R','E'),'conspiracy-realist-truther':('R','-','E'),'free-speech-civil-libertarians':('X','-','W'),
 'heterodox-academy-open-inquiry':('C','-','W'),'independent-anti-establishment-journalism':('X','-','E'),
 'free-press-heterodox-institutional':('CR','-','W'),'idw-remnant-evolutionary-lens':('X','R','E'),'rogan-verse-longform-commons':('X','-','E'),
 'populist-horseshoe-anti-establishment':('X','-','E'),'bridging-depolarization-explainers':('C','-','W'),
 'metacrisis-great-simplification':('X','R','E'),'metamodernism':('X','-','-'),'integral-wilberian':('X','-','-'),
 'meaning-crisis-religious-turn':('X','R','-'),'conspirituality-sovereignty':('X','R','E'),'medical-freedom-vaccine-sceptic':('R','R','E'),
 'uap-disclosure':('X','-','E'),'lost-civilization-alt-history':('X','-','E'),
 'christian-postliberals-integralists':('R','R','W'),'evangelical-megachurch-mainstream':('CR','-','W'),'evangelical-conscience-critics':('C','-','W'),
 'reformed-tgc':('CR','R','W'),'progressive-christianity':('L','-','W'),'post-religious-deconstruction-nones':('L','-','E'),
 'catholic-evangelical-mainstream':('CR','-','W'),'progressive-catholic':('CL','-','W'),'catholic-traditionalist':('R','R','E'),
 'orthodox-convert-wave':('R','R','E'),'black-church-prophetic':('L','-','W'),'charismatic-pentecostal':('R','-','W'),
 'apologetics-debate-culture':('X','-','-'),'latter-day-saints':('CR','-','W'),'american-muslim-mainstream':('X','-','W'),
 'muslim-dawah-anti-liberal':('X','R','E'),'jewish-orthodox-traditional':('CR','R','W'),'jewish-progressive-renewal':('L','-','W'),
 'new-atheist-secular-humanist':('X','-','-'),'new-age-manifestation-wellness':('X','-','E'),'psychedelic-spirituality':('X','-','E'),
 'pagan-witchcraft':('L','-','E'),'buddhist-contemplative':('X','R','-'),'esoteric-occult-traditionalism':('X','-','E'),
 'hindu-american-voices':('X','-','W'),'latino-christianity':('X','-','W'),
 'lgbtq-trans-rights':('L','-','W'),'red-pill-dating':('R','-','E'),'alpha-hustle-masculinity':('R','A','E'),'mens-boys-advocacy':('C','-','W'),
 'looksmaxxing-blackpill':('X','-','E'),'tradwife-trad-femininity':('R','R','E'),'reactionary-feminism':('X','R','-'),
 'liberal-feminism':('L','-','W'),'gender-critical-feminism':('X','-','-'),'gender-medicine-skeptics':('R','R','-'),
 'pronatalism':('R','A','E'),'modern-dating-mainstream':('X','-','-'),'fitness-biohacking':('X','A','E'),'hustle-finfluencer':('R','A','E'),
 'gen-z-disaffection':('X','R','E'),'anti-woke-gamer':('R','-','E'),'fat-liberation':('L','-','-'),'neurodivergence-identity':('L','-','-'),
 'parenting-philosophies':('X','R','-'),
 'regens-refi':('L','A','E'),'ecomodernism-nuclear-abundance':('C','A','W'),'climate-justice-movement':('L','R','W'),
 'clean-energy-electrification':('CL','A','W'),'energy-dominance-climate-skeptic':('R','A','W'),'degrowth-post-growth':('L','R','E'),
 'bioregionalism-regenerative-culture':('L','R','E'),'permaculture-homesteading':('X','R','E'),'regen-ag-food-freedom':('X','R','E'),
 'preppers-self-reliance':('R','R','E'),'mmt-heterodox-macro':('L','-','W'),'sound-money-austrian-gold':('R','-','E'),
 'personal-finance-fire':('X','-','E'),'anti-monopoly-neo-brandeisian':('L','R','W'),'cooperative-solidarity-economy-commons':('L','-','E'),
 'urbanism-strong-towns-car-free':('X','-','W'),'housing-justice-tenant-movement':('L','-','W'),'rural-populist-farmers':('X','R','W'),
 'animal-rights-vegan':('L','-','-'),'land-back-indigenous-sovereignty':('L','R','E'),'hunter-conservationists':('X','R','W'),'skeptics-debunkers':('CL','-','W'),
 'peace-through-strength-hawks':('R','-','W'),'anti-disinformation-field':('CL','-','W'),'pro-palestinian-movement':('L','-','E'),
 'foreign-policy-realists-restrainers':('X','R','W'),'dissident-military-analysis-circuit':('X','R','E'),'multipolarity-global-south':('L','-','E'),
 'left-restraint-foreign-policy':('L','R','E'),'foreign-policy-establishment':('CL','-','W'),'liberal-internationalist-democracy-defenders':('CL','-','W'),
 'osint-war-analysis':('X','-','E'),'china-hawks':('R','-','W'),'china-engagers-detente':('CL','R','W'),'pro-israel-zionist-commentators':('CR','-','W'),
 'liberal-zionists':('CL','-','W'),'jewish-anti-zionist-non-zionist-left':('L','-','E'),'legacy-media-institutionalists':('CL','-','W'),
 'censorship-industrial-complex-critics':('R','-','E'),'election-integrity-fraud-concern':('R','-','W'),'democracy-protection-voting-rights':('CL','-','W'),
}
FEMALE = set('''alena-kate-pettitt alex-clark alex-cooper alex-hanna alexandria-ocasio-cortez allie-beth-stuckey ana-kasparian anne-applebaum
anne-helen-petersen aru-shiney-ajay aubrey-gordon bari-weiss becky-kennedy briahna-joy-gray candace-owens casey-means
catherine-engelbrecht catherine-pakaluk cea-weaver chloe-cole cindy-cohn claudia-de-la-cruz cleta-mitchell dalia-mogahed danya-ruttenberg
diana-butler-bass diana-rodgers divya-siddarth emily-m-bender emily-oster erika-kirk erin-reed estee-williams freya-india gabrielle-bernstein
gabrielle-judge hannah-neeleman hannah-pearl-davis hannah-ritchie heather-cox-richardson heather-heying helen-joyce holly-elmore hope-woodard
imara-jones isabel-carlisle isabelle-boemeke jenay-manley jennifer-kavanagh jerusalem-demsas jessica-chen-weiss jessica-mccabe jessica-valenti
jill-filipovic jill-jacobs joy-ann-reid justine-bateman kara-dansky karen-hao karla-ortiz kate-raworth katherine-boyle kelley-robinson
kimberley-strassel kim-iversen krystal-ball kristan-hawkins laura-loomer laura-shin lila-rose lina-khan liv-boeree louise-perry lyn-alden
mariame-kaba maria-elvira-salazar marjorie-dannenfelser marjorie-taylor-greene mary-annaise-heglar mary-anne-franks mary-harrington
matika-wilbur mayra-flores medea-benjamin meghan-murphy megyn-kelly meredith-whittaker molly-white monica-guzman nadia-bolz-weber
nadine-strossen natalie-brunell natalie-wynn nellie-bowles nikole-hannah-jones nina-jankowicz pam-grossman paola-ramos paula-white-cain
pavlina-tcherneva pramila-jayapal rachel-maddow rashida-tlaib renee-diresta robin-wall-kimmerer sally-fallon-morell sara-nelson sarah-isgur
sarah-longwell sharon-brous simone-zimmerman stefanie-fox stephanie-kelton suhag-shukla sunita-viswanath tara-brach tara-leigh-cobble
tara-raghuveer timnit-gebru virginia-sole-smith winona-laduke yvette-carnell zephyr-teachout abigail-shrier margaret-killjoy red-scare
anne-helen-petersen'''.split())
MIXED = {'zac-davis-ashley-mckinless','simone-malcolm-collins'}
NONBINARY = {'devon-price','audrey-tang'}  # Tang self-describes as post-gender
FLAGS = {  # landmark -> flag text for Benjamin (kept in data; not removed)
 'nick-fuentes':'Possible harassment/incitement-primary output; movement widely described as white nationalist. Keep descriptively or exclude?',
 'joel-webbon':'Confrontational livestream output; D5 asked for harassment-exclusion review.',
 'timothy-gordon':'Combative output; D5 asked for harassment-exclusion review.',
 'mohammed-hijab':'Confrontational street-debate output; D5 asked for harassment-exclusion review. UK-based.',
 'myron-gaines':'2025 political drift of Fresh & Fit toward far-right content; review against harassment/incitement bar.',
 'andrew-tate':'High-profile; output primarily commentary/self-help per D6, but review against harassment bar.',
 'tristan-tate':'As Andrew Tate.',
 'alex-jones':'Long history of output courts found defamatory; now on AlexJonesLive. Keep descriptively or exclude?',
 'jared-taylor':'Self-described white advocate; legal and public, but confirm inclusion.',
 'sneako':'Aligned with Fuentes; review with Fuentes decision.',
 'laura-loomer':'Output centred on targeting named individuals for firing; review against harassment bar.',
 'clavicular':'Young (20) creator in a minors-dense scene; confirm comfort with inclusion.',
}
TRIM = {
 'mike-pence':'Low longform, unverified; hawks niche at cap.', 'moses-mcpherson':'Orthodox niche over cap; medium edge.',
 'trevin-wax':'Reformed/TGC niche over cap; medium edge.', 'stephen-gomes':'Low longform; author-proximate bioregional scene kept lean.',
 'jacob-mchangama':'Non-US, unverified; free-speech niche over cap.', 'divya-siddarth':'Low longform, unverified.',
 'kelley-robinson':'Low longform, unverified.', 'stefanie-fox':'Low longform, unverified (D8 itself flagged).',
 'adrian-vermeule':'Low longform (text-only), unverified; integralism represented by Pecknold.', 'byron-donalds':'Low longform, unverified elected official.',
 'dryden-brown':'Low longform, unverified.', 'adam-back':'Low longform, unverified.', 'jake-chervinsky':'Low longform, unverified.',
 'lewis-bollard':'Low longform, unverified.', 'sean-o-brien':'Low longform, unverified.', 'dean-spade':'Low longform, unverified; niche keeps Kaba as bridger.',
 'pramila-jayapal':'Low longform, unverified elected official.', 'ralph-reed':'Low longform, unverified.',
 'marjorie-dannenfelser':'Low longform, unverified.', 'mark-kern':'Low longform, unverified.',
}
def apply(niches,lms):
    for t in TRIM:
        if t in lms:
            l=lms.pop(t); niches.setdefault('_trimmed',{})
            niches['_trimmed'][t]=(l['name'],l['primary_niche'],TRIM[t])
    tr=niches.pop('_trimmed',{})
    for N in niches.values():
        N['atlas_match']=ATLAS.get(N['niche_id'])
        p=P.get(N['niche_id'],('?','?','?'))
        N['placement']={'left_right':p[0],'atlas_accelerate_restrain':{'A':'accelerate','R':'restrain','-':'neutral/mixed'}.get(p[1],p[1]),
                        'atlas_institutions_exit':{'W':'within-institutions','E':'exit','-':'neutral/mixed'}.get(p[2],p[2]),'basis':'QA judgment, rough'}
    for l in lms.values():
        lid=l['landmark_id']
        l['gender']='female' if lid in FEMALE else 'mixed' if lid in MIXED else 'nonbinary' if lid in NONBINARY else 'male'
        l['flag_for_benjamin']=FLAGS.get(lid)
    apply.trimmed=tr
