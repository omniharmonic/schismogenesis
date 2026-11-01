import json,collections,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from decisions import NICHE_MERGE, MERGED_META, DROP
SEED='/home/claude/dialogos-arena/seed'
s=json.load(open(SEED+'/scripts/_state.json'))
N=s['niches'];L=s['lms']
DOM=['d1-right','d2-left-center','d3-tech-futures','d4-heterodox-sensemaking','d5-religion-spirituality','d6-gender-lifestyle-subcultures','d7-economy-ecology-place','d8-geopolitics-media']
DN={'d1-right':'D1 Right','d2-left-center':'D2 Left & center','d3-tech-futures':'D3 Tech & futures','d4-heterodox-sensemaking':'D4 Heterodox & sensemaking','d5-religion-spirituality':'D5 Religion & spirituality','d6-gender-lifestyle-subcultures':'D6 Gender, lifestyle & subcultures','d7-economy-ecology-place':'D7 Economy, ecology & place','d8-geopolitics-media':'D8 Geopolitics & media'}
for l in L.values(): l['domain']=N[l['primary_niche']]['domain']
niches=sorted(N.values(),key=lambda n:(DOM.index(n['domain']),n['name']))
for n in niches: n.pop('qa_decision_text',None)
lms=sorted(L.values(),key=lambda l:l['landmark_id'])
ORDER_N=['niche_id','name','domain','cross_domains','aliases','description','telos','sacred_values','existential_threats','combatants','adjacent_niches','sub_niches','size_estimate','cultural_influence','trajectory','atlas_match','limberg_barnes_match','placement','landmarks','secondary_landmarks','merged_from','qa_decision','sources','notes']
ORDER_L=['landmark_id','name','primary_niche','secondary_niches','domain','role','why','platforms','longform_output','active_2025_2026','verification','gender','flag_for_benjamin','sources','source_domains']
def od(d,o): return {k:d.get(k) for k in o}
meta=dict(version='SEED-v1',generated='2026-10-31',author_of_record='Benjamin Life (@omniharmonic)',
  stage='Stage 1 seed - QA/merge pass',inputs=[f'raw/{d}.json' for d in DOM]+['atlas-2026-07-28-partial.md'],
  counts=dict(niches=len(niches),landmarks=len(lms),raw_niches=194,raw_landmark_entries=654,raw_unique_people=572),
  schema_notes={'landmark_id':'kebab-case of public name; stable key','niche.landmarks':'landmark_ids whose primary_niche is this niche, ordered core>bridger>edge then longform',
    'niche.secondary_landmarks':'landmark_ids that list this niche as a secondary','placement':'rough QA judgment: left_right in L/CL/C/CR/R/X(cross-cutting); Atlas axes accelerate<->restrain and within-institutions<->exit',
    'active_2025_2026':'true = output seen/claimed in 2025-26; null = not confirmed (NOT inactive)','atlas_match':'from the PARTIAL Atlas list (39/58 names); null where no match in that list'},
  scripts='scripts/build.py (merge), scripts/render.py (outputs); decisions in scripts/decisions.py, gapfill.py, hygiene.py, annotate.py')
json.dump(dict(niches=[od(n,ORDER_N) for n in niches],landmarks=[od(l,ORDER_L) for l in lms],meta=meta),open(SEED+'/SEED-v1.json','w'),indent=1,ensure_ascii=False)

# ---------- stats
def pct(a,b): return f'{100*a/b:.0f}%'
nL=len(lms)
def table(rows,hdr):
    o='| '+' | '.join(hdr)+' |\n|'+'---|'*len(hdr)+'\n'
    for r in rows: o+='| '+' | '.join(str(x) for x in r)+' |\n'
    return o
by_dom=[(DN[d],sum(1 for n in niches if n['domain']==d),sum(1 for l in lms if l['domain']==d),
         sum(1 for l in lms if l['domain']==d and l['verification']=='verified')) for d in DOM]
