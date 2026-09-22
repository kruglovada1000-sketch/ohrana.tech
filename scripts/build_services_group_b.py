#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'site-src'
SITE=json.loads((SRC/'site.json').read_text(encoding='utf-8'))
GROUP=json.loads((SRC/'services-group-b.json').read_text(encoding='utf-8'))

PROFILES={
'ohrana-zhk-tszh':{
'intro':['Жилой комплекс и ТСЖ требуют постоянного контроля входных групп, дворовой территории, парковки, технических помещений и работы подрядчиков.','Схема охраны строится так, чтобы поддерживать безопасность жителей без лишнего вмешательства в повседневную жизнь дома.'],
'risks':['проход посторонних в подъезды и закрытые зоны','кражи и повреждение имущества в общих помещениях','конфликты на территории и в местах общего пользования','несанкционированный въезд на парковку','проникновение в технические и служебные помещения']},
'ohrana-kottedzhnyh-poselkov':{
'intro':['Коттеджный посёлок или СНТ имеет протяжённый периметр, въездные группы, внутренние дороги и большое количество частных домов.','Охрана сочетает контроль КПП, патрулирование территории и технические средства безопасности с учётом режима проживания и сезонности.'],
'risks':['несанкционированный въезд транспорта','проникновение через периметр','кражи имущества с участков и из домов','нарушения порядка на общей территории','доступ посторонних подрядчиков и посетителей без согласования']},
'ohrana-dach-kottedzhey':{
'intro':['Частный дом или дача особенно уязвимы в периоды отсутствия владельцев и в ночное время.','Пультовая охрана, тревожная сигнализация, видеонаблюдение и выезд группы реагирования могут дополняться физическим постом при необходимости.'],
'risks':['проникновение в дом в отсутствие владельцев','кража имущества и оборудования','вандализм и повреждение территории','проникновение через ворота или ограждение','пожарные и технические тревоги при подключении соответствующих датчиков']},
'ohrana-garazhey':{
'intro':['Гаражный кооператив требует контроля въезда, сохранности автомобилей, имущества собственников и общих технических зон.','Режим охраны зависит от количества въездов, площади территории, графика доступа и наличия видеонаблюдения.'],
'risks':['угон или попытка доступа к автомобилям','кража имущества из гаражей','проникновение посторонних на территорию','несанкционированный въезд транспорта','вандализм и повреждение общего имущества']},
'ohrana-parkovok':{
'intro':['Парковка и автостоянка требуют контроля въезда и выезда, наблюдения за территорией и быстрого реагирования на конфликтные и тревожные ситуации.','Физический пост может сочетаться с видеонаблюдением, СКУД, шлагбаумами и регулярными обходами.'],
'risks':['угон и попытки доступа к автомобилям','повреждение транспортных средств','несанкционированный въезд','конфликты между посетителями','проникновение на территорию в нерабочее время']}
}

INCLUDED=['физический пост или контроль КПП — по задаче','контроль входных и въездных групп','обходы и патрулирование территории по регламенту','пультовая охрана и тревожная сигнализация — при необходимости','видеонаблюдение, СКУД и взаимодействие с ГБР — по схеме объекта']

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
    rel=item['image']; p=ROOT/rel.lstrip('/'); alt=f"{item['name']} — ЧОО «Рускорпорация»"
    if p.exists():
        return f'<figure class="service-photo-slot"><img src="{rel}" alt="{alt}" width="1200" height="800" loading="eager" decoding="async"></figure>'
    return f'<figure class="service-photo-slot" data-image-file="{rel}" aria-label="Место для тематического изображения"><span>Файл изображения: {rel.split("/")[-1]}</span></figure>'

def faq_items(item:dict):
    return [
      (f"Сколько стоит {item['name'].lower()}?",f"{item['price']}. Итоговая стоимость зависит от режима, площади, количества постов, точек доступа и дополнительных задач."),
      ('Можно ли организовать круглосуточную охрану?','Да. Режим и состав смены определяются после оценки объекта и требований заказчика.'),
      ('Можно ли подключить пультовую охрану и ГБР?','Да. При необходимости физическая охрана дополняется пультовой защитой, тревожной сигнализацией и реагированием ГБР.'),
      ('Можно ли подключить видеонаблюдение и СКУД?','Да. Технические средства безопасности включаются в схему после обследования объекта и согласования задач.'),
      ('Что нужно для расчёта стоимости?','Адрес, площадь, количество входов или въездов, режим работы и основные задачи охраны.')
    ]

