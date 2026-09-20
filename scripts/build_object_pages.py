#!/usr/bin/env python3
from __future__ import annotations

from build_site import ROOT, build_legacy_page, validate_html


def main() -> None:
    build_legacy_page("ohrana-ofisov", "ohrana-ofisov.source.html")
    validate_html(ROOT / "ohrana-ofisov" / "index.html")
    print("Built and validated: /ohrana-ofisov/")


if __name__ == "__main__":
    main()
