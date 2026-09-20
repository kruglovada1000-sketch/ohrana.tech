#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'site-src'
ALIASES = {
    '/ohrana-stroyaploshchadok/': '/ohrana-stroitelnyh-obektov/',
    '/ohrana-uvelirnyh-magazinov/': '/ohrana-yuvelirnyh-magazinov/',
}
RESOURCE_REPLACEMENTS = {
    'src="schit.jpg"': 'src="/images/schit.jpg"',
    "src='schit.jpg'": "src='/images/schit.jpg'",
    'src="/ohrana-moskovskaya-oblast/schit.jpg"': 'src="/images/schit.jpg"',
    "src='/ohrana-moskovskaya-oblast/schit.jpg'": "src='/images/schit.jpg'",
}

RESPONSIVE_FIX_MARKER = '/* browser-qa-responsive-fixes */'
RESPONSIVE_FIXES = '''
/* browser-qa-responsive-fixes */
/* Keep wide price tables inside the mobile viewport. Their own content remains
   horizontally scrollable instead of widening the entire document. */
@media(max-width:768px){
  main .price-table{
    display:block!important;
    width:100%!important;
    max-width:100%!important;
    overflow-x:auto!important;
    -webkit-overflow-scrolling:touch;
  }
}
/* Two legacy expert articles use a 12-column .crit7 grid. The generic tablet
   rule has lower specificity, so explicitly collapse that grid here. */
@media(max-width:960px){
  main .cards-grid.crit7{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
  }
  main .cards-grid.crit7 .sign-card,
  main .cards-grid.crit7 .sign-card:nth-child(n+4){
    grid-column:auto!important;
  }
}
@media(max-width:640px){
  main .cards-grid.crit7{
    grid-template-columns:1fr!important;
  }
}
'''


def load_manifest(name: str) -> list[dict[str, object]]:
    path=SRC/name
    if not path.exists(): return []
    value=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value,list): raise RuntimeError(f'{name} must contain a list')
    return value


def article_built_pages() -> list[Path]:
    report=SRC/'article-pages.generated.json'
    if not report.exists(): return []
    value=json.loads(report.read_text(encoding='utf-8'))
    items=list(value.get('regular',[]))+list(value.get('custom',[]))
    return [ROOT/'stati'/item['file'] for item in items]


def generated_pages() -> list[Path]:
    paths=[ROOT/'ohrana-skladov'/'index.html',ROOT/'ceny'/'index.html']
    for manifest_name in ('object-pages.json','shared-pages.json','custom-pages.json'):
        paths.extend(ROOT/str(page['slug'])/'index.html' for page in load_manifest(manifest_name))
    paths.extend(article_built_pages())
    unique=[];seen=set()
    for path in paths:
        if path not in seen: seen.add(path);unique.append(path)
    return unique


def normalize_shared_css() -> bool:
    path=ROOT/'assets'/'css'/'site-shell.css'
    if not path.exists():
        raise RuntimeError(f'Shared CSS missing before responsive normalization: {path}')
    text=path.read_text(encoding='utf-8')
    if RESPONSIVE_FIX_MARKER in text:
        return False
    path.write_text(text.rstrip()+"\n"+RESPONSIVE_FIXES,encoding='utf-8')
    print('Applied browser-QA responsive guards: assets/css/site-shell.css')
    return True


def main() -> None:
    total=0
    resources=0
    for path in generated_pages():
        if not path.exists(): raise RuntimeError(f'Generated page missing before link normalization: {path}')
        text=path.read_text(encoding='utf-8');original=text
        for old,new in ALIASES.items():
            count=text.count(old)
            if count: text=text.replace(old,new);total+=count
        for old,new in RESOURCE_REPLACEMENTS.items():
            count=text.count(old)
            if count: text=text.replace(old,new);resources+=count
        if text!=original:
            path.write_text(text,encoding='utf-8');print(f'Normalized generated links/resources: {path.relative_to(ROOT)}')
    normalize_shared_css()
    print(f'Legacy link replacements: {total}')
    print(f'Legacy resource replacements: {resources}')

if __name__=='__main__': main()
