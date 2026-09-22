#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'site-src'
SITE = json.loads((SRC / 'site.json').read_text(encoding='utf-8'))
GROUP = json.loads((SRC / 'services-group-d.json').read_text(encoding='utf-8'))

PROFILES = {
'ohrana-stroitelnyh-obektov': {
'intro': ['Строительная площадка требует контроля периметра, въездов, техники, материалов и доступа подрядчиков в течение всего цикла работ.', 'Схема охраны учитывает график смен, количество КПП, зоны складирования, временные сооружения и особенности территории.'],
'risks': ['хищение строительных материалов и инструмента', 'несанкционированный въезд транспорта', 'проникновение через периметр', 'доступ посторонних в опасные зоны', 'повреждение техники и временной инфраструктуры']},
'ohrana-proizvodstvennyh-obektov': {
'intro': ['Производственный объект сочетает пропускной режим, материальные ценности, оборудование, складские зоны и движение персонала и транспорта.', 'Охрана выстраивается с учётом технологического режима, сменности, КПП, внутренних зон доступа и требований предприятия.'],
'risks': ['несанкционированный проход в производственные зоны', 'хищение сырья, продукции или оборудования', 'нарушения пропускного режима', 'несогласованный въезд и выезд транспорта', 'проникновение на территорию вне рабочего времени']},
'ohrana-selskohozyaystvennyh-obektov': {
'intro': ['Сельскохозяйственные объекты часто имеют большую территорию, удалённые участки, технику, склады и сезонные пики работ.', 'Формат охраны подбирается под периметр, количество въездов, режим хранения имущества и фактическую загрузку объекта.'],
'risks': ['кража техники, топлива и материалов', 'проникновение на удалённые участки', 'несанкционированный вывоз имущества', 'повреждение складов и хозяйственных построек', 'риски в периоды сезонного простоя']},
'ohrana-rynkov': {
'intro': ['Рынок объединяет большой поток посетителей, арендаторов, поставщиков, зоны разгрузки и денежные расчёты.', 'Охрана должна поддерживать порядок, контролировать служебные зоны и быстро реагировать на конфликтные и тревожные ситуации.'],
'risks': ['конфликты между посетителями и арендаторами', 'кражи в торговых рядах', 'несанкционированный доступ в складские зоны', 'нарушения при разгрузке и закрытии рынка', 'проникновение на территорию после завершения работы']},
'ohrana-aptek': {
'intro': ['Аптека требует защиты персонала, кассовой зоны, товарных запасов и служебных помещений при постоянном потоке посетителей.', 'Физическая охрана при необходимости дополняется тревожной кнопкой, видеонаблюдением и пультовым реагированием.'],
'risks': ['кражи из торгового зала', 'угрозы и конфликты с посетителями', 'несанкционированный доступ в служебные помещения', 'риски для кассовой зоны', 'проникновение в нерабочее время']},
'ohrana-fitnes-klubov-salonov': {
'intro': ['Фитнес-клубы и салоны работают с постоянным потоком клиентов, раздевалками, ресепшеном, служебными помещениями и материальными ценностями.', 'Охрана должна быть корректной для посетителей и одновременно обеспечивать контроль доступа и реагирование на инциденты.'],
'risks': ['кражи личных вещей посетителей', 'конфликты в клиентской зоне', 'проход посторонних в служебные помещения', 'нарушения режима доступа', 'риски в вечерние часы и при закрытии объекта']},
'ohrana-yaht-klubov': {
'intro': ['Яхт-клуб сочетает береговую территорию, причалы, дорогостоящее имущество, парковку и доступ владельцев, гостей и технического персонала.', 'Схема охраны учитывает особенности периметра, сезонность, ночной режим и контроль доступа к причалам и служебным зонам.'],
'risks': ['несанкционированный доступ к причалам', 'кража оборудования и имущества', 'проникновение на территорию в ночное время', 'несогласованный доступ транспорта и посетителей', 'повреждение инфраструктуры клуба']},
'ohrana-parkov-usadeb': {
'intro': ['Парки и усадьбы имеют протяжённую территорию, открытые зоны, объекты инфраструктуры и переменный поток посетителей.', 'Охрана сочетает патрулирование, контроль ключевых входов и наблюдение за зонами повышенного риска.'],
'risks': ['вандализм и повреждение имущества', 'проникновение в закрытые зоны', 'нарушения общественного порядка', 'кражи оборудования и элементов благоустройства', 'риски в вечернее и ночное время']},
'ohrana-pansionatov-sanatoriev': {
'intro': ['Пансионаты и санатории требуют спокойной и ненавязчивой охраны с контролем входов, территории, служебных помещений и парковки.', 'Схема безопасности учитывает проживание гостей, круглосуточную работу отдельных зон и доступ подрядчиков и посетителей.'],
'risks': ['проход посторонних в жилые корпуса', 'конфликтные ситуации с посетителями', 'кражи имущества гостей или объекта', 'несанкционированный доступ в служебные зоны', 'нарушения порядка в вечернее и ночное время']}
}

