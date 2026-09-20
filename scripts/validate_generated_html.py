#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'site-src'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
BALANCED={'html','head','body','header','nav','main','footer','section','div','table','thead','tbody','tr','th','td','article','figure','figcaption','ul','ol','li','button','a','script'}
ORGANIZATION_ID='https://ohrana.tech/#organization'

def load_manifest(name):
    p=SRC/name
    if not p.exists(): return []
    v=json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(v,list): raise RuntimeError(f'{name} must contain a list')
    return v

def article_built_pages():
    p=SRC/'article-pages.generated.json'
    if not p.exists(): return []
    v=json.loads(p.read_text(encoding='utf-8')); items=list(v.get('regular',[]))+list(v.get('custom',[]))
    return [ROOT/'stati'/x['file'] for x in items]

def pages_to_validate():
    paths=[ROOT/'ohrana-skladov'/'index.html']
    for n in ('object-pages.json','shared-pages.json'): paths.extend(ROOT/str(x['slug'])/'index.html' for x in load_manifest(n))
    paths.append(ROOT/'ceny'/'index.html'); paths.extend(article_built_pages())
    out=[];seen=set()
    for p in paths:
        if p not in seen: seen.add(p);out.append(p)
    return out

def local_target(href):
    if not href.startswith('/') or href.startswith('//'): return None
    path=urlsplit(href).path
    if not path or path=='/': return ROOT/'index.html'
    target=ROOT/path.lstrip('/')
    if path.endswith('/'): target=target/'index.html'
    return target

def organization_declarations(value):
    if isinstance(value,dict):
        t=value.get('@type'); types=t if isinstance(t,list) else [t]
        own=1 if value.get('@id')==ORGANIZATION_ID and 'Organization' in types else 0
        return own+sum(organization_declarations(c) for c in value.values())
    if isinstance(value,list): return sum(organization_declarations(c) for c in value)
    return 0

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.ids=[];self.links=[];self.count_open={t:0 for t in BALANCED};self.count_close={t:0 for t in BALANCED};self.in_jsonld=False;self.jsonld_chunks=[];self.current_jsonld=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower();a=dict(attrs)
        if tag in BALANCED and tag not in VOID:self.count_open[tag]+=1
        if a.get('id'):self.ids.append(a['id'])
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='script' and (a.get('type') or '').lower()=='application/ld+json':self.in_jsonld=True;self.current_jsonld=[]
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag in BALANCED and tag not in VOID:self.count_close[tag]+=1
        if tag=='script' and self.in_jsonld:self.jsonld_chunks.append(''.join(self.current_jsonld).strip());self.current_jsonld=[];self.in_jsonld=False
    def handle_data(self,data):
        if self.in_jsonld:self.current_jsonld.append(data)

def inspect(path):
    if not path.exists():raise SystemExit(f'Missing generated page: {path.relative_to(ROOT)}')
    text=path.read_text(encoding='utf-8'); p=Inspector();p.feed(text);p.close();errors=[]
    dup=sorted({x for x in p.ids if p.ids.count(x)>1})
    if dup:errors.append(f'duplicate ids: {dup}')
    for tag in sorted(BALANCED):
        if p.count_open[tag]!=p.count_close[tag]:errors.append(f'<{tag}> balance {p.count_open[tag]}/{p.count_close[tag]}')
    if not p.jsonld_chunks:errors.append('no JSON-LD')
    org=0
    for i,raw in enumerate(p.jsonld_chunks,1):
        try:org+=organization_declarations(json.loads(raw))
        except json.JSONDecodeError as exc:errors.append(f'JSON-LD #{i}: {exc}')
    if org!=1:errors.append(f'expected exactly one Organization declaration for {ORGANIZATION_ID}, got {org}')
    missing=[]
    for href in p.links:
        if href.startswith(('#','mailto:','tel:','javascript:')):continue
        t=local_target(href)
        if t is not None and not t.exists():missing.append(href)
    if missing:errors.append('missing internal links: '+', '.join(sorted(set(missing))))
    if len(re.findall(r'<h1\b',text,re.I))!=1:errors.append('expected exactly one H1')
    if len(re.findall(r'<header\b',text,re.I))!=1:errors.append('expected exactly one header')
    if len(re.findall(r'<main\b',text,re.I))!=1:errors.append('expected exactly one main')
    if len(re.findall(r'<footer\b',text,re.I))!=1:errors.append('expected exactly one footer')
    if re.search(r'<style\b',text,re.I):errors.append('inline style block remained in generated HTML')
    if 'href="/ceny/"' not in text:errors.append('shared Prices navigation link missing')
    if '{{site.' in text:errors.append('unresolved shared template variable')
    if errors:raise SystemExit(f"{path.relative_to(ROOT)} failed integrity check:\n - "+'\n - '.join(errors))
    print(f'HTML integrity OK: {path.relative_to(ROOT)}; {len(p.links)} links, {len(p.ids)} ids, {len(p.jsonld_chunks)} JSON-LD blocks, Organization declarations={org}')

def main():
    pages=pages_to_validate()
    for p in pages:inspect(p)
    print(f'Validated generated HTML batch: {len(pages)} pages')
if __name__=='__main__':main()
