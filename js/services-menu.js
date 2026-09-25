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

 // Header navigation refinement: full-width top + bottom gold lines on hover/active.
 // Kept here so the correction applies consistently to every page using the shared menu script.
 if(!document.getElementById('header-nav-v3')){
  var navStyle=document.createElement('style');
  navStyle.id='header-nav-v3';
  navStyle.textContent='\
@media(min-width:1101px){\
 #siteNav>.wrap>a{position:relative!important;overflow:visible!important}\
 #siteNav>.wrap>a::before,#siteNav>.wrap>a::after,#siteNav .services-nav>a.services-nav-link::before,#siteNav .services-nav>a.services-nav-link::after{content:""!important;display:block!important;position:absolute!important;height:2px!important;border-radius:2px!important;background:var(--gold,#E8C87A)!important;transform:scaleX(0)!important;transform-origin:center!important;transition:transform .28s var(--ease,cubic-bezier(.16,1,.3,1))!important;pointer-events:none!important}\
 #siteNav>.wrap>a::before{left:0!important;right:0!important;top:-6px!important}\
 #siteNav>.wrap>a::after{left:0!important;right:0!important;bottom:-6px!important}\
 #siteNav .services-nav>a.services-nav-link::before{left:0!important;right:-31px!important;top:-6px!important}\
 #siteNav .services-nav>a.services-nav-link::after{left:0!important;right:-31px!important;bottom:-6px!important}\
 #siteNav>.wrap>a:hover::before,#siteNav>.wrap>a:hover::after,#siteNav>.wrap>a:focus-visible::before,#siteNav>.wrap>a:focus-visible::after,#siteNav>.wrap>a.active::before,#siteNav>.wrap>a.active::after,#siteNav .services-nav:hover>a.services-nav-link::before,#siteNav .services-nav:hover>a.services-nav-link::after,#siteNav .services-nav:focus-within>a.services-nav-link::before,#siteNav .services-nav:focus-within>a.services-nav-link::after,#siteNav .services-nav.services-open>a.services-nav-link::before,#siteNav .services-nav.services-open>a.services-nav-link::after{transform:scaleX(1)!important}\
 #siteNav .services-panel::before{content:"";position:absolute;left:0;right:0;top:-14px;height:14px;background:transparent;pointer-events:auto}\
}\
';
  document.head.appendChild(navStyle);
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
 var closeTimer=null;

 function cancelClose(){
  if(closeTimer){clearTimeout(closeTimer);closeTimer=null;}
 }
 function setOpen(open){
  cancelClose();
  button.setAttribute('aria-expanded',String(open));
  panel.hidden=!open;
  group.classList.toggle('services-open',open);
 }
 function scheduleClose(){
  cancelClose();
  closeTimer=setTimeout(function(){
   closeTimer=null;
   if(mq.matches&&!group.matches(':hover')&&!panel.matches(':hover')&&!group.contains(document.activeElement))setOpen(false);
  },520);
 }

 button.addEventListener('click',function(){setOpen(panel.hidden);});
 group.addEventListener('mouseenter',function(){if(mq.matches){cancelClose();setOpen(true);}});
 group.addEventListener('mouseleave',function(){if(mq.matches)scheduleClose();});
 panel.addEventListener('mouseenter',function(){if(mq.matches)cancelClose();});
 panel.addEventListener('mouseleave',function(){if(mq.matches)scheduleClose();});
 group.addEventListener('focusin',cancelClose);
 group.addEventListener('focusout',function(){setTimeout(function(){if(!group.contains(document.activeElement))scheduleClose();},0);});
 group.addEventListener('keydown',function(e){
  if(e.key==='Escape'){e.preventDefault();setOpen(false);button.focus();}
  if(e.key==='ArrowDown'&&e.target!==panel&&!panel.contains(e.target)){e.preventDefault();setOpen(true);panel.querySelector('a').focus();}
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