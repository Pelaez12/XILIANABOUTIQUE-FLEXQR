import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
products = json.loads((OUT / 'productos-revisados-snapshot.json').read_text(encoding='utf-8'))
move_cortos = {
    54: ('Alta: instrucción directa', 'Referencia indicada por el usuario: minivestido negro de base lisa, bandas plateadas separadas en el frente y espalda completamente lisa. Las bandas no convierten toda la prenda en brillo.'),
    82: ('Alta: analogía visual clara con XL-054', 'Negro midi: líneas finas de strass en cuello y torso; mangas, cintura y falda negras lisas. El adorno ocupa menos superficie que las bandas del ejemplo XL-054.'),
    114: ('Media-alta: umbral comercial aclarado', 'Negro midi largo: cuerpo y falda lisos con perlas muy separadas; el bloque brillante está concentrado en la pieza de hombros. La superficie lisa domina el conjunto.'),
    118: ('Media-alta: umbral comercial aclarado', 'Negro corto asimétrico: lentejuelas negras discretas en el panel del corpiño; banda de escote, cintura, falda y volante lisos. No presenta brillo integral dominante.'),
    172: ('Media-alta: umbral comercial aclarado', 'Negro mini: decoración floral plateada en mangas y una media pechera; falda y buena parte del frente lisos. El adorno se concentra en zonas definidas.'),
}
floor_gala = [89, 101, 103, 137, 140, 160, 161, 164]
reasons = {
    10: 'Vestido azul a la rodilla con estampado floral; no se aprecia lentejuela ni pedrería dominante.',
    22: 'Blanco midi con rosas bordadas/estampadas en torso y mangas; falda lisa mate.',
    63: 'Vestido ocre satinado de cuello diagonal y drapeado; el lustre de tela no es una superficie de lentejuelas.',
    64: 'Celeste a la rodilla con capa corta en escote; tela lisa.',
    65: 'Verde terciopelo mini con una manga; el reflejo del terciopelo no es pedrería.',
    66: 'Verde terciopelo midi drapeado de manga larga; tela lisa sin pedrería visible.',
    67: 'Blanco drapeado de hombros descubiertos y mangas; superficie lisa.',
    69: 'Celeste mini drapeado con mangas amplias; sin adorno brillante dominante.',
    79: 'Blanco mini con una manga tipo capa; superficie lisa.',
    80: 'Negro corto drapeado con mangas transparentes; sin aplicación brillante dominante.',
    83: 'Blanco midi liso con único fleco de strass desde el nudo de cintura/abertura.',
    84: 'Amarillo satinado mini de tirantes; el lustre del satén no es lentejuela.',
    85: 'Mini marrón y blanco con dibujo ondulado impreso: ambos originales ampliados muestran estampado mate, no lentejuelas. Corrige la impresión de la lámina pequeña del informe anterior.',
    86: 'Crema midi de gasa: tres estrellas doradas centrales como adorno localizado; falda lisa.',
    121: 'Negro mini de tiras y aberturas; tela lisa.',
    122: 'Negro mini con plumas en escote; las plumas no aportan brillo de pedrería.',
    130: 'Plomo mini con caída lateral larga; lentejuelas limitadas a media copa y resto liso.',
    131: 'Azul intenso midi drapeado con escote halter; tela lisa.',
    16: 'Pedrería azul/plateada distribuida densamente por corsé y minifalda, con plumas.',
    17: 'Dorado de una manga y falda cruzada con lentejuelas extendidas por toda la prenda.',
    35: 'Cobre mini con lentejuelas repetidas por corpiño y falda.',
    38: 'Rosado mini y manga larga cubiertos de lentejuelas.',
    39: 'Verde corto con patrón de lentejuelas por torso y falda.',
    40: 'Verde midi con falda y cuerpo cubiertos de lentejuelas; la pequeña zona de terciopelo del busto no domina el conjunto.',
    49: 'Rojo mini con lentejuelas por todo el cuerpo y la falda.',
    51: 'Celeste mini con pedrería/lentejuelas densas por torso, mangas y falda.',
    52: 'Azul mini de una manga con lentejuelas por el cuerpo y la falda.',
    57: 'Blanco a la rodilla con brillo tornasolado repartido de forma densa por todo el vestido.',
    78: 'Negro mini: patrón plateado denso por cuello, torso y falda. A diferencia de XL-054, el dibujo brillante reviste la prenda completa.',
    117: 'Negro midi con malla plateada repetida por corpiño y falda; brillo integral dominante.',
    119: 'Verde lima mini: tejido/patrón brillante extendido por torso y falda.',
    120: 'Dorado/negro mini con tejido brillante uniforme por todo el vestido.',
    123: 'Corpiño blanco revestido de pedrería densa y minifalda negra cubierta de lentejuelas, incluida la caída lateral. No son unas bandas puntuales como XL-054.',
    127: 'Mini vino con caída lateral estampada o brillante; el material exacto no se confirma con la foto. Conservar categoría vigente, sin reclasificar por textura dudosa.',
    132: 'Dorado mini con lentejuelas densas por todo el vestido y borde de perlas.',
    133: 'Azul plateado a la rodilla con lentejuelas extendidas por torso, mangas y falda.',
    134: 'Negro con pedrería plateada densa por corpiño y falda; las plumas son secundarias.',
    135: 'Guinda mini: perlas/pedrería muy densas cubren torso, mangas y falda. El patrón brillante define integralmente la prenda.',
    149: 'Blanco mini con lentejuelas tornasoladas por todo el vestido.',
    150: 'Azul mini con lentejuelas y dibujo plateado densos por torso y falda, más flecos.',
    151: 'Palo rosa mini con aplicaciones/pedrería densas por corsé y falda.',
    152: 'Rojo mini con grandes aplicaciones en copas y cadenas de strass numerosas por toda la falda; pedrería protagonista.',
    153: 'Mangas y blusa blancas lisas, pero toda la minifalda es un bloque de lentejuelas doradas intenso y protagonista. No equivale a unas bandas sobre base lisa.',
    154: 'Conservar Cortos con brillo por indicación explícita del usuario sobre este modelo, registrada como excepción comercial.',
    155: 'Negro mini con patrón geométrico plateado repetido por todo el cuerpo y falda; no es adorno limitado al escote.',
    156: 'Negro transparente mini: pedrería por copas, estructura del corsé y líneas numerosas de la falda. La ornamentación se extiende por toda la prenda.',
    157: 'Negro mini con copas y corsé de pedrería densas y dibujo brillante por toda la falda.',
    166: 'Rojo a la rodilla con lentejuelas distribuidas por todo el vestido.',
    167: 'Torso y mangas negras lisas, pero toda la minifalda tiene dibujo de lentejuelas doradas que protagoniza el conjunto.',
    168: 'Champagne mini: filas de lentejuelas/pedrería por torso, mangas y falda. La base clara no convierte el patrón integral en adorno localizado.',
    169: 'Verde mini con lentejuelas/relieve brillante en dibujo de malla por torso, mangas y falda; distribución integral.',
    170: 'Verde mini con lentejuelas por toda la prenda.',
    171: 'Verde mini: copas densamente cubiertas y numerosas líneas de perlas por torso y falda; ornamentación integral.',
}

