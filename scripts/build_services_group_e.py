#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from services_catalog import image_block as catalog_image, root_hub as catalog_root, finish_group, finish_page

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'site-src'
SITE = json.loads((SRC / 'site.json').read_text(encoding='utf-8'))
GROUP = json.loads((SRC / 'services-group-e.json').read_text(encoding='utf-8'))

PROFILES = {
'pozharnaya-bezopasnost': {
'intro': ['Пожарная безопасность объекта строится на раннем обнаружении тревожных событий, исправной сигнализации и понятном алгоритме передачи сигнала ответственным лицам.', 'Технические решения подбираются после обследования объекта и могут интегрироваться с другими системами безопасности.'],
'risks': ['позднее обнаружение задымления или возгорания', 'неисправность или отсутствие контроля состояния сигнализации', 'несогласованное реагирование персонала на тревожный сигнал', 'отсутствие единого мониторинга технических систем', 'риски для имущества и непрерывности работы объекта'],
'included': ['обследование объекта и постановка задачи', 'подбор и интеграция технических средств пожарной сигнализации', 'контроль передачи тревожных сигналов — по проекту', 'сопряжение с другими системами безопасности — при необходимости', 'регламент уведомления ответственных лиц и дальнейших действий']},
'videonablyudenie': {
'intro': ['Видеонаблюдение помогает контролировать ключевые зоны объекта, фиксировать события и дополнять работу физической и пультовой охраны.', 'Состав камер и точки установки определяются после обследования, с учётом освещения, периметра, входов и задач заказчика.'],
'risks': ['слепые зоны на территории', 'невозможность подтвердить обстоятельства инцидента', 'несанкционированный доступ в контролируемые зоны', 'отсутствие удалённого визуального контроля', 'неэффективное размещение камер без учёта реальных рисков'],
'included': ['обследование и схема зон наблюдения', 'подбор камер и оборудования под задачу', 'настройка записи и хранения видео', 'удалённый просмотр и мониторинг — по проекту', 'интеграция с охранной сигнализацией и СКУД — при необходимости']},
'kontrol-dostupa-skud': {
'intro': ['СКУД позволяет управлять доступом сотрудников, посетителей и подрядчиков и фиксировать проходы через контролируемые точки.', 'Система может работать отдельно или вместе с видеонаблюдением, турникетами, шлагбаумами и физическим постом охраны.'],
'risks': ['проход посторонних лиц', 'доступ сотрудников в закрытые зоны', 'отсутствие учёта проходов и посещений', 'несогласованный въезд транспорта', 'потеря контроля над ключами и физическими пропусками'],
'included': ['обследование точек доступа', 'подбор контроллеров, считывателей и исполнительных устройств', 'настройка уровней и правил доступа', 'учёт событий прохода и доступа', 'интеграция с турникетами, шлагбаумами, видео и охраной — по проекту']},
'autsorsing-sluzhby-bezopasnosti': {
'intro': ['Аутсорсинг службы безопасности позволяет передать внешнему подрядчику организацию охраны, контроль постов, регламенты и часть функций внутренней безопасности.', 'Объём ответственности определяется задачами заказчика и фиксируется в договоре и рабочей документации.'],
'risks': ['разрозненная работа постов и подрядчиков', 'отсутствие единых регламентов', 'слабый контроль дисциплины и отчётности', 'неясное распределение ответственности', 'затраты на содержание собственной службы без необходимой загрузки'],
'included': ['аудит действующей системы безопасности', 'проектирование структуры постов и регламентов', 'организация контроля качества охраны', 'координация физической и технической защиты', 'отчётность и взаимодействие с ответственными представителями заказчика']},
'voditel-telohranitel': {
'intro': ['Водитель-телохранитель совмещает транспортное сопровождение с задачами личной безопасности в рамках согласованного маршрута и режима работы.', 'Формат услуги определяется после уточнения графика, требований к автомобилю, географии поездок и задач заказчика.'],
'risks': ['непредвиденные ситуации в пути', 'нарушение приватности и конфиденциальности', 'несогласованное изменение маршрута или графика', 'риски при посадке и высадке', 'необходимость постоянного сопровождения в течение рабочего дня'],
'included': ['персональное транспортное сопровождение', 'согласование графика и маршрутов', 'контроль обстановки в рамках обязанностей охраны', 'конфиденциальность информации о поездках', 'координация с другими сотрудниками охраны — при необходимости']},
'vip-ohrana': {
'intro': ['VIP-охрана организуется индивидуально с учётом графика, публичности, поездок, мероприятий и требований к конфиденциальности.', 'Состав группы и формат сопровождения определяются после оценки задач и условий работы.'],
'risks': ['повышенное внимание посторонних лиц', 'риски на публичных мероприятиях', 'нарушение приватности', 'непредвиденные ситуации при перемещениях', 'необходимость координации нескольких точек и участников'],
'included': ['индивидуальная схема сопровождения', 'согласование графика и ключевых точек', 'координация действий сотрудников охраны', 'конфиденциальность и минимальная заметность — по задаче', 'взаимодействие с охраной объекта или мероприятия']},
'vooruzhennaya-ohrana': {
'intro': ['Вооружённая охрана применяется только в случаях, когда это предусмотрено законом, лицензией и условиями конкретного объекта.', 'Формат услуги определяется после оценки рисков и правовых оснований; требования к сотрудникам и применяемым средствам устанавливаются действующим законодательством.'],
'risks': ['объекты с повышенной ценностью имущества', 'повышенные требования к защите отдельных зон', 'необходимость усиленного режима охраны', 'риски при круглосуточной работе объекта', 'необходимость строгого соблюдения специальных регламентов'],
'included': ['оценка задачи и законных оснований для формата охраны', 'подбор сотрудников с требуемой квалификацией', 'постовая служба по согласованному регламенту', 'контроль доступа и взаимодействие с пультом — по задаче', 'договорная фиксация режима и ответственности сторон']},
'ohrannik-vahter-kontroler': {
'intro': ['Для объектов с базовыми задачами контроля доступа может требоваться охранник, контролёр или вахтёр с понятным перечнем обязанностей.', 'Роль и полномочия сотрудника определяются требованиями объекта и действующим законодательством.'],
'risks': ['проход посторонних', 'отсутствие контроля входа и выхода', 'нарушение внутреннего режима объекта', 'несогласованный доступ подрядчиков и посетителей', 'необходимость регистрации событий и обращений'],
'included': ['контроль входной группы или проходной', 'регистрация посетителей — по регламенту', 'проверка пропусков и соблюдения режима', 'информирование ответственных лиц о нарушениях', 'ведение установленной заказчиком отчётности']},
'konsyerzh-servis': {
'intro': ['Консьерж-сервис подходит жилым комплексам, бизнес-центрам и другим объектам, где важны контроль входной группы, порядок и помощь посетителям.', 'Функции консьержа согласуются отдельно и не подменяют специальные полномочия лицензированной физической охраны.'],
'risks': ['отсутствие контроля входной группы', 'неорганизованный поток гостей и курьеров', 'нарушения порядка в общих зонах', 'несогласованный доступ подрядчиков', 'отсутствие единой точки связи для жителей или арендаторов'],
'included': ['присутствие сотрудника на входной группе', 'встреча и информирование посетителей', 'регистрация обращений и событий — по регламенту', 'контроль порядка в зоне ответственности', 'оперативная связь с управляющей компанией или ответственными лицами']}
}


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


