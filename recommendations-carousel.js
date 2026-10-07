const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

document.querySelectorAll('.product-recommendations').forEach(section => {
  const track = section.querySelector('.recommendations-grid');
  const controls = section.querySelector('.recommendations-arrows');
  const previous = section.querySelector('[data-recommendations-prev]');
  const next = section.querySelector('[data-recommendations-next]');
  if (!track || !controls || !previous || !next) return;

  const update = () => {
    const maximum = track.scrollWidth - track.clientWidth;
    controls.hidden = maximum <= 2;
    previous.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= maximum - 2;
  };
  const move = direction => {
    const cards = [...track.querySelectorAll('.recommendation-card')];
    const start = cards[0].offsetLeft;
    const positions = cards.map(card => card.offsetLeft - start);
    const destination = direction > 0
      ? positions.find(position => position > track.scrollLeft + 2)
      : positions.reverse().find(position => position < track.scrollLeft - 2);
    track.scrollTo({ left: destination ?? (direction > 0 ? track.scrollWidth : 0),
      behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  };
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', event => {
    if (event.target !== track || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') move(event.key === 'ArrowRight' ? 1 : -1);
    else track.scrollTo({ left: event.key === 'Home' ? 0 : track.scrollWidth,
      behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  });
  track.addEventListener('scroll', update, { passive: true });
  new ResizeObserver(update).observe(track);
  update();
});
