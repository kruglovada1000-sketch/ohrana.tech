(function(){
'use strict';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Contract table-of-contents scroll spy. */
(function(){
  var tocLinks=document.querySelectorAll('.toc a');
  if(!tocLinks.length||!('IntersectionObserver' in window))return;
  var map={};
  tocLinks.forEach(function(a){var href=a.getAttribute('href')||'';if(href.charAt(0)==='#')map[href.slice(1)]=a;});
  var spy=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(!entry.isIntersecting)return;
      tocLinks.forEach(function(link){link.classList.remove('active');});
      var link=map[entry.target.id];
      if(link)link.classList.add('active');
    });
  },{rootMargin:'-25% 0px -65% 0px'});
  document.querySelectorAll('.doc-body h2[id]').forEach(function(h){spy.observe(h);});
})();

function goal(name){try{if(typeof ym==='function')ym(Number(document.body.dataset.metrikaId)||111882478,'reachGoal',name);}catch(e){}}
function toast(message){
  var el=document.getElementById('toast');
  if(!el){el=document.createElement('div');el.id='toast';el.setAttribute('role','status');el.setAttribute('aria-live','polite');document.body.appendChild(el);}
  el.textContent=message;
  el.classList.add('show');
  clearTimeout(el._timer);
  el._timer=setTimeout(function(){el.classList.remove('show');},2600);
}

/* Copy requisites. */
var copyReq=document.getElementById('copyReq');
if(copyReq){
  copyReq.addEventListener('click',function(){
    goal('copy_req');
    var text='ООО ЧОО «Рускорпорация»\n'+
      'ИНН 5902050810 · КПП 590501001\n'+
      'ОГРН 1185958064665\n'+
      'Лицензия № Л056-00106-59/00033018\n'+
      'Тел.: +7 (925) 047-42-25\n'+
      'Email: fizohrana@ruscor24.ru';
    function ok(){toast('Реквизиты скопированы в буфер обмена');}
    function fallback(){
      var ta=document.createElement('textarea');
      ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';
      document.body.appendChild(ta);ta.select();
      try{document.execCommand('copy');ok();}catch(e){toast('Скопируйте реквизиты вручную из блока выше');}
      document.body.removeChild(ta);
    }
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok).catch(fallback);}else{fallback();}
  });
}

/* Rotating shield canvas from the legacy page, isolated from shared shell JS. */
var canvas=document.getElementById('shieldCanvas');
if(canvas&&canvas.getContext){
  var ctx=canvas.getContext('2d');
  var img=new Image();
  img.crossOrigin='anonymous';
  img.src='/images/logo-animation.jpg';
  var angle=0,animId=null;
  var numbers=[12,1,2,3,4,5,6,7,8,9,10,11];
  var radius=260,centerX=300,centerY=300,imgSize=440;

  function getActiveIndex(angleDeg){var deg=((angleDeg%360)+360)%360;return Math.round(deg/30)%12;}
  function drawShield(advance){
    if(!ctx)return;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.save();ctx.translate(centerX,centerY);ctx.rotate(angle);ctx.drawImage(img,-imgSize/2,-imgSize/2,imgSize,imgSize);ctx.restore();
    var activeIdx=getActiveIndex(angle*180/Math.PI);
    ctx.save();ctx.translate(centerX,centerY);
    for(var i=0;i<numbers.length;i++){
      var theta=(i/12)*2*Math.PI-Math.PI/2;
      var x=radius*Math.cos(theta),y=radius*Math.sin(theta);
      ctx.textAlign='center';ctx.textBaseline='middle';
      if(i===activeIdx){ctx.font='600 40px Cormorant, Georgia, serif';ctx.fillStyle='#F5E3B3';ctx.shadowColor='rgba(232,200,122,.85)';ctx.shadowBlur=50;}
      else{ctx.font='500 30px Cormorant, Georgia, serif';ctx.fillStyle='rgba(142,148,163,.38)';ctx.shadowColor='rgba(232,200,122,.05)';ctx.shadowBlur=5;}
      ctx.fillText(numbers[i],x,y);
    }
    ctx.restore();
    ctx.save();ctx.translate(centerX,centerY);ctx.rotate(angle);
    ctx.shadowColor='rgba(232,200,122,.45)';ctx.shadowBlur=16;
    ctx.beginPath();ctx.moveTo(0,-radius+20);ctx.lineTo(-12,-radius+45);ctx.lineTo(12,-radius+45);ctx.closePath();ctx.fillStyle='#F5E3B3';ctx.fill();
    ctx.strokeStyle='rgba(232,200,122,.3)';ctx.lineWidth=1;ctx.stroke();
    ctx.shadowBlur=22;ctx.beginPath();ctx.arc(0,0,12,0,2*Math.PI);ctx.fillStyle='#F5E3B3';ctx.fill();
    ctx.shadowBlur=10;ctx.beginPath();ctx.arc(0,0,6,0,2*Math.PI);ctx.fillStyle='#07090D';ctx.fill();ctx.restore();
    if(advance){angle+=0.012;animId=requestAnimationFrame(function(){drawShield(true);});}
  }
  img.onload=function(){drawShield(!RM);};
  img.onerror=function(){
    ctx.fillStyle='#171003';ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#E8C87A';ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='600 46px Cormorant, Georgia, serif';
    ctx.fillText('РУСКОРПОРАЦИЯ',canvas.width/2,canvas.height/2-10);
    ctx.font='italic 500 22px Cormorant, Georgia, serif';ctx.fillStyle='#8E94A3';ctx.fillText('охрана и консалтинг',canvas.width/2,canvas.height/2+40);
  };
  window.addEventListener('beforeunload',function(){if(animId)cancelAnimationFrame(animId);});
}
})();
