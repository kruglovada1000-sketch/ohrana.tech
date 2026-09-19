#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"

SITE = json.loads((SRC / "site.json").read_text(encoding="utf-8"))


def render(text: str) -> str:
    for key, value in SITE.items():
        text = text.replace("{{site.%s}}" % key, str(value))
    return text


def read_partial(name: str) -> str:
    return render((SRC / "partials" / name).read_text(encoding="utf-8"))


def first(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return m.group(0).strip() if m else ""


def inner(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""


def page_head_from_legacy(html: str) -> str:
    chunks = []
    for pattern in [
        r"<title>.*?</title>",
        r"<meta\s+name=[\"']description[\"'][^>]*>",
        r"<meta\s+name=[\"']keywords[\"'][^>]*>",
        r"<link\s+rel=[\"']canonical[\"'][^>]*>",
        r"<meta\s+property=[\"']og:[^\"']+[\"'][^>]*>",
    ]:
        chunks.extend(re.findall(pattern, html, re.I | re.S))
    chunks.extend(re.findall(r"<script\s+type=[\"']application/ld\+json[\"']>.*?</script>", html, re.I | re.S))
    return "\n".join(x.strip() for x in chunks if x.strip())


def build_legacy_page(slug: str, source_name: str) -> None:
    source_path = SRC / "pages" / source_name
    html = source_path.read_text(encoding="utf-8")
    main = first(r"<main\b[^>]*>.*?</main>", html)
    if not main:
        raise RuntimeError(f"No <main> in {source_path}")

    style = inner(r"<style[^>]*>(.*?)</style>", html)
    if not style:
        raise RuntimeError(f"No <style> in {source_path}")

    css_path = ROOT / "assets" / "css" / f"{slug}.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(style + "\n", encoding="utf-8")

    head_common = read_partial("head-common.html")
    organization = read_partial("organization-jsonld.html")
    header = read_partial("header.html")
    footer = read_partial("footer.html")
    mobile = read_partial("mobile-bar.html")
    chat = read_partial("chat.html")
    page_head = page_head_from_legacy(html)

    out = f'''<!DOCTYPE html>
<html lang="ru" class="no-js">
<head>
{head_common}
{page_head}
{organization}
<link rel="stylesheet" href="/assets/css/site-shell.css">
<link rel="stylesheet" href="/assets/css/{slug}.css">
</head>
<body data-metrika-id="{SITE['metrika_id']}">
<div id="progress"></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="cursor-ring" aria-hidden="true"></div>
{header}
{main}
{footer}
{mobile}
{chat}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    out_path = ROOT / slug / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")


def validate_html(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    required = ["<title>", "rel=\"canonical\"", "<h1", "application/ld+json", "/assets/js/site.js"]
    missing = [token for token in required if token not in html]
    if missing:
        raise RuntimeError(f"{path}: missing {missing}")


def main() -> None:
    # First migrated commercial page. Add other legacy snapshots here after review.
    build_legacy_page("ohrana-skladov", "ohrana-skladov.source.html")
    validate_html(ROOT / "ohrana-skladov" / "index.html")
    validate_html(ROOT / "ceny" / "index.html")
    print("Built: /ohrana-skladov/; validated: /ceny/")


if __name__ == "__main__":
    main()
