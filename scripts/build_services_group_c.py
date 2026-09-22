#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'site-src'
SITE=json.loads((SRC/'site.json').read_text(encoding='utf-8'))
GROUP=json.loads((SRC/'services-group-c.json').read_text(encoding='utf-8'))

PROFILES={
'ohrana-shkol-detsadov':{
'intro':['Школы и детские сады требуют строгого контроля доступа, понятного порядка допуска посетителей и повышенного внимания к безопасности детей и сотрудников.','Схема охраны учитывает расписание, входные группы, работу подрядчиков, массовые мероприятия и требования администрации объекта.'],
'risks':['проход посторонних без согласования','конфликтные ситуации у входа или внутри объекта','угрозы безопасности детей и персонала','несанкционированный доступ в служебные помещения','повреждение имущества и нарушения установленного режима']},
'ohrana-vuzov':{
'intro':['ВУЗы сочетают большой поток студентов, преподавателей, гостей и подрядчиков с учебными, административными и техническими зонами.','Охрана помогает поддерживать пропускной режим, контролировать ключевые точки доступа и реагировать на нарушения порядка.'],
'risks':['проход посторонних в учебные корпуса','конфликты в местах массового пребывания','несанкционированный доступ в служебные и технические зоны','кражи имущества и оборудования','нарушения режима во время мероприятий и в вечернее время']},
'ohrana-bolnic':{
'intro':['Больницы и медицинские центры работают с постоянным потоком пациентов и посетителей, поэтому охрана должна сочетать контроль доступа с корректным отношением к людям.','Особое внимание уделяется входным группам, служебным помещениям, оборудованию, ночному режиму и конфликтным ситуациям.'],
'risks':['конфликтные ситуации с посетителями','несанкционированный доступ в служебные зоны','кражи оборудования и имущества','нарушения порядка в ночное время','попытки прохода в помещения с ограниченным доступом']},
'ohrana-muzeev':{
'intro':['Музеи и галереи требуют одновременно защищать экспонаты, посетителей, служебные помещения и инфраструктуру объекта.','Посты и маршруты охраны формируются с учётом выставочных залов, входных групп, фондовых помещений и мероприятий.'],
'risks':['хищение или повреждение экспонатов','нарушение правил посетителями','несанкционированный доступ в служебные и фондовые зоны','проникновение вне рабочего времени','риски во время выставок и массовых мероприятий']},
'ohrana-bibliotek':{
'intro':['Библиотека — открытое общественное пространство с читальными залами, фондами, техникой и служебными помещениями.','Охрана помогает контролировать порядок, доступ в закрытые зоны и сохранность имущества, не мешая посетителям.'],
'risks':['повреждение или хищение имущества','конфликты в общественных зонах','несанкционированный доступ в фонды и служебные помещения','проникновение после закрытия','нарушение правил доступа посетителями']},
'ohrana-teatrov':{
'intro':['Театры и кинотеатры работают с большими потоками посетителей и имеют зрительские, служебные, технические и закулисные зоны.','Охрана подбирается под расписание сеансов и спектаклей, мероприятия, количество входов и особенности площадки.'],
'risks':['конфликты и нарушения порядка','проход без разрешения в служебные и закулисные зоны','скопление людей у входов','кражи имущества посетителей или организации','нарушения режима во время мероприятий и после закрытия']},
'ohrana-hramov':{
'intro':['Храмы и религиозные объекты открыты для большого количества посетителей и требуют деликатного, но устойчивого режима безопасности.','Охрана контролирует входные зоны, порядок во время служб и мероприятий, а также доступ в служебные помещения.'],
'risks':['кражи пожертвований и имущества','конфликтные ситуации среди посетителей','несанкционированный доступ в служебные зоны','вандализм и повреждение имущества','нарушения порядка во время массовых служб']},
'ohrana-kladbish':{
'intro':['Кладбища и мемориальные территории имеют большую площадь, открытый периметр, транспортные въезды и участки, удалённые от постов.','Охрана может включать контроль въезда, обходы, патрулирование и видеонаблюдение на ключевых участках.'],
'risks':['вандализм и повреждение объектов','хищение имущества и материалов','несанкционированный въезд транспорта','проникновение на территорию в закрытые часы','конфликтные ситуации на территории']},
'ohrana-gosuchrezhdeniy':{
'intro':['Государственные учреждения требуют чёткого пропускного режима, контроля посетителей и защиты служебных зон и имущества.','Состав охраны определяется режимом объекта, количеством входов, потоком посетителей и требованиями заказчика.'],
'risks':['несанкционированный проход','конфликтные ситуации с посетителями','доступ в помещения с ограниченным режимом','кражи документов, техники и имущества','проникновение вне рабочего времени']}
}

