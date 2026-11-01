"""Content hygiene: remove personal allegations / criminal / health / conduct claims; apply verified recent-claim fixes."""
import re
LM_WHY = {
 'clavicular': 'Most visible looksmaxxing streamer of 2025-26; uses PSL hierarchy framing. Adult (20 as of May 2026).',
 'michael-l-brown': 'Line of Fire radio host; Jewish-born charismatic theologian who debates cessationists and rabbis.',
 'shmuley-boteach': 'Rabbi, author, World Values Network founder; high-volume media and debate presence.',
 'mohammed-hijab': 'UK-based debater and dawah YouTuber (~1.3M subscribers) with a large US audience; debated Shmuley Boteach (2023).',
 'william-j-barber-ii': "Poor People's Campaign co-chair, Repairers of the Breach; led faith-based civil-disobedience actions and a 51-mile march (2025-26).",
 'chloe-cole': 'Detransitioner advocate (Do No Harm) and plaintiff in a high-profile gender-medicine case. Adult (b. 2004).',
 'jordan-b-peterson': 'We Who Wrestle with God (2024); declined to self-identify as Christian in a May 2025 Jubilee debate. On hiatus from new podcasting and lecturing in 2026; the podcast releases archived lectures weekly (June 2026). Large back-catalogue.',
 'alex-jones': 'Founder of Infowars (final broadcast ~30 Apr 2026); continues as host of AlexJonesLive.',
 'laura-loomer': 'Self-described loyalty enforcer of the MAGA movement; argues with both the Fuentes and Tucker camps.',
 'russell-brand': 'Stay Free with Russell Brand (Rumble); spirituality-to-Christianity convert and MAGA-adjacent; bridges wellness spirituality to the populist right.',
 'casey-means': 'Metabolic-health physician (Levels; Good Energy); MAHA spokesperson; her surgeon-general nomination was withdrawn in April 2026.',
 'marjorie-taylor-greene': 'Former MAGA congresswoman who broke with Trump over the Epstein files, foreign policy and healthcare costs; resigned from Congress effective January 2026; now a frequent guest on mainstream and independent shows.',
}
NICHE_FIX = {  # niche_id -> {field: new text}
 'looksmaxxing-blackpill': {'trajectory':'rising (mainstream breakout via Clavicular in 2025-26)',
    'notes':'STRICT under-18 exclusion: many looksmaxxing TikTokers and forum figures are minors; only confirmed adults are seeded. Androgenic held out until age is verified. Mike Mew is UK; included because central to the US mewing meme. Mapped descriptively.'},
 'alpha-hustle-masculinity': {'trajectory':'declining-to-stable (return to US Mar 2025; mainstream fatigue)',
    'notes':'Output is primarily commentary, self-help and business content; mapped descriptively. Adin Ross considered but primarily an entertainment streamer. Overlaps D1 online right. FLAGGED for Benjamin (see QA-REPORT).'},
 'charismatic-pentecostal': {'trajectory':'stable'},
 'meaning-crisis-religious-turn': {'trajectory':'stable (Peterson on hiatus from new output in 2026; Vervaeke and Douthat active)'},
 'conspirituality-sovereignty': {'trajectory':'splitting (one wing toward MAGA / Christian revival, one back toward ecological spirituality)'},
 'red-pill-dating': {'notes':'Kevin Samuels (d. 2022) excluded as inactive; lineage noted as sub-niche. Fresh & Fit moved toward far-right political content in 2025 (critics describe some of it as antisemitic); overlaps D1 online right; mapped descriptively. MGTOW folded in as a sub-niche. X handles for Gaines/Davis/Tomassi not re-verified. FLAGGED for Benjamin (Myron Gaines).'},
}
NOTE_SUBS = [  # regex on niche notes -> replacement
 (r"Brand is a UK figure whose audience is largely US\. His criminal trial \(from Oct 2026\) is noted factually; it does not exclude him under the brief, but his output volume may drop; flag for review\.",
  "Brand is a UK figure whose audience is largely US; 2026 output volume should be re-checked."),
 (r"Alex Jones: courts found his Sandy Hook statements defamatory; his overall output is broadcast commentary rather than primarily harassment, so he is included as an edge voice, but the orchestrator may choos[^.|]*\.?",
  "Alex Jones is included descriptively; FLAGGED for Benjamin (see QA-REPORT)."),
 (r"Matt Christman left Chapo \(health\), so not listed\.", "Matt Christman no longer co-hosts Chapo, so not listed."),
 (r"Tates face criminal charges \(trafficking/rape allegations, denied\); ", ""),
 (r"Clavicular has faced allegations involving a minor partner \(IBTimes\) and an April 2026 overdose; mapped descr\w*\.?", ""),
 (r"died in mid-2026 \(a tribute episode dated 2026-06-16 says he 'died recently after a period of illness'\)",
  "died on 27 May 2026 (VERIFIED at QA: Wikipedia citing the Obaugh Funeral Home obituary)"),
 (r"Cole's 2025-26 public speaking not directly confirmed \(lawsuit is\)\.", "Cole's 2025-26 public speaking not directly confirmed."),
 (r"Peterson's 2025-26 output is minimal; extraction will rely on 2024-May 2025 material\.",
  "Peterson's 2026 output is limited to archive releases; extraction should weight 2024-25 material."),
]
SCRUB = re.compile(r'overdos|rape|traffick|minor partner|criminal trial|misconduct investigation|Sandy Hook|(?<!mental )illness', re.I)
def apply(niches, lms):
    log=[]
    for lid,why in LM_WHY.items():
        if lid in lms and lms[lid]['why']!=why:
            log.append(f'landmark {lid}: why rewritten (was: "{lms[lid]["why"][:90]}...")'); lms[lid]['why']=why
    for nid,fx in NICHE_FIX.items():
        for k,v in fx.items():
            if nid in niches: log.append(f'niche {nid}: {k} rewritten'); niches[nid][k]=v
    for N in niches.values():
        for pat,rep in NOTE_SUBS:
            new=re.sub(pat,rep,N['notes'])
            if new!=N['notes']: log.append(f"niche {N['niche_id']}: notes scrubbed ({pat[:40]}...)"); N['notes']=new
    if 'network-state-charter-cities' in niches:
        niches['network-state-charter-cities']['notes'] += ' | [QA] Balaji Srinivasan\'s Network School acquired Farcaster from Neynar (15 Oct 2026; VERIFIED, The Block) and rebranded it as the Network State Protocol; a new platform venue for this niche.'
        niches['network-state-charter-cities']['sources'].append('https://www.theblock.co/news/ecosystems/2026-10-15-network-school-acquires-farcaster-from-neynar-418720')
    # Peterson verification status
    if 'jordan-b-peterson' in lms:
        lms['jordan-b-peterson']['verification']='verified'; lms['jordan-b-peterson']['active_2025_2026']=True
        lms['jordan-b-peterson']['sources'] += ['https://www.dailywire.com/news/dr-jordan-b-peterson-returns-to-his-roots-with-answer-the-call','https://www.ibtimes.com.au/jordan-peterson-archived-lectures-health-update-1871112']
    if 'alex-jones' in lms:
        lms['alex-jones']['platforms']['other']='AlexJonesLive (successor show and app, May 2026)'
        lms['alex-jones']['sources'].append('https://barrettmedia.com/2026/05/01/alex-jones-signs-off-from-infowars/')
    # residual scan
    for N in niches.values():
        for k in ('description','trajectory','notes','telos'):
            if SCRUB.search(N[k]): log.append(f"RESIDUAL niche {N['niche_id']}.{k}: {SCRUB.search(N[k]).group(0)}")
    for l in lms.values():
        if SCRUB.search(l['why']): log.append(f"RESIDUAL landmark {l['landmark_id']}: {SCRUB.search(l['why']).group(0)}")
    return log
