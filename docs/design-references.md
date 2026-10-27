# Referencias de diseño

Guardadas el 15 de octubre de 2026 a petición del equipo. Este documento conserva los enlaces y su propósito; no instala paquetes ni copia los skills externos al proyecto.

## Recursos

- [Taste Skill](https://www.tasteskill.dev/): referencia para dirección visual, tipografía, espaciado, composición y movimiento.
- [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines): referencia de interacción, accesibilidad, adaptación a pantallas y rendimiento. Las preferencias de marca de Vercel no sustituyen la identidad de UP.
- [awesome-design-md](https://github.com/voltagent/awesome-design-md): colección de referencias de sistemas de diseño. Consultar ejemplos concretos cuando aporten al sitio; conservar la identidad aprobada del centro.
- [image-to-code-skill](https://github.com/Leonxlnx/taste-skill/tree/main/skills/image-to-code-skill): recurso para trabajar a partir de referencias visuales. Cualquier uso debe respetar las restricciones de imágenes del proyecto y las decisiones del equipo.

## Aplicación en este proyecto

Conservar el HTML y CSS compartido como fuente de presentación, las imágenes locales y la dirección visual aprobada. Consultar el contenido vigente de cada recurso antes de aplicarlo. No ejecutar instaladores ni introducir frameworks o dependencias solo porque una referencia los recomiende.

Los cambios acordados y las dudas pendientes de la revisión están en [editorial-review-2026-10-15.md](editorial-review-2026-10-15.md).


## Regla de composición confirmada — 19 de octubre de 2026

Por defecto, las imágenes junto a un bloque editorial deben aproximarse a la altura de ese texto en escritorio, salvo indicación distinta del usuario. Las fotografías pueden llenar su marco sin deformarse. Primeras páginas de documentos y gráficos informativos se muestran completos. En móvil los bloques se apilan y las imágenes conservan su proporción. Se mantienen las excepciones aprobadas: galería cuadrada y retratos de People/Team uniformes.

El subrayado distingue enlaces del contenido (títulos, referencias, nombres enlazados y créditos). No se aplica a menús, idiomas, breadcrumbs, navegación secundaria o controles con apariencia de botón; conservan sus estados de foco y selección. Por petición expresa posterior, la marca del Centro sí se subraya, tanto en encabezado como en footer.

Orden de navegación principal y móvil confirmado: Research → People → Seminars → Publications (y sus traducciones).

Para imágenes de proyectos, «altura del texto» significa solo la descripción: excluir título, investigadores y notas de presentación. La imagen comienza junto al párrafo descriptivo y termina a su altura; el crédito queda debajo. Este detalle sustituye la interpretación anterior del bloque completo. Las tres líneas de marca deben tener subrayado propio, incluido el texto dentro de la primera línea flex.

La alineación con la descripción también se aplica a la vista previa de publicaciones en las áreas de Research: título encima, autores/revista/enlaces debajo; el archivo compacto conserva su composición de referencia.

## Tipografía institucional — 26 de octubre de 2026

- [Marca institucional UP](https://www.up.edu.mx/marca-institucional/marca/): muestras oficiales de Panamericana y Seravek, consultadas el 26 de octubre de 2026.
- [Preguntas frecuentes de la marca](https://www.up.edu.mx/marca-institucional/faqs/): identifica Panamericana como fuente institucional primaria para encabezados y descriptivos.
- Aplicación al sitio: Panamericana en títulos de contenido; Seravek en lectura, identificación sencilla del centro en navegación e interfaz. Archivos locales originales y variantes en `design/assets/fonts/`; procedencia, autorización de uso web confirmada por el usuario e inventario en `docs/institutional-font-assets-2026-10-26.json`.

Esta decisión sustituye las referencias anteriores a Manrope/Ubuntu; conserva composición, contenido e imágenes aprobados.

### Revisión de arquitectura e interfaz

El [manual completo enlazado desde la guía de UP](https://www.dropbox.com/scl/fi/93odkq4ud55rmgt7b14zk/UP_Manual-de-marca.pdf?rlkey=qi09kpm6xlavsr7l63adyrs8a&dl=0) se revisó el 26 de octubre de 2026: tipografía (págs. 30–31), marca y usos incorrectos (60–75), y ejemplos del sistema visual. El PDF usa la denominación antigua Laurentian; la web actual y las fuentes aportadas usan Panamericana. No contiene una ficha de componentes web/botones. Para web, las [instrucciones actuales](https://www.up.edu.mx/instrucciones-de-instalacion/) recomiendan WOFF/WOFF2. Decisiones concretas y límites en `brand-interface-review-2026-10-26.md`.

### Referencia aportada para el logo del centro

El usuario pidió expresamente retirar el Roble y crear una propuesta propia tomando como referencia los nombres apilados de las submarcas. [Referencia interna](sources/2026-10-26-subbrand-style-reference.png) y [decisión vigente](center-logo-proposal-2026-10-26.md). No reutilizar el Roble en esta propuesta local.