rows = []
for p in products:
    pid = p['id']
    category = p['category']
    if pid in move_cortos:
        proposed = 'Cortos'
        confidence, reason = move_cortos[pid]
    elif pid in floor_gala:
        proposed = 'Gala'
        confidence = 'Largo visual claro; restauración coordinada por agente principal'
        reason = 'La falda principal continúa hasta el suelo: abertura alta en vestido largo, sin minifalda independiente. La abertura no determina la categoría Cortos; el usuario corrigió expresamente XL-089.'
    else:
        proposed = category
        confidence = 'Conservar categoría: material dudoso' if pid == 127 else 'Alta en observación visual'
        reason = reasons.get(pid, 'Ver lámina y revisión visual individual.')
    rows.append({'id': pid, 'nombre': p['name'], 'categoria_snapshot': category, 'categoria_propuesta': proposed, 'confianza': confidence, 'motivo': reason, 'foto_principal_revisada': p['image']})

counts = {c: sum(r['categoria_propuesta'] == c for r in rows) for c in ['Cortos', 'Cortos con brillo', 'Gala']}
report = {
    'fecha': '2026-10-15',
    'criterio': 'Regla comercial aclarada por el usuario, anclada a XL-054: base lisa con bandas/aplicaciones o brillo disperso pertenece a Cortos; brillo dominante por toda la prenda o un bloque protagonista corresponde a Cortos con brillo. No se exige 100% literal de brillo ni se usa la cuota 43 como objetivo.',
    'modelos_revisados': len(rows),
    'snapshot': {'Cortos': sum(p['category'] == 'Cortos' for p in products), 'Cortos con brillo': sum(p['category'] == 'Cortos con brillo' for p in products)},
    'ids_propuestos_brillo_a_cortos': sorted(move_cortos),
    'ids_recomendados_cortos': [r['id'] for r in rows if r['categoria_propuesta'] == 'Cortos'],
    'ids_restauracion_largos_a_gala_por_agente_principal': floor_gala,
    'conteo_derivado_de_observaciones_no_objetivo': counts,
    'fronteras_y_excepciones': [
        {'id': 114, 'decision': 'Cortos', 'limite': 'Tiene una pieza superior brillante; la base negra lisa y las perlas dispersas dominan. Decisión comercial coherente con XL-054.'},
        {'id': 118, 'decision': 'Cortos', 'limite': 'Corpiño con lentejuelas negras discretas; falda lisa mayoritaria. No equivale a bloque dorado protagonista de XL-153.'},
        {'id': 172, 'decision': 'Cortos', 'limite': 'Mangas y media pechera decoradas; negro liso dominante en cuerpo y falda.'},
        {'id': 127, 'decision': 'Conservar Cortos con brillo', 'limite': 'No asegurar el tipo de material a partir de esta imagen; no cambiar por textura dudosa.'},
        {'id': 154, 'decision': 'Conservar Cortos con brillo', 'limite': 'Excepción explícita del usuario; no generalizarla a todos los vestidos largos con abertura.'},
    ],
    'extras': {'110': 'Revisada foto original: vestido blanco largo con rayas brillantes que continúan hasta el suelo y capa/tul lateral. No se ve minifalda independiente; conservar Gala.', '135': 'Ampliada foto original: ornamentación muy densa por todo el mini; conservar Cortos con brillo.', '85': 'Los dos originales ampliados confirman estampado marrón/blanco mate; Cortos vigente es correcto. Esta observación sustituye la impresión inicial del informe anterior.'},
    'conciliacion_identidades': 'Las 16 filas oficiales anteriores sin asociación segura siguen pendientes de identidad. No se reinterpretan como 16 faltantes confirmados ni se intenta completar cifras reclasificando fotos.',
    'filas': rows,
    'archivos_evidencia': [f'todos-{i}.jpg' for i in range(1, 7)],
    'sin_cambios_compartidos': True,
}
(OUT / 'reporte.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = [
    '# Revisión comercial de Cortos y Cortos con brillo', '',
    'Revisadas **66 prendas**: las 18 Cortos y 48 Cortos con brillo de la instantánea guardada en esta carpeta. Las seis láminas `todos-1.jpg` a `todos-6.jpg` cubren todas las fotos principales; se ampliaron originales y vistas adicionales de los casos comparativos.', '',
    'La referencia es **XL-054**, que el usuario indicó como Cortos aunque tenga bandas plateadas. Se distingue base lisa con adorno localizado/disperso frente a brillo que domina el vestido o un bloque protagonista. No se exige 100% literal de brillo; las mangas lisas no eliminan una minifalda completamente cubierta de lentejuelas. Las cuotas esperadas no intervienen.', '',
    '## Cambios recomendados a Cortos', '',
    '| ID | Confianza | Motivo visual |', '|---|---|---|',
]
for pid in sorted(move_cortos):
    conf, reason = move_cortos[pid]
    lines.append(f'| XL-{pid:03d} | {conf} | {reason} |')
