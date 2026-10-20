# Auditoría de colecciones · 19 de octubre de 2026

## Confirmación posterior del propietario: 22 vestidos en Largos

El propietario identificó expresamente 22 vestidos en tres capturas del catálogo de WhatsApp. La [conciliación individual de los 22](confirmacion-largos-22.json) registra nombre, precio, código visible, fila de origen e ID web. Diez ya estaban publicados; las doce fichas restantes, **XL-203 a XL-214**, se incorporaron con las imágenes entregadas por el propietario en el orden indicado. Los 22 vestidos confirmados tienen ficha web en Largos.

La fila 19 de las 23 entradas de WhatsApp es **Blusa cola de pato asimétrico blanco con negro S/239**. La lista expresa del propietario la excluye de los 22 vestidos. Por tanto, 23 entradas de WhatsApp = 22 vestidos confirmados + una blusa. La web tiene ahora **25 fichas en Largos**: los 22 vestidos identificados y XL-098, XL-102 y XL-173, que se mantienen por su evidencia individual anterior. Ese total es consecuencia de la conciliación individual, no el criterio de clasificación.

Las doce imágenes entregadas se guardaron sin sustituir las fotos anteriores; cada ficha nueva tiene su propio archivo, tamaño y hash. Ninguno de los 163 productos anteriores se eliminó ni cambió de categoría.

| Orden de foto | Ficha nueva | Modelo | Precio WhatsApp |
|---:|---|---|---:|
| 1 | XL-203 | Vestido romano largo floreado | S/439 |
| 2 | XL-204 | Vestido largo floreado de tirantes | S/499 |
| 3 | XL-205 | Vestido largo anaranjado de mangas largas de rosas | S/369 |
| 4 | XL-206 | Vestido largo animal prient | S/599 |
| 5 | XL-207 | Vestido largo Bandage color Rojo | S/549 |
| 6 | XL-208 | Vestido largo floreado | S/449 |
| 7 | XL-209 | Vestido estampado multicolor | S/289 |
| 8 | XL-210 | Vestido Animal Prient Multicolor | S/329 |
| 9 | XL-211 | Vestido floreado multicolor | S/349 |
| 10 | XL-212 | Vestido corte A animal prient | S/349 |
| 11 | XL-213 | vestido largo de rayas cremas con negro | S/279 |
| 12 | XL-214 | Vestido rosado largo estampado de flores | S/549 |

## Alcance y decisión

Se cotejaron las 175 prendas publicadas con las 185 entradas de vestidos del inventario de WhatsApp del 18/10, las once ofertas, la conciliación del 15/10, las 157 fichas históricas y las confirmaciones individuales posteriores. La [matriz completa vigente](matriz-175.json) contiene ID web, referencia visible de WhatsApp, nombre, precio, todas las rutas y hashes de fotos, apariciones por colección, categoría publicada, evidencia posterior y propuesta. `matriz-163.json` y `matriz-171.json` conservan las instantáneas anteriores. `numero_visible=1200` en Liquidación es un marcador de la captura, no un código de producto; por eso la matriz deja ese código vacío cuando no hay otra referencia.

**Cambios de categoría en fichas anteriores: ninguno.** Se incorporaron doce productos nuevos directamente en Largos. Se corrigieron dos metadatos de procedencia en `products.js`: XL-107 figura en Gala de WhatsApp (código 2078), y XL-187 en Cortos (código 1914). Las categorías visibles ya eran Gala y Cortos. El registro vigente `review/publicados-confirmados.json` se sincronizó con los 175 productos; los JSON históricos se conservaron.

| Colección | WhatsApp 18/10: entradas | Identidades asociadas a web | Web actual/final | Diferencia explicada |
|---|---:|---:|---:|---|
| Gala | 53 | 53 | 50 | XL-125 está en Liquidación; XL-098 y XL-102 en Largos por detalle brillante localizado. |
| Largos | 23 | 22 | 25 | Los 22 vestidos confirmados tienen ficha; la entrada restante es una blusa. XL-098 y XL-102 proceden de Gala; XL-173 tiene confirmación anterior. |
| Cortos con brillo | 43 | 42 | 37 | Dos entradas código 644 son XL-039; cinco prendas están en Liquidación y XL-117 tiene confirmación específica para Gala. XL-127 sigue publicado por confirmación individual y no aparece en las 43 entradas. |
| Cortos | 33 | 31 | 29 | XL-066 aparece dos veces (códigos 2025/2024); tres fichas están en Liquidación; el blanco código 1894 queda sin asociación; XL-114 está en web y no en esta lista. |
| Bandage | 22 | 20 | 23 | Falda código 1733 y vestido negro/amarillo código 2074 sin ficha web identificada; XL-072, XL-076 y XL-147 figuran en web pero no tienen referencia inequívoca en la lista vigente. |
| Liquidación | 11 | 11 | 11 | Cada oferta coincide individualmente por nombre, precio y/o referencia cruzada. |

