const { products } = require('../products.js');

console.log('--- ALL PRODUCTS ---');
products.forEach(p => {
  console.log(JSON.stringify({
    id: p.id,
    cat: p.category,
    name: p.name,
    price: p.price,
    origPrice: p.originalPrice || null,
    photo: p.photos && p.photos[0] ? p.photos[0].src : null
  }));
});
