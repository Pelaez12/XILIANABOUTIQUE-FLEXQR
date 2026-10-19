const fs = require('fs');
const path = require('path');
const { products } = require('../products.js');

let html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Revisión 139 Vestidos</title>
<style>
body { font-family: sans-serif; background: #111; color: #eee; padding: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.card { background: #222; border-radius: 8px; padding: 10px; border: 1px solid #444; }
.card img { width: 100%; height: 280px; object-fit: cover; border-radius: 4px; }
.card h4 { margin: 8px 0 4px; font-size: 13px; }
.card .meta { font-size: 12px; color: #aaa; }
.badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
.cat-Gala { background: #854d0e; color: #fef08a; }
.cat-Largos { background: #1e3a8a; color: #bfdbfe; }
.cat-Cortos { background: #14532d; color: #bbf7d0; }
.cat-Cortos-con-brillo { background: #701a75; color: #f5d0fe; }
.cat-Bandage { background: #831843; color: #fbcfe8; }
</style>
</head>
<body>
<h1>Catálogo Actual: 139 Vestidos</h1>
<div class="grid">
`;

for (const p of products) {
  const catClass = 'cat-' + p.category.replace(/\s+/g, '-');
  const imgPath = p.photos[0] ? p.photos[0].src.replace(/^\.\//, '../') : '';
  html += `
  <div class="card" id="p-${p.id}">
    <img src="${imgPath}" loading="lazy" alt="${p.name}">
    <span class="badge ${catClass}">${p.category}</span>
    <h4>XL-${String(p.id).padStart(3, '0')}: ${p.name}</h4>
    <div class="meta">Precio: S/ ${p.price}</div>
  </div>`;
}

html += `</div></body></html>`;

fs.writeFileSync('review/catalogo_visual_139.html', html);
console.log('Generado review/catalogo_visual_139.html');
