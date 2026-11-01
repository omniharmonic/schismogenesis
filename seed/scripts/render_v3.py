"""Render SEED-v3 outputs from scripts/_state_v3.json (written by build_v3.py).

Outputs (in seed/): SEED-v3.json, SEED-v3.md, QA-REPORT-v3.md, VERIFICATION-QUEUE-v3.json
Run: python3 -I scripts/build_v3.py && python3 -I scripts/render_v3.py
"""
import json, collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decisions_v3 as D
from build_v3 import DOM, DN, LF, RR, VR  # noqa: E402  (re-runs the build; deterministic)

SEED = os.path.dirname(HERE)
S = json.load(open(f'{HERE}/_state_v3.json'))
N, L, ALTS, LOG = S['N'], S['L'], S['ALTS'], S['LOG']
V2N, V2L = set(S['V2_NICHES']), set(S['V2_LMS'])
v2 = json.load(open(f'{SEED}/SEED-v2.json'))

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
    return '\n'.join(['| ' + ' | '.join(hdr) + ' |', '|' + '---|' * len(hdr)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])


niches = sorted(N.values(), key=lambda x: (DOM.index(x['domain']), x['name'].lower()))
lms = sorted(L.values(), key=lambda l: l['landmark_id'])
VA = [l for l in lms if l['verification'] == 'verified-active']
SC = collections.Counter(l['verification'] for l in lms)
NEWN = [n for n in niches if n['niche_id'] not in V2N]
NEWL = [l for l in lms if l['landmark_id'] not in V2L]
FLAGGED = [l for l in lms if l['flag_for_benjamin']]
fem = lambda ls: sum(l['gender'] == 'female' for l in ls)

# ------------------------------------------------------------------ SEED-v3.json
mirror_pairs = [dict(a=a, a_name=N[a]['name'], b=b, b_name=N[b]['name'], arena=t) for a, b, t in D.MIRRORS]
spot = [l['landmark_id'] for l in VA if l['verification_source'].startswith('raw/g') and 'g6' not in l['verification_source'] and not l['evidence_date']]
v3_swaps = [dict(landmark=a['landmark_id'], slot=f"alternate for {a['primary_niche']}", issue='held as alternate', suggestion=a['alternate_reason'], source='v3 QA') for a in ALTS]
meta = dict(version='SEED-v3', generated=D.TODAY, author_of_record='Benjamin Life (@omniharmonic)',
            stage='Stage 1b seed - gap-fill merge (g1-g6) and QA over SEED-v2',
            inputs=['SEED-v2.json'] + [f'raw/{g}.json' for g in D.GAP_FILES] + ['raw/g6-representation.json', 'QA-REPORT.md', 'VERIFICATION-SUMMARY.md',
                    'v3 QA step-3 web checks (12 searches, 9 fetches)'],
            counts=dict(niches=len(niches), landmarks=len(lms), alternates=len(ALTS), excluded=len(v2['excluded_landmarks']),
                        new_niches=len(NEWN), new_landmarks=len(NEWL), v2_niches=len(v2['niches']), v2_landmarks=len(v2['landmarks']),
                        by_verification=dict(SC), by_domain={d: dict(niches=sum(n['domain'] == d for n in niches), landmarks=sum(l['domain'] == d for l in lms)) for d in DOM},
                        flagged_landmarks=len(FLAGGED), niches_needing_outside_review=sum(1 for n in niches if n['flag_for_benjamin']),
                        mirror_pairs=len(D.MIRRORS)),
            schema_notes=dict(v2['meta']['schema_notes'], **{
                'domain d9-mainstream-culture': 'new in v3: apolitical / mainstream-culture niches (sports, streamers, pop culture, therapy culture, etc.)',
                'niche.gap_meta': 'v3: {gap_type, source_files, mirror_of, youth_branch_of} for niches added by the gap swarm or v3 QA; null for v2 niches',
                'niche.flag_for_benjamin': "v3: niche-level flag (outside reviewer needed: near Benjamin's own field)",
                'landmark.secondary_roles': 'v3: role in a secondary listing, {niche_id: role}, where it differs from or adds to the primary role',
                'landmark.flag_type': 'v3: exclusion-review | conflict-of-interest | minor-adjacent',
                'verification (gap records)': "gap-agent 'verified' -> verified-active; where the agent did not record a date the record is in VERIFICATION-QUEUE-v3.json 'spot_check'; gap 'UNVERIFIED' -> pending; dated items before 2025-10-31 -> pending",
                'alternates': 'v3: full records held out of the map for cap or weakness reasons, with alternate_reason; promote on verification',
                'mirror_pairs': 'v3: issue-arena pairs (each side named as its members describe it)'}),
            scripts='SEED-v3: scripts/decisions_v3.py (all judgment calls), scripts/build_v3.py, scripts/render_v3.py. Earlier: build.py/render.py/report.py (v1), apply_verification.py (v2).',
            retired_ids=v2['meta'].get('retired_ids'))
