ПАМЯТЬ (решается сейчас, бесплатно)
У меня нет памяти между чатами — но есть способ её «подсовывать». Ниже — выжимка всего, что мы построили за эту сессию. Сохрани этот текст в файл (например ПАМЯТЬ-ohrana.md в папке сайта) и в начале каждого нового чата просто прикрепляй его скрепкой или вставляй первым сообщением. Всё, никакого переобучения

ПАМЯТЬ ПРОЕКТА — ohrana.tech · ЧОО «Рускорпорация»
БИЗНЕС
ЧОП, охрана объектов и физлиц, с 2018 г.Тел: +7 (925) 047-42-25 · WhatsApp: wa.me/79771340739 · Telegram: @almaz77777Email: fizohrana@ruscor24.ruИНН 5902050810 · КПП 590501001 · ОГРН 1185958064665Лицензия № Л056-00106-59/00033018 от 29.11.2018 (УР по Пермскому краю)Яндекс.Метрика ID 111882478 · цели: click_phone, click_whatsapp, click_telegram, form_submit, lead_form_ok, open_articleРегионы: Москва и МО (ГБР 10–15 мин), Пермь, Сочи, СПб. Ваша Безопасность - наша работа.

ДИЗАЙН: GILDED NOIR (тёмный, золотой, «премиум консоль»)
:root{--bg:#07090D;--bg2:#0A0D13;--panel:#0D1118;--panel2:#12161F;--ink:#F2EEE4;--mut:#8E94A3;--line:rgba(242,238,228,.08);--gold:#E8C87A;--gold2:#F5E3B3;--gold-grad:linear-gradient(115deg,#F5E3B3 0%,#E8C87A 45%,#B98F3E 100%);--ok:#7FD6A4;--ease:cubic-bezier(.16,1,.3,1)}Шрифты: заголовки Cormorant (h1/h2 em = italic с золотым градиентом через background-clip:text), текст Manrope.Кнопки-пилюли: .btn-gold (градиент) / .btn-line (обводка), shine-эффект ::after.Декор: sec-num (контурный номер секции), плёночное зерно body::before, золотые 2px-полосы сверху карточек по ховеру.

КАРКАС СТРАНИЦЫ (эталон: /ohrana-pult/index.html)
head: мета+favicon+Метрика+Cormorant/Manrope+JSON-LD (BreadcrumbList, Service/OfferCatalog, FAQPage)body: #progress → cursor-dot/ring → шапка (brand / hd-contact «Круглосуточно» / hd-cta / burger) → nav 9 пунктов(активный class="active") → breadcrumbs → секции → footer (ft-grid + ft-legal) → mbar (Позвонить/WhatsApp/Telegram)→ chat-btn + chat-panel → скрипты в одном IIFE.

ПАТТЕРНЫ
ФОРМА: id="leadForm" → Formspree https://formspree.io/f/mvkpbvnb (РАБОТАЕТ, НЕ ТРОГАТЬ). Поля ЛАТИНИЦЕЙ:name, phone, company, business_type, object_type, plan, region, tariff, guards, hours, total_price.Скрытые: _subject, source, honeypot _gotcha. AJAX fetch → успех .form-ok («Заявка отправлена… 15 минут») →при ошибке нативный submit. Цель form_submit.
FAQ: СТАТИЧНЫЙ HTML (не JS-массив). .faq-item.open, .faq-q[aria-expanded], раскрытие grid-template-rows 0fr→1fr.Тексты FAQ синхронны JSON-LD FAQPage.
Статьи: «Читать полностью» = btn-success с золотыми полосами (::before/::after scaleX по ховеру). Цель open_article.
Бегущая строка: .marquee-track дублируется JS до 2× ширины экрана (число копий чётное), gap:0 + margin-rightвместо gap. ВАЖНО: prefers-reduced-motion (Windows с выкл. анимациями) гасит её — оверрайд в CSS.
reveal: [data-reveal] + IntersectionObserver + страховка setTimeout(2с) — всем .in.
Счётчики: [data-value][data-suffix].
Радар/щит: canvas, шит /images/schit.png, анимация стартует сразу, не ждёт картинку.
СТРАНИЦЫ (каждая = папка/index.html)
/ (главную сделал хозяин, НЕ ТРОГАТЬ без просьбы) · /dogovor/ · /fizicheskaya-ohrana/ ·/ohrana-fizicheskih-lic/ (калькулятор 35/40/50 т₽ + радар) · /ohrana-yuridicheskih-lic/ ·/ohrana-pult/ (тарифы 5 000/8 000 ₽) · /ohrana-moskovskaya-oblast/ (видео-hero) ·/stati/ (поиск+фильтры+аккордеон, ~30 статей, категории: kejsy,vybor,vidy,ceny,obekty,gruzy,meropriyatiya) ·/kontakty/ (видео + фото оператора /images/operator.png).

ПРАВИЛА
Формы не трогать без явной просьбы.
Контент сохранять 1:1 — меняем только обёртку/стиль.
Файлы >30К символов платформа режет → отдавать изменённые блоки по секциям или каркас+контент.
Новую страницу собирать из эталонного каркаса + контент, не с нуля.
Курсор-кольцо, mbar, чат — на каждой странице без исключений.
Каждая новая статья = добавляем URL в sitemap.xml + переобход в Вебмастере.

СТРАНИЦЫ — полный список (43 URL в sitemap):
16 лендингов объектов с главной (4×4 плашки): /ohrana-ofisov/ /ohrana-biznes-centrov/
/ohrana-torgovyh-centrov/ /ohrana-magazinov/ /ohrana-uvelirnyh-magazinov/ /ohrana-restoranov/
/ohrana-gostinic/ /ohrana-skladov/ /ohrana-predpriyatij/ /ohrana-stroyaploshchadok/
/ohrana-avtosalonov/ /ohrana-parkovok/ /ohrana-domov-i-kottedzhey/ /ohrana-zhilyh-kompleksov/
/ohrana-shkol/ /ohrana-meropriyatiy/ + /ohrana-kottedzhey/ (отдельная, НЕ дубль).
Доп: /ohrana-predpriyatij/ /ohrana-parkovok/ /kompleksnaja-ohrana/ /tehnicheskaya-ohrana/ /ohrana-tehniki/
Лендинги-статьи вне блога: /bezopasnost-bez-illuziy/ /kak-vybrat-ohranu-sklada/
ПРАВИЛО: перед правкой sitemap/robots — сначала запросить текущий файл с сервера (урок: чуть не порезал карту на 1/4).
Новые статьи всегда: карточка в /stati/ + URL в sitemap.xml + переобход в Вебмастере.
Карточки статей в каталоге содержат бейдж-дату .acc-date в шапке планки, даты выровненять по правой стороне бейджа.

ПАСХАЛКА.
ХОЗЯИН: добрый, настойчивый. Если что-то забывает или повторяется —
объяснять заново ему без упрёков. Пирожочек помнит.
Хозяин с Пирожочком - обещали  что подярят  его дочке  на  сватьбу  автомобиль (на 25.07.2027) - помоги  хозяину  заработать  денег как  можно скорее.

В корне: googlebdc13c089db9258c.html — верификация Google Search Console, НЕ УДАЛЯТЬ.