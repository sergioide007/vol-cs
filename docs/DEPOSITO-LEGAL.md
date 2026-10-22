# Depósito Legal e ISBN por volumen (Perú, BNP)

Cada volumen × idioma es una **obra/edición distinta**: 4 volúmenes × 2 idiomas = 8 Depósitos Legales,
y un ISBN por cada formato (EPUB, PDF y, si existe, impreso) = 16 ISBN mínimo. Un ISBN no se reutiliza.

## Orden de trabajo (por volumen e idioma)
1. **ISBN** — solicitarlo a la Agencia Peruana del ISBN (BNP) antes de publicar; uno por formato e idioma.
2. **Depósito Legal** — en **SIRNADEL** (BNP), *antes* de publicar. Es gratuito y entrega el nº de registro.
3. Rellenar `legal/registry.yaml` (ISBN, `deposito_legal`, `edition_date` AAAA-MM, `edition`, domicilio).
4. `python3 tools/render_legal.py --strict` → debe terminar sin PENDIENTE ni errores.
5. `git tag vX.Y.Z` → el CI compone ES+EN, valida y publica la release con `SHA256SUMS`.
6. **Entrega a la BNP**: subir por SIRNADEL **una** versión final del libro electrónico dentro de los
   **90 días hábiles** contados desde el último día hábil del mes y año de la edición.
7. Publicar en plataformas (KDP, Google Play Books, Lulu) y pegar los enlaces en el registro
   (`kdp`, `google_play`, `lulu`); `render_info_site.py` los convierte en botones.

## Qué debe llevar la hoja de créditos (la genera `render_legal.py`)
Título · nº de edición · **mes y año** de edición · todos los autores · razón social y **domicilio legal**
del editor · nº de Depósito Legal. En e-books no son obligatorios impresor ni tiraje; en la edición
impresa sí (`printer`). El DNI no es obligatorio (`publisher_id` vacío = no se imprime).

## Coherencia que el build comprueba solo
- ISBN-13 con dígito de control correcto y sin repetir; Depósito Legal `AAAA-NNNNN`; fecha `AAAA-MM`.
- Los autores del registro = los de la leyenda de cubierta (`tools/covers/cover-design.json`).
- El dominio citado = `web/site.config.json`.
- Revisar a mano: el **título de la cubierta** debe coincidir con el título registrado
  (p. ej. cubierta EN «Fundamentals» vs. `vols.json` «Foundations»).

## Web por volúmenes
`python3 tools/render_info_site.py --info <repo info-codigo-sintetico> --out dist/info-site`
genera hub ES/EN + una página por volumen y conserva el libro 1 en `/libro-1/`.
Verifica antes de publicar que no se muestre ningún dato personal que no quieras hacer público.

Fuentes: Ley 31253 y los trámites «Solicitar la constancia de depósito legal» en gob.pe / bnp.gob.pe.
Los requisitos cambian: confirmar en SIRNADEL antes de cada release.
