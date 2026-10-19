const fs = require('fs');

const brillo = JSON.parse(fs.readFileSync('review/catalogo-whatsapp-2026-10-12/brillo-completo.json'));
const cortos = JSON.parse(fs.readFileSync('review/catalogo-whatsapp-2026-10-12/cortos-completo.json'));
const largos = JSON.parse(fs.readFileSync('review/catalogo-whatsapp-2026-10-12/largos-completo.json'));
const gala = JSON.parse(fs.readFileSync('review/catalogo-whatsapp-2026-10-12/gala-completo.json'));

console.log('=== BRILLO COMPLETO (' + brillo.length + ') ===');
brillo.forEach((item, i) => console.log(`${i+1}. ${item.name || item.text}`));

console.log('\n=== CORTOS COMPLETO (' + cortos.length + ') ===');
cortos.forEach((item, i) => console.log(`${i+1}. ${item.name || item.text}`));

console.log('\n=== LARGOS COMPLETO (' + largos.length + ') ===');
largos.forEach((item, i) => console.log(`${i+1}. ${item.name || item.text}`));

console.log('\n=== GALA COMPLETO (' + gala.length + ') ===');
gala.slice(0, 25).forEach((item, i) => console.log(`${i+1}. ${item.name || item.text}`));
