'use strict';
const state={busy:false};
const feedback=document.getElementById('feedback');
async function submit(payload){if(state.busy)return;state.busy=true;feedback.textContent='核算中…';document.querySelectorAll('button').forEach(b=>b.disabled=true);try{const response=await fetch('/api/runs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const body=await response.json();if(!response.ok)throw new Error(body.message);feedback.textContent='批单已复算 / '+body.run_id;window.location.reload()}catch(error){feedback.textContent=error.message+'，请检查输入';}finally{state.busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false)}}
document.getElementById('run').addEventListener('click',()=>submit({sample:'dirty.csv'}));
document.getElementById('print').addEventListener('click',()=>window.print());
const form=document.getElementById('source');if(form)form.addEventListener('submit',event=>{event.preventDefault();const csv=document.getElementById('csv').value;submit(csv?{csv}:{sample:document.getElementById('sample').value})});
const review=document.getElementById('review');if(review)review.addEventListener('click',async()=>{try{const r=await fetch('/api/runs/'+review.dataset.run+'/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({version:Number(review.dataset.version),decision:'通过'})});const d=await r.json();if(!r.ok)throw new Error(d.message);feedback.textContent='签审完成 / REV '+d.review_version;review.dataset.version=d.review_version;}catch(e){feedback.textContent=e.message;}});
