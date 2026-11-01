import json,glob,collections,re,unicodedata
R='/home/claude/dialogos-arena/seed/raw'
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    s=re.sub(r'\(.*?\)','',s).lower()
    s=re.sub(r'\b(fr|rev|bishop|dr|sj)\b\.?','',s)
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
occ=collections.defaultdict(list)
for f in sorted(glob.glob(R+'/*.json')):
    for n in json.load(open(f)):
        for l in n['landmarks']:
            occ[norm(l['name'])].append((n['niche_id'],l['role'],l['name']))
d={k:v for k,v in occ.items() if len(v)>1}
print(len(occ),'unique;',len(d),'dupes')
for k,v in sorted(d.items()): print(k, [x[0]+':'+x[1] for x in v])
