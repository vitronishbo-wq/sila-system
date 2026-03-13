import { useEffect, useState } from "react";
import { Bell, Check, Loader2, Inbox, Clock } from "lucide-react";
import api from "@/services/api";
import { toast } from "react-hot-toast";

interface Notification {
    id: string;
    title: string;
    message: string;
    status: string;
    created_at: string;
}

export default function Notifications() {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchNotifications = async () => {
        try {
            const res = await api.get("/notifications/");
            setNotifications(res.data);
        } catch (err) {
            console.error("Erro ao carregar notificações:", err);
            toast.error("Falha ao carregar notificações");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        let isMounted = true;
        if (isMounted) fetchNotifications();
        return () => { isMounted = false; };
    }, []);

    const markAsRead = async (id: string) => {
        try {
            await api.post(`/notifications/${id}/read`);
            setNotifications((prev) =>
                prev.map((n) => (n.id === id ? { ...n, status: "read" } : n))
            );

            // Dispara evento para o Header atualizar o badge imediatamente
            window.dispatchEvent(new Event("notificationRead"));
            toast.success("Notificação lida");
        } catch (err) {
            toast.error("Erro ao atualizar status");
        }
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
                <Loader2 className="h-12 w-12 animate-spin text-red-700" />
                <p className="text-gray-500 font-medium">Sincronizando com o portal...</p>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto px-4 py-12">
            <div className="flex items-center justify-between mb-10 border-b pb-6">
                <div className="flex items-center gap-4">
                    <div className="bg-red-100 p-3 rounded-2xl">
                        <Bell className="h-8 w-8 text-red-700" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-black text-gray-900">Centro de Notificações</h1>
                        <p className="text-gray-500 font-medium text-sm">Gerencie seus alertas e comunicados oficiais</p>
                    </div>
                </div>
                <div className="text-right">
                    <span className="text-2xl font-black text-red-700">
                        {notifications.filter(n => n.status !== "read").length}
                    </span>
                    <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Pendentes</p>
                </div>
            </div>

            {notifications.length === 0 ? (
                <div className="text-center py-24 bg-white rounded-[2.5rem] border-2 border-dashed border-gray-100 shadow-sm">
                    <Inbox className="h-20 w-20 mx-auto text-gray-200 mb-6" />
                    <h2 className="text-xl font-bold text-gray-800">Caixa de entrada vazia</h2>
                    <p className="text-gray-400 mt-2">Você não possui notificações no momento.</p>
                </div>
            ) : (
                <div className="grid gap-4">
                    {notifications.map((notification) => (
                        <div
                            key={notification.id}
                            className={`group relative p-6 rounded-[2rem] border-2 transition-all duration-300 ${notification.status !== "read"
                                    ? "bg-white border-red-50 shadow-md shadow-red-900/5 ring-1 ring-red-100/50"
                                    : "bg-gray-50/50 border-transparent opacity-70"
                                }`}
                        >
                            <div className="flex items-start justify-between gap-6">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className={`text-lg font-extrabold ${notification.status !== "read" ? "text-gray-900" : "text-gray-600"
                                            }`}>
                                            {notification.title}
                                        </h3>
                                        {notification.status !== "read" && (
                                            <span className="h-2 w-2 bg-red-600 rounded-full animate-pulse" />
                                        )}
                                    </div>
                                    <p className="text-gray-600 leading-relaxed mb-4">
                                        {notification.message}
                                    </p>
                                    <div className="flex items-center gap-2 text-[11px] font-bold text-gray-400 uppercase tracking-tighter">
                                        <Clock className="h-3 w-3" />
                                        {new Date(notification.created_at).toLocaleString("pt-AO")}
                                    </div>
                                </div>

                                {notification.status !== "read" && (
                                    <button
                                        onClick={() => markAsRead(notification.id)}
                                        className="flex items-center gap-2 px-5 py-3 bg-gray-900 text-white text-sm font-bold rounded-2xl hover:bg-red-700 transition-all shadow-lg active:scale-95"
                                    >
                                        <Check className="h-4 w-4" />
                                        Lida
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}