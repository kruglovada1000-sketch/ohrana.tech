#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"
SITE = json.loads((SRC / "site.json").read_text(encoding="utf-8"))
PRICING = json.loads((SRC / "pricing.json").read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html_lib.escape(str(value), quote=True)


def render(text: str) -> str:
    for key, value in SITE.items():
        text = text.replace("{{site.%s}}" % key, str(value))
    return text


def read_partial(name: str) -> str:
    return render((SRC / "partials" / name).read_text(encoding="utf-8"))


def first(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    match = re.search(pattern, text, flags)
    return match.group(0).strip() if match else ""


def inner(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else ""


def page_head_from_legacy(page: str) -> str:
    chunks: list[str] = []
    patterns = [
        r"<title>.*?</title>",
        r"<meta\s+name=[\"']description[\"'][^>]*>",
        r"<meta\s+name=[\"']keywords[\"'][^>]*>",
        r"<link\s+rel=[\"']canonical[\"'][^>]*>",
        r"<meta\s+property=[\"']og:[^\"']+[\"'][^>]*>",
    ]
    for pattern in patterns:
        chunks.extend(re.findall(pattern, page, re.I | re.S))
    chunks.extend(re.findall(r"<script\s+type=[\"']application/ld\+json[\"']>.*?</script>", page, re.I | re.S))
    return "\n".join(item.strip() for item in chunks if item.strip())


def legacy_defines_organization(page_head: str) -> bool:
    organization_id = f"{SITE['site_url']}/#organization"
    scripts = re.findall(
        r"<script\s+type=[\"']application/ld\+json[\"']>(.*?)</script>",
        page_head,
        re.I | re.S,
    )
    organization_type = re.compile(
        r'"@type"\s*:\s*(?:"Organization"|\[[^\]]*"Organization"[^\]]*\])',
        re.I | re.S,
    )
    return any(organization_id in script and organization_type.search(script) for script in scripts)


def publish_shared_assets() -> None:
    pairs = [
        (SRC / "assets" / "site-shell.css", ROOT / "assets" / "css" / "site-shell.css"),
        (SRC / "assets" / "pricing.css", ROOT / "assets" / "css" / "pricing.css"),
        (SRC / "assets" / "site.js", ROOT / "assets" / "js" / "site.js"),
    ]
    for source, target in pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        # Fix an early draft typo in the embedded grain SVG if an old checkout still contains it.
        text = text.replace("</filter id='n'>", "</filter>")
        target.write_text(text, encoding="utf-8")


def build_legacy_page(slug: str, source_name: str) -> None:
    source_path = SRC / "pages" / source_name
    legacy = source_path.read_text(encoding="utf-8")
    main = first(r"<main\b[^>]*>.*?</main>", legacy)
    if not main:
        raise RuntimeError(f"No <main> in {source_path}")

    style = inner(r"<style[^>]*>(.*?)</style>", legacy)
    if not style:
        raise RuntimeError(f"No <style> in {source_path}")

    css_path = ROOT / "assets" / "css" / f"{slug}.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(style + "\n", encoding="utf-8")

    page_head = page_head_from_legacy(legacy)
    organization_jsonld = "" if legacy_defines_organization(page_head) else read_partial("organization-jsonld.html")

    out = f'''<!DOCTYPE html>
<html lang="ru" class="no-js">
<head>
{read_partial("head-common.html")}
{page_head}
{organization_jsonld}
<link rel="stylesheet" href="/assets/css/{slug}.css">
<link rel="stylesheet" href="/assets/css/site-shell.css">
</head>
<body data-metrika-id="{SITE['metrika_id']}">
<div id="progress"></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="cursor-ring" aria-hidden="true"></div>
{read_partial("header.html")}
{main}
{read_partial("footer.html")}
{read_partial("mobile-bar.html")}
{read_partial("chat.html")}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    out_path = ROOT / slug / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")


def money(value: int | None, unit: str | None) -> str:
    if value is None:
        return "Индивидуальный расчёт"
    formatted = f"{value:,}".replace(",", " ")
    return f"от {formatted} ₽/{esc(unit or '')}"


def absolute_url(url: str) -> str:
    return SITE["site_url"].rstrip("/") + url


def pricing_jsonld() -> str:
    offers = []
    for item in PRICING["services"]:
        offers.append({
            "@type": "Offer",
            "name": item["name"],
            "url": absolute_url(item["url"]),
            "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "minPrice": str(item["price_from"]),
                "priceCurrency": PRICING["currency"],
                "unitText": item["unit"],
            },
        })
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{SITE['site_url']}/ceny/#webpage",
                "url": f"{SITE['site_url']}/ceny/",
                "name": "Цены на услуги ЧОП в Москве",
                "description": "Единый каталог ориентировочных цен на охранные услуги и типы объектов.",
                "about": {"@id": f"{SITE['site_url']}/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE['site_url']}/"},
                    {"@type": "ListItem", "position": 2, "name": "Цены", "item": f"{SITE['site_url']}/ceny/"},
                ],
            },
            {"@type": "OfferCatalog", "name": "Цены на охранные услуги", "itemListElement": offers},
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def build_prices_page() -> None:
    service_by_id = {item["id"]: item for item in PRICING["services"]}
    object_rows: list[str] = []
    for item in PRICING["objects"]:
        service_names = ", ".join(service_by_id[sid]["name"] for sid in item["recommended"])
        object_rows.append(
            f'''<tr data-price-row>
<td><strong>{esc(item['name'])}</strong></td>
<td>{esc(service_names)}</td>
<td><span class="price-value">{money(item.get('display_from'), item.get('display_unit'))}</span></td>
<td>{esc(item['note'])}</td>
<td><a class="price-link" href="{esc(item['url'])}">Подробнее →</a></td>
</tr>'''
        )

    cards: list[str] = []
    for item in PRICING["services"]:
        cards.append(
            f'''<article class="service-price-card" data-reveal>
<h3>{esc(item['name'])}</h3>
<div class="big">{money(item['price_from'], item['unit'])}</div>
<p>{esc(item['note'])}</p>
<a class="price-link" href="{esc(item['url'])}">Об услуге →</a>
</article>'''
        )

    title = "Цены на услуги ЧОП в Москве — стоимость охраны объектов | ЧОО «Рускорпорация»"
    description = "Цены на физическую и пультовую охрану, охрану мероприятий, личную охрану и сопровождение грузов. Подбор стоимости по типу объекта."
    out = f'''<!DOCTYPE html>
<html lang="ru" class="no-js">
<head>
{read_partial("head-common.html")}
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE['site_url']}/ceny/">
<meta property="og:title" content="Цены на охранные услуги | ЧОО «Рускорпорация»">
<meta property="og:description" content="Единый каталог ориентировочных цен на охрану объектов, мероприятия и сопровождение грузов.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE['site_url']}/ceny/">
<meta property="og:locale" content="ru_RU">
{read_partial("organization-jsonld.html")}
<script type="application/ld+json">{pricing_jsonld()}</script>
<link rel="stylesheet" href="/assets/css/pricing.css?v=20260920-mobilecards1">
<link rel="stylesheet" href="/assets/css/site-shell.css">
</head>
<body data-metrika-id="{SITE['metrika_id']}">
<div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>
{read_partial("header.html")}
<main>
<div class="wrap"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Цены</b></nav></div>
<section class="price-hero"><div class="wrap" data-reveal><span class="price-kicker">Стоимость услуг</span><h1>Цены на <em>охранные услуги</em></h1><p class="price-lead">Единый каталог ориентировочных тарифов. Выберите тип объекта или услугу. Точный расчёт делаем после уточнения режима, количества постов, площади и задач.</p><div class="price-actions"><a class="btn btn-gold" href="#objects">Подобрать по объекту</a><a class="btn btn-line" href="/kontakty/">Получить точный расчёт</a></div></div></section>
<section class="price-section alt" id="objects"><div class="wrap"><div class="price-head" data-reveal><span class="eyebrow">По типу объекта</span><h2>Найдите свой <em>объект</em></h2><p>Все варианты находятся в HTML страницы: фильтр нужен только для удобства пользователя и не скрывает каталог от поисковых и AI-роботов.</p></div><div class="price-tools"><input id="priceFilter" type="search" placeholder="Например: склад, магазин, ЖК, мероприятие" aria-label="Поиск по каталогу цен"></div><div class="price-table-wrap" data-reveal><table class="price-table"><thead><tr><th>Объект</th><th>Рекомендуемые услуги</th><th>Ориентир</th><th>Что влияет на цену</th><th>Страница</th></tr></thead><tbody>{''.join(object_rows)}</tbody></table></div><p class="price-note">{esc(PRICING['disclaimer'])}</p></div></section>
<section class="price-section"><div class="wrap"><div class="price-head" data-reveal><span class="eyebrow">По услуге</span><h2>Базовые <em>тарифы</em></h2><p>Тарифы собраны из действующих коммерческих страниц проекта и теперь управляются централизованно.</p></div><div class="service-cards">{''.join(cards)}</div></div></section>
<section class="price-section alt"><div class="wrap"><div class="price-head" data-reveal><span class="eyebrow">Расчёт</span><h2>Что меняет <em>итоговую стоимость</em></h2></div><div class="factors"><div class="factor" data-reveal><b>Режим</b><span>24/7, дневная, ночная или разовая охрана.</span></div><div class="factor" data-reveal><b>Объект</b><span>Площадь, периметр, входы, КПП и поток людей.</span></div><div class="factor" data-reveal><b>Состав</b><span>Количество сотрудников, разряд, вооружение и ГБР.</span></div><div class="factor" data-reveal><b>Техника</b><span>Сигнализация, камеры, СКУД и другие системы безопасности.</span></div></div></div></section>
<section class="price-cta"><div class="wrap"><div class="price-cta-box" data-reveal><h2>Нужен точный расчёт?</h2><p>Сообщите тип объекта, адрес и режим работы. Подберём схему охраны и рассчитаем стоимость под конкретные задачи.</p><a class="btn btn-gold" href="/kontakty/">Рассчитать охрану</a></div></div></section>
</main>
{read_partial("footer.html")}
{read_partial("mobile-bar.html")}
{read_partial("chat.html")}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    path = ROOT / "ceny" / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")


def internal_path(url: str) -> Path | None:
    if not url.startswith("/") or url.startswith("//"):
        return None
    clean = url.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None
    relative = clean.lstrip("/")
    if not relative:
        return ROOT / "index.html"
    candidate = ROOT / relative
    if clean.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def validate_pricing_registry() -> None:
    service_ids = [item["id"] for item in PRICING["services"]]
    if len(service_ids) != len(set(service_ids)):
        raise RuntimeError("pricing.json: duplicate service ids")
    valid_ids = set(service_ids)
    urls: set[str] = set()
    for service in PRICING["services"]:
        urls.add(service["url"])
    for obj in PRICING["objects"]:
        unknown = [sid for sid in obj["recommended"] if sid not in valid_ids]
        if unknown:
            raise RuntimeError(f"pricing.json: {obj['name']} references unknown services {unknown}")
        urls.add(obj["url"])
    missing = []
    for url in sorted(urls):
        path = internal_path(url)
        if path is not None and not path.exists():
            missing.append(url)
    if missing:
        raise RuntimeError(f"pricing.json: missing internal targets: {missing}")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    loc = f"{SITE['site_url']}/ceny/"
    if loc in text:
        return
    block = f'''<url>
<loc>{loc}</loc>
<lastmod>2026-09-20</lastmod>
<changefreq>monthly</changefreq>
<priority>0.9</priority>
</url>
'''
    text = text.replace("</urlset>", block + "</urlset>")
    path.write_text(text, encoding="utf-8")


def validate_html(path: Path) -> None:
    page = path.read_text(encoding="utf-8")
    required = ["<title>", 'rel="canonical"', "<h1", "application/ld+json", "/assets/js/site.js", 'href="/ceny/"']
    missing = [token for token in required if token not in page]
    if missing:
        raise RuntimeError(f"{path}: missing {missing}")
    checks = {
        "title": len(re.findall(r"<title\b", page, re.I)),
        "canonical": len(re.findall(r"<link\s+rel=[\"']canonical[\"']", page, re.I)),
        "header": len(re.findall(r"<header\b", page, re.I)),
        "main": len(re.findall(r"<main\b", page, re.I)),
        "footer": len(re.findall(r"<footer\b", page, re.I)),
    }
    bad = {name: count for name, count in checks.items() if count != 1}
    if bad:
        raise RuntimeError(f"{path}: expected one of each structural tag, got {bad}")
    if re.search(r"<style\b", page, re.I):
        raise RuntimeError(f"{path}: inline <style> remained after build")
    if "{{site." in page:
        raise RuntimeError(f"{path}: unresolved site template variable")


def main() -> None:
    validate_pricing_registry()
    publish_shared_assets()
    build_legacy_page("ohrana-skladov", "ohrana-skladov.source.html")
    build_prices_page()
    update_sitemap()
    validate_html(ROOT / "ohrana-skladov" / "index.html")
    validate_html(ROOT / "ceny" / "index.html")
    print("Built and validated: /ohrana-skladov/, /ceny/; shared assets and sitemap updated")


if __name__ == "__main__":
    main()
