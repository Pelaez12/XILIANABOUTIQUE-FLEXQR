from pathlib import Path
import json,csv
r=Path(__file__).resolve().parents[1]
p=r/'review/confirmaciones-usuario.json'
d=json.loads(p.read_text(encoding='utf-8-sig'))
new=[('Vestido corto Blanco de una manga',289,[160]),('Vestido corto drapeado',249,[163]),('Vestido largo marrón con detalle plateados',319,[140]),('Vestido corto con escote y detalles plateados',279,[157]),('Vestido 3/4 blanco de mangas con strass plateadas',549,[113,114]),('Vestido corto satín (Talla S)',179,[10,159]),('Vestido corto drapeado marrón con blanco',389,[13,162]),('Vestido crema de Gaza con detalles estrellas doradas',289,[161])]
for name,price,indices in new:
 if any(x['indices']==indices for x in d):continue
 d.append(dict(codigo='Captura-2026-10-06-R'+str(indices[0]),nombre=name,precio=price,categoria='Cortos sin brillo',indices=indices,fecha='2026-10-06',fuente='Coincidencia visual con capturas adjuntas del usuario'))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'review/real-classification.json'
c=json.loads(p.read_text(encoding='utf-8-sig'))
for x in c['pending']:
 if x['code'] in ['PD-001','PD-002']:
  x['category']='Cortos con brillo';x['status']='Categoría confirmada por usuario; nombre oficial y precio pendientes'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'pendientes-dueno/PRECIOS-POR-CONFIRMAR.csv'
with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.reader(f,delimiter=';'))
for x in rows:
 if x[0] in ['PD-001','PD-002']:x[2]='Cortos con brillo'
with p.open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f,delimiter=';').writerows(rows)
