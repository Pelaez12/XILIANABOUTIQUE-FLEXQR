# Xiliana Boutique

Sitio web de Xiliana Boutique. Requiere Node.js 22 o posterior para construir y validar las paginas estaticas.

## Construir y revisar

    node build.cjs
    node server.cjs

La vista local se abre en http://127.0.0.1:8090/. La construccion comprueba identidades, fotos, enlaces, fichas y sitemap antes de finalizar.

## Archivos necesarios

- `products.js`: catalogo de prendas publicado y galerias activas.
- `data/accessories.json`: nombres, precios, codigos y fotos de accesorios.
- `data/catalog-identities.json`: reglas de integridad para evitar reintroducir identidades consolidadas.
- HTML, CSS y JavaScript de la interfaz, mas los recursos activos de `images/`.
- `build.cjs`, `seo-build.cjs`, validadores y `wrangler.jsonc`: construccion y despliegue.
- `ordenar/`: herramienta del propietario, excluida de los buscadores.

`public/` es una salida regenerable y no se sube a Git. Los informes, capturas de auditoria, pruebas locales, originales retirados y archivos temporales quedan fuera del repositorio. No son dependencias de construccion.

## Publicar

Cloudflare Workers Builds ejecuta `npx --yes wrangler@4.147.0 deploy` desde la raiz del repositorio. Wrangler ejecuta `node build.cjs` y publica solo `public/`.

`.gitignore` contiene una lista de archivos permitidos. Al incorporar un producto o cambiar su galeria, incluir tambien las nuevas fotos activas en esa lista. No usar `git add -f` para informes ni carpetas de trabajo.
