"""SEED-v3 build: SEED-v2.json + raw/g1..g6 gap outputs + decisions_v3.py  ->  SEED-v3.json (+ md, QA report, queue).

Run:  python3 -I /home/claude/dialogos-arena/seed/scripts/build_v3.py
SEED-v2.json is read only. Author of record: Benjamin Life (@omniharmonic).
"""
import json, copy, re, collections, sys, os, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decisions_v3 as D

SEED = os.path.dirname(HERE)
LF = {'high': 3, 'medium': 2, 'low': 1}
RR = {'core': 3, 'bridger': 2, 'edge': 1}
VR = {'verified-active': 0, 'pending': 1, 'stale': 2}
DOM = ['d1-right', 'd2-left-center', 'd3-tech-futures', 'd4-heterodox-sensemaking', 'd5-religion-spirituality',
       'd6-gender-lifestyle-subcultures', 'd7-economy-ecology-place', 'd8-geopolitics-media', 'd9-mainstream-culture']
DN = {'d1-right': 'D1 Right', 'd2-left-center': 'D2 Left & center', 'd3-tech-futures': 'D3 Tech & futures',
      'd4-heterodox-sensemaking': 'D4 Heterodox & sensemaking', 'd5-religion-spirituality': 'D5 Religion & spirituality',
      'd6-gender-lifestyle-subcultures': 'D6 Gender, lifestyle & subcultures', 'd7-economy-ecology-place': 'D7 Economy, ecology & place',
      'd8-geopolitics-media': 'D8 Geopolitics & media', 'd9-mainstream-culture': 'D9 Mainstream culture (new)'}
ATLAS_NAMES = ['effective accelerationists', 'progress & abundance movement', 'hard-tech & space frontier', 'rationalists', 'AI-safety doomers',
    'effective altruists', 'tpot / post-rationalists', 'consciousness & psychedelic twitter', 'bitcoin maxis', 'ethereum builders',
    'DeFi & stablecoin builders', 'degens & memecoin culture', 'regens & solarpunks', 'degrowthers & climate realists', 'longevity & biohackers',
    'MAHA & health freedom', 'neoreaction & the new right', 'network-state builders', 'indie hackers', 'maga / populist right', 'progressive left',
    'liberal establishment', 'wall street / macro', 'christian twitter', 'stan / pop culture', 'sports twitter', 'georgists', 'girardians',
    'landian accel', 'metamodernists', 'forecasters', 'cryonicists', 'pronatalists', 'doomer optimists', 'remilia / net spirituality',
    'cozyweb', 'trad catholics', 'wallstreetbets', 'astrology twitter']

WARN, LOG = [], collections.defaultdict(list)


