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
    ROOT / "site-src" / "document-pages.json",
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

SKIP_TOP_LEVEL = {".git", ".github", "assets", "css", "images", "js", "scripts", "site-src"}


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


def page_risks(text: str) -> list[str]:
    return [name for name, pattern in RISK_MARKERS.items() if re.search(pattern, text, re.I)]


def audit_indexes() -> list[tuple[str, str, int, int, str]]:
    migrated = manifest_slugs()
    rows: list[tuple[str, str, int, int, str]] = []
    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        if rel == Path("index.html"):
            continue
        if rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        if len(rel.parts) == 2 and rel.parts[0] in migrated:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        forms = len(re.findall(r"<form\b", text, re.I))
        body_js = body_inline_scripts(text)
        risks = page_risks(text)
        if not re.search(r"<main\b[^>]*>.*?</main>", text, re.I | re.S):
            risks.append("no-main")
        if not re.search(r"<style\b[^>]*>.*?</style>", text, re.I | re.S):
            risks.append("no-style")
        status = "SIMPLE" if not risks else "CUSTOM"
        rows.append((str(rel), status, forms, body_js, ",".join(risks) or "-"))
    return rows


def audit_articles() -> list[tuple[str, str, int, int, str]]:
    rows: list[tuple[str, str, int, int, str]] = []
    articles_dir = ROOT / "stati"
    if not articles_dir.exists():
        return rows
    for path in sorted(articles_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        main = re.search(r"<main\b[^>]*>(.*?)</main>", text, re.I | re.S)
        forms = len(re.findall(r"<form\b", text, re.I))
        body_js = body_inline_scripts(text)
        risks = page_risks(text)
        if not main:
            risks.append("no-main")
            structure = "NO_MAIN"
        elif re.search(r"<h1\b", main.group(1), re.I):
            structure = "H1_IN_MAIN"
        elif re.search(r"<h1\b", text[:main.start()], re.I):
            structure = "H1_BEFORE_MAIN"
        else:
            structure = "NO_H1"
            risks.append("no-h1")
        rows.append((path.name, structure, forms, body_js, ",".join(risks) or "-"))
    return rows


def main() -> None:
    rows = audit_indexes()
    print("path\tstatus\tforms\tbody_js\trisks")
    for row in rows:
        print("\t".join(map(str, row)))
    print(f"Remaining standalone index pages: {len(rows)}")
    if rows:
        raise SystemExit("Unmanaged standalone index pages remain")

    articles = audit_articles()
    print("\narticle\tstructure\tforms\tbody_js\trisks")
    for row in articles:
        print("\t".join(map(str, row)))
    print(f"Standalone article HTML files to classify: {len(articles)}")


if __name__ == "__main__":
    main()
