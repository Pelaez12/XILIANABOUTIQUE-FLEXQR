const { products } = require('../products.js');

const longDresses = products.filter(p => p.category === 'Gala' || p.category === 'Largos' || p.id === 154);
console.log('Total long dresses:', longDresses.length);

for (const p of longDresses) {
  const name = p.name;
  const hasBrillo = /brill|lentejuela|pedrer|diamante|strass|perla|platead|dorad|gold|copas de pedrería/.test(name.toLowerCase());
  const isEstampadoOrCampo = /estampad|floral|flores|rayas|campo|fucsia|gasa|satín|gamuz|bruselas/.test(name.toLowerCase());
  console.log(`ID ${String(p.id).padStart(3, '0')} | Cat: ${p.category.padEnd(6)} | Brillo: ${hasBrillo ? 'YES' : 'NO '} | Est/Campo: ${isEstampadoOrCampo ? 'YES' : 'NO '} | ${name}`);
}
