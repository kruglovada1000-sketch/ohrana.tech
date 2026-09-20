(function(){
'use strict';

function setContactsFaqState(item,open){
  if(!item)return;
  var q=item.querySelector('.faq-q');
  var answer=item.querySelector('.faq-a');
  var arrow=item.querySelector('.faq-arrow');
  item.classList.toggle('open',!!open);
  if(q)q.setAttribute('aria-expanded',String(!!open));
  if(answer)answer.style.maxHeight=open?answer.scrollHeight+'px':'';
  if(arrow){
    arrow.textContent=open?'↓':'←';
    arrow.style.transform='none';
  }
}

document.querySelectorAll('#faq .faq-item').forEach(function(item){
  setContactsFaqState(item,item.classList.contains('open'));
});

document.addEventListener('click',function(e){
  var q=e.target.closest('#faq .faq-q');
  if(!q)return;
  e.preventDefault();
  e.stopImmediatePropagation();
  e.stopPropagation();
  var item=q.closest('.faq-item');
  var shouldOpen=!!item&&!item.classList.contains('open');
  document.querySelectorAll('#faq .faq-item.open').forEach(function(openItem){
    if(openItem!==item)setContactsFaqState(openItem,false);
  });
  setContactsFaqState(item,shouldOpen);
},true);

var button=document.getElementById('copyReq');
if(!button)return;
function goal(name){try{if(typeof ym==='function')ym(Number(document.body.dataset.metrikaId)||111882478,'reachGoal',name);}catch(e){}}
function toast(message){
  var el=document.getElementById('toast');
  if(!el){
    el=document.createElement('div');
    el.id='toast';
    el.setAttribute('role','status');
    el.setAttribute('aria-live','polite');
    el.style.cssText='position:fixed;left:50%;bottom:28px;transform:translate(-50%,16px);z-index:6000;background:#12161F;border:1px solid rgba(232,200,122,.5);border-radius:999px;padding:12px 22px;color:#F5E3B3;font:700 13px Manrope,system-ui,sans-serif;box-shadow:0 18px 50px rgba(0,0,0,.6);opacity:0;transition:.25s;pointer-events:none';
    document.body.appendChild(el);
  }
  el.textContent=message;el.style.opacity='1';el.style.transform='translate(-50%,0)';
  clearTimeout(el._timer);el._timer=setTimeout(function(){el.style.opacity='0';el.style.transform='translate(-50%,16px)';},2600);
}
var text='ООО ЧОП «Рускорпорация»\n'+
  'ИНН: 5902050810 | КПП: 590501001\n'+
  'ОГРН: 1185958064665\n'+
  'Лицензия № Л056-00106-59/00033018 от 29.11.2018\n'+
  'Тел.: +7 (925) 047-42-25\n'+
  'Email: fizohrana@ruscor24.ru';
function ok(){toast('Реквизиты скопированы в буфер обмена');}
function fallback(){
  var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy');ok();}catch(e){toast('Скопируйте реквизиты вручную из блока выше');}
  document.body.removeChild(ta);
}
button.addEventListener('click',function(){goal('copy_req');if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok).catch(fallback);}else{fallback();}});
})();