def image_block(item):
    return catalog_image(item, GROUP)

def faq_items(item: dict):
    return [
        (f"Сколько стоит услуга «{item['name']}»?", f"{item['price']}. Итоговая стоимость зависит от объёма работ, режима, технического оснащения и дополнительных задач."),
        ('Можно ли объединить услугу с физической охраной?', 'Да. Дополнительные услуги могут быть частью комплексной схемы безопасности объекта.'),
        ('Можно ли подключить пультовую охрану и ГБР?', 'Да, если это соответствует задаче и выбранной конфигурации объекта.'),
        ('Нужно ли обследование объекта?', 'Для большинства технических и комплексных решений обследование позволяет корректно определить состав работ и оборудования.'),
        ('Что нужно для расчёта?', 'Краткое описание объекта, адрес, режим работы и перечень задач, которые необходимо закрыть.')
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
    desc = f"{item['name']} в Москве и Московской области. Решение под задачи объекта, интеграция с физической и пультовой охраной. Индивидуальный расчёт."
    risks = ''.join(f'<li>{x}</li>' for x in p['risks'])
    included = ''.join(f'<li>{x}</li>' for x in p['included'])
    intro = ''.join(f'<p class="service-lead">{x}</p>' for x in p['intro'])
    siblings = ''.join(f'<a href="{x["url"]}">{x["name"]}</a>' for x in GROUP['services'] if x['url'] != item['url'])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>
{partial('head-common.html')}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{SITE['site_url']}{item['url']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE['site_url']}{item['url']}">
<script type="application/ld+json">{schema(item)}</script><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head>
<body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}
<main class="service-page"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><a href="{GROUP['url']}">{GROUP['title']}</a><span>/</span><b>{item['name']}</b></nav>
<section class="service-hero"><div><span class="service-kicker">Дополнительные услуги</span><h1>{item['name']} в Москве и Московской области</h1>{intro}<div class="service-actions"><a class="btn btn-gold" href="#request">Рассчитать стоимость</a><a class="btn btn-line" href="/kontakty/">Связаться</a></div></div>{image_block(item)}</section>
<section class="service-section"><h2>Основные задачи и риски</h2><div class="service-grid"><article class="service-card"><h3>Что учитываем</h3><ul class="service-list">{risks}</ul></article><article class="service-card"><h3>Что входит в услугу</h3><ul class="service-list">{included}</ul></article></div></section>
<section class="service-section"><h2>Стоимость</h2><div class="service-card"><div class="service-price">{item['price']}</div><p class="service-note">Итоговая стоимость зависит от объёма работ, режима, состава решения, технического оснащения и дополнительных требований.</p><div class="service-actions"><a class="btn btn-gold" href="#request">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Все тарифы</a></div></div></section>
<section class="service-section"><h2>Как формируется решение</h2><div class="service-card"><p>Конфигурация определяется после уточнения задач и, когда это необходимо, обследования объекта. Технические и организационные решения согласуются до запуска работ.</p></div></section>
<section class="service-section"><h2>Почему ЧОО «Рускорпорация»</h2><div class="service-grid"><article class="service-card"><h3>Опыт</h3><p>Опыт команды в сфере безопасности — с 2007 года.</p></article><article class="service-card"><h3>Комплексный подход</h3><p>Физическая охрана, пульт, технические средства и дополнительные услуги объединяются в единую схему под объект.</p></article><article class="service-card"><h3>Договор</h3><p>Объём работ, ответственность и границы услуги фиксируются в договорных документах.</p></article><article class="service-card"><h3>Интеграция</h3><p>При необходимости решение связывается с существующей системой безопасности заказчика.</p></article></div></section>
<section class="service-section"><h2>Частые вопросы</h2><div class="service-faq">{faq_html(item)}</div></section>
<section class="service-section"><h2>Смотрите также</h2><div class="service-links"><a href="/fizicheskaya-ohrana/">Физическая охрана</a><a href="/ohrana-pult/">Пультовая охрана</a><a href="/ohrana-fizicheskih-lic/">Охрана физических лиц</a><a href="/ohrana-meropriyatiy/">Охрана мероприятий</a></div><div class="service-links" style="margin-top:12px">{siblings}</div></section>
<section class="service-section" id="request"><h2>Получить расчёт</h2><form class="service-form" action="{SITE['formspree_url']}" method="POST"><div class="service-form-grid"><input name="name" required placeholder="Ваше имя"><input name="phone" required inputmode="tel" placeholder="Телефон"><textarea class="full" name="message" placeholder="Опишите объект и задачу"></textarea><label class="service-consent full"><input type="checkbox" required> <span>Согласен на обработку персональных данных.</span></label><div class="full"><button class="btn btn-gold" type="submit">Отправить заявку</button></div></div></form></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''


