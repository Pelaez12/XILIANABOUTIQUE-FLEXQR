const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function validateCatalog(products, backup, identities) {
  assert.equal(new Set(products.map(p => p.id)).size, products.length, 'Hay IDs repetidos en products.js');
  assert.deepEqual(backup, products, 'review/publicados-confirmados.json no coincide con products.js');
  const byId = new Map(products.map(p => [p.id, p]));
  for (const product of products) {
    const confirmation = product.ownerConfirmation;
    if (!confirmation) continue;
    assert.equal(product.category, confirmation.categoria, `Categoría distinta de la última confirmación de XL-${product.id}`);
    assert.equal(product.price, confirmation.precio_pen, `Precio distinto de la última confirmación de XL-${product.id}`);
  }
  for (const separation of identities.separaciones || []) {
    assert.equal(new Set(separation.modelos.map(m => m.id)).size, separation.modelos.length, 'Dos modelos distintos comparten una ficha');
    for (const model of separation.modelos) {
      const product = byId.get(model.id);
      assert(product, `Falta el modelo distinto XL-${model.id}`);
      assert.equal(product.catalogCode, model.codigo, `Código incorrecto para XL-${model.id}`);
      assert.equal(product.price, model.precio_pen, `Precio incorrecto para el código ${model.codigo}`);
      const ownHashes = new Set(model.fotos.map(p => p.sha256));
      assert(product.photos.some(p => ownHashes.has(p.sha256)), `Las fotos de XL-${model.id} no corresponden a su identidad confirmada`);
      for (const other of separation.modelos.filter(m => m.id !== model.id)) {
        const foreignHashes = new Set(other.fotos.map(p => p.sha256));
        const foreignPaths = new Set(other.fotos.map(p => p.src));
        assert(!product.photos.some(p => foreignHashes.has(p.sha256) || foreignPaths.has(p.src)), `XL-${model.id} contiene fotos del modelo distinto ${other.codigo}`);
      }
    }
  }
  const retiredIds = new Set(identities.consolidaciones.map(r => r.id_retirado));
  for (const identity of identities.consolidaciones) {
    assert(!byId.has(identity.id_retirado), `XL-${identity.id_retirado} está retirado por duplicación y no puede publicarse`);
    assert(!retiredIds.has(identity.id_vigente), 'La ficha vigente de una consolidación también está retirada');
    const canonical = byId.get(identity.id_vigente);
    assert(canonical, `Falta la ficha vigente XL-${identity.id_vigente}`);
    assert.equal(canonical.price, identity.precio_vigente_pen, `Precio distinto de la confirmación de XL-${identity.id_vigente}`);
    assert.equal(canonical.category, identity.categoria_vigente, `Categoría distinta de la confirmación de XL-${identity.id_vigente}`);
    const knownHashes = new Set(identity.fotos_identidad.map(p => p.sha256));
    const knownPaths = new Set(identity.fotos_identidad.map(p => p.src));
    for (const product of products) {
      if (product.id === identity.id_vigente) continue;
      assert(!(product.photos || []).some(photo => knownHashes.has(photo.sha256) || knownPaths.has(photo.src)),
        `XL-${product.id} reutiliza una foto de la identidad consolidada XL-${identity.id_vigente}`);
    }
  }
}

function validateRegistry(root = __dirname) {
  const source = fs.readFileSync(path.join(root, 'products.js'), 'utf8');
  const products = JSON.parse(source.match(/export const products = ([\s\S]*?);\s*export const categories/)[1]);
  const identities = JSON.parse(fs.readFileSync(path.join(root, 'data/catalog-identities.json'), 'utf8'));
  // Verificar los hashes reales evita que un metadato alterado o vacío oculte
  // una fotografía conocida de una identidad ya consolidada.
  const actual = products.map(product => ({...product, photos: (product.photos || []).map(photo => {
    const hash = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, photo.src))).digest('hex');
    if (photo.sha256) assert.equal(photo.sha256, hash, `Hash de foto incorrecto: ${photo.src}`);
    return {...photo, sha256: hash};
  })}));
  validateCatalog(products, products, identities);
  validateCatalog(actual, actual, identities);
  console.log(`Registro vigente validado: ${products.length} productos; fotos e identidades verificadas y duplicados consolidados bloqueados.`);
  return products;
}

module.exports = { validateCatalog, validateRegistry };
if (require.main === module) validateRegistry();
