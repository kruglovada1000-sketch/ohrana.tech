#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from build_site import ROOT, SRC, SITE, read_partial

ORG_ID = f"{SITE['site_url']}/#organization"
SCRIPT_RE = re.compile(
    r"<script\s+type=[\"']application/ld\+json[\"']>(.*?)</script>",
    re.I | re.S,
)


def load_manifest(name: str) -> list[dict[str, object]]:
    path = SRC / name
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise RuntimeError(f"{name} must contain a list")
    return value


def generated_pages() -> list[Path]:
    paths = [ROOT / "ohrana-skladov" / "index.html", ROOT / "ceny" / "index.html"]
    for manifest_name in ("object-pages.json", "custom-pages.json"):
        paths.extend(ROOT / str(page["slug"]) / "index.html" for page in load_manifest(manifest_name))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def types_of(value: dict) -> set[str]:
    node_type = value.get("@type")
    if isinstance(node_type, list):
        return {str(item) for item in node_type}
    if node_type:
        return {str(node_type)}
    return set()


def looks_like_company(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("@id") == ORG_ID:
        return True
    name = " ".join(str(value.get(key, "")) for key in ("name", "legalName", "alternateName")).lower()
    url = str(value.get("url", "")).rstrip("/")
    return "рускорпорац" in name or url == str(SITE["site_url"]).rstrip("/")


def is_company_organization(value: object) -> bool:
    return isinstance(value, dict) and "Organization" in types_of(value) and looks_like_company(value)


def sanitize(value: object, *, graph_item: bool = False) -> object | None:
    if isinstance(value, list):
        cleaned = []
        for item in value:
            result = sanitize(item, graph_item=graph_item)
            if result is not None:
                cleaned.append(result)
        return cleaned

    if not isinstance(value, dict):
        return value

    if graph_item and is_company_organization(value):
        return None

    result: dict = {}
    for key, child in value.items():
        if key == "@graph" and isinstance(child, list):
            graph = []
            for node in child:
                cleaned = sanitize(node, graph_item=True)
                if cleaned is not None:
                    graph.append(cleaned)
            result[key] = graph
            continue

        if key in {"provider", "publisher", "seller"} and looks_like_company(child):
            result[key] = {"@id": ORG_ID}
            continue

        cleaned = sanitize(child, graph_item=False)
        if cleaned is not None:
            result[key] = cleaned
    return result


def normalize_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        data = json.loads(raw)
        if is_company_organization(data):
            return ""
        cleaned = sanitize(data)
        if isinstance(cleaned, dict) and cleaned.get("@graph") == []:
            return ""
        return '<script type="application/ld+json">' + json.dumps(
            cleaned, ensure_ascii=False, separators=(",", ":")
        ) + "</script>"

    text = SCRIPT_RE.sub(replace, text)
    organization = read_partial("organization-jsonld.html").strip()
    text = text.replace("</head>", organization + "\n</head>", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for path in generated_pages():
        if not path.exists():
            raise RuntimeError(f"Missing generated page before JSON-LD normalization: {path}")
        normalize_page(path)
        print(f"Normalized JSON-LD organization: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
