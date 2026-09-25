/* Services disclosure enhances a real catalogue link; no header replacement. */
(function(){
 'use strict';

 // Shared visual regression fixes for the current site shell.
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

 // Price carousel uses the transparent brand shield.
 document.querySelectorAll('.price-tariffs .tariff-shield').forEach(function(shield){
  shield.src='/images/schit.png';
  shield.removeAttribute('width');
  shield.removeAttribute('height');
 });

 var group=document.querySelector('#siteNav .services-nav');
 if(!group||group.dataset.servicesBound)return;

 var button=group.querySelector('.services-nav-toggle');
 var panel=group.querySelector('.services-panel');
 var nav=document.getElementById('siteNav');
 if(!button||!panel||!nav)return;

 group.dataset.servicesBound='1';

 var mq=window.matchMedia('(min-width:1101px)');
 var closeTimer=null;
 var overGroup=false;
 var overPanel=false;

 function cancelClose(){
  if(closeTimer!==null){
   clearTimeout(closeTimer);
   closeTimer=null;
  }
 }

 function setOpen(open){
  cancelClose();
  button.setAttribute('aria-expanded',open?'true':'false');
  panel.hidden=!open;
  group.classList.toggle('services-open',open);
 }

 function scheduleClose(){
  cancelClose();
  closeTimer=setTimeout(function(){
   closeTimer=null;
   var focusInside=group.contains(document.activeElement);
   if(!overGroup&&!overPanel&&!focusInside){
    setOpen(false);
   }
  },650);
 }

 // Desktop: hover opens; leaving gives enough time to reach the dropdown.
 group.addEventListener('mouseenter',function(){
  overGroup=true;
  if(mq.matches)setOpen(true);
 });
 group.addEventListener('mouseleave',function(){
  overGroup=false;
  if(mq.matches)scheduleClose();
 });
 panel.addEventListener('mouseenter',function(){
  overPanel=true;
  if(mq.matches){cancelClose();setOpen(true);}
 });
 panel.addEventListener('mouseleave',function(){
  overPanel=false;
  if(mq.matches)scheduleClose();
 });

 // Click/touch remains available on desktop and mobile.
 button.addEventListener('click',function(e){
  e.preventDefault();
  setOpen(panel.hidden);
 });

 group.addEventListener('focusin',function(){
  cancelClose();
  if(mq.matches)setOpen(true);
 });
 group.addEventListener('focusout',function(){
  setTimeout(function(){
   if(!group.contains(document.activeElement))scheduleClose();
  },0);
 });

 group.addEventListener('keydown',function(e){
  if(e.key==='Escape'){
   e.preventDefault();
   setOpen(false);
   button.focus();
  }
  if(e.key==='ArrowDown'&&!panel.contains(e.target)){
   var firstLink=panel.querySelector('a');
   if(firstLink){
    e.preventDefault();
    setOpen(true);
    firstLink.focus();
   }
  }
 });

 document.addEventListener('click',function(e){
  if(!group.contains(e.target))setOpen(false);
 });
 panel.addEventListener('click',function(e){
  if(e.target.closest('a'))setOpen(false);
 });

 new MutationObserver(function(){
  if(!mq.matches&&!nav.classList.contains('open'))setOpen(false);
 }).observe(nav,{attributes:true,attributeFilter:['class']});

 function handleModeChange(){
  overGroup=false;
  overPanel=false;
  setOpen(false);
 }
 if(mq.addEventListener)mq.addEventListener('change',handleModeChange);
 else mq.addListener(handleModeChange);

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
