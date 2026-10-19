import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
text = (ROOT / 'products.js').read_text(encoding='utf-8')
products = json.loads(text[text.index('['):text.index('];') + 1])
by_id = {p['id']: p for p in products}
official = json.loads((ROOT / 'review/catalogo-whatsapp-2026-10-12/cortos-completo.json').read_text(encoding='utf-8'))

# IDs are candidates supported by names and the visible garment. A missing ID
# means no safe association within the saved 139 products, not proven absence.
matches = {
    1: [10], 7: [63], 9: [64], 12: [65], 13: [66], 16: [67],
    17: [68], 18: [130], 20: [69, 131], 22: [84], 23: [85],
    24: [86], 25: [79], 27: [80], 28: [81], 30: [82], 33: [83],
}
base_ids = sorted(p['id'] for p in products if p['category'] == 'Cortos')
rows = []
for index, raw in enumerate(official, 1):
    ids = matches.get(index, [])
    name = re.split(r'Prendas Importadas|PEN|\d+% Descuento', raw)[0].strip()
    prices = [float(v) for v in re.findall(r'PEN\s*([\d.]+)', raw)]
    row = {
        'fila_oficial': index,
        'nombre_oficial': name,
        'precio_oficial': prices[0] if prices else None,
        'ids_candidatos': ids,
        'categorias_guardadas': [by_id[i]['category'] for i in ids],
        'estado': 'Sin asociación segura' if not ids else 'Candidato único por nombre y prenda' if len(ids) == 1 else 'Dos modelos distintos comparten este nombre',
    }
    if index in (6, 10):
        row['observacion'] = 'La captura oficial muestra la misma miniatura en ambas filas; nombres y precios distintos. Posible duplicado sin confirmar.'
    if index == 19:
        row['observacion'] = 'El nombre dice largo, pero no hay fotografía identificada en products.js que permita decidir su largo real.'
    if index == 20:
        row['observacion'] = 'XL-069 es celeste mini con mangas; XL-131 es azul intenso midi de escote halter. Ambos usan el mismo nombre y S/389. No fusionarlos ni contar dos veces una fila oficial.'
    if index in (17, 28):
        row['observacion'] = 'La foto guardada muestra una falda continua casi al tobillo; no hay minifalda debajo ni cola lateral separada.'
    rows.append(row)

proposals = [
    {'id': 83, 'desde': 'Cortos con brillo', 'hacia': 'Cortos', 'condicion': 'Solo si se aplica a Cortos la regla de adorno brillante localizado', 'confianza': 'Alta en descripción visual; condicionada en taxonomía', 'motivo': 'Vestido blanco midi de tela lisa; una tira/fleco de strass sale del nudo en la cintura y acompaña la abertura. No hay lentejuelas repartidas por el vestido.'},
    {'id': 86, 'desde': 'Cortos con brillo', 'hacia': 'Cortos', 'condicion': 'Solo si se aplica a Cortos la regla de adorno brillante localizado', 'confianza': 'Alta en descripción visual; condicionada en taxonomía', 'motivo': 'Vestido crema midi de gasa. Tres estrellas doradas son un adorno central; la falda es lisa. Los relieves claros del corpiño no presentan el brillo de lentejuelas.'},
    {'id': 130, 'desde': 'Cortos con brillo', 'hacia': 'Cortos', 'condicion': 'Solo si se aplica a Cortos la regla de adorno brillante localizado', 'confianza': 'Alta en descripción visual; condicionada en taxonomía', 'motivo': 'Falda principal mini por encima de rodilla con caída lateral larga independiente; tela ploma lisa y lentejuelas limitadas a una media copa del escote.'},
]
borderline = {'id': 82, 'desde': 'Cortos con brillo', 'hacia_posible': 'Cortos', 'motivo': 'Vestido negro midi liso con líneas de strass en cuello y torso hasta cintura. La decoración cubre buena parte del corpiño; es más extensa que un borde o broche. No mover automáticamente con la regla estricta de detalle localizado.'}

