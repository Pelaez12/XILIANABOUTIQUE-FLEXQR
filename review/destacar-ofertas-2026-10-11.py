from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'seo-build.cjs';t=p.read_text(encoding='utf-8')
t=t.replace('const cards = items =>',"const discount = p => p.originalPrice > p.price && p.price != null ? Math.round((1-p.price/p.originalPrice)*100) : 0;\n  const cards = items =>")
t=t.replace("p.originalPrice ? '<span class=\"sale-tag\">Oferta</span>' : ''","discount(p) ? `<span class=\"sale-tag\">−${discount(p)}%</span>` : ''")
t=t.replace('<nav aria-label="Navegación principal"><a href="/#coleccion">','<nav aria-label="Navegación principal"><a class="offers-nav" href="/colecciones/liquidacion/">Ofertas</a><a href="/#coleccion">')
t=t.replace("const items = ordered.filter(p => p.category === category);","const items = ordered.filter(p => category === 'Liquidación' ? discount(p) > 0 : p.category === category);")
t=t.replace("Liquidación:'ÚLTIMA OPORTUNIDAD'","Liquidación:'OFERTAS · LIQUIDACIÓN'")
t=t.replace("Liquidación:'Tu próximo look especial, a un precio de oportunidad. Consulta disponibilidad con la boutique.'","Liquidación:'Descubre vestidos con descuento. Compara el precio anterior con el actual y consulta disponibilidad con la boutique.'")
t=t.replace('${escape(c)}</span><small>Explorar colección',"${escape(c === 'Liquidación' ? 'Ofertas · Liquidación' : c)}</span><small>Explorar colección")
t=t.replace('${money(p.originalPrice)}</del>` : \'\'}</p><div class="product-availability">','${money(p.originalPrice)}</del>` : \'\'}${discount(p) ? `<span class="discount-label">Ahorras ${discount(p)}%</span>` : \'\'}</p><div class="product-availability">')
p.write_text(t,encoding='utf-8')
