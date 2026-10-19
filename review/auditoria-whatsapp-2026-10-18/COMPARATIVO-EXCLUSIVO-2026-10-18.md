# Comparación del catálogo de WhatsApp con la web local

Fecha: 18 de octubre de 2026. Fuente: `inventario_actualizado.json` (272 entradas observadas), `pendientes_unificados.json` (56 artículos únicos) y la compilación local de `XILIANA`.

## Criterio de conteo

- Un artículo de la lista de Liquidación se cuenta **solo en Liquidación**, aunque WhatsApp también lo muestre en una colección de vestidos. De sus 11 entradas, 9 repiten artículos de las colecciones principales y 2 figuran solo en Liquidación. Son 10 vestidos y 1 top.
- PENDIENTES 1, 2 y 3 tienen 83 entradas en conjunto. Hay 27 entradas repetidas verificadas; por tanto, equivalen a **56 artículos únicos**, agrupados en una sola sección de la web.
- Los dos artículos llamados «Vestido corto negro con plateado» se distinguen por precio: S/ 75.60 corresponde a Liquidación y S/ 449.00 permanece en Cortos con brillo.
- El usuario confirmó que las fichas 2024 y 2025 de Cortos muestran el mismo vestido verde. Se conserva la ficha **2025 a S/ 429.00**; la 2024 a S/ 359.00 se considera duplicada para el conteo web.

| Categoría final | WhatsApp, artículos únicos | Web local | Diferencia |
| --- | ---: | ---: | ---: |
| Gala | 52 | 50 | 2 |
| Largos | 23 | 13 | 10 |
| Cortos con brillo | 38 | 37 | 1 |
| Cortos | 29 | 29 | 0 |
| Bandage | 22 | 23 | −1 |
| Liquidación | 11 | 11 | 0 |
| Pendientes, lista única | 56 | 56 | 0 |
| Calzados | 1 | 0 | 1 |
| Accesorios u otros | 3 | 0 | 3 |
| **Total** | **235** | **219** | **16** |

**Cobertura por cantidad:** 219 ÷ 235 = **93.19 %**; el saldo es de 16 artículos por cantidad, equivalentes al **6.81 %**. Antes de crear la lista única de Pendientes y añadir las fichas verificadas, la web tenía 157 ÷ 235 = 66.81 % por cantidad. Esta métrica compara el número de artículos y no acredita identidad ni similitud de fotos. Bandage tiene una ficha web más que la colección de WhatsApp; esa diferencia no identifica por sí sola cuál ficha sobra.

**El saldo de 16 no equivale a 16 nombres identificados.** Una ficha web sobrante o duplicada puede compensar numéricamente otra ficha ausente. La comparación individual dejó 36 entradas de prendas de WhatsApp sin emparejamiento inequívoco y 24 fichas web sin correspondencia única. No es correcto seleccionar 16 de ellas y llamarlas ausentes.

Entre prendas de las cinco colecciones principales y Liquidación, WhatsApp suma 175 artículos únicos frente a 163 fichas web: diferencia de 12 por cantidad. Liquidación tiene los 10 vestidos y el «Top Amarillo» con ficha web. «Vestidos largo estampado geométrico (Verde y Nude)» figura a S/ 37.80 (antes S/ 189.00) con dos fotos entregadas por el usuario; la ficha observada de WhatsApp registraba una foto.

## Estado de la comparación individual

La comparación conservadora por código visible o nombre único emparejó 137 de las 173 entradas únicas de las cinco colecciones principales. En esas coincidencias no se detectaron diferencias de precio ni de categoría, teniendo en cuenta la exclusividad de Liquidación. Otras 36 entradas no tienen un emparejamiento inequívoco bajo esas reglas; **no se puede afirmar que las 36 falten**. Hay 24 fichas web sin correspondencia única bajo el mismo método. Las fotos de todas las prendas no se compararon una a una. Se agregaron a Largos el «Vestido estampado floreado», código 1842, S/ 629.00, con cuatro fotos; el «Vestido largo blanco con estampado flores», S/ 269.00, con una; y el «Vestido rojo estraple con detalles», código 2022, S/ 339.00, con dos. Se agregó a Bandage el «Bralette negro con pedrería de colores», código 1806, S/ 199.00, con las tres fotos de producto de la ficha WhatsApp. Se agregó a Liquidación el «Top Amarillo», S/ 48.30 (antes S/ 69.00), con una foto, y «Vestidos largo estampado geométrico (Verde y Nude)», S/ 37.80 (antes S/ 189.00), con dos fotos entregadas por el usuario. El montaje adicional del bralette quedó solo como referencia de auditoría. El vestido verde de Cortos 2024/2025 se mantiene como una sola ficha, con nombre y precio de 2025.

Los 56 pendientes ya figuran en una sola página local con nombre y precio del catálogo. Sus fotos originales no se obtuvieron: las capturas guardadas muestran la interfaz de WhatsApp y no se publicaron como imágenes del producto. La página pide solicitar la foto a la boutique. Calzados y Accesorios u otros todavía no se han incorporado a la web.

## Cambios locales

- Nueve vestidos existentes de Liquidación figuran únicamente en esa categoría; dejaron de aparecer en Gala, Cortos y Cortos con brillo. El vestido Bandage Blanco/Negro conserva un descuento en la web, pero no está en la lista de Liquidación de WhatsApp y permanece en Bandage.
- La web local tiene una sola ruta de pendientes: `/colecciones/pendientes/`, con 56 nombres y precios sin duplicados.
- La compilación local pasó la validación SEO y de enlaces: 171 páginas, 56 filas de pendientes, 11 fichas de Liquidación y 13 fotos de las seis fichas nuevas.

Estos cambios están en el proyecto local; esta auditoría no confirma una publicación en el sitio remoto.
