(() => {
 const form=document.querySelector('.filters');const list=document.getElementById('news-list');const count=document.getElementById('news-count');
 if(!form||!list||!count)return;
 const search=document.getElementById('news-search'),year=document.getElementById('news-year'),category=document.getElementById('news-type');
 const records=[...list.querySelectorAll('.news-record')];
 function apply(){const query=search.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();let shown=0;
  for(const card of records){const text=(card.dataset.search||card.textContent).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const visible=(!query||text.includes(query))&&(!year.value||card.dataset.year===year.value)&&(!category.value||card.dataset.category===category.value);card.hidden=!visible;if(visible)shown++;}
  if(records.length&&shown===0){if(!list.querySelector('[data-filter-empty]')){const empty=document.createElement('p');empty.className='empty-state';empty.dataset.filterEmpty='true';empty.textContent='No announcements match these filters.';list.append(empty);}}else list.querySelector('[data-filter-empty]')?.remove();
  count.textContent=records.length?`Showing ${shown} approved update${shown===1?'':'s'}`:'No approved announcements have been added yet.';
 }
 window.filterNews=apply;window.resetNews=()=>{search.value='';year.value='';category.value='';apply();};window.browseNewsYear=value=>{year.value=value;apply();year.focus();form.scrollIntoView({block:'start'});};
 form.addEventListener('submit',event=>{event.preventDefault();apply();});search.addEventListener('input',apply);year.addEventListener('change',apply);category.addEventListener('change',apply);apply();
})();
