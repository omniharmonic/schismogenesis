import json,glob,re,unicodedata,collections,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from decisions import *
import gapfill, hygiene, annotate
SEED='/home/claude/dialogos-arena/seed'
def kebab(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    s=re.sub(r'\(.*?\)','',s).lower()
    s=re.sub(r'\b(fr|rev|bishop|dr|sj)\b\.?','',s)
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def lid_of(name):
    k=kebab(name); return ALIAS.get(k,k)
LF={'high':3,'medium':2,'low':1}; RR={'core':3,'bridger':2,'edge':1}
WARN=[]
raw=[]
for f in sorted(glob.glob(SEED+'/raw/*.json')):
    for n in json.load(open(f)): raw.append(n)
# ---- structural validation
REQ=['niche_id','name','aliases','domain','description','telos','sacred_values','existential_threats','combatants','adjacent_niches','sub_niches','size_estimate','cultural_influence','trajectory','atlas_match','limberg_barnes_match','landmarks','sources','notes']
LREQ=['name','role','why','platforms','longform_output','active_2025_2026','verification','sources']
struct=[]
for n in raw:
    for k in REQ:
        if k not in n: struct.append(f"{n.get('niche_id')}: missing {k}")
    for l in n['landmarks']:
        for k in LREQ:
            if k not in l: struct.append(f"{n['niche_id']}/{l.get('name')}: missing {k}")
        if l['role'] not in RR: struct.append(f"{l['name']}: bad role {l['role']}")
        if l['longform_output'] not in LF: struct.append(f"{l['name']}: bad longform {l['longform_output']}")
        if l['verification'] not in ('verified','UNVERIFIED'): struct.append(f"{l['name']}: bad verification")
        if not isinstance(l['platforms'],dict): struct.append(f"{l['name']}: platforms not dict")
rawby={n['niche_id']:n for n in raw}
# ---- niches
niches={}
for n in raw:
    t=NICHE_MERGE.get(n['niche_id'],n['niche_id'])
    if t not in niches:
        if t in MERGED_META:
            base,name,dom,cross,dec=MERGED_META[t]; b=rawby[base]
            niches[t]=dict(niche_id=t,name=name,domain=dom,cross_domains=list(cross),aliases=[],description=b['description'],telos=b['telos'],
              sacred_values=list(b['sacred_values']),existential_threats=list(b['existential_threats']),combatants=[],adjacent_niches=[],sub_niches=[],
              size_estimate=b['size_estimate'],cultural_influence=b['cultural_influence'],trajectory=b['trajectory'],atlas_match=None,
              limberg_barnes_match=b['limberg_barnes_match'],sources=[],notes='',merged_from=[],qa_decision=dec)
        else:
            niches[t]=dict(niche_id=t,name=n['name'],domain=n['domain'],cross_domains=[],aliases=[],description=n['description'],telos=n['telos'],
              sacred_values=list(n['sacred_values']),existential_threats=list(n['existential_threats']),combatants=[],adjacent_niches=[],sub_niches=[],
              size_estimate=n['size_estimate'],cultural_influence=n['cultural_influence'],trajectory=n['trajectory'],atlas_match=None,
              limberg_barnes_match=n['limberg_barnes_match'],sources=[],notes='',merged_from=[],qa_decision=None)
    N=niches[t]; N['merged_from'].append(n['niche_id'])
    if n['domain']!=N['domain'] and n['domain'] not in N['cross_domains']: N['cross_domains'].append(n['domain'])
    def addu(key,vals):
        for v in vals:
            if v and v not in N[key]: N[key].append(v)
    addu('aliases',n['aliases']+([n['name']] if n['name']!=N['name'] else []))
    addu('combatants',n['combatants']); addu('adjacent_niches',n['adjacent_niches']); addu('sub_niches',n['sub_niches'])
    if t in MERGED_META and n['niche_id']!=MERGED_META[t][0]:
        addu('sacred_values',n['sacred_values'][:2]); addu('sub_niches',[n['name']+' (merged niche)'])
    addu('sources',n['sources'])
    if n['notes']: N['notes']+=('' if not N['notes'] else ' | ')+f"[{n['niche_id']}] "+n['notes']
# ---- landmarks
occ=collections.defaultdict(list)
for n in raw:
    t=NICHE_MERGE.get(n['niche_id'],n['niche_id'])
    for l in n['landmarks']:
        occ[lid_of(l['name'])].append((t,n['domain'],l))
lms={}
dropped={}
for lid,os_ in occ.items():
    if lid in DROP: dropped[lid]=(os_[0][2]['name'],[o[0] for o in os_],DROP[lid]); continue
    targets=[]
    for o in os_:
        if o[0] not in targets: targets.append(o[0])
    if lid in PRIMARY: prim=PRIMARY[lid]
    else:
        prim=targets[0]
        if len(targets)>1: WARN.append(f'no primary decision for {lid}: {targets}')
    if prim not in niches: WARN.append(f'{lid}: primary {prim} unknown')
    po=[o for o in os_ if o[0]==prim] or os_
    best=max(po,key=lambda o:RR[o[2]['role']])[2]
    plat={}
    for o in os_:
        for k,v in o[2]['platforms'].items():
            if v and not plat.get(k): plat[k]=v
    srcs=[]
    for o in os_:
        for s in o[2]['sources']:
            if s not in srcs: srcs.append(s)
    act=[o[2]['active_2025_2026'] for o in os_]
    lms[lid]=dict(landmark_id=lid,name=DISPLAY_NAME.get(lid,best['name']),primary_niche=prim,
        secondary_niches=[t for t in targets if t!=prim]+[x for x in EXTRA_SECONDARY.get(lid,[]) if x not in targets],
        role=ROLE_OVERRIDE.get(lid,best['role']),why=best['why'],platforms=plat,
        longform_output=max((o[2]['longform_output'] for o in os_),key=lambda x:LF[x]),
        active_2025_2026=True if True in act else (None if None in act else False),
        verification='verified' if any(o[2]['verification']=='verified' for o in os_) else 'UNVERIFIED',
        sources=srcs,source_domains=sorted({o[1] for o in os_}))
# ---- gap fills
for nn in gapfill.NEW_NICHES: niches[nn['niche_id']]=nn
for l in gapfill.NEW_LANDMARKS: lms[l['landmark_id']]=l
# ---- hygiene & claim fixes
hlog=hygiene.apply(niches,lms)
# ---- annotate
annotate.apply(niches,lms)
# secondary niches must exist
for l in lms.values():
    l['secondary_niches']=[s for s in dict.fromkeys(l['secondary_niches']) if s in niches and s!=l['primary_niche']]
# ---- link niches
for N in niches.values():
    ls=[l for l in lms.values() if l['primary_niche']==N['niche_id']]
    ls.sort(key=lambda l:(-RR[l['role']],-LF[l['longform_output']],l['verification']!='verified'))
    N['landmarks']=[l['landmark_id'] for l in ls]
    N['secondary_landmarks']=[l['landmark_id'] for l in lms.values() if N['niche_id'] in l['secondary_niches']]
    if len(ls)<2: WARN.append(f"THIN {N['niche_id']}: {len(ls)}")
    if len(ls)>5: WARN.append(f"OVER {N['niche_id']}: {len(ls)} {[l['landmark_id'] for l in ls]}")
    if not any(l['role']=='core' for l in ls): WARN.append(f"NOCORE {N['niche_id']}")
json.dump(dict(niches=niches,lms=lms,dropped=dropped,trimmed=getattr(annotate.apply,'trimmed',{}),struct=struct,warn=WARN,hlog=hlog),open(SEED+'/scripts/_state.json','w'),indent=1,default=str)
print('niches',len(niches),'landmarks',len(lms),'dropped',len(dropped),'struct',len(struct))
for w in WARN: print('WARN',w)
for s in struct[:20]: print('STRUCT',s)
