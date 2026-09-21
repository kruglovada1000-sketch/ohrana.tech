from pathlib import Path

root = Path('.')

# JS: deterministic pair-by-pair carousel via transform (no scroll mechanics).
js_path = root / 'site-src/assets/site.js'
js = js_path.read_text(encoding='utf-8')
start = js.find("document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){")
end = js.find("\n})();", start)
if start < 0 or end < 0:
    raise SystemExit('pricing carousel JS block not found')
new_js = r'''document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){
  var viewport=carousel.querySelector('[data-carousel-viewport]');
  var track=carousel.querySelector('.tariff-track');
  var pairs=Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-pair]'));
  var prev=carousel.querySelector('[data-carousel-prev]');
  var next=carousel.querySelector('[data-carousel-next]');
  var dots=Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-dot]'));
  if(!viewport||!track||!pairs.length)return;
  var active=0;
  function render(animate){
    if(!animate)track.style.transition='none';
    else track.style.transition='transform .45s cubic-bezier(.22,.61,.36,1)';
    track.style.transform='translate3d('+(-active*100)+'%,0,0)';
    dots.forEach(function(dot,index){
      dot.hidden=index>=pairs.length;
      dot.setAttribute('aria-pressed',String(index===active));
    });
    if(prev){prev.disabled=active===0;prev.setAttribute('aria-disabled',String(active===0));}
    if(next){next.disabled=active===pairs.length-1;next.setAttribute('aria-disabled',String(active===pairs.length-1));}
    if(!animate)requestAnimationFrame(function(){track.style.transition='transform .45s cubic-bezier(.22,.61,.36,1)';});
  }
  function go(index){
    var nextIndex=Math.max(0,Math.min(pairs.length-1,index));
    if(nextIndex===active)return;
    active=nextIndex;
    render(true);
  }
  if(prev)prev.addEventListener('click',function(e){e.preventDefault();go(active-1);});
  if(next)next.addEventListener('click',function(e){e.preventDefault();go(active+1);});
  dots.forEach(function(dot,index){dot.addEventListener('click',function(e){e.preventDefault();go(index);});});
  viewport.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){e.preventDefault();go(active-1);}
    else if(e.key==='ArrowRight'){e.preventDefault();go(active+1);}
  });
  render(false);
});'''
js = js[:start] + new_js + js[end:]
js_path.write_text(js, encoding='utf-8')

# CSS: hard final override. Exactly one pair fills viewport; each pair contains exactly 2 cards.
css_path = root / 'site-src/assets/pricing.css'
css = css_path.read_text(encoding='utf-8').rstrip()
marker = '/* pricing-pair-carousel-v3-exact-two */'
if marker in css:
    css = css.split(marker, 1)[0].rstrip()
css += r'''

/* pricing-pair-carousel-v3-exact-two */
.price-tariffs .tariff-carousel{position:relative!important;padding:0 72px!important;min-width:0!important}
.price-tariffs .tariff-viewport{position:relative!important;width:100%!important;max-width:100%!important;overflow:hidden!important;padding:8px 0 18px!important;scroll-snap-type:none!important;scroll-behavior:auto!important}
.price-tariffs .tariff-track{display:flex!important;flex-wrap:nowrap!important;width:100%!important;min-width:100%!important;max-width:none!important;gap:0!important;transform:translate3d(0,0,0);will-change:transform;align-items:stretch!important}
.price-tariffs .tariff-pair{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:24px!important;flex:0 0 100%!important;width:100%!important;min-width:100%!important;max-width:100%!important;padding:0!important;margin:0!important;box-sizing:border-box!important;scroll-snap-align:none!important}
.price-tariffs .tariff-pair>.tariff-card{display:flex!important;flex-direction:column!important;width:100%!important;min-width:0!important;max-width:none!important;min-height:520px!important;height:100%!important;box-sizing:border-box!important;scroll-snap-align:none!important}
.price-tariffs .tariff-pair>.tariff-image-card{display:block!important;padding:0!important;overflow:hidden!important}
.price-tariffs .tariff-pair>.tariff-image-card img{display:block!important;width:100%!important;height:100%!important;min-height:520px!important;object-fit:cover!important;object-position:center!important}
.price-tariffs .tariff-controls{display:flex!important;align-items:center!important;justify-content:center!important;min-height:60px!important;margin-top:4px!important;position:static!important}
.price-tariffs .tariff-dots{display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important}
.price-tariffs .tariff-arrows{position:absolute!important;inset:0!important;z-index:20!important;pointer-events:none!important;display:block!important}
.price-tariffs .tariff-arrow{position:absolute!important;top:46%!important;transform:translateY(-50%)!important;width:56px!important;height:56px!important;display:grid!important;place-items:center!important;border-radius:50%!important;pointer-events:auto!important;z-index:21!important;cursor:pointer!important}
.price-tariffs .tariff-arrow[data-carousel-prev]{left:5px!important}
.price-tariffs .tariff-arrow[data-carousel-next]{right:5px!important}
.price-tariffs .tariff-arrow:disabled{opacity:.28!important;cursor:default!important;pointer-events:none!important}
@media(max-width:900px){
  .price-tariffs .tariff-carousel{padding:0 58px!important}
  .price-tariffs .tariff-pair{gap:18px!important}
  .price-tariffs .tariff-pair>.tariff-card,.price-tariffs .tariff-pair>.tariff-image-card img{min-height:480px!important}
  .price-tariffs .tariff-arrow{width:48px!important;height:48px!important}
}
@media(max-width:700px){
  .price-tariffs .tariff-carousel{padding:0!important}
  .price-tariffs .tariff-pair{grid-template-columns:1fr!important;gap:14px!important}
  .price-tariffs .tariff-pair>.tariff-card{min-height:0!important}
  .price-tariffs .tariff-pair>.tariff-image-card img{min-height:340px!important}
  .price-tariffs .tariff-controls{display:grid!important;grid-template-columns:52px minmax(0,1fr) 52px!important;gap:12px!important;margin-top:10px!important}
  .price-tariffs .tariff-arrows{display:contents!important}
  .price-tariffs .tariff-arrow{position:static!important;transform:none!important;width:52px!important;height:52px!important}
  .price-tariffs .tariff-arrow[data-carousel-prev]{grid-column:1!important;grid-row:1!important}
  .price-tariffs .tariff-arrow[data-carousel-next]{grid-column:3!important;grid-row:1!important}
  .price-tariffs .tariff-dots{grid-column:2!important;grid-row:1!important}
}
''' + '\n'
css_path.write_text(css, encoding='utf-8')

# Cache-bust generated pricing page after rebuilding.
build_path = root / 'scripts/build_site.py'
b = build_path.read_text(encoding='utf-8')
b = b.replace('/assets/css/pricing.css?v=20260921-pairs2', '/assets/css/pricing.css?v=20260921-pairs3')
b = b.replace('/assets/js/site.js?v=20260921-pairs2', '/assets/js/site.js?v=20260921-pairs3')
build_path.write_text(b, encoding='utf-8')

print('fixed pricing carousel: exactly one 2-card pair per viewport; arrows use transform')
