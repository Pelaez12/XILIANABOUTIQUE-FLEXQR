# Revisión visual Bandage y Liquidación — 20 de octubre de 2026

Se revisaron las 52 fotos publicadas de 36 fichas: Bandage 25 fichas/38 fotos; Liquidación 11 fichas/14 fotos. No se consultó ni incluyó la colección PENDIENTES de WhatsApp. XL-200, XL-201 y XL-202 sí se revisaron porque están publicados en estas categorías. No se encontraron AGENTS.md aplicables en el proyecto o sus carpetas superiores inmediatas. No se modificó el catálogo.

## Hallazgos

| Fichas | Resultado | Certeza | Evidencia |
|---|---|---|---|
| XL-077 foto 1 / foto 2 | Misma toma frontal en distinta escala/recorte dentro de una galería; no dos productos diferentes. | Alta | `01-R055.jpeg` y `03-R148.jpeg`: misma posición de cara, brazos, manos y vestido. La foto 3 aporta espalda. Comparativa `amarillos.jpg`. |
| XL-076 / XL-116 | Posible mismo modelo amarillo mini fotografiado en sesiones distintas. No son fotos duplicadas exactas. | Media-alta | Copas con aro, tirantes, paneles de corsé y costuras de cintura/cadera muy parecidos; ambos S/389. XL-076 solo tiene frente. La matriz histórica asocia XL-116 al código 1969 y no demuestra código independiente para XL-076. No hay confirmación específica que pruebe identidad o diferencia. Comparativas `amarillos.jpg`, `amarillos-detalle.jpg`. |
| XL-115 / XL-200 / XL-215 | El conjunto XL-115 muestra componentes comercializados individualmente como bralette XL-200 y falda XL-215. No se debe considerar duplicación de ficha completa. | Alta en el bralette; media-alta en falda | Pedrería multicolor bajo copas negras y falda de cintura negra, franjas cruzadas blancas/rosadas; la foto extendida muestra parte superior gris. Precios S/349 conjunto, S/199 bralette, S/219 falda. `conjunto-bralette.jpg`, `falda-conjunto.jpg`. |

No se encontró ninguna galería que mezcle prendas diferentes. Frente/espalda y otras poses son vistas válidas de cada producto. Las 14 fotos de Liquidación corresponden de forma coherente a sus 11 fichas y no repiten modelos entre ellas. La similitud de color en los amarillos XL-077 y XL-076/XL-116 no basta para unirlos: XL-077 es midi, presenta paneles y escote diferentes.

SHA-256 calculado sobre archivos reales: ningún duplicado binario entre las 52 fotos (`hashes.json`). Esto no descarta recortes o un mismo producto en sesiones distintas.

## Evidencias

- `inventario.json`: inventario completo de 52 rutas y fichas revisadas.
- `contacto-01.jpg`, `contacto-02.jpg`, `contacto-03.jpg`: todas las fotos publicadas de las categorías asignadas, sin omisiones.
- `hallazgos.json`: resultados estructurados con rutas exactas.
- `hashes.json`: hashes de archivo comprobados.

La revisión es fotográfica. La identidad absoluta del par XL-076/XL-116 no puede cerrarse con sus fotos disponibles; conservar fichas y no fusionar automáticamente.

## Cruces con candidatos globales

Se inspeccionó `cruces-metricas.jpg`: los pares automáticos XL-010 con XL-040/XL-162/XL-100/XL-141/XL-163, XL-125 con XL-176/XL-086/XL-102, XL-077 con XL-085/XL-084/XL-192 y XL-051 con XL-216 son falsos positivos del algoritmo por silueta/fondo blanco. Se distinguen sin ambigüedad por color, longitud, escote, mangas y diseño. Ninguno repite el modelo de la ficha comparada.
