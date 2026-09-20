(function(){
'use strict';
var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(rm)return;
if(window.matchMedia&&window.matchMedia('(hover:none)').matches)return;
var cv=document.getElementById('sparkCanvas');
if(!cv||!cv.getContext)return;
var ctx=cv.getContext('2d');
var W=cv.width,H=cv.height,cx=W/2,cy=H/2+6,RX=100,RY=116;
function shieldPath(t){var a=t*Math.PI*2;var y=Math.sin(a);var x=Math.cos(a);var k=y>0?(1-y*.45):1;return{x:cx+x*RX*k,y:cy+y*RY};}
var head=0,sparks=[],TAILN=26,frame=0;
function spawnSpark(p){sparks.push({x:p.x,y:p.y,vx:(Math.random()-.5)*1.8,vy:(Math.random()-.5)*1.8-.7,life:1,decay:.018+Math.random()*.03,r:.7+Math.random()*1.8});}
function draw(){
  ctx.clearRect(0,0,W,H);
  for(var i=0;i<TAILN;i++){
    var tt=(head-(i+1)*.012+1)%1,p=shieldPath(tt),fade=1-i/TAILN;
    ctx.beginPath();ctx.arc(p.x,p.y,1.2+fade*1.9,0,7);ctx.fillStyle='rgba(232,200,122,'+(0.05+fade*.35)+')';ctx.fill();
  }
  var hp=shieldPath(head);var grd=ctx.createRadialGradient(hp.x,hp.y,0,hp.x,hp.y,20);
  grd.addColorStop(0,'rgba(255,240,200,.95)');grd.addColorStop(.35,'rgba(245,227,179,.55)');grd.addColorStop(1,'rgba(232,200,122,0)');
  ctx.beginPath();ctx.arc(hp.x,hp.y,20,0,7);ctx.fillStyle=grd;ctx.fill();
  for(var s=sparks.length-1;s>=0;s--){var sp=sparks[s];sp.x+=sp.vx;sp.y+=sp.vy;sp.vy+=.022;sp.life-=sp.decay;if(sp.life<=0){sparks.splice(s,1);continue;}ctx.beginPath();ctx.arc(sp.x,sp.y,sp.r*sp.life,0,7);ctx.fillStyle='rgba(255,220,150,'+sp.life+')';ctx.fill();}
  frame++;head=(head+.0035+Math.random()*.002)%1;if(frame%3===0)spawnSpark(hp);requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
})();
