import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
text = (ROOT/'products.js').read_text(encoding='utf-8-sig')
products = json.JSONDecoder().raw_decode(text[text.index('['):])[0]
by_id = {p['id']:p for p in products}
ids = [16,17,35,38,39,40,49,51,52,57,78,82,89,101,103,114,117,118,119,120,123,127,54,132,133,134,135,137,140,167,150,153,155,149,151,152,154,156,157,160,161,164,166,168,169,170,171,172]
assert len(ids) == len(set(ids)) == 48
old = json.loads((ROOT/'review/conciliacion-2026-10-15/revision-brillo/reporte-brillo.json').read_text(encoding='utf-8'))
old_rows = {r['id']:r for r in old['current_rows']}
old_candidates = {r['id']:r for r in old['outside_candidates']}
gala = [89,101,103,137,140,160,161,164]
cortos = [54,82,114,118,172]
notes = {
    54: 'Referencia explícita del usuario: pocas bandas anchas de strass sobre base negra/azul lisa; conserva mucha tela lisa y espalda totalmente lisa.',
    82: 'Filas de strass limitadas al cuello y a los lados del busto/cintura; mayor parte del vestido, mangas y toda falda lisos. El brillo ocupa menos superficie que en 54.',
    114: 'Midi hasta pantorrilla baja: capa de hombros brillante y perlas puntuales sobre cuerpo/falda negros lisos; espalda completamente lisa por debajo de capa. Brillo concentrado comparable a detalle.',
    118: 'Todo el brillo está en un panel del corpiño. Cintura, falda, bajo y banda del hombro son negros lisos. El brillo queda confinado a un bloque pequeño del vestido.',
    172: 'Flores plateadas solo en ambas mangas y un panel del escote; mayoría del torso y falda completamente lisos. Aunque el hilo plateado brille, no domina el vestido.',
    123: 'Original confirma lentejuelas plateadas por todo corpiño Y lentejuelas negras por toda falda/caída. La zona negra no es tela lisa; brillo extendido real muy superior a 54.',
    127: 'Única imagen 720x960: patrón animal print en corpiño y caída, minifalda interior vino satinada. No permite confirmar lentejuela frente a estampado. Se conserva categoría previa por incertidumbre material; no se afirma brillo probado.',
    153: 'Blusa blanca lisa y falda completa de lentejuelas doradas, con puños brillantes. El bloque continuo de falda brillante domina la lectura y supera claramente unas bandas decorativas.',
    167: 'Torso y mangas negros lisos; toda falda mini tiene patrón denso de lentejuelas doradas/negras. Bloque extenso y continuo de brillo, superior a los detalles de 54.',
    154: 'Excepción comercial individual confirmada antes por el usuario. Abertura extrema, corsé de pedrería y falda de lentejuelas; se conserva Brillo sin extender la excepción a otros maxis.',
    40: 'Lentejuelas densas en casi todo cuerpo y falda midi; solo la banda del escote/hombros es terciopelo liso. Brillo dominante en superficie extensa.',
    49: 'Faldita y copas/manga asimétrica con lentejuelas densas; abdomen de corsé satinado liso. El brillo ocupa los bloques mayores del vestido, no unas pocas bandas.',
    156: 'Pedrería repetida por copas, estructura del corpiño y numerosas filas de toda falda; las copas también tienen textura brillante. Densidad y continuidad muy superiores a 54.',
    171: 'Pedrería en copas, estructura del corpiño y flecos/filas densos por casi toda falda. El patrón se distribuye por la prenda, no solo por el borde.',
}
rows = []
for id in ids:
    p = by_id[id]
    previous = old_rows.get(id)
    candidate = old_candidates.get(id)
    length = previous['observed_length'] if previous else 'Maxi hasta suelo con abertura alta'
    shine = previous['observed_shine'] if previous else candidate['visual_reason']
    if id == 127:
        shine = 'Patrón animal print; material de brillo no confirmado'
    destination = 'Gala' if id in gala else 'Cortos' if id in cortos else 'Cortos con brillo'
    reason = notes.get(id)
    if id in gala:
        reason = 'Falda exterior larga hasta suelo y brillo extenso. La abertura alta descubre la pierna pero no convierte su falda maxi en corta; corregir traslado anterior.'
        if id == 140:
            reason += ' La extensión del brillo del corpiño merece cotejo en revisión Gala; su longitud excluye Cortos con brillo.'
        if id == 161:
            reason += ' La extensión del brillo de corpiño/mangas merece cotejo en revisión Gala; su longitud excluye Cortos con brillo.'
    if reason is None:
        reason = f'{shine}. El brillo se repite densamente por la superficie y domina más que las bandas aisladas de 54.'
    confidence = 'Material incierto; conservar provisional' if id == 127 else 'Excepción comercial explícita' if id == 154 else 'Recomendación clara'
    state = 'Ya coincide en products.js al crear reporte' if p['category'] == destination else 'Propuesto; no aplicado por este agente'
    rows.append({'id':id,'name':p['name'],'price':p['price'],'photos':p['photos'],'image':p['image'],
                 'category_at_start_review':'Cortos con brillo','category_in_source_at_report':p['category'],
                 'observed_length':length,'observed_shine':shine,'recommended_category':destination,
                 'decision_basis':reason,'confidence':confidence,'application_state':state})

