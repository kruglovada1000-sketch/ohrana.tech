#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"
ARTICLE_REPORT = SRC / "article-pages.generated.json"

MANIFESTS = [
    SRC / "object-pages.json",
    SRC / "shared-pages.json",
    SRC / "custom-pages.json",
    SRC / "document-pages.json",
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

# Source/build-only trees that are not public website documents.
SKIP_TOP_LEVEL = {".git", ".github", "assets", "images", "js", "scripts", "site-src"}

# Public HTML files that are intentionally not normal site pages.
ROOT_TECHNICAL_HTML = {
    Path("googlebdc13c089db9258c.html"),
    Path("yandex_7c7144a04a571dab.html"),
}
LEGACY_REDIRECTS = {
    Path("css/index.html"): {
        "canonical": "https://ohrana.tech/ohrana-ofisov/",
        "target": "/ohrana-ofisov/",
    }
}


def load_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_slugs() -> set[str]:
    result = {"ohrana-skladov", "ceny"}
    for path in MANIFESTS:
        pages = load_json(path, [])
        if not isinstance(pages, list):
            raise SystemExit(f"Invalid manifest: {path.relative_to(ROOT)}")
        result.update(str(page["slug"]) for page in pages)
    return result


def article_report() -> dict[str, object]:
    value = load_json(ARTICLE_REPORT, {})
    if not isinstance(value, dict):
        raise SystemExit("Invalid article-pages.generated.json")
    return value


def managed_article_files() -> set[str]:
    report = article_report()
    names: set[str] = set()
    for key in ("regular", "custom", "deferred"):
        rows = report.get(key, [])
        if not isinstance(rows, list):
            raise SystemExit(f"Invalid article report section: {key}")
        names.update(str(row["file"]) for row in rows)
    return names


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


def validate_legacy_redirects() -> None:
    for rel, rule in LEGACY_REDIRECTS.items():
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Managed legacy redirect missing: {rel}")
        text = path.read_text(encoding="utf-8", errors="replace")
        required = [
            '<meta name="robots" content="noindex,follow">',
            f'<link rel="canonical" href="{rule["canonical"]}">',
            f'url={rule["target"]}',
            f"location.replace('{rule['target']}')",
        ]
        missing = [marker for marker in required if marker not in text]
        if missing:
            raise SystemExit(f"Legacy redirect {rel} is incomplete: {missing}")
        print(f"Managed legacy redirect OK: {rel} -> {rule['target']}")


def audit_indexes() -> list[tuple[str, str, int, int, str]]:
    migrated = manifest_slugs()
    rows: list[tuple[str, str, int, int, str]] = []
    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        if rel == Path("index.html"):
            continue
        if rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        if rel in LEGACY_REDIRECTS:
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


def audit_public_html_inventory() -> None:
    actual: set[Path] = set()
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        actual.add(rel)

    managed: set[Path] = {Path("index.html")} | ROOT_TECHNICAL_HTML | set(LEGACY_REDIRECTS)
    managed.update(Path(slug) / "index.html" for slug in manifest_slugs())
    managed.update(Path("stati") / name for name in managed_article_files())

    unmanaged = sorted(actual - managed)
    missing = sorted(path for path in managed if not (ROOT / path).exists())
    if unmanaged:
        raise SystemExit("Unmanaged public HTML remains: " + ", ".join(map(str, unmanaged)))
    if missing:
        raise SystemExit("Managed public HTML missing: " + ", ".join(map(str, missing)))

    report = article_report()
    deferred = report.get("deferred", [])
    if deferred:
        raise SystemExit("Deferred articles remain: " + ", ".join(str(row.get("file")) for row in deferred))

    article_actual = {path.name for path in (ROOT / "stati").glob("*.html") if path.name != "index.html"}
    article_managed = managed_article_files()
    if article_actual != article_managed:
        only_actual = sorted(article_actual - article_managed)
        only_report = sorted(article_managed - article_actual)
        raise SystemExit(f"Article inventory mismatch; unmanaged={only_actual}, missing={only_report}")

    print(
        f"Public HTML inventory OK: {len(actual)} files; "
        f"{len(article_managed)} managed articles; 0 unmanaged; 0 deferred"
    )


def main() -> None:
    validate_legacy_redirects()

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
    print(f"Managed standalone article HTML files: {len(articles)}")

    audit_public_html_inventory()


if __name__ == "__main__":
    main()
