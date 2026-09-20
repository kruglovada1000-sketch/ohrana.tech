#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "ohrana-skladov" / "index.html", ROOT / "ceny" / "index.html"]
ALIASES = {
    "/ohrana-stroyaploshchadok/": "/ohrana-stroitelnyh-obektov/",
    "/ohrana-uvelirnyh-magazinov/": "/ohrana-yuvelirnyh-magazinov/",
}


def main() -> None:
    total = 0
    for path in PAGES:
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
