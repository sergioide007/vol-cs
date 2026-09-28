# Auditoría del manuscrito

Fecha: 2026-09-28 · 4 volúmenes · 80 capítulos · 172.084 palabras de prosa

Generado por `tools/lint_manuscript.py`. Complementa a `validate_editions.py`, que solo comprueba la maquetación. La lista completa de hallazgos está en `dist/AUDIT.json`; este informe se recorta por archivo para que se pueda leer.

## Resumen por comprobación

| ID | Comprobación | Errores | Avisos |
|---|---|---:|---:|
| C1 | remisiones cruzadas | 0 | 37 |
| C2 | bibliografía sin verificar | 33 | 0 |
| C3 | cifras sin origen declarado | 0 | 263 |
| C4 | apéndices y marcadores pendientes | 0 | 14 |
| C5 | numeración antigua | 0 | 0 |
| C6 | modelos fijados en el texto | 0 | 0 |
| C7 | presupuesto de palabras | 0 | 23 |
| C8 | anclas bibliográficas | 0 | 0 |
| C9 | carpetas de imágenes | 0 | 13 |
| C11 | año de la cita | 1 | 0 |
| C12 | lenguaje | 0 | 0 |
| C13 | glifos no representables | 0 | 0 |

## Detalle por volumen

| Volumen | Capítulos | Palabras | Errores | Avisos |
|---|---:|---:|---:|---:|
| 1 — Fundamentos | 10 | 21.140 | 3 | 21 |
| 2 — Frontera y Aplicaciones | 32 | 58.177 | 17 | 111 |
| 3 — Madurez Organizacional | 25 | 52.933 | 7 | 94 |
| 4 — Patrones de Escala | 13 | 36.457 | 7 | 111 |

## C1 · remisiones cruzadas (37)

**`vol1-fundamentos/estado-del-arte/estado-del-arte.md`**

- L19 ! «capítulo 12» remite al cap. 12 sin decir de qué tomo: en el Vol. 1 no existe; sí en los Vols. 2, 3, 4

**`vol1-fundamentos/front-matter/04b_guia_de_lectura.md`**

- L49 ! «caps. 29–31» remite al cap. 29 sin decir de qué tomo: en el Vol. 1 no existe; sí en el Vol. 2
- L50 ! «cap. 13» remite al cap. 13 sin decir de qué tomo: en el Vol. 1 no existe; sí en los Vols. 2, 3, 4
- L50 ! «caps. 22–25» remite al cap. 22 sin decir de qué tomo: en el Vol. 1 no existe; sí en los Vols. 2, 3

**`vol1-fundamentos/manuscrito/capitulos/05_capitulo_5.md`**

- L211 ! «capítulos 19» remite al cap. 19 sin decir de qué tomo: en el Vol. 1 no existe; sí en los Vols. 2, 3

**`vol1-fundamentos/manuscrito/capitulos/08_capitulo_8.md`**

- L472 ! remisión mal formada: «(capítulo 1 (Vol. 4), Vol. 4)» — la forma correcta es «(Vol. N, cap. M)»

**`vol1-fundamentos/manuscrito/capitulos/10_capitulo_10.md`**

- L26 ! «cap. 14» remite al cap. 14 sin decir de qué tomo: en el Vol. 1 no existe; sí en los Vols. 2, 3

**`vol3-madurez-organizacional/manuscrito/capitulos/07_capitulo_7.md`**

- L30 ! «Cap. 26» remite al cap. 26 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2
- L30 ! «Cap. 27» remite al cap. 27 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2
- L79 ! «Cap. 27» remite al cap. 27 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2
- L83 ! «Cap. 29» remite al cap. 29 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/09_capitulo_9.md`**

- L23 ! «cap. 29» remite al cap. 29 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/10_capitulo_10.md`**

- L59 ! «cap. 32» remite al cap. 32 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/13_capitulo_13.md`**

- L77 ! «cap. 31» remite al cap. 31 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2
- L86 ! «cap. 27» remite al cap. 27 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/14_capitulo_14.md`**

- L89 ! «cap. 31» remite al cap. 31 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/20_capitulo_20.md`**

- L7 ! «cap. 29» remite al cap. 29 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol3-madurez-organizacional/manuscrito/capitulos/25_capitulo_25.md`**

