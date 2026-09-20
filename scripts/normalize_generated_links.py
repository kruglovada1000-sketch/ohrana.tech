#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"
ALIASES = {
    "/ohrana-stroyaploshchadok/": "/ohrana-stroitelnyh-obektov/",
    "/ohrana-uvelirnyh-magazinov/": "/ohrana-yuvelirnyh-magazinov/",
}


def generated_pages() -> list[Path]:
    manifest = json.loads((SRC / "object-pages.json").read_text(encoding="utf-8"))
    paths = [ROOT / "ohrana-skladov" / "index.html", ROOT / "ceny" / "index.html"]
    paths.extend(ROOT / page["slug"] / "index.html" for page in manifest)
    return paths


def main() -> None:
    total = 0
    for path in generated_pages():
        if not path.exists():
            raise RuntimeError(f"Generated page missing before link normalization: {path}")
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in ALIASES.items():
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                total += count
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"Normalized legacy links: {path.relative_to(ROOT)}")
    print(f"Legacy link replacements: {total}")


if __name__ == "__main__":
    main()
