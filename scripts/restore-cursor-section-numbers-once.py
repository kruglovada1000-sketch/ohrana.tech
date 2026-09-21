from pathlib import Path

root = Path('.')

# 1) Restore the exact crafted cursor treatment from the homepage on shared/internal pages.
css_path = root / 'site-src/assets/site-shell.css'
css = css_path.read_text(encoding='utf-8').rstrip()
marker = '/* shared-crafted-cursor-section-numbers-v1 */'
if marker in css:
    css = css.split(marker, 1)[0].rstrip()
css += r'''

/* shared-crafted-cursor-section-numbers-v1 */
.cursor-dot,.cursor-ring{position:fixed;top:0;left:0;z-index:5000;pointer-events:none;border-radius:50%;transform:translate(-50%,-50%)}
.cursor-dot{width:6px;height:6px;background:var(--gold2)}
.cursor-ring{width:38px;height:38px;border:1px solid rgba(232,200,122,.5);transition:width .35s var(--ease),height .35s var(--ease),border-color .35s,background .35s}
.cursor-ring.hov{width:64px;height:64px;border-color:rgba(232,200,122,.9);background:rgba(232,200,122,.06)}
@media (hover:none),(max-width:960px){.cursor-dot,.cursor-ring{display:none!important}}
.sec-num{position:absolute!important;top:-58px!important;right:0!important;font-family:var(--serif)!important;font-style:italic!important;font-size:clamp(4rem,9vw,8rem)!important;line-height:1!important;color:transparent!important;-webkit-text-stroke:1px rgba(232,200,122,.14)!important;pointer-events:none!important;user-select:none!important;z-index:0}
.sec-head.center .sec-num{right:50%!important;transform:translateX(50%)!important}
:root[data-theme="light"] .sec-num{-webkit-text-stroke-color:rgba(111,75,10,.20)!important}
'''.strip() + '\n'
css_path.write_text(css, encoding='utf-8')

# 2) Restore hover expansion behavior for the shared cursor.
js_path = root / 'site-src/assets/site.js'
js = js_path.read_text(encoding='utf-8')
js_marker = '/* shared-crafted-cursor-hover-v1 */'
if js_marker not in js:
    needle = "document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){"
    if needle not in js:
        raise SystemExit('carousel anchor not found in shared site.js')
    hover_js = r'''/* shared-crafted-cursor-hover-v1 */
document.addEventListener('mouseover',function(e){
  var ring=document.querySelector('.cursor-ring');
  if(ring)ring.classList.toggle('hov',!!e.target.closest('a,button,select,input,.switch-row'));
},{passive:true});
'''
    js = js.replace(needle, hover_js + needle, 1)
js_path.write_text(js, encoding='utf-8')

# 3) Restore decorative section numbers on the generated Prices page.
build_path = root / 'scripts/build_site.py'
b = build_path.read_text(encoding='utf-8')
repls = [
    ('<div class="price-head" data-reveal><span class="eyebrow">Тарифы</span>', '<div class="price-head" data-reveal><span class="sec-num">01</span><span class="eyebrow">Тарифы</span>'),
    ('<div class="price-head" data-reveal><span class="eyebrow">По типу объекта</span>', '<div class="price-head" data-reveal><span class="sec-num">02</span><span class="eyebrow">По типу объекта</span>'),
    ('<div class="price-head" data-reveal><span class="eyebrow">Расчёт</span>', '<div class="price-head" data-reveal><span class="sec-num">03</span><span class="eyebrow">Расчёт</span>'),
    ('<div class="price-cta-box" data-reveal><h2>', '<div class="price-cta-box" data-reveal><span class="sec-num price-cta-num">04</span><h2>'),
]
for old,new in repls:
    if new not in b:
        if old not in b:
            raise SystemExit(f'build_site.py anchor not found: {old[:80]}')
        b = b.replace(old,new,1)
b = b.replace('/assets/css/pricing.css?v=20260921-pairs3', '/assets/css/pricing.css?v=20260921-pairs4')
b = b.replace('/assets/js/site.js?v=20260921-pairs3', '/assets/js/site.js?v=20260921-pairs4')
build_path.write_text(b, encoding='utf-8')

# 4) Position the CTA number cleanly inside its panel, while price-head numbers use the shared rule.
pricing_path = root / 'site-src/assets/pricing.css'
p = pricing_path.read_text(encoding='utf-8').rstrip()
p_marker = '/* pricing-section-numbers-v1 */'
if p_marker in p:
    p = p.split(p_marker,1)[0].rstrip()
p += r'''

/* pricing-section-numbers-v1 */
.price-head{position:relative;z-index:1}
.price-head>.sec-num{z-index:-1}
.price-cta-box>.price-cta-num{top:20px!important;right:26px!important;z-index:0!important;font-size:clamp(4.5rem,9vw,8rem)!important}
.price-cta-box>h2,.price-cta-box>p,.price-cta-box>.btn{position:relative;z-index:1}
@media(max-width:700px){.price-cta-box>.price-cta-num{top:16px!important;right:18px!important;font-size:5rem!important}}
'''.strip() + '\n'
pricing_path.write_text(p, encoding='utf-8')

print('restored crafted cursor and decorative section numbers')
