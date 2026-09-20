(function(){
'use strict';
var links=Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"],.article-toc a[href^="#"],[data-article-toc] a[href^="#"]'));
if(!links.length)return;
var pairs=[];
links.forEach(function(link){
  var href=link.getAttribute('href')||'';
  if(href.length<2)return;
  try{var target=document.getElementById(decodeURIComponent(href.slice(1)));if(target)pairs.push({link:link,target:target});}catch(e){}
});
if(!pairs.length)return;
function activate(target){
  pairs.forEach(function(pair){
    var on=pair.target===target;
    pair.link.classList.toggle('active',on);
    if(on)pair.link.setAttribute('aria-current','location');else pair.link.removeAttribute('aria-current');
  });
}
if('IntersectionObserver' in window){
  var current=null;
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){current=entry.target;activate(current);}
    });
  },{rootMargin:'-18% 0px -68% 0px',threshold:[0,.1,1]});
  pairs.forEach(function(pair){io.observe(pair.target);});
}else{
  var ticking=false;
  window.addEventListener('scroll',function(){
    if(ticking)return;ticking=true;
    requestAnimationFrame(function(){
      var best=pairs[0].target,bestDist=Infinity;
      pairs.forEach(function(pair){var d=Math.abs(pair.target.getBoundingClientRect().top-innerHeight*.24);if(d<bestDist){bestDist=d;best=pair.target;}});
      activate(best);ticking=false;
    });
  },{passive:true});
}
})();
