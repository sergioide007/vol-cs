import { SITE } from './site.mjs';

// Aviso legal del pie. Borrador: revísalo con un abogado antes de publicar.
export const LEGAL = {
  es: {
    heading: 'Acceso abierto',
    body: `Esta obra se publica en acceso abierto: leerla en línea es gratuito y siempre lo será. ` +
      `Salvo indicación contraria, el texto se distribuye bajo la licencia <a href="${SITE.licenseUrl}" rel="license noopener">${SITE.licenseName}</a>: ` +
      `puedes compartirla y adaptarla citando la autoría, sin fines comerciales y con la misma licencia. ` +
      `Los fragmentos de código de ejemplo se ofrecen bajo licencia MIT. ` +
      `Si te ha sido útil, puedes apoyar al autor con un aporte voluntario: es una colaboración, no un pago por el acceso al contenido.`,
    support: 'Apoyo voluntario',
    donate: 'Donación puntual (Ko-fi)',
    patron: 'Membresía y mecenazgo (Patreon)',
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
      `If it has been useful, you can support the author with a voluntary contribution: it is a way to help, not a payment for access to the content.`,
    support: 'Voluntary support',
    donate: 'One-time donation (Ko-fi)',
    patron: 'Membership and patronage (Patreon)',
    marks: `“Synthetic Code” (“Código Sintético”) and “SpecSolid” are trademarks of ${SITE.author}; the license grants no rights over them or over the cover artwork.`,
    disclaimer: 'Content is provided “as is” for educational and technical purposes and is not legal, financial or professional advice. Prices, models and regulations cited change over time: see each volume’s currency note.',
    rights: `© 2026 ${SITE.author}.`,
  },
};
