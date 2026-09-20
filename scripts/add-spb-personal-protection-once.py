from pathlib import Path

published = Path('ohrana-fizicheskih-lic/index.html')
source = Path('site-src/pages/ohrana-fizicheskih-lic.source.html')

bullet = '            <li><strong>Санкт-Петербург:</strong> личная охрана и сопровождение по предварительному согласованию.</li>\n'

for p in (published, source):
    s = p.read_text(encoding='utf-8')
    if '<strong>Санкт-Петербург:</strong>' not in s:
        needle = '            <li><strong>Сочи и Краснодарский край:</strong> сезонная и постоянная охрана VIP-объектов и мероприятий.</li>\n'
        if needle not in s:
            raise SystemExit(f'region bullet anchor not found in {p}')
        s = s.replace(needle, needle + bullet, 1)

    if p == source:
        old = '    { "@type": "City", "name": "Сочи" }\n  ],'
        new = '    { "@type": "City", "name": "Сочи" },\n    { "@type": "City", "name": "Санкт-Петербург" }\n  ],'
    else:
        old = '{"@type":"City","name":"Сочи"}]'
        new = '{"@type":"City","name":"Сочи"},{"@type":"City","name":"Санкт-Петербург"}]'
    if '"name":"Санкт-Петербург"' not in s and '"name": "Санкт-Петербург"' not in s:
        if old not in s:
            raise SystemExit(f'areaServed anchor not found in {p}')
        s = s.replace(old, new, 1)

    p.write_text(s, encoding='utf-8')
    print('updated', p)
