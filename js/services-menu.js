/* Services disclosure enhances a real catalogue link; no header replacement. */
(function(){
 'use strict';
 var group=document.querySelector('#siteNav .services-nav');
 if(!group||group.dataset.servicesBound)return;
 group.dataset.servicesBound='1';
 var button=group.querySelector('.services-nav-toggle');
 var panel=group.querySelector('.services-panel');
 var nav=document.getElementById('siteNav');
 var mq=window.matchMedia('(min-width:1101px)');
 function setOpen(open){button.setAttribute('aria-expanded',String(open));panel.hidden=!open;}
 button.addEventListener('click',function(){setOpen(panel.hidden);});
 group.addEventListener('mouseenter',function(){if(mq.matches)setOpen(true);});
 group.addEventListener('mouseleave',function(){if(mq.matches&&!group.contains(document.activeElement))setOpen(false);});
 group.addEventListener('focusout',function(){setTimeout(function(){if(!group.contains(document.activeElement))setOpen(false);},0);});
 group.addEventListener('keydown',function(e){
  if(e.key==='Escape'){e.preventDefault();setOpen(false);button.focus();}
  if(e.key==='ArrowDown'&&e.target!==panel&& !panel.contains(e.target)){e.preventDefault();setOpen(true);panel.querySelector('a').focus();}
 });
 document.addEventListener('click',function(e){if(!group.contains(e.target))setOpen(false);});
 panel.addEventListener('click',function(e){if(e.target.closest('a'))setOpen(false);});
 new MutationObserver(function(){if(!mq.matches&&!nav.classList.contains('open'))setOpen(false);}).observe(nav,{attributes:true,attributeFilter:['class']});
 if(mq.addEventListener)mq.addEventListener('change',function(){setOpen(false);});
 else mq.addListener(function(){setOpen(false);});
 setOpen(false);
})();
