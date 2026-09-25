(function(){
'use strict';

/* 25 новых статей: нормальные компактные превью без reveal-мигания. */
var style=document.createElement('style');
style.id='article-catalog-fix-v2';
style.textContent='\
.accordion-container .accordion-item[data-reveal]{opacity:1!important;transform:none!important;transition:border-color .35s!important}\
.accordion-featured{display:grid!important;grid-template-columns:124px minmax(0,1fr)!important;gap:18px!important;align-items:center!important;padding:8px 24px 10px!important}\
.accordion-featured>a{display:block!important;width:124px!important;max-width:124px!important;aspect-ratio:2/3!important;overflow:hidden!important;border-radius:18px!important;border:2px solid transparent!important;background:linear-gradient(var(--panel),var(--panel)) padding-box,var(--gold-grad) border-box!important;box-shadow:0 10px 30px rgba(232,200,122,.16)!important}\
.accordion-featured img{display:block!important;width:100%!important;height:100%!important;object-fit:contain!important;padding:0!important;border-radius:15px!important;opacity:1!important;transform:none!important;filter:none!important;animation:none!important;transition:none!important;background:#090b10!important}\
.accordion-featured .accordion-trailer{padding:0!important;margin:0!important;align-self:center!important}\
@media(max-width:540px){.accordion-featured{grid-template-columns:92px minmax(0,1fr)!important;gap:12px!important;align-items:start!important;padding:8px 20px 10px!important}.accordion-featured>a{width:92px!important;max-width:92px!important;border-radius:15px!important}.accordion-featured img{border-radius:12px!important}.accordion-featured .accordion-trailer{font-size:.86rem!important;line-height:1.5!important}}';
document.head.appendChild(style);

/* В новых 25 статьях ставим более качественные тематические изображения,
   которые уже лежат в /images и используются на сайте. */
var coverMap={
  'chto-delat-esli-ohrannik-ne-vyshel-na-smenu.html':'/images/fizohrana-dva.jpg',
  'srok-zapuska-ohrany-novogo-obekta.html':'/images/tarif-post-fizicheskoy-ohrany.webp',
  'zamena-ohrannika-po-trebovaniyu-zakazchika.html':'/images/stati-smena-chop.webp',
  'otvetstvennost-choo-za-propazhu-imushchestva.html':'/images/vnutrennij-vor-sklad.jpg',
  'dokumenty-choo-do-nachala-ohrany.html':'/images/foto-dogovor.jpg',
  'zhurnaly-i-dokumenty-na-postu-ohrany.html':'/images/stati-tz-ohrana.webp',
  'imeet-li-ohrannik-pravo-osmatrivat-sumki-avtomobil.html':'/images/ohrannik-vahter-kontroler.webp',
  'mozhet-li-chastnyy-ohrannik-zaderzhat-narushitelya.html':'/images/security-2.jpg',
  'posetitel-otkazyvaetsya-soblyudat-propusknoy-rezhim.html':'/images/security-3.jpg',
  'dopusk-podryadchikov-kurerov-vremennyh-rabotnikov.html':'/images/kontrol-dostupa-skud.webp',
  'poteryan-propusk-klyuch-karta-dostupa.html':'/images/kontrol-dostupa-skud.webp',
  'kontrol-vezda-vyezda-transporta.html':'/images/ohrana-parkovok.jpg',
  'ohrana-pogruzki-i-razgruzki.html':'/images/ohrana-sklada.jpg',
  'kogda-nuzhen-starshiy-smeny-ohrany.html':'/images/stati-kolichestvo-ohrannikov.webp',
  'otvetstvennost-choo-i-sluzhby-bezopasnosti-zakazchika.html':'/images/stati-kontrol-chop.webp',
  'ohrana-pri-otklyuchenii-elektrichestva-interneta-skud.html':'/images/tehnicheskaya-ohrana.jpg',
  'zashchita-ohrannoy-signalizacii-ot-glusheniya.html':'/images/pultovaya-ohrana.webp',
  'kak-umenshit-lozhnye-trevogi.html':'/images/motion-sensor.jpg',
  'nuzhna-li-trevozhnaya-knopka-esli-est-kamery.html':'/images/pultovaya-ohrana.jpg',
  'kak-bystro-dolzhna-priehat-gbr.html':'/images/tarif-pultovaya-ohrana-gbr.webp',
  'usilenie-ohrany-nochyu-vyhodnye-prazdniki.html':'/images/nochnaya-ohrana.jpg',
  'ohrana-obekta-vo-vremya-remonta-pereezda.html':'/images/ohrana-strojki.jpg',
  'kak-zashchitit-dachu-zimoy.html':'/images/ohrana-dach-kottedzhey.webp',
  'kak-usilit-ohranu-sklada-v-pikovyy-sezon.html':'/images/1ohrana-skladov.jpg',
  'chop-choo-vnevedomstvennaya-ohrana-raznica.html':'/images/chop-company.jpg'
};

document.querySelectorAll('.accordion-item').forEach(function(item){
  item.removeAttribute('data-reveal');
  item.style.opacity='1';
  item.style.transform='none';
  var link=item.querySelector('.accordion-featured>a[href]');
  var img=item.querySelector('.accordion-featured img');
  if(!link||!img)return;
  var file=(link.getAttribute('href')||'').split('/').pop();
  if(coverMap[file]){
    img.src=coverMap[file];
    img.removeAttribute('srcset');
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