INCLUDED = [
'физический пост и контроль ключевых точек доступа',
'пропускной режим для персонала, посетителей и подрядчиков',
'обходы и патрулирование территории по регламенту',
'пультовая охрана и тревожная сигнализация — при необходимости',
'видеонаблюдение, СКУД и взаимодействие с ГБР — по задаче объекта'
]

def render(text: str) -> str:
    for k, v in SITE.items():
        text = text.replace('{{site.%s}}' % k, str(v))
    return text

def partial(name: str) -> str:
    out = render((SRC / 'partials' / name).read_text(encoding='utf-8'))
    if name == 'footer.html':
        out = out.replace('Лицензированное ЧОП — профессиональная охрана объектов и людей с 2018 года.', 'Лицензированное ЧОО — профессиональная охрана объектов и людей. Опыт команды — с 2007 года.')
        out = out.replace('ООО ЧОП «Рускорпорация»', 'ООО ЧОО «Рускорпорация»').replace('ООО ЧОП «Рускорпорация охрана и консалтинг»', 'ООО ЧОО «Рускорпорация охрана и консалтинг»')
    return out

def image_block(item: dict) -> str:
    rel = item['image']
    path = ROOT / rel.lstrip('/')
    alt = f"{item['name']} — ЧОО «Рускорпорация»"
    if path.exists():
        return f'<figure class="service-photo-slot"><img src="{rel}" alt="{alt}" width="1200" height="800" loading="eager" decoding="async"></figure>'
    return f'<figure class="service-photo-slot" data-image-file="{rel}" aria-label="Место для тематического изображения"><span>Файл изображения: {rel.split("/")[-1]}</span></figure>'

def faq_items(item: dict):
    return [
        (f"Сколько стоит {item['name'].lower()}?", f"{item['price']}. Итоговая стоимость зависит от режима, площади, количества постов, точек доступа и дополнительных задач."),
        ('Можно ли организовать круглосуточную охрану?', 'Да. Режим и состав смены определяются после обследования объекта и согласования требований заказчика.'),
        ('Можно ли подключить пультовую охрану и ГБР?', 'Да. При необходимости физическая охрана дополняется пультовой защитой, тревожной сигнализацией и реагированием ГБР.'),
        ('Можно ли использовать видеонаблюдение и СКУД?', 'Да. Технические средства безопасности включаются в схему после обследования объекта и согласования задач.'),
        ('Что нужно для расчёта стоимости?', 'Адрес, площадь, количество входов или КПП, режим работы и основные задачи охраны.')
    ]

