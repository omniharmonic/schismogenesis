"""SEED-v2: apply verification batches A-D to SEED-v1.

Run:  python3 -I scripts/apply_verification.py
Reads SEED-v1.json + verify/batch-{A,B,C,D}.json (latest batch wins, A<B<C<D).
Writes SEED-v2.json, SEED-v2.md, VERIFICATION-SUMMARY.md.
SEED-v1 artefacts and the v1 scripts (build.py, render.py, report.py) are not touched.
Balance tables reuse the v1 render.py table layout (same helper and columns).
"""
import json, collections, copy, os, sys
SEED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = '2026-10-31'
DOM = ['d1-right','d2-left-center','d3-tech-futures','d4-heterodox-sensemaking','d5-religion-spirituality','d6-gender-lifestyle-subcultures','d7-economy-ecology-place','d8-geopolitics-media']
DN = {'d1-right':'D1 Right','d2-left-center':'D2 Left & center','d3-tech-futures':'D3 Tech & futures','d4-heterodox-sensemaking':'D4 Heterodox & sensemaking','d5-religion-spirituality':'D5 Religion & spirituality','d6-gender-lifestyle-subcultures':'D6 Gender, lifestyle & subcultures','d7-economy-ecology-place':'D7 Economy, ecology & place','d8-geopolitics-media':'D8 Geopolitics & media'}
STATUSES = ['verified-active','pending','stale','excluded']
LF = {'high':3,'medium':2,'low':1}; RR = {'core':3,'bridger':2,'edge':1}

v1 = json.load(open(SEED+'/SEED-v1.json'))
queue = json.load(open(SEED+'/VERIFICATION-QUEUE.json'))
qids = {x['landmark_id'] for v in queue['queue'].values() for x in v}
L = {l['landmark_id']: copy.deepcopy(l) for l in v1['landmarks']}
N = {n['niche_id']: copy.deepcopy(n) for n in v1['niches']}

# ---------------------------------------------------------------- batches (latest wins)
FINAL, HIST = {}, collections.defaultdict(list)
for b in 'ABCD':
    for r in json.load(open(f'{SEED}/verify/batch-{b}.json')):
        FINAL[r['landmark_id']] = (b, r); HIST[r['landmark_id']].append(b)
missing_q = qids - set(FINAL)
assert not missing_q, f'queue items without a result: {missing_q}'

# ---------------------------------------------------------------- platform-correction overrides
# Most corrections are clean replacement values. These are notes/instructions, so they are
# resolved by hand into a usable platform value (the raw correction is still kept in the log).
P_OVERRIDE = {
  ('sean-hannity','podcast'): 'The Sean Hannity Show; Hang Out with Sean Hannity (Fox News Media podcast)',
  ('rachel-maddow','podcast'): 'Rachel Maddow Presents (MSNBC/MS NOW); The Rachel Maddow Show (MS NOW audio feed)',
  ('greg-lukianoff','podcast'): 'So to Speak (FIRE-affiliated feed; hosted by Nico Perrino, not Lukianoff)',
  ('greg-lukianoff','substack'): 'https://substack.com/@glukianoff (unverified as active); FIRE blog "The Eternally Radical Idea" https://www.thefire.org/news/blogs/eternally-radical-idea',
  ('jesse-jenkins','podcast'): 'Shift Key (Heatmap) - retitled "Shift Key with Robinson Meyer"; Jenkins not named in recent episodes',
  ('lina-khan','x'): '@linakhanFTC (likely outdated since she left the FTC; re-check)',
  ('alan-fisher','youtube'): 'https://www.youtube.com/@ArmchairUrbanist (channel now titled "Alan Fisher"; verify handle)',
  ('clavicular','other'): 'Kick livestreams; TikTok; Instagram @clavicular0',
  ('paul-saladino','podcast'): 'Paul Saladino MD podcast (Apple id1461771083; formerly "Fundamental Health")',
  ('randall-carlson','podcast'): 'Squaring The Circle, A Randall Carlson Podcast (libsyn feed rss.libsyn.com/shows/511063)',
  ('daniel-christian-wahl','substack'): None,   # Medium URL moved to `other` by the same correction
  ('casper-ter-kuile','podcast'): None,         # seed value was the literal "UNVERIFIED"; no current show found
}

