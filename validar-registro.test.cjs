const {test} = require('node:test');
const assert = require('node:assert/strict');
const {validateCatalog} = require('./validar-registro.cjs');
const current = [{id:214, name:'Vestido rosado', price:549, category:'Largos', photos:[{src:'./images/214.png',sha256:'actual'}]}];
const identities = {consolidaciones:[{id_retirado:173,id_vigente:214,precio_vigente_pen:549,categoria_vigente:'Largos',fotos_identidad:[{src:'./images/173.jpeg',sha256:'anterior'},{src:'./images/214.png',sha256:'actual'}]}]};

test('Rechaza un respaldo vigente desactualizado', () => {
  assert.throws(() => validateCatalog(current, [], identities), /no coincide/);
});
test('Bloquea reintroducir XL-173 y usar su foto bajo otro ID', () => {
  for (const id of [173, 300]) {
    const products = [...current, {id,price:450,category:'Largos',photos:[{src:'./images/173.jpeg',sha256:'anterior'}]}];
    assert.throws(() => validateCatalog(products, products, identities), /retirado|reutiliza/);
  }
});
test('Exige la ficha confirmada a S/549 y permite conservar su foto antigua en la misma identidad', () => {
  const merged = structuredClone(current);
  merged[0].photos.push({src:'./images/173.jpeg',sha256:'anterior'});
  assert.doesNotThrow(() => validateCatalog(merged, merged, identities));
  const wrongPrice = structuredClone(current);
  wrongPrice[0].price = 450;
  assert.throws(() => validateCatalog(wrongPrice, wrongPrice, identities), /Precio distinto/);
  assert.throws(() => validateCatalog([], [], identities), /Falta la ficha vigente/);
});
