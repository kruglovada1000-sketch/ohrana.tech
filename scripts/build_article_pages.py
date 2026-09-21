#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from build_site import ROOT, SRC, SITE, page_head_from_legacy, legacy_defines_organization, read_partial

ARTICLES = ROOT / 'stati'
SNAPSHOTS = SRC / 'articles'
REPORT = SRC / 'article-pages.generated.json'
ARTICLE_JS_SOURCE = SRC / 'assets' / 'article.js'
ARTICLE_JS_PUBLIC = ROOT / 'js' / 'article.js'
ARTICLE_CSS_DIR = ROOT / 'css' / 'articles'
ARTICLE_CUSTOM_JS_DIR = ROOT / 'js' / 'articles'

CUSTOM_PATTERNS = {
    'canvas': re.compile(r'<canvas\b|getContext\s*\(', re.I),
    'calculator': re.compile(r'total-price|total_price|guards-count|hours-count|calc-btn|rates\s*=|function\s+updatePrice|data-target=["\'](?:guards|hours)["\']', re.I),
    'ymaps': re.compile(r'\bymaps\b', re.I),
}

COMPAT_CSS = r'''
/* Compatibility layer: legacy article tokens mapped to homepage Gilded Noir. */
:root{
  --amber:var(--gold);--amber2:var(--gold2);--amber-deep:var(--gold-deep);
  --steel:var(--mut);--disp:var(--serif);--body:var(--sans);
  --txt:#D5D9E2;
}
body{font-family:var(--sans)}
h1,h2,h3,h4{font-family:var(--serif)}
.toc a.active,.article-toc a.active,[data-article-toc] a.active{color:var(--gold2)!important}
'''


def snapshot_name(public_name: str) -> str:
    return public_name[:-5] + '.source.html'


def ensure_snapshots() -> list[Path]:
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    source_paths: list[Path] = []
    for public in sorted(ARTICLES.glob('*.html')):
        if public.name == 'index.html':
            continue
        snapshot = SNAPSHOTS / snapshot_name(public.name)
        if not snapshot.exists():
            shutil.copyfile(public, snapshot)
            print(f'Snapshotted article: {public.name}')
        source_paths.append(snapshot)
    return source_paths


def repair_extra_closing_li(text: str, source: Path) -> tuple[str, bool]:
    opens = len(re.findall(r'<li\b[^>]*>', text, re.I))
    closes = len(re.findall(r'</li\s*>', text, re.I))
    if closes != opens + 1:
        return text, False
    depth = 0
    for match in re.finditer(r'<li\b[^>]*>|</li\s*>', text, re.I):
        token = match.group(0)
        if token.lower().startswith('<li'):
            depth += 1
            continue
        if depth == 0:
            repaired = text[:match.start()] + text[match.end():]
            if len(re.findall(r'<li\b[^>]*>', repaired, re.I)) != len(re.findall(r'</li\s*>', repaired, re.I)):
                raise RuntimeError(f'LI repair failed for {source}')
            print(f'Repaired one stray </li>: {source.name}')
            return repaired, True
        depth -= 1
    raise RuntimeError(f'One extra </li> detected but no stray close found: {source}')


def source_text(source: Path) -> tuple[str, list[str]]:
    text = source.read_text(encoding='utf-8')
    repairs: list[str] = []
    text, repaired = repair_extra_closing_li(text, source)
    if repaired:
        repairs.append('removed-stray-closing-li')
    return text, repairs


def custom_reasons(text: str) -> list[str]:
    return [name for name, pattern in CUSTOM_PATTERNS.items() if pattern.search(text)]


def extract_styles(text: str, source: Path) -> str:
    styles = re.findall(r'<style\b[^>]*>(.*?)</style>', text, re.I | re.S)
    if not styles:
        raise RuntimeError(f'No inline styles in article source: {source}')
    return '\n\n'.join(chunk.strip() for chunk in styles if chunk.strip())


def extract_main(text: str, source: Path) -> str:
    match = re.search(r'<main\b[^>]*>.*?</main>', text, re.I | re.S)
    if match:
        main = match.group(0).strip()
        if not re.search(r'<h1\b', main, re.I):
            raise RuntimeError(f'Article main has no H1: {source}')
        return main
    body_match = re.search(r'<body\b[^>]*>(.*?)</body>', text, re.I | re.S)
    if not body_match:
        raise RuntimeError(f'Article has no body: {source}')
    body = body_match.group(1)
    header_end = re.search(r'</header>', body, re.I)
    footer_start = re.search(r'<footer\b', body, re.I)
    if not header_end or not footer_start or footer_start.start() <= header_end.end():
        raise RuntimeError(f'Cannot isolate article content between header/footer: {source}')
    unique = body[header_end.end():footer_start.start()].strip()
    if not re.search(r'<h1\b', unique, re.I):
        raise RuntimeError(f'Article body slice lost H1: {source}')
    return '<main>\n' + unique + '\n</main>'


def inline_script_codes(text: str) -> list[str]:
    result: list[str] = []
    for match in re.finditer(r'<script(?P<attrs>[^>]*)>(?P<code>.*?)</script>', text, re.I | re.S):
        attrs = match.group('attrs') or ''
        code = (match.group('code') or '').strip()
        if not code or re.search(r'\bsrc\s*=', attrs, re.I) or 'application/ld+json' in attrs.lower():
            continue
        result.append(code)
    return result