Los conteos del 15/10 fueron **Gala 32, Largos 25, Cortos 37, Brillos 38, Bandage 22, Liquidación 1** sobre 155 prendas. La web actual tiene 175. Las 23 entradas de Largos del 18/10 contienen 22 vestidos y una blusa; el grupo web de 25 del 15/10 tenía otra composición.

### Los 25 Largos del 15/10 frente a los 23 del 18/10

El conjunto web de 25 del cierre anterior era **XL-005, 006, 020, 023, 024, 060, 088, 091, 093, 096, 098, 100, 102, 106, 113, 138, 139, 141, 159, 162, 163, 173, 176, 177 y 178**. De ellos, XL-005, 006, 020, 023, 024 y 113 siguen en Largos; XL-098 y 102 también. Los otros 16 se muestran hoy en Gala, como se detalla abajo. Desde entonces se sumaron a Largos XL-022, 197, 198, 199 y las doce fichas XL-203 a XL-214: **25 − 16 + 4 + 12 = 25**.

Las 23 entradas actuales de WhatsApp están enumeradas con sus ID, precios y estado de publicación en `confirmacion-largos-22.json`; la entrada 19 es la blusa excluida.

### Traslados anteriores revisados

Estos **16 movimientos de Largos a Gala** ocurrieron después del cierre del 15/10, no en este cambio. Todos tienen entrada individual en Gala del inventario del 18/10 y fotografía web en la matriz. La mención expresa «gala» y la confirmación del propietario refuerzan XL-100, 106, 159, 177 y 178. Los demás conservan la colección comercial observada; en varios, la tela parece lisa en la foto, por lo que conviene pedir confirmación individual si el propietario quiere clasificarlos por material en vez de por colección de WhatsApp.

| ID movido | Evidencia actual | ID movido | Evidencia actual |
|---|---|---|---|
| XL-060 | Gala fila 15, gasa azul S/649 | XL-088 | Gala fila 21, azul sirena S/499 |
| XL-091 | Gala fila 26, verde sirena S/389 | XL-093 | Gala fila 29, fucsia S/549 |
| XL-096 | Gala fila 33, verde gamuzado S/519 | XL-100 | Gala fila 38, rojo de gala S/389 |
| XL-106 | Gala fila 46, negro de gala S/429 | XL-138 | Gala fila 13, palo rosa gasa/satín S/649 |
| XL-139 | Gala fila 12, azul acero S/699 | XL-141 | Gala fila 18, azul S/349 |
| XL-159 | Gala fila 31, negro de gala S/449 | XL-162 | Gala fila 36, sirena rojo S/549 |
| XL-163 | Gala fila 3, sirena rojo S/449 | XL-176 | Gala fila 41, novia blanco S/849 |
| XL-177 | Gala fila 1, nude de gala S/649 | XL-178 | Gala fila 23, verde de gala S/649 |

### Duplicados y cruces de colección

- **Brillos código 644:** filas 11 y 33, mismo XL-039, S/329 y foto; 43 apariciones son 42 identidades.
- **Cortos códigos 2025/2024:** filas 13 y 15, mismo vestido verde XL-066. El propietario eligió la ficha 2025 a S/429; la de S/359 es una aparición duplicada documentada en `duplicados_confirmados.json`.
- **Cortos blanco con perlas:** fila 6, código 1914, S/329, es XL-187 por frente y prenda; fila 10, código 1894, S/319, queda pendiente. No se supuso que fuera XL-187.
- **XL-127/XL-140:** comparten nombre y S/549, pero sus fotos son vestidos distintos: minifalda con cola lateral y vestido largo. Gala fila 10 corresponde a XL-140; XL-127 conserva Cortos con brillo por confirmación anterior.
- **XL-117:** Gala fila 27, S/389, y Brillos fila 39, código 2062, S/379, son el mismo vestido por frente y espalda. Se conserva en Gala a S/389 por confirmación específica posterior del propietario. El desacuerdo de precio entre dos fichas de WhatsApp sigue visible y requiere que el propietario actualice o confirme la oferta de Brillos.
- **Liquidación:** nueve ofertas también aparecen en otra colección y dos tienen solo la ficha de oferta. La doble aparición comercial no genera otro producto web ni exige perder el precio rebajado.

