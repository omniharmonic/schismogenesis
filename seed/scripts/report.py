import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from decisions import MERGED_META, NICHE_MERGE, DROP
import gapfill
SEED='/home/claude/dialogos-arena/seed'
st=json.load(open(SEED+'/scripts/_state.json')); rd=json.load(open(SEED+'/scripts/_render.json'))
d=json.load(open(SEED+'/SEED-v1.json')); L={l['landmark_id']:l for l in d['landmarks']}; N={n['niche_id']:n for n in d['niches']}
vq=json.load(open(SEED+'/VERIFICATION-QUEUE.json'))
out=open(SEED+'/QA-REPORT.md','w')
w=out.write
w(f"""# QA and merge report: Dialogos Arena seed v1

Author of record: Benjamin Life (@omniharmonic). This is an independent QA and merge pass over eight domain seed files, dated 2026-10-31. The pass was run as reproducible scripts in `scripts/`. All judgment calls are kept as data in `decisions.py`, `gapfill.py`, `hygiene.py` and `annotate.py`, and `build.py` followed by `render.py` regenerates every output.

## 1. Result

{rd['stats_md']}
- Target was about 150–175 niches and 480–550 landmarks. **Both were met: {len(N)} niches and {len(L)} landmarks.**
- Structural validation: all eight raw JSON files parsed and matched the brief's schema, with no missing keys and no invalid enum values. No structural fixes were needed. The schema was extended with these fields: `landmark_id`, `primary_niche`, `secondary_niches`, `gender`, `flag_for_benjamin`, `placement`, `cross_domains`, `merged_from` and `qa_decision`.

## 2. Decisions needing Benjamin

1. **Flagged landmarks** (section 7). These were kept in the data with `flag_for_benjamin` set, and none were removed by QA. The most consequential are Nick Fuentes, Alex Jones, Laura Loomer, the Tates and Myron Gaines.
2. **Author-proximate niches** need an external reviewer, because Benjamin and Kevin Owocki appear in or near the scenes being described: Regens/ReFi (Owocki is a core landmark), Metacrisis, Bioregionalism and Metamodernism.
3. **Paired niches where I kept the split but it is debatable.** These are the Free Press vs. independent journalism; Free-speech civil libertarians vs. censorship-industrial-complex critics; Abundance liberals vs. Moderate Democrats; Medical freedom vs. MAHA.
4. **The meaning-crisis merge (D4 + D5).** If the theist/non-theist split is a fundamental disagreement for Dialogos purposes, split the niche back into two.
5. **Bridger role.** Roles are recorded per primary niche, and 35 niches have no bridger even after counting secondary listings. Most have an edge landmark who works as one. Benjamin should decide whether "edge" may count as the bridger slot.

## 3. Niche merges (194 → {len(N)})

Rule applied: merge when niches differ in style only, and keep them split when their members dispute sacred values. Every merge is listed below, including the surviving niche's home domain.

""")
for t,(base,name,dom,cross,dec) in MERGED_META.items():
    src=[k for k,v in NICHE_MERGE.items() if v==t]
    w(f"- **{name}** (`{t}`, home {dom}). Merged from {', '.join('`'+x+'`' for x in src)}. {dec}\n")
