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
- `images/dress-01.jpg` a `images/dress-17.jpg` son recortes de las fotografías mostradas en las fichas de WhatsApp Business. Algunos recortes conservan la marca de agua y los controles de galería visibles en WhatsApp.
- `images/catalog-18.jpg` a `images/catalog-58.jpg` son miniaturas extraídas de las capturas del catálogo compartidas por el usuario. Se añadieron reconstrucciones nuevas generadas con IA (`catalog-18-ai.png` a `catalog-58-ai.png`) y la galería las usa automáticamente. Son recreaciones visuales basadas en miniaturas: el color, corte exacto, stock y precio deben confirmarse con la boutique. Algunas referencias se presentan sobre maniquí invisible para evitar deformaciones y mantener el vestido completo.
- La ficha titulada **“Vestido largo de gala de lentejuelas rojo brillantes”** mostraba una fotografía de un vestido oscuro multicolor. Se conservó la asociación tal como apareció y se advierte en la ficha.
- Las tallas solo se indican cuando el catálogo las mostraba. Precio, talla, disponibilidad y entrega requieren confirmación con la boutique.
- Esta página prepara consultas a `+51 930 527 248` por WhatsApp; no envía mensajes ni procesa pagos.
- `images/xiliana-video.mp4` es el video proporcionado por la boutique. Es la primera sección y ocupa todo el ancho en formato horizontal; comienza sin sonido al terminar la presentación.
- `images/xiliana-logo-original.jpg` conserva el archivo original. `images/xiliana-logo-white.png` adapta ese mismo logo a fondo blanco para la cabecera y la presentación.
- La presentación muestra puntos, logo y el lema «Solo una vida para lucirte» durante 3,8 segundos, seguida de una salida de 0,6 segundos. Puede omitirse; con movimiento reducido, usa fundidos de opacidad y conserva el lema visible.
- La sección «Visítanos» contiene la dirección de la tienda, el teléfono, el correo y el mapa facilitados por la boutique.

La página está separada de las otras demos del repositorio.

## Publicar en Cloudflare Workers

El repositorio XILIANA incluye `wrangler.jsonc`. Usa el comando de despliegue `npx wrangler deploy` desde la raíz de este repositorio. Wrangler ejecuta `node build.cjs` y publica solamente `public/`, que contiene HTML, CSS, JavaScript y archivos multimedia. El historial `.git`, el servidor local y los registros de generación no se copian.

Para preparar y validar la carpeta sin publicar: `node build.cjs`. Todos los archivos se comprueban contra el límite de 25 MiB por archivo. No es necesario configurar un comando de compilación adicional en Cloudflare.

## SEO y dominio público

Dominio principal: **https://xilianaboutique.comunidadfortaleza.com/**. Se configura en `site-config.json`. Si cambia, vuelve a ejecutar `node build.cjs` y publica de nuevo.

La compilación genera 65 páginas estáticas: inicio, seis colecciones y 58 fichas de vestidos. Cada página incluye título, descripción, canonical, Open Graph y Twitter Card. El contenido y los enlaces de productos están en el HTML inicial; el catálogo conserva los filtros y la vista rápida con JavaScript.

Se generan `public/sitemap.xml` (incluye imágenes), `public/robots.txt`, datos estructurados de ClothingStore, WebSite, Product, Offer y BreadcrumbList, una página 404 y cabeceras de caché para Cloudflare. No se inventan reseñas, calificaciones, horarios ni disponibilidad de stock. Las variantes con forro opaco y las recreaciones IA se señalan en las fichas.

Validación local: `node validate-seo.cjs` después de compilar.

Después de publicar:

1. Comprueba que el dominio responde por HTTPS y sirve esta versión de la web.
2. Añade el dominio a Google Search Console y completa la verificación de propiedad mediante DNS o el método que el propietario prefiera. El registro de verificación lo proporciona Google; no hay uno genérico que pueda añadirse antes.
3. Envía `https://xilianaboutique.comunidadfortaleza.com/sitemap.xml` en Search Console y solicita la inspección de la página principal.
4. Verifica los datos estructurados con la prueba de resultados enriquecidos de Google. La disponibilidad de resultados enriquecidos depende de Google.
5. Vincula este dominio desde el Perfil de Empresa de Google y las redes oficiales de la boutique. Mantén nombre, dirección y teléfono iguales.
6. El propietario debe confirmar precios, detalles de las prendas, stock, horarios y condiciones de entrega; cuando estén disponibles se puede ampliar el marcado y la información visible.

La preparación técnica facilita el rastreo y la indexación; no garantiza una posición específica ni que todas las páginas se indexen.