# ---------------------------------------------------------------- step 1/2: apply verification
plog, lflog = [], []
for lid, l in L.items():
    l['verification_v1'] = l['verification']
    l['verification_batches'] = HIST.get(lid, [])
    if lid in FINAL:
        b, r = FINAL[lid]
        st = r['status']; assert st in STATUSES, (lid, st)
        l['verification'] = st
        l['active_2025_2026'] = True if st == 'verified-active' else (False if st == 'stale' else None)
        l['evidence_url'] = r['evidence_url']; l['evidence_date'] = r['evidence_date']
        l['last_checked'] = TODAY
        l['verification_source'] = f'verify/batch-{b}.json'
        l['verification_notes'] = r['notes']
        for k, v in r['platform_corrections'].items():
            old = l['platforms'].get(k)
            new = P_OVERRIDE.get((lid, k), v)
            if isinstance(new, str) and new.startswith('CORRECTION: '): new = new[len('CORRECTION: '):]
            if old != new:
                l['platforms'][k] = new
                plog.append(dict(landmark_id=lid, field=k, old=old, new=new, raw=v, batch=b))
        if r['longform_output'] != l['longform_output']:
            lflog.append(dict(landmark_id=lid, old=l['longform_output'], new=r['longform_output'], batch=b))
            l['longform_v1'] = l['longform_output']; l['longform_output'] = r['longform_output']
        if r['evidence_url'] and r['evidence_url'] not in l['sources']: l['sources'].append(r['evidence_url'])
    else:
        assert l['verification'] == 'verified', lid
        l['verification'] = 'verified-active'
        l['evidence_url'] = None; l['evidence_date'] = None
        l['last_checked'] = TODAY
        l['verification_source'] = 'SEED-v1 (verified by domain agent or QA during the v1 build; not re-checked in batches A-D)'
        l['verification_notes'] = None
    l['us_focus_flag'] = False; l['us_focus_note'] = None
    l['open_checks'] = []
    l['replaces'] = None; l['replaced_by'] = None; l['converted_from'] = None
    l['record_type'] = 'person'

# ---------------------------------------------------------------- step 3: sourced replacements for stale/failed records
REPLACEMENTS = [dict(
    old='jesse-jenkins',
    reason='Batch C: Shift Key is now "Shift Key with Robinson Meyer" and recent episodes (through ep 158, 2026-10-29) name Meyer as sole host; Jenkins appears to have left the show and no dated personal item was found.',
    new=dict(landmark_id='robinson-meyer', name='Robinson Meyer', primary_niche='clean-energy-electrification', secondary_niches=[],
        role='core', why='Heatmap journalist and sole current host of the weekly Shift Key podcast on climate, clean energy and electrification policy.',
        platforms={'podcast':'Shift Key with Robinson Meyer https://shows.acast.com/shift-key/episodes','other':'https://heatmap.news/podcast'},
        longform_output='high', gender='male', flag_for_benjamin=None,
        sources=['https://shows.acast.com/shift-key/episodes'], source_domains=['verify-batch-C'],
        evidence_url='https://shows.acast.com/shift-key/episodes', evidence_date='2026-10-29 (Shift Key ep 158; show-level evidence)'))]
for rp in REPLACEMENTS:
    o = L[rp['old']]
    o['verification'] = 'stale'; o['active_2025_2026'] = None
    o['replaced_by'] = rp['new']['landmark_id']
    o['verification_notes'] = (o['verification_notes'] or '') + ' | SEED-v2: marked stale as a landmark (no longer hosts the show this record relies on); kept, not deleted. ' + rp['reason']
    n = dict(rp['new']); n.update(domain=N[n['primary_niche']]['domain'], verification='pending', verification_v1=None, active_2025_2026=None,
        last_checked=TODAY, verification_source='verify/batch-C.md (replacement recommendation)', verification_batches=['C'],
        verification_notes=f"Added in SEED-v2 as the sourced replacement for {rp['old']}. Pending until a person-level check is done. {rp['reason']}",
        us_focus_flag=False, us_focus_note=None, open_checks=['person-level verification of the replacement'], replaces=rp['old'], replaced_by=None,
        converted_from=None, record_type='person')
    L[n['landmark_id']] = n