- L54 ! «cap. 26» remite al cap. 26 sin decir de qué tomo: en el Vol. 3 no existe; sí en el Vol. 2

**`vol4-patrones-de-escala/manuscrito/capitulos/05_capitulo_5.md`**

- L81 ! «capítulos 14» remite al cap. 14 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L105 ! «capítulos 14» remite al cap. 14 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L210 ! «capítulo 20» remite al cap. 20 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3

**`vol4-patrones-de-escala/manuscrito/capitulos/07_capitulo_7.md`**

- L12 ! «capítulos 14» remite al cap. 14 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3

**`vol4-patrones-de-escala/manuscrito/capitulos/08_capitulo_8.md`**

- L17 ! «cap. 16» remite al cap. 16 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L117 ! «capítulos 15» remite al cap. 15 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3

**`vol4-patrones-de-escala/manuscrito/capitulos/12_capitulo_12.md`**

- L178 ! «Cap. 22» remite al cap. 22 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3

**`vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md`**

- L53 ! «caps. 17» remite al cap. 17 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L54 ! «cap. 19» remite al cap. 19 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L54 ! «cap. 20» remite al cap. 20 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L54 ! «cap. 21» remite al cap. 21 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L55 ! «cap. 22» remite al cap. 22 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L55 ! «cap. 23» remite al cap. 23 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L55 ! «cap. 24» remite al cap. 24 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L55 ! «cap. 25» remite al cap. 25 sin decir de qué tomo: en el Vol. 4 no existe; sí en los Vols. 2, 3
- L56 ! «cap. 26» remite al cap. 26 sin decir de qué tomo: en el Vol. 4 no existe; sí en el Vol. 2
- L61 ! «cap. 29» remite al cap. 29 sin decir de qué tomo: en el Vol. 4 no existe; sí en el Vol. 2
- L62 ! «cap. 30» remite al cap. 30 sin decir de qué tomo: en el Vol. 4 no existe; sí en el Vol. 2
- L62 ! «cap. 31» remite al cap. 31 sin decir de qué tomo: en el Vol. 4 no existe; sí en el Vol. 2


## C2 · bibliografía sin verificar (33)

**`vol1-fundamentos/referencias/referencias.md`**

- L20 ✘ «chase2025» se declara sin verificar (01_capitulo_1.md)
- L92 ✘ «mitchell2025» se declara sin verificar (01_capitulo_1.md)
- L158 ✘ «wang2023aieng» se declara sin verificar (02_capitulo_2.md)

**`vol2-frontera-y-aplicaciones/referencias/referencias.md`**

- L45 ✘ «cisco2024» se declara sin verificar (11_capitulo_11.md)
- L58 ✘ «conab2024» se declara sin verificar (20_capitulo_20.md)
- L71 ✘ «ecns2026» se declara sin verificar (17_capitulo_17.md)
- L75 ✘ «epochai2024» se declara sin verificar (02_capitulo_2.md)
- L83 ✘ «globaltimes2026» se declara sin verificar (17_capitulo_17.md)
- L87 ✘ «googledeepmind2024» se declara sin verificar (23_capitulo_23.md)
- L96 ✘ «govtechsg2024» se declara sin verificar (11_capitulo_11.md)
- L117 ✘ «idrcunesco2023» se declara sin verificar (20_capitulo_20.md)
- L121 ✘ «jerald2009» se declara sin verificar (32_capitulo_32.md)
- L130 ✘ «khanacademy2024» se declara sin verificar (10_capitulo_10.md)
- L151 ✘ «meta2024» se declara sin verificar (32_capitulo_32.md)
- L163 ✘ «chinamem2026» se declara sin verificar (17_capitulo_17.md)
- … y 4 más en `dist/AUDIT.json`

**`vol3-madurez-organizacional/referencias/referencias.md`**

- L16 ✘ «acp2026» se declara sin verificar (03_capitulo_3.md)
- L49 ✘ «cenepred2017» se declara sin verificar (03_capitulo_3.md)
- L53 ✘ «chase2025» se declara sin verificar (02_capitulo_2.md)
- L65 ✘ «digitalai2024» se declara sin verificar (25_capitulo_25.md)
- L146 ✘ «msresearch2023» se declara sin verificar (11_capitulo_11.md)
- L150 ✘ «mitchell2025» se declara sin verificar (02_capitulo_2.md)
- L158 ✘ «noaa2026» se declara sin verificar (03_capitulo_3.md)

