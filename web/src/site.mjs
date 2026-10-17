// Datos "de negocio" del sitio: se editan en web/site.config.json (lo lee también tools/web_sync.py).
import cfg from '../site.config.json';
export const SITE = cfg;
export const buyEnabled = !String(cfg.buyUrl).startsWith('PENDIENTE');
