from pathlib import Path
import re

root = Path('.')

# 1) Replace continuous auto-scroll carousel JS with manual pair navigation.
js_path = root / 'site-src/assets/site.js'
js = js_path.read_text(encoding='utf-8')
start = js.find("document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){")
end = js.find("\n})();", start)
if start < 0 or end < 0:
    raise SystemExit('pricing carousel JS block not found')
new_js = r'''document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){
  var viewport=carousel.querySelector('[data-carousel-viewport]');
  var pairs=Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-pair]'));
  var prev=carousel.querySelector('[data-carousel-prev]');
  var next=carousel.querySelector('[data-carousel-next]');
  var dots=Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-dot]'));
  if(!viewport||!pairs.length)return;
  var active=0,scrollTick=false;
  function setUi(){
    dots.forEach(function(dot,index){dot.hidden=index>=pairs.length;dot.setAttribute('aria-pressed',String(index===active));});
    if(prev)prev.disabled=active===0;
    if(next)next.disabled=active===pairs.length-1;
  }
  function go(index,behavior){
    active=Math.max(0,Math.min(pairs.length-1,index));
    viewport.scrollTo({left:pairs[active].offsetLeft,behavior:behavior||(rm?'auto':'smooth')});
    setUi();
  }
  function nearest(){
    var left=viewport.scrollLeft,best=0,distance=Infinity;
    pairs.forEach(function(pair,index){var d=Math.abs(pair.offsetLeft-left);if(d<distance){distance=d;best=index;}});
    if(best!==active){active=best;setUi();}
  }
  if(prev)prev.addEventListener('click',function(){if(active>0)go(active-1);});
  if(next)next.addEventListener('click',function(){if(active<pairs.length-1)go(active+1);});
  dots.forEach(function(dot,index){dot.addEventListener('click',function(){if(index<pairs.length)go(index);});});
  viewport.addEventListener('scroll',function(){if(scrollTick)return;scrollTick=true;requestAnimationFrame(function(){nearest();scrollTick=false;});},{passive:true});
  viewport.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){e.preventDefault();if(active>0)go(active-1);}else if(e.key==='ArrowRight'){e.preventDefault();if(active<pairs.length-1)go(active+1);}});
  window.addEventListener('resize',function(){go(active,'auto');},{passive:true});
  go(0,'auto');
});'''
js = js[:start] + new_js + js[end:]
js_path.write_text(js, encoding='utf-8')

# 2) Replace the running-tape CSS with pair-per-slide CSS.
css_path = root / 'site-src/assets/pricing.css'
css = css_path.read_text(encoding='utf-8')
marker = '/* pricing-seamless-paired-carousel-v1 */'
if marker not in css:
    raise SystemExit('seamless carousel CSS marker not found')
css = css.split(marker,1)[0].rstrip() + r'''

/* pricing-manual-paired-carousel-v2 */
.tariff-viewport{overflow-x:auto!important;overflow-y:hidden!important;scroll-snap-type:x mandatory!important;scroll-behavior:smooth!important;overscroll-behavior-x:contain!important;padding-bottom:22px;scrollbar-width:none}
.tariff-viewport::-webkit-scrollbar{display:none}
.tariff-track{display:flex!important;width:100%!important;min-width:100%!important;gap:0!important;align-items:stretch}
.tariff-pair{flex:0 0 100%;width:100%;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;scroll-snap-align:start;scroll-snap-stop:always;padding:8px 2px 10px;box-sizing:border-box}
.tariff-pair>.tariff-card{min-width:0;width:100%;height:100%;min-height:520px}
.tariff-image-card{padding:0!important;background:var(--panel);overflow:hidden}
.tariff-image-card::before{display:none!important}
.tariff-image-card img{display:block;width:100%;height:100%;min-height:520px;object-fit:cover;object-position:center;transition:transform .55s var(--ease),filter .35s;filter:saturate(.92) contrast(1.04)}
.tariff-image-card:hover img{transform:scale(1.018);filter:saturate(1) contrast(1.05)}
.tariff-controls{display:flex!important;justify-content:center!important;align-items:center!important;min-height:58px!important}
.tariff-arrow:disabled{opacity:.32!important;cursor:default!important;pointer-events:none!important}
@media(max-width:900px){.tariff-pair{gap:18px}.tariff-pair>.tariff-card,.tariff-image-card img{min-height:500px}}
@media(max-width:700px){.tariff-pair{grid-template-columns:1fr;gap:14px;padding-inline:0}.tariff-pair>.tariff-card{min-height:0}.tariff-image-card,.tariff-image-card img{min-height:360px}.tariff-controls{display:grid!important}}
'''.strip() + '\n'
css_path.write_text(css, encoding='utf-8')

