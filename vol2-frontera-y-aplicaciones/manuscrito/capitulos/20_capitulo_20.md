# Capítulo 20: América Latina y África en multiagentes, el salto que aún es posible y los mecanismos para darlo

> *No se compite con quien lleva 40 años construyendo. Se construye en los espacios que el que lleva 40 años nunca pudo alcanzar.*

## La paradoja del rezago que habilita

**■ PISTA EJECUTIVA**


Existe una asimetría estructural que pocas veces se enuncia con precisión técnica: América Latina y el África subsahariana no poseen la infraestructura de cómputo de China, ni los capitales de riesgo de USA, ni el tejido regulatorio maduro de Europa. Sin embargo, carecen también del lastre que esas ventajas traen consigo: cuarenta años de sistemas monolíticos que migrar, deuda técnica acumulada en COBOL y mainframes, y resistencias culturales a la adopción de nuevos paradigmas en organizaciones saturadas de procesos heredados.

La implicación técnica es directa: una institución bancaria nueva en Nairobi o en Medellín no hereda el problema de legado que documentan Feathers (2004) en *Working Effectively with Legacy Code* o que describe el teorema de Lehman sobre la degradación de sistemas de larga vida. Puede diseñar su stack desde el primer día con arquitectura agéntica nativa: orquestadores en LangGraph o AutoGen, memoria distribuida en Redis Vector, herramientas expuestas vía MCP. La ausencia de pasado es una ventaja de arquitectura.

## África subsahariana: la ventaja del móvil como plataforma universal

Ahora bien, el caso africano demanda un análisis independiente del latinoamericano porque sus condicionantes estructurales difieren. La tasa de penetración de smartphones en África subsahariana alcanzó el 51 % en 2023 (GSMA, *Mobile Economy Sub-Saharan Africa 2024*), mientras que la penetración de banca tradicional permanece por debajo del 40 % en muchos mercados. Esta asimetría (más dispositivos móviles que cuentas bancarias) configura un entorno donde los agentes de IA se despliegan necesariamente sobre infraestructura móvil, no sobre servidores de escritorio ni navegadores web.

El modelo M-Pesa (plataforma de pago móvil que en Kenya procesa más del 50 % del PIB nacional anualmente) ilustra cómo la adopción masiva puede producirse sin pasar por las fases intermedias que recorrió Occidente. La hipótesis técnica es que los enjambres de agentes seguirán el mismo patrón: salto directo a agentes conversacionales en WhatsApp, Telegram o plataformas USSD para mercados sin datos móviles.

La comunidad Masakhane (fundada en 2018, con más de 800 investigadores en 30 países africanos) ha producido modelos de lenguaje y datasets para más de 56 lenguas africanas, publicando en venues Q1 como ACL, EMNLP y NAACL:

| Iniciativa Masakhane | Contribución técnica | Publicación |
|---------------------|---------------------|-------------|
| MasakhaNER 2.0 | NER en 21 lenguas africanas | Adelani et al. (2022), EMNLP |
| AfriSenti | Análisis de sentimiento en 14 lenguas | Muhammad et al. (2023), EMNLP |
| Lafand-MT | Traducción automática para lenguas de baja dotación | Alabi et al. (2022), ACL |
| MasakhaPOS | POS tagging para 20 lenguas | Dione et al. (2023), ACL |

Estas contribuciones no son investigación académica desconectada de la práctica: son los datasets y modelos base que hacen posible que un agente conversacional en Swahili, Yoruba o Amhárico entienda consultas médicas, agrícolas o financieras sin necesidad de pasar por inglés como lengua intermediaria, lo cual introduce errores de traducción cultural que ningún sistema de prompt engineering puede corregir completamente.

## América Latina: verticales donde el contexto local es ventaja competitiva

La situación latinoamericana difiere en estructura. La región posee una base tecnológica más madura (con hubs como São Paulo, Buenos Aires, Bogotá, Ciudad de México y Montevideo) y un mercado de talento de software considerablemente mayor que el africano. Argentina, con sus 320 000 desarrolladores de software (estimación CESSI, 2024), representa un pool de talento cuyo coste-hora es entre 3x y 5x inferior al de USA para perfiles equivalentes.

El problema central no es la falta de talento; es la falta de *dirección*. A este respecto, los enjambres que tienen mayor probabilidad de impacto en América Latina son aquellos donde el contexto local es una ventaja competitiva insuperable para actores externos:

