(() => {
 const {t,language}=window.SiteLanguage||{t:value=>value,language:'en'};
 const form=document.querySelector('.filters');
 const list=document.getElementById('publication-list');
 const count=document.getElementById('result-count');
 const search=document.getElementById('pub-search');
 if(!form||!list||!count||!search)return;
 const fields={topic:document.getElementById('pub-topic'),year:document.getElementById('pub-year'),type:document.getElementById('pub-type')};
 const normalize=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const records=[...list.querySelectorAll('.publication[data-title]')];
 const params=new URLSearchParams(location.search);
 let author=params.get('author')||'';
 const authorNote=document.createElement('p');
 authorNote.className='note author-filter-note';
 if(author){
  const authorLink=records.flatMap(card=>[...card.querySelectorAll('.pub-authors a[href]')]).find(link=>new URL(link.href).hash==='#'+encodeURIComponent(author));
  authorNote.textContent=(language==='es'?'Publicaciones de: ':'Publications by: ')+(authorLink?.textContent||author);
  form.before(authorNote);
 }
 const keys={q:search,topic:fields.topic,year:fields.year,type:fields.type};
 for(const [key,element] of Object.entries(keys)){const value=params.get(key);if(key==='q'){if(value)element.value=value;}else if(value&&[...element.options].some(option=>option.value===value))element.value=value;}
 function apply(updateUrl=true){
  const query=normalize(search.value.trim());let shown=0;
  for(const card of records){
   const match=(!author||(card.dataset.personIds||'').split(/\s+/).includes(author))&&(!query||normalize(card.dataset.title+' '+card.dataset.authors+' '+card.dataset.type+' '+card.textContent).includes(query))&&(!fields.topic.value||card.dataset.topics.split(/\s+/).includes(fields.topic.value))&&(!fields.year.value||card.dataset.year===fields.year.value)&&(!fields.type.value||card.dataset.type===fields.type.value);
   card.hidden=!match;if(match)shown++;
  }
  const initialEmpty=list.querySelector('.empty-state');
  if(records.length&&shown===0){
   let empty=initialEmpty;
   if(!empty){empty=document.createElement('p');empty.className='empty-state';empty.dataset.filterEmpty='true';list.append(empty);}
   const noPublishedBriefs=fields.type.value==='Policy brief'&&!records.some(card=>card.dataset.type==='Policy brief');
   empty.textContent=t(noPublishedBriefs?'No policy briefs are published yet. Clear filters to browse all publications.':'No publications match these filters. Clear filters or try a broader search.');
  }
  else list.querySelector('[data-filter-empty]')?.remove();
  count.textContent=records.length?(language==='es'?`Mostrando ${shown} publicaci${shown===1?"ón verificada":"ones verificadas"}`:`Showing ${shown} verified publication${shown===1?'':'s'}`):t('No verified publications have been added yet.');
  if(updateUrl){const next=new URL(location.href);for(const [key,element] of Object.entries(keys)){if(element.value)next.searchParams.set(key,element.value);else next.searchParams.delete(key);}if(author)next.searchParams.set('author',author);else next.searchParams.delete('author');history.replaceState({},'',next);window.dispatchEvent(new Event('up:urlchange'));}
 }
 window.filterPubs=()=>apply();window.resetPubs=()=>{search.value='';author='';authorNote.remove();Object.values(fields).forEach(element=>element.value='');apply();};
 window.browsePubYear=year=>{fields.year.value=year;apply();fields.year.focus();form.scrollIntoView({block:'start'});};
 form.addEventListener('submit',event=>{event.preventDefault();apply();});
 search.addEventListener('input',()=>apply());Object.values(fields).forEach(element=>element.addEventListener('change',()=>apply()));
 apply(false);
})();
