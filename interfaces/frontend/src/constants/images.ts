// src/constants/images.ts

/**
 * SILA - Sistema Integrado de Logística de Angola
 * Mapeamento centralizado de assets para garantir consistência visual.
 * 
 * NOTA: Este arquivo consolida TODAS as imagens da aplicação. 
 * Evite importações diretas de imagens nos componentes.
 */

import brandLogo from '../assets/images/brand-logo-sila.webp';
import govInsigniaColor from '../assets/images/gov-insignia-color.webp';
import govInsigniaGold from '../assets/images/gov-insignia-gold.webp';
import authBgCitizen from '../assets/images/auth-bg-citizen.webp';
import authBgAdmin from '../assets/images/auth-bg-admin.webp';
import geoNational from '../assets/images/geo-level-national.webp';
import geoProvincial from '../assets/images/geo-level-provincial.webp';
import geoMunicipal from '../assets/images/geo-level-municipal.webp';
import heroCitizen from '../assets/images/dashboard-citizen-hero.webp';
import featureWallet from '../assets/images/feature-digital-wallet.webp';

/**
 * Objeto único e centralizado contendo todas as imagens da aplicação.
 * Estruturado por contexto de uso para melhor organização e autocomplete.
 */
export const IMAGES = {
  // Branding e Identidade Visual
  BRAND: {
    LOGO: brandLogo,
    INSIGNIA: govInsigniaColor,
    INSIGNIA_ALT: govInsigniaGold,
  },
  
  // Autenticação e Segurança
  AUTH: {
    CITIZEN_BG: authBgCitizen,
    ADMIN_BG: authBgAdmin,
  },
  
  // Níveis de Administração Geográfica
  GEO_LEVELS: {
    NATIONAL: geoNational,
    PROVINCIAL: geoProvincial,
    MUNICIPAL: geoMunicipal,
  },
  
  // Dashboard e Portais
  DASHBOARD: {
    HERO: heroCitizen,
    WALLET: featureWallet,
  }
} as const;

export default IMAGES;
