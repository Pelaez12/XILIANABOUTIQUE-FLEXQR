const fs = require('fs');
const { products } = require('../products.js');

const galaAndLargos = products.filter(p => p.category === 'Gala' || p.category === 'Largos');

console.log('Inspecting 61 Gala & Largos dresses:');
for (const p of galaAndLargos) {
  // Check height and width of first photo
  const photo = p.photos[0];
  console.log(`ID ${String(p.id).padStart(3, '0')} | Cat: ${p.category.padEnd(6)} | Name: ${p.name} | Photo: ${photo?.src}`);
}
