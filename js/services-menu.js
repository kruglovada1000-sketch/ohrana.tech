/* Services disclosure enhances a real catalogue link; no header replacement. */
(function(){
 'use strict';

 // Shared visual regression fixes for the current site shell.
 if(!document.querySelector('link[data-visual-fixes="20260924"]')){
  var visualFixes=document.createElement('link');
  visualFixes.rel='stylesheet';
  visualFixes.href='/css/visual-fixes-20260924.css?v=20260925-3';
  visualFixes.dataset.visualFixes='20260924';
  document.head.appendChild(visualFixes);
 }

 // Homepage proof block: urgent launch of physical security from the next day.
 (function addRapidDeployBlock(){
  var path=(location.pathname||'/').replace(/\/+$/,'')||'/';
  if(path!=='/'||document.getElementById('rapid-deploy'))return;

  var about=document.getElementById('about');
  if(!about)return;

  if(!document.querySelector('style[data-rapid-deploy="v1"]')){
   var rapidStyle=document.createElement('style');
   rapidStyle.dataset.rapidDeploy='v1';
   rapidStyle.textContent=`
#rapid-deploy{padding:56px 0 64px;position:relative;background:linear-gradient(180deg,rgba(232,200,122,.025),transparent 72%)}
#rapid-deploy .rapid-shell{position:relative;overflow:hidden;border:1px solid rgba(232,200,122,.26);border-radius:28px;background:linear-gradient(135deg,rgba(232,200,122,.08),rgba(13,17,24,.96) 42%,rgba(7,9,13,.98));box-shadow:0 28px 72px rgba(0,0,0,.28);padding:42px}
#rapid-deploy .rapid-shell::before{content:"";position:absolute;width:360px;height:360px;border-radius:50%;right:-120px;top:-180px;background:radial-gradient(circle,rgba(232,200,122,.14),transparent 68%);pointer-events:none}
#rapid-deploy .rapid-top{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.55fr);gap:34px;align-items:end;position:relative;z-index:1}
#rapid-deploy .rapid-kicker{display:inline-flex;align-items:center;gap:10px;margin-bottom:12px;color:var(--gold,#E8C87A);font-size:.76rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase}
#rapid-deploy .rapid-kicker::before{content:"";width:28px;height:1px;background:var(--gold,#E8C87A)}
#rapid-deploy h2{margin:0;font-family:var(--serif,'Cormorant',Georgia,serif);font-size:clamp(2rem,4vw,3.4rem);font-weight:500;line-height:1.03;color:var(--ink,#FFFDF7)}
#rapid-deploy h2 em{font-style:italic;color:var(--gold2,#F5E3B3);background:none;-webkit-text-fill-color:currentColor}
#rapid-deploy .rapid-lead{margin:16px 0 0;max-width:760px;color:var(--mut,#D4D7DE);font-size:1.02rem;line-height:1.75}
#rapid-deploy .rapid-badge{justify-self:end;display:flex;flex-direction:column;align-items:flex-start;min-width:230px;padding:20px 22px;border:1px solid rgba(232,200,122,.35);border-radius:18px;background:rgba(232,200,122,.08)}
#rapid-deploy .rapid-badge strong{font-family:var(--serif,'Cormorant',Georgia,serif);font-size:2.45rem;line-height:1;color:var(--gold2,#F5E3B3);font-weight:600}
#rapid-deploy .rapid-badge span{margin-top:8px;color:var(--ink,#FFFDF7);font-size:.88rem;line-height:1.45;font-weight:700}
#rapid-deploy .rapid-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:30px;position:relative;z-index:1}
#rapid-deploy .rapid-step{position:relative;padding:20px 20px 21px;border:1px solid rgba(242,238,228,.10);border-radius:17px;background:rgba(255,255,255,.025)}
#rapid-deploy .rapid-step-num{display:block;margin-bottom:10px;color:var(--gold,#E8C87A);font-size:.72rem;font-weight:800;letter-spacing:.16em}
#rapid-deploy .rapid-step b{display:block;color:var(--ink,#FFFDF7);font-size:1rem;margin-bottom:7px}
#rapid-deploy .rapid-step p{margin:0;color:var(--mut,#D4D7DE);font-size:.9rem;line-height:1.6}
#rapid-deploy .rapid-cases-title{display:flex;align-items:center;gap:12px;margin:30px 0 13px;color:var(--ink,#FFFDF7);font-size:.82rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;position:relative;z-index:1}
#rapid-deploy .rapid-cases-title::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,rgba(232,200,122,.35),transparent)}
#rapid-deploy .rapid-cases{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;position:relative;z-index:1}
#rapid-deploy .rapid-case{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;padding:20px;border:1px solid rgba(232,200,122,.20);border-radius:17px;background:rgba(232,200,122,.045)}
#rapid-deploy .rapid-case-mark{width:38px;height:38px;display:grid;place-items:center;border-radius:50%;background:var(--gold-grad,linear-gradient(115deg,#F5E3B3,#E8C87A,#B98F3E));color:#171003;font-weight:900;box-shadow:0 8px 20px rgba(232,200,122,.18)}
#rapid-deploy .rapid-case b{display:block;color:var(--gold2,#F5E3B3);font-size:1.02rem;margin-bottom:5px}
#rapid-deploy .rapid-case p{margin:0;color:var(--mut,#D4D7DE);font-size:.92rem;line-height:1.62}
#rapid-deploy .rapid-bottom{display:flex;align-items:center;justify-content:space-between;gap:22px;margin-top:26px;padding-top:22px;border-top:1px solid rgba(242,238,228,.09);position:relative;z-index:1}
#rapid-deploy .rapid-note{max-width:690px;margin:0;color:var(--mut,#D4D7DE);font-size:.78rem;line-height:1.55}
#rapid-deploy .rapid-cta{flex:none;display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:50px;padding:14px 24px;border-radius:999px;background:var(--gold-grad,linear-gradient(115deg,#F5E3B3,#E8C87A,#B98F3E));color:#171003!important;font-weight:800;font-size:.91rem;text-decoration:none;box-shadow:0 12px 32px rgba(232,200,122,.20);transition:transform .25s ease,box-shadow .25s ease}
#rapid-deploy .rapid-cta:hover{transform:translateY(-2px);box-shadow:0 16px 38px rgba(232,200,122,.30)}
html[data-theme="light"] #rapid-deploy{background:linear-gradient(180deg,rgba(169,127,47,.045),transparent 72%)}
html[data-theme="light"] #rapid-deploy .rapid-shell{background:linear-gradient(135deg,#FFF9EC,#FFFFFF 46%,#F5F1E9);border-color:rgba(169,127,47,.28);box-shadow:0 24px 60px rgba(69,49,20,.10)}
html[data-theme="light"] #rapid-deploy h2,html[data-theme="light"] #rapid-deploy .rapid-step b,html[data-theme="light"] #rapid-deploy .rapid-cases-title,html[data-theme="light"] #rapid-deploy .rapid-badge span{color:#111}
html[data-theme="light"] #rapid-deploy h2 em,html[data-theme="light"] #rapid-deploy .rapid-case b{color:#745015}
html[data-theme="light"] #rapid-deploy :where(.rapid-lead,.rapid-step p,.rapid-case p,.rapid-note){color:#34312D!important}
html[data-theme="light"] #rapid-deploy :where(.rapid-step,.rapid-case,.rapid-badge){background:rgba(255,255,255,.72);border-color:rgba(169,127,47,.22)}
@media(max-width:900px){#rapid-deploy .rapid-top{grid-template-columns:1fr}#rapid-deploy .rapid-badge{justify-self:start}#rapid-deploy .rapid-flow{grid-template-columns:1fr}#rapid-deploy .rapid-cases{grid-template-columns:1fr}}
@media(max-width:640px){#rapid-deploy{padding:38px 0 48px}#rapid-deploy .rapid-shell{padding:26px 20px;border-radius:22px}#rapid-deploy .rapid-badge{width:100%;min-width:0}#rapid-deploy .rapid-bottom{align-items:stretch;flex-direction:column}#rapid-deploy .rapid-cta{width:100%;min-height:56px;text-align:center}#rapid-deploy .rapid-case{grid-template-columns:auto minmax(0,1fr)}}
`;
   document.head.appendChild(rapidStyle);
  }

  var rapid=document.createElement('section');
  rapid.id='rapid-deploy';
  rapid.setAttribute('aria-labelledby','rapid-deploy-title');
  rapid.innerHTML=`
    <div class="wrap">
      <div class="rapid-shell">
        <div class="rapid-top">
          <div>
            <span class="rapid-kicker">Срочный запуск охраны</span>
            <h2 id="rapid-deploy-title">Позвонили сегодня — <em>пост может выйти завтра</em></h2>
            <p class="rapid-lead">Если объект нужно закрыть без паузы, после согласования задачи, графика и состава поста можем организовать вывод сотрудников охраны уже на следующий день.</p>
          </div>
          <div class="rapid-badge" aria-label="Срочный запуск от 24 часов">
            <strong>24 ч</strong>
            <span>от обращения до выхода поста при согласованных условиях</span>
          </div>
        </div>

        <div class="rapid-flow" aria-label="Как запускается срочная охрана">
          <div class="rapid-step"><span class="rapid-step-num">01 · ЗВОНОК</span><b>Получаем задачу</b><p>Уточняем объект, режим работы, количество сотрудников и требования к посту.</p></div>
          <div class="rapid-step"><span class="rapid-step-num">02 · СОГЛАСОВАНИЕ</span><b>Формируем решение</b><p>Согласовываем стоимость, график, обязанности и порядок выхода на объект.</p></div>
          <div class="rapid-step"><span class="rapid-step-num">03 · ВЫХОД</span><b>Выставляем пост</b><p>При наличии подходящего состава охрана приступает к работе уже на следующий день.</p></div>
        </div>

        <div class="rapid-cases-title">Реальные кейсы срочного запуска</div>
        <div class="rapid-cases">
          <article class="rapid-case">
            <span class="rapid-case-mark" aria-hidden="true">✓</span>
            <div><b>Складские объекты · Орехово-Зуево</b><p>После звонка и согласования условий посты физической охраны были подготовлены к выходу на следующий день.</p></div>
          </article>
          <article class="rapid-case">
            <span class="rapid-case-mark" aria-hidden="true">✓</span>
            <div><b>Томилино · складской объект на территории птицефабрики</b><p>Срочная задача по охране склада: состав поста сформирован с выводом сотрудников на следующий день.</p></div>
          </article>
        </div>

        <div class="rapid-bottom">
          <p class="rapid-note">Срок зависит от локации, режима поста, количества сотрудников и специальных требований. Возможность выхода на следующий день подтверждаем после короткого согласования задачи.</p>
          <a class="rapid-cta" href="tel:+79250474225">Нужен пост на завтра →</a>
        </div>
      </div>
    </div>`;
  about.parentNode.insertBefore(rapid,about);
 })();

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
   button.focus();
   setOpen(false);
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
