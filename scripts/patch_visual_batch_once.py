from pathlib import Path
import re

# 1) Personal-security radar: use the exact working radar implementation from the reference article.
target = Path('assets/js/ohrana-fizicheskih-lic.js')
radar_ref = Path('assets/js/articles/stoimost-bezopasnosti.js').read_text(encoding='utf-8').strip()
s = target.read_text(encoding='utf-8')
marker = '/* Decorative threat radar, isolated from the shared shell. */'
if marker not in s:
    raise SystemExit('personal-security radar marker not found')
start = s.index(marker)
end = s.rfind('})();')
if end <= start:
    raise SystemExit('personal-security JS closing wrapper not found')
prefix = s[:start].rstrip()
s = prefix + '\n\n/* Security radar: exact implementation used by the working “Стоимость безопасности” article. */\n' + radar_ref + '\n})();\n'
target.write_text(s, encoding='utf-8')

# 2) Shared light theme: make article text variables genuinely dark and add article-specific guardrails.
article_block = '''\n/* article-light-contrast-v2 */
:root[data-theme="light"] :where(.article-layout,.article-body){color:var(--ink)!important}
:root[data-theme="light"] .article-body :where(p,li){color:#34312D!important}
:root[data-theme="light"] .article-body :where(strong,b){color:#171717!important}
:root[data-theme="light"] :where(.hero .lead,.hero-checks li,.info-panel p,.info-panel li,.radar-text p,.article-card p,.article-card .excerpt,.note p){color:#34312D!important}
:root[data-theme="light"] :where(.article-body h2,.article-body h3,.radar-text h3,.info-panel h3){color:var(--gold2)!important}
:root[data-theme="light"] :where(.info-panel,.radar-section,.note,.article-card){background:#fff!important;border-color:rgba(23,23,23,.16)!important}
'''
extra_vars = '--txt:#34312D!important;--amber:#8A5E08!important;--amber2:#644507!important;--amber-deep:#6F4B0A!important;--steel:#52667A!important;--danger:#A52A1F!important;'
for css_path in [Path('assets/css/site-shell.css'), Path('site-src/assets/site-shell.css')]:
    css = css_path.read_text(encoding='utf-8')
    if '--txt:#34312D!important' not in css:
        needle = '--gold-ink:#171003!important}'
        if needle not in css:
            raise SystemExit(f'light theme variable anchor not found in {css_path}')
        css = css.replace(needle, '--gold-ink:#171003!important;' + extra_vars + '}', 1)
    if 'article-light-contrast-v2' not in css:
        css += article_block
    css_path.write_text(css, encoding='utf-8')

# 3) Homepage: same yin-yang styling as inner pages, white recommended tariff, black city chips.
home = Path('assets/css/home-light-fix.css')
h = home.read_text(encoding='utf-8')
home_block = '''\n/* homepage-visual-cleanup-v3 */
#siteNav .theme-toggle{width:44px!important;height:44px!important;flex:0 0 44px!important;margin:2px 0 2px 6px!important;border:1px solid var(--line)!important;border-radius:50%!important;display:inline-grid!important;place-items:center!important;background:var(--panel)!important;color:var(--ink)!important;box-shadow:0 8px 24px rgba(0,0,0,.10)!important;transition:background-color .25s,color .25s,border-color .25s,transform .25s!important}
#siteNav .theme-toggle:hover{border-color:var(--gold)!important;transform:translateY(-1px)!important}
#siteNav .theme-yinyang{font-size:1.3rem!important;line-height:1!important;transform:none!important}
html[data-theme="light"] #siteNav .theme-toggle{background:#fff!important;color:#171717!important;border-color:rgba(23,23,23,.16)!important;box-shadow:0 8px 24px rgba(0,0,0,.10)!important}
html[data-theme="light"] .plan.popular{background:#fff!important;border:1.5px solid #A97F2F!important;box-shadow:0 18px 48px rgba(69,49,20,.10)!important}
html[data-theme="light"] .plan.popular::before{display:none!important}
html[data-theme="light"] .plan.popular :where(h3,.desc,li){color:var(--ink)!important}
html[data-theme="light"] .reg-cities span{color:#0c0c0c!important;background:#fff!important;border-color:rgba(18,15,10,.16)!important}
'''
if 'homepage-visual-cleanup-v3' not in h:
    h += home_block
home.write_text(h, encoding='utf-8')

# 4) Contract rotating shield: high-contrast clock numbers in light mode.
dog = Path('assets/js/dogovor.js')
d = dog.read_text(encoding='utf-8')
old = """      if(i===activeIdx){ctx.font='600 40px Cormorant, Georgia, serif';ctx.fillStyle='#F5E3B3';ctx.shadowColor='rgba(232,200,122,.85)';ctx.shadowBlur=50;}\n      else{ctx.font='500 30px Cormorant, Georgia, serif';ctx.fillStyle='rgba(142,148,163,.38)';ctx.shadowColor='rgba(232,200,122,.05)';ctx.shadowBlur=5;}\n      ctx.fillText(numbers[i],x,y);"""
new = """      var light=document.documentElement.dataset.theme==='light';\n      if(i===activeIdx){\n        ctx.font='600 40px Cormorant, Georgia, serif';\n        ctx.fillStyle=light?'#B57910':'#F5E3B3';\n        ctx.strokeStyle='#111';ctx.lineWidth=light?3:2;\n        ctx.shadowColor=light?'rgba(169,127,47,.45)':'rgba(232,200,122,.85)';ctx.shadowBlur=light?18:50;\n      }else{\n        ctx.font='500 30px Cormorant, Georgia, serif';\n        ctx.fillStyle=light?'rgba(17,17,17,.84)':'rgba(242,238,228,.58)';\n        ctx.strokeStyle=light?'rgba(255,255,255,.92)':'rgba(7,9,13,.9)';ctx.lineWidth=light?2:1.5;\n        ctx.shadowColor=light?'rgba(255,255,255,.35)':'rgba(232,200,122,.08)';ctx.shadowBlur=light?5:7;\n      }\n      ctx.strokeText(numbers[i],x,y);\n      ctx.fillText(numbers[i],x,y);"""
if 'ctx.strokeText(numbers[i],x,y);' not in d:
    if old not in d:
        raise SystemExit('contract number drawing block not found')
    d = d.replace(old, new, 1)
dog.write_text(d, encoding='utf-8')

# Guardrails.
checks = {
    'assets/js/ohrana-fizicheskih-lic.js': ['shieldImage.src = \'/images/schit.jpg\'', 'MAX_TARGETS = 15', 'spawnSparks'],
    'assets/css/site-shell.css': ['article-light-contrast-v2', '--txt:#34312D!important'],
    'assets/css/home-light-fix.css': ['homepage-visual-cleanup-v3', '.plan.popular', '.reg-cities span', '#siteNav .theme-toggle'],
    'assets/js/dogovor.js': ['ctx.strokeText(numbers[i],x,y);', "dataset.theme==='light'"],
}
for name, needles in checks.items():
    text = Path(name).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'missing {needle!r} in {name}')
