from pathlib import Path
import json

ROOT = Path('.')
pricing_path = ROOT / 'site-src/pricing.json'
build_path = ROOT / 'scripts/build_site.py'
js_path = ROOT / 'site-src/assets/site.js'
css_path = ROOT / 'site-src/assets/pricing.css'

# Canonical tariff data: 7 tariffs. The 230k enhanced post remains separate
# from the 450k/month armed guard tariff.
data = json.loads(pricing_path.read_text(encoding='utf-8'))
services = [s for s in data['services'] if s.get('id') != 'enhanced-post']
for s in services:
    if s.get('id') == 'armed-post':
        s['name'] = 'Охрана с оружием'
        s['price_from'] = 450000
        s['unit'] = 'месяц'
        s['note'] = '1 смена — 12 часов; охранник 6-го разряда'
        break
else:
    raise SystemExit('armed-post service not found')
physical_index = next(i for i, s in enumerate(services) if s.get('id') == 'physical-post')
services.insert(physical_index + 1, {
    'id': 'enhanced-post',
    'name': 'Пост физической охраны усиленный',
    'price_from': 230000,
    'unit': 'месяц',
    'url': '/fizicheskaya-ohrana/',
    'note': 'усиленный режим поста, повышенные требования к охране',
})
data['services'] = services

data['featured_tariffs'] = [
    {
        'service_id': 'physical-post', 'badge': 'Пост 24/7',
        'description': 'Постоянная физическая охрана объекта, контроль доступа и поддержание установленного режима.',
        'schedule': '15/15, вахтовый режим', 'equipment': 'без оружия; спецсредства — по задаче',
        'training': '4–6 разряд', 'conditions': 'бытовые условия на объекте — по договорённости',
        'image': '/images/tarif-post-fizicheskoy-ohrany.webp', 'image_alt': 'Пост физической охраны объекта'
    },
    {
        'service_id': 'enhanced-post', 'badge': 'Усиленный пост',
        'description': 'Усиленный физический пост для объектов с повышенными требованиями к пропускному режиму и контролю территории.',
        'schedule': '15/15 или по режиму объекта', 'equipment': 'спецсредства и усиленная экипировка — по задаче',
        'training': '4–6 разряд', 'conditions': 'состав поста — после оценки объекта',
        'image': '/images/tarif-usilennyy-post.webp', 'image_alt': 'Усиленный пост физической охраны'
    },
    {
        'service_id': 'armed-post', 'badge': 'С оружием',
        'description': 'Вооружённая охрана для объектов с повышенными требованиями к режиму, материальным ценностям и уровню защиты.',
        'schedule': '1 смена — 12 часов', 'equipment': 'служебное оружие и спецсредства',
        'training': '6 разряд', 'conditions': 'состав поста — после оценки объекта',
        'image': '/images/tarif-ohrana-s-oruzhiem.webp', 'image_alt': 'Охрана объекта с оружием'
    },
    {
        'service_id': 'mobile-patrol', 'badge': 'Патрулирование',
        'description': 'Мобильная охрана территории, периметра и нескольких зон по согласованному маршруту.',
        'schedule': 'по маршруту и графику объекта', 'equipment': 'автомобиль, связь и спецсредства',
        'training': '4–6 разряд', 'conditions': '1 автомобиль, 2 сотрудника',
        'image': '/images/tarif-mobilnoe-patrulirovanie.webp', 'image_alt': 'Мобильное патрулирование охраняемой территории'
    },
    {
        'service_id': 'pult-chop', 'badge': 'Пульт + ГБР',
        'description': 'Круглосуточный контроль тревожных сигналов и выезд группы быстрого реагирования по событию.',
        'schedule': '24/7, круглосуточный мониторинг', 'equipment': 'тревожная сигнализация, связь с пультом',
        'training': 'экипаж ГБР по регламенту ЧОО', 'conditions': 'оборудование и монтаж рассчитываются отдельно',
        'image': '/images/tarif-pultovaya-ohrana-gbr.webp', 'image_alt': 'Пультовая охрана и группа быстрого реагирования'
    },
    {
        'service_id': 'event-standard', 'badge': 'Разовая охрана',
        'description': 'Охрана входной зоны, гостей, персонала и порядка на деловых и частных мероприятиях.',
        'schedule': 'от 4 часов', 'equipment': 'спецсредства — по формату мероприятия',
        'training': '4–6 разряд', 'conditions': 'базовый ориентир — до 100 гостей',
        'image': '/images/tarif-ohrana-meropriyatiya.webp', 'image_alt': 'Охрана делового или частного мероприятия'
    },
    {
        'service_id': 'personal', 'badge': 'Персональная защита',
        'description': 'Личная охрана клиента с индивидуальным маршрутом, режимом сопровождения и составом задач.',
        'schedule': 'до 12 часов в сутки', 'equipment': 'по задаче и требованиям клиента',
        'training': '6 разряд', 'conditions': '1 телохранитель',
        'image': '/images/tarif-lichnaya-ohrana.webp', 'image_alt': 'Личная охрана и сопровождение клиента'
    },
]
pricing_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Build generator: pair each tariff card with its image card.
s = build_path.read_text(encoding='utf-8')
start = s.index('    featured_cards: list[str] = []')
end = s.index('\n\n    title = ', start)
new_featured = '''    carousel_items: list[str] = []
    featured_tariffs = PRICING.get("featured_tariffs", [])
    for index, tariff in enumerate(featured_tariffs, start=1):
        service = service_by_id[tariff["service_id"]]
        carousel_items.append(
            f\'''<article class="tariff-card" data-tariff-card data-carousel-item>
<div class="tariff-card-head"><span class="tariff-badge">{esc(tariff['badge'])}</span><span class="tariff-no">{index:02d}</span></div>
<h3>{esc(service['name'])}</h3>
<div class="tariff-price">{money(service['price_from'], service['unit'])}</div>
<p class="tariff-desc">{esc(tariff['description'])}</p>
<dl class="tariff-specs">
<div><dt>График работы</dt><dd>{esc(tariff['schedule'])}</dd></div>
<div><dt>Экипировка</dt><dd>{esc(tariff['equipment'])}</dd></div>
<div><dt>Профподготовка</dt><dd>{esc(tariff['training'])}</dd></div>
<div><dt>Условия</dt><dd>{esc(tariff['conditions'])}</dd></div>
</dl>
<div class="tariff-card-actions"><a class="btn btn-gold" href="/kontakty/">Заказать</a><a class="tariff-more" href="{esc(service['url'])}">Подробнее →</a></div>
</article>\'''
        )
        carousel_items.append(
            f\'''<figure class="tariff-card tariff-image-card" data-carousel-item aria-label="{esc(tariff['image_alt'])}">
<img src="{esc(tariff['image'])}" alt="{esc(tariff['image_alt'])}" width="1200" height="900" loading="lazy" decoding="async">
</figure>\'''
        )
    carousel_dots = ''.join(
        f'<button type="button" data-carousel-dot aria-label="Показать тариф {i}" aria-pressed="false"></button>'
        for i in range(1, len(featured_tariffs) + 1)
    )'''