# ---------------------------------------------------------------- step 4: show-not-person records -> host records
CONVERT = {
  'red-scare': [('dasha-nekrasova','Dasha Nekrasova','female',{'podcast':'Red Scare - https://podcasts.apple.com/us/podcast/red-scare/id1364798971'}),
                ('anna-khachiyan','Anna Khachiyan','female',{'podcast':'Red Scare - https://podcasts.apple.com/us/podcast/red-scare/id1364798971','x':'@annakhachiyan'})],
  'conspirituality-podcast-hosts': [(i,nm,'male',{'podcast':'Conspirituality https://podcasts.apple.com/ca/podcast/id1515827446'}) for i,nm in
                [('derek-beres','Derek Beres'),('matthew-remski','Matthew Remski'),('julian-walker','Julian Walker')]],
}
WHY = {'red-scare': "Red Scare co-host; 'post-left' cultural contrarian whose show sits between the dirtbag left and the heterodox/right scene.",
       'conspirituality-podcast-hosts': 'Co-host of the Conspirituality podcast, which named and tracks the wellness-to-conspiracy pipeline.'}
converted = {}
for old, hosts in CONVERT.items():
    src = L.pop(old); converted[old] = [h[0] for h in hosts]
    for hid, nm, g, plat in hosts:
        h = copy.deepcopy(src)
        h.update(landmark_id=hid, name=nm, gender=g, platforms=plat, why=WHY[old], converted_from=old, record_type='person')
        h['verification_notes'] = (src['verification_notes'] or '') + f' | SEED-v2: split from show record `{old}`; evidence is show-level.'
        L[hid] = h
# multi-person records that name real people (not shows): keep, flag for a possible split
DUOS = [lid for lid, l in L.items() if l['gender'] == 'mixed' or ' & ' in l['name']]
for lid in DUOS:
    L[lid]['record_type'] = 'multi-person'
    L[lid]['open_checks'].append('multi-person record: consider splitting into person-level records')

# ---------------------------------------------------------------- step 5: non-US voices (batch C)
NON_US = {'jason-slaughter':'Amsterdam','canadian-prepper':'Canada','ed-winters':'UK','hannah-ritchie':'UK','kate-raworth':'UK',
          'bjrn-lomborg':'Denmark','kohei-saito':'Japan','jason-hickel':'Barcelona','daniel-christian-wahl':'Mallorca',
          'bayo-akomolafe':'Nigerian-born; base unverified','peter-singer':'Australian'}
for lid, loc in NON_US.items():
    L[lid]['us_focus_flag'] = True
    L[lid]['us_focus_note'] = f'Non-US voice ({loc}) per verify/batch-C.md; decide whether central to a US niche.'
# other open checks noted in the batches (non-activity)
OPEN = {'hope-woodard':['age: no reliable source yet (batch B)','Boysober ended 2026-04; find next platform'],
        'estee-williams':['age: not checked (batch B/D)'],
        'raw-egg-nationalist':['US focus: persona may be UK-based (batch A/D); not in the batch-C list, so us_focus_flag not set'],
        'jared-taylor':['inclusion decision open (batch A/D)'],'nick-fuentes':['inclusion decision vs harassment/incitement bar (batch A/D)'],
        'andrew-tate':['inclusion decision open (batch D)'],'tristan-tate':['inclusion decision open (batch D)'],
        'lina-khan':['X handle likely outdated'],'daniel-denvir':['confirm whether The Dig still carries the Jacobin label'],
        'greg-lukianoff':['So to Speak is hosted by Nico Perrino; find a Lukianoff-hosted long-form feed']}
for lid, cs in OPEN.items(): L[lid]['open_checks'] += cs

EXCLUDED = []
for lid, (b, r) in FINAL.items():
    if lid not in L and r['status'] == 'excluded':
        EXCLUDED.append(dict(landmark_id=lid, name='Androgenic' if lid == 'androgenic' else lid, verification='excluded', active_2025_2026=None,
            evidence_url=r['evidence_url'], evidence_date=r['evidence_date'], platforms=r['platform_corrections'],
            last_checked=TODAY, verification_source=f'verify/batch-{b}.json', verification_notes=r['notes'], domain=r['domain']))
assert [e['landmark_id'] for e in EXCLUDED] == ['androgenic']

