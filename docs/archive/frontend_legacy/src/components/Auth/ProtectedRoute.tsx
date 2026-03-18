import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import type { AdminLevel } from '@/types/auth';
import { useEffect } from 'react';

interface ProtectedRouteProps {
    allowedLevels?: AdminLevel[];
}

const levelThemeClass: Record<AdminLevel, string> = {
    CENTRAL: 'theme-central',
    PROVINCIAL: 'theme-provincial',
    LOCAL: 'theme-municipal',
};

export const ProtectedRoute = ({ allowedLevels }: ProtectedRouteProps) => {
    const { isAuthenticated, user, isLoading: authLoading, fetchUser } = useAuthStore();
    const location = useLocation();

    const token = localStorage.getItem('access_token');
    const isActuallyLoading = authLoading || (token && !user && !isAuthenticated);

    useEffect(() => {
        if (!user?.administrative_level) return;

        const newClass = levelThemeClass[user.administrative_level];
        document.body.classList.add(newClass);

        return () => {
            document.body.classList.remove(newClass);
        };
    }, [user?.administrative_level]);

    useEffect(() => {
        if (token && !user && !authLoading) {
            fetchUser();
        }
    }, [token, user, authLoading, fetchUser]);

    if (isActuallyLoading) {
        return (
            <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
                <div className="text-xl font-medium text-gray-800">A carregar ecossistema SILA...</div>
                <div className="mt-4 w-32 h-1 bg-gray-200 rounded overflow-hidden">
                    <div className="h-full bg-red-600 animate-pulse w-full origin-left"></div>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (allowedLevels && user && !allowedLevels.includes(user.administrative_level)) {
        return <Navigate to="/unauthorized" state={{ from: location }} replace />;
    }

    return <Outlet />;
};