s = s[:start] + new_featured + s[end:]
s = s.replace('Шесть основных вариантов для быстрого ориентира.', 'Семь основных вариантов для быстрого ориентира.')
s = s.replace("{''.join(featured_cards)}", "{''.join(carousel_items)}")
s = s.replace('/assets/css/pricing.css?v=20260920-carousel3', '/assets/css/pricing.css?v=20260921-loop1')
s = s.replace('/assets/js/site.js?v=20260920-theme-carousel3', '/assets/js/site.js?v=20260921-loop1')
# Preserve the current visual hero if the generator still contains the early text-only version.
old_hero = '<section class="price-hero"><div class="wrap" data-reveal><span class="price-kicker">Стоимость услуг</span><h1>Цены на <em>охранные услуги</em></h1><p class="price-lead">Единый каталог ориентировочных тарифов. Выберите тип объекта или услугу. Точный расчёт делаем после уточнения режима, количества постов, площади и задач.</p><div class="price-actions"><a class="btn btn-gold" href="#tariffs">Смотреть тарифы</a><a class="btn btn-line" href="/kontakty/">Получить точный расчёт</a></div></div></section>'
new_hero = '<section class="price-hero"><div class="wrap price-hero-grid" data-reveal data-pricing-visual="1"><div class="price-hero-copy"><span class="price-kicker">Стоимость услуг</span><h1>Цены на <em>охранные услуги</em></h1><p class="price-lead">Единый каталог ориентировочных тарифов. Выберите тип объекта или услугу. Точный расчёт делаем после уточнения режима, количества постов, площади и задач.</p><div class="price-actions"><a class="btn btn-gold" href="#tariffs">Смотреть тарифы</a><a class="btn btn-line" href="/kontakty/">Получить точный расчёт</a></div></div><figure class="price-hero-visual"><img class="price-hero-bg" src="/images/ceny-hero.svg?v=20260920-brandshield2" alt="Аналитика стоимости охранных услуг" width="1600" height="900" fetchpriority="high" decoding="async"><div class="price-brand-shield"><img src="/images/schit.png" alt="Логотип ЧОО «Рускорпорация»" loading="eager" decoding="async"><svg class="price-brand-spark" viewBox="0 0 120 140" aria-hidden="true"><path class="spark-rail" d="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/><path class="spark-run" d="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/><circle class="spark-head" r="2.2"><animateMotion dur="4.8s" repeatCount="indefinite" path="M60 7 107 25 102 76c-4 29-20 48-42 58-22-10-38-29-42-58L13 25 60 7Z"/></circle></svg></div></figure></div></section>'
if old_hero in s:
    s = s.replace(old_hero, new_hero, 1)