lines += [
    '', '**XL-054 y XL-082 son los casos más claros.** XL-114, XL-118 y XL-172 quedan del lado Cortos aplicando el umbral comercial recién aclarado; sus zonas brillantes se describen expresamente para que la decisión sea revisable.', '',
    'Las 18 Cortos de la instantánea se conservan. **XL-085 es estampado mate marrón/blanco**, según ambos originales ampliados; corrige una impresión previa de la lámina pequeña. XL-083, XL-086 y XL-130 tienen adornos brillantes localizados y conservan Cortos.', '',
    '## Casos que conservan Cortos con brillo', '',
    '- **XL-123:** pedrería densa en todo el corpiño y lentejuelas por toda la minifalda y caída lateral.',
    '- **XL-135:** perlas/pedrería muy densas por torso, mangas y falda.',
    '- **XL-153 y XL-167:** toda la minifalda es un bloque de lentejuelas protagonista, aunque tengan torso o mangas lisos.',
    '- **XL-127:** conservar la categoría vigente; su material no puede asegurarse a partir de la foto. No cambiar por textura dudosa.',
    '- **XL-154:** conservar por mandato explícito del usuario como excepción comercial. No extender a todos los maxivestidos con abertura.', '',
    '## Largo real', '',
    'XL-089, XL-101, XL-103, XL-137, XL-140, XL-160, XL-161 y XL-164 tienen falda principal hasta el suelo. Su restauración a Gala está coordinada por el agente principal. Una abertura alta no demuestra una minifalda independiente. XL-089 cuenta además con corrección expresa del usuario.', '',
    'XL-110, revisado fuera de las 66 prendas, también muestra falda decorada continua hasta el suelo y capa lateral: conservar Gala.', '',
    '## Registro de las 66 prendas', '',
    '| ID | Categoría de la instantánea | Propuesta | Observación |', '|---|---|---|---|',
]
for row in rows:
    lines.append(f'| XL-{row["id"]:03d} | {row["categoria_snapshot"]} | {row["categoria_propuesta"]} | {row["motivo"]} |')
lines += [
    '', 'Los conteos derivados dentro de estas 66 prendas son **23 Cortos, 35 Cortos con brillo y 8 Gala**. Son el resultado de las decisiones individuales, no una cuota buscada. Las categorías ajenas a esta instantánea corresponden a otras revisiones.', '',
    'Las 16 filas oficiales sin asociación segura del informe anterior conservan ese estado. No se han declarado faltantes físicos ni se han asignado fotografías por color.', '',
    'No se modificaron products.js ni manifiestos compartidos.', '',
]
(OUT / 'REPORTE.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'revisados': len(rows), 'mover_a_cortos': sorted(move_cortos), 'conteo_derivado': counts}, ensure_ascii=False))
