"""Shared catalogue presentation used by all five service generators."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [json.loads((ROOT / f'site-src/services-group-{letter}.json').read_text()) for letter in 'abcde']
LABELS = ['Коммерческие объекты', 'Жилая недвижимость', 'Социальные объекты', 'Специальные объекты', 'Дополнительные услуги']
IMAGES = ['commercial', 'residential', 'social', 'special', 'additional']
DESCRIPTIONS = [
    'Склады, офисы, магазины и бизнес-центры. Контроль доступа, имущества и рабочих процессов.',
    'Жилые комплексы, дома и посёлки. Спокойствие жителей, контроль въезда и обход территории.',
    'Образовательные, медицинские и культурные учреждения. Безопасность посетителей и персонала.',
    'Производство, стройплощадки и открытые территории. Контроль периметра, транспорта и имущества.',
    'Видеонаблюдение, СКУД, персональная защита и организационные решения под вашу задачу.',
]
ASSETS = '<link rel="stylesheet" href="/css/services-menu.css?v=20260923"><script src="/js/services-menu.js?v=20260923" defer></script>'

def menu():
    cards = ''.join(f'<a href="{g["url"]}"><strong>{LABELS[n]}</strong><span>{DESCRIPTIONS[n]}</span></a>' for n, g in enumerate(GROUPS))
    return ('<div class="services-nav"><a class="services-nav-link" href="/uslugi/">Услуги</a>'
            '<button class="services-nav-toggle" type="button" aria-label="Раскрыть направления услуг" aria-expanded="false" aria-controls="servicesPanel">'
            '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m3 6 5 5 5-5"/></svg></button>'
            '<div class="services-panel" id="servicesPanel" hidden>' + cards +
            '<a class="services-panel-all" href="/uslugi/"><strong>Все услуги →</strong><span>Подберите охрану для своего объекта</span></a></div></div>')

def navigation(text):
    if 'class="services-nav"' in text:
        return text
    # Only touch navigation inside the header, including the standalone home header.
    def patch_header(match):
        header = match[0]
        if '<a href="/uslugi/">Услуги</a>' not in header:
            if 'id="siteNav"' not in header:
                return header
            header=header.replace('<a href="/">Главная</a>', '<a href="/">Главная</a><a href="/uslugi/">Услуги</a>',1)
        header = header.replace('<a href="/uslugi/">Услуги</a>', menu(), 1)
        return header.replace('>', '>' + ASSETS, 1)
    return re.sub(r'<header\b[^>]*>[\s\S]*?</header>', patch_header, text, count=1)

def photo(group, loading='eager'):
    i = next(i for i,g in enumerate(GROUPS) if g['group'] == group['group'])
    return f'<figure class="service-photo-slot"><img src="/images/services-{IMAGES[i]}.webp" alt="{LABELS[i]} — иллюстрация охраны" width="1440" height="960" loading="{loading}" decoding="async"></figure>'

def image_block(item, group):
    # Keep the reserved per-service filename for future individual illustrations.
    if (ROOT / item['image'].lstrip('/')).exists():
        return f'<figure class="service-photo-slot"><img src="{item["image"]}" alt="{escape(item["name"])}" width="1200" height="800" decoding="async"></figure>'
    return photo(group)

def collection_metadata(text, url, title, description, items, image):
    graph = {'@context':'https://schema.org','@graph':[
        {'@type':'CollectionPage','@id':'https://ohrana.tech'+url,'name':title,'url':'https://ohrana.tech'+url,'description':description},
        {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':x['name'],'url':'https://ohrana.tech'+x['url']} for i,x in enumerate(items)]},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Главная','item':'https://ohrana.tech/'},
            {'@type':'ListItem','position':2,'name':'Услуги','item':'https://ohrana.tech/uslugi/'}
        ] + ([] if url=='/uslugi/' else [{'@type':'ListItem','position':3,'name':title,'item':'https://ohrana.tech'+url}])}
    ]}
    tags = f'<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="https://ohrana.tech{url}"><meta property="og:image" content="https://ohrana.tech/images/services-{image}.webp"><script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script>'
    return text.replace('</head>',tags+'</head>',1)

def root_hub(partial):
    cards = ''.join(f'<a class="service-hub-card service-direction" href="{g["url"]}"><img src="/images/services-{IMAGES[i]}.webp" alt="" width="1440" height="960" loading="lazy" decoding="async"><div><span class="service-card-count">{len(g["services"])} направлений</span><h2>{LABELS[i]}</h2><p>{DESCRIPTIONS[i]}</p><span class="service-card-go">Выбрать услугу →</span></div></a>' for i,g in enumerate(GROUPS))
    title = 'Услуги охраны в Москве и МО — ЧОО «Рускорпорация»'
    description = 'Выберите охрану для бизнеса, жилой недвижимости или общественного объекта. 45 направлений, технические решения и персональная защита.'
    text = f'''<!DOCTYPE html><html lang="ru" class="no-js"><head>{partial('head-common.html')}<title>{title}</title><meta name="description" content="{description}"><link rel="canonical" href="https://ohrana.tech/uslugi/"><link rel="stylesheet" href="/css/site-shell.css"><link rel="stylesheet" href="/css/service-pages.css"></head><body data-metrika-id="111882478"><div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>{partial('header.html')}<main class="service-group-hub"><div class="wrap"><nav class="service-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><b>Услуги</b></nav><section class="service-hero service-catalog-hero"><div><span class="service-kicker">Охрана под вашу задачу</span><h1>Безопасность начинается<br>с правильного решения</h1><p class="service-lead">Охраняем объекты и людей. Подбираем посты, контроль доступа и технические средства с учётом ваших рисков, графика и бюджета.</p><div class="service-actions"><a class="btn btn-gold" href="#directions">Выбрать направление</a><a class="btn btn-line" href="/ceny/">Цены и тарифы</a></div><p class="service-note service-experience">Опыт команды с 2007 года · Москва и Московская область</p></div>{photo(GROUPS[0])}</section><section class="service-section" id="directions"><span class="service-kicker">Пять направлений</span><h2>Что нужно защитить?</h2><div class="service-hub-grid service-directions">{cards}<div class="service-hub-card service-help"><span class="service-card-count">Поможем выбрать</span><h2>Нужна комплексная охрана?</h2><p>Расскажите об объекте. Обсудим задачи и предложим сочетание физической охраны, пульта и технических средств.</p><a class="btn btn-gold" href="/kontakty/">Обсудить задачу</a></div></div></section><section class="service-section"><h2>Как организуем охрану</h2><div class="service-links"><article class="service-card"><h3>01. Изучаем объект</h3><p>Уточняем адрес, режим, точки доступа и основные риски.</p></article><article class="service-card"><h3>02. Согласуем решение</h3><p>Определяем состав постов, оснащение, обязанности и стоимость.</p></article><article class="service-card"><h3>03. Запускаем работу</h3><p>Закрепляем порядок охраны и взаимодействия в договоре и инструкциях.</p></article></div></section><section class="service-section"><div class="service-card service-catalog-cta"><div><h2>Сколько стоит охрана?</h2><p>Сравните базовые тарифы или получите расчёт для своего объекта.</p></div><div class="service-actions"><a class="btn btn-line" href="/ceny/">Смотреть цены</a><a class="btn btn-gold" href="/kontakty/">Получить расчёт</a></div></div></section></div></main>{partial('footer.html')}{partial('mobile-bar.html')}{partial('chat.html')}<script src="/js/site.js?v=20260921-pairs4" defer></script></body></html>'''
    return collection_metadata(navigation(text), '/uslugi/', title, description, [{'name':LABELS[i],'url':g['url']} for i,g in enumerate(GROUPS)], 'commercial')

def finish_group(text, group):
    i = next(i for i,g in enumerate(GROUPS) if g['group']==group['group'])
    text = navigation(text)
    text = re.sub(r'Группа [A-E]', 'Направление охраны', text)
    text = text.replace('Существующий раздел','Подробнее об услуге →')
    # Retain the original heading and lead; give each direction a complete hero.
    text = re.sub(r'(<span class="service-kicker">[\s\S]*?<p class="service-lead">[\s\S]*?</p>)', lambda m:'<section class="service-hero service-catalog-hero"><div>'+m[1]+'<div class="service-actions"><a class="btn btn-gold" href="/kontakty/">Получить расчёт</a><a class="btn btn-line" href="/ceny/">Цены и тарифы</a></div></div>'+photo(group)+'</section>',text,count=1)
    if 'cursor-dot' not in text:
        text = text.replace('<div id="progress"></div>','<div id="progress"></div><div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>',1)
    return collection_metadata(text,group['url'],group['title'],DESCRIPTIONS[i],group['services'],IMAGES[i])

def finish_page(text, group):
    text = navigation(text)
    text = text.replace('Реальный кейс с цифрами публикуем только после подтверждения фактических данных.', 'Количество постов, маршруты обходов и порядок взаимодействия согласуем с заказчиком до начала работы.')
    i = next(i for i,g in enumerate(GROUPS) if g['group']==group['group'])
    if 'og:image' not in text:
        text=text.replace('</head>',f'<meta property="og:image" content="https://ohrana.tech/images/services-{IMAGES[i]}.webp"></head>',1)
    return text
