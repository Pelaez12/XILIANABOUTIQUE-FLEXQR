"""Comprueba cobertura de los tres agentes y consolida la auditoría fotográfica."""
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


analysis = read('analisis.json')
assignments = [
    ('gala-largos', 'gala-largos/inventario.json'),
    ('cortos-brillos', 'cortos-brillos/inventario-fotos.json'),
    ('bandage-liquidacion', 'bandage-liquidacion/inventario.json'),
]
expected = Counter((p['id'], p['src']) for p in analysis['inventario_fotos'])
reviewed = Counter()
coverage = []
for agent, filename in assignments:
    rows = read(filename)
    reviewed.update((p['id'], p['src']) for p in rows)
    coverage.append({'agente': agent, 'productos': len({p['id'] for p in rows}), 'fotos': len(rows), 'inventario': filename})
assert reviewed == expected, {'sin_revisar': list((expected-reviewed).elements()), 'sobrantes': list((reviewed-expected).elements())}
assert analysis['errores'] == []
assert analysis['sha_incorrectos'] == []
assert len({p['id'] for p in analysis['inventario_fotos']}) == analysis['productos'] == 178
assert sum(x['fotos'] for x in coverage) == analysis['fotos'] == 297

internal = read('gala-largos/candidatos-internos-revisados.json')
internal_by_key = {(r['a']['src'], r['b']['src']): r for r in internal}
decisions = []
for p in analysis['candidatos']:
    if p['misma_ficha']:
        continue
    detail = internal_by_key.get((p['a']['src'], p['b']['src']))
    confirmed = {p['a']['id'], p['b']['id']} == {173, 214}
    decisions.append({**p, 'resultado': 'duplicado_confirmado' if confirmed else 'descartado_visualmente',
                      'evidencia_visual': detail['evidencia_visual'] if detail else 'Prendas distintas por color, escote, mangas, longitud o aplicaciones; comparación visual en las seis hojas globales y revisión de los agentes.',
                      'evidencia': detail and 'gala-largos/candidatos-internos-revisados.json' or 'candidatos-entre-fichas-01.jpg a candidatos-entre-fichas-06.jpg'})
assert len(decisions) == 61
assert sum(d['resultado'] == 'duplicado_confirmado' for d in decisions) == 1

result = {
    'fecha': '2026-10-20',
    'alcance': 'Todas las fotos de las fichas publicadas de las seis categorías; colección PENDIENTES de WhatsApp excluida.',
    'productos_revisados': analysis['productos'], 'fotos_revisadas': analysis['fotos'],
    'cobertura_agentes': coverage,
    'cobertura_exacta': reviewed == expected,
    'archivos_faltantes_o_ilegibles': 0, 'hashes_declarados_incorrectos': 0,
    'duplicados_binarios': len(analysis['grupos_archivo_identico']),
    'duplicados_pixeles_exactos': len(analysis['grupos_pixeles_identicos']),
    'duplicados_confirmados_entre_fichas': [{
        'ids': [173, 214], 'tipo': 'misma_fotografia_y_mismo_modelo',
        'nombre': 'Vestido rosado largo estampado de flores, mangas abullonadas y rosa en cintura',
        'precios_publicados': {'XL-173': 450, 'XL-214': 549},
        'evidencia': 'gala-largos/duplicado-173-214.jpg',
        'nota': 'La alta de XL-214 reprodujo un modelo ya representado por XL-173. La codificación JPEG/PNG cambia los hashes de archivo, no la identidad visual.',
    }],
    'posibles_duplicados_entre_fichas': [{
        'ids': [76, 116], 'nombre': 'Vestido Bandage Amarillo mini', 'certeza': 'media-alta',
        'evidencia': 'bandage-liquidacion/amarillos-detalle.jpg',
        'motivo': 'Copas con aro, tirantes finos, paneles de corsé y costuras parecidas; ambos S/389. Sesiones distintas. Solo XL-116 tiene código 1969 acreditado; falta una confirmación de identidad.',
    }],
    'relaciones_conjunto_componentes': [{'ids': [115, 200, 215], 'tipo': 'conjunto_y_componentes_vendidos_por_separado', 'evidencia': 'bandage-liquidacion/falda-conjunto.jpg'}],
    'repeticiones_dentro_de_galeria': [
        {'id': 77, 'fotos': [1, 2], 'tipo': 'misma_toma_con_recorte', 'evidencia': 'bandage-liquidacion/amarillos.jpg'},
        {'id': 85, 'fotos': [1, 2], 'tipo': 'misma_toma', 'evidencia': 'cortos-brillos/comparacion-XL-085.jpg'},
        {'id': 187, 'fotos': [1, 2], 'tipo': 'misma_toma_en_distinta_resolucion', 'evidencia': 'cortos-brillos/comparacion-XL-187.jpg'},
        {'id': 84, 'fotos': [1, 2], 'tipo': 'misma_vista_y_pose_con_variante_de_presentacion', 'evidencia': 'cortos-brillos/comparacion-XL-084.jpg'},
        {'id': 131, 'fotos': [1, 2], 'tipo': 'misma_vista_y_pose_con_variante_de_presentacion', 'evidencia': 'cortos-brillos/comparacion-XL-131.jpg'},
    ],
    'galerias_con_prendas_ajenas_detectadas': [],
    'candidatos_automaticos_entre_fichas_revisados': decisions,
    'catalogo_modificado': False,
}
resolution_path = OUT / 'resolucion-xl173.json'
if resolution_path.exists():
    resolution = json.loads(resolution_path.read_text(encoding='utf-8'))
    result['resolucion_posterior'] = {k: resolution[k] for k in ('id_retirado', 'id_vigente', 'fecha', 'motivo', 'precio_vigente_pen', 'total_publicados', 'largos_publicados')}
    result['resolucion_posterior']['archivo'] = 'resolucion-xl173.json'
(OUT / 'resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Cobertura exacta: 178 productos / 297 fotos; 61 pares automáticos revisados; 1 duplicado confirmado y 1 posible descubierto visualmente.')
