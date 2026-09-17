# Nota sobre vigencia tecnológica

_Este volumen es el que contiene más cifras concretas de la serie: precios por token, costos de infraestructura, percentiles de latencia y configuraciones de herramientas. Es, por tanto, el que exige más disciplina de verificación por parte del lector._

## 1. Qué caduca y qué no

| Tipo de contenido | Vida útil | Cómo verificarlo |
|---|---|---|
| Precios por token y tarifas de proveedor | Muy corta (semanas) | Página oficial de precios del proveedor, con fecha |
| Benchmarks de modelos y comparativas de IDE | Muy corta | Tabla pública vigente; nunca citar este volumen sin cotejar |
| Versiones de herramientas y SDK | Corta | Notas de versión oficiales |
| Costos de infraestructura (EKS, on-premise, almacenamiento) | Media (6–18 meses) | Cotización propia; las cifras del libro son órdenes de magnitud |
| Métricas y umbrales (CIU, percentiles, alertas) | Larga | Se recalculan con sus propios datos; el **método** es lo que perdura |
| Patrones (arquitectura limpia, *event-driven*, DR agéntico, degradación) | Larga | Se validan por razonamiento y por resultados, no por la versión de la herramienta |

## 2. La regla que este volumen pide al lector

**Ninguna cifra de este volumen debe usarse en una decisión sin recalcularla con sus propios datos.** El libro da el método y el orden de magnitud; el número real sale de su gateway, su factura y su latencia medida. Cuando un capítulo ofrece una tabla de costos, la usa como estructura de cálculo, no como presupuesto.

## 3. Aviso sobre las configuraciones de referencia

El capítulo 13 (recuperación ante desastres) incluye protocolos y configuraciones de referencia (EKS + Velero + Argo; Ansible + Docker on-premise). Son puntos de partida verificables contra la documentación oficial de cada herramienta, no configuraciones listas para producir sin revisión. Trátelas como un plano, no como una instalación: la última comprobación siempre es un ensayo de recuperación real, y eso el propio capítulo lo exige.