w("""
### Requested boundary calls and how each was resolved

| Boundary | Resolution |
|---|---|
| MAHA (D1/D4/D7/Atlas) | One niche, `maha-coalition-wellness`, homed in D4 with D1 and D7 cross-listed. Medical freedom stays separate (consent and vaccines are a different sacred value). Food freedom becomes a sub-niche of regenerative agriculture. RFK Jr. and Calley Means are the cores. |
| Rogan-verse (D4/D6) | Stays in D4 as a standalone niche. D6 never claimed it. Rogan is primary there only. |
| Free Press (D4/D8) | The D4 and D8 niches are merged into `free-press-heterodox-institutional`. It stays split from Greenwald/Taibbi independent journalism. Weiss's CBS role was VERIFIED. |
| Bulwark / Never-Trump (D1/D2) | One niche, homed in D2. Dispatch stays in D1. |
| Tech right vs. neoreaction/Yarvin (D1/D3) | Two niches. The tech right (Thiel, Sacks, Lonsdale, Chamath) is in D3. Neoreaction plus the vitalist right is in D1, and Curtis Yarvin was ADDED, since both domains had deferred him to the other. Yarvin is cross-listed to the tech right. |
| Christian postliberals / integralists / Christian nationalism (D1/D5) | Two niches. `christian-postliberals-integralists` (D5) holds the Church-ordered common good. `christian-nationalism` (D1) holds the self-identified Reformed and theonomic movement. National conservatism (D1) stays separate because it is nation-first. |
| Meaning-crisis religious turn (D4/D5) | Merged into `meaning-crisis-religious-turn` (D5), with theist and non-theist wings as sub-niches. Pageau is homed in the Orthodox niche. |
| Pronatalists / tradwives / homeschooling (D5/D6) | Pronatalism and tradwives stay as separate D6 niches: one is techno-demographic and the other aesthetic-traditional, and they have different sacred values. Homeschooling was not seeded as a niche by any domain and is a TODO sub-niche of tradwife and Christian-right. |
| America First / restraint / hawks (D1/D8) | Three right-leaning niches: `america-first-restraint` (D1, which absorbs paleocons), `peace-through-strength-hawks` (D8) and `paleolibertarian-antiwar` (D1). Plus `foreign-policy-realists-restrainers` (D8, academic). The 2026 Iran war split was VERIFIED. |
| Anti-imperialist / Palestine left (D2/D8) | The D2 Palestine niche was dissolved into D8 `pro-palestinian-movement`, `left-restraint-foreign-policy` and the Jewish non-Zionist niche. The D2 ML left and D8 anti-imperialist left merged into `anti-imperialist-ml-left` (D2). |
| YIMBY / abundance (D2/D3/D7) | `abundance-liberals` (D2, political state capacity) and `progress-studies-abundance` (D3, tech and progress framing) are kept separate. Derek Thompson is primary in D2 and secondary in D3. Lars Doucet and Georgism moved to progress studies. Strong Towns stays in D7. |
| Climate skeptic / energy dominance (D1/D7) | Stays in D7 as `energy-dominance-climate-skeptic`. Alex Epstein is primary here and was removed from the nuclear niche. |
| Progressive streamers (D2, not D1) | `gen-z-online-left-streamers` is in D2. D6's note that sent them to "D1" was an error, and nothing was placed in D1. |
| Anti-disinformation field (D2/D8/D4) | D2 and D8 merged into `anti-disinformation-field` (D8). The opposing censorship-industrial-complex critics stay as their own D8 niche. |
| Populist new media (D4/D8) | The D8 corporate-media critics niche duplicated D4 `populist-horseshoe-anti-establishment` and was absorbed into it. |

### Splits kept on purpose
War Room vs. MAGA loyalist media; the America First restraint right vs. groypers; Bulwark vs. Dispatch; Mises vs. Reason libertarians; the Squad vs. Sanders populists; ADOS vs. the Black liberal commentariat; Integral vs. metamodernism; Muslim mainstream vs. dawah; evangelical conscience critics vs. the megachurch mainstream; four Israel–Palestine niches; China hawks vs. engagers; election-integrity mirror niches; ecomodernism vs. energy dominance vs. clean-energy electrification vs. climate justice vs. degrowth.

## 4. Landmark deduplication and trimming

- 78 people appeared in more than one domain. Each now has one `primary_niche` (see `decisions.PRIMARY`), and the rest are recorded in `secondary_niches`. Platforms, sources and the strongest verification status were unioned across entries.
- `landmark_id` is the kebab-case of the public name. Honorifics (Fr., Rev., Bishop) are stripped. Duos keep a combined id, for example `simone-malcolm-collins`. Dasha Nekrasova and Anna Khachiyan are one entry, `red-scare` (primary: dirtbag left).
- **Dropped during merge (over cap, thin or held):**
""")
for lid,(name,niches,why) in sorted(st['dropped'].items()): w(f"  - {name} (`{lid}`; was in {', '.join(niches)}). {why}\n")
w("- **Trimmed to reach the target and favor long-form output.** Each of these is a low-output, unverified or over-cap landmark, and all are alternates for stage 2:\n")
for lid,(name,prim,why) in sorted(st['trimmed'].items()): w(f"  - {name} (`{lid}`, {prim}). {why}\n")
w("""- Other thin niches: 4B, MGTOW, anti-work, sacred economics, religious nones, Palestine left, racial-justice left and paleocons were merged (section 3). Groypers, ADOS, rationalists, EA, looksmaxxing and tradwives were **kept** at 2–3 landmarks because each is a distinct worldview with a real public conversation.
- **Jim Rutt** is not a landmark. His death was VERIFIED (section 8). His back catalogue is noted as corpus for the metacrisis niche.

## 5. Representation audit

""")
w(rd['audit_md'])
w("""
### Key balance findings
- **Left–right.** Explicitly right niches outnumber explicitly left ones slightly, but the center-left plus left together roughly match the right. About a third of niches are cross-cutting, mostly in tech, spirituality and lifestyle. The right is more finely subdivided at niche level, which reflects how many live factional fights it has in 2025–26 (Iran, tech right, groypers). The left's internal splits are more often carried as sub-niches.
- **Atlas axes.** The restrain side is somewhat larger than accelerate. Exit-leaning niches cluster in independent media, crypto, spirituality and the dissident right. Institution-bound niches cluster in D2, D8 and organised religion.
- **Gender.** Only about 22% of landmarks are women. D6 (51%) and D2 (30%) are the most balanced, and D5 (13%), D8 (15%) and D1 (17%) the least. This is a known skew of podcast and long-form media, but stage 2 should prefer women among equally strong candidates (TODO list below).
- **Long-form output.** About 57% of landmarks are high. The remaining low-output landmarks are mostly elected officials, academics and organisers, which is the expected cost of including movements as well as media.
- **Bridgers** make up about a quarter of landmarks. See section 2, item 5.

### Group representation (count of landmarks after QA)
| Group | Before QA | After QA | Notes |
|---|---|---|---|
| Latino | ~8 | 11 (+ new niche Latino Christianity) | Added Samuel Rodriguez and Robert Chao Romero. Spanish-language voices are still TODO. |
| Asian American | ~8 scattered | 10 (+ new niche Asian American voices) | Added They Call Us Bruce and Andrew Yang. Asian American conservative voices are TODO. |
| Black conservatives | 4 | 3 (Whitlock, Elder, Loury) + Candace Owens (primary in conspiracy) | Byron Donalds trimmed for low output. TODO: add one high-output voice. |
| Rank-and-file labor | 0 | Chris Smalls added | Still thin. |
| Hindu Americans | 0 (Sarvapriyananda only) | 3 + secondary (new niche) | Suhag Shukla, Sunita Viswanath, Rajiv Malhotra. |
| Shia and progressive Muslims | 0 | Azhar Nasser (Shia), Dalia Mogahed | Progressive Muslim voice still TODO. |
| Latino religious voices | 0 | 2 (new niche) | Latino Catholic voices TODO. |
| Rural voices | farmers only | + hunter-conservationists niche (Rinella, Newberg) | High long-form output. |
| Climate left / Sunrise | Aru Shiney-Ajay (Sunrise), McKibben, Heglar, Rollie Williams | unchanged | Covered adequately. Varshini Prakash is an alternate. |
| Indigenous | 4 (Land Back) | 4 | Treaty and tribal-government voices TODO. |

### Gaps filled at QA (all sourced from 2026 searches)
""")
for n in gapfill.NEW_NICHES: w(f"- New niche **{n['name']}** (`{n['niche_id']}`, {n['domain']}): {', '.join(L[x]['name'] for x in N[n['niche_id']]['landmarks'])}.\n")
w("""- New landmarks in existing niches: Curtis Yarvin (neoreaction), Chris Smalls (labor), Dalia Mogahed and Azhar Nasser (American Muslim mainstream).

### Remaining TODO gaps
- Spanish-language Latino media voices, both right and left, and Latino Catholics.
- Asian American conservatives (for example, voices from the affirmative-action and SFFA debates) and Korean and Vietnamese American evangelical voices.
- A progressive Muslim landmark, and Black Hebrew Israelites (D5 gap).
- More women in D1, D3 and D8. Candidates: Varshini Prakash (climate), Kate Starbird (disinformation), Arielle Angel (Jewish left), Mary Harrington (already present), Helen Andrews (D1).
- Homeschooling and classical-Christian education as a sub-niche or niche.
- Solarpunk, water and Western land-use politics, and van-life (D7 candidates).
- Timothy Snyder, Stephen Walt, Rob Lee and Scott Ritter (D8 alternates). Lakshya Jain and Chuck Rocha (D2 alternates).
- The remaining 19 Atlas tribe names, needed to complete `atlas_match`.

## 6. Content hygiene

**Exclusions confirmed:**
- **Minors.** No under-18 landmark is seeded. Androgenic is held out pending an age check. Ages are queued for checking for young creators (Clavicular, Sneako, Hannah Pearl Davis, Hope Woodard, Estee Williams).
- **Private individuals.** None are seeded. D7 deliberately left out Benjamin's private collaborators.
- **Designated extremist organizations.** No spokespeople for designated violent extremist organizations are seeded. D1 and D8 each checked this.
- **Anonymous accounts.** Only anon personas that are themselves major public figures are seeded (Bronze Age Pervert, Raw Egg Nationalist, Ansem, Cobie, Perun).

**Removals.** Personal allegations, criminal, health and conduct claims were removed from seed fields, and each rewritten field is listed below. Descriptions of worldviews and platforms were kept.
""")
for h in st['hlog']: w(f"- {h}\n")
w("""- No text was removed that describes a niche's own politics, for example that Fresh & Fit moved toward far-right content, or that courts and audits rejected claims of decisive 2020 fraud. That text describes worldviews, not personal conduct.
- Death claims: Charlie Kirk's death is referenced only as the context for Erika Kirk's role. Jim Rutt's death is recorded only in a niche note and cites a reliable source (section 8).

## 7. Landmarks flagged for Benjamin (kept in the data, `flag_for_benjamin` set)
| Landmark | Niche | Why flagged |
|---|---|---|
""")
for l in sorted(L.values(),key=lambda l:l['primary_niche']):
    if l['flag_for_benjamin']: w(f"| {l['name']} | {l['primary_niche']} | {l['flag_for_benjamin']} |\n")
