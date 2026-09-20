#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "site-src" / "pages"
SLUGS = [
    "ohrana-ofisov",
    "ohrana-biznes-centrov",
    "ohrana-torgovyh-centrov",
    "ohrana-magazinov",
    "ohrana-yuvelirnyh-magazinov",
    "ohrana-restoranov",
    "ohrana-gostinic",
    "ohrana-skladov",
    "ohrana-predpriyatij",
    "ohrana-stroitelnyh-obektov",
    "ohrana-avtosalonov",
    "ohrana-parkovok",
    "ohrana-domov-i-kottedzhey",
    "ohrana-zhilyh-kompleksov",
    "ohrana-shkol",
    "ohrana-meropriyatiy",
]

RISK_MARKERS = {
    "form": r"<form\b|leadForm|formspree|fetch\s*\(",
    "canvas": r"<canvas\b|getContext\s*\(",
    "video": r"<video\b|\.play\s*\(",
    "calculator": r"калькулятор|calculator|calc[A-Z_]|total_price|tariff",
    "custom_data": r"data-value|data-suffix",
}


def source_for(slug: str) -> tuple[Path, str]:
    snapshot = SOURCE_DIR / f"{slug}.source.html"
    if snapshot.exists():
        return snapshot, "snapshot"
    return ROOT / slug / "index.html", "live"


def main() -> None:
    print("slug\tclass\tsource\tforms\tscripts\trisks")
    simple = []
    custom = []
    for slug in SLUGS:
        path, source_kind = source_for(slug)
        if not path.exists():
            print(f"{slug}\tMISSING\t{source_kind}\t0\t0\tmissing-file")
            custom.append(slug)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        forms = len(re.findall(r"<form\b", text, re.I))
        scripts = len(re.findall(r"<script\b", text, re.I))
        risks = [name for name, pattern in RISK_MARKERS.items() if re.search(pattern, text, re.I)]
        has_main = bool(re.search(r"<main\b[^>]*>.*?</main>", text, re.I | re.S))
        has_style = bool(re.search(r"<style\b[^>]*>.*?</style>", text, re.I | re.S))
        if not has_main:
            risks.append("no-main")
        if not has_style:
            risks.append("no-style")
        cls = "SIMPLE" if not risks else "CUSTOM"
        (simple if cls == "SIMPLE" else custom).append(slug)
        print(f"{slug}\t{cls}\t{source_kind}\t{forms}\t{scripts}\t{','.join(risks) or '-'}")
    print("\nSimple batch candidates:", ", ".join(simple) or "none")
    print("Custom-logic pages:", ", ".join(custom) or "none")


if __name__ == "__main__":
    main()
