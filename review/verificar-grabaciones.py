from pathlib import Path
import json, csv, re, unicodedata, shutil

root = Path(__file__).resolve().parents[1]
review = root / 'review'
incoming = json.loads((review/'catalogo-recibido-2026-10-06.json').read_text(encoding='utf-8-sig'))

def key(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in s if not unicodedata.combining(c))).strip()

# Transcripción visual de fotogramas de las cuatro grabaciones del usuario.
# No se infiere ningún precio para prendas que no aparecen en estos videos.
observations = []
def add(video, name, price, regular=None, alias=None):
    observations.append(dict(video=video, nombre=name, precio_final_pen=price,
                             precio_regular_pen=regular, alias=alias))

for name, price in [
    ('Vestido estampado floreado',629),('Vestido largo floreado de tirantes',499),
    ('Vestido rojo largo de manga abanicada',289),('Vestido largo anaranjado de mangas largas de rosas',369),
    ('Vestido blanco de corte sirena, de manga larga de rosas',349),('Vestido largo crema de mangas',319),
    ('Vestido largo amarillo corte romano',449),('Vestido largo verde limón',599),
    ('Vestido largo animal print',599),('Vestido largo Bandage color Rojo',549),
    ('Vestido largo floreado',449),('Vestido estampado multicolor',289),
    ('Vestido Animal Print Multicolor',329),('Vestido floreado multicolor',349),
    ('Vestido largo blanco con estampado flores',269),('Vestido corte A animal print',349),
    ('Blusa cola de pato asimétrico blanco con negro',239)]: add(1,name,price)

for name, price in [
    ('Vestido corto azul',329),('Vestido corto de lentejuelas verde',369),
    ('Vestido de lentejuelas corto rojo',289),('Vestido corto de una manga color marrón',389),
    ('Vestido corto de lentejuelas rosado de una manga',389),
    ('Vestido verde de lentejuelas y mostacillas',329),
    ('Vestido corto 3/4 de lentejuelas con terciopelo en el busto',399),
    ('Vestido de lentejuelas palo rosa de transparencias',389),
    ('VESTIDO CORTO Negro con tirantes y pedrería',399),
    ('Vestido corto champagne de lentejuelas con cuello alto',389),
    ('Vestido corto blanco de lentejuelas tornasoladas',349),
    ('Vestido corto de tirantes negro con pedrería de tirantes con transparencia',369),
    ('Vestido corto rojo de pedrería',329),('Vestido Corto Verde de Pedrería Plateadas y de Perlas',399),
    ('Vestido largo de lentejuelas con diamantes',349)]: add(2,name,price)
add(2,'Vestido corto color verde (S M)',114.50,229)
add(2,'Vestido corto dorado de una manga',194.50,389)
add(2,'Vestido corto negro con plateado',75.60,189)
add(2,'Vestido corto negro con mangas plateadas',119.50,239)
add(2,'Vestido (L) transparente con diamantes de imitación',164.50,329)

for name, price in [
    ('Vestido corto licrado azul',249),('Vestido lila en rib',289),
    ('Vestido blanco mini elegante con perlas',329),('Vestido corto cuello diagonal, plisado y liso',319),
    ('Vestido corto verde agua con tirantes',299),('Vestido corto celeste con corte sirena',239),
    ('Vestido blanco con perlas',319),('Vestido corto blanco con capa',239),
    ('Vestido Corto Bellmet asimétrica color verde',189),
    ('Vestido color verde terciopelo semi drapeado con manga y escote',429),
    ('Vestido corto azul con cinturón de Aplicaciones plateado',369),
    ('Vestido drapeado verde de mangas con escote',359),
    ('Vestido corto blanco drapeado con mangas largas',389),
    ('Vestido de cuello cuadrado de manga larga color rosado',299),
    ('Vestido corto plomo con detalle de lentejuelas y pliegues',319),
    ('Vestido largo verde con estampado de rosas verdes',229),
    ('Vestido drapeado azul asimétrico',389)]: add(3,name,price)
add(3,'Vestido corto con mangas y ajustado color azul con estampado floral',68.70,229)
add(3,'Vestido corto satín estampado',86.70,289)
add(3,'Vestido corto con volantes de cuello redondo',115.60,289)

for name, price in [
    ('Vestido Bandage Color Verde Con Rayas',379),
    ('VESTIDO BANDAGE Rojo corto de pedrería plateada',379),
    ('Bandage Dress de colores',399),('Bandage Dress Negro con pedrería',349),
    ('Bandage dress nude con blanco',389),
    ('Vestido Bandage corto negro con aplicaciones plateadas',389),
    ('Bralette negro con pedrería de colores',199),('Falda Bandage Dress',219),
    ('Vestido Bandage Dorado',449),('Vestido Bandage negro con aplicaciones plateadas',389),
    ('Vestido Bandage rojo',389),('Vestido Bandage negro con rosado y perlas rosadas',679),
    ('Vestido Bandage Negro/Blanco',449),('Conjunto Bandage',349),
    ('Vestido Bandage blanco y crema de perlas',549),('Vestido Bandage negro con lazo blanco',389)]: add(4,name,price)
add(4,'Vestido Bandage Blanco/Negro',144.50,289)
add(4,'Vestido Bandage Amarillo — mini',389)
add(4,'Vestido Bandage Amarillo — midi',429)
add(4,'VESTIDO BANDAGE Caqui ceñido',None)

