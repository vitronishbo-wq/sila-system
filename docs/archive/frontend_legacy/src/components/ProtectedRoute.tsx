import React, { useMemo } from 'react';
import { Navigate } from 'react-router-dom';
import type { User } from '../types';
import { authService } from '../services/authService';

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole?: string[];
    user: User | null;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
    children,
    requiredRole,
    user
}) => {
    const resolvedRole = authService.getUserRole(user);

    // Verificar acesso usando o user do parent (App.tsx)
    const isAllowed = useMemo(() => {
        if (!user) {
            return false;
        }

        if (!resolvedRole) {
            return false;
        }

        // Se requiredRole foi especificado, verificar se o user possui um dos roles
        if (requiredRole && requiredRole.length > 0) {
            return requiredRole.includes(resolvedRole);
        }

        // Caso contrário, apenas verificar se está autenticado
        return true;
    }, [user, requiredRole, resolvedRole]);

    // Se não está autenticado ou role não é permitido, redirecionar
    if (!isAllowed) {
        if (!user) {
            return <Navigate to="/login" replace />;
        }

        // Usuário autenticado mas role não é permitido - redirecionar para seu dashboard
        const dashboard = authService.getDashboardForRole(user);
        return <Navigate to={dashboard} replace />;
    }

    // Acesso permitido - renderizar children
    return <>{children}</>;
};
