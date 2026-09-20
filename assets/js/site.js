(function(){
'use strict';
var root=document.documentElement;
var body=document.body;
var metrikaId=Number(body&&body.dataset?body.dataset.metrikaId:0)||111882478;
function goal(name){try{if(typeof ym==='function')ym(metrikaId,'reachGoal',name);}catch(e){}}
document.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;var href=a.getAttribute('href')||'';if(href.indexOf('tel:')===0)goal('click_phone');if(href.indexOf('wa.me')>-1)goal('click_whatsapp');if(href.indexOf('t.me')>-1)goal('click_telegram');});
var progress=document.getElementById('progress');if(progress){window.addEventListener('scroll',function(){var h=root;var d=h.scrollHeight-h.clientHeight;progress.style.width=(d>0?(h.scrollTop/d*100):0)+'%';},{passive:true});}
var burger=document.getElementById('burger'),nav=document.getElementById('siteNav');if(burger&&nav){burger.addEventListener('click',function(){var open=nav.classList.toggle('open');burger.classList.toggle('open',open);burger.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');burger.classList.remove('open');burger.setAttribute('aria-expanded','false');});});}
if(nav){var path=location.pathname.replace(/index\.html$/,'');nav.querySelectorAll('a').forEach(function(a){var href=(a.getAttribute('href')||'').replace(/index\.html$/,'');if(href==='/'?path==='/':path.indexOf(href)===0)a.classList.add('active');});}
var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;var reveal=document.querySelectorAll('[data-reveal]');if('IntersectionObserver'in window&&!rm){var io=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){entry.target.classList.add('in');io.unobserve(entry.target);}});},{threshold:.1});reveal.forEach(function(el){io.observe(el);});setTimeout(function(){reveal.forEach(function(el){el.classList.add('in');});},2000);}else{reveal.forEach(function(el){el.classList.add('in');});}
function setFaqState(item,open){if(!item)return;var q=item.querySelector('.faq-q'),answer=item.querySelector('.faq-a');item.classList.toggle('open',!!open);if(q)q.setAttribute('aria-expanded',String(!!open));if(answer)answer.style.maxHeight=open?answer.scrollHeight+'px':'';}
document.querySelectorAll('.faq-item').forEach(function(item){setFaqState(item,item.classList.contains('open'));});
var faq=document.querySelectorAll('.faq-item .faq-q');faq.forEach(function(q){
  if(q.dataset.sharedFaqBound==='1')return;
  q.dataset.sharedFaqBound='1';
  q.addEventListener('click',function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var item=q.closest('.faq-item');
    var shouldOpen=!!item&&!item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(function(openItem){if(openItem!==item)setFaqState(openItem,false);});
    setFaqState(item,shouldOpen);
  },true);
});

/* Shared flip-card accessibility for pages that use CSS hover on desktop. */
var finePointer=window.matchMedia&&window.matchMedia('(hover:hover) and (pointer:fine)').matches;
document.querySelectorAll('.flip').forEach(function(card){
  if(card.dataset.sharedFlipBound==='1')return;
  card.dataset.sharedFlipBound='1';
  if(!finePointer){card.addEventListener('click',function(e){if(e.target.closest('a,button,input,select,textarea,label'))return;card.classList.toggle('flipped');});}
  card.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){if(e.target!==card)return;e.preventDefault();card.classList.toggle('flipped');}});
});

var chatBtn=document.getElementById('chatBtn'),chatPanel=document.getElementById('chatPanel');if(chatBtn&&chatPanel){chatBtn.addEventListener('click',function(e){e.stopPropagation();chatPanel.classList.toggle('open');});document.addEventListener('click',function(e){if(!chatPanel.contains(e.target)&&!chatBtn.contains(e.target))chatPanel.classList.remove('open');});}
var filter=document.getElementById('priceFilter');if(filter){filter.addEventListener('input',function(){var q=(filter.value||'').trim().toLowerCase();document.querySelectorAll('[data-price-row]').forEach(function(row){var text=(row.textContent||'').toLowerCase();row.hidden=!!q&&text.indexOf(q)===-1;});});}
var typeSelect=document.getElementById('priceType');if(typeSelect){typeSelect.addEventListener('change',function(){var v=typeSelect.value;document.querySelectorAll('[data-price-row]').forEach(function(row){row.hidden=!!v&&row.dataset.kind!==v;});});}

var counters=document.querySelectorAll('[data-value]');
function setCounterValue(el,value){var suffix=el.getAttribute('data-suffix')||'';var decimals=(String(el.getAttribute('data-value')||'').split('.')[1]||'').length;var text=decimals?Number(value).toFixed(decimals):Math.round(Number(value)).toLocaleString('ru-RU');el.textContent=text+suffix;}
function runCounter(el){if(el.dataset.counterDone==='1')return;el.dataset.counterDone='1';var target=Number(el.getAttribute('data-value'));if(!Number.isFinite(target)){return;}if(rm){setCounterValue(el,target);return;}var start=performance.now(),duration=1100;function tick(now){var p=Math.min(1,(now-start)/duration);var eased=1-Math.pow(1-p,3);setCounterValue(el,target*eased);if(p<1)requestAnimationFrame(tick);}requestAnimationFrame(tick);}
if(counters.length){if('IntersectionObserver'in window&&!rm){var counterIo=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){runCounter(entry.target);counterIo.unobserve(entry.target);}});},{threshold:.35});counters.forEach(function(el){counterIo.observe(el);});}else{counters.forEach(runCounter);}}

