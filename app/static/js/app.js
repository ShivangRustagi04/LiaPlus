async function api(path, method='GET', body=null){
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  if(!r.ok) {
    const e = await r.json().catch(()=>({error:'unknown'}));
    throw new Error(e.error || 'Request failed');
  }
  return r.json();
}

function renderMessage(m){
  const container = document.createElement('div');
  container.className = 'msg ' + (m.speaker === 'User' ? 'user' : 'bot');
  const bubble = document.createElement('div');
  bubble.className = 'bubble ' + (m.speaker === 'User' ? 'user' : 'bot');
  bubble.textContent = m.text;
  container.appendChild(bubble);
  const meta = document.createElement('div');
  meta.className = 'meta';
  if(m.speaker === 'User' && m.sentiment){
    meta.innerHTML = 'Sentiment: <strong>' + m.sentiment.label + '</strong> (compound=' + m.sentiment.compound.toFixed(3) + ')';
  } else {
    meta.textContent = m.speaker;
  }
  container.appendChild(meta);
  return container;
}

async function loadHistory(){
  const data = await api('/api/history');
  const chat = document.getElementById('chat');
  chat.innerHTML = '';
  data.history.forEach(m => chat.appendChild(renderMessage(m)));
}

window.addEventListener('load', ()=>{ loadHistory().catch(e=>console.error(e)); });

document.getElementById('sendBtn').addEventListener('click', async ()=>{
  const ta = document.getElementById('userInput');
  const text = ta.value.trim();
  if(!text) return;
  try{
    await api('/api/send', 'POST', {text});
    ta.value = '';
    await loadHistory();
  }catch(e){
    alert(e.message);
  }
});

document.getElementById('finishBtn').addEventListener('click', async ()=>{
  try{
    const s = await api('/api/summary');
    const div = document.getElementById('summary');
    div.style.display = 'block';
    div.innerHTML = '<strong>Overall conversation sentiment:</strong> ' + s.overall_label + ' (avg compound=' + s.avg_compound.toFixed(3) + ')<br/>' +
                    '<strong>Messages analyzed:</strong> ' + s.count + '<br/>' +
                    '<strong>Distribution:</strong> Positive=' + s.distribution.Positive + ', Neutral=' + s.distribution.Neutral + ', Negative=' + s.distribution.Negative + '<br/>' +
                    '<strong>Trend:</strong> ' + s.trend;
  }catch(e){ alert(e.message); }
});

document.getElementById('resetBtn').addEventListener('click', async ()=>{
  await fetch('/api/reset', {method:'POST'});
  document.getElementById('summary').style.display='none';
  await loadHistory();
});
