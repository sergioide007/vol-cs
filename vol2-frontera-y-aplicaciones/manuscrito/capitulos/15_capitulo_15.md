# Capítulo 15: Música en multiagentes de IA: del acorde al enjambre melódico que aprende de sí mismo

> *Un compositor escribe una nota. Un enjambre de agentes compone una sinfonía que entiende por qué esa nota era la única posible en ese compás.*

## Cuando la armonía emerge del caos distribuido: el estado del arte

He aquí un fenómeno que desafía la intuición musical convencional: la composición de calidad es un diálogo entre especialistas sintéticos con dominios de conocimiento no solapados, no el acto solitario de un genio. Para comprender por qué esto es así, conviene primero trazar el arco de la investigación en generación musical por IA.

El paper de Dhariwal et al. (*Jukebox: A Generative Model for Music*, NeurIPS 2020) marcó el primer hito de la generación de audio crudo a nivel de muestra (no MIDI): Jukebox producía canciones completas con voz, letra e instrumentación usando transformers sobre tokens de audio comprimido. Sin embargo, Jukebox generaba bloques de audio sin semántica musical estructurada: la armonía emergía de patrones estadísticos, no de reglas de contrapunto.

El salto cualitativo llegó con MusicLM (Agostinelli et al., *MusicLM: Generating Music From Text*, Google Research, arXiv:2301.11325, 2023): por primera vez, un modelo convertía descripciones de texto en audio musical de alta fidelidad, condicionado semánticamente. La arquitectura MusicLM opera con tokens jerárquicos (MuLaN para semántica textual-musical, SoundStream para tokens de audio): el texto "guitarra acústica melancólica en modo menor, tempo lento" produce audio coherente con esa descripción.

| Modelo | Año | Entrada | Calidad audio | Coherencia musical | Acc. |
|--------|-----|---------|---------------|--------------------|----|
| Jukebox (OpenAI) | 2020 | Género + artista | 44 kHz raw | Baja estructural | Abierto |
| MusicLM (Google) | 2023 | Texto | 24 kHz | Media | Restringido |
| AudioCraft/MusicGen (Meta) | 2023 | Texto + melodía ref. | 32 kHz | Alta | Abierto |
| Stable Audio (Stability AI) | 2023 | Texto + duración | 44 kHz | Alta | Comercial |
| Suno v3 (Suno) | 2024 | Texto + letra | 44 kHz + voz | Muy alta | Comercial |
| Udio (Udio) | 2024 | Texto | 44 kHz | Muy alta | Comercial |

## Por qué los géneros musicales demandan especialización agéntica: la arquitectura de la diversidad

La música clásica, el jazz, la música electrónica, el flamenco y la música étnica tienen *arquitecturas de conocimiento radicalmente distintas* que ningún modelo generalista puede dominar simultáneamente en profundidad.

La música clásica exige conocimiento de las reglas de contrapunto codificadas por Johann Joseph Fux en *Gradus ad Parnassum* (1725) y consolidadas en la práctica barroca y clásica: prohibición de quintas y octavas paralelas, resolución obligatoria de sensibles, conducción de voces por grados conjuntos cuando es posible. Un *agente de contrapunto* entrenado exclusivamente sobre el corpus de Bach, Handel y Haydn puede evaluar y corregir una propuesta melódica contra estas reglas con una precisión que ningún modelo generalista alcanza.

El jazz opera sobre una lógica diferente: las reglas armónicas son *tensiones que esperan resolución*, no prohibiciones. Un ii-V-I en Re menor implica posibilidades de sustitución tritonal (reemplazar G7 por Db7), uso de escalas alteradas (la "superlocria"), y cromatismo idiomático. Un *agente de improvisación jazz* debe entender no solo la teoría, sino las convenciones estilísticas de sub-géneros (bebop, post-bop, modal jazz), que tienen vocabularios diferentes.

La consecuencia arquitectónica es ineludible: una arquitectura monolítica que pretenda generar música clásica, jazz, electrónica y flamenco con igual profundidad es, en el mejor caso, mediocre en todos los géneros. El enjambre especializa cada agente en un dominio y delega al orquestador la selección del agente apropiado según la intención compositiva.

## La arquitectura técnica: codecs neurales, tokens de audio y orquestación por eventos

**► PISTA TÉCNICA**


La plataforma técnica que habilita el enjambre musical descansa sobre un avance clave de 2022: los *codecs de audio neurales*. EnCodec (Défossez et al., Meta AI Research, arXiv:2210.13438, 2022) y DAC (*Descript Audio Codec*, Kumar et al., NeurIPS 2023) codifican audio de alta fidelidad en secuencias de tokens discretos a tasas de compresión de 8–16x respecto al PCM crudo. Esta compresión es lo que hace posible que un transformer opere sobre audio de minutos de duración dentro de una ventana de contexto manejable.

Sobre esta base, el enjambre musical opera con la siguiente topología de agentes especializados:

