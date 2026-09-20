(function(){
'use strict';

/* Personal-security price calculator. Form submission is handled by shared site.js. */
var guardsDisplay=document.getElementById('guards-count');
var hoursDisplay=document.getElementById('hours-count');
var totalDisplay=document.getElementById('total-price');
var guardTypeSelect=document.getElementById('calc-guard-type');
var guardsInput=document.getElementById('guards-input');
var hoursInput=document.getElementById('hours-input');
var totalInput=document.getElementById('total-input');
var rates={
  'Эконом — 35 000 ₽ / 8 ч':35000,
  'Стандарт — 40 000 ₽ / 8 ч':40000,
  'VIP — 50 000 ₽ / 8 ч (с авто)':50000
};
var guards=guardsDisplay?Math.max(1,parseInt(guardsDisplay.textContent,10)||1):1;
var hours=hoursDisplay?Math.max(4,parseInt(hoursDisplay.textContent,10)||4):4;
function updatePrice(){
  if(!guardTypeSelect||!totalDisplay)return;
  var rate=rates[guardTypeSelect.value]||rates['Стандарт — 40 000 ₽ / 8 ч'];
  var total=Math.round(guards*hours*(rate/8));
  totalDisplay.textContent=total.toLocaleString('ru-RU')+' ₽';
  if(guardsInput)guardsInput.value=String(guards);
  if(hoursInput)hoursInput.value=String(hours);
  if(totalInput)totalInput.value=String(total);
}
document.querySelectorAll('.stepper button[data-target][data-dir]').forEach(function(btn){
  btn.addEventListener('click',function(){
    var dir=parseInt(btn.dataset.dir,10)||0;
    if(btn.dataset.target==='guards'){
      guards=Math.max(1,guards+dir);
      if(guardsDisplay)guardsDisplay.textContent=String(guards);
    }else if(btn.dataset.target==='hours'){
      hours=Math.max(4,hours+dir);
      if(hoursDisplay)hoursDisplay.textContent=String(hours);
    }
    updatePrice();
  });
});
if(guardTypeSelect)guardTypeSelect.addEventListener('change',updatePrice);
updatePrice();

/* Decorative threat radar, isolated from the shared shell. */
var canvas=document.getElementById('radarCanvas');
if(!canvas||!canvas.getContext)return;
var ctx=canvas.getContext('2d');
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var w=canvas.width||600,h=canvas.height||600,cx=w/2,cy=h/2,r=Math.min(w,h)*.38,raf=0,start=performance.now(),inView=true;
var contacts=[
  {a:.38,d:.72,p:.2},{a:1.7,d:.48,p:1.3},{a:2.75,d:.83,p:2.1},{a:4.1,d:.58,p:.7},{a:5.25,d:.9,p:2.8}
];
function ring(radius,alpha){ctx.beginPath();ctx.arc(cx,cy,radius,0,Math.PI*2);ctx.strokeStyle='rgba(232,200,122,'+alpha+')';ctx.lineWidth=1;ctx.stroke();}
function draw(now){
  var t=(now-start)/1000;
  ctx.clearRect(0,0,w,h);
  var bg=ctx.createRadialGradient(cx,cy,0,cx,cy,r*1.25);bg.addColorStop(0,'rgba(232,200,122,.08)');bg.addColorStop(.75,'rgba(232,200,122,.025)');bg.addColorStop(1,'rgba(232,200,122,0)');ctx.fillStyle=bg;ctx.fillRect(0,0,w,h);
  for(var i=1;i<=4;i++)ring(r*i/4,.13+i*.015);
  ctx.strokeStyle='rgba(232,200,122,.12)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(cx-r,cy);ctx.lineTo(cx+r,cy);ctx.moveTo(cx,cy-r);ctx.lineTo(cx,cy+r);ctx.stroke();
  var angle=reduce?-.7:t*1.75;
  var sweep=ctx.createRadialGradient(cx,cy,0,cx,cy,r);sweep.addColorStop(0,'rgba(245,227,179,.20)');sweep.addColorStop(1,'rgba(232,200,122,0)');ctx.save();ctx.translate(cx,cy);ctx.rotate(angle);ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,r,-.36,0);ctx.closePath();ctx.fillStyle=sweep;ctx.fill();ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(r,0);ctx.strokeStyle='rgba(245,227,179,.82)';ctx.lineWidth=2;ctx.shadowColor='rgba(232,200,122,.7)';ctx.shadowBlur=14;ctx.stroke();ctx.restore();
  contacts.forEach(function(c,index){
    var x=cx+Math.cos(c.a)*r*c.d,y=cy+Math.sin(c.a)*r*c.d;
    var pulse=reduce?1:(.5+.5*Math.sin(t*3.2+c.p));
    ctx.beginPath();ctx.arc(x,y,4+pulse*3,0,Math.PI*2);ctx.fillStyle='rgba(245,227,179,'+(.5+pulse*.35)+')';ctx.shadowColor='rgba(232,200,122,.9)';ctx.shadowBlur=10+pulse*10;ctx.fill();ctx.shadowBlur=0;
    if(index<3){ctx.beginPath();ctx.arc(x,y,11+pulse*8,0,Math.PI*2);ctx.strokeStyle='rgba(232,200,122,'+(.16+pulse*.18)+')';ctx.stroke();}
  });
  ctx.fillStyle='rgba(245,227,179,.7)';ctx.font='700 15px Manrope,system-ui,sans-serif';ctx.textAlign='left';ctx.fillText('360°  КОНТРОЛЬ',24,32);
  ctx.fillStyle='rgba(142,148,163,.7)';ctx.font='600 11px Manrope,system-ui,sans-serif';ctx.fillText('СКАНИРОВАНИЕ УГРОЗ',24,51);
  if(!reduce&&inView)raf=requestAnimationFrame(draw);else raf=0;
}
if('IntersectionObserver'in window&&!reduce){new IntersectionObserver(function(entries){entries.forEach(function(entry){inView=entry.isIntersecting;if(inView&&!raf)raf=requestAnimationFrame(draw);if(!inView&&raf){cancelAnimationFrame(raf);raf=0;}});},{threshold:.05}).observe(canvas);}
if(reduce)draw(performance.now());else raf=requestAnimationFrame(draw);
window.addEventListener('beforeunload',function(){if(raf)cancelAnimationFrame(raf);});
})();
