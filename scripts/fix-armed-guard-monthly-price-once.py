from pathlib import Path
import json

pricing = Path('site-src/pricing.json')
page = Path('ceny/index.html')

obj = json.loads(pricing.read_text(encoding='utf-8'))
for svc in obj.get('services', []):
    if svc.get('id') == 'armed-post':
        svc['name'] = 'Охрана с оружием'
        svc['price_from'] = 450000
        svc['unit'] = 'месяц'
        svc['note'] = '1 смена — 12 часов; охранник 6-го разряда'
        break
else:
    raise SystemExit('armed-post not found')

for ft in obj.get('featured_tariffs', []):
    if ft.get('service_id') == 'armed-post':
        ft['schedule'] = '1 смена — 12 часов'
        break

pricing.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

s = page.read_text(encoding='utf-8')
s = s.replace('"name":"Охрана с оружием","url":"https://ohrana.tech/fizicheskaya-ohrana/","priceSpecification":{"@type":"UnitPriceSpecification","minPrice":"450000","priceCurrency":"RUB","unitText":"смена"}',
              '"name":"Охрана с оружием","url":"https://ohrana.tech/fizicheskaya-ohrana/","priceSpecification":{"@type":"UnitPriceSpecification","minPrice":"450000","priceCurrency":"RUB","unitText":"месяц"}', 1)
s = s.replace('<h3>Охрана с оружием</h3>\n<div class="tariff-price">от 450 000 ₽/смена</div>',
              '<h3>Охрана с оружием</h3>\n<div class="tariff-price">от 450 000 ₽/месяц</div>', 1)
s = s.replace('<div><dt>График работы</dt><dd>сменный, по режиму объекта</dd></div>\n<div><dt>Экипировка</dt><dd>служебное оружие и спецсредства</dd></div>',
              '<div><dt>График работы</dt><dd>1 смена — 12 часов</dd></div>\n<div><dt>Экипировка</dt><dd>служебное оружие и спецсредства</dd></div>', 1)

if 'от 450 000 ₽/месяц' not in s or '1 смена — 12 часов' not in s:
    raise SystemExit('published page replacement failed')
page.write_text(s, encoding='utf-8')
print('corrected armed guard monthly price')
