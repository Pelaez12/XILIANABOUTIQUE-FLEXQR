import './order-ui.js';
import { startVideo } from './video-audio.js';
import { introFinished, playBrandIntro } from './brand-intro.js?v=signature-20261022';

// Las siete colecciones ya llegan en el HTML, incluso sin JavaScript.
// El movimiento acompaña la exploración y nunca oculta las tarjetas.
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
if (!motionPreference.matches && 'IntersectionObserver' in window) {
  const animations = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.filter(entry => entry.isIntersecting).forEach((entry, index) => {
      observer.unobserve(entry.target);
      const animation = entry.target.animate(
        [{ opacity: .88 }, { opacity: 1 }],
        { duration: 320, delay: Math.min(index, 2) * 40, easing: 'cubic-bezier(.22,1,.36,1)' }
      );
      animations.add(animation);
      animation.onfinish = () => animations.delete(animation);
    });
  }, { threshold: .12 });
  document.querySelectorAll('.category-tile').forEach(tile => observer.observe(tile));
  motionPreference.addEventListener('change', event => {
    if (!event.matches) return;
    observer.disconnect();
    animations.forEach(animation => animation.cancel());
    animations.clear();
  });
}

introFinished.then(startVideo);
document.querySelector('[data-replay-intro]')?.addEventListener('click',()=>playBrandIntro(true).then(startVideo));

