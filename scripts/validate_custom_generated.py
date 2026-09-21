#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_generated_html import ROOT, inspect

SRC = ROOT / "site-src"


def main() -> None:
    pages = json.loads((SRC / "custom-pages.json").read_text(encoding="utf-8"))
    for config in pages:
        slug = str(config["slug"])
        marker = str(config.get("script_marker", ""))
        page = ROOT / slug / "index.html"
        js = ROOT / "js" / f"{slug}.js"
        css = ROOT / "css" / f"{slug}.css"

        inspect(page)
        if not js.exists():
            raise SystemExit(f"Missing custom JS: {js.relative_to(ROOT)}")
        if not css.exists():
            raise SystemExit(f"Missing custom CSS: {css.relative_to(ROOT)}")

        html = page.read_text(encoding="utf-8")
        script = js.read_text(encoding="utf-8")
        if marker:
            if marker not in html:
                raise SystemExit(f"{slug}: marker {marker!r} missing from HTML")
            if marker not in script:
                raise SystemExit(f"{slug}: marker {marker!r} missing from custom JS")
        if '/js/site.js' not in html:
            raise SystemExit(f"{slug}: shared site.js missing")
        if f'/js/{slug}.js' not in html:
            raise SystemExit(f"{slug}: custom JS reference missing")
        if html.index('/js/site.js') > html.index(f'/js/{slug}.js'):
            raise SystemExit(f"{slug}: shared site.js must load before custom module")
        if 'href="/ceny/"' not in html:
            raise SystemExit(f"{slug}: prices navigation item missing")

        print(f"Custom integrity OK: /{slug}/; marker={marker or '-'}")

    print(f"Validated custom batch: {len(pages)} page(s)")


if __name__ == "__main__":
    main()
