const { products } = require('../products.js');

console.log('Total products:', products.length);
const byCat = {};
for (const p of products) {
  byCat[p.category] = byCat[p.category] || [];
  byCat[p.category].push(p);
}

for (const cat in byCat) {
  console.log(`\n=== CATEGORY: ${cat} (${byCat[cat].length}) ===`);
  for (const p of byCat[cat]) {
    console.log(`ID ${String(p.id).padStart(3, '0')} | ${p.name} | S/ ${p.price}`);
  }
}
