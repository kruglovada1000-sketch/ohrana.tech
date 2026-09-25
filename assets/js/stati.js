(function(){
'use strict';

/* Статьи: стабильные превью без reveal/fade и без подмены src после загрузки. */
var style=document.createElement('style');
style.id='article-catalog-fix-v4';
style.textContent='\
.accordion-container .accordion-item[data-reveal]{opacity:1!important;transform:none!important;transition:border-color .35s!important}\
.accordion-content,.accordion-content.active{opacity:1!important;animation:none!important;transition:max-height .32s var(--ease)!important}\
.accordion-featured{display:grid!important;grid-template-columns:124px minmax(0,1fr)!important;gap:18px!important;align-items:center!important;padding:8px 24px 10px!important;animation:none!important}\
.accordion-featured>a{display:block!important;width:124px!important;max-width:124px!important;aspect-ratio:2/3!important;overflow:hidden!important;border-radius:18px!important;border:2px solid transparent!important;background:linear-gradient(var(--panel),var(--panel)) padding-box,var(--gold-grad) border-box!important;box-shadow:0 10px 30px rgba(232,200,122,.16)!important;animation:none!important;transition:none!important}\
.accordion-featured>a::before,.accordion-featured>a::after{animation:none!important;transition:none!important}\
.accordion-featured img{display:block!important;width:100%!important;height:100%!important;object-fit:contain!important;padding:0!important;border-radius:15px!important;opacity:1!important;visibility:visible!important;transform:none!important;filter:none!important;animation:none!important;transition:none!important;background:#090b10!important;backface-visibility:hidden!important}\
.accordion-item.open .accordion-featured img{opacity:1!important;transform:none!important;filter:none!important;animation:none!important;transition:none!important}\
.accordion-featured .accordion-trailer{padding:0!important;margin:0!important;align-self:center!important}\
@media(max-width:540px){.accordion-featured{grid-template-columns:92px minmax(0,1fr)!important;gap:12px!important;align-items:start!important;padding:8px 20px 10px!important}.accordion-featured>a{width:92px!important;max-width:92px!important;border-radius:15px!important}.accordion-featured img{border-radius:12px!important}.accordion-featured .accordion-trailer{font-size:.86rem!important;line-height:1.5!important}}';
document.head.appendChild(style);

/* Важно: src обложек здесь НЕ меняем. Любая подмена после загрузки страницы
   давала визуальное мерцание при первом раскрытии карточки. */
document.querySelectorAll('.accordion-item').forEach(function(item){
  item.removeAttribute('data-reveal');
  item.style.opacity='1';
  item.style.transform='none';
  var img=item.querySelector('.accordion-featured img');
  if(img){
    img.loading='eager';
    img.decoding='async';
    img.style.opacity='1';
    img.style.visibility='visible';
  }
});

var items=Array.prototype.slice.call(document.querySelectorAll('.accordion-item'));if(!items.length)return;
var searchInput=document.getElementById('artSearch'),clearBtn=document.getElementById('artClear'),resetBtn=document.getElementById('artReset'),countEl=document.getElementById('artCount'),noRes=document.getElementById('artNoRes');
var catBtns=Array.prototype.slice.call(document.querySelectorAll('.cat-btn')),activeCat='all';
function plural(n){var n10=n%10,n100=n%100;if(n10===1&&n100!==11)return'статья';if(n10>=2&&n10<=4&&(n100<12||n100>14))return'статьи';return'статей';}
function closeItem(item){var h=item.querySelector('.accordion-header'),c=item.querySelector('.accordion-content');item.classList.remove('open');if(h){h.classList.remove('active');h.setAttribute('aria-expanded','false');}if(c){c.classList.remove('active');c.style.maxHeight='';}}
function applyFilter(){var q=searchInput?(searchInput.value||'').trim().toLowerCase():'';if(clearBtn)clearBtn.style.display=q?'grid':'none';var visible=0;items.forEach(function(item){var text=(item.textContent||'').toLowerCase(),cat=item.dataset.cat||'',show=(!q||text.indexOf(q)!==-1)&&(activeCat==='all'||cat===activeCat);item.hidden=!show;if(show)visible++;else closeItem(item);});if(countEl)countEl.innerHTML=q||activeCat!=='all'?'Найдено: <b>'+visible+'</b> '+plural(visible)+' из '+items.length:'Показано: <b>'+visible+'</b> из '+items.length+' статей';if(noRes)noRes.style.display=visible?'none':'block';}
if(searchInput)searchInput.addEventListener('input',applyFilter);if(clearBtn)clearBtn.addEventListener('click',function(){if(searchInput){searchInput.value='';searchInput.focus();}applyFilter();});if(resetBtn)resetBtn.addEventListener('click',function(){if(searchInput)searchInput.value='';activeCat='all';catBtns.forEach(function(b){b.classList.toggle('on',b.dataset.cat==='all');});applyFilter();});
catBtns.forEach(function(btn){btn.addEventListener('click',function(){activeCat=btn.dataset.cat||'all';catBtns.forEach(function(b){b.classList.toggle('on',b===btn);});applyFilter();});});
items.forEach(function(item){var header=item.querySelector('.accordion-header'),content=item.querySelector('.accordion-content');if(!header||!content)return;header.setAttribute('aria-expanded','false');header.addEventListener('click',function(){var was=header.classList.contains('active');items.forEach(closeItem);if(!was&&!item.hidden){item.classList.add('open');header.classList.add('active');header.setAttribute('aria-expanded','true');content.classList.add('active');content.style.maxHeight=(content.scrollHeight+80)+'px';}});var collapse=item.querySelector('.btn-collapse');if(collapse)collapse.addEventListener('click',function(e){e.preventDefault();closeItem(item);header.focus();});});
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){document.querySelectorAll('.accordion-header.active').forEach(function(h){var c=h.nextElementSibling;if(c)c.style.maxHeight=(c.scrollHeight+80)+'px';});},120);},{passive:true});
applyFilter();
})();