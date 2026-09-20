(function(){
'use strict';
var guardsDisplay=document.getElementById('guards-count');
var hoursDisplay=document.getElementById('hours-count');
var totalDisplay=document.getElementById('total-price');
var guardTypeSelect=document.getElementById('guard-type');
if(!guardsDisplay||!hoursDisplay||!totalDisplay||!guardTypeSelect)return;
var rates={standard:1200,premium:1800,vip:2800};
var guards=2,hours=4;
function updatePrice(){var rate=rates[guardTypeSelect.value]||rates.premium;var actualHours=Math.max(hours,4);var total=guards*actualHours*rate;totalDisplay.textContent=total.toLocaleString('ru-RU')+' ₽';}
document.querySelectorAll('.calc-btn').forEach(function(btn){btn.addEventListener('click',function(){var target=this.getAttribute('data-target');var dir=parseInt(this.getAttribute('data-dir'),10);if(target==='guards'){guards=Math.max(1,guards+dir);guardsDisplay.textContent=guards;}else if(target==='hours'){hours=Math.max(4,hours+dir);hoursDisplay.textContent=hours;}updatePrice();});});
guardTypeSelect.addEventListener('change',updatePrice);
updatePrice();
})();