**`vol4-patrones-de-escala/referencias/referencias.md`**

- L8 ✘ «clineanthropic2024» se declara sin verificar (10_capitulo_10.md)
- L12 ✘ «aspuru2024» se declara sin verificar (10_capitulo_10.md)
- L20 ✘ «bloomberg2025» se declara sin verificar (10_capitulo_10.md)
- L73 ✘ «langchain2024» se declara sin verificar (10_capitulo_10.md)
- L77 ✘ «lis2025» se declara sin verificar (10_capitulo_10.md)
- L101 ✘ «nvidia2024» se declara sin verificar (10_capitulo_10.md)
- L135 ✘ «syssec2025» se declara sin verificar (10_capitulo_10.md)


## C3 · cifras sin origen declarado (263)

**`vol1-fundamentos/manuscrito/capitulos/02_capitulo_2.md`**

- L31 ! cifra sin origen declarado: «4.000 tokens» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L124 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L126 ! cifra sin origen declarado: «94 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol1-fundamentos/manuscrito/capitulos/03_capitulo_3.md`**

- L248 ! cifra sin origen declarado: «30 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol1-fundamentos/manuscrito/capitulos/04_capitulo_4.md`**

- L190 ! cifra sin origen declarado: «95 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L238 ! cifra sin origen declarado: «500 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol1-fundamentos/manuscrito/capitulos/08_capitulo_8.md`**

- L519 ! cifra sin origen declarado: «18.000 tokens» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol1-fundamentos/manuscrito/capitulos/09_capitulo_9.md`**

- L238 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/01_capitulo_1.md`**

- L76 ! cifra sin origen declarado: «67%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/02_capitulo_2.md`**

- L74 ! cifra sin origen declarado: «55%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/03_capitulo_3.md`**

- L17 ! cifra sin origen declarado: «26%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L86 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L94 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/04_capitulo_4.md`**

- L65 ! cifra sin origen declarado: «200 milisegundos» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/07_capitulo_7.md`**

- L25 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/09_capitulo_9.md`**

- L19 ! cifra sin origen declarado: «200.000 tokens» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L277 ! cifra sin origen declarado: «0.5%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/10_capitulo_10.md`**

- L101 ! cifra sin origen declarado: «18%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/11_capitulo_11.md`**

- L19 ! cifra sin origen declarado: «99.999%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L88 ! cifra sin origen declarado: «15%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L90 ! cifra sin origen declarado: «21%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L92 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/12_capitulo_12.md`**

- L9 ! cifra sin origen declarado: «60%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L40 ! cifra sin origen declarado: «5ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L45 ! cifra sin origen declarado: «5ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L50 ! cifra sin origen declarado: «500ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L82 ! cifra sin origen declarado: «$4» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L86 ! cifra sin origen declarado: «10ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L114 ! cifra sin origen declarado: «99.95%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L123 ! cifra sin origen declarado: «60%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L131 ! cifra sin origen declarado: «$4» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/13_capitulo_13.md`**

- L17 ! cifra sin origen declarado: «40 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L65 ! cifra sin origen declarado: «30%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L89 ! cifra sin origen declarado: «4,7 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/14_capitulo_14.md`**

- L72 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/16_capitulo_16.md`**

- L34 ! cifra sin origen declarado: «90 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L55 ! cifra sin origen declarado: «90 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L59 ! cifra sin origen declarado: «90 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/17_capitulo_17.md`**

- L3 ! cifra sin origen declarado: «$6» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L19 ! cifra sin origen declarado: «60 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L55 ! cifra sin origen declarado: «60 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L86 ! cifra sin origen declarado: «35 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/18_capitulo_18.md`**

- L9 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L35 ! cifra sin origen declarado: «54 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L56 ! cifra sin origen declarado: «$9» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/19_capitulo_19.md`**

- L62 ! cifra sin origen declarado: «18 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L68 ! cifra sin origen declarado: «34 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/20_capitulo_20.md`**

