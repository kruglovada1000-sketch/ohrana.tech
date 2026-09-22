#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'site-src'
SITE=json.loads((SRC/'site.json').read_text(encoding='utf-8'))
GROUP=json.loads((SRC/'services-group-a.json').read_text(encoding='utf-8'))

PROFILES={
'ohrana-skladov':{
'intro':['Склад и логистический центр требуют контроля входов, движения транспорта, зон отгрузки, периметра и доступа персонала.','Схема охраны подбирается под график объекта, количество ворот и КПП, площадь территории и режим хранения материальных ценностей.'],
'risks':['несанкционированный доступ на территорию','хищение товара и материальных ценностей','вынос имущества персоналом или подрядчиками','проникновение через периметр и служебные зоны','нарушения при въезде, выезде и отгрузке']},
'ohrana-magazinov':{
'intro':['Охрана магазина должна учитывать посетительский поток, кассовую зону, складские помещения, персонал и режим открытия и закрытия.','Физический пост может дополняться тревожной сигнализацией, видеонаблюдением и пультовым реагированием.'],
'risks':['кражи из торгового зала','конфликты с посетителями','несанкционированный доступ в служебные помещения','риски при открытии и закрытии магазина','хищения в зоне приёмки и хранения товара']},
'ohrana-ofisov':{
'intro':['Для офиса важны управляемый доступ сотрудников и посетителей, контроль общих зон и защита имущества вне рабочего времени.','Охрана может работать по графику офиса или круглосуточно, а физический пост дополняться СКУД, видеонаблюдением и тревожной сигнализацией.'],
'risks':['проход посторонних лиц','кража оборудования и документов','конфликтные ситуации на ресепшен','несанкционированный доступ в закрытые зоны','риски в нерабочее время']},
'ohrana-bankov':{
'intro':['Банковские помещения требуют повышенного внимания к контролю доступа, реагированию и защите режимных зон.','Состав охраны определяется задачами конкретного офиса, графиком работы и требованиями к техническим средствам безопасности.'],
'risks':['попытки несанкционированного прохода','угрозы персоналу и посетителям','конфликтные ситуации в клиентской зоне','риски для кассовых и режимных помещений','проникновение в нерабочее время']},
'ohrana-torgovyh-centrov':{
'intro':['В торговом центре одновременно работают посетительские, служебные, технические, парковочные и разгрузочные зоны, поэтому охрана строится как единая система.','Количество постов и маршрутов патрулирования зависит от площади, числа входов, режима работы арендаторов и особенностей объекта.'],
'risks':['конфликты и нарушения порядка','кражи в общественных и торговых зонах','проникновение в служебные помещения','нарушения на парковке и разгрузочных площадках','несанкционированный доступ после закрытия']},
'ohrana-biznes-centrov':{
'intro':['Бизнес-центр требует сочетать безопасность с удобным проходом сотрудников, арендаторов, гостей, курьеров и подрядчиков.','Охрана контролирует лобби, служебные входы, общие зоны, парковку и соблюдение установленного пропускного режима.'],
'risks':['проход посторонних лиц','несогласованный доступ к арендаторам','кражи в общих и служебных зонах','конфликты на ресепшен и парковке','нарушения режима в вечернее и ночное время']},
'ohrana-gostinic':{
'intro':['В гостинице охрана должна быть заметной для нарушителя, но корректной и ненавязчивой для гостей.','Ключевые зоны — вход, лобби, служебные помещения, парковка, коридоры и площадки проведения мероприятий.'],
'risks':['конфликты с гостями или посетителями','проход посторонних в жилую часть','кражи имущества','нарушения в ночное время','несанкционированный доступ в служебные зоны']},
'ohrana-avtosalonov':{
'intro':['Автосалон объединяет дорогостоящее имущество, ключи, автомобили на открытых площадках, шоурум, сервисную зону и поток посетителей.','Охрана контролирует доступ, перемещение автомобилей и режим объекта как в рабочее, так и в ночное время.'],
'risks':['несанкционированный доступ к автомобилям и ключам','кражи имущества из шоурума или сервиса','проникновение на парковку ночью','конфликты с посетителями','несогласованный выезд транспорта']},
'ohrana-azs':{
'intro':['АЗС работает с постоянным потоком посетителей и транспорта, поэтому охрана должна быстро реагировать на конфликтные и тревожные ситуации.','Формат охраны подбирается с учётом круглосуточного режима, расположения станции и требований к технической безопасности.'],
'risks':['конфликты с посетителями','кражи из торговой зоны','угрозы персоналу в ночное время','проникновение в служебные помещения','повреждение имущества и оборудования']},
'ohrana-restoranov':{
'intro':['Охрана ресторана должна поддерживать безопасность гостей и персонала, не мешая атмосфере заведения.','Особое внимание уделяется входной группе, вечерним и ночным часам, конфликтным ситуациям и закрытию объекта.'],
'risks':['конфликты между посетителями','агрессивное поведение','кражи имущества гостей или заведения','проход в служебные помещения','риски при закрытии объекта']},
'ohrana-nochnyh-klubov':{
'intro':['Для ночного клуба или бара ключевыми задачами становятся входной контроль, предупреждение конфликтов и быстрое реагирование внутри площадки.','Состав смены определяется вместимостью, графиком, форматом мероприятий и требованиями администрации.'],
'risks':['конфликты между посетителями','пронос запрещённых предметов по правилам объекта','агрессивное поведение','несанкционированный доступ в служебные зоны','скопление людей у входа']},
'ohrana-lombardov':{
'intro':['Ломбард и ювелирный магазин требуют повышенного внимания к материальным ценностям, входной зоне, витринам, кассе и тревожному реагированию.','Физическая охрана рассматривается вместе с техническими средствами безопасности и заранее согласованным алгоритмом действий при тревоге.'],
'risks':['попытки хищения ценностей','угрозы сотрудникам','несанкционированный доступ в служебные зоны','разбойные риски','проникновение вне рабочего времени']},
'ohrana-bukmekerskih-kontor':{
'intro':['Пункт приёма ставок требует контроля посетительской зоны, защиты персонала и предупреждения конфликтных ситуаций.','Охрана подбирается с учётом графика работы, потока посетителей, кассовой зоны и расположения объекта.'],
'risks':['конфликты с посетителями','угрозы персоналу','нарушение порядка в клиентской зоне','несанкционированный доступ к служебным помещениям','риски в вечерние и ночные часы']}
}

