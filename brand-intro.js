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
 opening.innerHTML=`<div class="opening__stage"><div class="opening__signature" aria-hidden="true"></div><div class="opening__brand"><img class="opening__logo" src="/images/xiliana-logo-gold-black.png" alt="Xiliana Boutique by Antonio Grau"/></div><p class="opening__slogan"><span>Solo una vida</span><span>para <em>lucirte.</em></span></p></div><div class="opening__progress" aria-hidden="true"></div><button type="button" class="opening__skip">Omitir presentación</button>`;
 currentIntro=new Promise(resolve=>{
  let finished=false,timer,exitTimer;
  const finish=()=>{
   if(finished)return;finished=true;clearTimeout(timer);opening.classList.add('is-exiting');
   const cleanup=()=>{
    if(!opening.isConnected)return;
    clearTimeout(exitTimer);opening.close();opening.remove();document.body.classList.remove('opening-active');currentIntro=null;
    const target=previousFocus!==document.body&&previousFocus?.isConnected?previousFocus:document.querySelector('.site-header .brand-logo');
    target?.focus({preventScroll:true});resolve();
   };
   opening.addEventListener('transitionend',event=>{
    if(event.target===opening&&event.propertyName==='opacity')cleanup();
   });
   exitTimer=setTimeout(cleanup,reducedMotion?250:650);
  };
  opening.querySelector('button').addEventListener('click',finish);
  opening.addEventListener('cancel',event=>{event.preventDefault();finish();});
  opening.addEventListener('animationend',event=>{
   if(event.target.classList.contains('opening__slogan'))finish();
  });
  document.body.append(opening);document.body.classList.add('opening-active');opening.showModal();
  const logo=opening.querySelector('.opening__logo');
  const decoded=logo.decode?logo.decode().catch(()=>{}):Promise.resolve();
  decoded.then(()=>requestAnimationFrame(()=>{
   if(finished)return;
   opening.classList.add('is-playing');
   // La última fase dirige la salida; este límite evita bloquear la navegación
   // si el navegador no entrega animationend.
   timer=setTimeout(finish,9000);
  }));
 });
 return currentIntro;
}
export const introFinished=playBrandIntro();
