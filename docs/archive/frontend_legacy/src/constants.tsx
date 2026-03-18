import IMAGES from './constants/images';

export const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api').replace(/\/?$/, '/');
export const APP_VERSION = '2026.1';

/**
 * Serviços essenciais do SILA disponíveis para cidadãos.
 * Este objeto define o menu principal de serviços públicos.
 */
export const ESSENTIAL_SERVICES = [
  { id: 'identity', name: 'Identidade Civil', icon: 'fa-id-card', color: 'bg-blue-500' },
  { id: 'registry', name: 'Registo Civil', icon: 'fa-book', color: 'bg-green-500' },
  { id: 'tax', name: 'Contribuinte (AGT)', icon: 'fa-receipt', color: 'bg-yellow-500' },
  { id: 'water', name: 'Água e Saneamento', icon: 'fa-droplet', color: 'bg-cyan-500' },
  { id: 'energy', name: 'Energia Elétrica', icon: 'fa-bolt', color: 'bg-orange-500' },
  { id: 'employment', name: 'Emprego e Trabalho', icon: 'fa-briefcase', color: 'bg-purple-500' },
  { id: 'licensing', name: 'Licenciamento', icon: 'fa-file-signature', color: 'bg-red-500' },
  { id: 'transport', name: 'Transportes', icon: 'fa-bus', color: 'bg-emerald-500' },
  { id: 'notaries', name: 'Cartórios e Notariado', icon: 'fa-stamp', color: 'bg-indigo-500' }
];

// Re-export IMAGES para compatibilidade
export { IMAGES } from './constants/images';
