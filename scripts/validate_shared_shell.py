#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"


def object_slugs() -> list[str]:
    manifest = json.loads((SRC / "object-pages.json").read_text(encoding="utf-8"))
    return ["ohrana-skladov"] + [page["slug"] for page in manifest]


def main() -> None:
    errors: list[str] = []
    for slug in object_slugs():
        path = ROOT / slug / "index.html"
        css = ROOT / "assets" / "css" / f"{slug}.css"
        if not path.exists():
            errors.append(f"{slug}: generated HTML missing")
            continue
        if not css.exists():
            errors.append(f"{slug}: page CSS missing")
            continue
        text = path.read_text(encoding="utf-8")
        page_css = f'/assets/css/{slug}.css'
        shell_css = '/assets/css/site-shell.css'
        if page_css not in text:
            errors.append(f"{slug}: page CSS link missing")
        if shell_css not in text:
            errors.append(f"{slug}: shared shell CSS link missing")
        if page_css in text and shell_css in text and text.index(page_css) > text.index(shell_css):
            errors.append(f"{slug}: shared shell must load after page CSS")
        if '/assets/js/site.js' not in text:
            errors.append(f"{slug}: shared JS missing")
        if 'href="/ceny/"' not in text:
            errors.append(f"{slug}: prices navigation item missing")
        if re.search(r'<style\b', text, re.I):
            errors.append(f"{slug}: inline style remained")
        if '{{site.' in text:
            errors.append(f"{slug}: unresolved template variable")
        for tag in ('header', 'main', 'footer'):
            if len(re.findall(fr'<{tag}\b', text, re.I)) != 1:
                errors.append(f"{slug}: expected exactly one <{tag}>")

    prices = ROOT / "ceny" / "index.html"
    if not prices.exists():
        errors.append("ceny: generated HTML missing")
    else:
        text = prices.read_text(encoding="utf-8")
        if '/assets/css/pricing.css' not in text or '/assets/css/site-shell.css' not in text:
            errors.append("ceny: expected pricing + shared shell CSS")
        if text.index('/assets/css/pricing.css') > text.index('/assets/css/site-shell.css'):
            errors.append("ceny: shared shell must load after pricing CSS")
        if 'href="/ceny/"' not in text:
            errors.append("ceny: prices navigation item missing")

    if errors:
        raise SystemExit("Shared shell validation failed:\n - " + "\n - ".join(errors))
    print(f"Shared shell OK: {len(object_slugs())} object pages + /ceny/")


if __name__ == "__main__":
    main()
