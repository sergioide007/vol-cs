# Guía de lectura y mapa de prerrequisitos

_Este es el volumen más operativo de la serie: no explica qué es un agente, sino qué hacer el lunes después de tenerlo en producción. Su dificultad no está en los conceptos, sino en que casi todos sus capítulos piden un sistema real delante. Esta guía indica con qué orden sacarles partido y qué necesitar tener ya construido._

## 1. Estructura del volumen

- **Economía y medición (caps. 1, 2, 11, 12).** Costo por iteración útil, estimación probabilística, métricas de enjambre y eficiencia energética. Es el bloque que responde a «cuánto cuesta y cómo lo sé».
- **Calidad y defensa (caps. 3, 4, 6).** Testing de sistemas no deterministas, seguridad del stack agéntico y arquitectura limpia. Bloque de verificación.
- **Operación y datos (caps. 7, 8).** Arquitectura *event-driven* y observabilidad/MLOps para equipos pequeños.
- **Práctica completa (caps. 5, 9).** Un playbook de casos de uso y una semana real de trabajo documentada día a día.
- **Horizonte (caps. 10, 13 y Epílogo).** Evolución de las arquitecturas, recuperación ante desastres y cierre de la serie.

## 2. Tres rutas de lectura

| Ruta | Para quién | Secuencia |
|---|---|---|
| **«Mi agente ya está en producción y me cuesta dinero»** | Equipos con sistema vivo | 1 → 2 → 11 → 8 → 12 |
| **«Voy a construir en serio la próxima vez»** | Quien diseña ahora | 6 → 7 → 3 → 4 → 5 → 13 |
| **Lectura secuencial** | Quien prepara un plan completo de operación | 1 → 13 en orden, con el playbook (cap. 5) y la semana real (cap. 9) al final como integración |

## 3. Mapa de prerrequisitos

| Capítulo | Prerrequisito real | Si le resulta denso |
|---|---|---|
| 1. El silencioso Token-Burn | Vol. 1, cap. 3 (gateway y presupuesto) | Vol. 1, cap. 3 |
| 2. Estimaciones probabilísticas | Ninguno; ayuda haber estimado proyectos | — |
| 3. Testing de sistemas agénticos | Vol. 1, cap. 4 (evals y arnés) | Vol. 1, cap. 4 |
| 4. Seguridad en el stack agéntico | Vol. 2, cap. 1 | Vol. 2, cap. 1 |
| 5. El playbook del orquestador | Vol. 1, caps. 5, 8 y 9 | Vol. 1, cap. 8 |
| 6. Arquitectura limpia | Vol. 1, cap. 6 (DDD) | Vol. 1, cap. 6 |
| 7. Arquitectura *event-driven* | Vol. 2, cap. 4 (reactivo) | Vol. 2, cap. 4 |
| 8. Observabilidad y MLOps | Ninguno; ayuda conocer métricas de servicio | — |
| 9. La semana del coverage | Haber usado un agente en el IDE | Caps. 6 y 8 |
| 10. Evolución de las arquitecturas | Vol. 1 completo, en especial caps. 9 y 10 | Vol. 1, caps. 9 y 10 |
| 11. Métricas de KPI | Cap. 8 | Cap. 8 |
| 12. Bajo consumo de energía | Cap. 1 | Cap. 1 |
| 13. Recuperación ante desastres | Caps. 7 y 8 | Caps. 7 y 8 |

## 4. Cómo usar este volumen como manual de consulta

Tres de sus capítulos funcionan como referencia permanente, no como lectura de una vez: el **capítulo 5** (playbook de casos, se consulta por caso), el **capítulo 8** (se consulta por alerta o por métrica ausente) y el **capítulo 13** (se consulta el día que hay un incidente, y conviene haberlo leído antes de que ocurra). El **Índice de consulta rápida** de este volumen traduce «qué me está pasando» a un capítulo y una sección concretos.

## 5. Nota sobre el Epílogo de la serie

El **Epílogo** es común a los cuatro volúmenes y no añade teoría: sintetiza, cierra y agradece. Se puede leer en cualquier momento, pero su lectura completa solo rinde después del capítulo 13 de este volumen. Contiene «Lo esencial del recorrido completo», útil como repaso final de toda la serie.