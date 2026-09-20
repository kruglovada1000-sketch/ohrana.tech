#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "ohrana-skladov" / "index.html", ROOT / "ceny" / "index.html"]
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
BALANCED = {"html","head","body","header","nav","main","footer","section","div","table","thead","tbody","tr","th","td","article","figure","figcaption","ul","ol","li","button","a","script"}


def local_target(href: str) -> Path | None:
    if not href.startswith("/") or href.startswith("//"):
        return None
    path = urlsplit(href).path
    if not path or path == "/":
        return ROOT / "index.html"
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    return target


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.count_open = {tag: 0 for tag in BALANCED}
        self.count_close = {tag: 0 for tag in BALANCED}
        self.in_jsonld = False
        self.jsonld_chunks: list[str] = []
        self.current_jsonld: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr = dict(attrs)
        if tag in BALANCED and tag not in VOID:
            self.count_open[tag] += 1
        if "id" in attr and attr["id"]:
            self.ids.append(attr["id"] or "")
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"] or "")
        if tag == "script" and (attr.get("type") or "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.current_jsonld = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in BALANCED and tag not in VOID:
            self.count_close[tag] += 1
        if tag == "script" and self.in_jsonld:
            self.jsonld_chunks.append("".join(self.current_jsonld).strip())
            self.current_jsonld = []
            self.in_jsonld = False

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self.current_jsonld.append(data)


def inspect(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    parser = Inspector()
    parser.feed(text)
    parser.close()

    errors: list[str] = []
    duplicate_ids = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicate_ids:
        errors.append(f"duplicate ids: {duplicate_ids}")

    for tag in sorted(BALANCED):
        opened = parser.count_open[tag]
        closed = parser.count_close[tag]
        if opened != closed:
            errors.append(f"<{tag}> balance {opened}/{closed}")

    if not parser.jsonld_chunks:
        errors.append("no JSON-LD")
    for index, raw in enumerate(parser.jsonld_chunks, 1):
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON-LD #{index}: {exc}")

    missing_links: list[str] = []
    for href in parser.links:
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        target = local_target(href)
        if target is not None and not target.exists():
            missing_links.append(href)
    if missing_links:
        errors.append("missing internal links: " + ", ".join(sorted(set(missing_links))))

    if len(re.findall(r"<h1\b", text, re.I)) != 1:
        errors.append("expected exactly one H1")
    if errors:
        raise SystemExit(f"{path.relative_to(ROOT)} failed integrity check:\n - " + "\n - ".join(errors))
    print(f"HTML integrity OK: {path.relative_to(ROOT)}; {len(parser.links)} links, {len(parser.ids)} ids, {len(parser.jsonld_chunks)} JSON-LD blocks")


def main() -> None:
    for path in PAGES:
        inspect(path)


if __name__ == "__main__":
    main()
