# Revisión visual de Gala y Largos — 20 de octubre de 2026

Se inspeccionaron las 133 fotos publicadas de 76 fichas: Gala 50 fichas/95 fotos y Largos 26 fichas/38 fotos. Incluye todos los frentes, espaldas y detalles disponibles. Los seis mosaicos `hoja-01.jpg` a `hoja-06.jpg` muestran cada foto con su ID e índice; `inventario.json` conserva las rutas. `revision-visual.json` registra la revisión por ficha.

Se excluyó la colección/fuente de WhatsApp Pendientes según la instrucción del propietario. Los productos ya publicados se revisaron por su categoría web vigente. No se modificó products.js, ni se eliminó producto o fotografía.

## Duplicado confirmado

| Fichas | Evidencia | Certeza | Decisión de auditoría |
|---|---|---|---|
| XL-173 y XL-214 | Misma pose y fotografía del vestido rosado largo floral: mangas abullonadas, escote en V, rosa en cintura y abertura frontal. Rutas `images/productos-reales/XL-173/01-N029.jpeg` y `images/productos-reales/XL-214/01-frente.png`; ambas 1122 × 1402 px. La compresión/formato produce hashes distintos. Comparación ampliada en `duplicado-173-214.jpg`. | Confirmado visualmente | Son una identidad de producto representada por dos fichas. Conservar ambas evidencias; informar al coordinador antes de consolidar. XL-173 figura S/450 confirmado el 12/10; XL-214 S/549, código WhatsApp 2083, inventario 18/10 y foto entregada 19/10. |

## Parecidos revisados y descartados

| Fichas | Diferencia concreta | Decisión |
|---|---|---|
| XL-106 / XL-159 | XL-106 lleva canesú de tul transparente en hombros/espalda y cuello plateado continuo; XL-159 lleva cuerpo/hombros opacos azul muy oscuro y otros motivos dorados en cuello y puños. | Dos prendas distintas; conservar. |
| XL-203 / XL-204 | Comparten estampado floral rosa, pero XL-203 tiene un solo hombro y cinturón liso; XL-204 tiene escote halter profundo y hebilla metálica. | Dos modelos distintos; conservar. |
| XL-162 / XL-199 | Ambos rojos con hombros descubiertos, pero XL-162 tiene manga larga y pedrería en escote; XL-199 tiene banda horizontal, botonadura/adorno en cintura y cae lateralmente como capa. | Dos modelos distintos; conservar. |
| XL-102 / XL-141 | XL-102 es blanco con aplicaciones plateadas/moradas y tirantes; XL-141 es azul con otro corpiño y cola. | No es la misma foto ni la misma variante vendible; conservar. |

No se detectó foto de otra prenda insertada en las galerías de Gala o Largos. Las vistas de frente/espalda de cada ficha mantienen escote, material, estampado y costuras compatibles. No se cuenta como duplicación de fichas la repetición de la prenda en diferentes poses dentro de su propia galería. Los cruces con las restantes categorías se completan en la revisión global del coordinador.

Revisión de los candidatos automáticos: se verificaron los 26 pares de fotos entre fichas internas Gala/Largos de `analisis.json`. Solo XL-173/XL-214 corresponde a duplicado. Los otros 25 pares se descartaron por prendas distintas; razones concretas en `candidatos-internos-revisados.json`. Las métricas similares responden a siluetas/fondos/poses parecidos.
