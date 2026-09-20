import { chromium } from 'playwright';
import fs from 'node:fs';

const BASE='http://127.0.0.1:4173';
const sitemap=fs.readFileSync('sitemap.xml','utf8');
const urls=[...sitemap.matchAll(/<loc>https:\/\/ohrana\.tech([^<]*)<\/loc>/g)].map(m=>m[1]||'/');
for(const p of ['/','/ceny/','/dogovor/','/kontakty/','/stati/','/fizicheskaya-ohrana/','/ohrana-fizicheskih-lic/','/ohrana-yuridicheskih-lic/','/ohrana-pult/','/ohrana-moskovskaya-oblast/']) if(!urls.includes(p)) urls.push(p);
const unique=[...new Set(urls)].sort();
const viewports=[['desktop',1440,1000],['tablet',768,1024],['mobile',390,844]];
const themes=['dark','light'];
const browser=await chromium.launch({headless:true});
const findings=[];
const stats={pages:unique.length,checks:0,errors:0,warnings:0};

function add(level,ctx,msg){findings.push({level,...ctx,msg});stats[level==='ERROR'?'errors':'warnings']++;}

for(const [vpName,width,height] of viewports){
  for(const theme of themes){
    const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,reducedMotion:'reduce'});
    await context.addInitScript(t=>{try{localStorage.setItem('ohrana-theme',t);}catch{}},theme);
    for(const url of unique){
      stats.checks++;
      const page=await context.newPage();
      const ctx={viewport:vpName,theme,url};
      const pageErrors=[];const consoleErrors=[];const badResponses=[];
      page.on('pageerror',e=>pageErrors.push(String(e?.message||e)));
      page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
      page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)badResponses.push(`${r.status()} ${r.url()}`)});
      let response=null;
      try{response=await page.goto(BASE+url,{waitUntil:'domcontentloaded',timeout:30000});await page.waitForTimeout(350);}catch(e){add('ERROR',ctx,`navigation failed: ${e.message}`);await page.close();continue;}
      if(response&&response.status()>=400)add('ERROR',ctx,`document HTTP ${response.status()}`);
      if(pageErrors.length)add('ERROR',ctx,`pageerror: ${pageErrors.slice(0,3).join(' | ')}`);
      if(badResponses.length)add('ERROR',ctx,`local HTTP errors: ${badResponses.slice(0,4).join(' | ')}`);
      if(consoleErrors.length)add('WARN',ctx,`console errors: ${consoleErrors.slice(0,3).join(' | ')}`);

      const m=await page.evaluate(({theme})=>{
        const de=document.documentElement,b=document.body;
        const visible=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>0&&r.width>0&&r.height>0};
        const dup=[...document.querySelectorAll('[id]')].reduce((a,e)=>(a[e.id]=(a[e.id]||0)+1,a),{});
        const duplicateIds=Object.entries(dup).filter(([id,n])=>id&&n>1).map(([id,n])=>`${id}×${n}`);
        const brokenImages=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src')||i.currentSrc||'?');
        const scrollWidth=Math.max(de.scrollWidth,b?.scrollWidth||0),overflow=scrollWidth-de.clientWidth;
        const h1=[...document.querySelectorAll('h1')].filter(visible).length;
        const unnamedButtons=[...document.querySelectorAll('button')].filter(visible).filter(x=>!((x.getAttribute('aria-label')||'').trim()||(x.innerText||'').trim()||x.getAttribute('title'))).slice(0,10).map(x=>x.id||x.className||'<button>');
        const unsafeBlank=[...document.querySelectorAll('a[target="_blank"]')].filter(a=>!/(^|\s)noopener(\s|$)/.test(a.getAttribute('rel')||'')).slice(0,10).map(a=>a.getAttribute('href'));
        const emptyLinks=[...document.querySelectorAll('a[href="#"],a:not([href])')].filter(visible).slice(0,10).map(a=>(a.innerText||'').trim().slice(0,50)||a.className||'<a>');
        const toggle=document.getElementById('themeToggle');
        const toggleInfo=toggle?{count:document.querySelectorAll('#themeToggle').length,parent:toggle.parentElement?.parentElement?.id||toggle.parentElement?.className||'',text:(toggle.innerText||'').trim(),aria:toggle.getAttribute('aria-label')||'',visible:visible(toggle)}:null;
        const nav=document.getElementById('siteNav');
        const yin=toggle?.querySelector('.theme-yinyang')?.textContent?.trim()||'';
        const canvases=[...document.querySelectorAll('canvas')].filter(visible).map(c=>({id:c.id,w:c.clientWidth,h:c.clientHeight}));

        function rgb(v){const m=v.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(Number);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};}
        function lum(c){const f=n=>{n/=255;return n<=.04045?n/12.92:Math.pow((n+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b)}
        function ratio(a,b){const A=lum(a),B=lum(b);return (Math.max(A,B)+.05)/(Math.min(A,B)+.05)}
        const low=[];
        if(theme==='light'){
          const sels='p,li,small,label,td,th,h1,h2,h3,h4,h5,h6,a,button,.lead,.desc,.accordion-trailer,.sec-head p';
          for(const el of document.querySelectorAll(sels)){
            if(low.length>=16||!visible(el))continue;
            const text=(el.innerText||el.textContent||'').replace(/\s+/g,' ').trim();if(text.length<2)continue;
            const es=getComputedStyle(el);const fg=rgb(es.color);if(!fg||fg.a<.8)continue;
            let bgEl=el,bg=null,gradient=false;
            while(bgEl&&bgEl!==document.documentElement){const s=getComputedStyle(bgEl);if(s.backgroundImage&&s.backgroundImage!=='none'){gradient=true;break;}const c=rgb(s.backgroundColor);if(c&&c.a>.92){bg=c;break;}bgEl=bgEl.parentElement;}
            if(gradient)continue;if(!bg){bg=rgb(getComputedStyle(document.body).backgroundColor)||{r:255,g:255,b:255,a:1};}
            const cr=ratio(fg,bg);const fs=parseFloat(es.fontSize)||16;if(cr<2.35&&fs<32){low.push({tag:el.tagName.toLowerCase(),cls:String(el.className||'').slice(0,80),text:text.slice(0,70),cr:+cr.toFixed(2),color:es.color,bg:`rgb(${bg.r},${bg.g},${bg.b})`});}
          }
        }
        return {overflow,h1,duplicateIds,brokenImages,unnamedButtons,unsafeBlank,emptyLinks,toggleInfo,yin,hasNav:!!nav,canvases,low,themeAttr:de.dataset.theme||''};
      },{theme});

      if(m.overflow>6)add('ERROR',ctx,`horizontal overflow ${m.overflow}px`);
      if(m.h1!==1)add('WARN',ctx,`visible h1 count ${m.h1}`);
      if(m.duplicateIds.length)add('ERROR',ctx,`duplicate ids: ${m.duplicateIds.slice(0,8).join(', ')}`);
      if(m.brokenImages.length)add('ERROR',ctx,`broken images: ${m.brokenImages.slice(0,6).join(', ')}`);
      if(m.unnamedButtons.length)add('WARN',ctx,`unnamed buttons: ${m.unnamedButtons.join(', ')}`);
      if(m.unsafeBlank.length)add('WARN',ctx,`target=_blank without noopener: ${m.unsafeBlank.join(', ')}`);
      if(m.emptyLinks.length)add('WARN',ctx,`empty/# links: ${m.emptyLinks.join(' | ')}`);
      if(m.themeAttr!==theme)add('ERROR',ctx,`theme init mismatch: expected ${theme}, got ${m.themeAttr||'(none)'}`);
      if(m.hasNav){if(!m.toggleInfo||!m.toggleInfo.visible)add('ERROR',ctx,'theme toggle missing/not visible');else if(m.yin!=='☯')add('ERROR',ctx,`theme toggle is not yin-yang: ${JSON.stringify(m.yin)}`);}
      if(m.canvases.some(c=>c.w<20||c.h<20))add('WARN',ctx,`tiny canvas: ${JSON.stringify(m.canvases.filter(c=>c.w<20||c.h<20))}`);
      if(m.low.length)add('WARN',ctx,`severe light-theme contrast: ${m.low.slice(0,6).map(x=>`${x.tag}.${x.cls} cr=${x.cr} “${x.text}”`).join(' || ')}`);

      if(vpName==='mobile'&&m.hasNav){const burger=page.locator('#burger');if(await burger.count()&&await burger.isVisible().catch(()=>false)){await burger.click().catch(()=>{});await page.waitForTimeout(80);const ok=await page.locator('#siteNav').evaluate(n=>n.classList.contains('open')).catch(()=>false);if(!ok)add('ERROR',ctx,'mobile burger failed to open');}}
      if(m.toggleInfo?.visible){const before=await page.evaluate(()=>document.documentElement.dataset.theme);await page.locator('#themeToggle').click().catch(()=>{});await page.waitForTimeout(50);const after=await page.evaluate(()=>document.documentElement.dataset.theme);if(before===after)add('ERROR',ctx,'theme toggle click did not switch theme');}
      await page.close();
    }
    await context.close();
  }
}
await browser.close();
const grouped=findings.reduce((a,f)=>{const k=`${f.level} ${f.viewport} ${f.theme} ${f.url}`;(a[k]??=[]).push(f.msg);return a;},{});
console.log(`AUDIT pages=${stats.pages} checks=${stats.checks} errors=${stats.errors} warnings=${stats.warnings}`);
for(const [k,msgs] of Object.entries(grouped))console.log(`${k}: ${msgs.join('; ')}`);
fs.mkdirSync('site-audit',{recursive:true});
fs.writeFileSync('site-audit/report.json',JSON.stringify({stats,findings},null,2));
