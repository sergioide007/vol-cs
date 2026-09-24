---
name: anti-cliches-ia
description: >
  Pasador editorial para manuscritos técnicos en español que elimina las marcas
  de prosa generada por IA (metadiscurso enfatico: "Merece enfasis que",
  "Conviene senalar", "Cabe destacar", "Importa destacar") y los tics
  estilo Wikipedia (remisiones metadiscursivas, conectores repetidos, lexico
  expansivo), sin tocar nunca tablas, codigo ni citas. Usalo tras escribir o
  traducir cualquier capitulo, y como auditoria periodica de la coleccion.
version: 1.0
---

# Skill: anti-clichés de IA y escritura tipo Wikipedia

## 1. Objetivo

Dejar la prosa en **voz de autor**, no en voz de plantilla. La prueba de
aceptación no es «no hay clichés», sino: *¿el lector percibe una persona
afirmando algo, o un modelo anunciando que va a afirmar algo?*

## 2. Protecciones duras (nunca se tocan)

El pasador debe **rechazar** cualquier cambio en:

| Zona | Patrón de protección |
|---|---|
| Bloques de código cercados | líneas con ``` o ~~~ (incluido el interior) |
| Código sangrado | líneas que empiezan por 4 espacios o tabulador |
| Tablas Markdown | líneas que empiezan por `\|` |
| Código en línea | segmentos entre acentos graves `...` |
| Citas bibliográficas | anclas `{#ref-...}` y enlaces `[...](#ref-...)` |
| Fórmulas | `$...$`, `$$...$$`, `\begin{...}` |
| Rutas y URLs | `/imagenes/`, `.png`, `http` |

Si una corrección sólo puede aplicarse sobre texto protegido, **se descarta y se
reporta**; nunca se fuerza.

## 3. Categorías y reglas

### 3.1 Metadiscurso enfático (marca principal de LLM)

Formas: `Merece énfasis que…`, `Merece énfasis particular…`, `Conviene señalar
que…`, `Conviene enfatizar…`, `Importa destacar que…`, `Cabe destacar que…`,
`Cabe precisar que…`, `No podemos dejar de…`, `Es fundamental recordar…`,
`Nótese que…`, `Recuerde que…`, `Sin duda`.

**Regla:** *eliminar el metadiscurso y enunciar el contenido directamente.*
El autor no anuncia la importancia de lo que va a decir; la importancia se
demuestra con la evidencia que sigue.

- ❌ «Merece énfasis que el ROI no es automático.»
- ✅ «El ROI no es automático.»
- ❌ «Conviene señalar que el relato oscila entre dos polos.»
- ✅ «El relato oscila entre dos polos.»
- ❌ «Importa destacar que esta transformación tiene implicaciones.»
- ✅ «Esta transformación tiene implicaciones directas.»

**Variante con contenido útil:** cuando la frase porte un matiz, se conserva la
 idea y se cambia el marco, no se borra el matiz.
- ❌ «Merece énfasis este hecho: ninguno fue ornamental.»
- ✅ «Ninguno fue ornamental.»

### 3.2 Fórmulas de identidad (negación binaria)

`No es X: es Y` / `No solo X, sino Y` / `No se trata de X, sino de Y`, repetidas
como muletilla retórica. Regla: conservar **una sola vez por sección** y solo si
aporta contraste real; en el resto, enunciar Y.

### 3.3 Léxico de grandilocuencia

`revolucionario`, `sin precedentes`, `panorama actual`, `pionero`, `innovador`,
`sin paralelo`, `de vanguardia`, `revoluciona`, `impulsado por la IA`,
`la clave está en`, `potenciar`, `empoderar`, `desbloquear`, `game-changer`.

**Regla:** sustituir por el dato verificable que el adjetivo sustituye. Si el
dato no existe, eliminar el adjetivo.
- ❌ «Inversión de magnitud sin precedentes: el ecosistema captó 97,4 B USD.»
- ✅ «Inversión de gran magnitud: el ecosistema captó 97,4 B USD.»
- ❌ «en la era de la IA / en la era de los agentes»
- ✅ «con los agentes» / «en sistemas agénticos»

### 3.4 Meta-referencia del texto (tic Wikipedia)

`En este trabajo…`, `En este capítulo…` repetido, `A lo largo de esta obra…`,
`Cabe mencionar que`, `Anteriormente` como conector.

**Regla:** el texto no debe comentar sobre sí mismo salvo en prólogo, guía de
lectura y epílogo (donde sí es función documental). En cuerpo, sustituir por la
referencia concreta («el capítulo 8», «el protocolo del apartado anterior»).

### 3.5 Densidad de conectores

`En consecuencia`, `Por consiguiente`, `No obstante`, `Por lo tanto`,
`Asimismo`, `De acuerdo con`, `Dado que`, `Es decir`, repetidos como muletilla
sintáctica. Son español legítimo: **no se eliminan en bloque**. Se corrige sólo
cuando (a) hay dos conectores equivalentes en la misma frase, o (b) el mismo
conector aparece más de 2 veces en un mismo párrafo.

### 3.6 Falsos positivos conocidos (NO tocar)

Estos disparan el detector pero son correctos en el contexto de esta obra:

- `¿Cuál es…?` en ejercicios, diálogos y guiones socráticos.
- `constituye una/un` como verbo técnico en densidad argumentativa.
- `vale la pena` en reglas de decisión («vale la pena solo si: (a)…»).
- `en última instancia` con función lógica real.
- **Terminología propia de la serie** (p. ej. «era agéntica»): es término
  definido por la obra, no cliché; sustituirlo sería un error terminológico.
- Preguntas retóricas de los cuadros de discusión crítica.

## 4. Procedimiento

1. **Detectar** con `tools/skill_cliches.py` (solo lectura).
2. **Clasificar** cada hallazgo: `FIX` (cliché real) / `KEEP` (legítimo).
3. **Reescribir** enunciando el contenido; nunca cambiar la afirmación técnica,
   las cifras, las citas ni el sentido argumental.
4. **Aplicar** con `tools/skill_aplicar.py`, que contiene el mapa curado y
   verifica que cada original aparezca **exactamente una vez**.
5. **Verificar**: re-ejecutar el detector (los FIX deben bajar a 0), comprobar
   con `git diff` que ninguna línea protegida cambió, y reconstruir.

## 5. Criterio de no-reescritura

Si la frase es clara, técnica y propia, **se deja**. La consigna no es
uniformizar el libro, sino quitar la voz ajena. Sobreeeditar un buen párrafo es
un error editorial tan grave como dejar un cliché.
