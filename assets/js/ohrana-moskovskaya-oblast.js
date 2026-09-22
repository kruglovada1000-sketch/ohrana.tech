(function(){
'use strict';
function setRegionsFaqState(item,open){
  if(!item)return;
  var q=item.querySelector('.faq-q');
  var answer=item.querySelector('.faq-a');
  var arrow=item.querySelector('.faq-arrow');
  item.classList.toggle('open',!!open);
  if(q)q.setAttribute('aria-expanded',String(!!open));
  if(answer)answer.style.maxHeight=open?answer.scrollHeight+'px':'';
  if(arrow){arrow.textContent=open?'↓':'←';arrow.style.transform='none';}
}
document.querySelectorAll('#faq .faq-item').forEach(function(item){
  setRegionsFaqState(item,item.classList.contains('open'));
});
document.addEventListener('click',function(e){
  var q=e.target.closest('#faq .faq-q');
  if(!q)return;
  e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();
  var item=q.closest('.faq-item');
  var shouldOpen=!!item&&!item.classList.contains('open');
  document.querySelectorAll('#faq .faq-item.open').forEach(function(openItem){
    if(openItem!==item)setRegionsFaqState(openItem,false);
  });
  setRegionsFaqState(item,shouldOpen);
},true);
})();
