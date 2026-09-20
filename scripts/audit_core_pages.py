#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ("dogovor", ROOT / "dogovor" / "index.html"),
    ("fizicheskaya-ohrana", ROOT / "fizicheskaya-ohrana" / "index.html"),
    ("ohrana-fizicheskih-lic", ROOT / "ohrana-fizicheskih-lic" / "index.html"),
    ("ohrana-yuridicheskih-lic", ROOT / "ohrana-yuridicheskih-lic" / "index.html"),
    ("ohrana-pult", ROOT / "ohrana-pult" / "index.html"),
    ("ohrana-moskovskaya-oblast", ROOT / "ohrana-moskovskaya-oblast" / "index.html"),
    ("kontakty", ROOT / "kontakty" / "index.html"),
    ("stati", ROOT / "stati" / "index.html"),
    ("tehnicheskaya-ohrana", ROOT / "tehnicheskaya-ohrana" / "index.html"),
    ("ohrana-tehniki", ROOT / "ohrana-tehniki" / "index.html"),
]

MARKERS = {
    "form": r"<form\b|formspree\.io|new\s+FormData|fetch\s*\(",
    "canvas": r"<canvas\b|getContext\s*\(",
    "video": r"<video\b|\.play\s*\(|\.pause\s*\(",
    "calculator": r"калькулятор|calculator|total-price|total_price|calc-btn|data-price|rate\s*=|rates\s*=",
    "search_filter": r"type=[\"']search[\"']|\.filter\s*\(|dataset\.category|data-category",
    "counter": r"data-value|data-suffix",
    "flip_cards": r"class=[\"'][^\"']*\bflip\b|classList\.toggle\([\"']flipped",
    "clipboard": r"navigator\.clipboard|execCommand\([\"']copy|id=[\"']copyReq[\"']",
    "scroll_spy": r"tocLinks|\.toc\s+a|doc-body\s+h2\[id\]",
    "marquee": r"marquee|marquee-track",
    "map": r"ymaps|iframe[^>]+map|карта",
}


def inline_body_script_count(text: str) -> int:
    body = re.search(r"<body\b[^>]*>(.*?)</body>", text, re.I | re.S)
    if not body:
        return 0
    return sum(
        1
        for match in re.finditer(r"<script(?P<attrs>[^>]*)>(?P<code>.*?)</script>", body.group(1), re.I | re.S)
        if not re.search(r"\bsrc\s*=", match.group("attrs") or "", re.I)
        and (match.group("code") or "").strip()
    )


def main() -> None:
    print("slug\tstatus\tforms\tbody_js\trisks")
    for slug, path in PAGES:
        if not path.exists():
            print(f"{slug}\tMISSING\t0\t0\tmissing-file")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        forms = len(re.findall(r"<form\b", text, re.I))
        body_js = inline_body_script_count(text)
        risks = [name for name, pattern in MARKERS.items() if re.search(pattern, text, re.I)]
        if not re.search(r"<main\b[^>]*>.*?</main>", text, re.I | re.S):
            risks.append("no-main")
        if not re.search(r"<style\b[^>]*>.*?</style>", text, re.I | re.S):
            risks.append("no-style")
        status = "SIMPLE" if not risks else "CUSTOM"
        print(f"{slug}\t{status}\t{forms}\t{body_js}\t{','.join(risks) or '-'}")


if __name__ == "__main__":
    main()
