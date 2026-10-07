// Recommendations use catalogue details, with visual clues from the photo audit
// for models whose official names do not describe their colour or neckline.
const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const clues = [
  ['negro', /\bnegr\w*/], ['blanco', /\bblanc\w*/], ['azul', /\bazul\w*|\bblue\b/],
  ['celeste', /\bceleste\b/], ['verde', /\bverd\w*/], ['amarillo', /\bamarill\w*/],
  ['rosado', /\brosad\w*|\brosa\b|\bfucsia\b/], ['morado', /\bmorad\w*|\blila\b/],
  ['rojo', /\broj\w*/], ['guinda', /\bguinda\b|\bvino\b/],
  ['dorado', /\bdorad\w*|\bgold\b/], ['crema', /\bcrema\b|\bnude\b/],
  ['marrón', /\bmarron\b|\bbrown\b/], ['plomo', /\bplomo\b|\bgris\b/],
  ['pedrería', /pedreria|diamantes|mostacillas|strass|brillos plateados|aplicaciones plateadas/],
  ['lentejuelas', /lentejuela/], ['perlas', /perla/], ['encaje', /encaje/],
  ['gasa', /\bgasa\b|\bgaza\b|\btull?\b/], ['terciopelo', /terciopelo|gamuz|gamusa/],
  ['drapeado', /drapead|pliegue/], ['asimétrico', /asimetr|una manga|cuello diagonal/],
  ['sirena', /sirena/], ['tirantes', /tirante|\btiras\b/], ['strapless', /strapless/],
  ['mangas', /manga/], ['flecos', /fleco/], ['lazo', /lazo/], ['estampado', /estampad|floral|rayas/]
];
const colours = new Set(clues.slice(0, 14).map(([name]) => name));
const details = new Set(['pedrería', 'lentejuelas', 'perlas', 'encaje', 'gasa', 'terciopelo', 'flecos', 'lazo', 'estampado']);
const visualClues = {
  40: ['verde', 'strapless'], 54: ['azul', 'strapless'], 59: ['verde', 'blanco'],
  61: ['gasa', 'lentejuelas', 'mangas'], 69: ['mangas'], 78: ['pedrería'],
  80: ['negro'], 84: ['amarillo'], 95: ['azul'], 98: ['guinda'],
  102: ['blanco'], 108: ['crema'], 111: ['tirantes'], 119: ['verde', 'tirantes'],
  123: ['pedrería', 'asimétrico'], 131: ['tirantes'], 132: ['dorado', 'asimétrico'],
  133: ['mangas'], 134: ['tirantes', 'pedrería']
};
const features = product => new Set([
  ...clues.filter(([, pattern]) => pattern.test(normalize(product.name))).map(([name]) => name),
  ...(visualClues[product.id] || [])
]);
const compatible = (a, b) => a === b ||
  [a, b].every(c => ['Gala', 'Largos'].includes(c)) ||
  [a, b].every(c => ['Cortos', 'Cortos con brillo', 'Liquidación'].includes(c));
const reasonFor = (shared, sameCategory, category) => {
  if (shared.includes('pedrería')) return 'Más detalles de pedrería';
  if (shared.includes('lentejuelas')) return 'También con lentejuelas';
  if (shared.includes('perlas')) return 'Otro look con perlas';
  if (shared.includes('encaje')) return 'También con encaje';
  if (shared.includes('flecos')) return 'Más movimiento con flecos';
  if (shared.includes('asimétrico')) return 'Otro diseño asimétrico';
  if (shared.includes('sirena')) return 'También con corte sirena';
  const colour = shared.find(feature => colours.has(feature));
  if (colour) return `Más ideas en ${colour}`;
  return sameCategory ? `Más de ${category.toLowerCase()}` : 'Otra idea para tu look';
};

export function recommendProducts(current, catalogue, limit = 4) {
  if (!current || limit <= 0) return [];
  const currentFeatures = features(current);
  const currentPhotos = new Set((current.photos || []).map(photo => photo.sha256).filter(Boolean));
  const ranked = catalogue.filter(product => product.id !== current.id && !product.photoPending &&
    product.photos?.length && product.price > 0 && compatible(current.category, product.category) &&
    !product.photos.some(photo => photo.sha256 && currentPhotos.has(photo.sha256)))
    .map(product => {
      const shared = [...features(product)].filter(feature => currentFeatures.has(feature));
      const sameCategory = product.category === current.category;
      const priceDistance = Math.abs(Math.log(product.price / current.price));
      const styleScore = shared.reduce((score, feature) => score + (details.has(feature) ? 10 : colours.has(feature) ? 8 : 6), 0);
      return { product, reason: reasonFor(shared, sameCategory, current.category),
        score: (sameCategory ? 60 : 0) + styleScore + 12 * Math.exp(-3 * priceDistance), priceDistance };
    });
  ranked.sort((a, b) => b.score - a.score || a.priceDistance - b.priceDistance || a.product.id - b.product.id);
  return ranked.slice(0, limit).map(({ product, reason }) => ({ product, reason }));
}
