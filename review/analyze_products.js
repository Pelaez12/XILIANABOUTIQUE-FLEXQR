const fs = require('fs');
const { products } = require('../products.js');

// Let's analyze all products
const analysis = products.map(p => {
  const name = p.name.toLowerCase();
  const id = p.id;
  const currentCat = p.category;
  
  // Clues
  const isBandage = name.includes('bandage') || currentCat === 'Bandage';
  const hasBrillo = /brill|lentejuela|pedrer|diamante|strass|perla|platead|dorad|gold|shimmer/.test(name);
  const isLargo = /largo|sirena|cola|romano|novia/.test(name);
  const isCorto = /corto|3\/4|mini|midi/.test(name);
  const isEstampadoCampoFucsia = /estampad|floral|flores|rayas|campo|fucsia|palo rosa|verde limón|bruselas|amarillo/.test(name);

  return {
    id,
    name: p.name,
    currentCat,
    price: p.price,
    photo: p.photos[0]?.src,
    isBandage,
    hasBrillo,
    isLargo,
    isCorto,
    isEstampadoCampoFucsia
  };
});

fs.writeFileSync('review/products_analysis.json', JSON.stringify(analysis, null, 2));
console.log('Analysis saved to review/products_analysis.json');
