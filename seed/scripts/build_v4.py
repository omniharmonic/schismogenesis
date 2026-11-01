"""SEED-v4 build: SEED-v3.json + raw/g7, raw/g8 (+ additions) + decisions_v4.py -> SEED-v4.json, SEED-v4.md, QA-REPORT-v4.md, VERIFICATION-QUEUE-v4.json

Run:  python3 -I /home/claude/dialogos-arena/seed/scripts/build_v4.py
Extends the v3 pipeline (build_v3.py / render_v3.py conventions) as a delta over the published SEED-v3.json, which is read only.
Author of record: Benjamin Life (@omniharmonic).
"""
import json, copy, re, collections, sys, os, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decisions_v4 as D

SEED = os.path.dirname(HERE)
LF = {'high': 3, 'medium': 2, 'low': 1}
RR = {'core': 3, 'bridger': 2, 'edge': 1}
VR = {'verified-active': 0, 'pending': 1, 'stale': 2}
DOM = ['d1-right', 'd2-left-center', 'd3-tech-futures', 'd4-heterodox-sensemaking', 'd5-religion-spirituality',
       'd6-gender-lifestyle-subcultures', 'd7-economy-ecology-place', 'd8-geopolitics-media', 'd9-mainstream-culture']
DN = {'d1-right': 'D1 Right', 'd2-left-center': 'D2 Left & center', 'd3-tech-futures': 'D3 Tech & futures',
      'd4-heterodox-sensemaking': 'D4 Heterodox & sensemaking', 'd5-religion-spirituality': 'D5 Religion & spirituality',
      'd6-gender-lifestyle-subcultures': 'D6 Gender, lifestyle & subcultures', 'd7-economy-ecology-place': 'D7 Economy, ecology & place',
      'd8-geopolitics-media': 'D8 Geopolitics & media', 'd9-mainstream-culture': 'D9 Mainstream culture'}
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
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def addu(lst, vals):
    for v in vals:
        if v and v not in lst: lst.append(v)


def parse_date(s):
    m = re.match(r'(\d{4})-(\d{2})(?:-(\d{2}))?', str(s or ''))
    return f'{m.group(1)}-{m.group(2)}-{m.group(3) or "01"}' if m else None


# ------------------------------------------------------------------ load (v3 read only)
v3 = json.load(open(f'{SEED}/SEED-v3.json'))
N = {n['niche_id']: copy.deepcopy(n) for n in v3['niches']}
L = {l['landmark_id']: copy.deepcopy(l) for l in v3['landmarks']}
ALTS = copy.deepcopy(v3['alternates'])
V3N, V3L = set(N), set(L)
ALL_IDS = V3L | {a['landmark_id'] for a in ALTS}
NAME_IDX = {kebab(l['name']): l['landmark_id'] for l in list(L.values()) + ALTS}
GAP = {g: json.load(open(f'{SEED}/raw/{g}.json')) for g in D.GAP_FILES}
ADD = {g: json.load(open(f'{SEED}/raw/{g}.json')) for g in D.ADD_FILES}

# ------------------------------------------------------------------ structural validation
REQ = ['niche_id', 'name', 'aliases', 'domain', 'description', 'telos', 'sacred_values', 'existential_threats', 'combatants',
       'adjacent_niches', 'sub_niches', 'size_estimate', 'cultural_influence', 'trajectory', 'atlas_match', 'limberg_barnes_match',
       'landmarks', 'sources', 'notes']
LREQ = ['name', 'role', 'why', 'platforms', 'longform_output', 'active_2025_2026', 'verification', 'sources']
STRUCT = []
for g, arr in GAP.items():
    for n in arr:
        for k in REQ + ['gap_type']:
            if k not in n: STRUCT.append(f'{g}/{n.get("niche_id")}: missing {k}')
        if n['domain'] not in DOM: STRUCT.append(f'{g}/{n["niche_id"]}: bad domain')
        if n['niche_id'] in N: STRUCT.append(f'{g}/{n["niche_id"]}: niche id collides with v3')
        for l in n['landmarks']:
            for k in LREQ + ['gender']:
                if k not in l: STRUCT.append(f'{g}/{n["niche_id"]}/{l.get("name")}: missing {k}')
            if l['role'] not in RR: STRUCT.append(f'{l["name"]}: bad role')
            if l['longform_output'] not in LF: STRUCT.append(f'{l["name"]}: bad longform')
            if not str(l['verification']).startswith(('verified', 'UNVERIFIED', 'pending')): STRUCT.append(f'{l["name"]}: bad verification')
for g, a in ADD.items():
    for x in a['additions']:
        for k in ['landmark_id', 'name', 'role', 'why', 'platforms', 'longform_output', 'verification', 'sources', 'gender']:
            if k not in x['landmark']: STRUCT.append(f'{g}/{x["niche_id"]}: missing {k}')
        if x['niche_id'] not in N: STRUCT.append(f'{g}: addition targets unknown niche {x["niche_id"]}')

# ------------------------------------------------------------------ new niches
NEW = {}
for g, arr in GAP.items():
    for n in arr:
        nid = n['niche_id']
        X = dict(niche_id=nid, name=n['name'], domain=n['domain'], cross_domains=list(n.get('cross_domains') or []), aliases=list(n['aliases']),
                 description=n['description'], telos=n['telos'], sacred_values=list(n['sacred_values']), existential_threats=list(n['existential_threats']),
                 combatants=list(n['combatants']), adjacent_niches=list(n['adjacent_niches']), sub_niches=list(n['sub_niches']),
                 size_estimate=n['size_estimate'], cultural_influence=n['cultural_influence'], trajectory=n['trajectory'],
                 atlas_match=n['atlas_match'], limberg_barnes_match=n['limberg_barnes_match'], placement=None, landmarks=[], secondary_landmarks=[],
                 verified_active_landmarks=0, has_verified_active_core=False, merged_from=[], qa_decision='Added in v4 from ' + g + '.',
                 gap_meta=dict(gap_type=n.get('gap_type'), source_files=[g], mirror_of=n.get('mirror_of'), youth_branch_of=None),
                 flag_for_benjamin=None, sources=list(n['sources']), notes=f"[{nid}] {n['notes']}" if n['notes'] else '')
        NEW[nid] = X
for s in D.STEP2_NICHES:
    s = copy.deepcopy(s); gt = s.pop('gap_type'); mo = s.pop('mirror_of')
    s.update(placement=None, landmarks=[], secondary_landmarks=[], verified_active_landmarks=0, has_verified_active_core=False, merged_from=[],
             qa_decision='Added at v4 QA (step 2 cheap gap: mirror of medical freedom).',
             gap_meta=dict(gap_type=gt, source_files=['v4-QA step 2'], mirror_of=mo, youth_branch_of=None), flag_for_benjamin=None)
    NEW[s['niche_id']] = s
for nid, X in NEW.items():
    if X['atlas_match'] not in ATLAS_NAMES or nid in D.ATLAS:
        new = D.ATLAS.get(nid)
        if X['atlas_match'] != new: LOG['atlas'].append((nid, X['atlas_match'], new))
        X['atlas_match'] = new
    if nid not in D.PLACEMENT: WARN.append(f'no placement for {nid}'); continue
    lr, ar, ie = D.PLACEMENT[nid]
    X['placement'] = dict(left_right=lr, atlas_accelerate_restrain=ar, atlas_institutions_exit=ie,
                          basis='QA judgment, rough (v4)' + (f'. {D.PLACEMENT_NOTES[nid]}' if nid in D.PLACEMENT_NOTES else ''))
