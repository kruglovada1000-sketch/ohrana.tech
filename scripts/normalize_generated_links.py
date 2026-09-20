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

PRICING_VISUAL_MARKER = 'data-pricing-visual="1"'
PRICING_CSS_MARKER = '/* pricing-hero-visual */'
PRICING_OG_IMAGE = 'https://ohrana.tech/images/ceny-hero.svg'
PRICING_HERO_OLD = '''<section class="price-hero"><div class="wrap" data-reveal><span class="price-kicker">Стоимость услуг</span><h1>Цены на <em>охранные услуги</em></h1><p class="price-lead">Единый каталог ориентировочных тарифов. Выберите тип объекта или услугу. Точный расчёт делаем после уточнения режима, количества постов, площади и задач.</p><div class="price-actions"><a class="btn btn-gold" href="#tariffs">Смотреть тарифы</a><a class="btn btn-line" href="/kontakty/">Получить точный расчёт</a></div></div></section>'''
PRICING_HERO_NEW = '''<section class="price-hero"><div class="wrap price-hero-grid" data-reveal data-pricing-visual="1"><div class="price-hero-copy"><span class="price-kicker">Стоимость услуг</span><h1>Цены на <em>охранные услуги</em></h1><p class="price-lead">Единый каталог ориентировочных тарифов. Выберите тип объекта или услугу. Точный расчёт делаем после уточнения режима, количества постов, площади и задач.</p><div class="price-actions"><a class="btn btn-gold" href="#tariffs">Смотреть тарифы</a><a class="btn btn-line" href="/kontakty/">Получить точный расчёт</a></div></div><figure class="price-hero-visual"><img class="price-hero-bg" src="/images/ceny-hero.svg?v=20260920-brandshield2" alt="Аналитика стоимости охранных услуг" width="1600" height="900" fetchpriority="high" decoding="async"><div class="price-brand-shield"><img src="/images/schit.png" alt="Логотип ЧОО «Рускорпорация»" loading="eager" decoding="async"><svg class="price-brand-spark" viewBox="0 0 120 140" aria-hidden="true"><path class="spark-rail" d="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/><path class="spark-run" d="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/><circle class="spark-head" r="2.2"><animateMotion dur="4.8s" repeatCount="indefinite" path="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/></circle></svg></div></figure></div></section>'''
PRICING_CSS = '''
/* pricing-hero-visual */
.price-hero-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(360px,.95fr);gap:48px;align-items:center}.price-hero-copy{min-width:0}.price-hero-visual{margin:0;position:relative;aspect-ratio:16/9;border-radius:24px;overflow:hidden;border:1px solid rgba(232,200,122,.28);background:#0d1118;box-shadow:0 30px 80px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.025) inset}.price-hero-visual::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(135deg,rgba(245,227,179,.06),transparent 35%,rgba(0,0,0,.08)),radial-gradient(480px 220px at 82% 0%,rgba(232,200,122,.13),transparent 62%)}.price-hero-visual img{display:block;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.96) contrast(1.03)}
@media(max-width:960px){.price-hero-grid{grid-template-columns:1fr;gap:34px}.price-hero-visual{width:min(100%,760px);margin:4px auto 0}.price-lead{max-width:820px}}
@media(max-width:700px){.price-hero-grid{gap:28px}.price-hero-visual{border-radius:18px;aspect-ratio:16/10}.price-hero-visual img{object-fit:cover}}
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


def enhance_pricing_page() -> bool:
    image=ROOT/'images'/'ceny-hero.svg'
    if not image.exists():
        raise RuntimeError(f'Pricing hero image missing: {image}')
    path=ROOT/'ceny'/'index.html'
    if not path.exists():
        raise RuntimeError(f'Pricing page missing before visual enhancement: {path}')
    text=path.read_text(encoding='utf-8')
    original=text
    if PRICING_VISUAL_MARKER not in text:
        if PRICING_HERO_OLD not in text:
            raise RuntimeError('Pricing hero markup changed; refusing blind replacement')
        text=text.replace(PRICING_HERO_OLD,PRICING_HERO_NEW,1)
    if PRICING_OG_IMAGE not in text:
        anchor='<meta property="og:locale" content="ru_RU">'
        og='''<meta property="og:image" content="https://ohrana.tech/images/ceny-hero.svg">\n<meta property="og:image:width" content="1600">\n<meta property="og:image:height" content="900">\n<meta name="twitter:card" content="summary_large_image">'''
        if anchor not in text:
            raise RuntimeError('Pricing OG locale anchor missing')
        text=text.replace(anchor,anchor+'\n'+og,1)
    if text!=original:
        path.write_text(text,encoding='utf-8')
        print('Enhanced pricing hero markup and social preview: ceny/index.html')
        return True
    return False


def enhance_pricing_css() -> bool:
    path=ROOT/'assets'/'css'/'pricing.css'
    if not path.exists():
        raise RuntimeError(f'Pricing CSS missing before visual enhancement: {path}')
    text=path.read_text(encoding='utf-8')
    if PRICING_CSS_MARKER in text:
        return False
    path.write_text(text.rstrip()+"\n"+PRICING_CSS,encoding='utf-8')
    print('Applied pricing hero visual styles: assets/css/pricing.css')
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
    enhance_pricing_page()
    enhance_pricing_css()
    normalize_shared_css()
    print(f'Legacy link replacements: {total}')
    print(f'Legacy resource replacements: {resources}')

if __name__=='__main__': main()