- L16 ! cifra sin origen declarado: «51 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L18 ! cifra sin origen declarado: «50 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L45 ! cifra sin origen declarado: «120 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L54 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/21_capitulo_21.md`**

- L32 ! cifra sin origen declarado: «100 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L37 ! cifra sin origen declarado: «15 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L76 ! cifra sin origen declarado: «47 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/22_capitulo_22.md`**

- L44 ! cifra sin origen declarado: «1.4 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/23_capitulo_23.md`**

- L7 ! cifra sin origen declarado: «92 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L15 ! cifra sin origen declarado: «200 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L39 ! cifra sin origen declarado: «37 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L43 ! cifra sin origen declarado: «92 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L53 ! cifra sin origen declarado: «92 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/24_capitulo_24.md`**

- L7 ! cifra sin origen declarado: «92%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L13 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L17 ! cifra sin origen declarado: «50ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L21 ! cifra sin origen declarado: «20%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L23 ! cifra sin origen declarado: «50ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L34 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L42 ! cifra sin origen declarado: «92%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/25_capitulo_25.md`**

- L9 ! cifra sin origen declarado: «33%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L25 ! cifra sin origen declarado: «5ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L36 ! cifra sin origen declarado: «1ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L38 ! cifra sin origen declarado: «$3» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L53 ! cifra sin origen declarado: «$3» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L57 ! cifra sin origen declarado: «33%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/26_capitulo_26.md`**

- L37 ! cifra sin origen declarado: «92%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/27_capitulo_27.md`**

- L85 ! cifra sin origen declarado: «30%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/28_capitulo_28.md`**

- L19 ! cifra sin origen declarado: «50.000 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L30 ! cifra sin origen declarado: «40 milisegundos» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/29_capitulo_29.md`**

- L72 ! cifra sin origen declarado: «55%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L82 ! cifra sin origen declarado: «55.8%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L88 ! cifra sin origen declarado: «55%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/30_capitulo_30.md`**

- L82 ! cifra sin origen declarado: «$2» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/31_capitulo_31.md`**

- L52 ! cifra sin origen declarado: «100ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L117 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md`**

- L19 ! cifra sin origen declarado: «15 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L21 ! cifra sin origen declarado: «80 GB» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L117 ! cifra sin origen declarado: «4%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L119 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L127 ! cifra sin origen declarado: «5 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L206 ! cifra sin origen declarado: «18 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L210 ! cifra sin origen declarado: «2%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L229 ! cifra sin origen declarado: «18%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L247 ! cifra sin origen declarado: «16,67 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L446 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L459 ! cifra sin origen declarado: «35%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L467 ! cifra sin origen declarado: «20 ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- … y 7 más en `dist/AUDIT.json`

**`vol3-madurez-organizacional/manuscrito/capitulos/01_capitulo_1.md`**

- L5 ! cifra sin origen declarado: «99 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L191 ! cifra sin origen declarado: «6 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L211 ! cifra sin origen declarado: «7 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/03_capitulo_3.md`**

- L69 ! cifra sin origen declarado: «0.0195 ×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L102 ! cifra sin origen declarado: «90%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L121 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/04_capitulo_4.md`**

- L33 ! cifra sin origen declarado: «99.5%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L145 ! cifra sin origen declarado: «97%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/05_capitulo_5.md`**

- L11 ! cifra sin origen declarado: «73%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L13 ! cifra sin origen declarado: «20%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L23 ! cifra sin origen declarado: «68%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L27 ! cifra sin origen declarado: «63%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L29 ! cifra sin origen declarado: «70%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L96 ! cifra sin origen declarado: «15%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L164 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L166 ! cifra sin origen declarado: «30%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L188 ! cifra sin origen declarado: «6×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L201 ! cifra sin origen declarado: «0.03%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L209 ! cifra sin origen declarado: «10%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L213 ! cifra sin origen declarado: «0.03%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/06_capitulo_6.md`**

- L13 ! cifra sin origen declarado: «23%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L150 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L189 ! cifra sin origen declarado: «10%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L195 ! cifra sin origen declarado: «10%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L202 ! cifra sin origen declarado: «66%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L209 ! cifra sin origen declarado: «80%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L224 ! cifra sin origen declarado: «71%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/07_capitulo_7.md`**

- L11 ! cifra sin origen declarado: «70%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L37 ! cifra sin origen declarado: «29%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L49 ! cifra sin origen declarado: «23%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L51 ! cifra sin origen declarado: «$3» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L111 ! cifra sin origen declarado: «30%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L115 ! cifra sin origen declarado: «4.5×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L140 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L203 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/08_capitulo_8.md`**

