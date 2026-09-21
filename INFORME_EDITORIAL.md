# Informe editorial — Serie «Código Sintético» (4 volúmenes)

_Documento de trabajo del editor jefe. Registra qué se corrigió, con qué criterio, y qué queda pendiente. Su objetivo es que el lector pueda **entender, pensar, criticar y consultar** la obra, y que el autor pueda auditar cada cambio._

## 1. Alcance del encargo

Revisión editorial integral de los cuatro volúmenes (80 capítulos + Epílogo de la serie) con cuatro objetivos:
1. **Entender:** que el lector sepa de qué trata cada capítulo y en qué orden leerlo.
2. **Pensar:** que tenga preguntas y autoevaluación para discutir con el texto.
3. **Criticar:** que pueda emitir una crítica fundamentada con criterios explícitos.
4. **Consultar:** que pueda volver al libro a buscar una solución concreta sin releerlo entero.

## 2. Diagnóstico: defectos encontrados y estado

| # | Defecto | Dónde | Estado |
|---|---|---|---|
| 1 | Falta el encabezado «Lo esencial del capítulo 9»; la lista de puntos quedaba huérfana sin título | Vol. 1, cap. 9 | **Corregido** |
| 2 | Falta el encabezado «Lo esencial del capítulo 17»; la lista quedaba huérfana | Vol. 2, cap. 17 | **Corregido** |
| 3 | Encabezado «Lo Esencial del Capítulo 9» dentro del capítulo 10 (numeración cruzada errónea) | Vol. 4, cap. 10 | **Corregido** |
| 4 | Subsecciones numeradas «21.x» dentro del capítulo 9 (arrastre de una numeración anterior) | Vol. 4, cap. 9 | **Corregido** (9.1–9.10 y las dos referencias internas) |
| 5 | Ejercicio sin numerar («## Ejercicio») | Vol. 4, cap. 9 | **Corregido** → «Ejercicio resuelto 9.1» |
| 6 | Ejercicios desordenados: 4.2 aparecía antes que 4.1 | Vol. 1, cap. 4 | **Corregido** (renumerados por orden de aparición) |
| 7 | Referencia cruzada duplicada «(Vol. 3) (Vol. 3)» | Vol. 1, cap. 8 | **Corregido** |
| 8 | Referencia cruzada contradictoria «(Vol. 4) (Vol. 3)» | Vol. 1, cap. 9 | **Corregido** |
| 9 | El resumen «Lo esencial» estaba a mitad del capítulo, no al cierre | Vol. 3, cap. 2 | **Corregido** (movido al final) |
| 10 | «Epílogo» interno del Vol. 3 confundible con el «Epílogo de la serie» del Vol. 4 | Vol. 3, cap. 2 | **Corregido** → «Cierre del volumen» |
| 11 | Artefactos de plantillas dentro del índice («Objetivo», «Protocolo», «Tabla de precios»…) | Vol. 1, cap. 7 | **Corregido** |
| 12 | Artefactos en el índice («Q1 2025…», «Estado: Aceptado…», «Contexto», «Decisión»…) | Vol. 3, caps. 6 y 18 | **Corregido** |
| 13 | Artefactos en el índice («Proceso», «Stack técnico», «Comandos clave»…) | Vol. 4, caps. 5 y 9 | **Corregido** |
| 14 | «Lo esencial» sin numerar en el índice | Vol. 2, cap. 12 | **Corregido** |
| 15 | Erratas: «provenencia» (×3), «compuesición», «desacoplada el acceso», «genernar» | Vols. 2 y 4 | **Corregido** |
| 16 | Faltaba el aparato de lectura crítica, glosario e índice de consulta en los 4 volúmenes | Todos | **Añadido** |
| 17 | Faltaban guía de lectura y nota de vigencia en los vols. 2, 3 y 4 | Vols. 2–4 | **Añadido** |
| 18 | El índice imprimía decenas de filas de puntos con folio pero **sin título** bajo «Referencias» (anclas bibliográficas `### {#ref-…}` convertidas en encabezados vacíos) | 4 volúmenes | **Corregido** (filtro `tools/lua/reference-anchors.lua`, activo en PDF y EPUB) |
| 19 | El índice rápido del Vol. 1 remitía a un «Mapa de prerrequisitos» entre volúmenes que **no existía** en su guía de lectura: era el único volumen sin mapa de serie | Vol. 1, guía y índice rápido | **Corregido** (nueva sección «Mapa de la serie») |
| 20 | La causa señalada del «salto abrupto» entre teoría y código no estaba en el capítulo 8 (que ya abría con nota de orientación) sino en la guía de lectura, que no explicaba **cómo** leer los bloques de código | Vol. 1, guía y cap. 8 | **Corregido** (nueva sección «Cómo leer el código de este volumen»; la nota del cap. 8 ahora remite a ella) |
| 21 | La guía y el índice del Vol. 4 afirmaban que el Epílogo es «común a los cuatro volúmenes»; el Epílogo **solo existe como sección en el Vol. 4** (los vols. 2 y 3 no lo mencionan siquiera; el Vol. 1 solo lo menciona, sin imprimirlo) | Vol. 4, guía y tabla de contenido | **Corregido** («se imprime en este volumen, no en los tres anteriores») |

## 3. Aparato editorial añadido (uniforme en los cuatro volúmenes)

Cada volumen incorpora ahora cinco secciones preliminares con el mismo nombre y la misma función, adaptadas a su contenido:

| Archivo | Función | Responde a |
|---|---|---|
| `04b_guia_de_lectura.md` | Rutas de lectura, mapa de prerrequisitos y uso como manual de consulta | **Entender** |
| `04c_nota_vigencia.md` | Qué caduca, qué no y cómo verificarlo | **Confiabilidad** |
| `05_cuaderno_de_lectura_critica.md` | Rúbrica de evaluación, plantilla de reseña y preguntas por capítulo | **Pensar y criticar** |
| `06_glosario.md` | Glosario operativo con remisión al capítulo | **Entender** |
| `07_indice_de_consulta_rapida.md` | Tabla «problema/síntoma → dónde acudir» + índice de ejercicios | **Consultar y resolver** |

Los cuatro `04_tabla_contenido.md` se actualizaron para anunciar estas secciones, de modo que el lector las vea desde el índice.

### Preguntas de discusión cubiertas
- Vol. 1: 10 capítulos.
- Vol. 2: 32 capítulos.
- Vol. 3: 25 capítulos.
- Vol. 4: 13 capítulos + Epílogo de la serie.
- **Total: 80 capítulos + Epílogo.**

## 4. Criterios editoriales aplicados

1. **Uniformidad sin homogeneizar el contenido.** Misma estructura de secciones en los cuatro volúmenes, con rúbrica y preguntas adaptadas al tipo de afirmación de cada uno (ingeniería en el Vol. 1, geopolítica y frontera en el Vol. 2, organización en el Vol. 3, métricas en el Vol. 4).
2. **Separación principio / implementación / dato.** Es la regla que el propio libro enseña y la que se aplicó al reseñarlo: permite criticar sin confundir niveles.
3. **Nada de relleno.** Cada pregunta remite a una sección o caso concreto del capítulo; las preguntas «Crítica:» señalan el punto donde el texto es más discutible, para que la crítica sea posible y no genérica.
4. **Trazabilidad mínima intervención.** Las correcciones de contenido se limitaron a errores objetivos (títulos, numeración, referencias cruzadas, erratas). No se reescribió prosa del autor.

## 5. Pendientes recomendados (no ejecutados)

Estos puntos no son defectos de lectura, pero afectan a la coherencia final de la obra. Se recomiendan antes de cerrar la edición:

1. **Nomenclatura de imágenes heredada de numeración antigua.** Existen carpetas `capitulo76/`, `capitulo77/`, `capitulo78/` (Vol. 2) y `capitulo80/` (Vol. 4), y activos `c21_1_*`, `c21_2_*`, `c21_3_*` referenciados desde el capítulo 9 del Vol. 4. Conviene renombrarlos y actualizar las rutas, o documentar el mapeo.
2. **ISBN pendiente.** Los cuatro `metadata_es.yaml` conservan `PENDIENTE-ISBN-VOLx-ES`.
3. **Residuo de conversión BibTeX→Markdown en las bibliografías de los vols. 2–4, y 70 entradas sin fuente verificada.** El Vol. 1 está limpio (0 patrones de máquina). En los demás, las entradas imprimen sintaxis de BibTeX dentro de la prosa:

   | Volumen | Entradas | Con residuo de máquina | Con «As cited…» / «no verificado» | Patrones `campo =` |
   |---|---|---|---|---|
   | 1 | 56 | **0** | 8 | 0 |
   | 2 | 73 | 54 | 29 | 116 |
   | 3 | 72 | 50 | 21 | 138 |
   | 4 | 44 | 22 | 12 | 57 |

   Ejemplos literales: `**Baghai, Mehrdad; Coley, Stephen; White, David** (1999). *The Alchemy of Growth, publisher = Perseus Books, year = 1999*.` y `**Autoridad del Canal de Panam\'a, title = As cited in the manuscript, August, year = 2026**`. También hay llaves sueltas (`…O'Reilly Media}, year = {2017.`) y escapes LaTeX (`D\'iaz-Rodr\'iguez`). Se confirmó que el residuo **llega al lector** en las ediciones ya generadas: `year =` aparece 76, 74 y 34 veces en los EPUB de los vols. 2, 3 y 4. La parte mecánica (retirar sintaxis sin inventar datos) es automatizable; la parte de fondo —las 70 entradas que remiten al manuscrito o declaran «bibliographic detail not fully verified»— exige verificación documental fuente por fuente y **no** puede resolverse maquetando. Ambas deben cerrarse antes de publicar.

   Causa raíz identificada: una conversión de `.bib` a `.md` que no se completó. De ahí también que los vols. 2–4 no conserven el `.bib` (el Vol. 1 sí).
4. **Índice analítico general de la serie.** Los índices de consulta rápida son por volumen; un índice maestro «concepto → volumen/capítulo» ayudaría al lector que cruza los cuatro tomos.
5. **Numeración del capítulo 10 del Vol. 4.** Su índice interno mezcla «Sección 1..5» con ejercicios 10.1/10.2; conviene decidir si se unifica en «10.1..10.x».
6. **Vol. 3, capítulo 6: sección «Q1 2025: Quarterly Closing»** es el ejemplo resuelto del ejercicio 6.1. Se retiró del índice por coherencia con el resto de la serie; si se quiere conservar en el índice, debe etiquetarse como parte del ejercicio.

## 6. Verificación

- Se comprobó que **los 80 capítulos** tienen sección de cierre («Lo esencial») y que **no quedan** referencias a la numeración antigua (`21.x`), títulos duplicados ni erratas detectadas.
- Se verificó la coherencia entre los nuevos índices y los capítulos: la numeración de ejercicios citada en cada `07_indice_de_consulta_rapida.md` coincide con los encabezados reales de los capítulos.
- Las cinco secciones donde «Lo esencial» no está al final (Vol. 2 cap. 1; Vol. 3 caps. 3, 6 y 7; Vol. 4 cap. 12) siguen un patrón **deliberado y consistente** de la serie: resumen y a continuación el ejercicio resuelto. No se modificaron.

## 7. Respuesta a la crítica externa del Vol. 1

Se recibió una reseña externa del Volumen 1 con cinco fortalezas y dos oportunidades de mejora. Las fortalezas se verificaron contra los datos del propio manuscrito; las dos objeciones se tradujeron en correcciones concretas.

### 7.1 Fortalezas alegadas, verificadas

| Fortaleza señalada | Verificación en el manuscrito (volumen completo, excluida la bibliografía) |
|---|---|
| Estado del arte con literatura indexada | Existe `estado-del-arte/estado-del-arte.md` propio del Vol. 1, con nueve secciones, alcance y método declarados y revisión crítica de literatura indexada (Hou et al. 2024; He et al. 2025, *ACM TOSEM*) |
| Distinción *workflow* / agente | Espectro de autonomía de cinco niveles en el cap. 1; 8 usos explícitos de la distinción |
| El arnés como sistema de control | 26 ocurrencias de «arnés»; sección propia en el cap. 4 |
| Advertencia sobre el *Token-Burn* | 6 ocurrencias; cuantificado además en el cap. 1 del Vol. 4 |
| Pragmatismo código en mano | 24 bloques de código, 1.306 líneas: el **55,7 % de todas las líneas del volumen**. AI Gateway (cap. 3), bucle ReAct tipado (cap. 4), orquestador y máquina de estados (cap. 8), servidor MCP (cap. 9) |
| Ley de Conway y SOLID adaptados | 6 y 9 ocurrencias respectivamente; los caps. 6 y 8 los traducen a dominios, roles y prompts |

### 7.2 Objeciones y corrección aplicada

| Objeción | Diagnóstico | Corrección |
|---|---|---|
| **Densidad cognoscitiva:** el paso de la teoría abstracta de agentes a bloques de código densos fatiga al lector sin base backend | Objetiva y medible: el **55,7 % de las líneas del volumen son código**; el cap. 3 dedica 148 líneas a un solo bloque, el 56,3 % de su extensión, y el cap. 8 acumula 374 líneas en 4 bloques (Python, TypeScript y Java). Los dos capítulos densos ya abrían con nota de orientación, pero la guía de lectura no explicaba **cómo** atravesar los bloques: el lector quedaba sin instrucción de uso | Nueva sección **«Cómo leer el código de este volumen»** en la guía (tres reglas: leer la frase que precede al bloque, no ejecutar en la primera pasada, separar patrón de herramienta) y enlace desde la nota de orientación del cap. 8 |
| **Estructura de serie:** las referencias constantes a los vols. 3 y 4 generan «ansiedad de completitud» | Objetiva: el cap. 8 remite 13 veces a otros tomos, y los caps. 9 y 10, diez veces cada uno. Además, el índice rápido prometía un «Mapa de prerrequisitos» entre volúmenes que **no existía** en la guía del Vol. 1, el único de los cuatro volúmenes sin mapa de serie. En cambio, la tabla de prerrequisitos del Vol. 1 no contiene **ninguna** entrada externa: el volumen se cierra a sí mismo | Nueva sección **«Mapa de la serie»** en la guía, con tabla de doble dirección (qué aporta cada tomo y qué necesita de este) y la declaración explícita de que las remisiones son profundizaciones diferidas, no requisitos; el índice rápido se actualizó para nombrar esa sección. Se corrigió además la afirmación, inexacta, de que el Epílogo es «común a los cuatro volúmenes» |

**Criterio aplicado.** Ninguna de las dos objeciones se resolvió reescribiendo prosa del autor: se corrigieron piezas del aparato editorial (guía de lectura, nota de capítulo, índice rápido) y se verificó cada afirmación nueva contra los datos del manuscrito. Las tablas de la sección «Mapa de la serie» se derivaron de las tablas de prerrequisitos ya existentes en las guías de los vols. 2, 3 y 4, sin añadir dependencias nuevas.