# ---------------------------------------------------------------- suggestions (NOT applied)
SUGGESTED = [
  ('adolph-reed-jr','core, class-first-heterodox-left','stale (latest dated item 2025-08-27)','Keep as a historical anchor marked stale, or demote to edge. No replacement needed: the niche keeps verified cores Briahna Joy Gray and Freddie deBoer.','batch D'),
  ('gregory-landua','core, regens-refi','pending; Planetary Regeneration Podcast dormant (last ep 2025-04-14)','Replacement still needs sourcing; no sourced candidate was found.','batch C'),
  ('casper-ter-kuile','core, post-religious-deconstruction-nones','pending; no current show or dated item','Promote tim-whitaker (The New Evangelicals, weekly) to core, or source a nones/deconstruction podcaster. https://podcasts.apple.com/qa/podcast/the-new-evangelicals-podcast/id1557794865','batch C'),
  ('jason-mankey','core, pagan-witchcraft','pending; latest item 2025-10-19 (guest spot)','Promote mat-auryn (co-host, The Circle Is podCAST) once a newer episode is confirmed. https://www.buzzsprout.com/2372877/episodes/18039324','batch C'),
  ('pavlina-tcherneva','core, mmt-heterodox-macro','pending; low longform','Promote warren-mosler or rely on stephanie-kelton (both pending).','batch C'),
  ('patrick-deneen / chad-pecknold','core, christian-postliberals-integralists','pending; Postliberal Order active but own bylines undated','Keep; clear with a dated byline on postliberalorder.com.','batch C'),
  ('david-cole','core, free-speech-civil-libertarians','pending; no dated item','Nico Perrino (FIRE), host of weekly So to Speak. https://podcasts.apple.com/us/podcast/id1108027131','batch B'),
  ('shayne-coplan','core, forecasters-prediction-markets','verified-active; low longform','A Chopping Block (Unchained) co-host such as Tom Schmidt or Tarun Chitra (not verified as people). https://haseebq.com/now/','batch A'),
  ('ansem / murad-mahmudov / cobie','crypto (d3)','low longform','A host with a regular crypto show, e.g. a Chopping Block co-host. https://unchainedcrypto.com/the-chopping-block-2025-winners-losers-2026-predictions/','batch A'),
  ('mayra-flores','core, hispanic-realignment-conservatives','low longform','Keep using the CC Originals ep104 interview, or add a Hispanic-right figure with a show (none named).','batch A'),
  ('hannah-neeleman','core, tradwife-trad-femininity','pending; low longform','A trad-femininity voice with a podcast, after verifying one (none named).','batch B'),
  ('jonathan-rowson','edge, metamodernism','pending; latest dated item 2024-12','Keep pending; Alexander Beiner (verified) covers the space.','batch B'),
  ('hope-woodard','edge, liberal-feminism','verified-active, but Boysober ended 2026-04','Re-verify her next platform before deciding.','batch B'),
  ('elbridge-colby','bridger, china-hawks','low longform (official)','Keep using hearings/FP Munich podcast as transcripts, or lean on Jennifer Kavanagh (already seeded).','batch B'),
  ('gabe-brown / justin-rhodes / andrew-millison','regen-ag / homesteading','pending; undated hits only','Keep; clear with a dated YouTube upload.','batch C'),
]

# ---------------------------------------------------------------- relink niches (as build.py does)
for l in L.values(): l['domain'] = N[l['primary_niche']]['domain']
VR = {'verified-active':0,'pending':1,'stale':2}
for n in N.values():
    ls = [l for l in L.values() if l['primary_niche'] == n['niche_id']]
    ls.sort(key=lambda l: (-RR[l['role']], VR[l['verification']], -LF[l['longform_output']], l['landmark_id']))
    n['landmarks'] = [l['landmark_id'] for l in ls]
    n['secondary_landmarks'] = sorted(l['landmark_id'] for l in L.values() if n['niche_id'] in l['secondary_niches'])
    va = [l for l in ls if l['verification'] == 'verified-active']
    n['verified_active_landmarks'] = len(va)
    n['has_verified_active_core'] = any(l['role'] == 'core' for l in va)

# ---------------------------------------------------------------- write SEED-v2.json
niches = sorted(N.values(), key=lambda n: (DOM.index(n['domain']), n['name']))
lms = sorted(L.values(), key=lambda l: l['landmark_id'])
ORDER_N = ['niche_id','name','domain','cross_domains','aliases','description','telos','sacred_values','existential_threats','combatants','adjacent_niches','sub_niches','size_estimate','cultural_influence','trajectory','atlas_match','limberg_barnes_match','placement','landmarks','secondary_landmarks','verified_active_landmarks','has_verified_active_core','merged_from','qa_decision','sources','notes']
ORDER_L = ['landmark_id','name','primary_niche','secondary_niches','domain','role','why','platforms','longform_output','active_2025_2026','verification','evidence_url','evidence_date','last_checked','verification_source','verification_batches','verification_notes','verification_v1','longform_v1','us_focus_flag','us_focus_note','open_checks','record_type','converted_from','replaces','replaced_by','gender','flag_for_benjamin','sources','source_domains']
def od(d, o):
    extra = set(d) - set(o); assert not extra, extra
    return {k: d.get(k) for k in o}
