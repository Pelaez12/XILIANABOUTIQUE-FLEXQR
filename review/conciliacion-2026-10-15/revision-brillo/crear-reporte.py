import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
source = json.loads((OUT / 'fuente-actual.json').read_text(encoding='utf-8'))
products = {p['id']:p for p in source['brillo'] + source['similares']}

DATA = '''16|Mini|Pedrería repartida por corpiño y falda azul|Conservar
17|Mini asimétrico|Lentejuelas doradas en toda superficie|Conservar
35|Mini drapeado|Lentejuelas marrones en todo cuerpo y falda|Conservar
38|Mini drapeado|Lentejuelas rosadas en cuerpo, falda y manga|Conservar
39|Corto sobre rodilla|Lentejuelas y mostacillas verdes en toda superficie|Conservar
40|Midi a pantorrilla|Lentejuelas en toda falda y parte central del cuerpo; escote liso|Conservar
49|Mini|Lentejuelas rojas en copas y falda|Conservar
51|Mini|Lentejuelas azul/celeste por cuerpo, falda y mangas|Conservar
52|Mini|Lentejuelas azules por cuerpo y falda|Conservar
54|Mini|Cintas anchas de strass cruzan desde escote hasta bajo|Conservar
57|Midi bajo rodilla|Lentejuelas blancas/tornasoladas en toda superficie|Conservar
78|Mini|Líneas de pedrería plateada cubren cuerpo y falda|Conservar
82|Midi bajo rodilla|Filas de strass desde cuello hasta cintura, mangas/falda lisas|Frontera: conservar provisionalmente
83|Midi a pantorrilla|Único fleco/tira de strass del nudo de cintura hacia abertura; resto liso|Cortos si se extiende regla de adorno localizado
85|Mini drapeado|Estampado marrón/blanco plano; no se observan lentejuelas ni pedrería|Recomendar Cortos
86|Midi a pantorrilla|Tres estrellas doradas al centro; relieves crema y falda mate|Cortos si se extiende regla de adorno localizado
114|Midi largo a pantorrilla|Pieza superior de pedrería extensa y perlas dispersas en falda|Conservar
117|Midi con flecos|Pedrería/lentejuelas dibujan toda superficie y flecos|Conservar
118|Corto sobre rodilla|Panel completo del corpiño con lentejuelas negras; falda lisa|Conservar
119|Mini|Patrón de lentejuelas verde lima por cuerpo y falda|Conservar
120|Mini|Textura de brillo granular dorado por toda superficie|Conservar
123|Mini con caída lateral|Pedrería en corpiño plateado y puntos brillantes en parte negra|Conservar
127|Mini con caída lateral larga|Corpiño y caída completa de lentejuelas, falda mini interior vino|Conservar
130|Mini con caída lateral larga|Lentejuelas concentradas en una mitad del busto; resto plomo liso|Cortos si se extiende regla de adorno localizado
132|Mini|Lentejuelas doradas densas y detalle de perlas|Conservar
133|Midi bajo rodilla|Lentejuelas azules/grises continuas por cuerpo y mangas|Conservar
134|Midi bajo rodilla|Pedrería plateada dibuja cuerpo/falda completos|Conservar
135|Mini|Líneas de perlas y strass guinda por cuerpo, falda y mangas|Conservar
149|Mini|Lentejuelas blancas tornasoladas por todo vestido|Conservar
150|Mini con flecos|Lentejuelas azules por cuerpo/falda y flecos|Conservar
151|Mini|Pedrería y lentejuelas rosas en copas y falda|Conservar
152|Mini|Cadenas/strass cubren corpiño y falda roja|Conservar
153|Mini|Falda entera de lentejuelas doradas y puños brillantes|Conservar
155|Mini|Líneas densas de strass geométrico por todo vestido|Conservar
156|Mini|Líneas de pedrería por corpiño transparente y falda negra|Conservar
157|Mini|Pedrería plateada densa en copas y por toda falda|Conservar
166|Corto a rodilla|Lentejuelas rojas por cuerpo y falda|Conservar
167|Mini|Toda falda tiene patrón de lentejuelas doradas/negras; torso negro liso|Conservar
168|Mini|Patrón de lentejuelas champagne por cuerpo y mangas|Conservar
169|Mini|Lentejuelas verdes forman retícula y franjas por todo vestido|Conservar
170|Mini|Lentejuelas verdes en toda superficie|Conservar
171|Mini|Pedrería plateada en copas, corpiño y casi toda falda verde|Conservar
172|Mini|Mangas y panel del escote con flores plateadas; material exacto incierto|Reserva de material: conservar provisionalmente'''

