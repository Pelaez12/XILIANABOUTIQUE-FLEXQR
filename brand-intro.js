const seenKey='xiliana-brand-intro-v2';
let currentIntro;
function seen(){try{return sessionStorage.getItem(seenKey)==='1';}catch{return false;}}
function remember(){try{sessionStorage.setItem(seenKey,'1');}catch{}}

export function playBrandIntro(force=false){
 if(currentIntro)return currentIntro;
 if(!force&&(!['/','/index.html'].includes(location.pathname)||location.hash||seen()))return Promise.resolve();
 remember();
 const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const previousFocus=document.activeElement;
 const opening=document.createElement('dialog');
 opening.id='opening';opening.className=reducedMotion?'opening is-reduced':'opening';opening.setAttribute('aria-label','Presentación de Xiliana Boutique');
 opening.innerHTML=`<div class="opening__stage"><div class="opening__dots" aria-hidden="true"><i></i><i></i><i></i></div><img class="opening__logo" src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique by Antonio Grau"/><p class="opening__slogan">Solo una vida para lucirte.</p></div><div class="opening__progress" aria-hidden="true"></div><button type="button" class="opening__skip">Omitir presentación</button>`;
 currentIntro=new Promise(resolve=>{
  let finished=false,timer;
  const finish=()=>{
   if(finished)return;finished=true;clearTimeout(timer);opening.classList.add('is-exiting');
   setTimeout(()=>{opening.close();opening.remove();document.body.classList.remove('opening-active');currentIntro=null;
    const target=previousFocus!==document.body&&previousFocus?.isConnected?previousFocus:document.querySelector('.site-header .brand-logo');
    target?.focus({preventScroll:true});resolve();},600);
  };
  opening.querySelector('button').addEventListener('click',finish);
  opening.addEventListener('cancel',event=>{event.preventDefault();finish();});
  document.body.append(opening);document.body.classList.add('opening-active');opening.showModal();
  requestAnimationFrame(()=>{
   if(finished)return;
   opening.classList.add('is-playing');
   // 6.1 seconds of presentation + 0.6 seconds of exit, like FLEXQR.
   timer=setTimeout(finish,6100);
  });
 });
 return currentIntro;
}
export const introFinished=playBrandIntro();