**Agentes de precisión agrícola.** Brasil concentra el 26 % de la producción global de soja ([CONAB, 2024](#ref-conab2024)) y posee el sistema de monitoreo de deforestación más sofisticado del mundo (PRODES/INPE). Un enjambre de agentes que integre imágenes Sentinel-2 del Copernicus Program con datos de rendimiento de cultivos de Embrapa puede generar recomendaciones de fertilización a escala de parcela que ningún actor global puede replicar sin los datos específicos del Cerrado y la Amazonia Legal.

**Agentes de logística urbana caótica.** Ciudad de México, São Paulo y Bogotá figuran entre las ciudades con mayor congestión de tráfico del mundo ([TomTom Traffic Index, 2023](#ref-tomtom2023)). Rappi, Mercado Libre y iFood han entrenado modelos de optimización de rutas sobre millones de entregas en condiciones que los modelos entrenados sobre datos de Amsterdam o Berlín no pueden generalizar. Los agentes de enrutamiento de última milla entrenados en caos urbano latinoamericano son, por tanto, exportables a otras megalópolis de países en desarrollo: Lagos, Mumbai, Jakarta.

**Agentes de salud en entornos de recursos limitados.** El sistema de salud de Perú, Guatemala o Bolivia opera con densidades médicas de 1–2 médicos por 1 000 habitantes, frente a los 4–5 de la OCDE. Un agente de triaje conversacional en español coloquial (que entienda regionalismos, que maneje ambigüedad diagnóstica y que sepa cuándo referir) tiene un mercado de 400 millones de hispanohablantes en situaciones de acceso limitado a atención primaria.

## La brecha que persiste: infraestructura de cómputo e inversión

No obstante, sería una distorsión intelectual omitir la brecha real que persiste. El entrenamiento de modelos fundacionales requiere clusters de GPU que América Latina y África no poseen a escala competitiva. El primer data center de Google en América Latina con capacidad de GPU de alta densidad abrió en Querétaro, México, en 2023; AWS inauguró su región en Chile en 2023. África subsahariana tiene acceso a GPU de alta gama principalmente vía Microsoft Azure (región Sudáfrica Norte, Johannesburgo) y Google Cloud (región Africa-West1, Accra). La latencia de estas regiones respecto a los centros de datos en Virginia, Oregón o Sao Paulo supone una penalización de 80–120 ms adicionales para cargas de trabajo agénticas en tiempo real.

La respuesta arquitectónica a esta limitación es la misma que el capítulo 12 articula para las arquitecturas híbridas: inferencia local para agentes de baja latencia, cloud para entrenamiento y modelos de largo contexto. Modelos cuantizados de 7B–13B parámetros corriendo en dispositivos de borde con NPUs (el escenario que MediaTek y Qualcomm están habilitando en el segmento móvil) pueden ejecutar la gran mayoría de las tareas de los agentes de primer nivel sin latencia de red.

## El mecanismo del salto: educación como palanca de corto plazo

**■ PISTA EJECUTIVA**


La trama se complica de manera interesante cuando se observa el vector de inversión más eficiente disponible: la educación agéntica. Mientras que competir en modelos fundacionales requiere de billones de dólares en GPU y años de investigación, formar arquitectos de enjambres requiere meses de formación intensiva y hardware modesto.

La Universidad de São Paulo, la Universidad de los Andes (Bogotá), el ITAM (Ciudad de México) y la Universidad de Buenos Aires poseen cuerpos docentes de machine learning y sistemas distribuidos capaces de insertar contenidos de arquitectura agéntica en sus currículos en 12–18 meses. La iniciativa AI4D Africa ([IDRC/UNESCO, 2023](#ref-idrcunesco2023)) financia exactamente ese tipo de capacitación en 10 países africanos. El retorno sobre la inversión es asimétrico: 1 millón de dólares en educación agéntica produce 50 arquitectos que pueden diseñar enjambres para verticales locales que generan cientos de millones de dólares en eficiencia.

> **Visión general:** La ausencia de infraestructura monolítica heredada en economías de ingreso medio-bajo constituye un factor habilitante para la adopción de arquitecturas de inteligencia artificial distribuida que no ha sido suficientemente tematizado en la literatura de transferencia tecnológica. Contrariamente a la hipótesis dominante que equipara rezago tecnológico con incapacidad de adopción agéntica, puede sostenerse que la inexistencia de deuda técnica sistémica (verificable en el caso de nuevas instituciones financieras subsaharianas (Kenya, Nigeria, Ghana) y en el de startups tecnológicas latinoamericanas post-2015) constituye una ventaja de primer orden para la adopción de arquitecturas agénticas nativas. Esta hipótesis es consistente con la evidencia empírica producida por la comunidad Masakhane (Adelani et al., EMNLP 2022; Muhammad et al., EMNLP 2023) y con los patrones de adopción documentados en el sector AgTech brasileño (Embrapa/INPE, 2023-2024), que muestran tasas de adopción de herramientas de IA distribuida superiores a las de mercados con mayor madurez tecnológica previa.

## Lo esencial del capítulo 20

- La ausencia de deuda técnica heredada es ventaja arquitectónica: América Latina y África pueden ser nativas en agentes desde el primer día.
- La comunidad Masakhane ha producido modelos y datasets Q1 para 56+ lenguas africanas, habilitando agentes conversacionales sin intermediación anglófona.
- Los verticales de mayor impacto en LATAM son agroprecisión, logística urbana caótica y salud en entornos de recursos limitados, todos con contextos locales irreproducibles por actores globales.
- La brecha de infraestructura de GPU se mitiga con inferencia local (modelos 7B–13B cuantizados en dispositivos de borde) + cloud para tareas de largo contexto.
- La educación agéntica es la palanca de mayor retorno: 1M USD en formación produce arquitectos que diseñan enjambres para verticales de cientos de millones.