- L41 ! cifra sin origen declarado: «85%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L76 ! cifra sin origen declarado: «85%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/09_capitulo_9.md`**

- L57 ! cifra sin origen declarado: «60%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/10_capitulo_10.md`**

- L9 ! cifra sin origen declarado: «55%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L68 ! cifra sin origen declarado: «70%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L97 ! cifra sin origen declarado: «55%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/11_capitulo_11.md`**

- L9 ! cifra sin origen declarado: «20%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L27 ! cifra sin origen declarado: «90%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L80 ! cifra sin origen declarado: «70%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/12_capitulo_12.md`**

- L21 ! cifra sin origen declarado: «183%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L31 ! cifra sin origen declarado: «184%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L35 ! cifra sin origen declarado: «10 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L62 ! cifra sin origen declarado: «60%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/14_capitulo_14.md`**

- L17 ! cifra sin origen declarado: «5%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L19 ! cifra sin origen declarado: «80%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L21 ! cifra sin origen declarado: «18%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/15_capitulo_15.md`**

- L197 ! cifra sin origen declarado: «100%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/16_capitulo_16.md`**

- L190 ! cifra sin origen declarado: «10%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/19_capitulo_19.md`**

- L31 ! cifra sin origen declarado: «$4» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L37 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/20_capitulo_20.md`**

- L40 ! cifra sin origen declarado: «20%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L50 ! cifra sin origen declarado: «73%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L68 ! cifra sin origen declarado: «12%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L78 ! cifra sin origen declarado: «95 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/21_capitulo_21.md`**

- L19 ! cifra sin origen declarado: «0,1%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L21 ! cifra sin origen declarado: «0,1%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L23 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L76 ! cifra sin origen declarado: «85%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/22_capitulo_22.md`**

- L17 ! cifra sin origen declarado: «56%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L39 ! cifra sin origen declarado: «30%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L63 ! cifra sin origen declarado: «47%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L74 ! cifra sin origen declarado: «68%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L78 ! cifra sin origen declarado: «68%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/23_capitulo_23.md`**

- L17 ! cifra sin origen declarado: «34%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L19 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L73 ! cifra sin origen declarado: «31%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L83 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/24_capitulo_24.md`**

- L11 ! cifra sin origen declarado: «2,3 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L27 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L45 ! cifra sin origen declarado: «2000ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L79 ! cifra sin origen declarado: «3,7 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L96 ! cifra sin origen declarado: «7 veces» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol3-madurez-organizacional/manuscrito/capitulos/25_capitulo_25.md`**

- L7 ! cifra sin origen declarado: «71%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L69 ! cifra sin origen declarado: «60 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L71 ! cifra sin origen declarado: «$2» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/01_capitulo_1.md`**

- L31 ! cifra sin origen declarado: «50 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L126 ! cifra sin origen declarado: «60 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L133 ! cifra sin origen declarado: «90.000 tokens» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/02_capitulo_2.md`**

- L9 ! cifra sin origen declarado: «85 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L123 ! cifra sin origen declarado: «$0» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L125 ! cifra sin origen declarado: «2.000 ×» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/03_capitulo_3.md`**

- L142 ! cifra sin origen declarado: «20 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/05_capitulo_5.md`**

- L85 ! cifra sin origen declarado: «70 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L152 ! cifra sin origen declarado: «80%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/06_capitulo_6.md`**

- L242 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/07_capitulo_7.md`**

- L128 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/08_capitulo_8.md`**

- L74 ! cifra sin origen declarado: «10 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L121 ! cifra sin origen declarado: «50 %» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/09_capitulo_9.md`**

