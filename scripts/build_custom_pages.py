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
    return pages


def extract_body_inline_scripts(legacy: str, source_path: Path) -> str:
    body = inner(r"<body\b[^>]*>(.*?)</body>", legacy)
    if not body:
        raise RuntimeError(f"No <body> in {source_path}")

    chunks: list[str] = []
    for match in re.finditer(r"<script(?P<attrs>[^>]*)>(?P<code>.*?)</script>", body, re.I | re.S):
        attrs = match.group("attrs") or ""
        code = (match.group("code") or "").strip()
        if re.search(r"\bsrc\s*=", attrs, re.I):
            raise RuntimeError(f"External body script requires explicit migration in {source_path}: {attrs.strip()}")
        if re.search(r"type\s*=\s*[\"']application/ld\+json[\"']", attrs, re.I):
            continue
        if code:
            chunks.append(code)

    if not chunks:
        raise RuntimeError(f"No inline body scripts found in {source_path}")
    return "\n\n/* ---- preserved legacy body script ---- */\n\n".join(chunks) + "\n"


def validate_custom_output(path: Path, slug: str, marker: str) -> None:
    page = path.read_text(encoding="utf-8")
    required = [
        "<title>",
        'rel="canonical"',
        "<h1",
        "application/ld+json",
        'href="/ceny/"',
        f'/assets/js/{slug}.js',
        f'/assets/css/{slug}.css',
        '/assets/css/site-shell.css',
    ]
    missing = [token for token in required if token not in page]
    if missing:
        raise RuntimeError(f"{path}: missing {missing}")
    if len(re.findall(r"<header\b", page, re.I)) != 1:
        raise RuntimeError(f"{path}: expected exactly one header")
    if len(re.findall(r"<main\b", page, re.I)) != 1:
        raise RuntimeError(f"{path}: expected exactly one main")
    if len(re.findall(r"<footer\b", page, re.I)) != 1:
        raise RuntimeError(f"{path}: expected exactly one footer")
    if re.search(r"<style\b", page, re.I):
        raise RuntimeError(f"{path}: inline style remained")
    if "{{site." in page:
        raise RuntimeError(f"{path}: unresolved template variable")
    js = (ROOT / "assets" / "js" / f"{slug}.js").read_text(encoding="utf-8")
    if marker and marker not in js:
        raise RuntimeError(f"{path}: custom JS marker {marker!r} missing")


def build_custom_page(config: dict[str, object]) -> None:
    slug = str(config["slug"])
    source_name = str(config["source"])
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

    organization_jsonld = "" if legacy_defines_organization(page_head) else read_partial("organization-jsonld.html")
    body_script = extract_body_inline_scripts(legacy, source_path)
    marker = str(config.get("script_marker", ""))
    if marker and marker not in body_script:
        raise RuntimeError(f"Custom script marker {marker!r} missing in {source_path}")

    css_path = ROOT / "assets" / "css" / f"{slug}.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(style + "\n", encoding="utf-8")

    js_path = ROOT / "assets" / "js" / f"{slug}.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.write_text(body_script, encoding="utf-8")

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
<script src="/assets/js/{slug}.js" defer></script>
</body>
</html>
'''
    out_path = ROOT / slug / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    validate_custom_output(out_path, slug, marker)
    print(f"Built custom page: /{slug}/; preserved script -> {js_path.relative_to(ROOT)}")


def main() -> None:
    pages = load_manifest()
    for config in pages:
        build_custom_page(config)
    print(f"Custom-page batch complete: {len(pages)} page(s)")


if __name__ == "__main__":
    main()