N.update(NEW)


# ------------------------------------------------------------------ landmark records
def new_record(x, nid, src, batch):
    ver_raw = str(x['verification'])
    evd = x.get('evidence_date')
    vnote = x.get('verification_notes') or None
    if ver_raw.startswith('verified'):
        ver = 'verified-active'
        p = parse_date(evd)
        if p and p < D.WINDOW:
            ver = 'pending'; vnote = ((vnote + ' | ') if vnote else '') + f'Dated item {evd} predates the window ({D.WINDOW}); needs a newer item.'
    else:
        ver = 'pending'
    if x.get('flag_for_benjamin'): LOG['raw_flag_dropped'].append((x.get('landmark_id'), x['flag_for_benjamin']))
    return dict(landmark_id=x['landmark_id'], name=x['name'], primary_niche=nid, secondary_niches=[], secondary_roles={}, domain=None, role=x['role'],
                why=x['why'], platforms=x['platforms'], longform_output=x['longform_output'], active_2025_2026=None, verification=ver,
                evidence_url=x.get('evidence_url'), evidence_date=evd, last_checked=x.get('last_checked') or D.TODAY, verification_source=src,
                verification_batches=[batch], verification_notes=vnote, verification_v1=None, longform_v1=None, us_focus_flag=False, us_focus_note=None,
                open_checks=[], record_type=x.get('record_type') or ('multi-person' if (' & ' in x['name']) else 'person'), converted_from=None,
                replaces=None, replaced_by=None, gender=x['gender'], flag_for_benjamin=None, flag_type=None, sources=list(x['sources']),
                source_domains=[src.replace('raw/', '')])


def resolve(lid, name):
    if lid and lid in ALL_IDS: return lid
    k = kebab(name or '')
    return NAME_IDX.get(k) or (k if k in ALL_IDS else None)


SEC = []  # (lid, niche, role, why)
for g, arr in GAP.items():
    for n in arr:
        nid = n['niche_id']
        for l in n['landmarks']:
            x = dict(l); x['landmark_id'] = l.get('landmark_id') or kebab(l['name'])
            ex = resolve(x['landmark_id'], l['name'])
            if ex: SEC.append((ex, nid, l['role'], f'{g}: listed as landmark')); LOG['dedupe'].append((ex, nid)); continue
            if x['landmark_id'] in L: WARN.append(f'duplicate new id {x["landmark_id"]}'); continue
            L[x['landmark_id']] = new_record(x, nid, f'raw/{g}', g[:2])
            LOG['new_lm'].append((x['landmark_id'], nid, x['role'], L[x['landmark_id']]['verification']))
        for s in n.get('secondary_landmarks') or []:
            ex = resolve(s.get('landmark_id'), s.get('name'))
            if not ex: WARN.append(f'secondary unknown {s}'); continue
            SEC.append((ex, nid, s.get('role'), f'{g}: secondary_landmarks'))
for g, a in ADD.items():
    for ad in a['additions']:
        x = copy.deepcopy(ad['landmark']); nid = ad['niche_id']
        ex = resolve(x['landmark_id'], x['name'])
        if ex: SEC.append((ex, nid, x['role'], f'{g}: addition')); LOG['dedupe'].append((ex, nid)); continue
        rec = new_record(x, nid, f'raw/{g}', g[:2]); rec['g_reason'] = ad['reason']
        L[x['landmark_id']] = rec
        for s in x.get('secondary_niches') or []: SEC.append((x['landmark_id'], s, x['role'], f'{g}: addition secondary'))
        LOG['add_lm'].append((x['landmark_id'], nid, x['role'], rec['verification'], ad['reason']))
for nid, arr in list(D.STEP2_LANDMARKS.items()) + list(D.STEP2_EXISTING_ADDS.items()):
    for x in arr:
        x = copy.deepcopy(x); secs = x.pop('secondary', {})
        if resolve(x['landmark_id'], x['name']) or x['landmark_id'] in L: WARN.append(f'step2 duplicate {x["landmark_id"]}'); continue
        L[x['landmark_id']] = new_record(x, nid, 'v4-QA step 2', 'v4-step2')
        LOG['step2'].append((x['landmark_id'], nid, x['role'], L[x['landmark_id']]['verification'], x['evidence_date']))
        for s, r in secs.items(): SEC.append((x['landmark_id'], s, r, 'v4 QA'))

# primary moves
for lid, (np_, role, oldrole, why) in D.PRIMARY_MOVES.items():
    R = L[lid]; old = R['primary_niche']
    R['primary_niche'] = np_; R['role'] = role
    addu(R['secondary_niches'], [old]); R['secondary_roles'][old] = oldrole
    R['secondary_niches'] = [s for s in R['secondary_niches'] if s != np_]; R['secondary_roles'].pop(np_, None)
    LOG['moved'].append((lid, old, np_, role, why))
# secondaries
for lid, nid, role, why in SEC:
    if nid not in N: WARN.append(f'secondary to unknown niche {nid}'); continue
    R = L.get(lid)
    if R is None: WARN.append(f'secondary of alternate/unknown {lid}'); continue
    if R['primary_niche'] == nid: continue
    addu(R['secondary_niches'], [nid])
    if role: R['secondary_roles'][nid] = role
    LOG['secondary'].append((lid, nid, role, why))
for lid, m in D.SECONDARY_EXTRA.items():
    for nid, role in m.items():
        R = L[lid]
        if R['primary_niche'] == nid: continue
        fresh = nid not in R['secondary_niches']
        addu(R['secondary_niches'], [nid]); R['secondary_roles'][nid] = role
        if fresh: LOG['secondary'].append((lid, nid, role, 'v4 QA'))

# ------------------------------------------------------------------ sub-niche changes
for nid, m in D.SUBNICHE_REPLACE.items():
    for old, new in m.items():
        if old in N[nid]['sub_niches']:
            N[nid]['sub_niches'] = [new if s == old else s for s in N[nid]['sub_niches']]; LOG['subniche'].append((nid, 'replaced', old, new))
        else:
            WARN.append(f'sub-niche not found {nid}: {old[:50]}')
for nid, adds in D.SUBNICHE_ADD.items():
    for s in adds:
        if s not in N[nid]['sub_niches']: N[nid]['sub_niches'].append(s); LOG['subniche'].append((nid, 'added', None, s))

# ------------------------------------------------------------------ hygiene, flags
HYG = []
for coll in (N.values(), L.values()):
    for o in coll:
        src = o.get('sources') or []
        bad = [x for x in src if isinstance(x, str) and (x.startswith('Parachute') or 'Gitcoin Brain' in x or x.startswith('vault/'))]
        if bad:
            o['sources'] = [x for x in src if x not in bad]
            for x in bad: HYG.append((o.get('niche_id') or o.get('landmark_id'), 'sources', 'private-vault citation removed: ' + x[:70]))
