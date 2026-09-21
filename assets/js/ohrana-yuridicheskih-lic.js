(function(){
'use strict';
var wrap=document.getElementById('holoShield');
var canvas=document.getElementById('holoShieldCanvas');
if(!wrap||!canvas||!canvas.getContext)return;
var ctx=canvas.getContext('2d');
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var dpr=Math.min(window.devicePixelRatio||1,2),w=0,h=0,cx=0,cy=0,r=0,raf=0,t0=performance.now(),boostUntil=0,inView=true;
var logo=new Image(),logoReady=false;
logo.onload=function(){logoReady=true;};
logo.onerror=function(){logoReady=false;};
logo.src='/images/schit.png';
function resize(){
  var rect=wrap.getBoundingClientRect();
  w=Math.max(280,Math.round(rect.width));h=Math.max(280,Math.round(rect.height||rect.width));
  canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);canvas.style.width=w+'px';canvas.style.height=h+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);cx=w/2;cy=h/2;r=Math.min(w,h)*.31;
}
function shieldPath(scale){
  var s=scale||1;ctx.beginPath();ctx.moveTo(cx,cy-r*1.18*s);ctx.bezierCurveTo(cx+r*.7*s,cy-r*.9*s,cx+r*.92*s,cy-r*.5*s,cx+r*.72*s,cy+r*.28*s);ctx.bezierCurveTo(cx+r*.53*s,cy+r*.82*s,cx+r*.12*s,cy+r*1.08*s,cx,cy+r*1.2*s);ctx.bezierCurveTo(cx-r*.12*s,cy+r*1.08*s,cx-r*.53*s,cy+r*.82*s,cx-r*.72*s,cy+r*.28*s);ctx.bezierCurveTo(cx-r*.92*s,cy-r*.5*s,cx-r*.7*s,cy-r*.9*s,cx,cy-r*1.18*s);ctx.closePath();
}
function draw(now){
  var t=now-t0,boost=t<boostUntil;
  ctx.clearRect(0,0,w,h);
  var glow=ctx.createRadialGradient(cx,cy,r*.15,cx,cy,r*1.45);glow.addColorStop(0,'rgba(245,227,179,'+(boost?.2:.11)+')');glow.addColorStop(.55,'rgba(232,200,122,'+(boost?.1:.045)+')');glow.addColorStop(1,'rgba(232,200,122,0)');ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
  ctx.save();shieldPath(1.08);ctx.strokeStyle='rgba(232,200,122,'+(boost?.72:.34)+')';ctx.lineWidth=1.2;ctx.shadowColor='rgba(232,200,122,.55)';ctx.shadowBlur=boost?28:14;ctx.stroke();ctx.restore();
  ctx.save();shieldPath(1);ctx.clip();
  for(var i=0;i<15;i++){var yy=cy-r*1.05+((t*.07+i*r*.18)%(r*2.1));ctx.strokeStyle='rgba(245,227,179,'+(boost?.18:.08)+')';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(cx-r,yy);ctx.lineTo(cx+r,yy);ctx.stroke();}
  if(logoReady){var size=r*1.45;ctx.globalAlpha=boost?.92:.68;ctx.drawImage(logo,cx-size/2,cy-size/2,size,size);}else{ctx.fillStyle='rgba(232,200,122,.12)';shieldPath(.72);ctx.fill();}
  var scanY=cy-r+((t*.11)%(r*2));var grad=ctx.createLinearGradient(0,scanY-18,0,scanY+18);grad.addColorStop(0,'rgba(245,227,179,0)');grad.addColorStop(.5,'rgba(245,227,179,'+(boost?.7:.38)+')');grad.addColorStop(1,'rgba(245,227,179,0)');ctx.fillStyle=grad;ctx.fillRect(cx-r,scanY-18,r*2,36);ctx.restore();
  ctx.save();ctx.textAlign='right';ctx.font='700 '+Math.max(9,r*.07)+'px Manrope,system-ui,sans-serif';ctx.fillStyle='rgba(245,227,179,'+(boost?.95:.62)+')';ctx.fillText(boost?'ГЛУБОКИЙ СКАН':'СКАНИРОВАНИЕ',w-18,24);ctx.restore();
  if(!reduce&&inView)raf=requestAnimationFrame(draw);
}
function boost(){boostUntil=(performance.now()-t0)+2000;try{if(typeof ym==='function')ym(Number(document.body.dataset.metrikaId)||111882478,'reachGoal','holo_scan');}catch(e){}if(reduce)draw(performance.now());}
wrap.addEventListener('click',boost);wrap.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();boost();}});
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){resize();if(reduce)draw(performance.now());},100);},{passive:true});
if('IntersectionObserver'in window&&!reduce){new IntersectionObserver(function(entries){entries.forEach(function(entry){inView=entry.isIntersecting;if(inView&&!raf)raf=requestAnimationFrame(draw);if(!inView&&raf){cancelAnimationFrame(raf);raf=0;}});},{threshold:.05}).observe(wrap);}
resize();if(reduce)draw(performance.now());else raf=requestAnimationFrame(draw);
window.addEventListener('beforeunload',function(){if(raf)cancelAnimationFrame(raf);});
})();