INCLUDED=['физический пост и контроль входной группы','пропускной режим для посетителей, персонала и подрядчиков','обходы и контроль ключевых зон по регламенту','пультовая охрана и тревожная сигнализация — при необходимости','видеонаблюдение, СКУД и взаимодействие с ГБР — по задаче объекта']

def render(text:str)->str:
    for k,v in SITE.items():
        text=text.replace('{{site.%s}}'%k,str(v))
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
      (f"Сколько стоит {item['name'].lower()}?",f"{item['price']}. Итоговая стоимость зависит от режима, количества постов, площади, числа входов и дополнительных задач."),
      ('Можно ли организовать круглосуточный пост?','Да. Режим и состав смены определяются после обследования объекта и согласования требований заказчика.'),
      ('Можно ли подключить тревожную кнопку и ГБР?','Да. Пультовая охрана, тревожная сигнализация и реагирование ГБР могут дополнять физический пост.'),
      ('Можно ли подключить видеонаблюдение и СКУД?','Да. Технические средства безопасности включаются в схему после обследования объекта и согласования задач.'),
      ('Что нужно для расчёта стоимости?','Адрес, режим работы, площадь, количество входов, поток посетителей и основные задачи охраны.')
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
    desc=f"{item['name']} в Москве и Московской области. Пропускной режим, физическая и пультовая охрана, видеонаблюдение и ГБР. Расчёт под объект."
    risks=''.join(f'<li>{x}</li>' for x in p['risks'])
    included=''.join(f'<li>{x}</li>' for x in INCLUDED)
    siblings=''.join(f'<a href="{x["url"]}">{x["name"]}</a>' for x in GROUP['services'] if x['url']!=item['url'])
    intro=''.join(f'<p class="service-lead">{x}</p>' for x in p['intro'])
    extra='<a href="/ohrana-shkol/">Охрана школ — существующая страница</a>' if slug=='ohrana-shkol-detsadov' else ''
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>\n{partial('head-common.html')}\n<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE['site_url']}{item['url']}">\n<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE['site_url']}{item['url']}">\n<script type="application/ld+json">{schema(item)}</script><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head>\n<body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}\n<main class="service-page"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><a href="{GROUP['url']}">{GROUP['title']}</a><span>/</span><b>{item['name']}</b></nav>\n<section class="service-hero"><div><span class="service-kicker">Социальные объекты</span><h1>{item['name']} в Москве и Московской области</h1>{intro}<div class="service-actions"><a class="btn btn-gold" href="#request">Рассчитать стоимость</a><a class="btn btn-line" href="/kontakty/">Связаться</a></div></div>{image_block(item)}</section>\n<section class="service-section"><h2>Основные риски объекта</h2><div class="service-grid"><article class="service-card"><h3>Что контролируем</h3><ul class="service-list">{risks}</ul></article><article class="service-card"><h3>Что входит в услугу</h3><ul class="service-list">{included}</ul></article></div></section>\n<section class="service-section"><h2>Стоимость охраны</h2><div class="service-card"><div class="service-price">{item['price']}</div><p class="service-note">Итоговая стоимость зависит от режима, количества постов, входов, потока посетителей, технического оснащения и дополнительных задач.</p><div class="service-actions"><a class="btn btn-gold" href="#request">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Все тарифы</a></div></div></section>\n<section class="service-section"><h2>Практическая конфигурация</h2><div class="service-card"><p>Схема охраны формируется после обследования объекта и уточнения режима работы, точек доступа и требований заказчика. Реальный кейс с цифрами публикуем только после подтверждения фактических данных.</p></div></section>\n<section class="service-section"><h2>Почему ЧОО «Рускорпорация»</h2><div class="service-grid"><article class="service-card"><h3>Лицензия</h3><p>Лицензия {SITE['license']}.</p></article><article class="service-card"><h3>Комплексный подход</h3><p>Физическая охрана, пульт, видеонаблюдение, СКУД и реагирование объединяются в единую схему под объект.</p></article><article class="service-card"><h3>Ответственность</h3><p>Условия ответственности и страхования фиксируются в договорных документах для конкретного проекта.</p></article><article class="service-card"><h3>Круглосуточный контроль</h3><p>При необходимости подключается пультовая охрана и реагирование ГБР.</p></article></div></section>\n<section class="service-section"><h2>Частые вопросы</h2><div class="service-faq">{faq_html(item)}</div></section>\n<section class="service-section"><h2>Смотрите также</h2><div class="service-links"><a href="/fizicheskaya-ohrana/">Физическая охрана</a><a href="/ohrana-pult/">Пультовая охрана</a><a href="/stati/">Статьи о безопасности</a><a href="/kontakty/">Контакты</a>{extra}</div><div class="service-links" style="margin-top:12px">{siblings}</div></section>\n<section class="service-section" id="request"><h2>Получить расчёт</h2><form class="service-form" action="{SITE['formspree_url']}" method="POST"><div class="service-form-grid"><input name="name" required placeholder="Ваше имя"><input name="phone" required inputmode="tel" placeholder="Телефон"><textarea class="full" name="message" placeholder="Адрес объекта, режим работы, количество входов и задачи"></textarea><label class="service-consent full"><input type="checkbox" required> <span>Согласен на обработку персональных данных.</span></label><div class="full"><button class="btn btn-gold" type="submit">Отправить заявку</button></div></div></form></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def group_hub()->str:
    cards=''.join(f'<a class="service-hub-card" href="{i["url"]}"><b>{i["name"]}</b><span>{i["price"]}</span></a>' for i in GROUP['services'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{GROUP['title']} в Москве и МО — ЧОО «Рускорпорация»</title><meta name="description" content="Охрана социальных объектов в Москве и МО: школы, детские сады, ВУЗы, больницы, музеи, библиотеки, театры, храмы и госучреждения."><link rel="canonical" href="{SITE['site_url']}{GROUP['url']}"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><b>{GROUP['title']}</b></nav><span class="service-kicker">Группа C</span><h1>{GROUP['title']} в Москве и Московской области</h1><p class="service-lead">Школы, детские сады, ВУЗы, медицинские учреждения, музеи, библиотеки, театры, храмы, кладбища и государственные учреждения.</p><section class="service-section"><div class="service-hub-grid">{cards}</div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''

def patch_root_hub():
    p=ROOT/'uslugi'/'index.html'; txt=p.read_text(encoding='utf-8')
    link='<a class="service-hub-card" href="/uslugi/ohrana-socialnyh-obektov/"><b>Социальные объекты</b><span>9 направлений — блок C</span></a>'
    if link in txt:
        return
    old='<div class="service-hub-card"><b>Социальные объекты</b><span>Следующий блок</span></div>'
    if old not in txt:
        raise SystemExit('Expected social placeholder not found in uslugi/index.html; refusing broad rewrite')
    p.write_text(txt.replace(old,link,1),encoding='utf-8')

def append_sitemap(urls):
    p=ROOT/'sitemap.xml'; txt=p.read_text(encoding='utf-8'); add=[]
    for u in urls:
        loc=SITE['site_url']+u
        if f'<loc>{loc}</loc>' in txt:
            continue
        add.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    if add:
        if '</urlset>' not in txt:
            raise SystemExit('sitemap.xml missing closing urlset; refusing rewrite')
        p.write_text(txt.replace('</urlset>',''.join(add)+'</urlset>',1),encoding='utf-8')

def main():
    if not (ROOT/'css'/'service-pages.css').exists():
        raise SystemExit('css/service-pages.css is required')
    patch_root_hub()
    gp=ROOT/GROUP['url'].strip('/'); gp.mkdir(parents=True,exist_ok=True); (gp/'index.html').write_text(group_hub(),encoding='utf-8')
    urls=[GROUP['url']]
    for item in GROUP['services']:
        out=ROOT/item['url'].strip('/'); out.mkdir(parents=True,exist_ok=True); (out/'index.html').write_text(page(item),encoding='utf-8'); urls.append(item['url'])
    append_sitemap(urls)
    print('Generated',len(GROUP['services']),'social service pages + hub')

if __name__=='__main__':
    main()
