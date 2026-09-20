from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

ROOT=Path('.')
SKIP_DIRS={'.git','site-src','scripts','.github'}
html_files=[p for p in ROOT.rglob('*.html') if not any(part in SKIP_DIRS for part in p.parts) and not (p.parts and p.parts[0]=='images')]
issues=[]
refs=[]

class P(HTMLParser):
    def __init__(self,path): super().__init__(convert_charrefs=True); self.path=path
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for attr in ('href','src','poster'):
            v=a.get(attr)
            if v: refs.append((self.path,tag,attr,v))
        if tag=='source' and a.get('src'): refs.append((self.path,tag,'src',a['src']))

for f in html_files:
    try: P(f).feed(f.read_text(encoding='utf-8'))
    except Exception as e: issues.append(('ERROR',str(f),f'HTML parse/read: {e}'))

def local_target(page,value):
    if value.startswith(('#','mailto:','tel:','javascript:','data:')): return None
    u=urlsplit(value)
    if u.scheme or u.netloc: return None
    path=unquote(u.path)
    if not path: return None
    if path.startswith('/'):
        rel=Path(path.lstrip('/'))
    else:
        rel=page.parent/path
    # Normalize without requiring existence.
    rel=Path(str(rel).replace('\\','/'))
    return rel

def exists_web(rel):
    if rel.exists(): return True
    s=str(rel)
    if s.endswith('/') and (rel/'index.html').exists(): return True
    if not rel.suffix and (rel/'index.html').exists(): return True
    return False

for page,tag,attr,value in refs:
    t=local_target(page,value)
    if t is None: continue
    if not exists_web(t): issues.append(('ERROR',str(page),f'broken {attr}={value!r} -> {t}'))

# CSS local url() references.
for css in ROOT.rglob('*.css'):
    if any(part in SKIP_DIRS for part in css.parts): continue
    text=css.read_text(encoding='utf-8',errors='replace')
    for raw in re.findall(r'url\(([^)]+)\)',text,re.I):
        v=raw.strip().strip('"\'')
        if v.startswith(('data:','http://','https://','#')): continue
        u=urlsplit(v); path=unquote(u.path)
        if not path: continue
        t=Path(path.lstrip('/')) if path.startswith('/') else css.parent/path
        if not t.exists(): issues.append(('ERROR',str(css),f'broken css url({v}) -> {t}'))

# Zero-byte public resources (exclude intentionally empty text-like files).
for p in ROOT.rglob('*'):
    if not p.is_file() or any(part in SKIP_DIRS for part in p.parts): continue
    if p.stat().st_size==0 and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.gif','.svg','.mp4','.webm','.pdf','.js','.css'}:
        issues.append(('WARN',str(p),'zero-byte public resource'))

# Suspicious duplicate/noncanonical published HTML files.
for p in html_files:
    if p.name!='index.html' and p.parent.name not in {'stati'} and 'google' not in p.name.lower() and 'yandex' not in p.name.lower():
        issues.append(('WARN',str(p),'nonstandard published HTML filename'))

errors=[x for x in issues if x[0]=='ERROR']; warns=[x for x in issues if x[0]=='WARN']
print(f'STATIC_AUDIT html={len(html_files)} refs={len(refs)} errors={len(errors)} warnings={len(warns)}')
for row in issues: print(' | '.join(row))