function nativeSubmit(form){try{HTMLFormElement.prototype.submit.call(form);}catch(e){form.submit();}}
function successNodeFor(form){
  var local=form.parentElement&&form.parentElement.querySelector('.form-ok,.form-success,[data-form-success]');
  var ok=document.getElementById('formOk')||local;
  if(ok)return ok;
  ok=document.createElement('div');
  ok.className='form-ok shared-form-ok';
  ok.setAttribute('role','status');
  ok.setAttribute('aria-live','polite');
  var heading=document.createElement('h3');heading.textContent='Заявка отправлена!';
  var text=document.createElement('p');text.textContent='Спасибо. Мы получили заявку и свяжемся с вами.';
  ok.appendChild(heading);ok.appendChild(text);
  (form.parentElement||form).appendChild(ok);
  return ok;
}
document.querySelectorAll('form[action*="formspree.io"]').forEach(function(form){
  if(form.dataset.sharedFormBound==='1')return;
  form.dataset.sharedFormBound='1';
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var button=form.querySelector('button[type="submit"],input[type="submit"]');
    var oldText=button?(button.tagName==='INPUT'?button.value:button.textContent):'';
    if(button){button.disabled=true;if(button.tagName==='INPUT')button.value='Отправляем…';else button.textContent='Отправляем…';}
    var data=new FormData(form);
    fetch(form.action,{method:'POST',body:data,headers:{'Accept':'application/json'}})
      .then(function(res){
        if(!res.ok){if(button){button.disabled=false;if(button.tagName==='INPUT')button.value=oldText;else button.textContent=oldText;}nativeSubmit(form);return;}
        goal('form_submit');goal('lead_form_ok');
        form.style.display='none';
        var ok=successNodeFor(form);ok.style.display='block';ok.hidden=false;
      })
      .catch(function(){if(button){button.disabled=false;if(button.tagName==='INPUT')button.value=oldText;else button.textContent=oldText;}nativeSubmit(form);});
  });
});

if(!rm&&window.matchMedia&&!window.matchMedia('(hover:none)').matches){var dot=document.querySelector('.cursor-dot'),ring=document.querySelector('.cursor-ring');if(dot&&ring){var mx=innerWidth/2,my=innerHeight/2,rx=mx,ry=my;document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;dot.style.transform='translate('+(mx-3)+'px,'+(my-3)+'px)';},{passive:true});(function loop(){rx+=(mx-rx)*.16;ry+=(my-ry)*.16;ring.style.transform='translate('+(rx-ring.offsetWidth/2)+'px,'+(ry-ring.offsetHeight/2)+'px)';requestAnimationFrame(loop);})();}}
/* pricing-carousel-v2 */
document.querySelectorAll('[data-price-carousel]').forEach(function(carousel){
  var viewport=carousel.querySelector('[data-carousel-viewport]'),cards=Array.prototype.slice.call(carousel.querySelectorAll('[data-tariff-card]')),prev=carousel.querySelector('[data-carousel-prev]'),next=carousel.querySelector('[data-carousel-next]'),dots=Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-dot]'));
  if(!viewport||!cards.length)return;
  var activePage=0,scrollTick=false;
  function perPage(){return window.matchMedia&&window.matchMedia('(max-width:700px)').matches?1:2;}
  function pageCount(){return Math.ceil(cards.length/perPage());}
  function wrapPage(i){var total=pageCount();return ((i%total)+total)%total;}
  function cardIndexForPage(page){return Math.min(wrapPage(page)*perPage(),cards.length-1);}
  function setUi(page){
    activePage=wrapPage(page);
    var total=pageCount();
    dots.forEach(function(dot,index){var visible=index<total;dot.hidden=!visible;dot.setAttribute('aria-pressed',String(visible&&index===activePage));});
    if(prev)prev.disabled=false;if(next)next.disabled=false;
  }
  function nearest(){
    var left=viewport.scrollLeft,total=pageCount(),best=0,distance=Infinity;
    for(var page=0;page<total;page++){var card=cards[cardIndexForPage(page)],d=Math.abs(card.offsetLeft-left);if(d<distance){distance=d;best=page;}}
    setUi(best);
  }
  function goPage(page){
    var targetPage=wrapPage(page),wrapped=Math.abs(targetPage-activePage)>1,targetCard=cards[cardIndexForPage(targetPage)];
    setUi(targetPage);
    viewport.scrollTo({left:targetCard.offsetLeft,behavior:(rm||wrapped)?'auto':'smooth'});
  }
  if(prev)prev.addEventListener('click',function(){goPage(activePage-1);});
  if(next)next.addEventListener('click',function(){goPage(activePage+1);});
  dots.forEach(function(dot,index){dot.addEventListener('click',function(){if(index<pageCount())goPage(index);});});
  viewport.addEventListener('scroll',function(){if(scrollTick)return;scrollTick=true;requestAnimationFrame(function(){nearest();scrollTick=false;});},{passive:true});
  viewport.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){e.preventDefault();goPage(activePage-1);}else if(e.key==='ArrowRight'){e.preventDefault();goPage(activePage+1);}});
  window.addEventListener('resize',function(){setUi(Math.min(activePage,pageCount()-1));goPage(activePage);},{passive:true});
  setUi(0);
});
})();
