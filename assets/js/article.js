(function(){
'use strict';

/* Статьи: одна спокойная обложка — без стелс-мигания, призрака и скан-линий. */
var style=document.createElement('style');
style.id='article-cover-fix-v2';
style.textContent='\
.shield-wrap{max-width:400px!important}\
.shield-wrap::before{inset:-12px!important;border-radius:32px!important;background:linear-gradient(135deg,rgba(245,227,179,.16),rgba(232,200,122,.06))!important;filter:blur(34px)!important}\
.shield-box{position:relative!important;width:100%!important;aspect-ratio:3/4!important;border-radius:26px!important;overflow:hidden!important;border:2px solid transparent!important;background:linear-gradient(#090b10,#090b10) padding-box,linear-gradient(135deg,#f5e3b3 0%,#e8c87a 48%,#a97f2f 100%) border-box!important;box-shadow:0 24px 70px rgba(0,0,0,.48),0 0 30px rgba(232,200,122,.13)!important}\
.shield-box .shield-active{display:block!important;position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:contain!important;padding:10px!important;border-radius:23px!important;opacity:1!important;filter:none!important;mix-blend-mode:normal!important;transform:none!important;animation:none!important;transition:none!important;background:#090b10!important}\
.shield-box .shield-ghost,.shield-box .shield-scan,.shield-box .shield-status{display:none!important;opacity:0!important;animation:none!important}\
@media(max-width:680px){.shield-wrap{max-width:300px!important}.shield-box{border-radius:22px!important}.shield-box .shield-active{padding:7px!important;border-radius:19px!important}}';
document.head.appendChild(style);

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
var file=(location.pathname||'').split('/').pop();
var cover=coverMap[file];
if(cover){
  document.querySelectorAll('.shield-box img').forEach(function(img){img.src=cover;img.removeAttribute('srcset');});
}
var ghost=document.querySelector('.shield-ghost');if(ghost)ghost.remove();
var scan=document.querySelector('.shield-scan');if(scan)scan.remove();
var status=document.querySelector('.shield-status');if(status)status.remove();
var active=document.querySelector('.shield-active');if(active){active.style.animation='none';active.style.opacity='1';active.style.filter='none';}

var links=Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"],.article-toc a[href^="#"],[data-article-toc] a[href^="#"]'));
if(!links.length)return;
var pairs=[];
links.forEach(function(link){
  var href=link.getAttribute('href')||'';
  if(href.length<2)return;
  try{var target=document.getElementById(decodeURIComponent(href.slice(1)));if(target)pairs.push({link:link,target:target});}catch(e){}
});
if(!pairs.length)return;
function activate(target){
  pairs.forEach(function(pair){
    var on=pair.target===target;
    pair.link.classList.toggle('active',on);
    if(on)pair.link.setAttribute('aria-current','location');else pair.link.removeAttribute('aria-current');
  });
}
if('IntersectionObserver' in window){
  var current=null;
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){current=entry.target;activate(current);}
    });
  },{rootMargin:'-18% 0px -68% 0px',threshold:[0,.1,1]});
  pairs.forEach(function(pair){io.observe(pair.target);});
}else{
  var ticking=false;
  window.addEventListener('scroll',function(){
    if(ticking)return;ticking=true;
    requestAnimationFrame(function(){
      var best=pairs[0].target,bestDist=Infinity;
      pairs.forEach(function(pair){var d=Math.abs(pair.target.getBoundingClientRect().top-innerHeight*.24);if(d<bestDist){bestDist=d;best=pair.target;}});
      activate(best);ticking=false;
    });
  },{passive:true});
}
})();