# Mejora técnica — 24 de octubre de 2026

Estado al cierre de la revisión local: implementación sin commit, push ni publicación. El usuario autorizó posteriormente publicar esta mejora; el despliegue se registra en GitHub Actions y en la PR de integración. Sin suites de tests, conforme a AGENTS.md y al plan. Se ejecutaron generación estática, inspección de sintaxis y rutas y revisión en navegador.

## Base y decisiones

La base es `origin/main` en `e95c46b` (PR #33), consultada con fetch. Se creó una copia aislada en `/home/jadrk040507/.codex/worktrees/a621/econ-site`. La rama confirmada de lanzamiento `795d431` tiene el mismo árbol que esa revisión publicada. Sus modificaciones sin confirmar y las del checkout original se conservaron íntegramente; no se incorporaron propuestas editoriales pendientes a esta mejora.

La 404 reutiliza el shell localizado de Research, el CSS, los scripts de navegación y el pie editorial. Su mensaje está en `templates/not-found.html`. Tiene un H1, ambos mensajes identificados con `lang`, enlaces absolutos a Inicio/Research/Publications en los dos idiomas y `noindex`. Se generan `/404.html` y `/es/404.html` fuera del sitemap. El selector recuerda EN/ES y convierte una dirección inexistente en la ruta fija del idioma elegido, evitando redirecciones repetidas sobre rutas anidadas.

`llms.txt` se deriva de las rutas canónicas realmente generadas, después de aplicar los filtros de publicación. Contiene 72 enlaces agrupados por idioma y familia: secciones públicas, nueve áreas y 21 publicaciones por idioma. Se omiten administración, rutas antiguas, registros ocultos, los cuatro documentos legales pendientes de revisión y la página auxiliar de créditos. La exclusión de las páginas legales es deliberada: siguen disponibles en la web con sus notas originales, pero no se presentan en este índice de investigación. No se añaden campos CMS, dependencias ni cambios a robots, diseño, dominio o contenido editorial.

## Comprobaciones

- `python3 tools/build_site.py`: 53 registros de búsqueda, 21 fichas de publicación y 14 personas. Los 82 destinos del sitemap existen; XML y todos los JSON-LD se analizaron correctamente. Un H1 en cada página del sitemap y en ambas 404.
- Sintaxis Python mediante `ast.parse`, JavaScript mediante `node --check design/language.js`, y espacios/conflictos mediante `git diff --check`.
- Los 72 enlaces Markdown de `llms.txt` pertenecen al sitemap y resuelven a archivos generados. La 404 no aparece en el índice ni en el sitemap. Se conservaron `User-agent: *`, `Allow: /` y el enlace al sitemap.
- Navegador Chromium local, movimiento reducido, a 1440, 390 y 320 px: página inexistente simple y anidada con HTTP 404, sin desbordamiento horizontal ni imágenes rotas; enlace de salto como primer foco y destino `main-content` al pulsar Enter. Menú móvil cierra con Escape. Selector ES/EN y preferencia española guardada llevan a la 404 correspondiente sin bucles. Las direcciones explícitas `/404.html` y `/es/404.html` son archivos existentes y responden 200; el 404 corresponde a la petición inexistente.
- El servidor de revisión local emuló únicamente la regla documentada de GitHub Pages: entregar el archivo raíz `404.html` con estado 404 para una dirección inexistente. Los enlaces y recursos absolutos del origen público se remitieron al mismo servidor local durante la revisión. No se comprobó un despliegue nuevo en GitHub Pages: el estado y la página reales del alojamiento quedan pendientes de una publicación autorizada. [Documentación de GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site).
- Capturas inspeccionadas: [móvil](404-mobile.png) y [escritorio](404-desktop.png). El contorno de foco del contenido principal en escritorio procede de la navegación con teclado.

## Datos estructurados

Se revisaron los grafos de las 82 páginas canónicas frente al [vocabulario oficial de Schema.org](https://schema.org/version/latest/schemaorg-current-https.jsonld), incluidos herencia y dominios de propiedades. Tipos usados: WebPage, WebSite, Organization, EducationalOrganization, ScholarlyArticle, Book y Person. No se encontraron tipos desconocidos ni propiedades ajenas al dominio de su tipo. Se revisaron además los rangos: autores Person, organización matriz EducationalOrganization (subtipo de Organization), publisher Organization, isPartOf referenciado a WebSite (CreativeWork), cadenas de texto/idioma, URL e identificadores y fechas ISO.

La revisión de significado contrastó títulos, autores y tipos con los registros publicados: 20 artículos académicos y un libro por idioma; las referencias al sitio y organización usan IDs coherentes. Los autores conservan su orden bibliográfico; no se atribuyen al Centro artículos de los investigadores como editor. El idioma del trabajo conserva el idioma original registrado, mientras el documento HTML identifica EN/ES. No se inventaron fechas completas ni datos de revista ausentes. La descripción localizada sigue perteneciendo a la presentación en ese idioma. `isPartOf` vincula el contenido de la ficha al sitio; no identifica el volumen o revista original. Se conserva el marcado existente: una representación bibliográfica más detallada podría separar explícitamente ficha web y obra, pero no es requisito para estas dos mejoras.

Esta es una revisión contra vocabulario y contenido, no una certificación de resultados enriquecidos ni una ejecución del validador remoto de Google. No se alteraron los metadatos de las páginas existentes.

## Textos alternativos por familia

Inspección de las 82 páginas y revisión de los textos EN/ES de áreas, proyectos, retratos y portada:

| Familia (ambos idiomas) | Imágenes | Alt vacío | Sin atributo alt | Evaluación |
| --- | ---: | ---: | ---: | --- |
| Inicio | 2 | 0 | 0 | Póster del video identificado. |
| People | 28 | 0 | 0 | Retratos identifican a la persona. |
| Research | 18 | 0 | 0 | Escenas, personas u objetos descritos en ambos idiomas. |
| Áreas | 144 | 96 | 0 | Alt vacío en retratos/miniaturas redundantes dentro de enlaces con nombre; proyectos y portadas descriptivos. |
| Publications | 42 | 42 | 0 | Miniaturas dentro de enlaces etiquetados con el título; el texto alternativo vacío evita repetirlo. |
| Fichas, Seminars, Media, créditos y páginas legales | 0 | 0 | 0 | Sin imágenes HTML en esta generación. |

No se encontraron imágenes sin atributo alt. Los vacíos revisados son deliberados y tienen texto adyacente o nombre accesible del enlace. Los textos describen el contenido disponible, sin incorporar afirmaciones nuevas sobre la investigación. No se cambió ningún alt editorial.

## Consola y rendimiento

[Observaciones del navegador](browser-observations.json): portada, Research, Development Economics, Seminars y la ficha Communicating a code of ethics en EN/ES. Diez cargas con respuesta 200 y sin errores de consola ni excepciones propias. Las peticiones inexistentes muestran el aviso de red 404 esperado; no es una excepción de JavaScript.

Medición exploratoria local de esas diez cargas, sin limitación artificial de red/CPU: DOMContentLoaded entre 19 y 60 ms, load entre 29 y 204 ms, primer contenido pintado entre 40 y 216 ms. JavaScript externo decodificado: 40,636 bytes en las vistas interiores y 41,495 bytes en portada. Las cifras son observaciones de una sesión local y pueden cambiar entre cargas. No representan latencia del alojamiento, dispositivos reales, LCP de campo ni Core Web Vitals. No justifican optimizaciones adicionales ni se han aplicado.

## Límites conservados

Las notas “Design preview”, la revisión institucional de documentos legales y las confirmaciones editoriales pendientes siguen presentes. No se cambia la política de rastreo. El índice opcional no promete posicionamiento ni derechos de reutilización. La respuesta real del alojamiento tras despliegue y la medición de campo siguen pendientes; el plan excluye publicar.

## Revisión independiente y decisiones finales

Revisión de código independiente, de solo lectura: sin hallazgos críticos ni importantes. Mejora menor corregida tras la indicación del usuario de continuar: los seis enlaces de recuperación seleccionan y guardan explícitamente el idioma que muestra su texto mediante `?lang=en` o `?lang=es`. Se revisaron los seis destinos con una preferencia opuesta guardada: todos abren y recuerdan el idioma elegido. El selector EN/ES sigue funcionando desde rutas de error anidadas. También se inspeccionó una ruta anidada sin JavaScript: HTTP 404, ambos mensajes y seis enlaces disponibles. Evidencia: [recuperación e idioma](recovery-links-observations.json).

Decisiones sobre los límites señalados por el revisor:

- Alojamiento real: se mantiene pendiente hasta una publicación autorizada; la emulación local no certifica GitHub Pages. Riesgo pendiente: una diferencia de configuración del alojamiento solo se detectaría después de desplegar.
- Rendimiento de producción: conservar las observaciones locales sin convertirlas en Core Web Vitals. Riesgo pendiente: no representan conexiones ni dispositivos de visitantes.
- Contenido editorial, permisos de imágenes y trabajo sin confirmar: conservar la base publicada y las notas existentes, dejando las dos copias previas intactas. Riesgo pendiente: las aprobaciones editoriales pendientes no se resuelven con esta mejora técnica.
- Modelado bibliográfico adicional y mejoras generales de alt: la revisión del vocabulario, rangos y textos existentes está documentada arriba; no ampliar estos cambios a una reestructuración de metadatos o imágenes. Riesgo pendiente: validar Schema.org no certifica todos los usos externos ni sustituye una auditoría completa de accesibilidad.
- Adopción de `llms.txt`: entregar el índice opcional sin prometer que los servicios externos lo usen. Riesgo pendiente: puede no influir en ningún buscador o sistema de IA.

No se ejecutaron tests por instrucción del proyecto; se sustituyeron las puertas de tests de las habilidades de proceso por la generación e inspecciones autorizadas en el plan. No se hicieron commits ni integración durante esa revisión local; la autorización posterior del usuario permite integrar y publicar la mejora.
