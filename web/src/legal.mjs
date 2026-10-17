import { SITE } from './site.mjs';

// Aviso legal del pie. Borrador: revísalo con un abogado antes de publicar.
export const LEGAL = {
  es: {
    heading: 'Acceso abierto',
    body: `Esta obra se publica en acceso abierto: leerla en línea es gratuito y siempre lo será. ` +
      `Salvo indicación contraria, el texto se distribuye bajo la licencia <a href="${SITE.licenseUrl}" rel="license noopener">${SITE.licenseName}</a>: ` +
      `puedes compartirla y adaptarla citando la autoría, sin fines comerciales y con la misma licencia. ` +
      `Los fragmentos de código de ejemplo se ofrecen bajo licencia MIT. ` +
      `Las ediciones empaquetadas (PDF compilado, EPUB, Kindle e impresión bajo demanda) son opcionales y tienen un precio de referencia de ${SITE.price} ${SITE.currency}: ` +
      `quien las adquiere paga el formato y apoya el proyecto, no el acceso al contenido.`,
    support: 'Apoyar el proyecto / obtener las ediciones',
    marks: `«Código Sintético» y «SpecSolid» son marcas de ${SITE.author}; la licencia no concede derechos sobre ellas ni sobre las cubiertas.`,
    disclaimer: 'El contenido se ofrece «tal cual», con fines educativos y técnicos; no constituye asesoría legal, financiera ni profesional. Precios, modelos y normativa citados cambian: consulta la nota de vigencia de cada volumen.',
    rights: `© 2026 ${SITE.author}.`,
  },
  en: {
    heading: 'Open access',
    body: `This work is published as open access: reading it online is free and always will be. ` +
      `Unless otherwise noted, the text is released under <a href="${SITE.licenseUrl}" rel="license noopener">${SITE.licenseName}</a>: ` +
      `you may share and adapt it with attribution, for non-commercial purposes, under the same license. ` +
      `Example code snippets are offered under the MIT license. ` +
      `Packaged editions (compiled PDF, EPUB, Kindle and print-on-demand) are optional, with a reference price of ${SITE.price} ${SITE.currency}: ` +
      `buyers pay for the format and support the project, not for access to the content.`,
    support: 'Support the project / get the packaged editions',
    marks: `“Synthetic Code” (“Código Sintético”) and “SpecSolid” are trademarks of ${SITE.author}; the license grants no rights over them or over the cover artwork.`,
    disclaimer: 'Content is provided “as is” for educational and technical purposes and is not legal, financial or professional advice. Prices, models and regulations cited change over time: see each volume’s currency note.',
    rights: `© 2026 ${SITE.author}.`,
  },
};
