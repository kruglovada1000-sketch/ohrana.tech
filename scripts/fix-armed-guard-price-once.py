from pathlib import Path
import json

repo = Path('.')
pricing = repo / 'site-src/pricing.json'
page = repo / 'ceny/index.html'

# Source data
obj = json.loads(pricing.read_text(encoding='utf-8'))
for svc in obj.get('services', []):
    if svc.get('id') == 'armed-post':
        svc['name'] = 'Охрана с оружием'
        svc['price_from'] = 450000
        svc['unit'] = 'смена'
        break
else:
    raise SystemExit('armed-post not found in pricing.json')
pricing.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Published page: structured data + visible tariff card only.
s = page.read_text(encoding='utf-8')
repls = [
    ('"name":"Вооружённый пост","url":"https://ohrana.tech/fizicheskaya-ohrana/","priceSpecification":{"@type":"UnitPriceSpecification","minPrice":"230000","priceCurrency":"RUB","unitText":"месяц"}',
     '"name":"Охрана с оружием","url":"https://ohrana.tech/fizicheskaya-ohrana/","priceSpecification":{"@type":"UnitPriceSpecification","minPrice":"450000","priceCurrency":"RUB","unitText":"смена"}'),
    ('<h3>Вооружённый пост</h3>\n<div class="tariff-price">от 230 000 ₽/месяц</div>',
     '<h3>Охрана с оружием</h3>\n<div class="tariff-price">от 450 000 ₽/смена</div>'),
]
for old, new in repls:
    if old not in s:
        raise SystemExit('expected armed tariff pattern not found in ceny/index.html')
    s = s.replace(old, new, 1)
page.write_text(s, encoding='utf-8')
print('updated armed tariff price and unit')
