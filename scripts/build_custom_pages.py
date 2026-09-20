#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from build_site import (
    ROOT,
    SRC,
    SITE,
    first,
    inner,
    legacy_defines_organization,
    page_head_from_legacy,
    read_partial,
)


def load_manifest() -> list[dict[str, object]]:
    path = SRC / "custom-pages.json"
    pages = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("custom-pages.json must contain a non-empty list")
    seen: set[str] = set()
    for page in pages:
        slug = str(page.get("slug", ""))
        source = str(page.get("source", ""))
        script_source = str(page.get("script_source", ""))
        if not slug or not source or not script_source:
            raise RuntimeError(f"Invalid custom page entry: {page}")
        if slug in seen:
            raise RuntimeError(f"Duplicate custom page slug: {slug}")
        seen.add(slug)
        if not (SRC / "pages" / source).exists():
            raise RuntimeError(f"Missing custom page source: {source}")
        if not (SRC / "custom-js" / script_source).exists():
            raise RuntimeError(f"Missing custom JS source: {script_source}")
    return pages


def validate_custom_output(path: Path, slug: str, marker: str) -> None:
    page = path.read_text(encoding="utf-8")
    required = [
        "<title>",
        'rel="canonical"',
        "<h1",
        "application/ld+json",
        'href="/ceny/"',
        '/assets/js/site.js',
        f'/assets/js/{slug}.js',
        f'/assets/css/{slug}.css',
        '/assets/css/site-shell.css',
    ]
    missing = [token for token in required if token not in page]
    if missing:
        raise RuntimeError(f"{path}: missing {missing}")
    for tag in ("header", "main", "footer"):
        if len(re.findall(fr"<{tag}\b", page, re.I)) != 1:
            raise RuntimeError(f"{path}: expected exactly one {tag}")
    if re.search(r"<style\b", page, re.I):
        raise RuntimeError(f"{path}: inline style remained")
    if "{{site." in page:
        raise RuntimeError(f"{path}: unresolved template variable")
    if page.index('/assets/js/site.js') > page.index(f'/assets/js/{slug}.js'):
        raise RuntimeError(f"{path}: shared site.js must load before custom module")
    js = (ROOT / "assets" / "js" / f"{slug}.js").read_text(encoding="utf-8")
    if marker and marker not in js:
        raise RuntimeError(f"{path}: custom JS marker {marker!r} missing")


def build_custom_page(config: dict[str, object]) -> None:
    slug = str(config["slug"])
    source_name = str(config["source"])
    script_source = str(config["script_source"])
    script_version = str(config.get("script_version", "")).strip()
    custom_script_src = f"/assets/js/{slug}.js" + (f"?v={script_version}" if script_version else "")
    source_path = SRC / "pages" / source_name
    legacy = source_path.read_text(encoding="utf-8")

    main = first(r"<main\b[^>]*>.*?</main>", legacy)
    if not main:
        raise RuntimeError(f"No <main> in {source_path}")

    style = inner(r"<style[^>]*>(.*?)</style>", legacy)
    if not style:
        raise RuntimeError(f"No <style> in {source_path}")

    page_head = page_head_from_legacy(legacy)
    replacements = config.get("url_replacements", {})
    if not isinstance(replacements, dict):
        raise RuntimeError(f"url_replacements must be an object for {slug}")
    for old, new in replacements.items():
        page_head = page_head.replace(str(old), str(new))
        main = main.replace(str(old), str(new))

    organization_jsonld = "" if legacy_defines_organization(page_head) else read_partial("organization-jsonld.html")
    marker = str(config.get("script_marker", ""))
    custom_js = (SRC / "custom-js" / script_source).read_text(encoding="utf-8")
    if marker and marker not in custom_js:
        raise RuntimeError(f"Custom script marker {marker!r} missing in {script_source}")
    if marker and marker not in main:
        raise RuntimeError(f"Custom HTML marker {marker!r} missing in {source_path}")

    css_path = ROOT / "assets" / "css" / f"{slug}.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(style + "\n", encoding="utf-8")

    js_path = ROOT / "assets" / "js" / f"{slug}.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.write_text(custom_js.rstrip() + "\n", encoding="utf-8")

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
<script src="{custom_script_src}" defer></script>
</body>
</html>
'''
    out_path = ROOT / slug / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    validate_custom_output(out_path, slug, marker)
    print(f"Built custom page: /{slug}/; module -> {js_path.relative_to(ROOT)}")


def main() -> None:
    pages = load_manifest()
    for config in pages:
        build_custom_page(config)
    print(f"Custom-page batch complete: {len(pages)} page(s)")


if __name__ == "__main__":
    main()