report = {
    'fecha': '2026-10-15',
    'alcance': 'Revisión independiente de Cortos sin brillo; 139 fotografías principales vistas, con ampliaciones y espaldas en casos de duda. Sin modificar products.js ni manifiestos compartidos.',
    'ids_cortos_guardados_confirmados': base_ids,
    'cantidad_cortos_guardados': len(base_ids),
    'ids_adicionales_condicionados_a_regla_de_adorno_localizado': [83, 86, 130],
    'ids_cortos_si_se_aplica_esa_regla': sorted(base_ids + [83, 86, 130]),
    'cantidad_si_se_aplica_esa_regla': len(base_ids) + 3,
    'caso_fronterizo': borderline,
    'cambios_propuestos_condicionales': proposals,
    'conciliacion_oficial': {
        'filas': len(rows),
        'filas_con_candidato_unico': sum(len(r['ids_candidatos']) == 1 for r in rows),
        'filas_con_dos_candidatos': sum(len(r['ids_candidatos']) == 2 for r in rows),
        'filas_sin_asociacion_segura': sum(not r['ids_candidatos'] for r in rows),
        'ids_guardados_candidatos': sorted({i for r in rows for i in r['ids_candidatos']}),
        'ids_cortos_guardados_que_no_coinciden_con_una_fila_oficial': [22, 121, 122],
        'hipotesis_31': '33 filas menos los dos modelos confirmados con falda casi al tobillo (XL-068 y XL-081) = 31 filas. No es una prueba de inventario ni un motivo para reclasificar las fotos.',
        'hipotesis_30': 'Si las filas 6 y 10 que usan la misma miniatura resultan ser una sola prenda, la hipótesis anterior bajaría a 30. No se ha confirmado el duplicado.',
        'filas_detalladas': rows,
    },
    'observaciones_visuales': [
        'XL-068: falda continua casi al tobillo, comprobada en frente y espalda; perlas pequeñas repartidas por el frente y mangas. No es un corto sin brillo.',
        'XL-081: falda recta continua hasta tobillo; aplicaciones plateadas en filas por corpiño y cadera. No es una minifalda con cola.',
        'XL-106 y XL-159: las espaldas muestran falda continua hasta tobillo; sin falda mini independiente. No los traslado a Cortos.',
        'XL-087, XL-107, XL-112, XL-136 y XL-175: diseños hasta zona baja de pantorrilla/tobillo, algunos con flecos o capas transparentes. No hay evidencia de mini debajo de cola. Además tienen brillo extendido, por lo que tampoco resuelven Cortos sin brillo.',
        'XL-022: blanco de rosas con falda midi a pantorrilla; conserva Cortos bajo el criterio existente que incluye midi. No aparece como coincidencia en la lista oficial de 33.',
        'XL-069 y XL-131: fotografías y siluetas distintas con el mismo nombre y precio; no son duplicados de imagen.',
        'XL-085: dibujo brillante extendido por vestido y mangas; conservar Cortos con brillo.',
        'XL-127: mini vino con caída lateral larga, pero el corpiño y la caída tienen brillo extendido; conservar Cortos con brillo.',
        'XL-114: falda midi larga negra con perlas repartidas y pieza superior brillante; el nombre largo no determina por sí solo la categoría, pero no corresponde a Cortos sin brillo.',
        'Los 21 Bandage se mantienen como familia identificada; la silueta ajustada o el largo mini no justifican pasarlos a Cortos.',
        'XL-125 tiene falda larga crema; conserva Liquidación según autorización previa.',
        'Nueva aclaración del usuario durante esta revisión: XL-154 debe quedar en Cortos con brillo por mostrar la pierna. Su posible extensión a otros modelos con abertura alta está pendiente; no cambia la lista de Cortos sin brillo.',
    ],
}
(OUT / 'reporte-cortos.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = [
    '# Revisión independiente de Cortos — 15 de octubre de 2026', '',
    'Se revisaron las 139 fotografías principales. Se usaron las láminas actuales de Gala/Largos, las anteriores de Cortos/Cortos con brillo/Bandage y ampliaciones de originales. Se comprobaron espaldas cuando el largo era dudoso. Las etiquetas antiguas de las láminas no se tomaron como clasificación vigente.', '',
    '## Resultado fotográfico', '',
    f'Los **14 Cortos guardados** son visualmente coherentes con el criterio existente de cortos o midi sin brillo extendido: **{", ".join(f"XL-{i:03d}" for i in base_ids)}**.', '',
    'No aparece un grupo de 17 minis sin brillo escondido en Gala o Largos. Algunas faldas llegan casi al tobillo y admiten una discusión de vocabulario entre midi largo y largo; sus fotos no muestran una minifalda independiente bajo una cola. El conteo 31 no se puede alcanzar mediante reclasificación visual fiable de los 139 modelos.', '',
    '## Aplicar la regla de adorno localizado a Cortos', '',
    'La aclaración recibida menciona Largos. Si se desea usar la misma regla en Cortos, recomiendo revisar estos tres cambios. Son propuestas condicionadas a ese criterio, no cambios ya hechos.', '',
    '| ID | Propuesta | Evidencia visual |',
    '|---|---|---|',
]
for proposal in proposals:
    lines.append(f'| XL-{proposal["id"]:03d} | Cortos con brillo → Cortos | {proposal["motivo"]} |')