```
Capa 1 — Director Creativo (humano o agente coordinador)
  │ intención emocional + género + referencia
  ▼
Capa 2 — Agente de Estructura
  │ define forma: Intro-A-B-A'-Outro, 32 compases, 4/4, 120 BPM
  ▼
Capa 3 — Agentes de Dominio (en paralelo)
  ├── Agente Armónico → propone progresión de acordes
  ├── Agente Melódico → propone línea de voz principal
  ├── Agente Rítmico → propone groove y subdivisiones
  └── Agente Tímbrico → selecciona paleta sonora (síntesis / samples)
  ▼
Capa 4 — Agente Evaluador (triple gate)
  ├── Gate 1: coherencia armónica (penaliza disonancias no idiomáticas)
  ├── Gate 2: continuidad melódica (penaliza saltos > octava no preparados)
  └── Gate 3: alineación emocional (valida mediante modelo MER)
  ▼
Capa 5 — Agente de Renderizado
  │ genera audio final vía AudioCraft / DAC / VST plugins
```

El *Agente Evaluador* merece análisis técnico específico. Su Gate 3 (alineación emocional) utiliza modelos de *Music Emotion Recognition* (MER) entrenados sobre el conjunto de datos DEAM (*Database for Emotional Analysis in Music*, Aljanaki et al., 2017) en el espacio bidimensional Valencia-Arousal de Russell (1980). Un fragmento con alta Valencia y alto Arousal (cuadrante "happy/excited") se valida como coherente con una intención compositiva de "celebración"; un fragmento con baja Valencia y bajo Arousal (cuadrante "sad/calm") se valida para "melancolía nocturna".

## La dimensión ejecutiva: propiedad intelectual y el modelo de negocio creativo

**■ PISTA EJECUTIVA**


La trama se complica cuando se traslada la discusión al plano de la propiedad intelectual y el modelo de negocio. En la jurisdicción americana, el caso Andersen v. Stability AI (2023) y el procedimiento del U.S. Copyright Office sobre obras creadas por IA (2023) han establecido que obras generadas íntegramente por IA sin selección y disposición humana creativa sustancial no son elegibles para protección por copyright. Para el Product Owner de una plataforma de composición musical por IA, esto implica un diseño cuidadoso del flujo de trabajo:

- La selección del género, la referencia emocional, la estructura formal y la revisión final (si las realiza el usuario humano) pueden constituir la "selección y disposición creativa" suficiente para establecer autoría.
- Un proceso donde el usuario simplemente pulsa "generar" sin aportación creativa documentada produce una obra en dominio público desde el momento de su creación.

Las plataformas Suno y Udio han adoptado estrategias de mitigación distintas: Suno posiciona al usuario como "letrista y director creativo" (la plataforma es la "orquesta"), mientras que Udio documenta cada parámetro de personalización como evidencia de aportación humana. Ambas estrategias buscan el mismo objetivo: crear una cadena de proveniencia que demuestre autoría humana sustancial sobre la obra resultante.

Para un Scrum Master que gestiona sprints de desarrollo de herramientas musicales con IA, la Definition of Done de cualquier feature de generación musical debe incluir: evidencia de auditoría de datasets de entrenamiento (fundamental para el cumplimiento del AI Act Art. 51 sobre GPAI), documentación del mecanismo de contribución creativa del usuario, y pruebas de que el modelo no reproduce fragmentos identificables de obras protegidas (mediante técnicas de membership inference testing).

> **Visión general:** La generación musical mediante arquitecturas de agentes especializados por dominio constituye una instancia del problema general de *satisfacción de restricciones distribuidas* (Distributed Constraint Satisfaction Problem, DisCSP) en el que las variables de decisión (progresión armónica, línea melódica, perfil rítmico, paleta tímbrica) presentan interdependencias que no pueden ser optimizadas simultáneamente por un único agente sin pérdida de coherencia estilística. La especialización agéntica por subdominio permite que cada agente opere sobre un espacio de búsqueda reducido y semanticamente coherente, incrementando la calidad de las propuestas locales, mientras que la arquitectura de evaluación multi-gate (coherencia armónica, continuidad melódica, alineación emocional en el espacio Valencia-Arousal de Russell 1980) funciona como mecanismo de coordinación que descarta las propuestas incompatibles antes de su materialización en audio, garantizando que solo los candidatos que satisfacen simultáneamente las restricciones de todos los dominios sean renderizados por la capa de síntesis.

## Lo esencial del capítulo 15

- La investigación evolucionó de Jukebox (2020, audio crudo estadístico) a MusicLM (2023, condicionado semánticamente) a Suno/Udio (2024, calidad comercial con voz): cada salto cualitativo demandó mayor especialización de componentes.
- Los codecs neurales (EnCodec, DAC) son la infraestructura técnica que hace posible que transformers operen sobre audio a escala de minutos: sin ellos, el enjambre musical no podría existir.
- La arquitectura de cinco capas (Director → Estructura → Dominio paralelo → Evaluador → Renderizado) materializa el principio de constraint satisfaction distribuido en producción musical real.
- La triple gate del Agente Evaluador (coherencia armónica + continuidad melódica + alineación emocional en Valencia-Arousal) es el mecanismo que garantiza coherencia emergente sin que ningún agente domine todos los dominios.
- La autoría de obras generadas por IA requiere diseño deliberado del flujo de interacción humana; sin aportación creativa documentada, el resultado es dominio público.
