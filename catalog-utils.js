export const restoredImageIds = new Set();
export const aiImageIds = new Set();
export const modelImageIds = new Set();
export const displayImage = product => product.image;
export const sizeLabel = 'Talla estándar';
export const featuredCategoryIds = {Gala:59,Largos:24,'Cortos con brillo':39,Cortos:10,Bandage:14};
export const slug = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
export const productPath = product => `/vestidos/${product.id}-${slug(product.name)}/`;
export const categoryPath = category => `/colecciones/${slug(category)}/`;