for lid, txt in D.CONFLICT_NEW.items():
    L[lid]['flag_for_benjamin'] = txt; L[lid]['flag_type'] = 'conflict-of-interest'
for nid, txt in D.OUTSIDE_REVIEW_NEW.items():
    N[nid]['flag_for_benjamin'] = txt

# ------------------------------------------------------------------ recompute links
for l in L.values():
    if l['primary_niche'] not in N: WARN.append(f'{l["landmark_id"]}: unknown primary')
    l['domain'] = N[l['primary_niche']]['domain']
    l['secondary_niches'] = [s for s in dict.fromkeys(l['secondary_niches']) if s in N and s != l['primary_niche']]
    l['secondary_roles'] = {k: v for k, v in (l.get('secondary_roles') or {}).items() if k in l['secondary_niches']}
    l['active_2025_2026'] = True if l['verification'] == 'verified-active' else (False if l['verification'] == 'stale' else None)
for X in N.values():
    ls = [l for l in L.values() if l['primary_niche'] == X['niche_id']]
    ls.sort(key=lambda l: (-RR[l['role']], -LF[l['longform_output']], VR[l['verification']], l['landmark_id']))
    X['landmarks'] = [l['landmark_id'] for l in ls]
    X['secondary_landmarks'] = sorted(l['landmark_id'] for l in L.values() if X['niche_id'] in l['secondary_niches'])
    X['verified_active_landmarks'] = sum(l['verification'] == 'verified-active' for l in ls)
    X['has_verified_active_core'] = any(l['verification'] == 'verified-active' and l['role'] == 'core' for l in ls)
    if len(ls) < 2: WARN.append(f"THIN {X['niche_id']}: {len(ls)}")
    if len(ls) > D.CAP: WARN.append(f"OVER {X['niche_id']}: {len(ls)}")
    if not any(l['role'] == 'core' for l in ls): WARN.append(f"NOCORE {X['niche_id']}")

# ------------------------------------------------------------------ residual keyword scan on v4 changes
KW = re.compile(r"\b(lawsuit|sued|arrest\w*|indict\w*|convicted|trafficking|assault\w*|defam\w*|died|death|hospital\w*|illness|rehab|affair|scandal\w*|alleg\w*|accus\w*|misconduct|jail\w*|sentenced|harass\w*|incite\w*|funeral|diagnos\w*|banned|resign\w*|Epstein|terroris\w*|addict\w*)\b", re.I)
RESID = []
for o in [N[x] for x in NEW] + [l for l in L.values() if l['landmark_id'] not in V3L]:
    for k in ('why', 'description', 'notes', 'trajectory', 'verification_notes', 'flag_for_benjamin'):
        v = o.get(k)
        if isinstance(v, str):
            for m in KW.finditer(v): RESID.append((o.get('niche_id') or o.get('landmark_id'), k, m.group(0), v[max(0, m.start() - 60):m.end() + 40]))

# ------------------------------------------------------------------ mirrors
MIRRORS = [(m['a'], m['b'], m['arena']) for m in v3['mirror_pairs']] + D.MIRRORS_V4
for a, b, _ in MIRRORS:
    for x in (a, b):
        if x not in N: WARN.append(f'mirror niche missing {x}')
in_pair = {x for a, b, _ in MIRRORS for x in (a, b)}
v3_exc = re.findall(r'^\| (.+?) \| (.+?) \|$', open(f'{SEED}/QA-REPORT-v3.md').read().split('Why no single mirror')[1].split('Unpaired after')[0], re.M)
NAME2ID = {n['name']: k for k, n in N.items()}
ISSUE_EXC = {NAME2ID.get(a, a): b for a, b in v3_exc if not a.startswith('---')}
ISSUE_EXC.update(D.ISSUE_EXCEPTIONS_V4)
issue_niches = [nid for nid, X in N.items() if X.get('gap_meta') and X['gap_meta']['gap_type'] in ('mirror', 'missing-arena')] + \
    ['pro-life-movement', 'second-amendment-movement', 'medical-freedom-vaccine-sceptic', 'maha-coalition-wellness', 'lgbtq-trans-rights',
     'gender-critical-feminism', 'gender-medicine-skeptics', 'pronatalism', 'election-integrity-fraud-concern', 'democracy-protection-voting-rights',
     'anti-disinformation-field', 'censorship-industrial-complex-critics', 'climate-justice-movement', 'housing-justice-tenant-movement',
     'pro-palestinian-movement', 'pro-israel-zionist-commentators', 'china-hawks', 'animal-rights-vegan', 'secession-national-divorce', 'tribal-nations-native-politics']
issue_niches = list(dict.fromkeys(issue_niches))
UNPAIRED = [x for x in issue_niches if x not in in_pair and x not in ISSUE_EXC]

print('niches', len(N), 'landmarks', len(L), 'alternates', len(ALTS), 'struct', len(STRUCT), 'new niches', len(NEW))
for w in WARN: print('WARN', w)
for s in STRUCT: print('STRUCT', s)
print('unpaired:', UNPAIRED, 'resid', len(RESID))
for r in RESID: print('  RESID', r)
for k in ('atlas', 'raw_flag_dropped'): print(k, LOG.get(k))

# ======================================================================== RENDER
ORDER_N = ['niche_id', 'name', 'domain', 'cross_domains', 'aliases', 'description', 'telos', 'sacred_values', 'existential_threats', 'combatants',
           'adjacent_niches', 'sub_niches', 'size_estimate', 'cultural_influence', 'trajectory', 'atlas_match', 'limberg_barnes_match', 'placement',
           'landmarks', 'secondary_landmarks', 'verified_active_landmarks', 'has_verified_active_core', 'merged_from', 'qa_decision', 'gap_meta',
           'flag_for_benjamin', 'sources', 'notes']
ORDER_L = ['landmark_id', 'name', 'primary_niche', 'secondary_niches', 'secondary_roles', 'domain', 'role', 'why', 'platforms', 'longform_output',
           'active_2025_2026', 'verification', 'evidence_url', 'evidence_date', 'last_checked', 'verification_source', 'verification_batches',
           'verification_notes', 'verification_v1', 'longform_v1', 'us_focus_flag', 'us_focus_note', 'open_checks', 'record_type', 'converted_from',
           'replaces', 'replaced_by', 'gender', 'flag_for_benjamin', 'flag_type', 'sources', 'source_domains']


def od(d, order):
    out = {k: d.get(k) for k in order}
    for k, v in d.items():
        if k not in out: out[k] = v
    return out


def pct(a, b): return f'{100 * a / b:.0f}%' if b else '-'


def table(rows, hdr):
    return '\n'.join(['| ' + ' | '.join(hdr) + ' |', '|' + '---|' * len(hdr)] + ['| ' + ' | '.join(str(c).replace('|', '/') for c in r) + ' |' for r in rows])