lines += [
    '', 'Esto llevaría Cortos a **17** y Cortos con brillo a **40**, antes de cualquier otro cambio detectado por las otras revisiones. XL-082 es fronterizo: sus líneas de strass recorren buena parte del corpiño. Si también se tratara como detalle, Cortos quedaría en 18. No recomiendo moverlo automáticamente.', '',
    'XL-085 y XL-127 mantienen Cortos con brillo: el brillo ocupa áreas extensas del vestido. No se usa el número esperado como criterio.', '',
    '## Conciliación con las 33 filas oficiales', '',
    'Hay **16 filas con un candidato único**, **una fila con dos candidatos distintos (XL-069/XL-131)** y **16 filas sin asociación segura** dentro de products.js. Los candidatos suman 18 IDs guardados, pero no equivalen a 18 modelos oficiales confirmados. Tres Cortos guardados (XL-022, XL-121 y XL-122) no tienen coincidencia segura en esas 33 filas.', '',
    '**Pista para 30/31:** 33 filas menos XL-068 y XL-081, cuyas fotos muestran falda casi al tobillo, dejan 31. Además, las filas 6 y 10 usan la misma miniatura blanca con perlas, con nombres y precios S/329 y S/319 distintos. Si son una sola prenda, quedarían 30. Son hipótesis de conciliación; no se fusiona ninguna ficha y no se descarta el verde de rosas solo porque su nombre diga largo.', '',
    'La evidencia de la miniatura compartida está en [catalogo-cortos-primeros10.png](catalogo-cortos-primeros10.png), recorte de la captura oficial guardada.', '',
    '| Fila | Nombre oficial | Precio | ID candidato | Categoría guardada | Estado |',
    '|---|---|---:|---|---|---|',
]
for row in rows:
    ids = ', '.join(f'XL-{i:03d}' for i in row['ids_candidatos']) or '—'
    cats = ', '.join(row['categorias_guardadas']) or '—'
    lines.append(f'| {row["fila_oficial"]} | {row["nombre_oficial"]} | {row["precio_oficial"]:.2f} | {ids} | {cats} | {row["estado"]} |')
lines += ['', '## Observaciones por foto', '']
lines += [f'- {observation}' for observation in report['observaciones_visuales']]
lines += ['', '## Límites del inventario guardado', '',
          'Sin asociación segura significa que falta identificar la foto del modelo oficial entre las 139 prendas guardadas, o que no se conserva aquí su foto. No demuestra ausencia física en la boutique. No se asignaron fotos por color solamente. La diferencia entre 14 y 31 no debe describirse como 17 modelos necesariamente faltantes: las categorías y la lista oficial no tienen la misma composición.', '',
          'No se modificaron productos, precios, galerías, categorías ni manifiestos compartidos. El reporte JSON conserva el cruce de las 33 filas y los cambios condicionados.', '']
(OUT / 'REPORTE-CORTOS.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'cortos_base': len(base_ids), 'filas_oficiales': len(rows), 'unicos': report['conciliacion_oficial']['filas_con_candidato_unico'], 'ambiguas': report['conciliacion_oficial']['filas_con_dos_candidatos'], 'sin_asociacion': report['conciliacion_oficial']['filas_sin_asociacion_segura']}, ensure_ascii=False))
