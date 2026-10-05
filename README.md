# Xiliana Boutique · vestidos

Vista local de la colección de vestidos de Xiliana Boutique. Contiene 58 fichas con sus imágenes, precios y descuentos observados en el catálogo de WhatsApp y en las capturas compartidas el 2 de octubre de 2026. El material facilitado es parcial. La portada organiza los vestidos en seis categorías fotográficas. No incluye accesorios ni blusas.

## Abrir

Desde esta carpeta:

```powershell
node build.cjs
node server.cjs
```

Luego abre `http://127.0.0.1:8090/`.

## Datos y fotos

- `products.js` contiene los nombres, categorías, precios y notas. Es el lugar para actualizar el catálogo.
- Las capturas recortadas dress-XX.jpg y catalog-XX.jpg se eliminaron por solicitud del usuario.
- `images/imagenes-reales/` conserva intactos los 166 archivos recibidos el 5 de octubre (156 archivos únicos). Se identificaron 20 productos del catálogo: sus fotos originales se copian sin modificar a `images/productos-reales/XL-XXX/`. `products.js` incluye las galerías, portada y dimensiones. Los otros 38 productos quedan pendientes de foto real; las capturas recortadas se eliminaron. Las 69 fotografías de prendas generadas con IA fueron eliminadas después de clasificar; el logo y el video se conservan.
- `pendientes-dueno/` contiene 80 grupos de fotos por confirmar, con nombres y categorías provisionales. Incluye algunas prendas fuera de vestidos y vistas posteriores sin correspondencia segura. Abre `VER-FOTOS-PENDIENTES.html` para revisarlos y completa `PRECIOS-POR-CONFIRMAR.csv`. No se incluyen en la publicación. `review/real-classification.json` registra cada fuente y su grupo; `review/CLASIFICACION-REAL.md` resume los productos y las fotos que faltan.
- La ficha titulada **“Vestido largo de gala de lentejuelas rojo brillantes”** mostraba una fotografía de un vestido oscuro multicolor. Se conservó la asociación tal como apareció y se advierte en la ficha.
- Las prendas se presentan como únicas y personalizadas, sin talla definida por ahora. Medidas, ajustes, precio, disponibilidad y entrega se coordinan con la boutique.
- Esta página prepara consultas a `+51 930 527 248` por WhatsApp; no envía mensajes ni procesa pagos.
- `images/xiliana-video.mp4` es el video proporcionado por la boutique. Es la primera sección y ocupa todo el ancho en formato horizontal. Intenta comenzar con sonido al terminar la presentación; si el navegador bloquea el audio automático, comienza silenciado y permite activarlo con el mismo botón de audio.
- `images/xiliana-logo-original.jpg` conserva el archivo original. La cabecera y la presentación usan `images/xiliana-logo-gold-black.png`: nombre dorado y firma negra sobre fondo blanco.
- La presentación muestra puntos, logo y el lema «Solo una vida para lucirte» durante 3,8 segundos, seguida de una salida de 0,6 segundos. Puede omitirse; con movimiento reducido, usa fundidos de opacidad y conserva el lema visible.
- La sección «Visítanos» contiene la dirección de la tienda, el teléfono, el correo y el mapa facilitados por la boutique.

La página está separada de las otras demos del repositorio.

## Publicar en Cloudflare Workers

El repositorio XILIANA incluye `wrangler.jsonc`. Usa el comando de despliegue `npx --yes wrangler@4.147.0 deploy` desde la raíz de este repositorio. Wrangler ejecuta `node build.cjs` y publica solamente `public/`, que contiene HTML, CSS, JavaScript y archivos multimedia. El historial `.git`, el servidor local y los registros de generación no se copian. La salida se regenera para eliminar archivos obsoletos y se valida automáticamente; un fallo detiene el despliegue.

Para preparar y validar la carpeta sin publicar: `node build.cjs`. Todos los archivos se comprueban contra el límite de 25 MiB por archivo. Para simular el despliegue: `npx --yes wrangler@4.147.0 deploy --dry-run`.

Configuración del proyecto en Cloudflare Workers Builds:

- Directorio raíz: raíz del repositorio XILIANABOUTIQUE-FLEXQR (vacío o `/`). Si se conecta otro repositorio que contiene esta carpeta, usar `XILIANA`.
- Comando de compilación: dejar vacío; Wrangler ya ejecuta y valida la compilación.
- Comando de despliegue: `npx --yes wrangler@4.147.0 deploy`.
- Carpeta de archivos estáticos: `public`, definida en `wrangler.jsonc`. No usar `.`.
- En Dominios y rutas del Worker, conectar `xilianaboutique.comunidadfortaleza.com`. El dominio debe estar disponible en la cuenta Cloudflare del propietario.

Subir al repositorio los archivos modificados y las nuevas imágenes antes de iniciar el despliegue por Git; `public/` se genera en Cloudflare y se excluye de Git. Esta revisión no ha publicado ni enviado los cambios a GitHub.

## SEO y dominio público

Dominio principal: **https://xilianaboutique.comunidadfortaleza.com/**. Se configura en `site-config.json`. Si cambia, vuelve a ejecutar `node build.cjs` y publica de nuevo.

La compilación genera 65 páginas estáticas: inicio, seis colecciones y 58 fichas de vestidos. Cada página incluye título, descripción, canonical, Open Graph y Twitter Card. El contenido y los enlaces de productos están en el HTML inicial; el catálogo conserva los filtros y la vista rápida con JavaScript.

Se generan `public/sitemap.xml` (incluye todas las fotos de las galerías), `public/robots.txt`, datos estructurados de ClothingStore, WebSite, Product, Offer y BreadcrumbList, una página 404 y cabeceras de caché para Cloudflare. No se inventan reseñas, calificaciones ni disponibilidad de stock. Las fotos actuales son originales; no se publican recreaciones de prendas con IA.

Validación local: `node validate-seo.cjs` después de compilar.

Después de publicar:

1. Comprueba que el dominio responde por HTTPS y sirve esta versión de la web.
2. Añade el dominio a Google Search Console y completa la verificación de propiedad mediante DNS o el método que el propietario prefiera. El registro de verificación lo proporciona Google; no hay uno genérico que pueda añadirse antes.
3. Envía `https://xilianaboutique.comunidadfortaleza.com/sitemap.xml` en Search Console y solicita la inspección de la página principal.
4. Verifica los datos estructurados con la prueba de resultados enriquecidos de Google. La disponibilidad de resultados enriquecidos depende de Google.
5. Vincula este dominio desde el Perfil de Empresa de Google y las redes oficiales de la boutique. Mantén nombre, dirección y teléfono iguales.
6. El propietario debe confirmar precios, detalles de las prendas, stock, horarios y condiciones de entrega; cuando estén disponibles se puede ampliar el marcado y la información visible.

La preparación técnica facilita el rastreo y la indexación; no garantiza una posición específica ni que todas las páginas se indexen.

## Retirada de capturas recortadas

Se eliminaron las 58 capturas dress-XX.jpg y catalog-XX.jpg por solicitud del usuario. Se muestran 20 productos con fotos reales en el catálogo. Las 38 fichas restantes conservan sus datos y URL con aviso de foto pendiente, sin capturas ni imágenes de IA. Sus datos están en pendientes-dueno/PRODUCTOS-SIN-FOTO-REAL.json. Los originales nuevos y el logo se conservan.

