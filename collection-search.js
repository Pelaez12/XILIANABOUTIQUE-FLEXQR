const searchArea = document.querySelector('.collection-search');
if (searchArea) {
  const input = document.querySelector('#collection-query');
  const list = document.querySelector('#collection-suggestions');
  const counter = document.querySelector('#collection-count');
  const empty = document.querySelector('.collection-empty');
  const cards = [...document.querySelectorAll('#collection-products .product-card')];
  const normalize = text => text.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  let suggestions = [];
  let active = -1;
  searchArea.hidden = false;

  function closeSuggestions() {
    list.hidden = true;
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    active = -1;
  }

  function filter(showSuggestions = true) {
    const term = normalize(input.value.trim());
    const words = term.split(/\s+/).filter(Boolean);
    const matches = cards.filter(card => words.every(word => normalize(card.dataset.name).includes(word)));
    cards.forEach(card => { card.hidden = !matches.includes(card); });
    counter.textContent = term ? `${matches.length} de ${cards.length} modelos para tu búsqueda` : `${cards.length} modelos en esta colección`;
    empty.hidden = matches.length > 0;
    suggestions = term ? matches.slice(0, 6) : [];
    list.replaceChildren();
    suggestions.forEach((card, index) => {
      const option = document.createElement('li');
      option.id = `suggested-dress-${index}`;
      option.setAttribute('role', 'option');
      option.setAttribute('aria-selected', 'false');
      option.dataset.index = index;
      const name = document.createElement('span');
      name.textContent = card.dataset.name;
      const price = document.createElement('small');
      price.textContent = card.querySelector('.price').textContent;
      option.append(name, price);
      list.append(option);
    });
    active = -1;
    input.removeAttribute('aria-activedescendant');
    const open = showSuggestions && suggestions.length > 0;
    list.hidden = !open;
    input.setAttribute('aria-expanded', String(open));
  }

  function select(index) {
    if (!suggestions[index]) return;
    input.value = suggestions[index].dataset.name;
    filter(false);
    input.focus();
  }

  input.addEventListener('input', () => filter());
  input.addEventListener('focus', () => filter());
  input.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); closeSuggestions(); return; }
    if (event.key === 'Enter') {
      event.preventDefault();
      if (!list.hidden && active >= 0) select(active); else closeSuggestions();
      return;
    }
    if (!['ArrowDown', 'ArrowUp'].includes(event.key) || !suggestions.length) return;
    event.preventDefault();
    list.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    active = active < 0 ? (event.key === 'ArrowDown' ? 0 : suggestions.length - 1) : (active + (event.key === 'ArrowDown' ? 1 : -1) + suggestions.length) % suggestions.length;
    [...list.children].forEach((option, index) => option.setAttribute('aria-selected', String(index === active)));
    input.setAttribute('aria-activedescendant', list.children[active].id);
  });
  list.addEventListener('pointerdown', event => event.preventDefault());
  list.addEventListener('click', event => {
    const option = event.target.closest('[data-index]');
    if (option) select(Number(option.dataset.index));
  });
  input.addEventListener('blur', closeSuggestions);
  document.querySelector('#clear-collection-search').addEventListener('click', () => {
    input.value = '';
    filter(false);
    input.focus();
  });
}