nm = lambda x: N[x]['name'] if x in N else x
niches = sorted(N.values(), key=lambda x: (DOM.index(x['domain']), x['name'].lower()))
lms = sorted(L.values(), key=lambda l: l['landmark_id'])
VA = [l for l in lms if l['verification'] == 'verified-active']
SC = collections.Counter(l['verification'] for l in lms)
NEWN = [n for n in niches if n['niche_id'] not in V3N]
NEWL = [l for l in lms if l['landmark_id'] not in V3L]
FLAGGED = [l for l in lms if l['flag_for_benjamin']]
CONFLICT = [l for l in FLAGGED if l['flag_type'] == 'conflict-of-interest']
NFLAG = [n for n in niches if n['flag_for_benjamin']]
fem = lambda ls: sum(l['gender'] == 'female' for l in ls)
femx = lambda ls: sum(l['gender'] in ('female', 'mixed') for l in ls)
br = lambda ls: sum(l['role'] == 'bridger' for l in ls)
v3c = v3['meta']['counts']
spot = sorted([l['landmark_id'] for l in NEWL if l['verification'] == 'verified-active' and not re.match(r'\d{4}-\d{2}', str(l['evidence_date'] or ''))])
spot_v3 = json.load(open(f'{SEED}/VERIFICATION-QUEUE-v3.json'))['spot_check']

# ------------------------------------------------------------------ g8 coverage matrix (parsed from raw/g8-holistic-sweep.md)
g8md = open(f'{SEED}/raw/g8-holistic-sweep.md').read()
cov_sec = g8md.split('## 1. Coverage matrix')[1].split('## 2.')[0]
COV = []
for blk in re.split(r'\n### ', cov_sec)[1:]:
    title = blk.split('\n')[0].strip()
    if title.startswith('1h'): continue          # orchestrator spot-checks, not an outside taxonomy
    rows = [r for r in re.findall(r'^\| (.+?) \| (.+?) \|$', blk, re.M) if not set(r[0]) <= set('-') and r[0] not in ('Tribe', 'Atlas tribe', 'Pew group', 'Segment', 'Category', 'Movement', 'Community', 'Item')]
    rows = [r for r in rows if not r[1].lower().startswith('see 1')]   # cross-references to rows already counted
    c = collections.Counter()
    for _, m in rows:
        ml = m.lower()
        if ml.startswith('excluded'): c['excluded by design'] += 1
        elif 'was gap' in ml: c['gap closed by v4 niche' if '**new**' in ml else 'gap closed by v4 sub-niche/landmark'] += 1
        elif ml.startswith('gap'): c['still a gap'] += 1
        elif 'not a gap by the bar' in ml: c['no niche needed (fails bar)'] += 1
        elif ml.startswith('other agent'): c['covered by g7'] += 1
        elif ml.startswith('sub'): c['sub-niche only'] += 1
        else: c['mapped to niche(s)'] += 1
    COV.append((title, len(rows), c))
COV_KEYS = ['mapped to niche(s)', 'gap closed by v4 niche', 'gap closed by v4 sub-niche/landmark', 'sub-niche only', 'covered by g7',
            'no niche needed (fails bar)', 'excluded by design', 'still a gap']
cov_tot = collections.Counter()
for _, _, c in COV: cov_tot.update(c)
COV_T = table([[t, n] + [c[k] for k in COV_KEYS] for t, n, c in COV] + [['**Total**', sum(x[1] for x in COV)] + [cov_tot[k] for k in COV_KEYS]],
              ['Outside taxonomy', 'Categories'] + COV_KEYS)
cov_mapped = sum(x[1] for x in COV) - cov_tot['still a gap'] - cov_tot['excluded by design'] - cov_tot['no niche needed (fails bar)']
cov_closed = cov_tot['gap closed by v4 niche'] + cov_tot['gap closed by v4 sub-niche/landmark']

# ------------------------------------------------------------------ SEED-v4.json
mirror_pairs = [dict(a=a, a_name=nm(a), b=b, b_name=nm(b), arena=t, added_in='v4' if (a, b, t) in D.MIRRORS_V4 else 'v3') for a, b, t in MIRRORS]
flags = dict(v3['flags_for_benjamin'])
flags['landmarks'] = [dict(landmark_id=l['landmark_id'], name=l['name'], niche=l['primary_niche'], type=l['flag_type'], reason=l['flag_for_benjamin'],
                           added_in='v4' if l['landmark_id'] in D.CONFLICT_NEW else 'v3') for l in FLAGGED]
flags['conflict_flags'] = [dict(landmark_id=l['landmark_id'], name=l['name'], niche=l['primary_niche'], reason=l['flag_for_benjamin'],
                                added_in='v4' if l['landmark_id'] in D.CONFLICT_NEW else 'v3') for l in CONFLICT]
flags['niches'] = [dict(niche_id=n['niche_id'], name=n['name'], reason=n['flag_for_benjamin'], added_in='v4' if n['niche_id'] in D.OUTSIDE_REVIEW_NEW else 'v3') for n in NFLAG]
meta = dict(version='SEED-v4', generated=D.TODAY, author_of_record='Benjamin Life (@omniharmonic)',
            stage='Stage 1c seed - g7 online subcultures + g8 holistic sweep merged over SEED-v3',
            inputs=['SEED-v3.json'] + [f'raw/{g}.json' for g in D.GAP_FILES + D.ADD_FILES] + ['raw/g8-holistic-sweep.md (coverage matrix)',
                    f'v4 QA step-2 web checks ({sum(1 for s in D.SEARCHES if s[0] == "WebSearch")} searches, {sum(1 for s in D.SEARCHES if s[0] == "WebFetch")} fetches)'],
            counts=dict(niches=len(niches), landmarks=len(lms), alternates=len(ALTS), excluded=len(v3['excluded_landmarks']),
                        new_niches=len(NEWN), new_landmarks=len(NEWL), v3_niches=v3c['niches'], v3_landmarks=v3c['landmarks'],
                        by_verification=dict(SC), by_domain={d: dict(niches=sum(n['domain'] == d for n in niches), landmarks=sum(l['domain'] == d for l in lms)) for d in DOM},
                        flagged_landmarks=len(FLAGGED), conflict_flags=len(CONFLICT), niches_needing_outside_review=len(NFLAG), mirror_pairs=len(MIRRORS),
                        women_pct=round(100 * fem(lms) / len(lms), 1), bridger_pct=round(100 * br(lms) / len(lms), 1)),
            schema_notes=dict(v3['meta']['schema_notes'], **{
                'flags_for_benjamin.conflict_flags': 'v4: all conflict-of-interest landmark flags in one list (v3 network ties + Brad Carson); added_in marks the version',
                'mirror_pairs.added_in': 'v4: v3 or v4',
                'gap_meta (v4)': "source_files raw/g7-online-subcultures, raw/g8-holistic-sweep or 'v4-QA step 2'",
                'verification (v4 gap records)': "raw 'verified' with a dated item on/after 2025-10-31 -> verified-active; year-only or approximate dates -> verified-active + VERIFICATION-QUEUE-v4 spot_check; UNVERIFIED/pending or older dates -> pending"}),
            scripts='SEED-v4: scripts/decisions_v4.py (judgment calls) + scripts/build_v4.py (build and render, delta over SEED-v3.json). Earlier: decisions_v3/build_v3/render_v3 (v3), apply_verification.py (v2), build/render/report (v1).',
            retired_ids=v3['meta'].get('retired_ids'))