def group_hub() -> str:
    new_cards = ''.join(f'<a class="service-hub-card" href="{i["url"]}"><b>{i["name"]}</b><span>{i["price"]}</span></a>' for i in GROUP['services'])
    existing = ''.join([
        '<a class="service-hub-card" href="/fizicheskaya-ohrana/"><b>Физическая охрана</b><span>Существующий раздел</span></a>',
        '<a class="service-hub-card" href="/ohrana-pult/"><b>Пультовая охрана</b><span>Существующий раздел</span></a>',
        '<a class="service-hub-card" href="/ohrana-fizicheskih-lic/"><b>Охрана физических лиц</b><span>Существующий раздел</span></a>',
        '<a class="service-hub-card" href="/ohrana-meropriyatiy/"><b>Охрана мероприятий</b><span>Существующий раздел</span></a>'
    ])
    return f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{GROUP['title']} — ЧОО «Рускорпорация»</title><meta name="description" content="Дополнительные услуги безопасности в Москве и МО: видеонаблюдение, СКУД, аутсорсинг службы безопасности, VIP-охрана и другие направления."><link rel="canonical" href="{SITE['site_url']}{GROUP['url']}"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="{SITE['metrika_id']}"><div id="progress"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs"><a href="/">Главная</a><span>/</span><a href="/uslugi/">Услуги</a><span>/</span><b>{GROUP['title']}</b></nav><span class="service-kicker">Группа E</span><h1>{GROUP['title']}</h1><p class="service-lead">Технические и организационные решения, которые дополняют физическую и пультовую охрану и позволяют собрать комплексную систему безопасности под конкретный объект или человека.</p><section class="service-section"><h2>Основные разделы охраны</h2><div class="service-hub-grid">{existing}</div></section><section class="service-section"><h2>Дополнительные направления</h2><div class="service-hub-grid">{new_cards}</div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''


def update_root_hub():
    (ROOT / "uslugi/index.html").write_text(catalog_root(partial), encoding="utf-8")

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
    (gp / 'index.html').write_text(finish_group(group_hub(), GROUP), encoding='utf-8')
    urls = [GROUP['url']]
    for item in GROUP['services']:
        out = ROOT / item['url'].strip('/')
        out.mkdir(parents=True, exist_ok=True)
        (out / 'index.html').write_text(finish_page(page(item), GROUP), encoding='utf-8')
        urls.append(item['url'])
    update_root_hub()
    append_sitemap(urls)
    print('Generated', len(GROUP['services']), 'additional service pages + hub')


if __name__ == '__main__':
    main()

