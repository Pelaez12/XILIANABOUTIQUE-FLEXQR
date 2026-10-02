// Transcripción del catálogo de WhatsApp de Xiliana Boutique, 2 de octubre de 2026.
// Los precios y tallas pueden cambiar; la boutique confirma disponibilidad.
export const products = [
  { id: 1, name: 'Vestido de largo gala nude con aplicaciones', category: 'Gala', price: 649, note: 'Prenda importada' },
  { id: 2, name: 'Vestido largo de gala de lentejuelas rojo brillantes', category: 'Gala', price: 649, note: 'Talla XL indicada en WhatsApp', imageNote: 'La foto visible en WhatsApp muestra un vestido oscuro multicolor; confirma el modelo con la boutique.' },
  { id: 3, name: 'Vestido sirena largo color rojo con Bruselas', category: 'Gala', price: 449, note: 'Prenda importada, según el catálogo.' },
  { id: 4, name: 'Vestido romano largo floreado', category: 'Largos', price: 439 },
  { id: 5, name: 'Vestido largo fucsia', category: 'Largos', price: 389 },
  { id: 6, name: 'Vestido largo amarillo con lazo', category: 'Largos', price: 449, note: 'Strapless de gasa con lazo en la cintura, según el catálogo.' },
  { id: 7, name: 'Vestido corto azul', category: 'Cortos con brillo', price: 329 },
  { id: 8, name: 'Vestido corto verde', category: 'Cortos con brillo', price: 114.50, originalPrice: 229, note: 'Tallas S y M indicadas en WhatsApp.' },
  { id: 9, name: 'Vestido corto de lentejuelas verde', category: 'Cortos con brillo', price: 369 },
  { id: 10, name: 'Vestido corto azul con estampado floral', category: 'Cortos', price: 68.70, originalPrice: 229, note: 'Mangas y silueta ajustada, según el catálogo.' },
  { id: 11, name: 'Vestido corto satín estampado', category: 'Cortos', price: 86.70, originalPrice: 289 },
  { id: 12, name: 'Vestido corto con volantes de cuello redondo', category: 'Cortos', price: 115.60, originalPrice: 289 },
  { id: 13, name: 'Vestido bandage blanco y negro', category: 'Bandage', price: 144.50, originalPrice: 289 },
  { id: 14, name: 'Vestido bandage verde con rayas', category: 'Bandage', price: 379 },
  { id: 15, name: 'Vestido bandage rojo corto con pedrería plateada', category: 'Bandage', price: 379 },
  { id: 16, name: 'Vestido transparente con diamantes de imitación', category: 'Liquidación', price: 164.50, originalPrice: 329, note: 'Talla L indicada en WhatsApp.' },
  { id: 17, name: 'Vestido corto dorado de una manga', category: 'Liquidación', price: 194.50, originalPrice: 389 },
].map(product => ({ ...product, image: `./images/dress-${String(product.id).padStart(2, '0')}.jpg` }));

export const categories = ['Todos', 'Gala', 'Largos', 'Cortos con brillo', 'Cortos', 'Bandage', 'Liquidación'];
