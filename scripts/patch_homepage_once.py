from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

actual_button = '''      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Переключить на светлую тему" title="Светлая / тёмная тема">
        <span class="theme-yinyang" aria-hidden="true">☯</span>
      </button>
'''
if actual_button not in s:
    raise SystemExit('theme toggle block not found in header')
s = s.replace(actual_button, '', 1)

contact = '      <a href="/kontakty/">Контакты</a>\n'
if contact not in s:
    raise SystemExit('Contacts nav link not found')
nav_button = '''      <button class="theme-toggle nav-theme-toggle" id="themeToggle" type="button" aria-label="Переключить на светлую тему" title="Светлая / тёмная тема">
        <span class="theme-yinyang" aria-hidden="true">☯</span>
      </button>
'''
s = s.replace(contact, contact + nav_button, 1)

old_css = 'nav.nav .theme-toggle{display:none!important}'
new_css = 'nav.nav .theme-toggle{display:inline-grid!important;width:38px;height:38px;flex:0 0 38px;margin:4px 0 4px 6px;align-self:center;place-items:center;border:1px solid rgba(232,200,122,.34);border-radius:50%;background:rgba(13,17,24,.82);color:var(--gold2)}'
if old_css not in s:
    raise SystemExit('old nav theme-toggle hiding rule not found')
s = s.replace(old_css, new_css, 1)

font_link = '<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">'
fix_link = '<link rel="stylesheet" href="/assets/css/home-light-fix.css?v=20260921-2">'
if fix_link not in s:
    if font_link not in s:
        raise SystemExit('Google fonts link anchor not found')
    s = s.replace(font_link, font_link + '\n' + fix_link, 1)

if s.count('id="themeToggle"') != 1:
    raise SystemExit('themeToggle id must occur exactly once')
nav_start = s.index('<nav class="nav" id="siteNav">')
nav_end = s.index('</nav>', nav_start)
nav = s[nav_start:nav_end]
if '<a href="/kontakty/">Контакты</a>\n      <button class="theme-toggle nav-theme-toggle" id="themeToggle"' not in nav:
    raise SystemExit('theme toggle is not immediately after Contacts')
if fix_link not in s:
    raise SystemExit('calculator light-theme stylesheet was not linked')

p.write_text(s, encoding='utf-8')
print('Homepage patch applied successfully')
