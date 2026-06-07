import React, { useEffect, useMemo } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import type { User } from '@/types';
import { authService } from '@/services/authService';
import { UserRole } from '@/types';

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole?: string[];
    user: User | null;
}

const RedirectNotice: React.FC<{ to: string; areaLabel: string }> = ({ to, areaLabel }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const t = setTimeout(() => navigate(to, { replace: true }), 1400);
        return () => clearTimeout(t);
    }, [navigate, to]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
            <div className="max-w-md text-center space-y-3">
                <div className="text-sm uppercase tracking-[0.2em] text-slate-400">Acesso Restrito</div>
                <h1 className="text-xl font-bold">Você está tentando acessar a {areaLabel}.</h1>
                <p className="text-sm text-slate-300">Redirecionando para o login correto...</p>
            </div>
        </div>
    );
};

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
    children,
    requiredRole,
    user
}) => {
    // Verificar acesso usando o user do parent (App.tsx)
    const isAllowed = useMemo(() => {
        if (!user) {
            return false;
        }

        // Se requiredRole foi especificado, verificar se o user possui um dos roles
        if (requiredRole && requiredRole.length > 0) {
            return requiredRole.includes(user.role);
        }

        // Caso contrário, apenas verificar se está autenticado
        return true;
    }, [user, requiredRole]);

    // Se não está autenticado ou role não é permitido, redirecionar
    if (!isAllowed) {
        if (!user) {
            const fallback = requiredRole?.includes(UserRole.CITIZEN) ? '/citizen/login' : '/login';
            return <Navigate to={fallback} replace />;
        }

        // Usuário autenticado mas role não é permitido - forçar logout e redirecionar
        const isCitizenArea = requiredRole?.includes(UserRole.CITIZEN) ?? false;
        const fallback = isCitizenArea ? '/citizen/login' : '/login';
        const areaLabel = isCitizenArea ? 'Área do Cidadão' : 'Área Administrativa';
        localStorage.clear();
        return <RedirectNotice to={fallback} areaLabel={areaLabel} />;
    }

    // Acesso permitido - renderizar children
    return <>{children}</>;
};
