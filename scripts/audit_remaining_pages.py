#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

MANIFESTS = [
    ROOT / "site-src" / "object-pages.json",
    ROOT / "site-src" / "shared-pages.json",
    ROOT / "site-src" / "custom-pages.json",
]

RISK_MARKERS = {
    "form": r"<form\b|formspree\.io|new\s+FormData|fetch\s*\(",
    "canvas": r"<canvas\b|getContext\s*\(",
    "video": r"<video\b|\.play\s*\(|\.pause\s*\(",
    "calculator": r"калькулятор|calculator|total-price|total_price|calc-btn|data-price|rate\s*=|rates\s*=",
    "search_filter": r"type=[\"']search[\"']|\.filter\s*\(|dataset\.category|data-category|artSearch",
    "counter": r"data-value|data-suffix",
    "flip_cards": r"class=[\"'][^\"']*\bflip\b|classList\.toggle\([\"']flipped",
    "clipboard": r"navigator\.clipboard|execCommand\([\"']copy|copyReq",
    "scroll_spy": r"tocLinks|\.toc\s+a|doc-body\s+h2\[id\]",
    "map": r"ymaps|<iframe[^>]+map|карта",
}

SKIP_TOP_LEVEL = {
    ".git",
    ".github",
    "assets",
    "css",
    "images",
    "js",
    "scripts",
    "site-src",
}


def manifest_slugs() -> set[str]:
    result = {"ohrana-skladov", "ceny"}
    for path in MANIFESTS:
        if not path.exists():
            continue
        pages = json.loads(path.read_text(encoding="utf-8"))
        result.update(page["slug"] for page in pages)
    return result


def body_inline_scripts(text: str) -> int:
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
    migrated = manifest_slugs()
    rows: list[tuple[str, str, int, int, str]] = []

    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        if rel == Path("index.html"):
            continue  # homepage is the visual reference, not a migration candidate
        if rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        if len(rel.parts) == 2 and rel.parts[0] in migrated:
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        forms = len(re.findall(r"<form\b", text, re.I))
        body_js = body_inline_scripts(text)
        risks = [name for name, pattern in RISK_MARKERS.items() if re.search(pattern, text, re.I)]
        if not re.search(r"<main\b[^>]*>.*?</main>", text, re.I | re.S):
            risks.append("no-main")
        if not re.search(r"<style\b[^>]*>.*?</style>", text, re.I | re.S):
            risks.append("no-style")
        status = "SIMPLE" if not risks else "CUSTOM"
        rows.append((str(rel), status, forms, body_js, ",".join(risks) or "-"))

    print("path\tstatus\tforms\tbody_js\trisks")
    for row in rows:
        print("\t".join(map(str, row)))
    print(f"Remaining standalone index pages: {len(rows)}")


if __name__ == "__main__":
    main()
