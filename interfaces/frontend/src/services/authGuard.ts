/**
 * Sistema de proteção de rotas baseado em papel
 * Redireciona automaticamente para o dashboard correto
 */

import { authService } from './authService';

export interface RouteGuardResult {
    allowed: boolean;
    redirectTo?: string;
    role?: string;
    message?: string;
}

class AuthGuard {
    /**
     * Verifica se o user pode aceder à rota atual
     * Se não puder, retorna para onde deve redirecionar
     */
    async checkRouteAccess(currentPath: string): Promise<RouteGuardResult> {
        try {
            // 1. Verificar se está autenticado
            const user = await authService.getMe();
            if (!user) {
                return {
                    allowed: false,
                    redirectTo: '/login',
                    message: 'Faça login para continuar'
                };
            }

            // 3. Mapa de rotas por papel (matching backend roles)
            const roleRoutes: Record<string, string[]> = {
                ADMIN_SUPER: ['/admin', '/'],
                ADMIN_CENTRAL: ['/admin', '/'],
                ADMIN_PROVINCIAL: ['/admin', '/'],
                ADMIN_MUNICIPAL: ['/admin', '/'],
                ADMIN_COMMUNAL: ['/admin', '/'],
                CITIZEN: ['/citizen', '/profile', '/requests']
            };

            // 4. Mapa de dashboards por papel
            const roleDashboards: Record<string, string> = {
                ADMIN_SUPER: '/admin',
                ADMIN_CENTRAL: '/admin',
                ADMIN_PROVINCIAL: '/admin',
                ADMIN_MUNICIPAL: '/admin',
                ADMIN_COMMUNAL: '/admin',
                CITIZEN: '/citizen/portal'
            };

            const role = user.role;
            const allowedPrefixes = roleRoutes[role] || [];

            // 5. Verificar se a rota atual é permitida
            const isAllowed = allowedPrefixes.some(prefix =>
                currentPath.startsWith(prefix)
            );

            if (!isAllowed) {
                // Rota não permitida → redirecionar para dashboard correto
                return {
                    allowed: false,
                    redirectTo: roleDashboards[role] || '/login',
                    role,
                    message: `Redirecionando para o seu dashboard de ${role}`
                };
            }

            // 6. Tudo OK
            return {
                allowed: true,
                role
            };

        } catch (error) {
            console.error('Erro no auth guard:', error);
            return {
                allowed: false,
                redirectTo: '/login',
                message: 'Erro de autenticação'
            };
        }
    }

    /**
     * Versão síncrona para uso em componentes
     */
    getDashboardForRole(role: string): string {
        const dashboards: Record<string, string> = {
            ADMIN_SUPER: '/admin',
            ADMIN_CENTRAL: '/admin',
            ADMIN_PROVINCIAL: '/admin',
            ADMIN_MUNICIPAL: '/admin',
            ADMIN_COMMUNAL: '/admin',
            CITIZEN: '/citizen/portal'
        };
        return dashboards[role] || '/login';
    }
}

export const authGuard = new AuthGuard();
