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


def main() -> None:
    total=0
    for path in generated_pages():
        if not path.exists(): raise RuntimeError(f'Generated page missing before link normalization: {path}')
        text=path.read_text(encoding='utf-8');original=text
        for old,new in ALIASES.items():
            count=text.count(old)
            if count: text=text.replace(old,new);total+=count
        if text!=original:
            path.write_text(text,encoding='utf-8');print(f'Normalized legacy links: {path.relative_to(ROOT)}')
    print(f'Legacy link replacements: {total}')

if __name__=='__main__': main()