# Video Gala Dresses: Grabación de pantalla 2026-10-05 235636.mp4.
for name, price in [
    ('Vestido de gala en degradado',749),
    ('Vestido largo azul acero',699),
    ('Vestido largo palo rosa',699),
    ('Vestido palo rosa gasa y satín',649),
    ('Vestido de gasa azul',649),
    ('Vestido largo morado claro',649),
    ('Vestido sirena palo rosa de lentejuelas',569),
    ('Vestido vino strapless de tirantes con copas de pedrería',549),
    ('Vestido largo corte sirena negro con lazo y mangas',549),
    ('Vestido largo azul',349)]: add(5,name,price)
add(5,'Vestido crema de encaje y tul asimétrico',194.50,389)
add(5,'Vestido largo de gala blanco con un hombro de lentejuelas',649)

aliases = {
    key('Vestido licra licrado azul'):key('Vestido corto licrado azul'),
    key('Vestido corto satén estampado'):key('Vestido corto satín estampado'),
    key('Vestidos Corto con mangas y ajustado color azul con estampado floral'):key('Vestido corto con mangas y ajustado color azul con estampado floral'),
    key('Vestido corto blanco de lentejuelas tornasoladas de un hombro con capa'):key('Vestido corto blanco de lentejuelas tornasoladas'),
}
lookup={key(o['nombre']):o for o in observations}
result=[]
for category, items in incoming['catalogo'].items():
    for item in items:
        record={'categoria_texto':category, **item}
        k=aliases.get(key(item['nombre']),key(item['nombre']))
        evidence=lookup.get(k)
        if k==key('Vestido Bandage Amarillo'):
            evidence=lookup.get(key('Vestido Bandage Amarillo — mini' if item['precio_final_pen']==389 else 'Vestido Bandage Amarillo — midi'))
        if evidence is None:
            record['estado']='No visible en las grabaciones recibidas; no validado'
        elif evidence['precio_final_pen'] is None:
            record['estado']='La grabación no muestra precio; confirmar con dueño'
            record['video']=evidence['video']
        else:
            record['precio_texto_pen']=item['precio_final_pen']
            record['precio_final_pen']=evidence['precio_final_pen']
            record['precio_regular_pen']=evidence['precio_regular_pen']
            record['video']=evidence['video']
            record['nombre_video']=evidence['nombre']
            record['estado']='Corregido según grabación' if (item['precio_final_pen']!=evidence['precio_final_pen'] or item['precio_regular_pen']!=evidence['precio_regular_pen']) else 'Precio confirmado en grabación'
        record['solo_vestido']=not key(item['nombre']).startswith(('blusa ','bralette ','falda ','conjunto '))
        result.append(record)

out={'fecha':'2026-10-06','criterio':'Precios leídos visualmente de videos. Colores y descripciones del texto no validados por defecto. Los dos bandage amarillos son modelos distintos.', 'registros':result, 'observaciones_video':observations}
(review/'catalogo-verificado-2026-10-06.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (review/'PRECIOS-VERIFICADOS-2026-10-06.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['categoria_texto','nombre','precio_texto_pen','precio_final_pen','precio_regular_pen','video','estado','solo_vestido']
    w=csv.DictWriter(f,fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(result)
conflicts=[r for r in result if r['estado']=='Corregido según grabación']
lines=['# Revisión de grabaciones — 6 de octubre de 2026','',
       f'{len(result)} registros recibidos; {sum("video" in r and "no muestra" not in r["estado"] for r in result)} con precio verificado; {len(conflicts)} discrepancias corregidas en el archivo de referencia.',
       '', 'Las cinco grabaciones muestran largos, cortos, brillos, bandage y Gala Dresses. Los 11 precios de Gala del texto coinciden con su grabación.',
       '', '| Prenda | Texto | Grabación | Video |','|---|---:|---:|---|']
for r in conflicts:lines.append(f'| {r["nombre"]} | S/{r["precio_texto_pen"]:.2f} | S/{r["precio_final_pen"]:.2f} | {r["video"]} |')
lines += ['', '## Clasificación', '',
    '- Blusa, bralette, falda y conjunto quedan fuera del catálogo de vestidos.',
    '- Los dos bandage amarillos son distintos: mini S/389 y midi S/429.',
    '- Bandage caqui: el precio no aparece en la grabación. No adoptar S/379 del texto.',
    '- Blanco con perlas: dos fichas con misma imagen, códigos 1914 y 1894, S/329 y S/319. Consultar con dueño.',
    '- R011 no corresponde al vestido negro con plateado código 174: cambian el escote, los hombros y el patrón. Se retira de esa ficha, conservando el original.',
    '- No se cambian precios existentes que las grabaciones ya confirman. Las prendas nuevas requieren asociar su foto exacta antes de publicarse.',
    '- No se recrean fotos ni se inventan detalles.',
    '', '## Grabaciones utilizadas', '',
    '1. Grabación de pantalla 2026-10-05 235800.mp4 — largos.',
    '2. Grabación de pantalla 2026-10-06 000256.mp4 — cortos con brillo.',
    '3. Grabación de pantalla 2026-10-06 000349.mp4 — cortos.',
    '4. Grabación de pantalla 2026-10-06 000657.mp4 — bandage.',
    '5. Grabación de pantalla 2026-10-05 235636.mp4 — Gala Dresses.',
    '', 'Fotogramas de evidencia: review/grabaciones-2026-10-06/.']
(review/'REVISION-GRABACIONES-2026-10-06.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'Registros: {len(result)}; discrepancias: {len(conflicts)}')
