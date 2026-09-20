#!/usr/bin/env python3
from __future__ import annotations

import json
import re

from build_site import ROOT, SRC, build_legacy_page, validate_html

MANIFESTS = ("object-pages.json", "shared-pages.json")


def load_manifest(name: str) -> list[dict[str, object]]:
    path = SRC / name
    if not path.exists():
        return []
    pages = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pages, list):
        raise RuntimeError(f"{name} must contain a list")

    seen: set[str] = set()
    for page in pages:
        slug = page.get("slug", "")
        source = page.get("source", "")
        if not slug or not source:
            raise RuntimeError(f"Invalid page entry in {name}: {page}")
        if slug in seen:
            raise RuntimeError(f"Duplicate page slug in {name}: {slug}")
        seen.add(str(slug))
        source_path = SRC / "pages" / str(source)
        if not source_path.exists():
            raise RuntimeError(f"Missing page source: {source_path}")
    return pages


def append_gilded_legacy_aliases(slug: str) -> None:
    css_path = ROOT / "assets" / "css" / f"{slug}.css"
    css = css_path.read_text(encoding="utf-8")
    css += """
/* Shared Gilded Noir compatibility for legacy amber templates. */
:root{
  --amber:var(--gold);--amber2:var(--gold2);--amber-deep:var(--gold-deep);
  --disp:var(--serif);--body:var(--sans);--steel:var(--mut);
}
body{font-family:var(--sans)}
h1,h2,h3{font-family:var(--serif)}
"""
    css_path.write_text(css, encoding="utf-8")


def build_regular_variant(page: dict[str, object]) -> None:
    slug = str(page["slug"])
    source = str(page["source"])
    source_path = SRC / "pages" / source
    legacy = source_path.read_text(encoding="utf-8")

    hero_class = str(page.get("pre_main_header_class") or "").strip()
    body_between = bool(page.get("body_between_header_footer"))

    if hero_class and body_between:
        raise RuntimeError(f"Conflicting page transform modes: {slug}")
    if not hero_class and not body_between:
        build_legacy_page(slug, source)
    elif hero_class:
        hero_pattern = re.compile(
            rf'<header\b[^>]*class=["\'][^"\']*\b{re.escape(hero_class)}\b[^"\']*["\'][^>]*>.*?</header>',
            re.I | re.S,
        )
        main_pattern = re.compile(r'<main\b[^>]*>(.*?)</main>', re.I | re.S)
        hero_match = hero_pattern.search(legacy)
        main_match = main_pattern.search(legacy)
        if not hero_match:
            raise RuntimeError(f"Missing pre-main header class {hero_class!r}: {source_path}")
        if not main_match:
            raise RuntimeError(f"Missing <main> for pre-main page: {source_path}")

        hero = hero_match.group(0).strip()
        hero = re.sub(r'^<header\b', '<section', hero, count=1, flags=re.I)
        hero = re.sub(r'</header>\s*$', '</section>', hero, count=1, flags=re.I)
        main_inner = main_match.group(1).strip()
        without_hero = legacy[:hero_match.start()] + legacy[hero_match.end():]
        transformed = main_pattern.sub(f"<main>\n{hero}\n{main_inner}\n</main>", without_hero, count=1)

        temp_name = f".__build-{slug}.source.html"
        temp_path = SRC / "pages" / temp_name
        temp_path.write_text(transformed, encoding="utf-8")
        try:
            build_legacy_page(slug, temp_name)
        finally:
            temp_path.unlink(missing_ok=True)
    else:
        head_match = re.search(r'<!DOCTYPE html>.*?</head>', legacy, re.I | re.S)
        body_match = re.search(r'<body\b[^>]*>(.*?)</body>', legacy, re.I | re.S)
        if not head_match or not body_match:
            raise RuntimeError(f"Missing head/body for body-slice page: {source_path}")
        body = body_match.group(1)
        header_end = re.search(r'</header>', body, re.I)
        footer_start = re.search(r'<footer\b', body, re.I)
        if not header_end or not footer_start or footer_start.start() <= header_end.end():
            raise RuntimeError(f"Cannot isolate unique body between header/footer: {source_path}")
        unique = body[header_end.end():footer_start.start()].strip()
        if '<h1' not in unique.lower():
            raise RuntimeError(f"Body slice lost H1: {source_path}")
        transformed = f"{head_match.group(0)}\n<body>\n<main>\n{unique}\n</main>\n</body>\n</html>\n"
        temp_name = f".__build-{slug}.source.html"
        temp_path = SRC / "pages" / temp_name
        temp_path.write_text(transformed, encoding="utf-8")
        try:
            build_legacy_page(slug, temp_name)
        finally:
            temp_path.unlink(missing_ok=True)

    if page.get("gilded_legacy_aliases"):
        append_gilded_legacy_aliases(slug)


def main() -> None:
    pages: list[dict[str, object]] = []
    seen: set[str] = set()
    for name in MANIFESTS:
        for page in load_manifest(name):
            slug = str(page["slug"])
            if slug in seen:
                raise RuntimeError(f"Duplicate regular page slug across manifests: {slug}")
            seen.add(slug)
            pages.append(page)

    if not pages:
        raise RuntimeError("No regular pages configured")

    for page in pages:
        slug = str(page["slug"])
        build_regular_variant(page)
        validate_html(ROOT / slug / "index.html")
        print(f"Built and validated: /{slug}/")
    print(f"Regular shared-page batch complete: {len(pages)} pages")


if __name__ == "__main__":
    main()
