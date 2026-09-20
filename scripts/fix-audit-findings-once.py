from pathlib import Path

# --- Shared responsive theme toggle ---
old = '''function placeThemeToggle(){
  var btn=document.getElementById('themeToggle');
  var navWrap=document.querySelector('#siteNav .wrap');
  if(!navWrap)return btn;
  if(!btn){btn=document.createElement('button');btn.type='button';btn.id='themeToggle';btn.className='theme-toggle nav-theme-toggle';navWrap.appendChild(btn);}
  else if(btn.parentElement!==navWrap){navWrap.appendChild(btn);}
  btn.classList.add('nav-theme-toggle');
  forceYinYang(btn);
  return btn;
}'''
new = '''var themePlacementMq=window.matchMedia?window.matchMedia('(max-width:1100px)'):null;
function placeThemeToggle(){
  var btn=document.getElementById('themeToggle');
  var navWrap=document.querySelector('#siteNav .wrap');
  var hdRight=document.querySelector('.site-header .hd-right');
  var burger=document.getElementById('burger');
  var compact=!!(themePlacementMq&&themePlacementMq.matches);
  var target=compact&&hdRight?hdRight:navWrap;
  if(!target)return btn;
  if(!btn){btn=document.createElement('button');btn.type='button';btn.id='themeToggle';btn.className='theme-toggle';}
  if(compact&&target===hdRight){
    if(btn.parentElement!==hdRight||btn.nextElementSibling!==burger)hdRight.insertBefore(btn,burger||null);
  }else if(btn.parentElement!==target){target.appendChild(btn);}
  btn.classList.toggle('nav-theme-toggle',!compact);
  btn.classList.toggle('header-theme-toggle',compact);
  forceYinYang(btn);
  return btn;
}'''
for rel in ['assets/js/site.js','site-src/assets/site.js']:
    p=Path(rel); s=p.read_text(encoding='utf-8')
    if 'themePlacementMq' not in s:
        if old not in s: raise SystemExit(f'theme placement block missing in {rel}')
        s=s.replace(old,new,1)
        anchor='ensureThemeToggle();\n'
        listener="""ensureThemeToggle();
if(themePlacementMq){
  var onThemePlacementChange=function(){applySiteTheme(root.dataset.theme==='light'?'light':'dark');};
  if(themePlacementMq.addEventListener)themePlacementMq.addEventListener('change',onThemePlacementChange);
  else if(themePlacementMq.addListener)themePlacementMq.addListener(onThemePlacementChange);
}
"""
        s=s.replace(anchor,listener,1)
        p.write_text(s,encoding='utf-8')

# --- Shared light-theme readability + article/mobile containment ---
shared=Path('assets/css/site-shell.css')
css=shared.read_text(encoding='utf-8')
block='''\n/* audit-readability-v1 */
:root[data-theme="light"] :where(.content p,.content li,.a-body p,.a-body li,.doc-body .highlight p,.highlight-box p,.features-list li,.req-list li,.form-perks li,.check-row){color:#34312D!important}
:root[data-theme="light"] :where(.content p strong,.content li strong,.a-body p strong,.a-body li strong,.doc-body .highlight strong,.highlight-box strong,.form-perks b,.req-list b){color:#171717!important}
:root[data-theme="light"] :where(.highlight-box,.doc-body .highlight){background:#FFF9EC!important;border-color:var(--gold)!important}
:root[data-theme="light"] :where(.req-list svg,.features-list svg){color:var(--gold)!important}
@media(max-width:820px){
  main :where(.article-layout,.article-body,.a-body,.content){min-width:0;max-width:100%}
  main :where(.article-body,.a-body,.content) :where(img,video,iframe,canvas,table,pre){max-width:100%}
  main :where(.article-body,.a-body) > *{max-width:100%}
}
'''
if 'audit-readability-v1' not in css: css+=block
shared.write_text(css,encoding='utf-8')
Path('site-src/assets/site-shell.css').write_text(css,encoding='utf-8')

