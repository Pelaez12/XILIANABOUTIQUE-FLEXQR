from pathlib import Path
import json, re, shutil, csv

root=Path(__file__).resolve().parents[1]
manifest_file=root/'review/real-classification.json'
m=json.loads(manifest_file.read_text(encoding='utf-8'))
wrong=next((g for g in m['matched'] if g['productId']==36),None)
if wrong:
    # Conservar la foto intacta en pendientes; retirar solo la asociación equivocada.
    folder=root/'pendientes-dueno/PD-081-corto-negro-plateado-escote-halter-por-identificar'
    folder.mkdir(exist_ok=True)
    old=root/wrong['photos'][0]['src']
    dest=folder/'01-R011.jpeg'
    shutil.copyfile(old,dest)
    photo={**wrong['photos'][0],'src':'./'+dest.relative_to(root).as_posix()}
    m['matched']=[g for g in m['matched'] if g['productId']!=36]
    m['pending'].append(dict(code='PD-081',name='Corto negro y plateado de escote halter por identificar',
        category='Cortos con brillo',price=None,sourceIndices=[11],photos=[photo],
        status='No corresponde a código 174. Confirmar nombre, precio y disponibilidad.'))
    m['withoutNewPhotos'].append(dict(productId=36,name=wrong['name'],price=wrong['price'],
        reason='R011 retirada: no coincide con foto oficial del código 174. Pendiente de foto exacta.'))
    manifest_file.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    products=root/'products.js'
    s=products.read_text(encoding='utf-8')
    match=re.search(r'const realPhotos = (\{[\s\S]*?\});',s)
    mapping=json.loads(match.group(1));mapping.pop('36',None)
    s=s[:match.start(1)]+json.dumps(mapping,ensure_ascii=False,indent=2)+s[match.end(1):]
    products.write_text(s,encoding='utf-8')
    (root/'pendientes-dueno/PRODUCTOS-SIN-FOTO-REAL.json').write_text(json.dumps(m['withoutNewPhotos'],ensure_ascii=False,indent=2),encoding='utf-8')
    with (root/'pendientes-dueno/PRECIOS-POR-CONFIRMAR.csv').open('a',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,delimiter=';');writer.writerow(['PD-081','Corto negro y plateado de escote halter por identificar','Cortos con brillo','','','R011','No corresponde al código 174'])
    html=root/'pendientes-dueno/VER-FOTOS-PENDIENTES.html'
    h=html.read_text(encoding='utf-8')
    h=h.replace('</body>','<section><h2>PD-081 · Modelo por identificar</h2><p>R011: escote halter. No corresponde al vestido código 174. Precio por confirmar.</p><img src="PD-081-corto-negro-plateado-escote-halter-por-identificar/01-R011.jpeg" alt="Vestido real negro y plateado de escote halter" style="max-width:320px;height:auto"></section></body>')
    html.write_text(h,encoding='utf-8')
    # Retirar la copia publicada de la ficha errónea; original y copia pendiente existen.
    assert old.resolve().is_relative_to((root/'images/productos-reales').resolve())
    assert dest.exists() and (root/'images/imagenes-reales').exists()
    old.unlink()
    audit_file=root/'review/whatsapp-review-live.json'
    audit=json.loads(audit_file.read_text(encoding='utf-8'))
    for record in audit['reviewed']:
        if record['productId']==36:
            record['realPhotoMatch']=[]
            record['note']='R011 no coincide: escote y dibujo diferentes. Foto preservada en PD-081.'
    audit_file.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Asociación R011 retirada; original intacto y copia conservada en PD-081.')
else:
    print('La asociación ya estaba corregida.')
