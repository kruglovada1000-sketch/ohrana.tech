(function(){
'use strict';
var items=Array.prototype.slice.call(document.querySelectorAll('.accordion-item'));
if(!items.length)return;
var searchInput=document.getElementById('artSearch');
var clearBtn=document.getElementById('artClear');
var resetBtn=document.getElementById('artReset');
var countEl=document.getElementById('artCount');
var noRes=document.getElementById('artNoRes');
var catBtns=Array.prototype.slice.call(document.querySelectorAll('.cat-btn'));
var activeCat='all';
function plural(n){var n10=n%10,n100=n%100;if(n10===1&&n100!==11)return'статья';if(n10>=2&&n10<=4&&(n100<12||n100>14))return'статьи';return'статей';}
function closeItem(item){
  var header=item.querySelector('.accordion-header'),content=item.querySelector('.accordion-content');
  item.classList.remove('open');
  if(header){header.classList.remove('active');header.setAttribute('aria-expanded','false');}
  if(content){content.classList.remove('active');content.style.maxHeight='';}
}
function applyFilter(){
  var q=searchInput?(searchInput.value||'').trim().toLowerCase():'';
  if(clearBtn)clearBtn.style.display=q?'grid':'none';
  var visible=0;
  items.forEach(function(item){
    var text=(item.textContent||'').toLowerCase();
    var cat=item.dataset.cat||'';
    var show=(!q||text.indexOf(q)!==-1)&&(activeCat==='all'||cat===activeCat);
    item.hidden=!show;
    if(show)visible++;else closeItem(item);
  });
  if(countEl)countEl.innerHTML=q||activeCat!=='all'?'Найдено: <b>'+visible+'</b> '+plural(visible)+' из '+items.length:'Показано: <b>'+visible+'</b> из '+items.length+' статей';
  if(noRes)noRes.style.display=visible?'none':'block';
}
if(searchInput)searchInput.addEventListener('input',applyFilter);
if(clearBtn)clearBtn.addEventListener('click',function(){if(searchInput){searchInput.value='';searchInput.focus();}applyFilter();});
if(resetBtn)resetBtn.addEventListener('click',function(){if(searchInput)searchInput.value='';activeCat='all';catBtns.forEach(function(btn){btn.classList.toggle('on',btn.dataset.cat==='all');});applyFilter();});
catBtns.forEach(function(btn){btn.addEventListener('click',function(){activeCat=btn.dataset.cat||'all';catBtns.forEach(function(b){b.classList.toggle('on',b===btn);});applyFilter();});});
var headers=Array.prototype.slice.call(document.querySelectorAll('.accordion-header'));
headers.forEach(function(header){
  header.setAttribute('aria-expanded','false');
  header.addEventListener('click',function(){
    var item=header.closest('.accordion-item'),content=header.nextElementSibling,isActive=header.classList.contains('active');
    items.forEach(closeItem);
    if(!isActive&&item&&content&&!item.hidden){
      item.classList.add('open');header.classList.add('active');header.setAttribute('aria-expanded','true');content.classList.add('active');content.style.maxHeight=(content.scrollHeight+60)+'px';
    }
  });
});
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){document.querySelectorAll('.accordion-header.active').forEach(function(header){var content=header.nextElementSibling;if(content)content.style.maxHeight=(content.scrollHeight+60)+'px';});},120);},{passive:true});
applyFilter();
})();