# 3) Make the generator emit 7 full-width pairs (each pair = tariff + matching image).
build_path = root / 'scripts/build_site.py'
b = build_path.read_text(encoding='utf-8')
b = b.replace('    carousel_items: list[str] = []\n', '    carousel_pairs: list[str] = []\n')
old = '''        carousel_items.append(\n            f\'\'\'<article class="tariff-card" data-tariff-card data-carousel-item>\n<div class="tariff-card-head"><span class="tariff-badge">{esc(tariff[\'badge\'])}</span><span class="tariff-no">{index:02d}</span></div>\n<h3>{esc(service[\'name\'])}</h3>\n<div class="tariff-price">{money(service[\'price_from\'], service[\'unit\'])}</div>\n<p class="tariff-desc">{esc(tariff[\'description\'])}</p>\n<dl class="tariff-specs">\n<div><dt>График работы</dt><dd>{esc(tariff[\'schedule\'])}</dd></div>\n<div><dt>Экипировка</dt><dd>{esc(tariff[\'equipment\'])}</dd></div>\n<div><dt>Профподготовка</dt><dd>{esc(tariff[\'training\'])}</dd></div>\n<div><dt>Условия</dt><dd>{esc(tariff[\'conditions\'])}</dd></div>\n</dl>\n<div class="tariff-card-actions"><a class="btn btn-gold" href="/kontakty/">Заказать</a><a class="tariff-more" href="{esc(service[\'url\'])}">Подробнее →</a></div>\n</article>\'\'\'\n        )\n        carousel_items.append(\n            f\'\'\'<figure class="tariff-card tariff-image-card" data-carousel-item aria-label="{esc(tariff[\'image_alt\'])}">\n<img src="{esc(tariff[\'image\'])}" alt="{esc(tariff[\'image_alt\'])}" width="1200" height="900" loading="lazy" decoding="async">\n</figure>\'\'\'\n        )'''
new = '''        carousel_pairs.append(\n            f\'\'\'<div class="tariff-pair" data-carousel-pair>\n<article class="tariff-card" data-tariff-card>\n<div class="tariff-card-head"><span class="tariff-badge">{esc(tariff[\'badge\'])}</span><span class="tariff-no">{index:02d}</span></div>\n<h3>{esc(service[\'name\'])}</h3>\n<div class="tariff-price">{money(service[\'price_from\'], service[\'unit\'])}</div>\n<p class="tariff-desc">{esc(tariff[\'description\'])}</p>\n<dl class="tariff-specs">\n<div><dt>График работы</dt><dd>{esc(tariff[\'schedule\'])}</dd></div>\n<div><dt>Экипировка</dt><dd>{esc(tariff[\'equipment\'])}</dd></div>\n<div><dt>Профподготовка</dt><dd>{esc(tariff[\'training\'])}</dd></div>\n<div><dt>Условия</dt><dd>{esc(tariff[\'conditions\'])}</dd></div>\n</dl>\n<div class="tariff-card-actions"><a class="btn btn-gold" href="/kontakty/">Заказать</a><a class="tariff-more" href="{esc(service[\'url\'])}">Подробнее →</a></div>\n</article>\n<figure class="tariff-card tariff-image-card" aria-label="{esc(tariff[\'image_alt\'])}">\n<img src="{esc(tariff[\'image\'])}" alt="{esc(tariff[\'image_alt\'])}" width="1200" height="900" loading="lazy" decoding="async">\n</figure>\n</div>\'\'\'\n        )'''
if old not in b:
    raise SystemExit('generator carousel append block not found')
b = b.replace(old,new,1)
b = b.replace("{''.join(carousel_items)}", "{''.join(carousel_pairs)}", 1)
b = b.replace('/assets/css/pricing.css?v=20260921-loop1', '/assets/css/pricing.css?v=20260921-pairs2')
b = b.replace('/assets/js/site.js?v=20260921-loop1', '/assets/js/site.js?v=20260921-pairs2')
build_path.write_text(b, encoding='utf-8')

print('restored manual pair-by-pair pricing carousel')
