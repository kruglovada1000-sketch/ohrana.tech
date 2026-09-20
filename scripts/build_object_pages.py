#!/usr/bin/env python3
from __future__ import annotations

import json

from build_site import ROOT, SRC, build_legacy_page, validate_html


def load_manifest() -> list[dict[str, str]]:
    path = SRC / "object-pages.json"
    pages = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("object-pages.json must contain a non-empty list")

    seen: set[str] = set()
    for page in pages:
        slug = page.get("slug", "")
        source = page.get("source", "")
        if not slug or not source:
            raise RuntimeError(f"Invalid object page entry: {page}")
        if slug in seen:
            raise RuntimeError(f"Duplicate object page slug: {slug}")
        seen.add(slug)
        source_path = SRC / "pages" / source
        if not source_path.exists():
            raise RuntimeError(f"Missing object page source: {source_path}")
    return pages


def main() -> None:
    pages = load_manifest()
    for page in pages:
        slug = page["slug"]
        source = page["source"]
        build_legacy_page(slug, source)
        validate_html(ROOT / slug / "index.html")
        print(f"Built and validated: /{slug}/")
    print(f"Object batch complete: {len(pages)} pages")


if __name__ == "__main__":
    main()
