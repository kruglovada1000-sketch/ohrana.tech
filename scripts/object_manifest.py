from __future__ import annotations

# Pages built from preserved source snapshots with the shared site shell.
OBJECT_PAGES = [
    ("ohrana-ofisov", "ohrana-ofisov.source.html"),
    ("ohrana-biznes-centrov", "ohrana-biznes-centrov.source.html"),
    ("ohrana-magazinov", "ohrana-magazinov.source.html"),
    ("ohrana-yuvelirnyh-magazinov", "ohrana-yuvelirnyh-magazinov.source.html"),
    ("ohrana-restoranov", "ohrana-restoranov.source.html"),
    ("ohrana-gostinic", "ohrana-gostinic.source.html"),
    ("ohrana-predpriyatij", "ohrana-predpriyatij.source.html"),
    ("ohrana-avtosalonov", "ohrana-avtosalonov.source.html"),
    ("ohrana-parkovok", "ohrana-parkovok.source.html"),
    ("ohrana-domov-i-kottedzhey", "ohrana-domov-i-kottedzhey.source.html"),
    ("ohrana-zhilyh-kompleksov", "ohrana-zhilyh-kompleksov.source.html"),
    ("ohrana-shkol", "ohrana-shkol.source.html"),
]

SPECIAL_OBJECT_SLUGS = ["ohrana-skladov"]
GENERATED_OBJECT_SLUGS = SPECIAL_OBJECT_SLUGS + [slug for slug, _ in OBJECT_PAGES]
GENERATED_PAGES = GENERATED_OBJECT_SLUGS + ["ceny"]