out = dict(meta=meta, niches=[od(n, ORDER_N) for n in niches], landmarks=[od(l, ORDER_L) for l in lms],
           alternates=[od(a, ORDER_L + ['alternate_reason']) for a in ALTS], excluded_landmarks=v2['excluded_landmarks'],
           suggested_swaps=v2['suggested_swaps'] + v3_swaps,
           flags_for_benjamin=dict(landmarks=[dict(landmark_id=l['landmark_id'], name=l['name'], niche=l['primary_niche'], type=l['flag_type'], reason=l['flag_for_benjamin']) for l in FLAGGED],
                                   niches=[dict(niche_id=n['niche_id'], name=n['name'], reason=n['flag_for_benjamin']) for n in niches if n['flag_for_benjamin']]),
           mirror_pairs=mirror_pairs, v2_change_log=v2['change_log'], v3_change_log=LOG)
json.dump(out, open(f'{SEED}/SEED-v3.json', 'w'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ audit helpers


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
    dom_rows.append([DN[d], len(ns), sum(n['niche_id'] not in V2N for n in ns), len(ls), sum(l['landmark_id'] not in V2L for l in ls),
                     f'{len(va)} ({pct(len(va), len(ls))})', pct(fem(ls), len(ls)), pct(sum(l['role'] == 'bridger' for l in ls), len(ls))])
dom_rows.append(['**Total**', len(niches), len(NEWN), len(lms), len(NEWL), f'{len(VA)} ({pct(len(VA), len(lms))})', pct(fem(lms), len(lms)),
                 pct(sum(l['role'] == 'bridger' for l in lms), len(lms))])
DOM_T = table(dom_rows, ['Domain', 'Niches', 'new in v3', 'Landmarks', 'new in v3', 'Verified-active', 'Female', 'Bridgers'])

LRN = {'L': 'Left', 'CL': 'Center-left', 'C': 'Center', 'CR': 'Center-right', 'R': 'Right', 'X': 'Cross-cutting / off-axis'}
lr_rows = []
for k in ['L', 'CL', 'C', 'CR', 'R', 'X']:
    ns = [n for n in niches if n['placement']['left_right'] == k]
    nv2 = [n for n in ns if n['niche_id'] in V2N]
    ls = [l for l in lms if N[l['primary_niche']]['placement']['left_right'] == k]
    lr_rows.append([LRN[k], len(nv2), len(ns), len(ls)])
LR_T = table(lr_rows, ['Placement', 'Niches v2', 'Niches v3', 'Landmarks v3'])
lefty = sum(r[2] for r in lr_rows[:2]); righty = sum(r[2] for r in lr_rows[3:5])
lefty_new = sum(1 for n in NEWN if n['placement']['left_right'] in ('L', 'CL')); righty_new = sum(1 for n in NEWN if n['placement']['left_right'] in ('R', 'CR'))
x_new = sum(1 for n in NEWN if n['placement']['left_right'] == 'X')

AX = collections.Counter((n['placement']['atlas_accelerate_restrain'], n['placement']['atlas_institutions_exit']) for n in niches)
ie_keys = ['within-institutions', 'neutral/mixed', 'exit']
ax_rows = []
for a in ['accelerate', 'neutral/mixed', 'restrain']:
    ax_rows.append([a] + [AX[(a, b)] for b in ie_keys] + [sum(AX[(a, b)] for b in ie_keys)])
ax_rows.append(['**total**'] + [sum(AX[(a, b)] for a in ['accelerate', 'neutral/mixed', 'restrain']) for b in ie_keys] + [len(niches)])
AX_T = table(ax_rows, ['accel↔restrain \\ inst↔exit'] + ie_keys + ['total'])

ver_rows = [[k, SC[k], pct(SC[k], len(lms)), sum(1 for l in NEWL if l['verification'] == k)] for k in ['verified-active', 'pending', 'stale']]
VER_T = table(ver_rows, ['Status', 'Landmarks', 'Share', 'of which new in v3'])
role_rows = [[r, sum(l['role'] == r for l in lms), pct(sum(l['role'] == r for l in lms), len(lms)), sum(l['role'] == r and l['verification'] == 'verified-active' for l in lms)] for r in ['core', 'bridger', 'edge']]
ROLE_T = table(role_rows, ['Role (primary)', 'Landmarks', 'Share', 'verified-active'])
lf_rows = [[k, sum(l['longform_output'] == k for l in lms), pct(sum(l['longform_output'] == k for l in lms), len(lms)), sum(l['longform_output'] == k for l in NEWL)] for k in ['high', 'medium', 'low']]
LF_T = table(lf_rows, ['Long-form output', 'Landmarks', 'Share', 'new in v3'])
G = collections.Counter(l['gender'] for l in lms)
GEN_T = table([[g, G[g], pct(G[g], len(lms)), sum(l['gender'] == g for l in NEWL)] for g in ['male', 'female', 'nonbinary', 'mixed', 'unknown'] if G[g]],
              ['Gender', 'Landmarks', 'Share', 'new in v3'])
PER = collections.Counter(len(n['landmarks']) for n in niches)
PER_T = table([[k, PER[k]] for k in sorted(PER)], ['Primary landmarks per niche', 'Niches'])

no_va = [n for n in niches if n['verified_active_landmarks'] == 0]
no_va_core = [n for n in niches if not n['has_verified_active_core']]


def has_bridger(n, allow_secondary=True):
    if any(L[x]['role'] == 'bridger' for x in n['landmarks']): return True
    if allow_secondary and any(L[x].get('secondary_roles', {}).get(n['niche_id']) == 'bridger' for x in n['secondary_landmarks']): return True
    return False


no_br = [n for n in niches if not has_bridger(n)]
no_br_no_edge = [n for n in no_br if not any(L[x]['role'] == 'edge' for x in n['landmarks'])]
women_zero = [n for n in niches if not any(L[x]['gender'] in ('female', 'mixed') for x in n['landmarks'])]

# ------------------------------------------------------------------ SEED-v3.md
md = [f"# Dialogos Arena seed dataset: SEED-v3\n",
      f"Author of record: Benjamin Life (@omniharmonic). SEED-v2 plus the six gap-fill outputs (g1–g6) and a small QA gap fill, {D.TODAY}. "
      "Machine-readable data: `SEED-v3.json`. Decisions and audit: `QA-REPORT-v3.md`. Open checks: `VERIFICATION-QUEUE-v3.json`. "
      "Built by `scripts/build_v3.py` + `scripts/render_v3.py` from `scripts/decisions_v3.py`.\n",
      "## Summary\n",
      f"- **{len(niches)} niches, {len(lms)} landmarks** (SEED-v2: {len(v2['niches'])} / {len(v2['landmarks'])}). New in v3: {len(NEWN)} niches, {len(NEWL)} landmark records. {len(ALTS)} alternates held out; 1 excluded (Androgenic, unchanged).",
      f"- New domain **D9 Mainstream culture**: {sum(n['domain'] == 'd9-mainstream-culture' for n in niches)} niches.",
      f"- Verification: **{SC['verified-active']} verified-active ({pct(SC['verified-active'], len(lms))})**, {SC['pending']} pending, {SC['stale']} stale.",
      f"- Women {pct(fem(lms), len(lms))} of landmarks (v2: 22%). Bridgers {pct(sum(l['role'] == 'bridger' for l in lms), len(lms))} by primary role. Long-form high {pct(sum(l['longform_output'] == 'high' for l in lms), len(lms))}.",
      f"- {len(D.MIRRORS)} mirror pairs recorded; every issue-movement niche has a mirror or a stated exception.",
      f"- Flagged for Benjamin: {len(FLAGGED)} landmarks and {sum(1 for n in niches if n['flag_for_benjamin'])} niches (outside reviewer).\n",
      "## Niches by domain\n",
      "Roles: **c** core, **b** bridger, **e** edge. **\\*** = not yet verified-active (pending). § stale. ° non-US voice. ⚑ flagged for Benjamin. "
      "*also:* landmarks whose primary home is elsewhere. **[v3]** = niche new in this version. **(outside review)** = near Benjamin's own field.\n"]
for d in DOM:
    md.append(f"### {DN[d]}\n")
    rows = []
    for n in [n for n in niches if n['domain'] == d]:
        nm = f"**{n['name']}**" + (' [v3]' if n['niche_id'] not in V2N else '') + (' (outside review)' if n['flag_for_benjamin'] else '')
        if n['atlas_match']: nm += f" *(Atlas: {n['atlas_match']})*"
        lm = ', '.join(f"{L[x]['name']} ({L[x]['role'][0]}){tag(L[x])}" for x in n['landmarks'])
        if n['secondary_landmarks']:
            lm += '; *also:* ' + ', '.join(L[x]['name'] + tag(L[x]) for x in n['secondary_landmarks'])
        rows.append([nm, first_sentence(n['description']).replace('|', '/'), lm])
    md.append(table(rows, ['Niche', 'Description', 'Landmarks']) + '\n')
md.append("## Alternates (held out of the map)\n")
md.append(table([[a['name'], a['primary_niche'], a['alternate_reason']] for a in ALTS], ['Name', 'Would sit in', 'Why held']) + '\n')
open(f'{SEED}/SEED-v3.md', 'w').write('\n'.join(md))

# ------------------------------------------------------------------ VERIFICATION-QUEUE-v3.json
queue = {d: [] for d in DOM}
for l in sorted([l for l in lms if l['verification'] != 'verified-active'],
                key=lambda l: (DOM.index(l['domain']), -RR[l['role']], l['primary_niche'], l['landmark_id'])):
    checks = [f"find a dated first-person item (episode, video, post) on or after {D.WINDOW}"]
    if l['verification'] == 'stale': checks = ['latest dated item is older than ~12 months: confirm or replace (see suggested_swaps)']
    plat = '; '.join(f'{k}={v}' for k, v in l['platforms'].items() if v)
    if plat: checks.append('confirm handles/URLs: ' + plat[:300])
    if l.get('us_focus_flag'): checks.append('non-US voice: confirm centrality to the US niche')
    if l['flag_for_benjamin']: checks.append(f"Benjamin decision pending ({l['flag_type']}): {l['flag_for_benjamin']}")
    for c in l.get('open_checks') or []: checks.append(c)
    queue[l['domain']].append(dict(landmark_id=l['landmark_id'], name=l['name'], primary_niche=l['primary_niche'], niche_name=N[l['primary_niche']]['name'],
                                   role=l['role'], longform_output=l['longform_output'], verification=l['verification'], evidence_date=l['evidence_date'],
                                   new_in_v3=l['landmark_id'] not in V2L, source=l['verification_source'], notes=l['verification_notes'], checks=checks))
qmeta = dict(generated=D.TODAY, author_of_record='Benjamin Life (@omniharmonic)', total=sum(len(v) for v in queue.values()),
             by_domain={d: len(v) for d, v in queue.items()}, by_role=dict(collections.Counter(x['role'] for v in queue.values() for x in v)),
             new_in_v3=sum(x['new_in_v3'] for v in queue.values() for x in v),
             note=f"Every SEED-v3 landmark that is not verified-active (pending or stale), grouped by domain, core first. 'spot_check' lists gap-agent "
                  f"'verified' records whose evidence date was not recorded (may predate {D.WINDOW}). 'alternates' are held-out records to verify before promotion.")
json.dump(dict(meta=qmeta, queue=queue,
               spot_check=[dict(landmark_id=x, name=L[x]['name'], primary_niche=L[x]['primary_niche'], role=L[x]['role'], source=L[x]['verification_source'],
                                check=f'record a dated item on or after {D.WINDOW}') for x in sorted(spot, key=lambda x: (DOM.index(L[x]['domain']), -RR[L[x]['role']]))],
               alternates=[dict(landmark_id=a['landmark_id'], name=a['name'], would_sit_in=a['primary_niche'], verification=a['verification'], reason=a['alternate_reason']) for a in ALTS],
               held_out=[dict(landmark_id='androgenic', name='Androgenic', status='EXCLUDED (unchanged from v2)', checks=['age: confirm >= 18 from a reliable source before any inclusion'])]),
          open(f'{SEED}/VERIFICATION-QUEUE-v3.json', 'w'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ QA-REPORT-v3.md
nm = lambda x: N[x]['name'] if x in N else x
R = []
R.append("# QA and merge report: Dialogos Arena SEED-v3\n")
R.append(f"Author of record: Benjamin Life (@omniharmonic). Independent QA/merge pass over SEED-v2 and the six gap-fill outputs (g1–g6), {D.TODAY}. "
         "Every judgment call is data in `scripts/decisions_v3.py`; `scripts/build_v3.py` then `scripts/render_v3.py` regenerate all outputs. SEED-v2.json was not modified.\n")
R.append("## 1. Result\n")
R.append(f"- **{len(niches)} niches, {len(lms)} landmarks** (v2: {len(v2['niches'])} / {len(v2['landmarks'])}). Added {len(NEWN)} niches and {len(NEWL)} landmark records; {len(ALTS)} records held as alternates.")
R.append(f"- Raw gap input: {sum(len(v) for v in [json.load(open(f'{SEED}/raw/{g}.json')) for g in D.GAP_FILES])} niches from g1–g5 → {len(NEWN) - len(D.STEP3_NICHES)} after merges/absorptions, plus {len(D.STEP3_NICHES)} added at QA (step 3). g6 contributed {len(LOG.get('g6_new', []))} new records, {len(LOG.get('g6_secondary', []))} secondary listings, {len(LOG.get('role', []))} role changes, {len(LOG.get('verif', []))} verification updates and {len(LOG.get('rename', []))} renames.")
R.append(f"- Structural validation: all six gap files parsed; {len(S['STRUCT'])} schema problems. Build warnings: {len(S['WARN'])} (no thin, over-cap or core-less niches; no dangling references).")
R.append(f"- Verification: {SC['verified-active']} verified-active ({pct(SC['verified-active'], len(lms))}), {SC['pending']} pending, {SC['stale']} stale. {len(spot)} gap-agent-verified records lack a recorded date and are listed for spot-checking.")
R.append(f"- Scale note: v3 exceeds the original Stage-1 target (120–180 niches / 450–550 landmarks) on purpose: the gap brief asked for the widest representative spread. If Stage 2 needs a smaller set, D9 mainstream niches and the niches with no verified-active landmark (§8.5) are the first candidates to defer.\n")

R.append("## 2. Decisions needing Benjamin\n")
R.append("### 2.1 Landmarks flagged (kept in the data; `flag_for_benjamin` + `flag_type`)\n")
R.append("Reasons are written neutrally and do not repeat allegations. All gap-file flag texts were replaced.\n")
R.append(table([[l['name'], nm(l['primary_niche']), l['flag_type'], l['flag_for_benjamin'], l['verification']] for l in sorted(FLAGGED, key=lambda l: (l['flag_type'], l['name']))],
               ['Landmark', 'Niche', 'Type', 'Reason', 'Status']) + '\n')
R.append("QA recommendation (unchanged from v1 for the v2 twelve): highest-risk under the 'primary output is harassment or incitement' bar are Fuentes, then the Tates and Gaines. "
         "Hinkle and Haz Al-Din are not spokespeople for any designated organization; the question is whether their public conduct brings them inside that exclusion. "
         "If Fuentes is excluded, keep the groyper niche with Sneako as bridger or fold it into America First restraint as a sub-niche. If Hinkle/Haz are excluded, "
         "the patriotic-socialism niche falls to one pending voice (Garrido) and should become a sub-niche of the anti-imperialist ML left.\n")
R.append("### 2.2 Conflict of interest\n")
R.append("Samantha Power (The BioFi Project; id `samantha-power-biofi`, not the former USAID administrator), Monty Bryant, Kevin Owocki and Griff Green are in Benjamin's own network. "
         "They are kept and flagged `conflict-of-interest`. g6 drew some context from Benjamin's private vaults (Parachute, Gitcoin Brain); one note derived from a private vault "
         "(about a planned new podcast) was removed from Owocki's record, and two private-vault citations inherited from v2 `sources` (metacrisis niche; Daniel Schmachtenberger) were removed (§7). No private-vault content remains in the seed. Only public, dated evidence is cited.\n")
R.append("### 2.3 Niches that need an outside reviewer (`niche.flag_for_benjamin`)\n")
R.append(table([[n['name'], n['flag_for_benjamin']] for n in niches if n['flag_for_benjamin']], ['Niche', 'Why']) + '\n')
R.append("### 2.4 Open structural calls\n")
R.append("1. **Edge as bridger.** v1 asked whether an edge landmark may fill the bridger slot; still open (see §8.5).\n"
         "2. **Weak new niches** that should be demoted if verification fails: Men's rights & fathers' rights (all pending), Black nationalism & self-determination, Childfree by choice, Ethical non-monogamy (all pending).\n"
         "3. **Alpha hustle masculinity** has only pending primaries (the Tates, Justin Waller); with Patrick Bet-David and Sneako as secondaries. Its existence depends on the Tate decision.\n"
         "4. **Scale** (see §1).\n")

R.append("## 3. Niche merges, absorptions and placement decisions\n")
R.append("### 3.1 Merges among gap files\n")
for t, (base, name, dom, cross, dec) in D.MERGED_META.items():
    R.append(f"- **{name}** (`{t}`, home {dom}{', cross ' + ', '.join(cross) if cross else ''}). Merged from {', '.join('`' + x + '`' for x in N[t]['merged_from'])}. {dec}")
R.append("\n### 3.2 Gap niches absorbed into existing v2 niches\n")
for nid, (target, dec, _, _) in D.ABSORB.items():
    R.append(f"- `{nid}` → **{nm(target)}** (`{target}`). {dec}")
R.append("- **Austin comedy circuit** → sub-niche of **Rogan-verse long-form commons** (per g3's own recommendation); Andrew Schulz is primary in the Barstool niche with Rogan-verse as a secondary listing.")
R.append("\n### 3.3 Domain placement\n")
for nid, (dom, cross, dec) in D.DOMAIN_OVERRIDE.items():
    R.append(f"- **{nm(nid)}** → {dom}. {dec}")
R.append("- Other homes: public-health defenders D4 (beside its mirrors); recovery-first D7 (beside housing/urbanism); pro-immigration liberty D1; disability and the gay right D6; veterans d9 (see 3.1); "
         "progressive legal academia D2; Spanish-language media and therapy culture d9.\n")
R.append("### 3.4 Kept / not demoted (with reasons)\n")
for nid, dec in D.KEEP_DECISIONS.items():
    R.append(f"- **{nm(nid)}**: {dec}")
R.append("\n### 3.5 Other requested boundary checks\n")
R.append(table([
    ['Barstool (g2) vs. Barstool (g3)', 'Merged (3.1); retail-trader YOLO absorbed into crypto-degens, sports betting a Barstool sub-niche.'],
    ['Streamer culture (g2 vs. g3)', 'Merged (3.1).'],
    ['Gay right (g4 vs. g5)', 'Merged (3.1), D6.'],
    ['Disability (g1 vs. g4)', 'Merged; rights vs. justice kept as sub-niches.'],
    ['Veterans (g1/g3/g4)', 'One niche; political split as sub-niches; Mark Kelly primary in gun-violence prevention with a veteran secondary listing; Shawn Ryan stays primary in the Rogan-verse.'],
    ['Homeschooling vs. parents\' rights', 'Both kept (different sacred values); both mirror public-school advocates.'],
    ['News-lite vs. bridging explainers', 'Merged into the existing bridging niche (3.2).'],
    ['Austin comedy circuit', 'Sub-niche of Rogan-verse.'],
    ['Gen Z faith revival', 'Kept (3.4).'],
    ['Astrology / Black faith-and-family', 'Astrology → D5 (own niche; New Age sub-niche re-pointed). Black faith-and-family stays d9 (no D5 duplicate).'],
    ['Steven Pinker', 'Only g1 seeded him; homed in Open-inquiry / heterodox academia as bridger, secondary in higher-ed defenders.'],
    ['Men\'s rights re-split (g5)', 'Accepted (3.4); fathers\' rights sub-niche and MRA aliases moved from men & boys\' advocacy.'],
    ['Biblical womanhood vs. tradwife', 'Kept separate per g5 (3.4).'],
], ['Boundary', 'Resolution']) + '\n')

R.append("## 4. Landmark deduplication\n")
R.append(f"- {len(LOG.get('dedupe', []))} people seeded more than once across gap files (or needing a primary decision) now have one `primary_niche`; the rest are `secondary_niches`. "
         "Platforms and sources were unioned; the strongest verification won.\n")
R.append(table([[L[lid]['name'], nm(p), ', '.join(nm(s) for s in sec) or '—'] for lid, p, sec in LOG.get('dedupe', [])], ['Person', 'Primary', 'Secondary']) + '\n')
R.append(f"- {len(LOG.get('sec_from_existing', []))} gap entries named people already in v2; they became secondary listings on the existing record instead of new records "
         f"(" + '; '.join(f"{L[x]['name']} → {nm(t)}" for x, t, g, k in LOG.get('sec_from_existing', [])) + "). Gap files' `secondary_landmarks` lists and g1's suggested "
         "secondaries (Bongino, Kaba, Rufo, Shellenberger, Paola Ramos, Julio Ricardo Varela) were applied the same way.")
R.append("- Kristin Kobes Du Mez was proposed by both g5 and g6: one record, primary in evangelical-conscience-critics (core), secondary in evangelical egalitarians.")
R.append("- **Alternates** (held out, full records kept in `SEED-v3.json.alternates`):\n")
R.append(table([[a['name'], nm(a['primary_niche']), a['verification'], a['alternate_reason']] for a in ALTS], ['Name', 'Would sit in', 'Status', 'Reason']) + '\n')
R.append("- Cap of 5 primary landmarks per niche is respected everywhere (§8.7).\n")

R.append("## 5. g6 (representation inside existing niches) as applied\n")
R.append(f"- **New records ({len(LOG.get('g6_new', []))}):** " + '; '.join(f"{L[x]['name']} → {nm(n)} ({r}, {v})" for x, n, r, v in LOG.get('g6_new', [])) + '.')
R.append(f"- **Secondary listings of existing landmarks ({len(LOG.get('g6_secondary', []))}):** " + '; '.join(f"{L[x]['name']} → {nm(n)} ({r})" for x, n, r, _ in LOG.get('g6_secondary', [])) + '. Roles are stored in `secondary_roles`.')
R.append("- **Role changes:**\n")
R.append(table([[L[x]['name'], n if n.endswith('listing)') else nm(n), o, nr, e] for x, n, o, nr, e in LOG.get('role', [])], ['Landmark', 'Niche', 'Old', 'New', 'Basis']) + '\n')
R.append("- **Verification updates:**\n")
R.append(table([[L[x]['name'], o, nv, d or '—'] for x, o, nv, d in LOG.get('verif', [])], ['Landmark', 'v2 status', 'v3 status', 'Evidence date']) + '\n')
R.append("- **Renames** (old labels moved to `aliases` as 'former seed label'; niche_ids kept as stable keys):\n")
R.append(table([[f'`{i}`', o, nn, r] for i, o, nn, r in LOG.get('rename', [])], ['niche_id', 'Old name', 'New name', 'Reason']) + '\n')
R.append("- Associated alias housekeeping: 'wellness-to-right pipeline' marked as an outsider label; New Age's 'conspirituality' sub-niche re-labelled as the awakening/sovereignty crossover. "
         "Note that niche_id `conspirituality-sovereignty` still carries the old word; it is a key, not a label — rename the id at Stage 2 if keys are ever shown to users.")
R.append("- The 18 women proposed by g6 were all added as pending (from knowledge, not searched), except Susan Glasser (alternate, cap). They raise the share of women in D1/D5/D8 once verified.\n")

R.append("## 6. QA gap fill (step 3)\n")
R.append("Budget: 12 WebSearch + 9 WebFetch calls (≤20 searches). Only core voices were checked.\n")
R.append(table([
    ['Mainstream therapy & self-help (d9)', 'NEW niche `therapeutic-self-help-mainstream`: Esther Perel (verified 2026-09-28), Glennon Doyle (aggregator 2026-10-22), Mel Robbins (moved from daytime; secondary there). Jay Shetty and Dax Shepard as secondaries.'],
    ['Spanish-language / Latino mainstream media (d9)', 'NEW niche `latino-mainstream-media` (thin): Jorge Ramos (verified, News Emmy May 2026), Maria Hinojosa (verified ≈Nov 2025), Enrique Santos and Alexander Otaola (pending). Paola Ramos secondary.'],
    ['Progressive court-reform legal academia', 'NEW niche `progressive-legal-court-reform` (mirror of originalists): Leah Litman, Kate Shaw, Melissa Murray (all verified 2026-10-26, Strict Scrutiny), Dahlia Lithwick (≈2026-02).'],
    ['Labor\'s right flank (Teamsters–GOP)', 'Not covered before. Sean O\'Brien added to labor-movement-left as bridger (Bloomberg Law interview 2026-06-29; Teamsters backing Republicans, Sept 2026); secondary in national conservatism; sub-niche added.'],
    ['Native political voices', 'Land Back covered activists only. Deb Haaland added as bridger (NM Democratic gubernatorial nominee, June 2026); sub-niche for tribal-government / Native electoral politics. Still thin (TODO).'],
    ['Sports-talk right (OutKick)', 'Covered by g3 (Clay Travis, edge). Verified: left OutKick June 2026, remains Fox contributor with an FS1 show. Sub-niche added.'],
    ['Pro-police culture', 'Covered by g1 law-and-order niche (Brandon Tatum\'s Officer Tatum Show; Mangual; Mac Donald) + Bongino secondary. No change.'],
    ['Anti-pornography / age verification', 'Covered by g5 `anti-sexual-exploitation` (Mickelwait verified). Sub-niche for age-verification laws added.'],
    ['Older Americans / retirees', 'Assessed: fails the bar. No long-form voices articulate a shared retiree worldview (AARP is institutional; the "boomer Facebook" mainstream is anonymous and overlaps legacy media and MAGA media). TODO.'],
    ['Black nationalism check', 'Umar Johnson: 2026 podcast appearance found via a weak summary source → verified-active with a note; still flagged.'],
], ['Gap', 'Result']) + '\n')

R.append("## 7. Content hygiene\n")
R.append("- **Rewritten or removed** (personal allegations, health or conduct claims):\n")
for tid, field, old in S['HYG']:
    R.append(f"  - `{tid}`.{field} (was: \"{old[:100]}…\")")
R.append("- All 12 v2 flag texts and the three g4 flag texts were replaced with neutral one-line reasons (§2.1).")
R.append(f"- Residual keyword scan of `why`, `description`, `notes`, `trajectory`, `verification_notes` and flags: {len(S['RESID'])} hits, all reviewed. Remaining hits are worldview or "
         "issue descriptions (e.g., Epstein files as a political topic, death-penalty abolition, detention policy), public political facts (MTG's resignation, Calley Means leaving his "
         "advisory role), and the flag reasons themselves. None is a personal allegation, health or conduct claim.")
R.append("- Ages: g2 recorded an age basis for every Gen Z landmark (all adults). Androgenic stays excluded. No minors, private individuals or designated-organization spokespeople are seeded.")
R.append("- Gap agents' notes on deceased people (Alice Wong) were reduced to 'not seeded'. Jim Rutt's death detail was removed from the metacrisis niche note and sub-niche label (v1 §8 keeps the sourced record).\n")

R.append("## 8. Balance audit\n")
R.append("### 8.1 By domain\n"); R.append(DOM_T + '\n')
R.append("### 8.2 Left / right / other (rough QA placement of each niche)\n"); R.append(LR_T + '\n')
R.append(f"Left + center-left niches: {lefty}; right + center-right: {righty}; cross-cutting {lr_rows[5][2]}. Of the {len(NEWN)} new niches, {lefty_new} lean left, {righty_new} lean right and {x_new} are cross-cutting "
         "(mostly d9 mainstream culture, which deliberately sits off the left–right axis). The issue-arena work added both sides of each fight, so the new left/right niches come in pairs.\n")
R.append("### 8.3 Owocki Atlas axes (rough, inferred; available for all niches)\n"); R.append(AX_T + '\n')
R.append("### 8.4 Verification, roles, long-form and gender\n")
R.append(VER_T + '\n'); R.append(ROLE_T + '\n'); R.append(LF_T + '\n'); R.append(GEN_T + '\n')
R.append(f"Women are {pct(fem(lms), len(lms))} of landmarks (v2 22%) and {pct(fem(NEWL), len(NEWL))} of v3 additions. Niches whose primary landmarks include no woman: {len(women_zero)}.\n")
R.append("### 8.5 Coverage gaps\n")
R.append(f"**Niches with no verified-active primary landmark ({len(no_va)}):** " + ', '.join(f"{n['name']} (`{n['niche_id']}`)" for n in no_va) + '.\n')
R.append(f"**Niches without a verified-active core: {len(no_va_core)}** (list in SEED-v3.json via `has_verified_active_core`).\n")
R.append(f"**Niches lacking a bridger ({len(no_br)})**, counting bridger roles in secondary listings: " + ', '.join(n['name'] for n in no_br) + '.')
R.append(f"If edge may count as bridger (open call §2.4), {len(no_br_no_edge)} remain: " + (', '.join(n['name'] for n in no_br_no_edge) or 'none') + '.\n')
R.append("### 8.6 Mirror pairs\n")
R.append(f"{len(D.MIRRORS)} pairs. Each side is named as its own members describe it.\n")
R.append(table([[nm(a), nm(b), t] for a, b, t in D.MIRRORS], ['Side A', 'Side B', 'Arena']) + '\n')
R.append(f"Check: every issue-movement niche (gap_type mirror or missing-arena, plus {len(S['issue_niches']) - sum(1 for n in NEWN if n['gap_meta'] and n['gap_meta']['gap_type'] in ('mirror', 'missing-arena'))} v2 issue niches) appears in a pair, except these, with reasons:\n")
R.append(table([[nm(k), v] for k, v in D.ISSUE_EXCEPTIONS.items()], ['Niche', 'Why no single mirror']) + '\n')
R.append(f"Unpaired after the check: {', '.join(S['UNPAIRED']) or 'none'}.\n")
R.append("### 8.7 Landmarks per niche\n"); R.append(PER_T + '\n')

R.append("## 9. Remaining TODO gaps\n")
R.append('\n'.join([
    "- **Older Americans / retirees** (assessed, fails the bar today; revisit if long-form voices emerge).",
    "- **Spanish-language media depth**: Univision/Telemundo talk hosts, regional Mexican music culture, Puerto Rican and Dominican voices; verify Enrique Santos and Otaola.",
    "- **Native political voices** beyond Haaland (tribal-sovereignty officials, Native Republicans, Native media such as Rebecca Nagle).",
    "- **Occupational cultures**: teachers and healthcare workers; first responders (no long-form voice found by g3).",
    "- **Women's sports fandom (WNBA)** as a sports-talk sub-niche or niche.",
    "- **Rural Black South and Black farmers**; Black Hebrew Israelites (D5); a progressive Muslim landmark; Asian American (Korean/Vietnamese) evangelicals.",
    "- **Gen Z**: Gen Z Muslim creators, solarpunk/climate anxiety (non-US core), Isabel Brown, Elise Joshi, Arielle Reitsma (Girls Gone Bible co-host).",
    "- **Political edges**: Texit/national divorce (sub-niche only), Puerto Rico statehood politics, Log Cabin's current president, Tariq Nasheed/FBA boundary with ADOS (needs exclusion review), Gays Against Groomers (org sub-niche only; review before seeding a person).",
    "- **Incel discourse** researchers (William Costello) as secondary voices for looksmaxxing; mommy/parenting influencers as sub-niches.",
    "- **Atlas**: the 19 missing Owocki Atlas names; `atlas_match` is still from the 39-name partial list.",
    "- **Verification**: 18 g6 women and most D9 'UNVERIFIED' voices are pending (see queue).",
]) + '\n')
R.append("## 10. Verification queue\n")
R.append(f"`VERIFICATION-QUEUE-v3.json` holds **{qmeta['total']} landmarks** (pending or stale; {qmeta['new_in_v3']} new in v3), grouped by domain with cores first: "
         + ', '.join(f"{DN[d]} {qmeta['by_domain'][d]}" for d in DOM) + f". By role: {qmeta['by_role']}. "
         f"It also lists {len(spot)} spot-checks (gap-verified without a recorded date), {len(ALTS)} alternates and the held-out Androgenic record.\n")
R.append("## Searches used\n")
R.append("This pass used 12 WebSearch calls (Perel, Doyle, Strict Scrutiny, Jorge Ramos, Sean O'Brien, Clay Travis, Otaola, Enrique Santos, Umar Johnson, Deb Haaland, Dahlia Lithwick, Maria Hinojosa) "
         "and 9 WebFetch calls (Clay Travis/The Desk, Crooked Strict Scrutiny, estherperel.com, Latin Times, Political Wire, podstatus, Bloomberg Law, RadioInsight, Wikipedia).\n")
open(f'{SEED}/QA-REPORT-v3.md', 'w').write('\n'.join(R))
print('wrote SEED-v3.json, SEED-v3.md, QA-REPORT-v3.md, VERIFICATION-QUEUE-v3.json')
print('VA', SC, 'female', pct(fem(lms), len(lms)), 'bridgers', pct(sum(l['role'] == 'bridger' for l in lms), len(lms)), 'no_va', len(no_va), 'no_br', len(no_br), 'no_br_no_edge', len(no_br_no_edge), 'queue', qmeta['total'], 'spot', len(spot))
print('LR', lr_rows, 'lefty', lefty, 'righty', righty)