out = dict(meta=meta, niches=[od(n, ORDER_N) for n in niches], landmarks=[od(l, ORDER_L) for l in lms], alternates=ALTS,
           excluded_landmarks=v3['excluded_landmarks'], suggested_swaps=v3['suggested_swaps'], flags_for_benjamin=flags, mirror_pairs=mirror_pairs,
           coverage_matrix_g8=dict(source='raw/g8-holistic-sweep.md §1', categories=sum(x[1] for x in COV), mapped=cov_mapped, still_gaps=cov_tot['still a gap'], closed_in_v4=cov_closed, excluded_or_not_needed=cov_tot['excluded by design'] + cov_tot['no niche needed (fails bar)'],
                                   by_taxonomy=[dict(taxonomy=t, categories=n, **{k: c[k] for k in COV_KEYS}) for t, n, c in COV]),
           v2_change_log=v3['v2_change_log'], v3_change_log=v3['v3_change_log'], v4_change_log=LOG)
json.dump(out, open(f'{SEED}/SEED-v4.json', 'w'), indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ audit tables
def tag(l):
    t = ''
    if l['verification'] == 'pending': t += '*'
    if l['verification'] == 'stale': t += '§'
    if l.get('us_focus_flag'): t += '°'
    if l['flag_for_benjamin']: t += '⚑'
    return t


def first_sentence(s):
    i = s.find('. ')
    return s if i < 0 else s[:i + 1]


dom_rows = []
for d in DOM:
    ns = [n for n in niches if n['domain'] == d]; ls = [l for l in lms if l['domain'] == d]
    va = [l for l in ls if l['verification'] == 'verified-active']
    dom_rows.append([DN[d], len(ns), sum(n['niche_id'] not in V3N for n in ns), len(ls), sum(l['landmark_id'] not in V3L for l in ls),
                     f'{len(va)} ({pct(len(va), len(ls))})', pct(fem(ls), len(ls)), pct(br(ls), len(ls))])
dom_rows.append(['**Total**', len(niches), len(NEWN), len(lms), len(NEWL), f'{len(VA)} ({pct(len(VA), len(lms))})', pct(fem(lms), len(lms)), pct(br(lms), len(lms))])
DOM_T = table(dom_rows, ['Domain', 'Niches', 'new in v4', 'Landmarks', 'new in v4', 'Verified-active', 'Female', 'Bridgers'])
LRN = {'L': 'Left', 'CL': 'Center-left', 'C': 'Center', 'CR': 'Center-right', 'R': 'Right', 'X': 'Cross-cutting / off-axis'}
lr_rows = []
v3place = {n['niche_id']: n['placement']['left_right'] for n in v3['niches']}
for k in ['L', 'CL', 'C', 'CR', 'R', 'X']:
    ns = [n for n in niches if n['placement']['left_right'] == k]
    ls = [l for l in lms if N[l['primary_niche']]['placement']['left_right'] == k]
    lr_rows.append([LRN[k], sum(1 for v in v3place.values() if v == k), len(ns), sum(1 for n in NEWN if n['placement']['left_right'] == k), len(ls)])
LR_T = table(lr_rows, ['Placement', 'Niches v3', 'Niches v4', 'new in v4', 'Landmarks v4'])
lefty = lr_rows[0][2] + lr_rows[1][2]; righty = lr_rows[3][2] + lr_rows[4][2]
ver_rows = [[k, SC[k], pct(SC[k], len(lms)), sum(1 for l in NEWL if l['verification'] == k), v3c['by_verification'].get(k, 0)] for k in ['verified-active', 'pending', 'stale']]
VER_T = table(ver_rows, ['Status', 'Landmarks v4', 'Share', 'of which new in v4', 'v3'])
ROLE_T = table([[r, sum(l['role'] == r for l in lms), pct(sum(l['role'] == r for l in lms), len(lms)), sum(l['role'] == r for l in NEWL)] for r in ['core', 'bridger', 'edge']],
               ['Role (primary)', 'Landmarks', 'Share', 'new in v4'])
G = collections.Counter(l['gender'] for l in lms)
GEN_T = table([[g, G[g], pct(G[g], len(lms)), sum(l['gender'] == g for l in NEWL)] for g in ['male', 'female', 'nonbinary', 'mixed', 'unknown'] if G[g]],
              ['Gender', 'Landmarks', 'Share', 'new in v4'])
PER = collections.Counter(len(n['landmarks']) for n in niches)
PER_T = table([[k, PER[k]] for k in sorted(PER)], ['Primary landmarks per niche', 'Niches'])
no_va = [n for n in niches if n['verified_active_landmarks'] == 0]
no_va_core = [n for n in niches if not n['has_verified_active_core']]


def has_bridger(n):
    return any(L[x]['role'] == 'bridger' for x in n['landmarks']) or any(L[x].get('secondary_roles', {}).get(n['niche_id']) == 'bridger' for x in n['secondary_landmarks'])


no_br = [n for n in niches if not has_bridger(n)]
no_br_no_edge = [n for n in no_br if not any(L[x]['role'] == 'edge' for x in n['landmarks'])]
women_zero = [n for n in niches if not any(L[x]['gender'] in ('female', 'mixed') for x in n['landmarks'])]
_v3L = {l['landmark_id']: l for l in v3['landmarks']}
v3_women_zero = sum(1 for n in v3['niches'] if not any(_v3L[x]['gender'] in ('female', 'mixed') for x in n['landmarks']))
v3_no_va = sum(1 for n in v3['niches'] if n['verified_active_landmarks'] == 0)
v3_no_br = sum(1 for n in v3['niches'] if not (any(_v3L[x]['role'] == 'bridger' for x in n['landmarks']) or any(_v3L[x].get('secondary_roles', {}).get(n['niche_id']) == 'bridger' for x in n['secondary_landmarks'])))

# ------------------------------------------------------------------ SEED-v4.md
md = ["# Dialogos Arena seed dataset: SEED-v4\n",
      f"Author of record: Benjamin Life (@omniharmonic). SEED-v3 plus the g7 (online subcultures) and g8 (holistic sweep) gap fills and a small QA gap fill, {D.TODAY}. "
      "Machine-readable data: `SEED-v4.json`. Decisions and audit: `QA-REPORT-v4.md`. Open checks: `VERIFICATION-QUEUE-v4.json`. "
      "Built by `scripts/build_v4.py` from `scripts/decisions_v4.py` over `SEED-v3.json`.\n",
      "## Summary\n",
      f"- **{len(niches)} niches, {len(lms)} landmarks** (SEED-v3: {v3c['niches']} / {v3c['landmarks']}). New in v4: {len(NEWN)} niches, {len(NEWL)} landmark records. {len(ALTS)} alternates held out; 1 excluded (unchanged).",
      f"- Verification: **{SC['verified-active']} verified-active ({pct(SC['verified-active'], len(lms))})**, {SC['pending']} pending, {SC['stale']} stale.",
      f"- Women {pct(fem(lms), len(lms))} of landmarks (v3: 29%). Bridgers {pct(br(lms), len(lms))} by primary role (v3: 26%).",
      f"- {len(MIRRORS)} mirror pairs ({len(D.MIRRORS_V4)} new).",
      f"- Flagged for Benjamin: {len(FLAGGED)} landmarks ({len(CONFLICT)} conflict-of-interest) and {len(NFLAG)} niches (outside reviewer).",
      f"- g8 coverage matrix: {sum(x[1] for x in COV)} outside-taxonomy categories checked; {cov_mapped} covered ({cov_closed} former gaps closed in v4), {cov_tot['still a gap']} still gaps.\n",
      "## Niches by domain\n",
      "Roles: **c** core, **b** bridger, **e** edge. **\\*** = pending. § stale. ° non-US voice. ⚑ flagged for Benjamin. "
      "*also:* landmarks whose primary home is elsewhere. **[v4]** = niche new in this version. **(outside review)** = near Benjamin's own field.\n"]
for d in DOM:
    md.append(f"### {DN[d]}\n")
    rows = []
    for n in [n for n in niches if n['domain'] == d]:
        nmx = f"**{n['name']}**" + (' [v4]' if n['niche_id'] not in V3N else '') + (' (outside review)' if n['flag_for_benjamin'] else '')
        if n['atlas_match']: nmx += f" *(Atlas: {n['atlas_match']})*"
        lm = ', '.join(f"{L[x]['name']} ({L[x]['role'][0]}){tag(L[x])}" for x in n['landmarks'])
        if n['secondary_landmarks']: lm += '; *also:* ' + ', '.join(L[x]['name'] + tag(L[x]) for x in n['secondary_landmarks'])
        rows.append([nmx, first_sentence(n['description']), lm])
    md.append(table(rows, ['Niche', 'Description', 'Landmarks']) + '\n')
md.append("## Alternates (held out of the map)\n")
md.append(table([[a['name'], a['primary_niche'], a['alternate_reason']] for a in ALTS], ['Name', 'Would sit in', 'Why held']) + '\n')
open(f'{SEED}/SEED-v4.md', 'w').write('\n'.join(md))

# ------------------------------------------------------------------ VERIFICATION-QUEUE-v4.json
queue = {d: [] for d in DOM}
for l in sorted([l for l in lms if l['verification'] != 'verified-active'], key=lambda l: (DOM.index(l['domain']), -RR[l['role']], l['primary_niche'], l['landmark_id'])):
    checks = [f"find a dated first-person item (episode, video, post) on or after {D.WINDOW}"]
    if l['verification'] == 'stale': checks = ['latest dated item is older than ~12 months: confirm or replace (see suggested_swaps)']
    plat = '; '.join(f'{k}={v}' for k, v in l['platforms'].items() if v)
    if plat: checks.append('confirm handles/URLs: ' + plat[:300])
    if l.get('us_focus_flag'): checks.append('non-US voice: confirm centrality to the US niche')
    if l['flag_for_benjamin']: checks.append(f"Benjamin decision pending ({l['flag_type']}): {l['flag_for_benjamin']}")
    for c in l.get('open_checks') or []: checks.append(c)
    queue[l['domain']].append(dict(landmark_id=l['landmark_id'], name=l['name'], primary_niche=l['primary_niche'], niche_name=nm(l['primary_niche']),
                                   role=l['role'], longform_output=l['longform_output'], verification=l['verification'], evidence_date=l['evidence_date'],
                                   new_in_v4=l['landmark_id'] not in V3L, source=l['verification_source'], notes=l['verification_notes'], checks=checks))
qmeta = dict(generated=D.TODAY, author_of_record='Benjamin Life (@omniharmonic)', total=sum(len(v) for v in queue.values()),
             by_domain={d: len(v) for d, v in queue.items()}, by_role=dict(collections.Counter(x['role'] for v in queue.values() for x in v)),
             new_in_v4=sum(x['new_in_v4'] for v in queue.values() for x in v),
             note=f"Every SEED-v4 landmark that is not verified-active, grouped by domain, core first. 'spot_check' = v3 spot-checks still open plus v4 records "
                  f"verified with a year-only or approximate date. 'alternates' are held-out records.")
spot_all = [s for s in spot_v3 if s['landmark_id'] in L and L[s['landmark_id']]['verification'] == 'verified-active'] + \
    [dict(landmark_id=x, name=L[x]['name'], primary_niche=L[x]['primary_niche'], role=L[x]['role'], source=L[x]['verification_source'],
          check=f"evidence date recorded as '{L[x]['evidence_date']}': record an exact dated item on or after {D.WINDOW}") for x in spot]
json.dump(dict(meta=qmeta, queue=queue, spot_check=spot_all,
               alternates=[dict(landmark_id=a['landmark_id'], name=a['name'], would_sit_in=a['primary_niche'], verification=a['verification'], reason=a.get('alternate_reason')) for a in ALTS],
               held_out=[dict(landmark_id='androgenic', name='Androgenic', status='EXCLUDED (unchanged)', checks=['age: confirm >= 18 from a reliable source before any inclusion'])],
               candidates_unverified_g7=ADD['g7-online-subcultures.additions']['candidates_unverified']),
          open(f'{SEED}/VERIFICATION-QUEUE-v4.json', 'w'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ QA-REPORT-v4.md
R = ["# QA and merge report: Dialogos Arena SEED-v4\n",
     f"Author of record: Benjamin Life (@omniharmonic). QA/merge pass over SEED-v3 and the g7 (online subcultures) and g8 (holistic sweep) gap fills, {D.TODAY}. "
     "Every judgment call is data in `scripts/decisions_v4.py`; `scripts/build_v4.py` applies them as a delta over `SEED-v3.json` and renders all outputs. No v3 file was modified.\n",
     "## 1. Result\n",
     f"- **{len(niches)} niches, {len(lms)} landmarks** (v3: {v3c['niches']} / {v3c['landmarks']}). Added {len(NEWN)} niches (g7 4, g8 9, QA 1) and {len(NEWL)} landmark records; {len(ALTS)} alternates unchanged.",
     f"- Structural validation: 4 g7/g8 files parsed; {len(STRUCT)} schema problems. Build warnings: {len(WARN)} (no thin, over-cap or core-less niches; no dangling references).",
     f"- Verification: {SC['verified-active']} verified-active ({pct(SC['verified-active'], len(lms))}), {SC['pending']} pending, {SC['stale']} stale.",
     f"- Women {pct(fem(lms), len(lms))} of landmarks (v3 29%); {pct(fem(NEWL), len(NEWL))} of v4 additions. Bridgers {pct(br(lms), len(lms))} (v3 26%).",
     f"- Mirror pairs: {len(MIRRORS)} ({len(D.MIRRORS_V4)} new). Unpaired issue niches: {', '.join(UNPAIRED) or 'none'}.",
     f"- g8 coverage matrix: {sum(x[1] for x in COV)} external categories across {len(COV)} taxonomies; {cov_mapped} covered (incl. {cov_closed} former gaps closed in v4: {cov_tot['gap closed by v4 niche']} by new niches, {cov_tot['gap closed by v4 sub-niche/landmark']} by sub-niches or landmarks), {cov_tot['still a gap']} still gaps, {cov_tot['excluded by design'] + cov_tot['no niche needed (fails bar)']} excluded or not needed (§8).\n",
     "## 2. Decisions needing Benjamin\n",
     "### 2.1 Conflict flags (`flags_for_benjamin.conflict_flags`)\n",
     table([[l['name'], nm(l['primary_niche']), 'v4' if l['landmark_id'] in D.CONFLICT_NEW else 'v3', l['flag_for_benjamin']] for l in CONFLICT], ['Landmark', 'Niche', 'Added', 'Reason']) + '\n',
     "Brad Carson is new: the funding claim is from g8's sources (\"reportedly\") and was not independently checked. Because the seed was assembled with an Anthropic model, keeping him is Benjamin's call, not the build's.\n",
     "### 2.2 All landmark flags (v3 flags kept unchanged)\n",
     table([[l['name'], nm(l['primary_niche']), l['flag_type'], l['flag_for_benjamin'], l['verification']] for l in sorted(FLAGGED, key=lambda l: (l['flag_type'], l['name']))],
           ['Landmark', 'Niche', 'Type', 'Reason', 'Status']) + '\n',
     "### 2.3 Niches that need an outside reviewer\n",
     table([[n['name'], 'v4' if n['niche_id'] in D.OUTSIDE_REVIEW_NEW else 'v3', n['flag_for_benjamin']] for n in NFLAG], ['Niche', 'Added', 'Why']) + '\n',
     "### 2.4 Open calls\n",
     "1. **Haaland and Woodard moved** (§4.2). Reverse if Benjamin prefers g8's minimal change for Haaland. Side effect: liberal feminism's remaining primaries (Valenti, Filipovic) are both pending, so it now has no verified-active primary; verifying either (both publish weekly newsletters) fixes this cheaply.\n"
     "2. **Taylor Lorenz and William Costello** are outside interpreters (edge) in looksmaxxing, not adherents; move Lorenz to streamer-creator-culture if landmarks must be adherents (that niche is at the cap).\n"
     "3. **Thin new niches** to demote if verification fails: Sober-curious (both primaries pending), Sikh American voices (Singh pending), Main Street small business (2 primaries), State sovereignty/secession (Evans pending).\n"
     "4. **Secession** maps the sovereign-citizen movement only as a sub-niche, with no landmarks (exclusion rule).\n"
     "5. v3 open calls (edge as bridger; scale; Tate/Fuentes decisions) are unchanged.\n",
     "## 3. New niches\n",
     table([[f"**{n['name']}** (`{n['niche_id']}`)", n['domain'].split('-')[0], (n['gap_meta'] or {}).get('gap_type'), n['placement']['left_right'],
             ', '.join(f"{L[x]['name']} ({L[x]['role'][0]}){tag(L[x])}" for x in n['landmarks']) + ('; also: ' + ', '.join(L[x]['name'] for x in n['secondary_landmarks']) if n['secondary_landmarks'] else '')]
            for n in NEWN], ['Niche', 'Dom', 'gap_type', 'L/R', 'Landmarks']) + '\n',
     "Atlas matches normalized to the 39 known Owocki names (raw partial labels replaced): " + '; '.join(f"`{a}`: '{b}' → {c}" for a, b, c in LOG.get('atlas', [])) + ".\n",
     "Boundary calls accepted from the agents: incel/blackpill stays a sub-niche of looksmaxxing (mapped only through adult researchers and journalists); 4B / decentering men promoted out of liberal feminism; "
     "wellness girlies kept apart from MAHA and fitness-biohacking; sober-curious kept apart from harm reduction and recovery-first; Sikh voices kept apart from Hindu American voices; "
     "farm-and-ranch mainstream kept apart from the rural populist farmer movement (now mirrored); tribal-nations split out of Land Back. g8 suggested minimalism as a degrowth sub-niche while g7 made it a niche: "
     "the niche wins, and degrowth's sub-niche now points to it.\n",
     "## 4. Additions to existing niches, dedupe and moves\n",
     "### 4.1 New records in existing niches\n",
     table([[L[x]['name'], nm(n), r, v, why] for x, n, r, v, why in LOG.get('add_lm', [])], ['Landmark', 'Niche', 'Role', 'Status', 'Reason']) + '\n',
     "### 4.2 Primary moves\n",
     table([[L[x]['name'], nm(o), nm(n), r, why] for x, o, n, r, why in LOG.get('moved', [])], ['Landmark', 'From', 'To', 'New role', 'Reason']) + '\n',
     f"Not moved: Ruby Warrington. {D.NOT_MOVED['ruby-warrington']}\n",
     "### 4.3 Dedupe and secondary listings\n",
     f"All {len(NEWL)} new names were checked against the {len(ALL_IDS)} v3 landmark and alternate ids (by id and by normalized name); none duplicates a v3 record. "
     f"{len(LOG.get('secondary', []))} secondary listings of existing people were applied (roles in `secondary_roles`):\n",
     table([[L[x]['name'], nm(L[x]['primary_niche']), nm(n), r or '—'] for x, n, r, _ in LOG.get('secondary', [])], ['Landmark', 'Primary', 'Secondary in', 'Role']) + '\n',
     "## 5. Cheap gaps (QA step 2)\n",
     table([
         ["Riley Gaines / 'Save women's sports'", "Added to **Gender-critical feminism** as bridger (verified 2025-12-17, new OutKick multi-year podcast deal). That niche already holds the anti-self-ID-in-sports position and has its mirror (LGBTQ+ & trans rights). Secondary in sports-talk culture (edge) and gender-medicine skeptics (bridger). Sub-niches added in both gender-critical feminism and sports-talk culture. No new niche (one voice checked)."],
         ['COVID-conscious community (mirror of medical freedom)', "**Added** `covid-conscious-long-covid` (D4, cross D6/D2): Betsy Ladyzhets (core, The Sick Times / Still Here, verified 2026-03-27), Beatrice Adler-Bolton & Artie Vierkant (Death Panel; bridger, verified Oct 2026), Julia Doubleday (core, pending). Bar met (2 verified adult long-form voices). Mirror pair recorded; disability sub-niche re-pointed."],
         ['A woman voice in minimalism', "Added **Dawn Madsen (The Minimal Mom)** as bridger (YouTube upload about 2026-10-02 via aggregator; approximate, in spot-check). Juliet Schor (secondary) is also a woman."],
     ], ['Gap', 'Result']) + '\n',
     "Considered and not added: " + '; '.join(f"{a}: {b}" for a, b in D.CONSIDERED_STEP2) + "\n",
     "## 6. Sub-niche changes\n",
     '\n'.join(f"- `{n}`: {k} " + (f"'{o[:80]}' → " if o else '') + f"'{s}'" for n, k, o, s in LOG.get('subniche', [])),
     f"- `crypto-degens`: {D.SUBNICHE_NOOP['crypto-degens']}\n",
     "## 7. Balance audit\n",
     "### 7.1 By domain (incl. D9)\n", DOM_T + '\n',
     "### 7.2 Left / right / other (rough QA placement)\n", LR_T + '\n',
     f"Left + center-left niches: {lefty}; right + center-right: {righty}; cross-cutting {lr_rows[5][2]}; center {lr_rows[2][2]}. "
     f"v4 adds {sum(1 for n in NEWN if n['placement']['left_right'] in ('L', 'CL'))} left-leaning, {sum(1 for n in NEWN if n['placement']['left_right'] in ('R', 'CR'))} right-leaning, "
     f"{sum(1 for n in NEWN if n['placement']['left_right'] == 'C')} center and {sum(1 for n in NEWN if n['placement']['left_right'] == 'X')} cross-cutting niches (the AI backlash and secession niches are cross-party).\n",
     "### 7.3 Verification, roles and gender\n", VER_T + '\n', ROLE_T + '\n', GEN_T + '\n',
     f"Women: {pct(fem(lms), len(lms))} of landmarks ({pct(femx(lms), len(lms))} counting mixed-gender duo records). Bridgers: {pct(br(lms), len(lms))} by primary role. "
     f"Niches whose primary landmarks include no woman: {len(women_zero)} (v3: {v3_women_zero}).\n",
     "### 7.4 Coverage gaps\n",
     f"**Niches with no verified-active primary landmark ({len(no_va)}; v3: {v3_no_va}):** " + (', '.join(f"{n['name']} (`{n['niche_id']}`)" for n in no_va) or 'none') + '.\n',
     f"**Niches without a verified-active core: {len(no_va_core)}** (field `has_verified_active_core`); new in v4: " + (', '.join(n['name'] for n in no_va_core if n['niche_id'] not in V3N) or 'none') + '.\n',
     f"**Niches lacking a bridger ({len(no_br)}; v3: {v3_no_br})**, counting bridger roles in secondary listings: " + ', '.join(n['name'] for n in no_br) + '.',
     f"If edge may count as bridger, {len(no_br_no_edge)} remain: " + (', '.join(n['name'] for n in no_br_no_edge) or 'none') + '.\n',
     "### 7.5 Mirror pairs\n",
     f"{len(MIRRORS)} pairs ({len(MIRRORS) - len(D.MIRRORS_V4)} from v3, {len(D.MIRRORS_V4)} new). New pairs:\n",
     table([[nm(a), nm(b), t] for a, b, t in D.MIRRORS_V4], ['Side A', 'Side B', 'Arena']) + '\n',
     "New issue exceptions: " + '; '.join(f"{nm(k)}: {v}" for k, v in D.ISSUE_EXCEPTIONS_V4.items()) + f" Unpaired after the check: {', '.join(UNPAIRED) or 'none'}.\n",
     "### 7.6 Landmarks per niche\n", PER_T + '\n',
     "## 8. g8 coverage matrix summary\n",
     f"g8 mapped SEED-v3 (plus its own new niches) against {len(COV)} outside taxonomies. Counts parsed from `raw/g8-holistic-sweep.md` §1; 'still a gap' is any row marked GAP without a v4 fix.\n",
     COV_T + '\n',
     f"**{sum(x[1] for x in COV)} external categories: {cov_mapped} covered (of which {cov_closed} were gaps closed in v4), {cov_tot['still a gap']} still gaps, {cov_tot['excluded by design'] + cov_tot['no niche needed (fails bar)']} excluded or not needed.** Remaining gaps: older Americans / boomers (fails the bar), Iranian American diaspora (unchecked); "
     "the 19 unknown Owocki Atlas names are outside the matrix. Neo-Nazis are excluded by design.\n",
     "## 9. Content hygiene\n",
     f"- Gap-file flag texts on landmarks: {len(LOG.get('raw_flag_dropped', []))} found (none carried; flags set only from decisions_v4).",
     f"- Private-vault citations removed: {len(HYG)}.",
     f"- Residual keyword scan of new niches/records ({len(RESID)} hits), all reviewed: " + ('; '.join(f"`{a}`.{b} '{c}'" for a, b, c, _ in RESID) or 'none') +
     ". They are topic words (addiction as a policy frame, chronic illness as the niche's subject, the Death Panel show name, the death penalty as a campaign issue); none is a personal allegation, health or conduct claim about a seeded person. The secession niche's sovereign-citizen sub-niche label notes the FBI's public view of that movement (descriptive, no person named).",
     "- Ages: Kareem Shami adult per the Guardian (2024, aged 22). No minors, private individuals or designated-organization spokespeople added.\n",
     "## 10. Remaining TODO gaps\n",
     '\n'.join([
         "- **Older Americans / retirees** (fails the bar; v3 and g8 agree).",
         "- **Iranian American diaspora** (regime-change vs. anti-war split; D8): unchecked.",
         "- **Jewish secular / cultural voices** (Tablet's Unorthodox): unchecked.",
         "- **Public-lands transfer side**: sub-niche only; needs a long-form voice before it can mirror hunter-conservationists.",
         "- **Occupational cultures**: nurses/healthcare workers, truckers, first responders (sub-niches only).",
         "- **Black women's 'leveling up' / divestment** (Christelyn Karazin): re-check; may meet the bar.",
         "- **AI-companion users**: strong candidate for promotion once adult public voices from the user side exist.",
         "- **'Save women's sports'**: if a second verified voice is found (Paula Scanlan, Payton McNabb), consider a small niche.",
         "- **Woman core voices** for markets-investing (CNBC/macro) and a Southern Black farmer with long-form output for Black agrarianism.",
         "- **g7 unverified candidates**: Eric Garcia, Ari Ne'eman (neurodivergence), Emmeline Clein, Christy Harrison (fat liberation), Christelyn Karazin (in VERIFICATION-QUEUE-v4.json).",
         "- **Pending in v4**: " + ', '.join(sorted(L[x]['name'] for x in [l['landmark_id'] for l in NEWL if l['verification'] == 'pending'])) + '.',
         "- Unchanged v3 TODOs: 19 unknown Atlas names; Puerto Rico statehood; Black Hebrew Israelites; Korean and Vietnamese evangelicals; Spanish-language media depth; WNBA fandom niche.",
     ]) + '\n',
     "## 11. Verification queue\n",
     f"`VERIFICATION-QUEUE-v4.json` holds **{qmeta['total']} landmarks** (pending or stale; {qmeta['new_in_v4']} new in v4), grouped by domain, cores first: "
     + ', '.join(f"{DN[d]} {qmeta['by_domain'][d]}" for d in DOM) + f". By role: {qmeta['by_role']}. Spot-checks: {len(spot_all)} ({len(spot)} new in v4: "
     + ', '.join(L[x]['name'] for x in spot) + "). Also lists alternates, the held-out record and g7's unverified candidates.\n",
     "## Searches used\n",
     f"{sum(1 for s in D.SEARCHES if s[0] == 'WebSearch')} WebSearch and {sum(1 for s in D.SEARCHES if s[0] == 'WebFetch')} WebFetch calls (budget ≤10 searches): " + '; '.join(f"{a}: {b}" for a, b in D.SEARCHES) + '.\n']
open(f'{SEED}/QA-REPORT-v4.md', 'w').write('\n'.join(R))
print('wrote SEED-v4.json, SEED-v4.md, QA-REPORT-v4.md, VERIFICATION-QUEUE-v4.json')
print('VA', dict(SC), 'female', pct(fem(lms), len(lms)), 'bridgers', pct(br(lms), len(lms)), 'no_va', len(no_va), 'no_br', len(no_br), 'queue', qmeta['total'], 'spot', len(spot_all), len(spot))
print('LR', lr_rows, 'COV', sum(x[1] for x in COV), cov_mapped, dict(cov_tot))
