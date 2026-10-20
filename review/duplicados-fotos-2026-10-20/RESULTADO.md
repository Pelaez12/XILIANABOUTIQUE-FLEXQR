# Auditoría de fotos duplicadas · 20 de octubre de 2026

**Resolución posterior del propietario:** se retiró **XL-173** y se conservó **XL-214 a S/549 en Largos**. La auditoría de abajo conserva los resultados sobre las 178 fichas originales. El catálogo corregido tiene **177 fichas y 25 en Largos**. [Resolución con ambas fichas originales](resolucion-xl173.json). El par amarillo XL-076/XL-116 continúa como posible; no se fusionó.

Se revisaron **297 fotos de 178 fichas publicadas** mediante tres agentes y una comprobación global. Se excluyó la colección **PENDIENTES de WhatsApp**, según la indicación del propietario. Las prendas ya incorporadas al catálogo se revisaron en su categoría publicada, incluidas las altas XL-197 a XL-217. El catálogo, sus precios y fotografías se conservaron.

## Cobertura comprobada

| Colección publicada | Fichas | Fotos |
|---|---:|---:|
| Gala | 50 | 95 |
| Largos | 26 | 38 |
| Cortos | 29 | 48 |
| Cortos con brillo | 37 | 64 |
| Bandage | 25 | 38 |
| Liquidación | 11 | 14 |
| **Total** | **178** | **297** |

Los inventarios de los tres agentes coinciden exactamente con todas las rutas e identidades publicadas: no quedó ninguna foto fuera de la revisión. Todos los archivos se pudieron abrir y todos los SHA-256 declarados coinciden con los archivos reales.

## Modelos duplicados entre fichas

| Fichas | Resultado | Evidencia y diferencia que requiere atención |
|---|---|---|
| **XL-173 / XL-214** | **Duplicado confirmado** | Es el mismo vestido rosado largo floral y la misma fotografía: mangas abullonadas, rosa en cintura, abertura y colocación de las flores idénticas. Ambas fotos tienen 1122 × 1402 px; cambian formato/compresión. XL-173 está a **S/450** y XL-214 a **S/549**. La incorporación de XL-214 reprodujo una prenda ya representada por XL-173. [Comparación ampliada](gala-largos/duplicado-173-214.jpg). |
| **XL-076 / XL-116** | **Posible duplicado; falta confirmar identidad** | Vestidos Bandage amarillos mini a **S/389**, con copas, tirantes y paneles de corsé muy semejantes, en sesiones diferentes. Solo XL-116 tiene código WhatsApp 1969 acreditado. XL-076 carece de espalda o un código independiente demostrado; no se puede resolver de forma definitiva con las fotos disponibles. [Frente y detalle](bandage-liquidacion/amarillos-detalle.jpg). |

El desacuerdo de precio del vestido rosado queda expresamente registrado. Esta auditoría verifica la duplicación fotográfica y no decide qué ficha o precio debe conservarse ni elimina productos. Las confirmaciones y referencias de cada ficha siguen en [el informe de Gala/Largos](gala-largos/INFORME.md).

## Conjunto y piezas individuales

**XL-115 Conjunto Bandage** contiene piezas visualmente coincidentes con **XL-200 Bralette negro con pedrería de colores** y **XL-215 Falda Bandage Dress**. El conjunto cuesta S/349; las piezas, S/199 y S/219. Esto es una relación de conjunto/componentes y no demuestra que las tres fichas completas sean duplicadas. La coincidencia del bralette es alta y la de la falda media-alta. [Bralette comparado](bandage-liquidacion/conjunto-bralette.jpg), [falda comparada](bandage-liquidacion/falda-conjunto.jpg).

## Repeticiones dentro de galerías

| Ficha | Fotos | Resultado |
|---|---|---|
| XL-077 | 1 y 2 | Misma toma frontal con diferente recorte; la tercera foto sí muestra espalda. |
| XL-085 | 1 y 2 | Misma toma frontal en dos archivos. |
| XL-187 | 1 y 2 | Misma foto a distinta resolución; la nueva imagen original se agregó conservando la anterior. La tercera foto muestra la prenda sola. |
| XL-084 | 1 y 2 | Misma vista y pose con cambios de fondo/escala; variante de presentación. |
| XL-131 | 1 y 2 | Misma vista frontal y pose con cambios de encuadre/escala. |

Las cinco galerías están ilustradas en los informes de [Bandage/Liquidación](bandage-liquidacion/INFORME.md) y [Cortos/Brillos](cortos-brillos/INFORME.md). Una toma repetida dentro de la misma ficha no es otro producto. No se detectaron galerías con fotografías inequívocas de una prenda ajena.

## Método y límites

Se calcularon hashes binarios, de píxeles y perceptuales sobre todas las fotos, incluyendo comparación del centro y del espejo. **No hay archivos ni píxeles exactamente repetidos**, pero eso no descarta fotografías recomprimidas: XL-173/XL-214 y las repeticiones de galerías lo demuestran.

El filtro global produjo **61 pares de fotos entre fichas**, inspeccionados visualmente: uno corresponde a XL-173/XL-214 y los otros 60 se descartaron por diferencias de color, escote, longitud, mangas o aplicaciones. Los fondos, modelos y poses compartidos explican esas similitudes automáticas. Los 27 pares del filtro dentro de la misma ficha incluyen vistas válidas de frente/espalda, poses distintas y algunas repeticiones; no se consideraron duplicados de producto.

La inspección completa por agentes encontró además el posible par XL-076/XL-116 y las relaciones del conjunto XL-115, que no dependieron del umbral de hashes. Una fotografía única no permite probar por sí sola la identidad comercial absoluta de dos vestidos similares; por eso el amarillo queda como posible, no confirmado.

Datos y trazabilidad:

- [Resultado estructurado y cobertura](resultado.json).
- [Inventario completo y métricas](analisis.json).
- [Revisión individual de las 76 fichas de Gala/Largos](gala-largos/revision-visual.json).
- Hojas de contacto con **todas las fotos** en las tres carpetas de agentes.
- `analizar.py` reproduce hashes y candidatos; `consolidar.py` comprueba cobertura exacta y reúne resultados.

No se requirió reconstruir la web: se generaron únicamente registros y evidencias de auditoría en esta carpeta.