def schema(item: dict) -> str:
    url = SITE['site_url'] + item['url']
    faq = [{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq_items(item)]
    data = {'@context':'https://schema.org','@graph':[
        {'@type':'LocalBusiness','@id':SITE['site_url']+'/#organization','name':SITE['name'],'legalName':SITE['legal_name'],'url':SITE['site_url'],'telephone':SITE['phone'],'email':SITE['email']},
        {'@type':'Service','@id':url+'#service','name':item['name'],'serviceType':item['name'],'areaServed':['Москва','Московская область'],'provider':{'@id':SITE['site_url']+'/#organization'},'url':url},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Главная','item':SITE['site_url']+'/'},
            {'@type':'ListItem','position':2,'name':'Услуги','item':SITE['site_url']+'/uslugi/'},
            {'@type':'ListItem','position':3,'name':GROUP['title'],'item':SITE['site_url']+GROUP['url']},
            {'@type':'ListItem','position':4,'name':item['name'],'item':url}
        ]},
        {'@type':'FAQPage','mainEntity':faq}
    ]}
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def faq_html(item: dict) -> str:
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq_items(item))

def page(item: dict) -> str:
    slug = item['url'].strip('/').split('/')[-1]
    p = PROFILES[slug]
    title = f"{item['name']} в Москве и МО — ЧОО «Рускорпорация»"
    desc = f"{item['name']} в Москве и Московской области. Физическая и пультовая охрана, контроль доступа, видеонаблюдение и ГБР. Расчёт под объект."
    risks = ''.join(f'<li>{x}</li>' for x in p['risks'])
    included = ''.join(f'<li>{x}</li>' for x in INCLUDED)
    intro = ''.join(f'<p class="service-lead">{x}</p>' for x in p['intro'])
    siblings = ''.join(f'<a href="{x["url"]}">{x["name"]}</a>' for x in GROUP['services'] if x['url'] != item['url'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>
{partial('head-common.html')}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE['site_url']}{item['url']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE['site_url']}{item['url']}">
<script type="application/ld+json">{schema(item)}</script><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head>
<body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}
<main class="service-page"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><a href="{GROUP['url']}">{GROUP['title']}</a><span>/</span><b>{item['name']}</b></nav>
<section class="service-hero"><div><span class="service-kicker">Специальные объекты</span><h1>{item['name']} в Москве и Московской области</h1>{intro}<div class="service-actions"><a class="btn btn-gold" href="#request">Рассчитать стоимость</a><a class="btn btn-line" href="/kontakty/">Связаться</a></div></div>{image_block(item)}</section>
<section class="service-section"><h2>Основные риски объекта</h2><div class="service-grid"><article class="service-card"><h3>Что контролируем</h3><ul class="service-list">{risks}</ul></article><article class="service-card"><h3>Что входит в услугу</h3><ul class="service-list">{included}</ul></article></div></section>
<section class="service-section"><h2>Стоимость охраны</h2><div class="service-card"><div class="service-price">{item['price']}</div><p class="service-note">Итоговая стоимость зависит от режима, площади, количества постов, точек доступа, технического оснащения и дополнительных задач.</p><div class="service-actions"><a class="btn btn-gold" href="#request">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Все тарифы</a></div></div></section>
<section class="service-section"><h2>Практическая конфигурация</h2><div class="service-card"><p>Схема охраны формируется после обследования объекта и уточнения режима работы, периметра, точек доступа и задач заказчика. Реальный кейс с цифрами публикуем только после подтверждения фактических данных.</p></div></section>
<section class="service-section"><h2>Почему ЧОО «Рускорпорация»</h2><div class="service-grid"><article class="service-card"><h3>Лицензия</h3><p>Лицензия {SITE['license']}.</p></article><article class="service-card"><h3>Комплексный подход</h3><p>Физическая охрана, пульт, видеонаблюдение, СКУД и реагирование объединяются в единую схему под объект.</p></article><article class="service-card"><h3>Ответственность</h3><p>Условия ответственности и страхования фиксируются в договорных документах для конкретного проекта.</p></article><article class="service-card"><h3>Круглосуточный контроль</h3><p>При необходимости подключается пультовая охрана и реагирование ГБР.</p></article></div></section>
<section class="service-section"><h2>Частые вопросы</h2><div class="service-faq">{faq_html(item)}</div></section>
<section class="service-section"><h2>Смотрите также</h2><div class="service-links"><a href="/fizicheskaya-ohrana/">Физическая охрана</a><a href="/ohrana-pult/">Пультовая охрана</a><a href="/stati/">Статьи о безопасности</a></div><div class="service-links" style="margin-top:12px">{siblings}</div></section>
<section class="service-section" id="request"><h2>Получить расчёт</h2><form class="service-form" action="{SITE['formspree_url']}" method="POST"><div class="service-form-grid"><input name="name" required placeholder="Ваше имя"><input name="phone" required inputmode="tel" placeholder="Телефон"><textarea class="full" name="message" placeholder="Адрес объекта, режим работы, точки доступа и задачи"></textarea><label class="service-consent full"><input type="checkbox" required> <span>Согласен на обработку персональных данных.</span></label><div class="full"><button class="btn btn-gold" type="submit">Отправить заявку</button></div></div></form></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def group_hub() -> str:
    cards = ''.join(f'<a class="service-hub-card" href="{i["url"]}"><b>{i["name"]}</b><span>{i["price"]}</span></a>' for i in GROUP['services'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{GROUP['title']} в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Охрана специальных объектов в Москве и МО: стройки, производство, сельхозобъекты, рынки, аптеки, фитнес-клубы, яхт-клубы, парки и санатории."><link rel="canonical" href="{SITE['site_url']}{GROUP['url']}"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><b>{GROUP['title']}</b></nav><span class="service-kicker">Группа D</span><h1>{GROUP['title']} в Москве и Московской области</h1><p class="service-lead">Строительные и производственные площадки, сельскохозяйственные объекты, рынки, аптеки, фитнес-клубы, яхт-клубы, парки, усадьбы, пансионаты и санатории.</p><section class="service-section"><div class="service-hub-grid">{cards}</div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def update_root_hub():
    path = ROOT / 'uslugi' / 'index.html'
    txt = path.read_text(encoding='utf-8')
    old = '<div class="service-hub-card"><b>Специальные объекты</b><span>Следующий блок</span></div>'
    new = f'<a class="service-hub-card" href="{GROUP["url"]}"><b>Специальные объекты</b><span>{len(GROUP["services"])} направлений — блок D</span></a>'
    if old in txt:
        txt = txt.replace(old, new, 1)
        path.write_text(txt, encoding='utf-8')
    elif GROUP['url'] not in txt:
        raise SystemExit('Special services placeholder not found in uslugi/index.html')

def append_sitemap(urls):
    path = ROOT / 'sitemap.xml'
    txt = path.read_text(encoding='utf-8')
    additions = []
    for u in urls:
        loc = SITE['site_url'] + u
        if f'<loc>{loc}</loc>' in txt:
            continue
        additions.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    if additions:
        txt = txt.replace('</urlset>', ''.join(additions) + '</urlset>')
        path.write_text(txt, encoding='utf-8')

def main():
    if not (ROOT / 'css' / 'service-pages.css').exists():
        raise SystemExit('css/service-pages.css is required')
    gp = ROOT / GROUP['url'].strip('/')
    gp.mkdir(parents=True, exist_ok=True)
    (gp / 'index.html').write_text(group_hub(), encoding='utf-8')
    urls = [GROUP['url']]
    for item in GROUP['services']:
        out = ROOT / item['url'].strip('/')
        out.mkdir(parents=True, exist_ok=True)
        (out / 'index.html').write_text(page(item), encoding='utf-8')
        urls.append(item['url'])
    update_root_hub()
    append_sitemap(urls)
    print('Generated', len(GROUP['services']), 'special service pages + hub')

if __name__ == '__main__':
    main()
