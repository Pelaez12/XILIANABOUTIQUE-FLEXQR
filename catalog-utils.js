export const modelImageIds = new Set([35, 42, 45, 46, 49, 56]);
export const aiImageIds = new Set(Array.from({ length: 41 }, (_, index) => index + 18));
export const displayImage = product => modelImageIds.has(product.id)
  ? `./images/catalog-${String(product.id).padStart(2, '0')}-model.png`
  : aiImageIds.has(product.id)
    ? `./images/catalog-${String(product.id).padStart(2, '0')}-ai.png`
    : product.image;
export const slug = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
export const productPath = product => `/vestidos/${product.id}-${slug(product.name)}/`;
export const categoryPath = category => `/colecciones/${slug(category)}/`;
