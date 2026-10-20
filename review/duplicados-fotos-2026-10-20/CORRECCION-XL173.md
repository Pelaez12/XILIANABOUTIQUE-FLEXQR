# Corrección de identidad XL-173 / XL-214

El propietario ordenó expresamente borrar XL-173. Se retiró esa ficha de `products.js` y del registro vigente `review/publicados-confirmados.json`; se conservó XL-214 en Largos, código 2083, a S/549. La foto y los registros históricos de XL-173 siguen como evidencia. El catálogo queda con 177 productos y 25 en Largos.

## Qué falló en el registro

Sí existía un JSON completo. `review/publicados-confirmados.json` respaldaba los productos publicados, y `categorias-confirmadas.json` y las matrices registraban las decisiones anteriores. Sin embargo, tener las dos fichas registradas no demostraba que fueran prendas distintas. El alta se cotejó por nombre/precio/referencia de WhatsApp sin resolver la equivalencia fotográfica con XL-173, cuyo nombre y precio eran otros. Por eso el respaldo quedó sincronizado con un catálogo que ya contenía el error. La auditoría visual completa lo detectó después.

## Registro vigente y comprobaciones

- `review/publicados-confirmados.json`: refleja exactamente los 177 productos de `products.js`.
- `review/identidades-consolidadas.json`: registra XL-173 como identidad retirada y XL-214 como ficha vigente, precio confirmado, instrucción y hashes de ambas fotos.
- `review/auditoria-whatsapp-2026-10-20/matriz-177.json`: conserva correspondencias con las 185 apariciones de WhatsApp y esta consolidación. Todas las apariciones tienen ficha asociada.
- `resolucion-xl173.json`: conserva las dos fichas completas y la resolución del propietario.

`build.cjs` ejecuta ahora `validar-registro.cjs` antes de regenerar la web. La comprobación rechaza un respaldo distinto del catálogo, IDs repetidos, la reaparición de XL-173, ausencia/cambio de precio o categoría de la ficha canónica confirmada y reutilización de las fotos conocidas de esta identidad en otra ficha. Verifica hashes contra archivos reales. Esto bloquea el duplicado conocido; una foto nueva recomprimida o una sesión distinta todavía requiere comparación visual antes de dar de alta otro producto.

Las tres pruebas de regresión verifican respaldo desactualizado, reincorporación del ID retirado o de su foto bajo otro ID y permanencia de la ficha confirmada a S/549. El build pasó con 241 páginas, 241 bloques JSON-LD, 354 imágenes de sitemap y enlaces locales presentes. La página de XL-173 ya no se genera; XL-214 permanece.
