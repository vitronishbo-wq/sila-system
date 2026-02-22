import { APP_IMAGES } from "@/constants/images";
import { useAuthStore } from "@/store/authStore";
import { Bell, LogOut, User } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/services/api";
import { GlobalSearchBar } from "../Search/GlobalSearchBar";
import { useNavigate } from "react-router-dom";

export const Header = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuthStore();
    const [unreadCount, setUnreadCount] = useState(0);

    useEffect(() => {
        let isMounted = true;

        const fetchNotifications = async () => {
            if (!user) return;
            try {
                const res = await api.get("/notifications/me");
                if (isMounted) {
                    setUnreadCount(res.data.unread_count || 0);
                }
            } catch (err) {
                console.error("Erro ao buscar notificações:", err);
            }
        };

        fetchNotifications();

        // Polling opcional: busca novas notificações a cada 2 minutos
        const interval = setInterval(fetchNotifications, 120000);

        return () => {
            isMounted = false;
            clearInterval(interval);
        };
    }, [user]);

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <header className="bg-gradient-to-r from-red-800 to-red-600 text-white shadow-xl sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20 gap-4">
                    {/* Lado Esquerdo: Logos e Título */}
                    <div className="flex items-center gap-8 shrink-0">
                        <div className="flex items-center gap-4">
                            <img
                                src={APP_IMAGES.LOGO}
                                alt="Brasão da República de Angola"
                                className="h-14 w-14 object-contain drop-shadow-lg"
                            />
                            <div className="h-10 w-px bg-white/30" />
                            <img
                                src={APP_IMAGES.FLAG}
                                alt="Bandeira de Angola"
                                className="h-8 object-contain"
                            />
                        </div>
                        <div className="hidden lg:block">
                            <h1 className="text-xl font-bold tracking-wide leading-none">SILA System</h1>
                            <p className="text-xs opacity-80 uppercase tracking-tighter">Portal do Cidadão</p>
                        </div>
                    </div>

                    {/* Centro: Barra de Busca Global */}
                    <div className="flex-1 max-w-2xl px-4">
                        <GlobalSearchBar />
                    </div>

                    {/* Lado Direito: Perfil e Ações */}
                    <div className="flex items-center gap-4 shrink-0">
                        <div className="text-right hidden sm:block border-r border-white/20 pr-4">
                            <p className="font-bold text-sm leading-tight uppercase">
                                {user?.full_name || "Cidadão"}
                            </p>
                            <p className="text-[10px] opacity-80 font-medium">REPÚBLICA DE ANGOLA</p>
                        </div>

                        <div className="flex items-center gap-1">
                            {/* Botão Notificações */}
                            <button
                                onClick={() => navigate("/notifications")}
                                className="relative p-2 hover:bg-white/10 rounded-full transition-colors"
                                title="Notificações"
                            >
                                <Bell className="h-5 w-5" />
                                {unreadCount > 0 && (
                                    <span className="absolute top-1 right-1 h-4 w-4 bg-white text-red-700 text-[10px] rounded-full flex items-center justify-center font-black shadow-sm">
                                        {unreadCount > 99 ? "99+" : unreadCount}
                                    </span>
                                )}
                            </button>

                            {/* Botão Perfil */}
                            <button
                                onClick={() => navigate("/profile")}
                                className="p-2 hover:bg-white/10 rounded-full transition-colors"
                                title="Meu Perfil"
                            >
                                <User className="h-5 w-5" />
                            </button>

                            {/* Botão Sair */}
                            <button
                                onClick={handleLogout}
                                className="p-2 hover:bg-red-900/40 rounded-full transition-colors text-red-100"
                                title="Sair do Sistema"
                            >
                                <LogOut className="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};