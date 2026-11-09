const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:780,height:1040},deviceScaleFactor:1});
 await p.goto('file://'+process.cwd()+'/kv.html',{waitUntil:'networkidle'});
 await p.waitForTimeout(1500);
 await p.screenshot({path:'kv_780.png'});
 // grid overlay version
 await p.evaluate(()=>{const s=document.getElementById('safe');[96,262,330,430,650,905].forEach(y=>{const d=document.createElement('div');d.className='grid';d.style.top=y+'px';d.innerHTML='<span>y='+y+'</span>';s.appendChild(d)})});
 await p.screenshot({path:'kv_780_grid.png'});
 // mobile 390 : scale 0.5
 const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
 await m.goto('file://'+process.cwd()+'/kv.html',{waitUntil:'networkidle'});
 await m.addStyleTag({content:'.kv{transform:scale(0.5);transform-origin:0 0}'});
 await m.waitForTimeout(1200);
 await m.screenshot({path:'kv_390.png',clip:{x:0,y:0,width:390,height:520}});
 // measure rendered sizes
 const t=await m.$eval('.title',e=>{const r=e.getBoundingClientRect();return {w:r.width,h:r.height}});
 const l=await m.$eval('.label',e=>{const r=e.getBoundingClientRect();return {w:r.width,h:r.height}});
 console.log(JSON.stringify({title_at_390:t,label_at_390:l}));
 await b.close();
})();
