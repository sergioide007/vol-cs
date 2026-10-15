# Synthetic Code — Editorial Translation & Linguistic Style Guide
**Target Language:** Native United States English (`en-US`)  
**Standard:** Chicago Manual of Style (17th ed.) / Merriam-Webster Unabridged  
**Domain Register:** High-level Systems Architecture, Distributed Computing, AI Engineering

---

## 1. Editorial Voice & Linguistic Register

The English edition of *Synthetic Code* must sound like it was conceived and authored natively in the English-speaking systems engineering community (in the tradition of Martin Kleppmann, Martin Fowler, Brendan Burns, and Stuart Russell). It is neither a literal word-for-word translation nor an academic lecture; it is an authoritative, pragmatic, and intellectually rigorous guide for lead architects and senior engineers.

### Cardinal Linguistic Rules
1. **American English Spelling & Mechanics:**
   - Use US conventions: *behavior*, *synchronization*, *canceled*, *program*, *modeling*, *defense*, *disc* (optical) vs. *disk* (magnetic/storage).
   - Commas and periods go **inside** quotation marks (*"Synthetic Code,"* not *,"*).
   - Em-dashes (`—`) are set without surrounding spaces: `word—another word`.
   - Oxford (serial) comma is mandatory: `perception, reasoning, action, and memory`.

2. **Elimination of "Translationese" & Nominalizations:**
   - Prefer strong, active verbs over passive voice and bloated noun stacks.
   - Spanish: *"La implementación del disyuntor agéntico permite la protección..."*
   - Bad literal English: *"The implementation of the agentic circuit breaker allows the protection of..."*
   - Native US English: *"The agentic circuit breaker shields the backend by cutting execution when failure rates spike..."*

3. **Strict Ban on AI Cliches & Fluff:**
   - Never use: *"In today's fast-paced world,"* *"Delve into,"* *"Tapestry,"* *"Beacon,"* *"Crucial to remember,"* *"It goes without saying,"* *"Game-changer,"* *"Holistic landscape."*
   - Be concise, direct, and unsparingly technical.

---

## 2. Canonical Terminology Lexicon (ES ↔ EN)

| Spanish Original | Canonical US English | Notes / Context |
|---|---|---|
| **Código Sintético** | **Synthetic Code** | Series main title |
| **Volumen 1: Fundamentos** | **Volume 1: Foundations** | Architecture, Economics & Ethics |
| **Volumen 2: Frontera y Aplicaciones** | **Volume 2: Frontiers and Applications** | Geopolitics, Critical Industries & IDEs |
| **Volumen 3: Madurez Organizacional** | **Volume 3: Organizational Maturity** | Governance, Autonomy & Agent Teams |
| **Volumen 4: Patrones de Escala** | **Volume 4: Scale Patterns** | Orchestration, Resilience & Cost |
| **Arnés (*harness*)** | **Harness** | The host runtime containing loop, security & tools |
| **Enjambre** | **Swarm** | Multi-agent collaborative ecosystem |
| **Bucle agéntico** | **Agent loop / Agentic loop** | Execution cycle (e.g., ReAct) |
| **Disyuntor agéntico** | **Agentic circuit breaker** | Failure-rate threshold trip |
| **Radio de impacto** | **Blast radius** | Safety and destruction perimeter |
| **Presupuesto de tokens / ciclos** | **Token budget / Iteration budget** | Bounded computation resource |
| **Frontera de dominio** | **Domain boundary / Bounded context** | DDD concept applied to agent roles |
| **Plano de control gobernado** | **Governed control plane** | Infrastructure-level policy enforcement |
| **Compañero de trabajo digital** | **Digital coworker** | Persistent agent (e.g., OpenAI Dots) |
| **Código Limpio Sintético** | **Synthetic Clean Code** | The adaptation of Clean Code to synthetic artifacts |
| **Pista ejecutiva** | **Executive Track** | Dedicated sidebar for leadership |
| **Lo esencial del capítulo** | **Chapter Takeaways** | Chapter-closing summary section |
| **Cuaderno de lectura crítica** | **Critical Reading Workbook** | Evaluation rubrics & review templates |
| **Guía de lectura** | **Reading Guide** | Reading pathways & prerequisites |
| **Nota de vigencia** | **Shelf-Life Note** | Technical obsolescence guide |
| **Índice de consulta rápida** | **Quick Reference Index** | Symptom-to-solution index |
| **Portadilla** | **Half-title / Interior Title** | Front matter title page |
| **Hoja de créditos** | **Copyright & CIP** | Legal and publisher imprint |
| **Dedicatoria** | **Dedication** | Author dedications |
| **Prólogo** | **Foreword** | Introductory guest essay |
| **Prefacio** | **Preface** | Author's framing remarks |

---

## 3. Structural & Code Formatting Invariants

1. **Citation Anchors:**  
   Anchor identifiers (`[Author, Year](#ref-anchor)`) and target IDs (`### {#ref-anchor}`) must remain **100% character-for-character identical** to the Spanish edition. This guarantees automated citation checkers, bibliography generation, and PDF link engines resolve properly.
2. **Code Blocks:**
   - Keep variable names and core syntax identical so readers and test suites can execute the code across languages.
   - Translate comments, docstrings, and console messages into natural, idiomatic American English.
3. **Diagrams & Visual Assets:**
   - Reference images in `manuscrito/imagenes/` preserving file paths and captions.
4. **Markdown Tables & Formatting:**
   - Retain GFM table formatting, alerts (`> [!NOTE]`, `> [!IMPORTANT]`), and callout headers verbatim.