def schema(item:dict)->str:
    url=SITE['site_url']+item['url']
    faq=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq_items(item)]
    graph={'@context':'https://schema.org','@graph':[
      {'@type':'LocalBusiness','@id':SITE['site_url']+'/#organization','name':SITE['name'],'legalName':SITE['legal_name'],'url':SITE['site_url'],'telephone':SITE['phone'],'email':SITE['email']},
      {'@type':'Service','@id':url+'#service','name':item['name'],'serviceType':item['name'],'areaServed':['Москва','Московская область'],'provider':{'@id':SITE['site_url']+'/#organization'},'url':url},
      {'@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':'Главная','item':SITE['site_url']+'/'},
        {'@type':'ListItem','position':2,'name':'Услуги','item':SITE['site_url']+'/uslugi/'},
        {'@type':'ListItem','position':3,'name':GROUP['title'],'item':SITE['site_url']+GROUP['url']},
        {'@type':'ListItem','position':4,'name':item['name'],'item':url}]},
      {'@type':'FAQPage','mainEntity':faq}]}
    return json.dumps(graph,ensure_ascii=False,separators=(',',':'))

def faq_html(item:dict)->str:
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faq_items(item))

def page(item:dict)->str:
    slug=item['url'].strip('/').split('/')[-1]; p=PROFILES[slug]
    title=f"{item['name']} в Москве и МО — ЧОО «Рускорпорация»"
    desc=f"{item['name']} в Москве и Московской области. Физическая и пультовая охрана, контроль доступа, видеонаблюдение и ГБР. Расчёт под объект."
    risks=''.join(f'<li>{x}</li>' for x in p['risks']); included=''.join(f'<li>{x}</li>' for x in INCLUDED)
    sibling=''.join(f'<a href="{x["url"]}">{x["name"]}</a>' for x in GROUP['services'] if x['url']!=item['url'])
    intro=''.join(f'<p class="service-lead">{x}</p>' for x in p['intro'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>
{partial('head-common.html')}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE['site_url']}{item['url']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE['site_url']}{item['url']}">
<script type="application/ld+json">{schema(item)}</script><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head>
<body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}
<main class="service-page"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><a href="{GROUP['url']}">{GROUP['title']}</a><span>/</span><b>{item['name']}</b></nav>
<section class="service-hero"><div><span class="service-kicker">Жилая недвижимость</span><h1>{item['name']} в Москве и Московской области</h1>{intro}<div class="service-actions"><a class="btn btn-gold" href="#request">Рассчитать стоимость</a><a class="btn btn-line" href="/kontakty/">Связаться</a></div></div>{image_block(item)}</section>
<section class="service-section"><h2>Основные риски объекта</h2><div class="service-grid"><article class="service-card"><h3>Что контролируем</h3><ul class="service-list">{risks}</ul></article><article class="service-card"><h3>Что входит в услугу</h3><ul class="service-list">{included}</ul></article></div></section>
<section class="service-section"><h2>Стоимость охраны</h2><div class="service-card"><div class="service-price">{item['price']}</div><p class="service-note">Итоговая стоимость зависит от режима, площади, количества постов, входов или въездов, технического оснащения и дополнительных задач.</p><div class="service-actions"><a class="btn btn-gold" href="#request">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Все тарифы</a></div></div></section>
<section class="service-section"><h2>Практическая конфигурация</h2><div class="service-card"><p>Схема охраны формируется после обследования территории и уточнения точек доступа, режима проживания или эксплуатации и задач заказчика. Реальный кейс с цифрами публикуем только после подтверждения фактических данных.</p></div></section>
<section class="service-section"><h2>Почему ЧОО «Рускорпорация»</h2><div class="service-grid"><article class="service-card"><h3>Лицензия</h3><p>Лицензия {SITE['license']}.</p></article><article class="service-card"><h3>Комплексный подход</h3><p>Физическая охрана, пульт, видеонаблюдение, СКУД и реагирование объединяются в единую схему под объект.</p></article><article class="service-card"><h3>Ответственность</h3><p>Условия ответственности и страхования фиксируются в договорных документах для конкретного проекта.</p></article><article class="service-card"><h3>Круглосуточный контроль</h3><p>При необходимости подключается пультовая охрана и реагирование ГБР.</p></article></div></section>
<section class="service-section"><h2>Частые вопросы</h2><div class="service-faq">{faq_html(item)}</div></section>
<section class="service-section"><h2>Смотрите также</h2><div class="service-links"><a href="/fizicheskaya-ohrana/">Физическая охрана</a><a href="/ohrana-pult/">Пультовая охрана</a><a href="/stati/">Статьи о безопасности</a><a href="/kontakty/">Контакты</a></div><div class="service-links" style="margin-top:12px">{sibling}</div></section>
<section class="service-section" id="request"><h2>Получить расчёт</h2><form class="service-form" action="{SITE['formspree_url']}" method="POST"><div class="service-form-grid"><input name="name" required placeholder="Ваше имя"><input name="phone" required inputmode="tel" placeholder="Телефон"><textarea class="full" name="message" placeholder="Адрес объекта, площадь, режим и задачи"></textarea><label class="service-consent full"><input type="checkbox" required> <span>Согласен на обработку персональных данных.</span></label><div class="full"><button class="btn btn-gold" type="submit">Отправить заявку</button></div></div></form></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def group_hub()->str:
    cards=''.join(f'<a class="service-hub-card" href="{i["url"]}"><b>{i["name"]}</b><span>{i["price"]}</span></a>' for i in GROUP['services'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{GROUP['title']} в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Охрана жилой недвижимости в Москве и МО: ЖК и ТСЖ, коттеджные поселки, дачи, гаражи, парковки и автостоянки."><link rel="canonical" href="{SITE['site_url']}{GROUP['url']}"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><b>{GROUP['title']}</b></nav><span class="service-kicker">Группа B</span><h1>{GROUP['title']} в Москве и Московской области</h1><p class="service-lead">Жилые комплексы, ТСЖ, коттеджные поселки, дачи, гаражи, парковки и автостоянки. Подбираем физическую и техническую защиту под конкретную территорию.</p><section class="service-section"><div class="service-hub-grid">{cards}</div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def root_hub()->str:
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>Услуги охраны в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Каталог услуг ЧОО «Рускорпорация»: физическая и пультовая охрана, охрана коммерческих, жилых, социальных и специальных объектов."><link rel="canonical" href="{SITE['site_url']}/uslugi/"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><b>Услуги</b></nav><span class="service-kicker">Каталог</span><h1>Услуги ЧОО «Рускорпорация»</h1><p class="service-lead">Направления собраны по группам. Существующие рабочие URL сохраняются, новые посадочные страницы развиваются внутри раздела «Услуги».</p><section class="service-section"><div class="service-hub-grid"><a class="service-hub-card" href="/uslugi/ohrana-kommercheskih-obektov/"><b>Коммерческие объекты</b><span>13 направлений — блок A</span></a><a class="service-hub-card" href="{GROUP['url']}"><b>Жилая недвижимость</b><span>5 направлений — блок B</span></a><a class="service-hub-card" href="/fizicheskaya-ohrana/"><b>Физическая охрана</b><span>Существующий раздел</span></a><a class="service-hub-card" href="/ohrana-pult/"><b>Пультовая охрана</b><span>Существующий раздел</span></a><div class="service-hub-card"><b>Социальные объекты</b><span>Следующий блок</span></div><div class="service-hub-card"><b>Специальные объекты</b><span>Следующий блок</span></div></div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def append_sitemap(urls):
    p=ROOT/'sitemap.xml'; txt=p.read_text(encoding='utf-8'); add=[]
    for u in urls:
        loc=SITE['site_url']+u
        if f'<loc>{loc}</loc>' in txt: continue
        add.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    if add: txt=txt.replace('</urlset>',''.join(add)+'</urlset>'); p.write_text(txt,encoding='utf-8')

def main():
    if not (ROOT/'css'/'service-pages.css').exists(): raise SystemExit('css/service-pages.css is required')
    (ROOT/'uslugi').mkdir(exist_ok=True)
    (ROOT/'uslugi'/'index.html').write_text(root_hub(),encoding='utf-8')
    gp=ROOT/GROUP['url'].strip('/'); gp.mkdir(parents=True,exist_ok=True); (gp/'index.html').write_text(group_hub(),encoding='utf-8')
    urls=[GROUP['url']]
    for item in GROUP['services']:
        out=ROOT/item['url'].strip('/'); out.mkdir(parents=True,exist_ok=True); (out/'index.html').write_text(page(item),encoding='utf-8'); urls.append(item['url'])
    append_sitemap(urls)
    print('Generated',len(GROUP['services']),'residential service pages + hub')
if __name__=='__main__': main()
