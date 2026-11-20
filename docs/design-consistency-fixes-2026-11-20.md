# Correcciones de consistencia — 20 de noviembre de 2026

Estado: implementación y comprobación local completadas. El usuario autorizó
commit, push, PR, merge y publicación el 20 de noviembre de 2026. El estado del
despliegue se comprueba en GitHub Actions después del merge.

## Alcance autorizado

El usuario autorizó las siete correcciones de **Auditoría general — UP Economics
Research Center**, guardada en
`.impeccable/audit/2026-11-20T15-24-47Z__project.md`. No existía un plan separado en
el directorio de planes; se usa la lista de esa auditoría por confirmación
expresa del usuario. Los siete elementos son obligatorios; no hay tiers ni
elementos opcionales. La auditoría original permanece intacta.

## Elementos implementados

1. **Entrega de imágenes:** copias WebP de 24 imágenes grandes ya aprobadas,
   con 67 variantes locales, `srcset` y `sizes`. People y Team calculan el
   tamaño solicitado a partir del marco y `portrait_crop`; no se hornean recortes
   ni se sustituyen originales. Se preservan orientación, transparencia y perfil
   de color cuando existe. Los diagramas completos y fuentes pequeñas no se
   procesan. El logo institucional tampoco se procesa.
2. **Espaciado tipográfico:** retiradas reglas históricas de tracking negativo
   que vencían al sistema institucional. Familias y pesos aprobados intactos.
3. **Jerarquía móvil:** encabezados de grupos/áreas a 28 px y títulos principales
   de esas páginas a al menos 36 px en los anchos revisados.
4. **Filtros:** campos, selectores y acción principal comparten altura de 54 px
   y radio de 3 px; la limpieza de filtros mantiene una variante textual
   secundaria consistente en Publications y Seminars, con mínimo táctil de 44 px.
5. **Créditos:** plantilla de cuerpo propia, cabecera/ruta compartidas y sin
   marcar Research como página actual. Idiomas, atribuciones y notas conservados.
   En la revisión visual se completaron dos traducciones de interfaz existentes
   para la miniatura de video; no cambia su significado ni procedencia.
6. **Entrada editorial:** usa el CSS compartido, el color institucional actual
   en sus metadatos y deja de enlazar íconos de la propuesta anterior. Se
   conservan los archivos históricos. El login y el diseño de Decap no se
   reemplazan ni se inicia una sesión autenticada.
7. **Guías:** README y guía EN/ES distinguen aprobación y merge administrativo.
   La excepción remota autorizada previamente permite omitir la aprobación,
   no autoaprobar un PR; para no administradores sigue siendo necesaria.
   Se recomienda revisión independiente y comprobar el build en ambos casos.
   Esta implementación no cambia permisos ni reglas remotas.

## Archivos

- `design/site-concept.css`: cascada tipográfica, escala móvil y controles.
- `tools/responsive_images.py`: selección estándar de copias y fallback.
- `tools/generate_responsive_images.py`: generación local con Pillow, ya usado
  por el generador de fichas bibliográficas; ninguna dependencia nueva en CI.
- `design/assets/responsive/`: copias, manifiesto de SHA-256 y guía.
- `tools/build_site.py`, `tools/site_seo.py`: atributos responsivos.
- `templates/image-credits.html`, `tools/site_locales.py`: créditos neutrales.
- `content/settings/interface-es.json`: dos traducciones de créditos.
- `admin/index.html`, `admin/editor-guide.html`, `README.md`: identidad y flujo.

El build solo necesita la biblioteca estándar. Si no hay variantes, si faltan
archivos o si el SHA-256 del original ya no coincide, vuelve a utilizar la fuente
original. Una fotografía nueva cargada desde el CMS no exige tener Pillow ni
usar una terminal para publicarse. Un responsable puede generar sus derivados
después siguiendo las instrucciones del README.

## Verificación local

| Comprobación | Resultado |
|---|---|
| `python3 tools/generate_responsive_images.py` | Correcto; 24 fuentes, 67 copias |
| `python3 tools/build_site.py` | Correcto; 58 registros de búsqueda, 21 publicaciones, 15 personas |
| Sintaxis Python de los cinco módulos afectados | Correcta, inspección AST |
| `git diff --check` | Sin errores |
| HTML/medios de 88 páginas públicas | Sin IDs duplicados, referencias ARIA sin destino, atributos alt ausentes ni archivos src/srcset faltantes |
| Conservación de originales | SHA-256 de las 24 fuentes coincide con sus bytes en HEAD |
| Matriz renderizada | 230 combinaciones: 23 rutas × EN/ES × 1440, 1024, 768, 390 y 320 px; sin desbordamiento horizontal |
| Jerarquía a 390 px | People 36/28 px; Health 36/28 px; tracking normal en títulos, nombres y publicaciones |
| Geometría de filtros | Input/select/submit a 54 px, radio 3 px; limpieza textual equivalente |
| Créditos EN/ES | H1 de 36 px en móvil, cabecera/ruta presentes, ninguna sección principal marcada como actual |
| Publications ES | Búsqueda sin coincidencias muestra 0; limpiar devuelve 21 |
| Buscador global | Escape cierra y devuelve foco al disparador con outline de 3 px |
| Movimiento reducido | Preferencia emulada activa; ninguna animación activa en la inspección |
| Entrada del CMS | Login de Decap carga sin errores; theme-color #8D1838, sin enlaces a íconos históricos |
| Revisión visual | Inicio, People, Publications y Health móvil EN/ES; People, proyectos Health, créditos y filtros de seminarios en escritorio |

### Medición de imágenes

En People se forzó únicamente en el navegador de diagnóstico la carga de todos
los retratos para leer los `currentSrc` seleccionados. A 390 px:

| Selección | Suma de archivos de retrato distintos | Reducción |
|---|---:|---:|
| Originales | 18.748.036 bytes | — |
| Copias seleccionadas, DPR 1 | 805.811 bytes | 95,7 % |
| Copias seleccionadas, DPR 2 | 1.704.641 bytes | 90,9 % |

Son tamaños de archivos seleccionados, no tiempos de carga ni Core Web Vitals.
No se presupone que todos se descarguen al abrir: la carga diferida sigue activa.

### Detector y excepciones

Se ejecutó una vez, al terminar los cambios de UI:

```sh
/home/jadrk040507/.config/opencode/skills/impeccable/scripts/impeccable detect --json --changed
```

Devuelve código 2 por una advertencia preexistente: el borde lateral de 3 px de
`.legal-review-note`. No se añadió ni modificó y no forma parte de estas siete
correcciones. Se conserva para no rediseñar o alterar notas legales/editoriales
fuera de alcance. La advertencia no es un fallo de ejecución ni evidencia de un
nuevo problema en las partes cambiadas.

Las notas públicas «Design preview · Illustrative content» y la confirmación
del contacto siguen intactas. No se inventan aprobaciones ni se cambian hechos,
autores, fotografías, títulos bibliográficos o permisos de reutilización.

## Límites y desviaciones

- No se ejecutaron suites de tests; se usaron generación, inspección de
  sintaxis/artefactos y comprobaciones manuales en navegador.
- Los tamaños móviles/tablet y DPR son emulados en Chrome; no se verificaron
  dispositivos físicos, gestos touch ni otros motores.
- Se comprobó la pantalla de login del CMS, no su sesión autenticada ni
  operaciones de guardado/publicación.
- Revisión realizada por el mismo agente, sin un crítico independiente.
- Única ampliación menor del listado: dos traducciones de interfaz de créditos
  identificadas al mirar el resultado. No se modificó el documento de auditoría.