by_dom.append(('**Total**',len(niches),nL,sum(1 for l in lms if l['verification']=='verified')))
T_dom=table([(a,b,c,f'{d} ({pct(d,c)})') for a,b,c,d in by_dom],['Domain','Niches','Landmarks','Verified'])
pl=collections.Counter(n['placement']['left_right'] for n in niches)
pll=collections.Counter(N[l['primary_niche']]['placement']['left_right'] for l in lms)
PLN={'L':'Left','CL':'Center-left','C':'Center','CR':'Center-right','R':'Right','X':'Cross-cutting / other'}
T_lr=table([(PLN[k],pl[k],pll[k]) for k in ['L','CL','C','CR','R','X']],['Placement','Niches','Landmarks'])
ax1=collections.Counter(n['placement']['atlas_accelerate_restrain'] for n in niches)
ax2=collections.Counter(n['placement']['atlas_institutions_exit'] for n in niches)
cross=collections.Counter((n['placement']['atlas_accelerate_restrain'],n['placement']['atlas_institutions_exit']) for n in niches)
A=['accelerate','neutral/mixed','restrain'];W=['within-institutions','neutral/mixed','exit']
T_ax=table([[a]+[cross[(a,w)] for w in W]+[ax1[a]] for a in A]+[['**total**']+[ax2[w] for w in W]+[len(niches)]],['accel↔restrain \\ inst↔exit']+W+['total'])
role=collections.Counter(l['role'] for l in lms)
T_role=table([(r,role[r],pct(role[r],nL)) for r in ['core','bridger','edge']],['Role','Landmarks','Share'])
lf=collections.Counter(l['longform_output'] for l in lms)
T_lf=table([(r,lf[r],pct(lf[r],nL)) for r in ['high','medium','low']],['Longform output','Landmarks','Share'])
g=collections.Counter(l['gender'] for l in lms)
gd=[(DN[d],)+tuple(sum(1 for l in lms if l['domain']==d and l['gender']==x) for x in ['male','female','mixed','nonbinary']) for d in DOM]
gd=[r+(pct(r[2],sum(r[1:])),) for r in gd]
T_g=table(gd+[('**Total**',g['male'],g['female'],g['mixed'],g['nonbinary'],pct(g['female'],nL))],['Domain','Male','Female','Mixed duo','Nonbinary','Female share'])
act=collections.Counter(str(l['active_2025_2026']) for l in lms)
nobridger=[n['niche_id'] for n in niches if not any(L[x]['role']=='bridger' for x in n['landmarks'])]
cnt=collections.Counter(len(n['landmarks']) for n in niches)
T_cnt=table([(k,cnt[k]) for k in sorted(cnt)],['Landmarks per niche (primary)','Niches'])
stats=f"""- **{len(niches)} niches, {nL} landmarks** (from 194 raw niches / 654 raw landmark entries / 572 unique people).
- Verified active by a domain agent or at QA: {sum(1 for l in lms if l['verification']=='verified')} ({pct(sum(1 for l in lms if l['verification']=='verified'),nL)}); `active_2025_2026` true {act['True']}, null {act['None']}.
- Bridgers: {role['bridger']} ({pct(role['bridger'],nL)}). Niches with no bridger in their primary set: {len(nobridger)}.
- Longform high: {pct(lf['high'],nL)}. Female landmarks: {pct(g['female'],nL)}.
- Atlas matches (partial list): {sum(1 for n in niches if n['atlas_match'])} niches.
- Landmarks with secondary niches: {sum(1 for l in lms if l['secondary_niches'])}. Flagged for Benjamin: {sum(1 for l in lms if l['flag_for_benjamin'])}.
"""
# ---------- SEED-v1.md
md=f"""# Dialogos Arena seed dataset: SEED-v1

Author of record: Benjamin Life (@omniharmonic). Stage 1 seed after the independent QA and merge pass, 2026-10-31. Machine-readable data: `SEED-v1.json`. Decisions are recorded in `QA-REPORT.md`, and the landmarks still to be checked are in `VERIFICATION-QUEUE.json`.

## Summary
{stats}
## Niches by domain

Landmark roles: **c** = core, **b** = bridger, **e** = edge. † marks a landmark not yet verified for 2025–26 activity. ⚑ marks a landmark flagged for Benjamin's decision. "Also:" lists landmarks whose primary home is elsewhere.

"""
for d in DOM:
    md+=f"### {DN[d]}\n\n| Niche | Description | Landmarks |\n|---|---|---|\n"
    for n in [n for n in niches if n['domain']==d]:
        desc=n['description'].split('. ')[0].rstrip('.')+'.'
        lm=', '.join(f"{L[x]['name']} ({L[x]['role'][0]}){'†' if L[x]['verification']!='verified' else ''}{'⚑' if L[x]['flag_for_benjamin'] else ''}" for x in n['landmarks'])
        if n['secondary_landmarks']: lm+='; *also:* '+', '.join(L[x]['name'] for x in n['secondary_landmarks'])
        am=f" *(Atlas: {n['atlas_match']})*" if n['atlas_match'] else ''
        md+=f"| **{n['name']}**{am} | {desc.replace('|','/')} | {lm} |\n"
    md+='\n'