snapshot = {'products':products,'review_ids':ids,'catalogue_count':len(products),'photos_count':sum(len(p['photos']) for p in products)}
(OUT/'productos-al-generar-reporte.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
report = {'date':'2026-10-15','reviewed_count':48,'reference_id':54,'revised_user_rule':'Brillo dominante y extendido; detalle localizado queda en Cortos. Falda maxi sigue larga aunque tenga abertura.',
          'recommended_to_gala':gala,'recommended_to_cortos':cortos,'material_uncertain_keep':[127],'commercial_exception_keep':[154],
          'keep_large_shiny_skirt_blocks':[153,167],'recommended_brillo_count':35,'rows':rows,'shared_catalogue_modified_by_agent':False}
(OUT/'reporte-brillo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
def sheets(photos,basename,cols=4,per_page=12):
    for start in range(0,len(photos),per_page):
        group = photos[start:start+per_page]
        canvas = Image.new('RGB',(360*cols,590*((len(group)+cols-1)//cols)),'#f1f1ec')
        d = ImageDraw.Draw(canvas)
        for i,(id,photo) in enumerate(group):
            p = by_id[id]
            x,y = i%cols*360,i//cols*590
            im = Image.open(ROOT/photo['src'].removeprefix('./')).convert('RGB')
            im = ImageOps.contain(im,(350,510))
            canvas.paste(im,(x+(360-im.width)//2,y))
            r = next(r for r in rows if r['id']==id)
            d.text((x+5,y+515),f"XL-{id:03} | {photo.get('view','?')}",fill='#111',font=font)
            d.text((x+5,y+545),f"Propuesto: {r['recommended_category']}",fill='#111',font=small)
            d.text((x+5,y+568),Path(photo['src']).name,fill='#111',font=small)
        canvas.save(OUT/f'{basename}-{start//per_page+1}.jpg',quality=94)

sheets([(id,next(p for p in by_id[id]['photos'] if p['src']==by_id[id]['image'])) for id in ids],'brillo-48-revision')
detail_ids=[54,82,114,118,172,123,153,167,127,40,49,156,171]
sheets([(id,p) for id in detail_ids for p in by_id[id]['photos']],'comparacion-umbral',cols=3,per_page=9)

md = '''# Revisión de las 48 prendas de Cortos con brillo con el nuevo umbral

Fecha: 15 de octubre de 2026. Se revisaron las 48 prendas que estaban en Cortos con brillo al comenzar este encargo, incluyendo originales y vistas adicionales de los casos fronterizos. La referencia es XL-054: el usuario indicó expresamente que sus bandas plateadas constituyen poco brillo y que corresponde a Cortos.

La regla aplicada distingue brillo dominante en superficies extensas de adorno concentrado sobre base lisa. No exige que cada manga y cada panel sean brillantes: una falda completa de lentejuelas es un bloque importante, distinto de unas pocas cintas decorativas. La longitud maxi se conserva aunque haya abertura alta. XL-154 queda como excepción comercial individual indicada por el usuario, sin extenderla a otros vestidos largos.

## Decisiones recomendadas

- **Cortos: XL-054, XL-082, XL-114, XL-118 y XL-172.** El brillo está concentrado en bandas, corpiño, capa de hombros o mangas; domina la tela lisa.
- **Gala: XL-089, XL-101, XL-103, XL-137, XL-140, XL-160, XL-161 y XL-164.** Tienen falda maxi continua hasta suelo. La abertura alta no define una minifalda independiente. En 140/161 el revisor de Gala puede precisar la extensión del brillo frente a Largos, pero no pertenecen a Cortos con brillo por longitud.
- **Conservar Brillo: XL-123.** El original muestra lentejuelas tanto en el corpiño plateado como en la falda y caída negra. No es un ejemplo de torso brillante sobre falda lisa.
- **Conservar Brillo: XL-153 y XL-167.** Falda completa de lentejuelas y torso liso; bloque brillante extenso, distinto del umbral XL-054.
- **Conservar Brillo con reserva: XL-127.** El único original 720×960 muestra patrón animal print. No permite confirmar lentejuelas frente a estampado. Se conserva categoría previa y no se altera por una suposición material.
- **Conservar Brillo: XL-154.** Excepción individual ya confirmada por el usuario.

Las demás prendas mantienen Brillo por lentejuelas, pedrería o textura brillante densa y extendida. No encuentro otros traslados claros en las 48 revisadas.

Si se aplican los 8 traslados a Gala y los 5 a Cortos, quedan **35 Brillo**, incluidos 127 provisional y 154 como excepción individual. La cifra deriva de estas decisiones y no responde a una cuota de 43 ni de 31.

## Comparación de los cinco Cortos respecto a XL-054

| ID | Evidencia decisiva |
|---|---|
| 54 | Base negra/azul lisa; unas cintas anchas de strass. La espalda es lisa. Referencia explícita del usuario. |
| 82 | Cuello y filas laterales del corpiño decorados; falda y mangas completamente lisas. Menos superficie brillante que 54. |
| 114 | La capa de hombros brilla; cuerpo y falda son negros lisos con perlas pequeñas separadas. Espalda lisa bajo la capa. Longitud midi a pantorrilla baja. |
| 118 | Lentejuelas limitadas al panel del corpiño; falda entera y banda del hombro lisas. |
| 172 | Flores plateadas en mangas y un panel del escote; falda y mayor parte del torso negros lisos. Aunque el hilo brillara, no domina el conjunto. |

## Casos conservados que superan el umbral

XL-040 tiene casi todo cuerpo/falda de lentejuelas y solo una banda lisa en escote. XL-049 tiene abdomen satinado, pero copas, manga asimétrica y falda de lentejuelas densas. XL-156 y XL-171 tienen pedrería repetida por corpiño y numerosas filas en toda falda. XL-078 y XL-155 tienen un dibujo de strass muy denso repetido por toda la superficie. Son más extensos y continuos que las bandas aisladas de XL-054.

XL-114 es midi largo, sin falda mini debajo de cola. Se propone Cortos siguiendo la familia comercial que incluye midi. Su nombre con «largo» no basta para decidir.

XL-110 no formaba parte de los 48 actuales. Conserva Gala: sobrecapa larga transparente sobre forro más corto, caso de transparencia separado.

## Matriz completa y estado de aplicación

Este agente **no editó products.js ni manifiestos compartidos**. La columna de estado distingue lo que ya coincidía en el archivo al generar el reporte de lo que se recomienda al agente principal. Los precios y galerías de referencia están completos en el JSON.

| ID | Largo | Brillo/material | Categoría propuesta | Estado en fuente al generar reporte | Motivo |
|---|---|---|---|---|---|
'''
for r in rows:
    md += f"| XL-{r['id']:03} | {r['observed_length']} | {r['observed_shine']} | {r['recommended_category']} | {r['category_in_source_at_report']} — {r['application_state']} | {r['decision_basis']} |\n"
md += '''
## Archivos de evidencia

- `brillo-48-revision-1.jpg` a `brillo-48-revision-4.jpg`: las 48 prendas con destinos propuestos visibles.
- `comparacion-umbral-1.jpg` y siguientes: XL-054 frente a adornos concentrados, bloques extensos y dudas de material; incluyen vistas adicionales disponibles.
- `productos-al-generar-reporte.json`: snapshot de las 139 prendas y 225 fotos al generar este reporte.
- `reporte-brillo.json`: decisiones estructuradas con ID, precio, galería, motivo, categoría propuesta y estado guardado.

Los reportes anteriores quedan como registro histórico. Estas recomendaciones sustituyen su umbral de brillo y la interpretación de aberturas altas.
'''
(OUT/'REPORTE-BRILLO.md').write_text(md,encoding='utf-8')
print(json.dumps({'reviewed':48,'recommended_brillo':35,'to_gala':gala,'to_cortos':cortos,'source_brillo_now':sum(p['category']=='Cortos con brillo' for p in products),'products':len(products),'photos':sum(len(p['photos']) for p in products)},ensure_ascii=True))