### Liquidación, artículo por artículo

| ID | Oferta | Otra aparición | Decisión y prueba |
|---|---:|---|---|
| XL-010 | S/68.70 | Cortos fila 1 | Conservar; vestido floral azul y precio idénticos a Liquidación fila 1. |
| XL-016 | S/164.50 | Brillos fila 9 | Conservar; transparente con diamantes, referencia 1475 y Liquidación fila 2. |
| XL-017 | S/194.50 | Brillos fila 4 | Conservar; dorado de una manga, referencia 708 y Liquidación fila 3. |
| XL-180 | S/86.70 | Cortos fila 2 | Conservar; satín estampado, referencia 796 y Liquidación fila 4. |
| XL-202 | S/37.80 | Solo oferta | Conservar; geométrico verde/nude, Liquidación fila 5 y fotos originales posteriores. |
| XL-155 | S/75.60 | Brillos fila 7 | Conservar; negro/plateado, referencia 174 y Liquidación fila 6. |
| XL-201 | S/48.30 | Solo oferta | Conservar; top amarillo, Liquidación fila 7 y foto original posterior. |
| XL-172 | S/119.50 | Brillos fila 8 | Conservar; mangas plateadas, referencia 165 y Liquidación fila 8. |
| XL-181 | S/115.60 | Cortos fila 3 | Conservar; volantes, referencia 1537 y Liquidación fila 9. |
| XL-169 | S/114.50 | Brillos fila 2 | Conservar; vestido verde S/M y Liquidación fila 10. |
| XL-125 | S/194.50 | Gala fila 20 | Conservar; crema de encaje, referencia 330 y Liquidación fila 11. |

Las ofertas con otra aparición permanecen en Liquidación por la ficha individual rebajada, no por el total once. XL-201 y XL-202 tienen además fotos entregadas después del catálogo histórico.

### Pendientes expresos

1. **Largos:** los 22 vestidos confirmados tienen foto y ficha web. La única entrada de esta colección de WhatsApp sin ID web es la blusa excluida. El detalle está en `confirmacion-largos-22.json` y `matriz-175.json`.
2. **Cortos:** blanco con perlas código 1894, S/319, podría ser diseño distinto del XL-187 código 1914 S/329. Confirmar con foto antes de crear otra ficha.
3. **Bandage:** falda código 1733 S/219 y negro/amarillo código 2074 S/449 no tienen ficha web identificada. XL-072, XL-076 y XL-147 aparecen en web pero no se asocian de forma inequívoca a una entrada vigente. Tampoco XL-114 en Cortos. Se conservan provisionalmente con `categoria_final_propuesta=null` en la matriz; falta confirmar vigencia o clasificación.
4. **Gala/Largos:** XL-060, 088, 091, 093, 096, 138, 139, 141, 162, 163 y 176 tienen silueta larga y apariencia lisa o brillo localizado en la fotografía, pero la lista vigente los coloca en Gala. Una regla comercial específica del propietario resolvería esta tensión. No se los movió para reproducir el antiguo total de 25.
5. **Precio XL-117:** Gala S/389 y Brillos S/379 para el mismo modelo. Se mantuvo S/389 por la instrucción específica posterior; la ficha comercial duplicada queda pendiente de rectificación.

## Validación y cambios de Antigravity

El árbol de Git estaba limpio al iniciar. El commit `8f41242` añadió la herramienta local `ordenar/` y conectó su archivo al build y a la validación; no había modificaciones sin confirmar de Antigravity. Tras las doce altas, `node build.cjs` y `node validate-seo.cjs` pasaron: 239 páginas, 239 bloques JSON-LD, 351 imágenes de sitemap y enlaces locales presentes. Las 175 fichas mantienen sus botones de WhatsApp. Los cuatro tests de `ordenar/model.test.cjs` pasaron. Se comprobaron doce fotos distintas, sus hashes y rutas.

Se abrieron visualmente en escritorio las seis colecciones generadas; encabezados, conteos, primeras tarjetas y fotos se mostraron. Se repitió la revisión con ancho móvil de 390 × 844 px; títulos, navegación, buscador, conteos y tarjetas visibles se adaptan sin desbordamiento horizontal observado. Tras las últimas cuatro altas, la colección de Largos muestra 25 modelos y los cuatro enlaces a sus fichas. Se revisó visualmente la ficha XL-211 en escritorio y móvil; el navegador se restauró al ancho anterior.