INCLUDED=['физический пост и пропускной режим','контроль ключевых зон объекта','обходы и патрулирование по регламенту','пультовая охрана и тревожная сигнализация — по задаче','взаимодействие с ГБР при тревожном событии']

def render(text:str)->str:
    for k,v in SITE.items(): text=text.replace('{{site.%s}}'%k,str(v))
    return text

def partial(name:str)->str:
    out=render((SRC/'partials'/name).read_text(encoding='utf-8'))
    if name=='footer.html':
        out=out.replace('Лицензированное ЧОП — профессиональная охрана объектов и людей с 2018 года.','Лицензированное ЧОО — профессиональная охрана объектов и людей. Опыт команды — с 2007 года.')
        out=out.replace('ООО ЧОП «Рускорпорация»','ООО ЧОО «Рускорпорация»').replace('ООО ЧОП «Рускорпорация охрана и консалтинг»','ООО ЧОО «Рускорпорация охрана и консалтинг»')
    return out

def image_block(item:dict)->str:
    rel=item['image']
    p=ROOT/rel.lstrip('/')
    alt=f"{item['name']} — ЧОО «Рускорпорация»"
    if p.exists():
        return f'<figure class="service-photo-slot"><img src="{rel}" alt="{alt}" width="1200" height="800" loading="eager" decoding="async"></figure>'
    return f'<figure class="service-photo-slot" data-image-file="{rel}" aria-label="Место для тематического изображения"><span>Файл изображения: {rel.split("/")[-1]}</span></figure>'

def schema(item:dict,profile:dict)->str:
    url=SITE['site_url']+item['url']
    faq=[
      {'@type':'Question','name':f"Сколько стоит {item['name'].lower()}?",'acceptedAnswer':{'@type':'Answer','text':f"{item['price']}. Итоговая стоимость зависит от режима, количества постов, площади и дополнительных задач."}},
      {'@type':'Question','name':'Можно ли организовать круглосуточный пост?','acceptedAnswer':{'@type':'Answer','text':'Да. Режим и состав смены определяются после оценки объекта и требований заказчика.'}},
      {'@type':'Question','name':'Можно ли подключить пультовую охрану и ГБР?','acceptedAnswer':{'@type':'Answer','text':'Да. При необходимости физический пост дополняется пультовой охраной, тревожной сигнализацией и реагированием ГБР.'}},
      {'@type':'Question','name':'Что нужно для расчёта?','acceptedAnswer':{'@type':'Answer','text':'Адрес объекта, график работы, площадь, количество входов или КПП и основные задачи охраны.'}},
      {'@type':'Question','name':'Можно ли использовать видеонаблюдение и СКУД?','acceptedAnswer':{'@type':'Answer','text':'Да. Технические средства безопасности включаются в схему охраны по задаче и после обследования объекта.'}}
    ]
    graph={
      '@context':'https://schema.org','@graph':[
        {'@type':'LocalBusiness','@id':SITE['site_url']+'/#organization','name':SITE['name'],'legalName':SITE['legal_name'],'url':SITE['site_url'],'telephone':SITE['phone'],'email':SITE['email']},
        {'@type':'Service','@id':url+'#service','name':item['name'],'serviceType':item['name'],'areaServed':['Москва','Московская область'],'provider':{'@id':SITE['site_url']+'/#organization'},'url':url},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Главная','item':SITE['site_url']+'/'},{'@type':'ListItem','position':2,'name':'Услуги','item':SITE['site_url']+'/uslugi/'},{'@type':'ListItem','position':3,'name':GROUP['title'],'item':SITE['site_url']+GROUP['url']},{'@type':'ListItem','position':4,'name':item['name'],'item':url}]},
        {'@type':'FAQPage','mainEntity':faq}
      ]}
    return json.dumps(graph,ensure_ascii=False,separators=(',',':'))

