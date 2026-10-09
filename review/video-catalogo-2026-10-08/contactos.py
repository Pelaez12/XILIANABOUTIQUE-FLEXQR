from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).parent
frames=sorted((r/'frames').glob('*.jpg'))
for batch in range(0,len(frames),12):
 selected=frames[batch:batch+12:2]
 canvas=Image.new('RGB',(1148,924*3),'white'); d=ImageDraw.Draw(canvas)
 for i,p in enumerate(selected):
  x=(i%2)*574;y=(i//2)*924
  d.text((x+10,y+6),f'{p.stem} · segundo {int(p.stem[1:])-1}',fill='black')
  canvas.paste(Image.open(p),(x,y+30))
 canvas.save(r/f'contacto-{batch//12+1:02}.jpg')
print(len(frames),'fotogramas')