build_path.write_text(s, encoding='utf-8')

# Shared JS: seamless continuously moving carousel. Duplicate one full 14-item strip;
# the reset is visually invisible because the duplicate is identical.
js = js_path.read_text(encoding='utf-8')
js_start = js.index("document.querySelectorAll('[data-price-carousel]').forEach(function(carousel)")
js_end = js.index('\n})();', js_start)
new_js = '''document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){
  var viewport=carousel.querySelector('[data-carousel-viewport]'),track=carousel.querySelector('.tariff-track');
  if(!viewport||!track)return;
  var originals=Array.prototype.slice.call(track.children);
  if(!originals.length)return;
  function itemWidth(){var gap=16;return window.matchMedia&&window.matchMedia('(max-width:700px)').matches?viewport.clientWidth:Math.max(280,(viewport.clientWidth-gap)/2);}
  function sizeItems(){var width=itemWidth();Array.prototype.slice.call(track.children).forEach(function(item){item.style.flexBasis=width+'px';item.style.width=width+'px';});}
  if(rm){sizeItems();carousel.classList.add('tariff-reduced-motion');return;}
  originals.forEach(function(item){var clone=item.cloneNode(true);clone.setAttribute('aria-hidden','true');clone.removeAttribute('data-tariff-card');clone.removeAttribute('data-carousel-item');clone.querySelectorAll('a,button,input,select,textarea,[tabindex]').forEach(function(el){el.setAttribute('tabindex','-1');});track.appendChild(clone);});
  var loopWidth=0,last=performance.now(),speed=42;
  function measure(){sizeItems();requestAnimationFrame(function(){var firstClone=track.children[originals.length];loopWidth=firstClone?firstClone.offsetLeft-track.children[0].offsetLeft:0;if(loopWidth>0&&viewport.scrollLeft>=loopWidth)viewport.scrollLeft%=loopWidth;});}
  function tick(now){var dt=Math.min(64,now-last);last=now;if(loopWidth>0){viewport.scrollLeft+=speed*dt/1000;if(viewport.scrollLeft>=loopWidth)viewport.scrollLeft-=loopWidth;}requestAnimationFrame(tick);}
  window.addEventListener('resize',measure,{passive:true});measure();requestAnimationFrame(tick);
});'''
js = js[:js_start] + new_js + js[js_end:]
js_path.write_text(js, encoding='utf-8')

# CSS overrides for 2-up text/image pairs and continuous loop.
css = css_path.read_text(encoding='utf-8')
marker = '/* pricing-seamless-paired-carousel-v1 */'
if marker not in css:
    css = css.rstrip() + '''\n\n/* pricing-seamless-paired-carousel-v1 */
.tariff-viewport{overflow:hidden!important;scroll-snap-type:none!important;scroll-behavior:auto!important;overscroll-behavior-x:none!important;padding-bottom:22px}
.tariff-track{display:flex!important;grid-auto-flow:unset!important;grid-auto-columns:unset!important;width:max-content!important;min-width:0!important;gap:16px;align-items:stretch}
.tariff-track>.tariff-card{flex:0 0 auto;scroll-snap-align:none!important}
.tariff-image-card{padding:0!important;min-height:500px;background:var(--panel);overflow:hidden}
.tariff-image-card::before{display:none!important}
.tariff-image-card img{display:block;width:100%;height:100%;min-height:500px;object-fit:cover;object-position:center;transition:transform .7s var(--ease),filter .4s;filter:saturate(.92) contrast(1.04)}
.tariff-image-card:hover img{transform:scale(1.025);filter:saturate(1) contrast(1.05)}
.tariff-controls{display:none!important}
.tariff-reduced-motion .tariff-viewport{overflow-x:auto!important;scroll-snap-type:x mandatory!important}
.tariff-reduced-motion .tariff-track>.tariff-card{scroll-snap-align:start!important}
@media(max-width:700px){.tariff-image-card,.tariff-image-card img{min-height:430px}}
''' + '\n'
css_path.write_text(css, encoding='utf-8')

print('prepared canonical 7-tariff / 14-item seamless pricing carousel')
