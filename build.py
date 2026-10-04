import json, html
P=json.load(open('pubs.json'))
def ini(g):
    parts=[p for p in g.replace('.',' ').replace('-',' -').split() if p]
    return ''.join((p[0] if not p.startswith('-') else '-'+p[1])+'.' for p in parts)
def authors(au):
    names=[]
    for f,g in au:
        n=f"{html.escape(f)}, {ini(g)}"
        if f=='Liu' and g.startswith('Dunyu') or (f=='Liu' and g in('D.','D')): n=f"<b>{n}</b>"
        names.append(n)
    if len(names)>12:
        mine=[n for n in names if '<b>' in n]
        return ', '.join(names[:8])+', … '+(mine[0]+', … ' if mine and mine[0] not in names[:8] else '')+f"& {names[-1]}"
    return ', '.join(names[:-1])+(' &amp; ' if len(names)>1 else '')+names[-1]
JFIX={'Journal of Geophysical Research: Solid Earth':'Journal of Geophysical Research: Solid Earth','Research Square':'Research Square (preprint)'}
PREV={'10.31223/X5R50Z':'EarthArXiv (preprint)','10.31223/X5D20T':'EarthArXiv (preprint)','10.22541/essoar.15005894/v1':'ESS Open Archive (preprint)','10.21203/rs.3.rs-10910110/v1':'Research Square (preprint)'}
items=[]
for p in P:
    au=p['authors']
    # Crossref sometimes gives 'Dunyu' variants; mark by family+given
    venue=PREV.get(p['doi']) or p['journal']
    vol=f", {p['vol']}" if p['vol'] else ''
    pg=f", {p['page']}" if p['page'] else ''
    items.append((p['year'],p['kind'],f'<li><span class="au">{authors(au)}</span> ({p["year"]}). {html.escape(p["title"])}. <i>{html.escape(venue)}</i>{vol}{pg}. <a href="https://doi.org/{p["doi"]}">doi:{p["doi"]}</a></li>'))
items.sort(key=lambda x:(-x[0]))
arts=[i for i in items if i[1]=='art']; pres=[i for i in items if i[1]=='pre']
out=[]
yrs=sorted({i[0] for i in arts},reverse=True)
for y in yrs:
    out.append(f'<h3 class="yr">{y}</h3><ol class="pubs">'+''.join(i[2] for i in arts if i[0]==y)+'</ol>')
pre_html='<ol class="pubs">'+''.join(i[2] for i in pres)+'</ol>'
t=open('template.html').read()
t=t.replace('{{ARTICLES}}','\n'.join(out)).replace('{{PREPRINTS}}',pre_html).replace('{{NART}}',str(len(arts))).replace('{{NPRE}}',str(len(pres)))
head='<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
open('index.html','w').write(head+t+'\n</html>\n')
print(len(arts),len(pres))
