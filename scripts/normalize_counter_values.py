#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"

TAG_RE = re.compile(
    r"<(?P<tag>[a-zA-Z][\w:-]*)(?P<attrs>[^>]*\bdata-value=(?P<q>[\"'])(?P<value>-?\d+(?:\.\d+)?)(?P=q)[^>]*)>"
    r"(?P<inner>[^<]*)</(?P=tag)>",
    re.I,
)
SUFFIX_RE = re.compile(r"\bdata-suffix=([\"'])(.*?)\1", re.I)


def page_slugs() -> list[str]:
    slugs = ["ohrana-skladov", "ceny"]
    for name in ("object-pages.json", "shared-pages.json", "custom-pages.json"):
        path = SRC / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        slugs.extend(str(item["slug"]) for item in data)
    return list(dict.fromkeys(slugs))


def format_value(raw: str) -> str:
    value = float(raw)
    if value.is_integer():
        return f"{int(value):,}".replace(",", " ")
    return (f"{value:.6f}".rstrip("0").rstrip(".")).replace(".", ",")


def normalize_html(text: str) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        attrs = match.group("attrs")
        suffix_match = SUFFIX_RE.search(attrs)
        suffix = suffix_match.group(2) if suffix_match else ""
        expected = format_value(match.group("value")) + suffix
        if match.group("inner").strip() == expected:
            return match.group(0)
        changed += 1
        return f'<{match.group("tag")}{attrs}>{expected}</{match.group("tag")}>'

    return TAG_RE.sub(repl, text), changed


def main() -> None:
    total = 0
    touched: list[str] = []
    for slug in page_slugs():
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        normalized, count = normalize_html(text)
        if count:
            path.write_text(normalized, encoding="utf-8")
            total += count
            touched.append(str(path.relative_to(ROOT)))

    # Verify every generated data-value element exposes its final value in source HTML.
    for slug in page_slugs():
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in TAG_RE.finditer(text):
            suffix_match = SUFFIX_RE.search(match.group("attrs"))
            suffix = suffix_match.group(2) if suffix_match else ""
            expected = format_value(match.group("value")) + suffix
            if match.group("inner").strip() != expected:
                raise RuntimeError(f"{path}: data-value source text is not final: {match.group(0)!r}")

    print(f"Counter source normalization OK: {total} value(s) updated across {len(touched)} page(s)")
    for item in touched:
        print(f"  {item}")


if __name__ == "__main__":
    main()