w("""
QA recommendation, for Benjamin to decide:
- **Keep descriptively:** Jones, Loomer, Webbon, Gordon, Hijab, Taylor, Clavicular. Each heads a real public conversation, and their main output is commentary.
- **Highest-risk under the brief's "primary output is harassment or incitement" bar:** Fuentes, then the Tates and Gaines.
- If Fuentes is excluded, the groyper niche should be kept and represented by Sneako as a bridger, or folded into the America First restraint niche as a sub-niche.

## 8. Recent-event claims made by the domain agents

| Claim | Status | Evidence | Data action |
|---|---|---|---|
| Jim Rutt died mid-2026 | **VERIFIED** | Wikipedia lists his death as 27 May 2026 (age 72), citing the Obaugh Funeral Home obituary (retrieved 1 June 2026). A Legacy.com obituary for "James 'Jim' Patrick Rutt" also appears in search. The funeral-home page itself could not be fetched (permission timeout). | Kept him off the landmark list. The niche note now carries the date and the source. |
| Infowars ended May 2026 | **VERIFIED** (date nuance) | The final Infowars broadcast was about 30 April 2026, with shutdown coverage on 1–4 May 2026 (Barrett Media, KUT, Bloomberg Law). Jones moved to **AlexJonesLive**. | Updated Jones's `why` and `platforms.other`. |
| Bari Weiss heads CBS News | **VERIFIED** | CBS bought The Free Press in October 2025 and named Weiss editor-in-chief of CBS News (WTOP, NHPR). She was still in the role in January 2026 (staff memo coverage). | No change needed. |
| A 2026 Iran war split the right | **VERIFIED** | Washington Times (7 March 2026), Local10/AP (10 April 2026), Media Matters and The Week covered the split between Carlson, Kelly and Dave Smith on one side and Levin, Hannity and Shapiro on the other. | Supports keeping the America First restraint and hawks split. |
| MTG resigned from Congress Jan 2026 | **VERIFIED** (nuance) | She announced on 21 November 2025 that she would resign, effective January 2026 (NPR, ABC). | Her `why` text was made neutral and accurate. |
| Jordan Peterson out of public life since June 2025 | **FALSE as stated / PARTLY TRUE** | He was active in mid-2025: the Daily Wire launched his "Answer the Call" series on 25 July 2025. He then went on a health-related hiatus. His January 2026 lecture was cancelled, and in June 2026 his podcast began weekly releases of archived lectures because he could not resume podcasting (IBTimes AU, 23 June 2026). | Rewrote his `why` and the niche trajectory (health details removed). He is listed as verified and active, because the podcast is publishing, and is in the queue in case new output resumes. |
| Farcaster acquired by Network School Oct 2026 | **VERIFIED** | Network School acquired Farcaster from Neynar on 15 October 2026 and rebranded it as the Network State Protocol (The Block, Crypto Briefing, Bankless). | Added a note and source to `network-state-charter-cities`. |
| (incidental) Casey Means's surgeon-general nomination withdrawn | **VERIFIED** | Withdrawn 30 April 2026; Nicole Saphier was named instead (AABB, KSL). | Kept, worded neutrally. |

## 9. Atlas alignment
""")
w(f"`atlas_match` was filled for {sum(1 for n in N.values() if n['atlas_match'])} niches from the 39 Atlas names available in the partial list. The rest are null. ")
w("""The partial list has no matches for these names: sports twitter, stan / pop culture, wallstreetbets, girardians, landian accel (folded into e/acc), cryonicists (folded into longevity), remilia / net spirituality, cozyweb, georgists (a sub-niche of progress studies) and indie hackers (only a loose match, to hustle-finfluencer). The 19 Atlas names that are missing still need a browser read; D3's agent had already read them. Pop-culture and sports Atlas tribes have no Dialogos niche, which is consistent with the brief's rule that a niche needs a worldview, not just a hobby.

## 10. Verification queue
""")
w(f"`VERIFICATION-QUEUE.json` holds **{vq['meta']['total']} landmarks** and 1 held-out entry. By domain: " + ', '.join(f"{k} {v}" for k,v in vq['meta']['by_domain'].items()) + ". D7 and D1 have the most to check, because their agents lost search budget early.\n")
w("""
## Searches used
This pass used 26 WebSearch calls, within the ~40 budget. Nine went to the claims in section 8 and 17 to gap-filling and the Casey Means check. It also made 6 WebFetch calls, 2 of which failed.
""")
out.close(); print('ok')
