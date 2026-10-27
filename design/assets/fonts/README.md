# Tipografías institucionales UP

Fuentes proporcionadas por el usuario el 26 de octubre de 2026, reorganizadas desde `font/` sin modificar los archivos.

- `panamericana/`: títulos y encabezados de contenido. TTF originales; pesos 300, 400, 600 y 700, con cursivas.
- `seravek/`: texto, identificación del centro en navegación, botones y formularios. OTF originales; pesos 200, 300, 400, 600 y 700, con cursivas. El archivo llamado Medium declara peso 600 en sus metadatos.
- Manrope y Ubuntu se conservan como recursos históricos; el CSS público ya no los carga.

Se conservan los TTF/OTF originales y se generan versiones WOFF2 sin cambiar glifos ni métricas, conforme a la recomendación web de UP. Las 18 variantes WOFF2 se registran en `design/site-concept.css` con `font-display: swap`; el navegador descarga las que necesita. Las familias de respaldo mantienen legible el contenido durante la carga. No se requiere instalar fuentes ni dependencias para generar el sitio. La vista previa del CMS reutiliza el mismo CSS.

Fuentes de la guía: https://www.up.edu.mx/marca-institucional/marca/ y https://www.up.edu.mx/marca-institucional/faqs/. Panamericana es la familia institucional principal para encabezados y descriptivos; la guía también presenta Seravek. La asignación concreta de Seravek al texto, identificación de navegación y los controles es la aplicación de esa jerarquía a este sitio.

El usuario confirmó expresamente autorización institucional de uso web de Seravek el 26 de octubre de 2026. Se conserva el acuerdo de escritorio recibido con los archivos como procedencia; ese acuerdo por sí solo no concede el uso web. No se afirma que las fuentes sean de licencia abierta. No convertir, sustituir ni ampliar su distribución para otros proyectos basándose únicamente en este registro. Inventario y SHA-256: `docs/institutional-font-assets-2026-10-26.json`.