def extract_custom_module(text: str, reasons: list[str], source: Path) -> str:
    selected: list[str] = []
    for code in inline_script_codes(text):
        use = False
        if 'canvas' in reasons and re.search(r'getContext\s*\(|radarCanvas', code, re.I): use = True
        if 'calculator' in reasons and re.search(r'total-price|total_price|guards-count|hours-count|rates\s*=|updatePrice', code, re.I): use = True
        if 'ymaps' in reasons and re.search(r'\bymaps\b', code, re.I): use = True
        if use and code not in selected:
            selected.append(code)
    if reasons and not selected:
        raise RuntimeError(f'Custom article markers found but no isolated module could be extracted: {source} ({reasons})')
    return '\n\n'.join(selected)


def build_article(source: Path, text: str, repairs: list[str], reasons: list[str]) -> dict[str, object]:
    public_name = source.name.replace('.source.html', '.html')
    stem = public_name[:-5]
    public = ARTICLES / public_name
    main = extract_main(text, source)
    css = extract_styles(text, source) + '\n' + COMPAT_CSS

    ARTICLE_CSS_DIR.mkdir(parents=True, exist_ok=True)
    css_path = ARTICLE_CSS_DIR / f'{stem}.css'
    css_path.write_text(css + '\n', encoding='utf-8')

    custom_script = ''
    custom_src = ''
    if reasons:
        custom_script = extract_custom_module(text, reasons, source)
        ARTICLE_CUSTOM_JS_DIR.mkdir(parents=True, exist_ok=True)
        module_path = ARTICLE_CUSTOM_JS_DIR / f'{stem}.js'
        module_path.write_text(custom_script + '\n', encoding='utf-8')
        custom_src = f'<script src="/js/articles/{stem}.js" defer></script>'

    head = page_head_from_legacy(text)
    org = '' if legacy_defines_organization(head) else read_partial('organization-jsonld.html')
    out = f'''<!DOCTYPE html>
<html lang="ru" class="no-js">
<head>
{read_partial('head-common.html')}
{head}
{org}
<link rel="stylesheet" href="/css/articles/{stem}.css">
<link rel="stylesheet" href="/css/site-shell.css">
</head>
<body data-metrika-id="{SITE['metrika_id']}">
<div id="progress"></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="cursor-ring" aria-hidden="true"></div>
{read_partial('header.html')}
{main}
{read_partial('footer.html')}
{read_partial('mobile-bar.html')}
{read_partial('chat.html')}
<script src="/js/site.js" defer></script>
<script src="/js/article.js" defer></script>
{custom_src}
</body>
</html>
'''
    public.write_text(out, encoding='utf-8')
    entry: dict[str, object] = {'file': public_name, 'source': source.name, 'css': f'css/articles/{stem}.css', 'repairs': repairs}
    if reasons:
        entry['reasons'] = reasons
        entry['script'] = f'js/articles/{stem}.js'
    return entry


def validate_article(entry: dict[str, object], custom: bool) -> None:
    path = ARTICLES / str(entry['file'])
    html = path.read_text(encoding='utf-8')
    errors: list[str] = []
    for tag in ('h1', 'header', 'main', 'footer'):
        if len(re.findall(rf'<{tag}\b', html, re.I)) != 1: errors.append(f'exactly one <{tag}> required')
    if re.search(r'<style\b', html, re.I): errors.append('inline style remained')
    if 'href="/ceny/"' not in html: errors.append('prices nav missing')
    if '/js/site.js' not in html: errors.append('site.js missing')
    if '/js/article.js' not in html: errors.append('article.js missing')
    if f'/css/articles/{Path(str(entry["file"])).stem}.css' not in html: errors.append('article css missing')
    if custom:
        expected = '/' + str(entry['script'])
        if expected not in html: errors.append('custom article module missing')
        module = ROOT / str(entry['script'])
        if not module.exists() or not module.read_text(encoding='utf-8').strip(): errors.append('custom article module empty')
    if errors:
        raise RuntimeError(f"{entry['file']}: " + '; '.join(errors))


def main() -> None:
    if not ARTICLES.exists(): raise RuntimeError('Missing /stati directory')
    sources = ensure_snapshots()
    ARTICLE_JS_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ARTICLE_JS_SOURCE, ARTICLE_JS_PUBLIC)

    regular: list[dict[str, object]] = []
    custom: list[dict[str, object]] = []
    deferred: list[dict[str, object]] = []
    for source in sources:
        text, repairs = source_text(source)
        reasons = custom_reasons(text)
        public_name = source.name.replace('.source.html', '.html')
        try:
            entry = build_article(source, text, repairs, reasons)
        except RuntimeError as exc:
            if reasons:
                deferred.append({'file': public_name, 'source': source.name, 'reasons': reasons, 'repairs': repairs, 'error': str(exc)})
                print(f'Deferred custom article: {public_name} ({exc})')
                continue
            raise
        validate_article(entry, bool(reasons))
        if reasons:
            custom.append(entry); print(f'Built custom article: /stati/{public_name} ({", ".join(reasons)})')
        else:
            regular.append(entry); print(f'Built article: /stati/{public_name}')

    report = {'regular': regular, 'custom': custom, 'deferred': deferred, 'total': len(sources)}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Article batch: {len(regular)} regular, {len(custom)} custom, {len(deferred)} deferred, {len(sources)} total')


if __name__ == '__main__':
    main()
