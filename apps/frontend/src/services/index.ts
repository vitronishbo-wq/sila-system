/**
 * 🛡️ GLOBAL SERVICES - RESTRICTED WHITELIST
 *
 * ⚠️ ONLY THESE THREE SERVICES ARE ALLOWED TO BE IMPORTED FROM @/services
 *
 * Any new service added to this folder is FORBIDDEN.
 * All new services MUST be in @/modules/*/services/*
 *
 * APPROVED SERVICES:
 * ✅ authService       - Authentication & token management
 * ✅ apiService        - HTTP abstraction layer
 * ✅ authGuard         - Route protection & role validation
 *
 * FORBIDDEN EXAMPLES:
 * ❌ operationsService    → must be in @/modules/operations/services
 * ❌ dashboardService     → must be in @/modules/admin/services
 * ❌ citizenAuthService   → deprecated, move to proper module
 * ❌ documentService      → deprecated, move to proper module
 *
 * RULE: If you need a new service, create a module for its bounded context
 * and place it in @/modules/[domain]/services/
 *
 * Compliance Level: ENTERPRISE - Zero violations tolerated
 */

export { authService } from '@/services/authService';
export { apiService } from '@/services/apiService';
export { authGuard } from '@/services/authGuard';

// 🚫 DO NOT ADD MORE EXPORTS HERE 🚫
