import json,glob,collections,sys,os
R='/home/claude/dialogos-arena/seed/raw'
vals=collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(R+'/*.json')):
    for n in json.load(open(f)):
        print(f"## {n['niche_id']} | {n['name']} | {n['domain']} | {n['size_estimate'][:20]}")
        for l in n['landmarks']:
            for k in ('role','longform_output','active_2025_2026','verification'):
                vals[k][repr(l[k])]+=1
            print(f"   - {l['name']} [{l['role']},{l['longform_output']},{l['active_2025_2026']},{l['verification']}]")
for k,v in vals.items(): print(k,dict(v))
