# Revisión visual de Cortos y Cortos con brillo — 20 de octubre de 2026

Se revisaron todas las fotos del catálogo publicado en `products.js`: 29 productos / 48 fotos de Cortos y 37 productos / 64 fotos de Cortos con brillo; total 66 productos / 112 fotos. Se excluyeron las fuentes y la colección de WhatsApp PENDIENTES por indicación del propietario. No existe una categoría web Pendientes. Los productos publicados se revisaron donde están actualmente.

No se encontró un modelo duplicado entre dos fichas de estas dos categorías ni una foto inequívoca de una prenda diferente dentro de sus galerías. Se revisaron además las 112 portadas de las otras categorías para detectar cruces; no apareció un duplicado con Cortos o Brillos. Esto es una evaluación visual, complementaria al análisis global de semejanza, y no una prueba de identidad por fotografía en los casos de una sola vista.

## Repeticiones de vista dentro de una misma ficha

Estas repeticiones no representan productos duplicados. No se modificaron ni eliminaron fotos.

| ID | Fotos | Evaluación y certeza | Evidencia |
|---|---|---|---|
| XL-085 | `01-R013.jpeg`, `02-R162.jpeg` | Misma toma frontal, encuadre casi idéntico; alta certeza visual. Los archivos tienen SHA distintos. | `comparacion-XL-085.jpg` |
| XL-187 | `03-propietario-frente.png`, `01-WA-Cortos-blanco-frente.png` | Misma fotografía frontal en distinta resolución/compresión; alta certeza visual. La tercera foto es la prenda sola. La incorporación previa de la versión de mayor resolución conservó la anterior por instrucción del propietario. | `comparacion-XL-187.jpg` |
| XL-084 | `01-R010.jpeg`, `02-R159.jpeg` | Misma vista frontal/pose del vestido amarillo, con fondo y escala diferentes. Alta certeza de misma prenda; variante de presentación, no una espalda. | `comparacion-XL-084.jpg` |
| XL-131 | `01-R009.jpeg`, `02-R158.jpeg` | Misma vista frontal del vestido azul, presentada con escala/encuadre diferentes. Alta certeza de misma prenda. | `comparacion-XL-131.jpg` |

Las rutas de las fotos anteriores comienzan por `images/productos-reales/XL-NNN/`, según el ID de cada fila.

## Candidatos automáticos descartados visualmente

La similitud de pose, modelo y fondo blanco produce coincidencias de hash perceptual que no corresponden a la misma prenda. Evidencia comparada: `candidatos-descartados.jpg`.

| Fichas | Motivo concreto para descartarlas |
|---|---|
| XL-122 / XL-131 | Negro corto con escote sin tirantes frente a azul midi con cuello asimétrico y abertura de lágrima. |
| XL-035 / XL-121 | Marrón de lentejuelas con busto de corsé frente a negro liso con múltiples tiras. |
| XL-084 / XL-192 | Amarillo de tirantes rectos frente a blanco drapeado con tiras caídas de hombros. |
| XL-084 / XL-085 | Amarillo liso de tirantes frente a marrón estampado con mangas largas. |
| XL-039 / XL-120 | Verde de cuello cerrado con malla frente a dorado de tirantes y escote pronunciado. |
| XL-057 / XL-119 | Blanco largo a rodilla con escote de corazón frente a verde limón mini con cuello halter profundo. |
| XL-040 / XL-051 | Verde midi sin mangas con hombros caídos frente a azul mini de mangas largas. |

XL-038 se examinó individualmente porque sus tres imágenes frontales parecían muy parecidas en miniatura: muestran poses diferentes, la misma manga única y falda cruzada de lentejuelas rosadas; no hay duplicado de toma demostrado. Evidencia: `comparacion-XL-038.jpg`.

## Evidencias y alcance

- `inventario-fotos.json`: las 112 rutas publicadas con ID y posición en galería.
- `contacto-01.jpg` a `contacto-04.jpg`: todas las fotos revisadas.
- `cruces-portadas-01.jpg` a `cruces-portadas-04.jpg`: portadas del resto del catálogo para cruce visual.
- Las cinco comparaciones individuales citadas permiten verificar las galerías que exigieron mayor detalle.

No se encontraron archivos AGENTS.md en el proyecto ni en la raíz de trabajo inmediata mediante la búsqueda de archivos. El catálogo y los precios no se editaron.
