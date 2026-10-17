// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const vols = JSON.parse(readFileSync(new URL('../tools/vols.json', import.meta.url), 'utf-8'));
const site = JSON.parse(readFileSync(new URL('./site.config.json', import.meta.url), 'utf-8'));

// Un grupo por volumen; dentro, tres subgrupos generados desde las carpetas.
const volumeGroup = (id) => {
  const n = id.replace('vol', '');
  return {
    label: `Vol. ${n} — ${vols.titles.es[id]}`,
    translations: { en: `Vol. ${n} — ${vols.titles.en[id]}` },
    collapsed: true,
    items: [
      { slug: id, label: 'Portada', translations: { en: 'Cover' } },
      { label: 'Preliminares', translations: { en: 'Front matter' }, collapsed: true,
        items: [{ autogenerate: { directory: `${id}/front` } }] },
      { label: 'Capítulos', translations: { en: 'Chapters' }, collapsed: true,
        items: [{ autogenerate: { directory: `${id}/chapters` } }] },
      { label: 'Apéndices y referencias', translations: { en: 'Appendices & references' }, collapsed: true,
        items: [{ autogenerate: { directory: `${id}/back` } }] },
    ],
  };
};

export default defineConfig({
  site: site.url,
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: { es: vols.series.es, en: vols.series.en },
      description: 'El arte de orquestar agentes de IA — obra técnica en cuatro volúmenes, en acceso abierto.',
      defaultLocale: 'es',
      locales: {
        es: { label: 'Español', lang: 'es' },
        en: { label: 'English', lang: 'en' },
      },
      social: [{ icon: 'github', label: 'GitHub', href: site.repo }],
      lastUpdated: false,
      customCss: ['./src/styles/custom.css'],
      components: { Footer: './src/components/Footer.astro' },
      sidebar: Object.keys(vols.slugs).map(volumeGroup),
      pagination: true,
      // Pagefind (búsqueda) viene activado por defecto y respeta el idioma.
    }),
  ],
});