audit=f"""## Balance audit

### By domain
{T_dom}
### By rough left–right placement
The placement is QA's rough judgment for each niche. X means cross-cutting or off the left–right axis.

{T_lr}
### Owocki Atlas axes (rough, inferred)
{T_ax}
### Landmark roles
{T_role}
### Long-form output
{T_lf}
### Gender of landmarks
{T_g}
### Landmarks per niche
{T_cnt}"""
md+=audit
open(SEED+'/SEED-v1.md','w').write(md)
json.dump(dict(stats_md=stats,audit_md=audit,nobridger=nobridger),open(SEED+'/scripts/_render.json','w'))

# ---------- verification queue
YOUNG={'clavicular':'Confirm age >= 18 (stated 20 as of May 2026).','sneako':'Confirm adult (believed mid-20s).','hannah-pearl-davis':'Confirm adult.',
       'chloe-cole':'Adult per D6 (b. 2004); re-confirm.','hope-woodard':'Confirm adult.','estee-williams':'Confirm adult.','joshua-citarella':None}
q=collections.defaultdict(list)
for l in lms:
    need=[]
    if l['verification']!='verified': need.append('verify 2025-26 activity (recent episodes/posts)')
    if l['active_2025_2026'] is not True: need.append('active_2025_2026 is null: confirm output in last ~12 months')
    pl=l['platforms']; filled=[k for k,v in pl.items() if v]
    if l['verification']!='verified' or len(filled)<=1: need.append('check handles/URLs: '+(', '.join(f"{k}={pl[k]}" for k in filled) if filled else 'no platforms listed'))
    if l['longform_output']=='low': need.append('low longform: find transcribable interviews or swap')
    if YOUNG.get(l['landmark_id']): need.append('age: '+YOUNG[l['landmark_id']])
    if l['landmark_id']=='jordan-b-peterson': need.append('on hiatus in 2026: confirm whether new output resumes')
    if l['landmark_id']=='russell-brand': need.append('re-check 2026 output volume')
    if l['landmark_id']=='matt-taibbi': need.append('D8 note: America This Week may have ended')
    if l['verification']!='verified' or l['active_2025_2026'] is not True or YOUNG.get(l['landmark_id']):
        q[l['domain']].append(dict(landmark_id=l['landmark_id'],name=l['name'],primary_niche=l['primary_niche'],role=l['role'],
            verification=l['verification'],active_2025_2026=l['active_2025_2026'],checks=need))
held=[dict(landmark_id='androgenic',name='Androgenic',status='HELD OUT of SEED-v1',checks=['age: confirm >= 18 before any inclusion','verify activity and handles'])]
vq=dict(meta=dict(generated='2026-10-31',author_of_record='Benjamin Life (@omniharmonic)',total=sum(len(v) for v in q.values()),
   by_domain={d:len(q[d]) for d in DOM},note='Every SEED-v1 landmark with verification UNVERIFIED or active_2025_2026 not true, plus age checks.'),
   queue={d:q[d] for d in DOM},held_out=held)
json.dump(vq,open(SEED+'/VERIFICATION-QUEUE.json','w'),indent=1,ensure_ascii=False)
print(stats); print('queue',vq['meta']['total'],vq['meta']['by_domain']); print('nobridger',nobridger)