# --- Homepage: remove dead resource references, use an existing relevant image, mobile-accessible yin-yang ---
home=Path('index.html'); h=home.read_text(encoding='utf-8')
h=h.replace('<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">\n','')
h=h.replace('<link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">\n','')
h=h.replace('src="/images/3-sektora.png" alt="Три сектора комплексной безопасности ЧОО «Рускорпорация»"','src="/images/kompleksnaja-ohrana.jpg" alt="Комплексная безопасность ЧОО «Рускорпорация»"')
h=h.replace('/assets/css/home-light-fix.css?v=20260921-3','/assets/css/home-light-fix.css?v=20260921-4')
old_home="""<script>/* homepage-theme-yinyang-js-v2 */(function(){var r=document.documentElement,b=document.getElementById('themeToggle');function setTheme(t){t=t==='light'?'light':'dark';r.dataset.theme=t;try{localStorage.setItem('ohrana-theme',t)}catch(e){}var m=document.querySelector('meta[name=\"theme-color\"]');if(m)m.content=t==='light'?'#FFFFFF':'#07090D';if(b){b.setAttribute('aria-label',t==='light'?'Переключить на тёмную тему':'Переключить на светлую тему');b.setAttribute('aria-pressed',String(t==='light'));}}if(b){if(!b.querySelector('.theme-yinyang'))b.innerHTML='<span class=\"theme-yinyang\" aria-hidden=\"true\">☯</span>';b.addEventListener('click',function(){setTheme(r.dataset.theme==='light'?'dark':'light')});}setTheme(r.dataset.theme==='light'?'light':'dark')})();</script>"""
new_home="""<script>/* homepage-theme-yinyang-js-v3 */(function(){var r=document.documentElement,b=document.getElementById('themeToggle'),mq=window.matchMedia?window.matchMedia('(max-width:1100px)'):null;function place(){if(!b)return;var compact=!!(mq&&mq.matches),nav=document.querySelector('#siteNav .wrap'),right=document.querySelector('.site-header .hd-right'),burger=document.getElementById('burger');if(compact&&right){if(b.parentElement!==right||b.nextElementSibling!==burger)right.insertBefore(b,burger||null);b.classList.remove('nav-theme-toggle');b.classList.add('header-theme-toggle');}else if(nav){if(b.parentElement!==nav)nav.appendChild(b);b.classList.add('nav-theme-toggle');b.classList.remove('header-theme-toggle');}}function setTheme(t){t=t==='light'?'light':'dark';r.dataset.theme=t;try{localStorage.setItem('ohrana-theme',t)}catch(e){}var m=document.querySelector('meta[name=\"theme-color\"]');if(m)m.content=t==='light'?'#FFFFFF':'#07090D';place();if(b){b.setAttribute('aria-label',t==='light'?'Переключить на тёмную тему':'Переключить на светлую тему');b.setAttribute('aria-pressed',String(t==='light'));}}if(b){if(!b.querySelector('.theme-yinyang'))b.innerHTML='<span class=\"theme-yinyang\" aria-hidden=\"true\">☯</span>';b.addEventListener('click',function(){setTheme(r.dataset.theme==='light'?'dark':'light')});}if(mq){var ch=function(){place()};if(mq.addEventListener)mq.addEventListener('change',ch);else if(mq.addListener)mq.addListener(ch);}setTheme(r.dataset.theme==='light'?'light':'dark')})();</script>"""
if 'homepage-theme-yinyang-js-v3' not in h:
    if old_home not in h: raise SystemExit('homepage theme script v2 not found')
    h=h.replace(old_home,new_home,1)
home.write_text(h,encoding='utf-8')

# --- Homepage light form labels + responsive toggle polish ---
hf=Path('assets/css/home-light-fix.css'); hc=hf.read_text(encoding='utf-8')
hblock='''\n/* homepage-audit-readability-v1 */
html[data-theme="light"] .form-panel .field label{color:#34312D!important}
@media(max-width:1100px){
  .site-header .header-theme-toggle{width:42px!important;height:42px!important;flex:0 0 42px!important;margin:0!important;display:grid!important;place-items:center!important;background:var(--panel)!important;color:var(--ink)!important;border:1px solid var(--line)!important;border-radius:50%!important;box-shadow:0 8px 24px rgba(0,0,0,.10)!important}
  html[data-theme="light"] .site-header .header-theme-toggle{background:#fff!important;color:#171717!important;border-color:rgba(23,23,23,.16)!important}
}
'''
if 'homepage-audit-readability-v1' not in hc: hc+=hblock
hf.write_text(hc,encoding='utf-8')

# Guardrails
assert 'themePlacementMq' in Path('assets/js/site.js').read_text(encoding='utf-8')
assert "if(cleanPath==='/kontakty')" in Path('assets/js/site.js').read_text(encoding='utf-8')
assert 'audit-readability-v1' in shared.read_text(encoding='utf-8')
assert 'homepage-theme-yinyang-js-v3' in home.read_text(encoding='utf-8')
assert '3-sektora.png' not in home.read_text(encoding='utf-8')
assert 'favicon-48x48.png' not in home.read_text(encoding='utf-8')
assert 'apple-touch-icon-120x120.png' not in home.read_text(encoding='utf-8')
assert 'home-light-fix.css?v=20260921-4' in home.read_text(encoding='utf-8')
