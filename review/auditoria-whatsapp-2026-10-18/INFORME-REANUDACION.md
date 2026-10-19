# Informe de auditoría — catálogo WhatsApp Business

Fecha: 18 de octubre de 2026. Contacto observado: +51 930 527 248. La revisión fue de solo lectura; no se editó WhatsApp ni la web.

## Inventario

Se observaron **272 entradas de catálogo**. Son entradas por colección, no 272 productos únicos: 11 corresponden a la lista adicional de Liquidación y pueden repetir prendas de las colecciones principales; también hay repeticiones comprobadas entre las tres secciones PENDIENTES.

| Colección de WhatsApp | Entradas |
| --- | ---: |
| Gala Dresess | 53 |
| Vestidos Largos | 23 |
| Vestidos Cortos Brillos | 43 |
| Vestidos Cortos | 33 |
| Vestidos Bandage's | 22 |
| PENDIENTES 1 | 26 |
| PENDIENTES 2 | 41 |
| PENDIENTES 3 | 16 |
| CALZADOS | 1 |
| ACCESORIOS U OTROS | 3 |
| PRENDAS LIQUIDACIÓN 💃🏻👠👗 | 11 |

Las 261 entradas tienen nombre observado; **una no muestra precio**: «VESTIDO BANDAGE», descrito como «Caqui ceñido». No se asignó un precio supuesto.

Se verificó el número de fotos en 268 fichas (174 vestidos de las colecciones principales, las 83 entradas de las tres secciones PENDIENTES y las 11 entradas de Liquidación). En CALZADOS y ACCESORIOS U OTROS se comprobó la foto principal, pero el número total de fotos de esas cuatro fichas continúa **NO VERIFICADO**.

## PENDIENTES unificados

PENDIENTES 1 contiene 26 entradas; las 26 están repetidas en PENDIENTES 2. PENDIENTES 2 contiene 41 entradas. PENDIENTES 3 contiene 16 entradas, de las cuales una está repetida. La lista unificada consta de **56 artículos**. Las 27 entradas repetidas coinciden por nombre, precio y número visible en la ficha; no se borró nada en WhatsApp.

Se recorrieron las 83 fichas de aretes y todos sus carruseles. Tras unificar duplicados hay 56 artículos con 62 fotos: 50 artículos tienen una foto y 6 tienen dos. La descarga directa del archivo de WhatsApp no funcionó porque la foto se presenta como `blob`; los archivos guardados son capturas de evidencia y no equivalen al archivo original para publicar.

Detalle: [tabla de 56 aretes](PENDIENTES-UNIFICADOS.md), [JSON unificado](pendientes_unificados.json), [duplicados](pendientes_duplicados.json).

## Liquidación

WhatsApp muestra **11 entradas** en `PRENDAS LIQUIDACIÓN 💃🏻👠👗`, aunque el conteo previo indicado era 10. Se conservaron como lista adicional y no se descontaron de sus categorías principales. Las 11 fichas muestran una foto cada una. Esta diferencia de 11 frente a 10 requiere confirmación del dueño.

## Comparación con la web local

El archivo `XILIANA/products.js` contiene 157 productos. Ninguno es de PENDIENTES, CALZADOS o ACCESORIOS U OTROS. Por tanto, faltan en la web los 56 aretes unificados, las sandalias y los tres accesorios: **60 artículos únicos de estas colecciones**.

De las 174 entradas de vestidos de WhatsApp, 133 tienen una posible correspondencia única por número visible o nombre normalizado único. Ninguna de esas 133 muestra precio distinto. En 41 entradas no se pudo establecer una correspondencia única con esas reglas; esto no demuestra que falten en la web. Quedan 24 fichas web sin correspondencia única. Las fotos de vestidos de ambos lados no se compararon en esta pasada.

Las 14 diferencias de categoría detectadas en esta comparación se corrigieron en `products.js` conforme a la colección de WhatsApp. Al repetir la comparación quedan **0 diferencias de categoría** entre las 133 correspondencias identificadas. Las 41 fichas sin correspondencia única no están cubiertas por esta comprobación.

La ficha «Vestido crema de encaje y tull asimétrico» aparece en Gala en WhatsApp y en Liquidación en la web; se mantiene como caso especial porque Liquidación puede coexistir con una categoría principal.

## Dudas pendientes de confirmación

- Precio de «VESTIDO BANDAGE» / «Caqui ceñido». WhatsApp no lo muestra.
- Liquidación contiene 11 entradas visibles, no 10. «Top Amarillo» y «Vestidos largo estampado geométrico (Verde y Nude)» no tienen una coincidencia exacta de nombre en las colecciones principales observadas.
- Si «Bruselas» en «Vestido sirena largo color rojo con Bruselas» describe la prenda o es un error del catálogo.
- Si «VESTIDO BANDAGE» / «Rojo corto de pedrería plateada» debe permanecer en Bandage's o ir a Cortos Brillos.
- Si «Vestido corto color verde (S M)» realmente tiene brillo suficiente para Cortos Brillos.
- Las 41 correspondencias de vestidos no resueltas requieren revisión de fotos o código; no se puede afirmar que falten en la web.
- Archivos originales de PENDIENTES: NO DESCARGADOS; WhatsApp mostró las imágenes como `blob`. El conteo de fotos sí quedó verificado y se guardaron capturas de evidencia.
- Total de fotos de CALZADOS y ACCESORIOS U OTROS: NO VERIFICADO; solo se comprobó su foto principal.

## Archivos

Inventario completo: [tabla de 272 entradas](inventario_actualizado.md) y [JSON](inventario_actualizado.json). Comparación detallada: [JSON](comparacion_web_conservadora.json).
