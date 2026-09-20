#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"
MANIFEST = SRC / "document-pages.json"

SEO_HEAD = """<meta name=\"robots\" content=\"noindex,follow\">\n<meta name=\"theme-color\" content=\"#07090D\">\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n<link href=\"https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500;600&family=Manrope:wght@400;600;700;800&display=swap\" rel=\"stylesheet\">"""


def main() -> None:
    pages = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("document-pages.json must contain at least one document")

    for item in pages:
        path = ROOT / item["path"]
        source = SRC / "pages" / item["source"]
        if not source.exists():
            raise RuntimeError(f"Missing document snapshot: {source}")
        html = source.read_text(encoding="utf-8")
        if '<meta name="robots"' not in html:
            viewport = re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', html, re.I)
            if not viewport:
                raise RuntimeError(f"No viewport meta in {source}")
            html = html[:viewport.end()] + "\n" + SEO_HEAD + html[viewport.end():]
        if '/css/style.css' not in html:
            raise RuntimeError(f"Document does not load /css/style.css: {source}")
        if 'class="kp-wrap"' not in html or '<h1' not in html.lower():
            raise RuntimeError(f"Document structure incomplete: {source}")
        if 'window.print()' not in html:
            raise RuntimeError(f"Print action missing: {source}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"Prepared managed document: /{item['slug']}/")


if __name__ == "__main__":
    main()
