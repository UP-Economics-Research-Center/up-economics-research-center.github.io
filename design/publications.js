(() => {
 const form=document.querySelector('.filters');
 const list=document.getElementById('publication-list');
 const count=document.getElementById('result-count');
 const search=document.getElementById('pub-search');
 if(!form||!list||!count||!search)return;
 const fields={topic:document.getElementById('pub-topic'),year:document.getElementById('pub-year'),type:document.getElementById('pub-type')};
 const normalize=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const records=[...list.querySelectorAll('.publication[data-title]')];
 const params=new URLSearchParams(location.search);
 const keys={q:search,topic:fields.topic,year:fields.year,type:fields.type};
 for(const [key,element] of Object.entries(keys)){const value=params.get(key);if(value&&[...element.options].some(option=>option.value===value))element.value=value;else if(key==='q'&&value)element.value=value;}
 function apply(updateUrl=true){
  const query=normalize(search.value.trim());let shown=0;
  for(const card of records){
   const match=(!query||normalize(card.dataset.title+' '+card.dataset.authors+' '+card.dataset.type+' '+card.textContent).includes(query))&&(!fields.topic.value||card.dataset.topics.split(/\s+/).includes(fields.topic.value))&&(!fields.year.value||card.dataset.year===fields.year.value)&&(!fields.type.value||card.dataset.type===fields.type.value);
   card.hidden=!match;if(match)shown++;
  }
  const initialEmpty=list.querySelector('.empty-state');
  if(records.length&&shown===0){if(!initialEmpty){const empty=document.createElement('p');empty.className='empty-state';empty.dataset.filterEmpty='true';empty.textContent='No publications match these filters. Clear filters or try a broader search.';list.append(empty);}}
  else list.querySelector('[data-filter-empty]')?.remove();
  count.textContent=records.length?`Showing ${shown} verified publication${shown===1?'':'s'}`:'No verified publications have been added yet.';
  if(updateUrl){const next=new URL(location.href);for(const [key,element] of Object.entries(keys)){if(element.value)next.searchParams.set(key,element.value);else next.searchParams.delete(key);}history.replaceState({},'',next);}
 }
 window.filterPubs=()=>apply();window.resetPubs=()=>{search.value='';Object.values(fields).forEach(element=>element.value='');apply();};
 window.browsePubYear=year=>{fields.year.value=year;apply();fields.year.focus();form.scrollIntoView({block:'start'});};
 form.addEventListener('submit',event=>{event.preventDefault();apply();});
 search.addEventListener('input',()=>apply());Object.values(fields).forEach(element=>element.addEventListener('change',()=>apply()));
 apply(false);
})();
