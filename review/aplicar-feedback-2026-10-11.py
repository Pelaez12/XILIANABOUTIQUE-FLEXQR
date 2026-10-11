from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'main.js';t=p.read_text(encoding='utf-8');start=t.index('const opening =');end=t.index('*/',start)+2
t=t[:start]+"document.querySelector('#opening')?.remove();\ndocument.body.classList.remove('opening-active');\nstartVideo();\n"+t[end:];p.write_text(t,encoding='utf-8')
p=r/'index.html';t=p.read_text(encoding='utf-8')
start=t.index('    <div class="opening"');end=t.index('    <div class="announcement"',start);t=t[:start]+t[end:]
t=t.replace('<a href="#visitanos">Visítanos</a>','<a href="#asesoria">Asesoría</a><a href="#visitanos">Visítanos</a>')
start=t.index('      <section class="contact-strip">');end=t.index('      <section class="visit"',start)
t=t[:start]+'''      <section class="contact-strip" id="asesoria"><div><p class="eyebrow">Asesoría para tu ocasión</p><h2>Tu próximo look empieza contigo.</h2><p>¿Todavía no sabes qué vestido elegir? Cuéntanos tu ocasión, consulta por diseños personalizados o coordina una cita. Te ayudamos a conocer tus medidas.</p></div><button type="button" class="button button-light" data-advice>Quiero asesoría ↗</button></section>
'''+t[end:];p.write_text(t,encoding='utf-8')
p=r/'seo-build.cjs';t=p.read_text(encoding='utf-8');t=t.replace('<a href="/#visitanos">Visítanos</a>','<a href="/#asesoria">Asesoría</a><a href="/#visitanos">Visítanos</a>')
t=t.replace('Solicitar pedido ↗','Consultar disponibilidad ↗')
t=t.replace('<p>Prenda única y personalizada, sin talla definida por ahora. Medidas y ajustes se coordinan con la boutique. Precio de referencia del catálogo; confirma disponibilidad y entrega antes de comprar.</p>','<div class="product-availability"><p><strong>Disponibilidad:</strong> consulta si este modelo está en tienda.</p><p><strong>Medidas y ajustes:</strong> te asesoramos antes de comprar. Confirma con la boutique las medidas disponibles y si admite ajustes.</p><p>Envíos a Lima y provincia. Entrega y costo se confirman por WhatsApp.</p></div>')
p.write_text(t,encoding='utf-8')
print('Inicio directo, acceso a asesoría y fichas con consulta breve preparados.')
