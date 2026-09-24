(()=>{
  const container=document.getElementById('campus-film');
  if(!container)return;
  const videoId=container.dataset.videoId;
  if(!/^[A-Za-z0-9_-]{11}$/.test(videoId||''))return;
  const playCampusVideo=(focusPlayer=false)=>{
    const frame=document.createElement('iframe');
    frame.src=`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&mute=1&playsinline=1&controls=1&rel=0`;
    frame.title='Ciudad Panamericana — Universidad Panamericana institutional video 2025–2026';
    frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen=true;
    frame.referrerPolicy='strict-origin-when-cross-origin';
    container.replaceChildren(frame);
    if(focusPlayer)frame.focus();
  };
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.getElementById('play-campus-film')?.addEventListener('click',()=>playCampusVideo(true));
  }else{
    playCampusVideo();
  }
})();