- L5 ! cifra sin origen declarado: «80 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L7 ! cifra sin origen declarado: «38 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L11 ! cifra sin origen declarado: «82.3 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L40 ! cifra sin origen declarado: «12 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L94 ! cifra sin origen declarado: «$2» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L107 ! cifra sin origen declarado: «$4» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L109 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L134 ! cifra sin origen declarado: «80 %» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L497 ! cifra sin origen declarado: «$8» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L545 ! cifra sin origen declarado: «dólares» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L557 ! cifra sin origen declarado: «$2» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md`**

- L148 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L154 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L156 ! cifra sin origen declarado: «90%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L162 ! cifra sin origen declarado: «100ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L168 ! cifra sin origen declarado: «3×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L170 ! cifra sin origen declarado: «8×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L188 ! cifra sin origen declarado: «50ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L190 ! cifra sin origen declarado: «100ms» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L200 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L202 ! cifra sin origen declarado: «$7» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L211 ! cifra sin origen declarado: «$0» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L217 ! cifra sin origen declarado: «95%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- … y 17 más en `dist/AUDIT.json`

**`vol4-patrones-de-escala/manuscrito/capitulos/11_capitulo_11.md`**

- L244 ! cifra sin origen declarado: «92%» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/12_capitulo_12.md`**

- L11 ! cifra sin origen declarado: «1,000 tokens» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L100 ! cifra sin origen declarado: «6×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L106 ! cifra sin origen declarado: «80%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L144 ! cifra sin origen declarado: «80%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L154 ! cifra sin origen declarado: «$0» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L158 ! cifra sin origen declarado: «88%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L188 ! cifra sin origen declarado: «50×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L198 ! cifra sin origen declarado: «14×» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L209 ! cifra sin origen declarado: «$0» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L215 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L221 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L304 ! cifra sin origen declarado: «$2» — marcar [D] dato, [E] estimación o [I] ilustrativa

**`vol4-patrones-de-escala/manuscrito/capitulos/13_capitulo_13.md`**

- L58 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L64 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L68 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L388 ! cifra sin origen declarado: «$8» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L435 ! cifra sin origen declarado: «34%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L769 ! cifra sin origen declarado: «35%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L771 ! cifra sin origen declarado: «$1» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L778 ! cifra sin origen declarado: «38%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L803 ! cifra sin origen declarado: «40%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L805 ! cifra sin origen declarado: «$4» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L811 ! cifra sin origen declarado: «85%» — marcar [D] dato, [E] estimación o [I] ilustrativa
- L924 ! cifra sin origen declarado: «$5» — marcar [D] dato, [E] estimación o [I] ilustrativa
- … y 2 más en `dist/AUDIT.json`

**`vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md`**

- L257 ! cifra sin origen declarado: «60%» — marcar [D] dato, [E] estimación o [I] ilustrativa


## C4 · apéndices y marcadores pendientes (14)

**`vol1-fundamentos/front-matter/03_hoja_creditos.md`**

- L13 ! marcador pendiente: «PENDIENTE]»
- L14 ! marcador pendiente: «PENDIENTE]»

**`vol1-fundamentos/manuscrito/capitulos/04_capitulo_4.md`**

- L40 ! marcador pendiente: «TODO»

**`vol2-frontera-y-aplicaciones/front-matter/03_hoja_creditos.md`**

- L13 ! marcador pendiente: «PENDIENTE]»
- L14 ! marcador pendiente: «PENDIENTE]»

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/12_capitulo_12.md`**

- L83 ! marcador pendiente: «TODO»
- L84 ! marcador pendiente: «TODO»

**`vol3-madurez-organizacional/front-matter/03_hoja_creditos.md`**

- L13 ! marcador pendiente: «PENDIENTE]»
- L14 ! marcador pendiente: «PENDIENTE]»

**`vol4-patrones-de-escala/front-matter/03_hoja_creditos.md`**

- L13 ! marcador pendiente: «PENDIENTE]»
- L14 ! marcador pendiente: «PENDIENTE]»

**`vol4-patrones-de-escala/manuscrito/capitulos/09_capitulo_9.md`**

- L204 ! marcador pendiente: «PENDIENTE).build();»
- L214 ! marcador pendiente: «PENDIENTE);»
- L363 ! marcador pendiente: «PENDIENTE' }));»


## C7 · presupuesto de palabras (23)

**`vol1-fundamentos/manuscrito/capitulos/03_capitulo_3.md`**

- L1 ! 1184 palabras (mínimo 1600): capítulo corto

**`vol1-fundamentos/manuscrito/capitulos/06_capitulo_6.md`**

- L1 ! 1139 palabras (mínimo 1600): capítulo corto

**`vol1-fundamentos/manuscrito/capitulos/07_capitulo_7.md`**

- L1 ! 929 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/15_capitulo_15.md`**

