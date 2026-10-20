# Auditoría de Cortos y sus tres ofertas de Liquidación · 20 de octubre de 2026

Se cotejaron las cuatro capturas ampliadas entregadas por el propietario con las 33 entradas del inventario, las fichas actuales y las fotos de las prendas. Los tres vestidos de oferta se compararon con sus fotografías web y las otras categorías. Se revisaron también las **48 fotos de las 29 fichas publicadas en Cortos**. No se cambió el catálogo ni ninguna foto de producto.

## Los tres vestidos de Liquidación

| Foto entregada | Ficha web | Precio web | Resultado |
|---|---|---:|---|
| Azul oscuro con flores blancas y mangas largas | XL-010 · Vestido corto azul con estampado floral | S/68.70 | Misma prenda y pose; cambia recorte/marca en la versión web. Solo en Liquidación. |
| Satín floral azul/verde, dos poses sobre fondo amarillo | XL-180 · Vestido corto satín estampado | S/86.70 | Misma fotografía compuesta. Solo en Liquidación. |
| Verde agua con mangas de volantes y abertura | XL-181 · Vestido corto con volantes de cuello redondo | S/115.60 | Misma prenda y foto frontal; la galería incluye espalda. Solo en Liquidación. |

Los tres IDs aparecen una sola vez en `products.js`. Sus enlaces solo figuran en la página de colección Liquidación, sin aparecer en Gala, Largos, Cortos, Brillos ni Bandage. Sus archivos no se reutilizan en otra ficha. La revisión visual completa del catálogo y esta comparación no detectan la misma prenda bajo otro ID. Las coincidencias de hashes perceptuales por fondos/poses no bastan para identificar prendas: en la foto recortada de XL-010 el algoritmo propone falsos parecidos, pero las flores, mangas, modelo y pose confirman XL-010.

[Comparación de las tres fotos y sus fichas actuales](liquidacion-comparada.jpg). [Comprobación de exclusividad y métricas](comprobacion-liquidacion.json).

## Conteo por identidad, no por número de anuncios

| Paso | Cantidad |
|---|---:|
| Entradas en las capturas | 33 |
| Entradas de Liquidación, excluidas de Cortos | −3 |
| Apariciones restantes para Cortos | 30 |
| Apariciones adicionales de dos prendas ya contadas | −2 |
| **Modelos únicos identificados en la lista para Cortos** | **28** |
| Modelo publicado adicional fuera de estas capturas: XL-114 | +1 |
| **Fichas actuales en la colección web Cortos** | **29** |

Las **29 fichas actuales son modelos visualmente distintos**, según sus 48 fotos y la auditoría global previa. Algunas galerías repiten una vista frontal con otra escala, fondo o resolución (XL-084, XL-085, XL-131 y XL-187), lo que no crea otro producto.

## Las dos repeticiones en WhatsApp

| Identidad web única | Apariciones en la captura | Evidencia |
|---|---|---|
| **XL-187** | «Vestido blanco mini elegante con perlas», S/329, código1914, fila6; y «Vestido blanco con perlas», S/319, código1894, fila10. | Misma imagen de vestido blanco con mangas abiertas y perlas. El propietario ya confirmó conservar S/329. [Registro de esa conciliación](../auditoria-whatsapp-2026-10-19/matriz-177.json). |
| **XL-066** | «Vestido color verde terciopelo semi drapeado con manga y escote», S/429, código2025, fila13; y «Vestido drapeado verde de mandas con escote», S/359, código2024, fila15. | El propietario confirmó previamente que es una sola prenda y que debe conservarse la referencia2025 a S/429. [Confirmación específica histórica](../auditoria-whatsapp-2026-10-18/duplicados_confirmados.json). No se consideran dos identidades por aparecer en dos anuncios. |

## Qué falta y qué no se ha confirmado

**No falta publicar ningún modelo único identificado en estas capturas:** los 28 ya están en Cortos. No existe un nombre adicional identificable que pueda darse de alta para completar 30 sin inventar una identidad.

**XL-114, «Vestido negro largo de perlas con detalles», S/319**, permanece publicado en Cortos por su registro anterior, pero no tiene una aparición inequívoca en estas 33 entradas. Se conserva y se señala expresamente esa diferencia. Su foto es la primera de la segunda hoja de contacto.

Todavía **no se ha demostrado un conjunto de 30 prendas únicas** para Cortos. Para justificarlo desde esta lista harían falta dos modelos distintos adicionales; si el propietario ratifica XL-114 como parte de esos 30, quedaría por identificar otro modelo diferente. No se duplica una de las 28 prendas ni se traslada Liquidación para cuadrar ese total.

## Registros y evidencias

- [Resultado JSON con las 33 filas, ID, categoría actual, precio y captura de origen](resultado.json).
- `lista-01-10.png`, `lista-11-20.png`, `lista-21-30.png` y `lista-31-33.png`: capturas originales ampliadas, ordenadas por fila del inventario.
- [Todas las fotos de Cortos, hoja1](cortos-todas-fotos-01.jpg) y [hoja2](cortos-todas-fotos-02.jpg).
- Las tres fotos de Liquidación entregadas se conservan en `propietario-XL-010.png`, `propietario-XL-180.png` y `propietario-XL-181.png` como evidencia, sin sustituir archivos publicados.
- `generar-informe.py` comprueba los conteos, las identidades asociadas y la exclusividad de Liquidación. El catálogo publicado permanece en 177 productos y Cortos en 29.
