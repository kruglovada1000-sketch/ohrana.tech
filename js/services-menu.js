/* Services disclosure enhances a real catalogue link; no header replacement. */
(function(){
 'use strict';

 // Shared visual regression fixes for the current site shell.
 // This stylesheet is intentionally scoped to the affected visuals only.
 if(!document.querySelector('link[data-visual-fixes="20260924"]')){
  var visualFixes=document.createElement('link');
  visualFixes.rel='stylesheet';
  visualFixes.href='/css/visual-fixes-20260924.css?v=20260924-1';
  visualFixes.dataset.visualFixes='20260924';
  document.head.appendChild(visualFixes);
 }

 // Restore the real company photograph on homepage section 01.
 if(location.pathname==='/'||location.pathname==='/index.html'){
  var aboutImage=document.querySelector('#about .about-visual img');
  if(aboutImage){
   aboutImage.src='/images/chop-company.jpg';
   aboutImage.alt='ЧОО «Рускорпорация» — охрана объектов и бизнеса';
  }
 }

 // Price carousel uses the transparent brand shield, never the baked-background version.
 var tariffShields=document.querySelectorAll('.price-tariffs .tariff-shield');
 tariffShields.forEach(function(shield){
  shield.src='/images/schit.png';
  shield.removeAttribute('width');
  shield.removeAttribute('height');
 });

 var group=document.querySelector('#siteNav .services-nav');
 if(!group||group.dataset.servicesBound)return;
 group.dataset.servicesBound='1';
 var button=group.querySelector('.services-nav-toggle');
 var panel=group.querySelector('.services-panel');
 var nav=document.getElementById('siteNav');
 var mq=window.matchMedia('(min-width:1101px)');
 function setOpen(open){button.setAttribute('aria-expanded',String(open));panel.hidden=!open;}
 button.addEventListener('click',function(){setOpen(panel.hidden);});
 group.addEventListener('mouseenter',function(){if(mq.matches)setOpen(true);});
 group.addEventListener('mouseleave',function(){if(mq.matches&&!group.contains(document.activeElement))setOpen(false);});
 group.addEventListener('focusout',function(){setTimeout(function(){if(!group.contains(document.activeElement))setOpen(false);},0);});
 group.addEventListener('keydown',function(e){
  if(e.key==='Escape'){e.preventDefault();setOpen(false);button.focus();}
  if(e.key==='ArrowDown'&&e.target!==panel&& !panel.contains(e.target)){e.preventDefault();setOpen(true);panel.querySelector('a').focus();}
 });
 document.addEventListener('click',function(e){if(!group.contains(e.target))setOpen(false);});
 panel.addEventListener('click',function(e){if(e.target.closest('a'))setOpen(false);});
 new MutationObserver(function(){if(!mq.matches&&!nav.classList.contains('open'))setOpen(false);}).observe(nav,{attributes:true,attributeFilter:['class']});
 if(mq.addEventListener)mq.addEventListener('change',function(){setOpen(false);});
 else mq.addListener(function(){setOpen(false);});
 setOpen(false);

 // Service-specific hero images while service pages are being completed.
 if(location.pathname==='/uslugi/voditel-telohranitel/'||location.pathname==='/uslugi/voditel-telohranitel'){
  var hero=document.querySelector('.service-photo-slot img');
  if(hero){
   hero.src='/images/voditel-telohranitel.webp';
   hero.alt='Водитель-телохранитель';
   hero.width=1024;
   hero.height=1536;
  }
 }
})();