def kebab(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\(.*?\)', '', s).lower()
    s = re.sub(r'\b(fr|rev|bishop|dr|sj)\b\.?', '', s)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def lid_of(name):
    k = kebab(name)
    return D.ALIAS.get(k, k)


def addu(lst, vals):
    for v in vals:
        if v and v not in lst:
            lst.append(v)


# ------------------------------------------------------------------ load
v2 = json.load(open(f'{SEED}/SEED-v2.json'))
N = {n['niche_id']: copy.deepcopy(n) for n in v2['niches']}
L = {l['landmark_id']: copy.deepcopy(l) for l in v2['landmarks']}
V2_NICHES, V2_LMS = set(N), set(L)
for n in N.values():
    n['gap_meta'] = None; n['flag_for_benjamin'] = None
for l in L.values():
    l['secondary_roles'] = {}; l['flag_type'] = None
ALTS = []

GAP = {}
for g in D.GAP_FILES:
    GAP[g] = json.load(open(f'{SEED}/raw/{g}.json'))
G6 = json.load(open(f'{SEED}/raw/g6-representation.json'))

# ------------------------------------------------------------------ structural validation
REQ = ['niche_id', 'name', 'aliases', 'domain', 'description', 'telos', 'sacred_values', 'existential_threats', 'combatants',
       'adjacent_niches', 'sub_niches', 'size_estimate', 'cultural_influence', 'trajectory', 'atlas_match', 'limberg_barnes_match',
       'landmarks', 'sources', 'notes']
LREQ = ['name', 'role', 'why', 'platforms', 'longform_output', 'active_2025_2026', 'verification', 'sources']
STRUCT = []
for g, arr in GAP.items():
    for n in arr:
        for k in REQ:
            if k not in n: STRUCT.append(f'{g}/{n.get("niche_id")}: missing {k}')
        if 'gap_type' not in n: STRUCT.append(f'{g}/{n["niche_id"]}: missing gap_type')
        if n['domain'] not in DOM: STRUCT.append(f'{g}/{n["niche_id"]}: bad domain {n["domain"]}')
        for l in n['landmarks']:
            for k in LREQ:
                if k not in l: STRUCT.append(f'{g}/{n["niche_id"]}/{l.get("name")}: missing {k}')
            if l['role'] not in RR: STRUCT.append(f'{l["name"]}: bad role')
            if l['longform_output'] not in LF: STRUCT.append(f'{l["name"]}: bad longform')
            if not str(l['verification']).startswith(('verified', 'UNVERIFIED')): STRUCT.append(f'{l["name"]}: bad verification')
            if not isinstance(l['platforms'], dict): STRUCT.append(f'{l["name"]}: platforms not dict')
for a in G6['additions']:
    for k in ['landmark_id', 'name', 'role', 'why', 'platforms', 'longform_output', 'verification', 'sources', 'gender']:
        if k not in a['landmark']: STRUCT.append(f'g6/{a["niche_id"]}: missing {k}')
    if a['niche_id'] not in V2_NICHES: STRUCT.append(f'g6 addition targets unknown niche {a["niche_id"]}')

# ------------------------------------------------------------------ new niches (g1-g5)
raw_by_id = {}
for g, arr in GAP.items():
    for n in arr:
        raw_by_id[n['niche_id']] = (g, n)


def niche_from_raw(n, g, nid=None, name=None, dom=None, cross=None):
    return dict(niche_id=nid or n['niche_id'], name=name or n['name'], domain=dom or n['domain'],
                cross_domains=list(cross if cross is not None else (n.get('cross_domains') or [])), aliases=list(n['aliases']),
                description=n['description'], telos=n['telos'], sacred_values=list(n['sacred_values']),
                existential_threats=list(n['existential_threats']), combatants=list(n['combatants']), adjacent_niches=list(n['adjacent_niches']),
                sub_niches=list(n['sub_niches']), size_estimate=n['size_estimate'], cultural_influence=n['cultural_influence'],
                trajectory=n['trajectory'], atlas_match=n['atlas_match'], limberg_barnes_match=n['limberg_barnes_match'], placement=None,
                landmarks=[], secondary_landmarks=[], verified_active_landmarks=0, has_verified_active_core=False, merged_from=[],
                qa_decision=None, sources=list(n['sources']), notes=f"[{n['niche_id']}] {n['notes']}" if n['notes'] else '',
                gap_meta=dict(gap_type=n.get('gap_type'), source_files=[g], mirror_of=n.get('mirror_of'), youth_branch_of=n.get('youth_branch_of')),
                flag_for_benjamin=None)


NEW = {}
for g, arr in GAP.items():
    for n in arr:
        nid = n['niche_id']
        if nid in D.ABSORB: continue
        t = D.NICHE_MERGE.get(nid, nid)
        if t in NEW: continue
        if t in D.MERGED_META:
            base, name, dom, cross, dec = D.MERGED_META[t]
            bg, bn = raw_by_id[base]
            NEW[t] = niche_from_raw(bn, bg, t, name, dom, cross)
            NEW[t]['qa_decision'] = dec
        else:
            NEW[t] = niche_from_raw(n, g)
# fold merged members in
for g, arr in GAP.items():
    for n in arr:
        nid = n['niche_id']
        if nid in D.ABSORB: continue
        t = D.NICHE_MERGE.get(nid, nid)
        X = NEW[t]; X['merged_from'].append(nid)
        if t in D.MERGED_META and nid != D.MERGED_META[t][0]:
            addu(X['aliases'], n['aliases'] + [n['name']])
            addu(X['combatants'], n['combatants']); addu(X['adjacent_niches'], n['adjacent_niches'])
            addu(X['sub_niches'], n['sub_niches']); addu(X['sacred_values'], n['sacred_values'][:2])
            addu(X['existential_threats'], n['existential_threats'][:1]); addu(X['sources'], n['sources'])
            if n['notes']: X['notes'] += ('' if not X['notes'] else ' | ') + f"[{nid}] {n['notes']}"
            addu(X['gap_meta']['source_files'], [g])
            if n['domain'] != X['domain']: addu(X['cross_domains'], [n['domain']])
            addu(X['sub_niches'], [n['name'] + ' (merged niche)'])
            LOG['niche_merge'].append((nid, t))
# merged-niche specific sub-niches
addu(NEW['disability-rights-justice']['sub_niches'], ['disability rights (ADA / inclusion / legal-liberal wing)', 'disability justice (intersectional, Sins Invalid lineage)'])
addu(NEW['veteran-warrior-culture-media']['sub_niches'], ["America First vets (Hegseth)", "pro-constitution veterans (Mark Kelly)", "independent / anti-duopoly vets (Rieckhoff)", "progressive veterans (VoteVets, Common Defense)", "veteran lifestyle brands & mil-humor (Black Rifle Coffee)"])
addu(NEW['barstool-boys-culture']['sub_niches'], ['sports betting & fantasy (absorbed from g3 retail-trader / sports-betting)'])
for t in NEW:
    for nid in NEW[t]['merged_from']:
        pass
# domain overrides and keep decisions
for nid, (dom, cross, dec) in D.DOMAIN_OVERRIDE.items():
    old = NEW[nid]['domain']; NEW[nid]['domain'] = dom; NEW[nid]['cross_domains'] = cross
    NEW[nid]['qa_decision'] = dec; LOG['domain'].append((nid, old, dom, dec))
for nid, dec in D.KEEP_DECISIONS.items():
    NEW[nid]['qa_decision'] = (NEW[nid]['qa_decision'] + ' ' if NEW[nid]['qa_decision'] else '') + dec
# atlas
for nid, X in NEW.items():
    am = D.ATLAS_NEW.get(nid, X['atlas_match'])
    if am and am not in ATLAS_NAMES:
        LOG['atlas_dropped'].append((nid, am)); am = None
    X['atlas_match'] = am
# step-3 niches
for s in D.STEP3_NICHES:
    s = copy.deepcopy(s); pl = s.pop('placement'); gt = s.pop('gap_type')
    s.update(placement=None, landmarks=[], secondary_landmarks=[], verified_active_landmarks=0, has_verified_active_core=False,
             merged_from=[], qa_decision='Added at v3 QA (step 3 gap fill).', gap_meta=dict(gap_type=gt, source_files=['v3-QA step 3'], mirror_of=None, youth_branch_of=None),
             flag_for_benjamin=None)
    NEW[s['niche_id']] = s
    D.PLACEMENT[s['niche_id']] = pl
for nid, X in NEW.items():
    if nid not in D.PLACEMENT: WARN.append(f'no placement for {nid}'); continue
    lr, ar, ie = D.PLACEMENT[nid]
    NORM = {'neutral': 'neutral/mixed', 'mixed': 'neutral/mixed', 'within': 'within-institutions'}  # v2 vocabulary
    ar, ie = NORM.get(ar, ar), NORM.get(ie, ie)
    X['placement'] = dict(left_right=lr, atlas_accelerate_restrain=ar, atlas_institutions_exit=ie, basis='QA judgment, rough (v3)')
for nid in NEW:
    if nid in N: WARN.append(f'new niche id collides with v2: {nid}')
N.update(NEW)

# ------------------------------------------------------------------ absorptions into existing niches
for nid, (target, dec, aliases, subs) in D.ABSORB.items():
    g, n = raw_by_id[nid]
    T = N[target]
    addu(T['aliases'], aliases + [n['name']]); addu(T['sub_niches'], subs); addu(T['sources'], n['sources'])
    T['merged_from'] = (T.get('merged_from') or []) + [nid]
    T['qa_decision'] = ((T.get('qa_decision') or '') + ' | v3: ' + dec).strip(' |')
    T['notes'] += f" | [{nid}, absorbed v3] {n['notes']}"
    LOG['absorb'].append((nid, target, dec))

# ------------------------------------------------------------------ landmarks from g1-g5
GEN = {}
for gname, ids in D.GENDER_NEW.items():
    for i in ids: GEN[i] = gname
occ = collections.defaultdict(list)
SEC_PENDING = []  # (lid, niche, note)
for g, arr in GAP.items():
    for n in arr:
        nid = n['niche_id']
        target = D.ABSORB[nid][0] if nid in D.ABSORB else D.NICHE_MERGE.get(nid, nid)
        for l in n['landmarks']:
            lid = lid_of(l['name'])
            is_sec = l.get('secondary_of_existing_landmark') or l.get('secondary_landmark') or l['verification'].startswith('verified (via')
            if lid in V2_LMS:
                SEC_PENDING.append((lid, target, f'{g}: listed in {nid}'))
                LOG['sec_from_existing'].append((lid, target, g, 'marked secondary' if is_sec else 'listed as a landmark'))
                continue
            occ[lid].append(dict(target=target, g=g, nid=nid, l=l))
        for s in n.get('secondary_landmarks') or []:
            lid = kebab(s.get('landmark_id') or s.get('name', ''))
            lid = D.ALIAS.get(lid, lid)
            SEC_PENDING.append((lid, target, f'{g}: secondary_landmarks of {nid}'))


def parse_date(s):
    m = re.match(r'(\d{4})-(\d{2})(?:-(\d{2}))?', str(s or ''))
    return f'{m.group(1)}-{m.group(2)}-{m.group(3) or "01"}' if m else None


def make_record(lid, os_):
    targets = []
    for o in os_: addu(targets, [o['target']])
    if lid in D.PRIMARY: prim = D.PRIMARY[lid]
    else:
        prim = targets[0]
        if len(targets) > 1: WARN.append(f'no primary decision for {lid}: {targets}')
    po = [o for o in os_ if o['target'] == prim] or os_
    best = max(po, key=lambda o: RR[o['l']['role']])['l']
    plat, srcs, notes = {}, [], []
    for o in os_:
        for k, v in o['l']['platforms'].items():
            if v and not plat.get(k): plat[k] = v
        addu(srcs, o['l']['sources'])
        for k in ('age_check', 'notes', 'note'):
            if o['l'].get(k): addu(notes, [f"{k.replace('_', ' ')} ({o['g'][:2]}): {o['l'][k]}"])
    ver = 'verified-active' if any(o['l']['verification'].startswith('verified') for o in os_) else 'pending'
    evd = next((o['l'].get('evidence_date') for o in os_ if o['l'].get('evidence_date')), None)
    vnote = None
    if ver == 'verified-active':
        pdte = parse_date(evd)
        if pdte and pdte < D.WINDOW:
            ver = 'pending'; vnote = f'Gap agent dated item {evd} predates the v2 window ({D.WINDOW}); needs a newer item.'
        elif not evd:
            vnote = f'Gap agent ({"/".join(sorted({o["g"][:2] for o in os_}))}) found a dated 2025-26 item; the date was not recorded, so it may predate the v2 window ({D.WINDOW}).'
    if notes: vnote = ((vnote + ' | ') if vnote else '') + ' | '.join(notes)
    name = D.DISPLAY_NAME.get(lid, best['name'])
    rec = dict(landmark_id=lid, name=name, primary_niche=prim, secondary_niches=[t for t in targets if t != prim], domain=None,
               role=D.ROLE.get(lid, best['role']), why=best['why'], platforms=plat,
               longform_output=max((o['l']['longform_output'] for o in os_), key=lambda x: LF[x]),
               active_2025_2026=None, verification=ver, evidence_url=None, evidence_date=evd, last_checked=D.TODAY,
               verification_source='raw/' + '+'.join(sorted({o['g'] for o in os_})), verification_batches=[], verification_notes=vnote,
               verification_v1=None, longform_v1=None, us_focus_flag=False, us_focus_note=None, open_checks=[],
               record_type='multi-person' if (' & ' in name or ', ' in name) else 'person', converted_from=None, replaces=None,
               replaced_by=None, gender=GEN.get(lid, 'male'), flag_for_benjamin=None, flag_type=None, sources=srcs,
               source_domains=sorted({o['g'] for o in os_}), secondary_roles={})
    return rec


for lid, os_ in occ.items():
    rec = make_record(lid, os_)
    if lid in D.ALTERNATES:
        rec['alternate_reason'] = D.ALTERNATES[lid]; ALTS.append(rec); continue
    L[lid] = rec
    LOG['new_lm'].append(lid)
    if len({o['target'] for o in os_}) > 1 or lid in D.PRIMARY:
        LOG['dedupe'].append((lid, rec['primary_niche'], rec['secondary_niches']))

# ------------------------------------------------------------------ g6: additions, roles, verification, renames
for a in G6['additions']:
    x = copy.deepcopy(a['landmark']); lid = x['landmark_id']; nid = a['niche_id']
    note = x.get('verification_notes') or ''
    for old, new in D.PRIVATE_SCRUB: note = note.replace(old, new)
    if lid in L and lid in V2_LMS:   # existing v2 record -> secondary listing
        if L[lid]['primary_niche'] != nid:
            addu(L[lid]['secondary_niches'], [nid]); L[lid]['secondary_roles'][nid] = x['role']
        LOG['g6_secondary'].append((lid, nid, x['role'], a['reason']))
        continue
    if lid in L:                      # created above from g1-g5 (e.g., Du Mez)
        R = L[lid]
        if R['primary_niche'] != nid: addu(R['secondary_niches'], [nid])
        addu(R['sources'], x['sources']); addu(R['source_domains'], ['g6-representation'])
        R['verification_notes'] = ((R['verification_notes'] or '') + ' | g6: ' + note).strip(' |')
        LOG['g6_merged_into_new'].append((lid, nid)); continue
    rec = dict(landmark_id=lid, name=x['name'], primary_niche=nid, secondary_niches=[], domain=None, role=x['role'], why=x['why'],
               platforms=x['platforms'], longform_output=x['longform_output'], active_2025_2026=None, verification=x['verification'],
               evidence_url=x.get('evidence_url'), evidence_date=x.get('evidence_date'), last_checked=x.get('last_checked', D.TODAY),
               verification_source='raw/g6-representation', verification_batches=['g6'], verification_notes=note or None,
               verification_v1=None, longform_v1=None, us_focus_flag=False, us_focus_note=None, open_checks=[],
               record_type=x.get('record_type', 'person'), converted_from=None, replaces=None, replaced_by=None, gender=x['gender'],
               flag_for_benjamin=None, flag_type=None, sources=x['sources'], source_domains=['g6-representation'], secondary_roles={},
               g6_reason=a['reason'])
    if lid in D.ALTERNATES:
        rec['alternate_reason'] = D.ALTERNATES[lid]; ALTS.append(rec); LOG['alternate'].append(lid); continue
    L[lid] = rec; LOG['g6_new'].append((lid, nid, x['role'], x['verification']))
for rc in G6['role_changes']:
    lid = D.ALIAS.get(rc['landmark_id'], rc['landmark_id']); R = L[lid]
    if R['primary_niche'] == rc['niche_id']:
        LOG['role'].append((lid, rc['niche_id'], R['role'], rc['new_role'], rc['evidence'])); R['role'] = rc['new_role']
    else:
        addu(R['secondary_niches'], [rc['niche_id']]); R['secondary_roles'][rc['niche_id']] = rc['new_role']
        LOG['role'].append((lid, rc['niche_id'] + ' (secondary listing)', '-', rc['new_role'], rc['evidence']))
for lid, roles in D.SECONDARY_ROLE.items():
    L[lid]['secondary_roles'].update(roles)
for vu in G6['verification_updates']:
    R = L[vu['landmark_id']]; note = vu['note']
    for old, new in D.PRIVATE_SCRUB: note = note.replace(old, new)
    LOG['verif'].append((vu['landmark_id'], R['verification'], vu['new_verification'], vu['evidence_date']))
    R.update(verification=vu['new_verification'], evidence_url=vu['evidence_url'], evidence_date=vu['evidence_date'], last_checked=D.TODAY,
             verification_source='raw/g6-representation', verification_notes=note)
    R['verification_batches'] = list(R.get('verification_batches') or []) + ['g6']
for rn in G6['renames']:
    X = N[rn['niche_id']]; old = X['name']
    addu(X['aliases'], [f'{old} (former seed label)', rn['old_name_to_alias']])
    X['name'] = rn['new_name']; LOG['rename'].append((rn['niche_id'], old, rn['new_name'], rn['reason']))
for nid, ex in D.RENAME_ALIAS_EXTRA.items():
    for old, new in ex['mark_outsider'].items():
        N[nid]['aliases'] = [new if a == old else a for a in N[nid]['aliases']]
na = N['new-age-manifestation-wellness']
na['sub_niches'] = [("awakening/sovereignty crossover (see conspirituality-sovereignty; 'conspirituality' is a critics' label)" if s.startswith('conspirituality') else
                     'astrology/tarot TikTok (now its own niche: astrology-mainstream)' if s.startswith('astrology') else s) for s in na['sub_niches']]
# mens-rights split: move fathers' rights / MRA from mens-boys-advocacy
mb = N['mens-boys-advocacy']
mb['sub_niches'] = [s for s in mb['sub_niches'] if s not in ("fathers' rights", "Men's rights & MGTOW (merged niche)")]
mb['aliases'] = [a for a in mb['aliases'] if a not in ('MRA', "Men's rights & MGTOW")]
addu(N['mens-rights-fathers-rights']['aliases'], ['MRA', "Men's rights & MGTOW (v1 merged label)"])
LOG['moved'].append("mens-boys-advocacy: sub-niches \"fathers' rights\" and \"Men's rights & MGTOW (merged niche)\" and aliases MRA / \"Men's rights & MGTOW\" moved to mens-rights-fathers-rights")

# ------------------------------------------------------------------ step 3: records and updates
for nid, arr in list(D.STEP3_LANDMARKS.items()) + list(D.STEP3_EXISTING_NICHE_ADDS.items()):
    for x in arr:
        x = copy.deepcopy(x); lid = x['landmark_id']
        if lid in L: WARN.append(f'step3 duplicate {lid}'); continue
        L[lid] = dict(landmark_id=lid, name=x['name'], primary_niche=nid, secondary_niches=[], domain=None, role=x['role'], why=x['why'],
                      platforms=x['platforms'], longform_output=x['longform_output'], active_2025_2026=None, verification=x['verification'],
                      evidence_url=x['evidence_url'], evidence_date=x['evidence_date'], last_checked=D.TODAY, verification_source='v3-QA step 3',
                      verification_batches=['v3-step3'], verification_notes=x['verification_notes'], verification_v1=None, longform_v1=None,
                      us_focus_flag=False, us_focus_note=None, open_checks=[], record_type='person', converted_from=None, replaces=None,
                      replaced_by=None, gender=x['gender'], flag_for_benjamin=None, flag_type=None, sources=x['sources'],
                      source_domains=['v3-QA'], secondary_roles={})
        LOG['step3'].append((lid, nid, x['role'], x['verification']))
for lid, up in D.STEP3_EXISTING_UPDATES.items():
    R = L[lid]; po = up.pop('platforms_other', None)
    LOG['step3_update'].append((lid, R['verification'], up['verification']))
    R.update(up); R['verification_source'] = 'v3-QA step 3'; R['last_checked'] = D.TODAY
    R['verification_batches'] = list(R['verification_batches']) + ['v3-step3']
    if po: R['platforms']['other'] = po
for nid, subs in D.STEP3_SUBNICHES.items():
    addu(N[nid]['sub_niches'], subs)

# ------------------------------------------------------------------ secondaries (gap secondary lists + extras)
for lid, nid, why in SEC_PENDING:
    if lid not in L:
        if any(a['landmark_id'] == lid for a in ALTS): continue
        WARN.append(f'secondary ref to unknown landmark {lid} ({why})'); continue
    if nid not in N: WARN.append(f'secondary to unknown niche {nid}'); continue
    if L[lid]['primary_niche'] != nid: addu(L[lid]['secondary_niches'], [nid])
for lid, nids in D.EXTRA_SECONDARY.items():
    if lid not in L: WARN.append(f'extra secondary unknown {lid}'); continue
    for nid in nids:
        if L[lid]['primary_niche'] != nid: addu(L[lid]['secondary_niches'], [nid])
# v2 records moved to alternates
for lid in list(D.ALTERNATES):
    if lid in L and lid in V2_LMS:
        rec = L.pop(lid); rec['alternate_reason'] = D.ALTERNATES[lid]; ALTS.append(rec); LOG['alternate'].append(lid)

# ------------------------------------------------------------------ hygiene
HYG = []
for tid, field, old, new in D.SCRUB:
    obj = N.get(tid) or L.get(tid)
    if obj is None: WARN.append(f'scrub target missing {tid}'); continue
    cur = obj.get(field) or ''
    if old is None:
        HYG.append((tid, field, cur[:110])); obj[field] = new
    elif old in cur:
        HYG.append((tid, field, old[:110])); obj[field] = cur.replace(old, new)
    else:
        WARN.append(f'scrub text not found: {tid}.{field}')
N['metacrisis-great-simplification']['sub_niches'] = ['Game B' if s.startswith('Game B (after') else s for s in N['metacrisis-great-simplification']['sub_niches']]
HYG.append(('metacrisis-great-simplification', 'sub_niches', "Game B (after Jim Rutt's death in 2026)"))
# private-vault citations are not public evidence: strip them from sources (kept out of the public seed)
for coll in (N.values(), L.values()):
    for o in coll:
        src = o.get('sources') or []
        bad = [x for x in src if isinstance(x, str) and (x.startswith('Parachute') or 'Gitcoin Brain' in x or x.startswith('vault/'))]
        if bad:
            o['sources'] = [x for x in src if x not in bad]
            for x in bad: HYG.append((o.get('niche_id') or o.get('landmark_id'), 'sources', 'private-vault citation removed: ' + x[:70]))
# drop gap-file flag texts (they repeat allegations); flags are re-set below from neutral reasons
for l in list(L.values()) + ALTS:
    l['flag_for_benjamin'] = None; l['flag_type'] = None
for lid, (ft, txt) in D.FLAGS.items():
    if lid not in L: WARN.append(f'flag target missing {lid}'); continue
    L[lid]['flag_for_benjamin'] = txt; L[lid]['flag_type'] = ft
for nid, txt in D.OUTSIDE_REVIEW_NICHES.items():
    N[nid]['flag_for_benjamin'] = txt

# ------------------------------------------------------------------ recompute links
for l in L.values():
    if l['primary_niche'] not in N: WARN.append(f'{l["landmark_id"]}: unknown primary {l["primary_niche"]}')
    l['domain'] = N[l['primary_niche']]['domain']
    l['secondary_niches'] = [s for s in dict.fromkeys(l['secondary_niches']) if s in N and s != l['primary_niche']]
    l['secondary_roles'] = {k: v for k, v in l['secondary_roles'].items() if k in l['secondary_niches']}
    l['active_2025_2026'] = True if l['verification'] == 'verified-active' else (False if l['verification'] == 'stale' else None)
CAPW = []
for X in N.values():
    ls = [l for l in L.values() if l['primary_niche'] == X['niche_id']]
    ls.sort(key=lambda l: (-RR[l['role']], -LF[l['longform_output']], VR[l['verification']], l['landmark_id']))
    X['landmarks'] = [l['landmark_id'] for l in ls]
    X['secondary_landmarks'] = sorted(l['landmark_id'] for l in L.values() if X['niche_id'] in l['secondary_niches'])
    X['verified_active_landmarks'] = sum(l['verification'] == 'verified-active' for l in ls)
    X['has_verified_active_core'] = any(l['verification'] == 'verified-active' and l['role'] == 'core' for l in ls)
    if len(ls) < 2: CAPW.append(f"THIN {X['niche_id']}: {len(ls)}")
    if len(ls) > D.CAP: CAPW.append(f"OVER {X['niche_id']}: {len(ls)} {X['landmarks']}")
    if not any(l['role'] == 'core' for l in ls): CAPW.append(f"NOCORE {X['niche_id']}")
WARN += CAPW

# ------------------------------------------------------------------ residual keyword scan (for the report)
KW = re.compile(r"\b(lawsuit|sued|arrest\w*|indict\w*|convicted|trafficking|assault\w*|defam\w*|died|death|hospital\w*|illness|rehab|affair|scandal\w*|alleg\w*|accus\w*|misconduct|jail\w*|sentenced|harass\w*|incite\w*|Nasrallah|Houthi\w*|funeral|diagnos\w*|banned|resign\w*|detention|Epstein)\b", re.I)
RESID = []
for coll in (N.values(), L.values()):
    for o in coll:
        for k in ('why', 'description', 'notes', 'trajectory', 'verification_notes', 'flag_for_benjamin'):
            v = o.get(k)
            if isinstance(v, str):
                for m in KW.finditer(v):
                    RESID.append((o.get('niche_id') or o.get('landmark_id'), k, m.group(0), v[max(0, m.start() - 70):m.end() + 50]))

# ------------------------------------------------------------------ mirrors
for a, b, _ in D.MIRRORS:
    for x in (a, b):
        if x not in N: WARN.append(f'mirror niche missing {x}')
in_pair = {x for a, b, _ in D.MIRRORS for x in (a, b)}
ISSUE_TYPES = {'mirror', 'missing-arena'}
issue_niches = sorted(nid for nid, X in N.items() if X.get('gap_meta') and X['gap_meta']['gap_type'] in ISSUE_TYPES) + \
    ['pro-life-movement', 'second-amendment-movement', 'medical-freedom-vaccine-sceptic', 'maha-coalition-wellness', 'lgbtq-trans-rights',
     'gender-critical-feminism', 'gender-medicine-skeptics', 'pronatalism', 'election-integrity-fraud-concern', 'democracy-protection-voting-rights',
     'anti-disinformation-field', 'censorship-industrial-complex-critics', 'climate-justice-movement', 'housing-justice-tenant-movement',
     'pro-palestinian-movement', 'pro-israel-zionist-commentators', 'china-hawks', 'animal-rights-vegan']
UNPAIRED = [x for x in dict.fromkeys(issue_niches) if x not in in_pair and x not in D.ISSUE_EXCEPTIONS]

# ------------------------------------------------------------------ write state for render
state = dict(N=N, L=L, ALTS=ALTS, WARN=WARN, LOG=LOG, STRUCT=STRUCT, HYG=HYG, RESID=RESID, UNPAIRED=UNPAIRED,
             issue_niches=list(dict.fromkeys(issue_niches)), V2_NICHES=sorted(V2_NICHES), V2_LMS=sorted(V2_LMS))
json.dump(state, open(f'{HERE}/_state_v3.json', 'w'), indent=1, default=str)
print('niches', len(N), 'landmarks', len(L), 'alternates', len(ALTS), 'struct', len(STRUCT), 'new niches', len(NEW))
for w in WARN: print('WARN', w)
for s in STRUCT: print('STRUCT', s)
print('unpaired issue niches:', UNPAIRED)
print('residual keyword hits:', len(RESID))
