#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
BASE_HOST = "ohrana.tech"


def target_for_path(path: str) -> Path:
    if path == "/":
        return ROOT / "index.html"
    clean = path.lstrip("/")
    target = ROOT / clean
    if path.endswith("/"):
        target = target / "index.html"
    return target


def main() -> None:
    tree = ET.parse(SITEMAP)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for node in tree.findall("s:url/s:loc", ns):
        if not node.text:
            continue
        parsed = urlparse(node.text.strip())
        if parsed.netloc != BASE_HOST:
            raise SystemExit(f"Unexpected sitemap host: {node.text}")
        urls.append((node.text.strip(), target_for_path(parsed.path)))

    seen = set()
    duplicates = []
    missing = []
    for url, target in urls:
        if url in seen:
            duplicates.append(url)
        seen.add(url)
        if not target.exists():
            missing.append((url, str(target.relative_to(ROOT))))

    if duplicates:
        print("Duplicate sitemap URLs:")
        for url in duplicates:
            print(" -", url)
    if missing:
        print("Missing sitemap targets:")
        for url, target in missing:
            print(f" - {url} -> {target}")
    if duplicates or missing:
        raise SystemExit(1)

    print(f"Sitemap OK: {len(urls)} URLs, all targets exist, no duplicates")


if __name__ == "__main__":
    main()
