import { useEffect, useState } from "react";
import api from "@/services/api";
import { useAuthStore } from "@/store/authStore";
import { Users, FileText, DollarSign, Building2, TrendingUp, AlertTriangle } from "lucide-react";

interface AdminStats {
    total_users: number;
    total_documents: number;
    total_payments: number;
    pending_requests: number;
    revenue_month: number;
    critical_alerts: number;
}

export const AdminPanel = () => {
    const [stats, setStats] = useState<AdminStats | null>(null);
    const [loading, setLoading] = useState(true);
    const { user } = useAuthStore();

    useEffect(() => {
        // Lógica de autorização baseada no novo esquema Governamental
        const isAdmin = user?.roles?.includes("admin") || user?.administrative_level === "CENTRAL";

        if (isAdmin) {
            api
                .get<AdminStats>("/statistics/admin")
                .then((res) => setStats(res.data))
                .catch((err) => {
                    console.error("[SILA] Erro ao carregar estatísticas:", err);
                    setStats(null);
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, [user]);

    const cards = [
        { title: "Total de Cidadãos", value: stats?.total_users ?? 0, icon: Users, color: "text-blue-600" },
        { title: "Documentos Emitidos", value: stats?.total_documents ?? 0, icon: FileText, color: "text-purple-600" },
        { title: "Receita Mensal (AOA)", value: stats?.revenue_month?.toLocaleString("pt-AO") ?? "0", icon: DollarSign, color: "text-green-600" },
        { title: "Pedidos Pendentes", value: stats?.pending_requests ?? 0, icon: Building2, color: "text-orange-600" },
        { title: "Pagamentos Processados", value: stats?.total_payments ?? 0, icon: TrendingUp, color: "text-cyan-600" },
        { title: "Alertas Críticos", value: stats?.critical_alerts ?? 0, icon: AlertTriangle, color: "text-red-600" },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
            <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="mb-10 flex flex-col md:flex-row md:items-center md:justify-between border-b pb-6 border-gray-200">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800 mb-2">Painel Administrativo</h1>
                        <p className="text-gray-600">Gestão Central do SILA System — República de Angola</p>
                    </div>
                    <div className="mt-4 md:mt-0 px-4 py-2 bg-red-100 text-red-700 rounded-full text-sm font-bold uppercase tracking-widest">
                        Acesso Restrito: {user?.administrative_level}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {cards.map((card) => (
                        <div
                            key={card.title}
                            className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-2xl transition-all duration-300 border border-gray-200 group"
                        >
                            <div className="flex items-center justify-between mb-6">
                                <div className={`p-3 rounded-xl bg-gray-50 group-hover:bg-white transition-colors`}>
                                    <card.icon className={`h-10 w-10 ${card.color}`} />
                                </div>
                                <span className="text-4xl font-extrabold text-gray-800">
                                    {loading ? "..." : card.value}
                                </span>
                            </div>
                            <h3 className="text-lg font-semibold text-gray-700">{card.title}</h3>
                        </div>
                    ))}
                </div>

                {/* Histórico de Atividades */}
                <div className="mt-12 bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                    <div className="flex items-center gap-3 mb-6">
                        <TrendingUp className="text-red-600" />
                        <h2 className="text-2xl font-bold text-gray-800">Atividade Recente do Sistema</h2>
                    </div>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                            <span className="text-gray-700 font-medium">Novo pagamento recebido</span>
                            <span className="text-green-600 font-bold">+15.000 AOA</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                            <span className="text-gray-700 font-medium">Documento emitido (BI)</span>
                            <span className="text-blue-600 font-bold">Luanda - Belas</span>
                        </div>
                        <div className="flex items-center justify-between p-4 bg-orange-50 rounded-xl border border-orange-100">
                            <span className="text-gray-700 font-medium">Pedido pendente (atualização BI)</span>
                            <span className="text-orange-600 font-bold italic text-sm">3 dias em atraso</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
