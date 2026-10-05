export const restoredImageIds = new Set([18,21,22,23,25,27,28,29,30,31,32,33,34,37,39,40,43,44,50,53,57,58]);
export const aiImageIds = restoredImageIds;
export const modelImageIds = new Set();
export const displayImage = product => restoredImageIds.has(product.id)
  ? `./images/catalog-${String(product.id).padStart(2, '0')}-faithful-v2.png`
  : product.image;
export const slug = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
export const productPath = product => `/vestidos/${product.id}-${slug(product.name)}/`;
export const categoryPath = category => `/colecciones/${slug(category)}/`;