SC = collections.Counter(l['verification'] for l in lms)
meta = copy.deepcopy(v1['meta'])
meta.update(version='SEED-v2', generated=TODAY, author_of_record='Benjamin Life (@omniharmonic)',
    stage='Stage 1 seed - verification pass applied (batches A-D)',
    inputs=['SEED-v1.json','VERIFICATION-QUEUE.json']+[f'verify/batch-{b}.json' for b in 'ABCD']+[f'verify/batch-{b}.md' for b in 'ABCD'],
    counts=dict(niches=len(niches), landmarks=len(lms), excluded=len(EXCLUDED), v1_landmarks=len(v1['landmarks']),
                by_verification={s: SC[s] for s in STATUSES if s != 'excluded'}),
    scripts='SEED-v1: scripts/build.py, scripts/render.py, scripts/report.py. SEED-v2: scripts/apply_verification.py (reads SEED-v1.json + verify/*).')
meta['schema_notes'].update({
  'verification':'verified-active = dated 2025-10-31-or-later item found (or verified during the v1 build and not re-queued); pending = not confirmed within budget (NOT inactive); stale = latest dated item older than ~12 months, or the record no longer holds (see replaced_by); excluded = held out (see excluded_landmarks)',
  'active_2025_2026':'true iff verified-active; false iff stale by date; null = not confirmed',
  'verification_batches':'every batch that checked this record; the last one (verification_source) wins',
  'evidence_url/evidence_date':'from the winning batch; evidence_date is free text and may be approximate',
  'longform_v1 / verification_v1':'pre-v2 values, kept where v2 changed them',
  'us_focus_flag':'true = non-US voice per batch C; needs a decision on centrality to a US niche',
  'record_type':'person | multi-person (duo record naming real people; consider splitting)',
  'converted_from':'show-level v1 record this host record was split from (see meta.retired_ids)',
  'replaces/replaced_by':'sourced replacement pairs; the replaced record is kept and marked stale',
  'niche.verified_active_landmarks / has_verified_active_core':'computed over primary landmarks only'})
meta['retired_ids'] = converted
meta['platform_corrections_applied'] = len(plog); meta['longform_changes_applied'] = len(lflog)
out = dict(niches=[od(n, ORDER_N) for n in niches], landmarks=[od(l, ORDER_L) for l in lms], excluded_landmarks=EXCLUDED,
           suggested_swaps=[dict(landmark=a, slot=b, issue=c, suggestion=d, source=e) for a,b,c,d,e in SUGGESTED],
           change_log=dict(platform_corrections=plog, longform_changes=lflog), meta=meta)