def faq_html(item):
    rows=[
      (f"Сколько стоит {item['name'].lower()}?",f"{item['price']}. Итоговая стоимость зависит от режима, количества постов, площади и дополнительных задач."),
      ('Можно ли организовать круглосуточный пост?','Да. Режим и состав смены определяются после оценки объекта и требований заказчика.'),
      ('Можно ли подключить пультовую охрану и ГБР?','Да. При необходимости физический пост дополняется пультовой охраной, тревожной сигнализацией и реагированием ГБР.'),
      ('Что нужно для расчёта?','Адрес объекта, график работы, площадь, количество входов или КПП и основные задачи охраны.'),
      ('Можно ли использовать видеонаблюдение и СКУД?','Да. Технические средства безопасности включаются в схему охраны по задаче и после обследования объекта.')]
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in rows)

def page(item):
    slug=item['url'].strip('/').split('/')[-1]
    p=PROFILES[slug]
    title=f"{item['name']} в Москве и МО — ЧОО «Рускорпорация»"
    desc=f"{item['name']} в Москве и Московской области. Физический пост, пропускной режим, пультовая охрана и ГБР. Расчёт под задачи объекта."
    risks=''.join(f'<li>{x}</li>' for x in p['risks'])
    included=''.join(f'<li>{x}</li>' for x in INCLUDED)
    sibling=''.join(f'<a href="{x["url"]}">{x["name"]}</a>' for x in GROUP['services'] if x['url']!=item['url'])
    intro=''.join(f'<p class="service-lead">{x}</p>' for x in p['intro'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>
{partial('head-common.html')}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE['site_url']}{item['url']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE['site_url']}{item['url']}">
<script type="application/ld+json">{schema(item,p)}</script><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head>
<body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}
<main class="service-page"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><a href="{GROUP['url']}">{GROUP['title']}</a><span>/</span><b>{item['name']}</b></nav>
<section class="service-hero"><div><span class="service-kicker">Коммерческие объекты</span><h1>{item['name']} в Москве и Московской области</h1>{intro}<div class="service-actions"><a class="btn btn-gold" href="#request">Рассчитать стоимость</a><a class="btn btn-line" href="/kontakty/">Связаться</a></div></div>{image_block(item)}</section>
<section class="service-section"><h2>Основные риски объекта</h2><div class="service-grid"><article class="service-card"><h3>Что контролируем</h3><ul class="service-list">{risks}</ul></article><article class="service-card"><h3>Что входит в услугу</h3><ul class="service-list">{included}</ul></article></div></section>
<section class="service-section"><h2>Стоимость охраны</h2><div class="service-card"><div class="service-price">{item['price']}</div><p class="service-note">Цена является ориентиром. Итоговая стоимость зависит от режима, количества постов и сотрудников, площади, периметра, количества входов и дополнительных задач.</p><div class="service-actions"><a class="btn btn-gold" href="#request">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Все тарифы</a></div></div></section>
<section class="service-section"><h2>Практическая конфигурация</h2><div class="service-card"><p>Для этого типа объекта схема охраны формируется после обследования и уточнения режима работы, точек доступа и задач заказчика. Реальный кейс с цифрами публикуем только после подтверждения фактических данных.</p></div></section>
<section class="service-section"><h2>Почему ЧОО «Рускорпорация»</h2><div class="service-grid"><article class="service-card"><h3>Лицензия</h3><p>Лицензия {SITE['license']}.</p></article><article class="service-card"><h3>Комплексный подход</h3><p>Физическая охрана, пульт, технические средства и реагирование объединяются в одну схему под объект.</p></article><article class="service-card"><h3>Ответственность</h3><p>Условия ответственности и страхования фиксируются в договорных документах для конкретного проекта.</p></article><article class="service-card"><h3>Круглосуточный контроль</h3><p>При необходимости подключается пультовая охрана и реагирование ГБР.</p></article></div></section>
<section class="service-section"><h2>Частые вопросы</h2><div class="service-faq">{faq_html(item)}</div></section>
<section class="service-section"><h2>Смотрите также</h2><div class="service-links"><a href="/fizicheskaya-ohrana/">Физическая охрана</a><a href="/ohrana-pult/">Пультовая охрана</a><a href="/stati/">Статьи о безопасности</a>{sibling[:0]}</div><div class="service-links" style="margin-top:12px">{sibling}</div></section>
<section class="service-section" id="request"><h2>Получить расчёт</h2><form class="service-form" action="{SITE['formspree_url']}" method="POST"><div class="service-form-grid"><input name="name" required placeholder="Ваше имя"><input name="phone" required inputmode="tel" placeholder="Телефон"><textarea class="full" name="message" placeholder="Адрес объекта, график, количество входов и задачи"></textarea><label class="service-consent full"><input type="checkbox" required> <span>Согласен на обработку персональных данных.</span></label><div class="full"><button class="btn btn-gold" type="submit">Отправить заявку</button></div></div></form></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def group_hub():
    cards=''.join(f'<a class="service-hub-card" href="{i["url"]}"><b>{i["name"]}</b><span>{i["price"]}</span></a>' for i in GROUP['services'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{GROUP['title']} в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Охрана коммерческих объектов в Москве и МО: склады, магазины, офисы, банки, ТЦ, бизнес-центры, гостиницы, АЗС и другие объекты."><link rel="canonical" href="{SITE['site_url']}{GROUP['url']}"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><b>{GROUP['title']}</b></nav><span class="service-kicker">Группа A</span><h1>{GROUP['title']} в Москве и Московской области</h1><p class="service-lead">Склады, магазины, офисы, банки, торговые и бизнес-центры, гостиницы, автосалоны, АЗС, рестораны и другие объекты бизнеса.</p><section class="service-section"><div class="service-hub-grid">{cards}</div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def root_hub():
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>Услуги охраны в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Каталог услуг ЧОО «Рускорпорация»: физическая и пультовая охрана, охрана коммерческих, жилых, социальных и специальных объектов."><link rel="canonical" href="{SITE['site_url']}/uslugi/"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><b>Услуги</b></nav><span class="service-kicker">Каталог</span><h1>Услуги ЧОО «Рускорпорация»</h1><p class="service-lead">Новые направления добавляем по блокам, сохраняя существующие рабочие URL и общий дизайн сайта.</p><section class="service-section"><div class="service-hub-grid"><a class="service-hub-card" href="{GROUP['url']}"><b>Коммерческие объекты</b><span>13 направлений — блок A</span></a><a class="service-hub-card" href="/fizicheskaya-ohrana/"><b>Физическая охрана</b><span>Существующий раздел</span></a><a class="service-hub-card" href="/ohrana-pult/"><b>Пультовая охрана</b><span>Существующий раздел</span></a><div class="service-hub-card"><b>Жилая недвижимость</b><span>Следующий блок</span></div><div class="service-hub-card"><b>Социальные объекты</b><span>Следующий блок</span></div><div class="service-hub-card"><b>Специальные объекты</b><span>Следующий блок</span></div></div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def append_sitemap(urls):
    p=ROOT/'sitemap.xml'; txt=p.read_text(encoding='utf-8')
    add=[]
    for u in urls:
        loc=SITE['site_url']+u
        if f'<loc>{loc}</loc>' in txt: continue
        add.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    if add: txt=txt.replace('</urlset>',''.join(add)+'</urlset>'); p.write_text(txt,encoding='utf-8')

def main():
    css=(ROOT/'css'/'service-pages.css')
    if not css.exists(): raise SystemExit('css/service-pages.css is required')
    (ROOT/'uslugi').mkdir(exist_ok=True)
    (ROOT/'uslugi'/'index.html').write_text(root_hub(),encoding='utf-8')
    gp=ROOT/GROUP['url'].strip('/'); gp.mkdir(parents=True,exist_ok=True); (gp/'index.html').write_text(group_hub(),encoding='utf-8')
    urls=['/uslugi/',GROUP['url']]
    for item in GROUP['services']:
        out=ROOT/item['url'].strip('/'); out.mkdir(parents=True,exist_ok=True); (out/'index.html').write_text(page(item),encoding='utf-8'); urls.append(item['url'])
    append_sitemap(urls)
    print('Generated',len(GROUP['services']),'service pages + hubs')
if __name__=='__main__': main()
