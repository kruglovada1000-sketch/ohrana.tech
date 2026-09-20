#!/usr/bin/env python3
from __future__ import annotations

import json

from build_site import ROOT, SRC, build_legacy_page, validate_html

MANIFESTS = ("object-pages.json", "shared-pages.json")


def load_manifest(name: str) -> list[dict[str, str]]:
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
        seen.add(slug)
        source_path = SRC / "pages" / source
        if not source_path.exists():
            raise RuntimeError(f"Missing page source: {source_path}")
    return pages


def main() -> None:
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for name in MANIFESTS:
        for page in load_manifest(name):
            slug = page["slug"]
            if slug in seen:
                raise RuntimeError(f"Duplicate regular page slug across manifests: {slug}")
            seen.add(slug)
            pages.append(page)

    if not pages:
        raise RuntimeError("No regular pages configured")

    for page in pages:
        slug = page["slug"]
        source = page["source"]
        build_legacy_page(slug, source)
        validate_html(ROOT / slug / "index.html")
        print(f"Built and validated: /{slug}/")
    print(f"Regular shared-page batch complete: {len(pages)} pages")


if __name__ == "__main__":
    main()
