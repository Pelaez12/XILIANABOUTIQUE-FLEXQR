from pathlib import Path
import json
r=Path(__file__).resolve().parent
p=r/'confirmaciones-usuario.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
rows=[
('Vestido Largo Color Pic Blue',579,[16]),
('Vestido largo azul corte sirena con tirantes cruzados',499,[39,40,42]),
('Vestido largo de gala dorado',549,[124,130]),
('Vestido de gala gamusa color guinda con perlas',589,[76,77]),
('Vestido elegante sirena color verde',389,[74,75]),
('Vestido largo de gala lentejuelas negro con mangas',729,[82,87,98,104]),
('Vestido fucsia con escote y pliegue izquierdo',549,[72,78]),
('Vestido largo de gala asimétrico de una manga dorado con negro',579,[90,91]),
('Vestido corte acampanado de tejido brillante',589,[68,73]),
('Vestido sirena color verde gamuzado con mangas y cuello cuadrado',519,[79,83]),
('Vestido sirena de lentejuelas verdes con detalles en los hombros',549,[86,92]),
('Vestido largo de mangas semi drapeado con detalles de brillos en…',549,[84,85]),
('Vestido asimétrico dorado largo de gala',649,[100,101]),
('Vestido rojo de gala con strass plateadas',389,[64,102,103]),
('Vestido de gala rojo con aplicaciones plateadas',349,[62]),
('Vestido largo con semi cola y detalles de pedrería plateados y mora…',699,[106]),
('Vestido sirena de gala verde con perlas',729,[105]),
('Vestido de gala de lentejuelas color Brown',589,[23,24]),
('Vestido de gala de lentejuelas rosa',469,[17,21]),
('Vestido de gala negro con detalles plateados',429,[134,136]),
('Vestido de gala de lentejuelas · modelo plomo',529,[112,116]),
('Vestido de gala de lentejuelas · modelo estampado',449,[138,139]),
('Vestido de gala crema con azul',569,[137,141]),
('Vestido largo de gala blanco con rayas moradas y morado y de cap…',579,[110,111]),
('Vestido largo crema de perlas y pedrería plateadas',669,[118,119]),
('Vestido largo de gala dorado con rayas doradas y blanco',539,[117,120])]
for name,price,indices in rows:
 if any(set(x['indices'])&set(indices) for x in d):raise ValueError(name)
 d.append(dict(codigo='GALA-CAPTURA-R'+str(indices[0]),nombre=name,precio=price,categoria='Gala',indices=indices,fecha='2026-10-06',fuente='Coincidencia visual con capturas completas de Gala Dresses. Nombres con puntos suspensivos conservan el texto visible.'))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
missing=[('Vestido de largo gala nude con aplicaciones',649),('Vestido largo de gala de lentejuelas rojo brillantes',649),('Vestido sirena largo color rojo con Bruselas',449),('Vestido largo de mangas largas con hebilla',389),('Vestido largo de gala verde agua de lentejuelas',649),('Vestido largo de gala morado con lentejuelas',649),('Vestido largo de gala rojo de malla con lentejuelas',719),('Vestido largo de gala blanco con un hombro de lentejuelas',649),('Vestido vino strapless de tirantes con copas de pedrería',549),('Vestido largo palo rosa',699),('Vestido largo azul acero',699),('Vestido palo rosa gasa y satín',649),('Vestido sirena palo rosa de lentejuelas',569),('Vestido largo azul',349),('Vestido crema de encaje y tul asimétrico',194.5),('Vestido largo de gala color azul de lentejuelas',569),('Vestido de gala color verde asimétrico con una rosa',649),('Vestido negro brillante',389),('Vestido de gala largo negro con detalles en cuello y mangas',449),('Vestido sirena rosado de lentejuelas con detalles en los hombros',579),('Vestido sirena color rojo estraple de perlas',549),('Vestido estilo novia blanco con pedrería plateadas y verde esmeral…',849),('Vestido de gala de lentejuelas color gold',549),('Vestido largo plomo de tull con detalles de flores',439)]
(r/'gala-sin-foto-confirmada.json').write_text(json.dumps([dict(nombre=n,precio=p,categoria='Gala',estado='Sin foto original identificada') for n,p in missing],ensure_ascii=False,indent=2),encoding='utf-8')
print('26 modelos nuevos de gala, 24 fichas de gala sin foto confirmada')
