#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "sitemap.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

ALIASES = {
    "https://ohrana.tech/ohrana-uvelirnyh-magazinov/": "https://ohrana.tech/ohrana-yuvelirnyh-magazinov/",
    "https://ohrana.tech/ohrana-stroyaploshchadok/": "https://ohrana.tech/ohrana-stroitelnyh-obektov/",
}
REMOVE = {
    "https://ohrana.tech/kompleksnaja-ohrana/",
    "https://ohrana.tech/ohrana-kottedzhey/",
}


def main() -> None:
    tree = ET.parse(PATH)
    root = tree.getroot()
    q = f"{{{NS}}}"
    seen: set[str] = set()
    changed = False

    for url_node in list(root.findall(f"{q}url")):
        loc_node = url_node.find(f"{q}loc")
        if loc_node is None or not loc_node.text:
            root.remove(url_node)
            changed = True
            continue

        loc = loc_node.text.strip()
        if loc in REMOVE:
            root.remove(url_node)
            changed = True
            continue

        replacement = ALIASES.get(loc)
        if replacement:
            loc_node.text = replacement
            loc = replacement
            changed = True

        if loc in seen:
            root.remove(url_node)
            changed = True
            continue
        seen.add(loc)

    ET.indent(tree, space="  ")
    tree.write(PATH, encoding="utf-8", xml_declaration=True)
    print(f"Sitemap normalized: {len(seen)} URLs" + ("; changes applied" if changed else "; already clean"))


if __name__ == "__main__":
    main()
