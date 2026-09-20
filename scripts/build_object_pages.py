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


def build_regular_or_pre_main(page: dict[str, object]) -> None:
    slug = str(page["slug"])
    source = str(page["source"])
    hero_class = str(page.get("pre_main_header_class") or "").strip()
    if not hero_class:
        build_legacy_page(slug, source)
        return

    source_path = SRC / "pages" / source
    legacy = source_path.read_text(encoding="utf-8")
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
        build_regular_or_pre_main(page)
        validate_html(ROOT / slug / "index.html")
        print(f"Built and validated: /{slug}/")
    print(f"Regular shared-page batch complete: {len(pages)} pages")


if __name__ == "__main__":
    main()