- L1 ! 1380 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/16_capitulo_16.md`**

- L1 ! 1382 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/19_capitulo_19.md`**

- L1 ! 1592 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/20_capitulo_20.md`**

- L1 ! 1529 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/21_capitulo_21.md`**

- L1 ! 1477 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/22_capitulo_22.md`**

- L1 ! 1443 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/23_capitulo_23.md`**

- L1 ! 1398 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/24_capitulo_24.md`**

- L1 ! 972 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/25_capitulo_25.md`**

- L1 ! 1025 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/26_capitulo_26.md`**

- L1 ! 1015 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/29_capitulo_29.md`**

- L1 ! 1423 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/30_capitulo_30.md`**

- L1 ! 1553 palabras (mínimo 1600): capítulo corto

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md`**

- L1 ! 4606 palabras (máximo 4500): considerar dividirlo

**`vol3-madurez-organizacional/manuscrito/capitulos/16_capitulo_16.md`**

- L1 ! 1476 palabras (mínimo 1600): capítulo corto

**`vol4-patrones-de-escala/manuscrito/capitulos/02_capitulo_2.md`**

- L1 ! 946 palabras (mínimo 1600): capítulo corto

**`vol4-patrones-de-escala/manuscrito/capitulos/03_capitulo_3.md`**

- L1 ! 954 palabras (mínimo 1600): capítulo corto

**`vol4-patrones-de-escala/manuscrito/capitulos/04_capitulo_4.md`**

- L1 ! 1167 palabras (mínimo 1600): capítulo corto

**`vol4-patrones-de-escala/manuscrito/capitulos/05_capitulo_5.md`**

- L1 ! 4904 palabras (máximo 4500): considerar dividirlo

**`vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md`**

- L1 ! 7426 palabras (máximo 4500): considerar dividirlo

**`vol4-patrones-de-escala/manuscrito/capitulos/13_capitulo_13.md`**

- L1 ! 5372 palabras (máximo 4500): considerar dividirlo


## C9 · carpetas de imágenes (13)

**`vol2-frontera-y-aplicaciones/manuscrito/imagenes/capitulo29`**

- L1 ! `capitulo29` guarda la numeración antigua: lo usa el cap. 1 de este volumen

**`vol2-frontera-y-aplicaciones/manuscrito/imagenes/capitulo60`**

- L1 ! `capitulo60` guarda la numeración antigua: lo usa el cap. 13 de este volumen

**`vol2-frontera-y-aplicaciones/manuscrito/imagenes/capitulo76`**

- L1 ! `capitulo76` guarda la numeración antigua: lo usa el cap. 29 de este volumen

**`vol2-frontera-y-aplicaciones/manuscrito/imagenes/capitulo77`**

- L1 ! `capitulo77` guarda la numeración antigua: lo usa el cap. 30 de este volumen

**`vol2-frontera-y-aplicaciones/manuscrito/imagenes/capitulo78`**

- L1 ! `capitulo78` guarda la numeración antigua: lo usa el cap. 31 de este volumen

**`vol3-madurez-organizacional/manuscrito/imagenes/capitulo16`**

- L1 ! `capitulo16` guarda la numeración antigua: lo usa el cap. 2 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo10`**

- L1 ! `capitulo10` guarda la numeración antigua: lo usa el cap. 1 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo13`**

- L1 ! `capitulo13` guarda la numeración antigua: lo usa el cap. 4 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo14`**

- L1 ! `capitulo14` guarda la numeración antigua: lo usa el cap. 5 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo15`**

- L1 ! `capitulo15` guarda la numeración antigua: lo usa el cap. 6 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo16`**

- L1 ! `capitulo16` guarda la numeración antigua: lo usa el cap. 6, 7 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo17`**

- L1 ! `capitulo17` guarda la numeración antigua: lo usa el cap. 7 de este volumen

**`vol4-patrones-de-escala/manuscrito/imagenes/capitulo80`**

- L1 ! `capitulo80` guarda la numeración antigua: lo usa el cap. 13 de este volumen


## C11 · año de la cita (1)

**`vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md`**

- L271 ✘ la cita dice 2023 y la entrada «unity2023» es de 2020, 2025

