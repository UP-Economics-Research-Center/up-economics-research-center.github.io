
(() => {
 const menu=document.querySelector('.mobile-menu');
 const panel=document.getElementById('site-search');
 const input=document.getElementById('site-query');
 const clear=document.querySelector('.search-clear');
 const close=document.querySelector('.search-close');
 const results=document.getElementById('search-results');
 const status=document.getElementById('search-status');
 const triggers=[...document.querySelectorAll('.search-button,[data-search-toggle]')];
 let opener=null,timer;
 const sections=[
 ['Research','Explore the Center’s research areas.','research.html','research projects empirical applied economics'],
 ['People','Faculty researchers and research professionals.','people.html','people faculty researchers directory team staff'],
 ['Publications','Journal articles, working papers, books, and analysis.','publications.html','publications journal articles working papers books policy briefs archive'],
 ['Seminars','General and student research seminars.','seminars.html','seminars talks events students calendar archive'],
 ['News','Announcements and updates from the Center.','news.html','news announcements updates archive'],
 ['About and contact','The Center, collaborations, and contact information.','about.html','about contact collaboration institutions email'],
 ];
 const areas=[
 ['Education and Human Capital','education-and-human-capital'],
 ['Digital and Business Economics','digital-and-business-economics'],
 ['Political Economy','political-economy'],
 ['Macroeconomics','macro-economy'],
 ['Development Economics','development-economics'],
 ['Health, Water and Sanitation','water-and-sanitation'],
 ['Agricultural Economics','agriculture-economics'],
 ['Environmental Economics','environmental-economics'],
 ['Economic Demography','demographic-economics']
 ];
 const index=[...sections.map(([name,description,url,keywords])=>({name,description,url,keywords,group:'Section'})),
 ...areas.map(([name,slug])=>({name,description:'Projects, researchers, and publications in this area.',url:'research-area.html?area='+slug,keywords:name+' research area topic',group:'Research area'}))];
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
 function draw(items){
  const list=document.createElement('ul');list.className='search-result-list';
  for(const item of items){
   const li=document.createElement('li'),link=document.createElement('a'),text=document.createElement('span'),title=document.createElement('strong'),description=document.createElement('small'),arrow=document.createElement('span');
   link.href=item.url;
   title.textContent=item.name;description.textContent=item.description;
   arrow.className='search-result-arrow';arrow.textContent='→';arrow.setAttribute('aria-hidden','true');
   text.append(title,description);link.append(text,arrow);li.append(link);list.append(li);
  }
  results.append(list);
 }
 function render(){
  clearTimeout(timer);
  const query=normalize(input.value);
  clear.hidden=!input.value;
  results.replaceChildren();
  if(!query){
   status.textContent='Explore the Center';
   draw(index.filter(item=>['Research','People','Publications','Seminars'].includes(item.name)));
   return;
  }
  const terms=query.split(' ');
  const matches=index.map(item=>{
   const name=normalize(item.name),all=normalize(item.name+' '+item.keywords+' '+item.description);
   const match=terms.every(term=>all.includes(term));
   const score=(name===query?100:0)+(name.startsWith(query)?40:0)+(name.includes(query)?20:0)+terms.filter(term=>name.includes(term)).length*5;
   return {item,match,score};
  }).filter(x=>x.match).sort((a,b)=>b.score-a.score).map(x=>x.item);
  status.textContent=matches.length ? matches.length+' result'+(matches.length===1?'':'s')+' for “'+input.value.trim()+'”' : 'No results for “'+input.value.trim()+'”';
  if(matches.length){draw(matches);return;}
  const hint=document.createElement('p');hint.className='search-empty';hint.textContent='Try a broader topic, such as education or development, or browse these sections.';
  results.append(hint);draw(index.slice(0,4));
 }
 function setOpen(open,restore=false){
  panel.hidden=!open;panel.classList.toggle('open',open);
  triggers.forEach(button=>button.setAttribute('aria-expanded',String(open)));
  if(open){if(menu)menu.open=false;render();input.focus();}
  else {clearTimeout(timer);if(restore)(opener?.getClientRects().length?opener:triggers.find(b=>b.getClientRects().length))?.focus();}
 }
 window.toggleSearch=()=>{
  const opening=panel.hidden;
  if(opening)opener=triggers.includes(document.activeElement)?document.activeElement:triggers.find(b=>b.getClientRects().length);
  setOpen(opening);
 };
 window.searchSite=event=>{event.preventDefault();render();return false;};
 input.addEventListener('input',()=>{clear.hidden=!input.value;clearTimeout(timer);timer=setTimeout(render,150);});
 clear.addEventListener('click',()=>{input.value='';render();input.focus();});
 close.addEventListener('click',()=>setOpen(false,true));
 results.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false);});
 if(menu){
  menu.addEventListener('toggle',()=>{if(menu.open)setOpen(false);});
  menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{menu.open=false;}));
 }
 document.addEventListener('click',event=>{
  if(menu?.open&&!menu.contains(event.target))menu.open=false;
  if(!panel.hidden&&!panel.contains(event.target)&&!triggers.some(button=>button.contains(event.target)))setOpen(false);
 });
 document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  if(!panel.hidden){event.preventDefault();setOpen(false,true);}
  else if(menu?.open){menu.open=false;menu.querySelector('summary').focus();}
 });
})();