json.dump(out, open(SEED+'/SEED-v2.json','w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- stats (render.py table layout)
def pct(a, b): return f'{100*a/b:.0f}%' if b else '-'
def table(rows, hdr):
    o = '| '+' | '.join(hdr)+' |\n|'+'---|'*len(hdr)+'\n'
    for r in rows: o += '| '+' | '.join(str(x) for x in r)+' |\n'
    return o
nL = len(lms); Lx = {l['landmark_id']: l for l in lms}
VA = [l for l in lms if l['verification'] == 'verified-active']
T_status = table([(s, SC[s], pct(SC[s], nL)) for s in ['verified-active','pending','stale']]+[('excluded (held out, not in landmarks)', len(EXCLUDED), '-')], ['Verification','Landmarks','Share'])
rows = []
for d in DOM:
    dl = [l for l in lms if l['domain'] == d]; dn = [n for n in niches if n['domain'] == d]
    rows.append((DN[d], len(dn), len(dl))+tuple(sum(1 for l in dl if l['verification']==s) for s in ['verified-active','pending','stale'])
                +(pct(sum(1 for l in dl if l['verification']=='verified-active'), len(dl)), f"{sum(n['has_verified_active_core'] for n in dn)}/{len(dn)}"))
rows.append(('**Total**', len(niches), nL, SC['verified-active'], SC['pending'], SC['stale'], pct(SC['verified-active'], nL), f"{sum(n['has_verified_active_core'] for n in niches)}/{len(niches)}"))
T_dom = table(rows, ['Domain','Niches','Landmarks','Verified-active','Pending','Stale','VA share','Niches with VA core'])
rc = collections.Counter((l['role'], l['verification']) for l in lms)
T_role = table([(r, sum(rc[(r,s)] for s in VR), rc[(r,'verified-active')], rc[(r,'pending')], rc[(r,'stale')]) for r in ['core','bridger','edge']], ['Role','Landmarks','Verified-active','Pending','Stale'])
lf = collections.Counter(l['longform_output'] for l in lms); lfv = collections.Counter(l['longform_output'] for l in VA)
lf1 = collections.Counter(l['longform_output'] for l in v1['landmarks'])
T_lf = table([(r, lf1[r], f'{lf[r]} ({pct(lf[r],nL)})', f'{lfv[r]} ({pct(lfv[r],len(VA))})') for r in ['high','medium','low']], ['Longform output','SEED-v1','SEED-v2 all','SEED-v2 verified-active'])
G = ['male','female','mixed','nonbinary']
g = collections.Counter(l['gender'] for l in lms); gv = collections.Counter(l['gender'] for l in VA)
gd = []
for d in DOM:
    c = collections.Counter(l['gender'] for l in lms if l['domain'] == d); n_ = sum(c.values())
    gd.append((DN[d],)+tuple(c[x] for x in G)+(pct(c['female'], n_),))
T_g = table(gd+[('**Total**',)+tuple(g[x] for x in G)+(pct(g['female'], nL),), ('Verified-active only',)+tuple(gv[x] for x in G)+(pct(gv['female'], len(VA)),)],
            ['Domain','Male','Female','Mixed duo','Nonbinary','Female share'])
nocore = [n for n in niches if not n['has_verified_active_core']]
zero = [n for n in niches if n['verified_active_landmarks'] == 0]
cnt = collections.Counter(len(n['landmarks']) for n in niches)
T_cnt = table([(k, cnt[k]) for k in sorted(cnt)], ['Landmarks per niche (primary)','Niches'])
stats = f"""- **{len(niches)} niches, {nL} landmarks** (SEED-v1: {len(v1['landmarks'])}; +1 sourced replacement, +3 net from splitting two show records into hosts) plus {len(EXCLUDED)} excluded (Androgenic).
- Verification: **{SC['verified-active']} verified-active ({pct(SC['verified-active'],nL)})**, {SC['pending']} pending ({pct(SC['pending'],nL)}), {SC['stale']} stale. `active_2025_2026` is true only for verified-active records.
- Core coverage: **{len(niches)-len(nocore)}/{len(niches)} niches have at least one verified-active core**; {len(nocore)} do not, and {len(zero)} niches have no verified-active landmark at all.
- Longform high: {pct(lf['high'],nL)} (v1 {pct(lf1['high'],len(v1['landmarks']))}). Female landmarks: {pct(g['female'],nL)} overall, {pct(gv['female'],len(VA))} among verified-active.
- Applied {len(plog)} platform corrections and {len(lflog)} longform changes. {sum(l['us_focus_flag'] for l in lms)} landmarks carry `us_focus_flag`. Flagged for Benjamin: {sum(1 for l in lms if l['flag_for_benjamin'])}.
"""
audit = f"""## Balance audit

### Verification status
{T_status}
### By domain
{T_dom}
### By role
{T_role}
### Long-form output
{T_lf}
### Gender of landmarks
{T_g}
### Landmarks per niche
{T_cnt}"""

# ---------------------------------------------------------------- SEED-v2.md (v1 layout)
def tag(x):
    l = Lx[x]
    return f"{l['name']} ({l['role'][0]}){'†' if l['verification']=='pending' else ''}{'§' if l['verification']=='stale' else ''}{'°' if l['us_focus_flag'] else ''}{'⚑' if l['flag_for_benjamin'] else ''}"
md = f"""# Dialogos Arena seed dataset: SEED-v2

Author of record: Benjamin Life (@omniharmonic). SEED-v1 with verification batches A–D applied, {TODAY}. Machine-readable data: `SEED-v2.json`. Verification status, pending lists and suggested swaps are in `VERIFICATION-SUMMARY.md`. Built by `scripts/apply_verification.py`.

## Summary
{stats}
## Niches by domain

Landmark roles: **c** = core, **b** = bridger, **e** = edge. † pending verification. § stale. ° non-US voice (`us_focus_flag`). ⚑ flagged for Benjamin's decision. "Also:" lists landmarks whose primary home is elsewhere. Niches marked **(no VA core)** have no verified-active core.

"""
for d in DOM:
    md += f"### {DN[d]}\n\n| Niche | Description | Landmarks |\n|---|---|---|\n"
    for n in [n for n in niches if n['domain'] == d]:
        desc = n['description'].split('. ')[0].rstrip('.')+'.'
        lm = ', '.join(tag(x) for x in n['landmarks'])
        if n['secondary_landmarks']: lm += '; *also:* '+', '.join(Lx[x]['name'] for x in n['secondary_landmarks'])
        am = f" *(Atlas: {n['atlas_match']})*" if n['atlas_match'] else ''
        nc = '' if n['has_verified_active_core'] else ' **(no VA core)**'
        md += f"| **{n['name']}**{am}{nc} | {desc.replace('|','/')} | {lm} |\n"
    md += '\n'
md += audit
open(SEED+'/SEED-v2.md','w').write(md)

# ---------------------------------------------------------------- VERIFICATION-SUMMARY.md
w = []
w.append(f"""# Verification summary: SEED-v2

Author of record: Benjamin Life (@omniharmonic). Generated {TODAY} by `scripts/apply_verification.py` from SEED-v1 and verification batches A–D. Where a landmark appears in more than one batch, the latest batch wins (A→B→C→D; batch D re-checked every pending item from A and B).

## Headline
{stats}
{T_status}
### By domain
{T_dom}
### By role
{T_role}
### Long-form output
{T_lf}
### Gender
{T_g}
## What was applied

- **Verification results**: all {len(FINAL)} batch records ({len(qids)} queued landmarks plus Androgenic). Each sets `verification`, `active_2025_2026`, `evidence_url`, `evidence_date`, `last_checked` = {TODAY}, `verification_source` and `verification_notes`; the v1 status is kept in `verification_v1`.
- **SEED-v1 verified landmarks not in the queue** ({sum(1 for l in lms if l['verification_source'].startswith('SEED-v1'))}) were normalized to `verified-active`. They were not re-checked in batches A–D.
- **Four v1-verified landmarks were queued only for age checks.** sneako and hope-woodard came back verified-active. clavicular and hannah-pearl-davis came back pending: both are confirmed adults, but no dated output item was found. The batch result was applied.
- **Platform corrections**: {len(plog)} field changes. Instruction-style notes such as "add …" or "CORRECTION: …" were resolved into usable values (see `P_OVERRIDE`). Every change, with the raw correction, is in `SEED-v2.json` → `change_log.platform_corrections`.
- **Longform changes**: {len(lflog)}. Upgrades: {', '.join(x['landmark_id'] for x in lflog if LF[x['new']]>LF[x['old']])}. Downgrades: {', '.join(x['landmark_id'] for x in lflog if LF[x['new']]<LF[x['old']]) or 'none'}.
- **Sourced replacement (step 3)**: **Robinson Meyer** was added as a `pending` core in clean-energy-electrification, sourced to https://shows.acast.com/shift-key/episodes. **Jesse Jenkins** was marked `stale` (kept, with `replaced_by`). This was the only recommendation that both named a person with a source and concerned a stale or failed record.
- **Show records converted to hosts**: `red-scare` became Dasha Nekrasova and Anna Khachiyan, and `conspirituality-podcast-hosts` became Derek Beres, Matthew Remski and Julian Walker. Each inherits the show's role, niche and verification (the evidence is show-level). The old ids are in `meta.retired_ids`.
- **Multi-person records naming real people** were kept and flagged with `record_type: multi-person` and an open check: {', '.join(DUOS)}.
- **Androgenic** stays excluded and appears only in `excluded_landmarks`.
- **Non-US voices (batch C)**: `us_focus_flag: true` on {', '.join(f'{k} ({v})' for k,v in NON_US.items())}. raw-egg-nationalist was raised as possibly UK-based in batches A and D. It is not on the batch-C list, so it carries an open check instead of the flag.

## Niches lacking a verified-active core ({len(nocore)})

| Niche | Domain | Primary landmarks (status) | Any VA landmark? |
|---|---|---|---|
""")
for n in nocore:
    ls = ', '.join(f"{Lx[x]['name']} ({Lx[x]['role'][0]}, {Lx[x]['verification']})" for x in n['landmarks'])
    w.append(f"| {n['name']} (`{n['niche_id']}`) | {DN[n['domain']]} | {ls} | {'yes' if n['verified_active_landmarks'] else '**no**'} |\n")
w.append(f"\n**Niches with zero verified-active landmarks ({len(zero)}):** " + ', '.join(f"`{n['niche_id']}`" for n in zero) + "\n")

r = N['regens-refi']
w.append(f"""
## Regens / ReFi niche (`regens-refi`): status

**Status: {'has' if r['has_verified_active_core'] else 'LACKS'} a verified-active core, but that rests on one record that was not re-checked.**

| Landmark | Role | v2 status | Basis |
|---|---|---|---|
""")
for x in r['landmarks']:
    l = Lx[x]
    w.append(f"| {l['name']} | {l['role']} | {l['verification']} | {(l['verification_notes'] or l['verification_source']).replace('|','/')} |\n")
w.append("""
- Kevin Owocki's `verified-active` comes from the SEED-v1 domain agents, whose sources were the Greenpill feed and the Atlas page. He was never in the verification queue, so batches A–D did not re-check him. Batch C concluded that "on current public evidence, the regens-refi niche has no verified-active landmark" without checking Owocki. **Recommendation:** get one dated 2025-10-31-or-later Greenpill episode or post for Owocki before treating the niche as covered.
- Gregory Landua (core) remains pending. His podcast's last episode is dated 2025-04-14, so he leans stale, and batch C found no sourced replacement. Griff Green (bridger) remains pending, with only 2022–23 appearances found.
- Adjacent scenes are also weak. In `bioregionalism-regenerative-culture`, Wahl and Akomolafe are both pending and both carry the non-US flag. In `cooperative-solidarity-economy-commons`, Nathan Schneider (core) is pending.
- This is Benjamin's own scene: Owocki is a collaborator, and Benjamin works with Gitcoin/Techne. The QA report's call for an external reviewer of this niche still applies.
""")

w.append(f"\n## Stale landmarks ({SC['stale']})\n\n| Landmark | Niche | Role | Latest evidence | Note |\n|---|---|---|---|---|\n")
for l in lms:
    if l['verification'] == 'stale':
        w.append(f"| {l['name']} (`{l['landmark_id']}`) | {l['primary_niche']} | {l['role']} | {l['evidence_date'] or '-'} | {('Replaced by `'+l['replaced_by']+'`. ') if l['replaced_by'] else ''}{(l['verification_notes'] or '').split(' | SEED-v2')[0][:220].replace('|','/')} |\n")

w.append(f"\n## Pending landmarks by domain ({SC['pending']})\n\nCore landmarks are in **bold**. Each entry gives the niche and the reason recorded by the last batch.\n")
for d in DOM:
    pl = [l for l in lms if l['domain'] == d and l['verification'] == 'pending']
    pl.sort(key=lambda l: (-RR[l['role']], l['landmark_id']))
    w.append(f"\n### {DN[d]} ({len(pl)})\n\n")
    for l in pl:
        nt = (l['verification_notes'] or '').split(' | SEED-v2')[0]
        head, _, prior = nt.replace('Batch D: ','').partition(' | prior: ')
        why = (prior if head.startswith('No new evidence') and prior else head)
        why = why.split(' [source batch')[0][:220] + (' (no new evidence in batch D)' if head.startswith('No new evidence') else '')
        nm = f"**{l['name']}**" if l['role'] == 'core' else l['name']
        w.append(f"- {nm} (`{l['landmark_id']}`, {l['role']}, {l['primary_niche']}). {why}\n")

w.append("\n## Suggested swaps (not applied)\n\nThese recommendations came from the batch summaries but were not applied. Each either concerns a landmark that is not stale or failed, or names no sourced person. Benjamin decides.\n\n| Landmark | Slot | Issue | Suggestion | From |\n|---|---|---|---|---|\n")
for a,b,c,d,e in SUGGESTED: w.append(f"| {a} | {b} | {c} | {d} | {e} |\n")

oc = [l for l in lms if l['open_checks'] and l['record_type'] != 'multi-person']
w.append("\n## Other open checks\n\n")
for l in oc: w.append(f"- `{l['landmark_id']}`: {'; '.join(l['open_checks'])}\n")
w.append(f"- `androgenic` (excluded): {EXCLUDED[0]['verification_notes'][:160]}…\n")
w.append("""
## Cheapest next pass
Per batches C and D, approving these blocked fetches would clear several pending records at once. Substack and sitemap feeds cover McKibben, Akomolafe, Nordhaus, Kelton and Wahl. Single feed fetches cover Rufo, Strassel, Gillespie and Filipovic (throughline.news). The four core landmarks with relative dates only are jessica-valenti, charles-eisenstein, kimberley-strassel and nick-gillespie.
""")
open(SEED+'/VERIFICATION-SUMMARY.md','w').write(''.join(w))

print(stats)
print('no VA core:', len(nocore), [n['niche_id'] for n in nocore])
print('zero VA:', [n['niche_id'] for n in zero])
print('plog', len(plog), 'lflog', len(lflog), 'duos', DUOS)