rows = []
for line in DATA.splitlines():
    id, length, shine, decision = line.split('|')
    p = products[int(id)]
    rows.append({'id':p['id'], 'name':p['name'], 'category_before':p['category'], 'price':p['price'], 'photos':p['photos'], 'observed_length':length, 'observed_shine':shine, 'recommendation':decision})
assert len(rows) == 43
assert set(r['id'] for r in rows) == {p['id'] for p in source['brillo']}

candidate_data = [
    (154, 'Confirmado por usuario', 'Lentejuelas/pedrería extensas; abertura desde cadera y pierna descubierta, con panel largo lateral.', 'Cortos con brillo'),
    (101, 'Pendiente alcance; similitud máxima', 'Abertura desde parte alta del muslo y frente lateral largo; strass distribuido desde escote hasta bajo.', 'Cortos con brillo si la regla incluye diseños similares a 154'),
    (89, 'Pendiente alcance', 'Falda continua hasta suelo, abertura alta lateral, muslo visible y brillo extendido.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (103, 'Pendiente alcance', 'Falda larga recta de lentejuelas verdes; abertura lateral por encima de rodilla.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (137, 'Pendiente alcance', 'Falda sirena de lentejuelas con cola; abertura alta lateral.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (140, 'Pendiente alcance', 'Falda maxi lisa con abertura alta; todo el corpiño cubierto de líneas de strass.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (160, 'Pendiente alcance', 'Falda larga de lentejuelas con abertura lateral alta y muslo visible.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (161, 'Pendiente alcance', 'Falda azul maxi lisa con abertura alta; corpiño y mangas ampliamente brillantes.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (164, 'Pendiente alcance', 'Tela blanca de lentejuelas, falda larga con cola y abertura alta.', 'Cortos con brillo si se incluyen todas las aberturas altas'),
    (110, 'Caso separado: transparencia', 'Sobrefalda brillante transparente hasta suelo sobre forro corto; piernas visibles por tul, sin abertura como 154.', 'Mantener Gala hasta aclarar si transparencia entra en la regla'),
]
candidates = []
for id, status, reason, decision in candidate_data:
    p = products[id]
    candidates.append({'id':id, 'category_before':p['category'], 'price':p['price'], 'photos':p['photos'], 'status':status, 'visual_reason':reason, 'recommendation':decision})

report = {'date':'2026-10-15', 'catalogue_products':source['total'], 'current_brillo_count':43,
          'current_rows':rows, 'outside_candidates':candidates,
          'clear_recommended_changes':[{'id':154,'from':'Gala','to':'Cortos con brillo','basis':'Instrucción explícita del usuario'}, {'id':85,'from':'Cortos con brillo','to':'Cortos','basis':'Estampado plano sin brillo observado en original'}],
          'conditional_detail_changes':[83,86,130], 'keep_provisional':[82,172],
          'pending_high_slit':[101,89,103,137,140,160,161,164], 'pending_transparency':[110],
          'catalogue_modified':False}
(OUT/'reporte-brillo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

header = '''# Revisión independiente de Cortos con brillo — 15 de octubre de 2026

Se revisaron las 43 principales guardadas en Cortos con brillo, los candidatos con aberturas de Gala y las láminas actuales completas de Gala y Largos. Se abrieron originales y espaldas de los casos dudosos. Las láminas nuevas usan products.js; las etiquetas de las láminas del 14 no se trataron como clasificación actual. No se modificó el catálogo.

## Cambios claros por evidencia

- **XL-154: Gala → Cortos con brillo.** Instrucción explícita del usuario al mostrar esta misma foto. Tiene lentejuelas y pedrería, abertura hasta cadera y pierna descubierta con panel largo que cae al lado. No depende de la respuesta sobre el resto de aberturas.
- **XL-085: recomendar Cortos con brillo → Cortos.** El original 01-R013.jpeg (1086×1448) muestra un estampado marrón y blanco de formas planas, continuas y rellenas; no se ve lentejuela, pedrería, perla ni textura granular de brillo. La segunda foto 02-R162.jpeg es otra versión del mismo frente y coincide. El nombre y su coincidencia con la fila 23 de la lista oficial de Cortos apoyan la foto; no se usaron por sí solos para decidir.

**Discrepancia con el reporte previo de Cortos:** allí se describió el dibujo de XL-085 como brillo extendido. Al abrir el original, mi lectura independiente es estampado plano. Recomiendo que el agente principal compruebe esa foto antes de aplicar el cambio. No es un caso de adorno localizado, sino de ausencia de brillo visible.

Aplicar únicamente estos dos cambios dejaría 43 Cortos con brillo por aritmética. Ese número no se usa como argumento de clasificación ni como objetivo.

## Adorno localizado: cambios condicionados

La regla del usuario sobre adornos concentrados se comunicó para Largos. Para mantener la decisión comercial bajo control, las siguientes salidas de Brillo siguen condicionadas a extenderla también a Cortos:

- **XL-083 → Cortos:** blanco midi y mangas capa de tela lisa. Un fleco/tira de strass sale del nudo de cintura y acompaña una abertura. El frente y la espalda restantes son lisos.
- **XL-086 → Cortos:** crema midi de gasa; tres estrellas doradas al centro son el único brillo claro. Los pequeños relieves crema del corpiño parecen aplicaciones textiles mates; la falda es lisa.
- **XL-130 → Cortos:** minifalda ploma real, confirmada por espalda, con caída lateral larga. Las lentejuelas están en una mitad del busto; cuerpo, falda y caída restantes son lisos. La cola no lo convierte en Gala.

Si se autorizan los tres después de los dos cambios claros, Brillo quedaría en 40. No recomiendo completar la cifra moviendo otros vestidos por parecido de color o nombre.

## Modelos que conservaría con reserva

**XL-082:** las filas de strass no se limitan al borde del escote: bajan por ambos lados del corpiño hasta la cintura. Las mangas y falda son lisas. Es fronterizo entre decoración concentrada y corpiño decorado; lo conservaría provisionalmente en Brillo, sujeto a cómo el usuario delimite esa decoración. No lo junto automáticamente con 83/86/130.

**XL-172:** flores plateadas ocupan ambas mangas completas y un panel amplio del escote. No son un pequeño borde, pero el original no permite distinguir con seguridad bordado de hilo plateado frente a lentejuela. Mantener provisionalmente en Brillo es razonable; solo movería a Cortos si se confirma que el bordado es mate y no se considera brillo comercialmente. No basta que la falda sea lisa para sacarlo.

## Similares a XL-154 fuera de Brillo

**XL-101 es el más cercano.** Tiene abertura desde la parte alta del muslo, casi cadera, una pierna descubierta y panel largo que cae por el lado. No se propone aplicar el cambio antes de resolver el alcance pendiente de la regla.

**XL-089, XL-103, XL-137, XL-140, XL-160, XL-161 y XL-164** muestran muslo mediante una abertura alta y tienen brillo real extendido en falda o corpiño. Conservan una falda exterior larga continua, por lo que dependen de si el usuario incluye toda abertura alta o solo la construcción semejante a 154.

**XL-110 es distinto:** hay una sobrefalda larga transparente y brillante sobre forro corto. La pierna se ve por el tul, sin la abertura lateral de 154. No lo trasladaría por la regla de abertura sin incluir expresamente transparencia.

**XL-099 no es candidato de abertura alta.** Su falda sirena es continua hasta suelo. Tampoco añadiría 68 por una abertura que empieza aproximadamente a la altura de la rodilla. Las aberturas de 6/20/24/93/96/100/113/162/173/178 no los convierten en Brillo: sus cuerpos son lisos, estampados o tienen detalles concentrados; corresponden al cruce de Largos/Cortos según la regla comercial que se confirme.

Los mini con caída larga **XL-123 y XL-127** ya están bien dentro de Brillo, y 130 está pendiente solo por la extensión del brillo, no por su longitud. XL-118, XL-153 y XL-167 conservan Brillo: la decoración cubre respectivamente todo el corpiño o toda la falda, y supera un detalle pequeño.

## Matriz de las 43 prendas actuales

'''
md = header + '| ID | Longitud observada | Brillo observado | Recomendación |\n|---|---|---|---|\n'
for r in rows:
    md += f"| XL-{r['id']:03} | {r['observed_length']} | {r['observed_shine']} | {r['recommendation']} |\n"
md += '\n## Matriz de candidatos externos\n\n| ID | Estado | Motivo visual | Recomendación |\n|---|---|---|---|\n'
for c in candidates:
    md += f"| XL-{c['id']:03} | {c['status']} | {c['visual_reason']} | {c['recommendation']} |\n"
md += '''
## Evidencia guardada

- `brillo-actual-1.jpg` a `brillo-actual-3.jpg`: principales de las 43 prendas actuales.
- `similares-1.jpg`: comparación de 154 con 101, las demás aberturas y 110.
- `detalles-1.jpg` y `detalles-2.jpg`: detalles y espaldas que distinguen extensión del brillo y construcción de falda.
- `fuente-actual.json`: snapshot de precios, fotos y clasificación al inicio de esta revisión.
- `reporte-brillo.json`: decisiones estructuradas y matriz con precios/galerías de referencia.

No se alteró ningún precio, foto, prenda, categoría ni manifiesto compartido. Las 225 fotos del catálogo permanecen intactas; los archivos de esta carpeta son evidencia de revisión.
'''
(OUT/'REPORTE-BRILLO.md').write_text(md,encoding='utf-8')
print(f'Reporte de {len(rows)} prendas actuales y {len(candidates)} candidatos externos creado.')
