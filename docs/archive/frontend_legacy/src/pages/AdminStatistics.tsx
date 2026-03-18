import { useEffect, useState } from "react";
import api from "@/api/axios"; // Novo cliente centralizado
import { TrendingUp, FileText, Users, AlertCircle, CheckCircle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { StatisticsSkeleton } from "@/components/Statistics/StatisticsSkeleton";

interface Stats {
    total_documents: number;
    total_users: number;
    documents_today: number;
    volume_today_mb: number;
    new_users_today: number;
    status_breakdown: {
        pending: number;
        processing: number;
        completed: number;
        failed: number;
    };
}

export const AdminStatistics = () => {
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;
        (api.get("/statistics/admin") as unknown as Promise<Stats>) // Type cast para o interceptor que transforma response -> data
            .then(data => {
                if (isMounted) setStats(data);
            })
            .catch(err => {
                if (isMounted) {
                    if (err.response?.status === 403) {
                        setError("Este painel é restrito ao Nível Central. Contacte a administração.");
                    } else {
                        setError("Erro ao carregar estatísticas do sistema.");
                    }
                    console.error("Erro ao carregar estatísticas:", err);
                }
            })
            .finally(() => {
                if (isMounted) setLoading(false);
            });
        return () => { isMounted = false; };
    }, []);

    if (loading) return <StatisticsSkeleton />;

    if (error) return (
        <div className="min-h-screen bg-gray-50/50 flex items-center justify-center p-4">
            <div className="bg-white rounded-[2rem] shadow-xl p-10 border border-red-100 max-w-md w-full text-center">
                <AlertCircle className="h-16 w-16 text-red-600 mx-auto mb-6" />
                <h3 className="text-2xl font-black text-gray-900 mb-2">Acesso Negado</h3>
                <p className="text-gray-600 mb-8">{error}</p>
                <button
                    onClick={() => window.location.reload()}
                    className="w-full bg-red-600 text-white py-4 rounded-xl font-bold hover:bg-red-700 transition"
                >
                    Tentar Novamente
                </button>
            </div>
        </div>
    );

    const statusData = [
        { name: "Concluídos", value: stats?.status_breakdown?.completed || 0, color: "#10b981" },
        { name: "Processando", value: stats?.status_breakdown?.processing || 0, color: "#f59e0b" },
        { name: "Pendentes", value: stats?.status_breakdown?.pending || 0, color: "#6b7280" },
        { name: "Falhas", value: stats?.status_breakdown?.failed || 0, color: "#ef4444" },
    ];

    return (
        <div className="min-h-screen bg-gray-50/50 py-12 font-sans">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex items-center justify-between mb-12">
                    <h1 className="text-4xl font-black text-gray-900 tracking-tighter">
                        Painel de Estatísticas <span className="text-red-600 uppercase">SILA</span>
                    </h1>
                    <div className="bg-white px-4 py-2 rounded-2xl shadow-sm border border-gray-100 text-xs font-black text-gray-400 uppercase tracking-widest">
                        Live Data Engine
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                    <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/40 p-8 border border-gray-100 transition-all hover:translate-y-[-4px]">
                        <div className="flex items-center justify-between mb-6">
                            <div className="p-3 bg-red-50 rounded-2xl">
                                <FileText className="h-7 w-7 text-red-600" />
                            </div>
                            <TrendingUp className="h-5 w-5 text-green-500" />
                        </div>
                        <p className="text-gray-400 text-xs font-black uppercase tracking-widest">Documentos</p>
                        <p className="text-4xl font-black text-gray-900 mt-2">{stats?.total_documents?.toLocaleString() || 0}</p>
                        <div className="flex items-center gap-1 text-sm text-green-600 mt-4 font-bold">
                            <span>+{stats?.documents_today || 0}</span>
                            <span className="text-gray-400 font-medium">hoje</span>
                        </div>
                    </div>

                    <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/40 p-8 border border-gray-100 transition-all hover:translate-y-[-4px]">
                        <div className="flex items-center justify-between mb-6">
                            <div className="p-3 bg-blue-50 rounded-2xl">
                                <Users className="h-7 w-7 text-blue-600" />
                            </div>
                            <TrendingUp className="h-5 w-5 text-green-500" />
                        </div>
                        <p className="text-gray-400 text-xs font-black uppercase tracking-widest">Cidadãos</p>
                        <p className="text-4xl font-black text-gray-900 mt-2">{stats?.total_users?.toLocaleString() || 0}</p>
                        <div className="flex items-center gap-1 text-sm text-green-600 mt-4 font-bold">
                            <span>+{stats?.new_users_today || 0}</span>
                            <span className="text-gray-400 font-medium">novos</span>
                        </div>
                    </div>

                    <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/40 p-8 border border-gray-100 transition-all hover:translate-y-[-4px]">
                        <div className="flex items-center justify-between mb-6">
                            <div className="p-3 bg-green-50 rounded-2xl">
                                <CheckCircle className="h-7 w-7 text-green-600" />
                            </div>
                        </div>
                        <p className="text-gray-400 text-xs font-black uppercase tracking-widest">Volume Útil</p>
                        <p className="text-4xl font-black text-gray-900 mt-2">{stats?.volume_today_mb || 0} <span className="text-xl font-medium">MB</span></p>
                        <p className="text-xs text-gray-400 mt-4 font-medium uppercase tracking-tighter">Tráfego de processamento</p>
                    </div>

                    <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/40 p-8 border border-red-100 bg-red-50/10 transition-all hover:translate-y-[-4px]">
                        <div className="flex items-center justify-between mb-6">
                            <div className="p-3 bg-red-600 rounded-2xl">
                                <AlertCircle className="h-7 w-7 text-white" />
                            </div>
                        </div>
                        <p className="text-red-900/40 text-xs font-black uppercase tracking-widest">Erros Críticos</p>
                        <p className="text-4xl font-black text-red-600 mt-2">{stats?.status_breakdown?.failed || 0}</p>
                        <p className="text-xs text-red-500 mt-4 font-bold uppercase animate-pulse tracking-tighter">Ação Necessária</p>
                    </div>
                </div>

                <div className="bg-white rounded-[3rem] shadow-xl shadow-gray-200/40 p-10 border border-gray-100 chart-container">
                    <div className="flex flex-col md:flex-row md:items-center justify-between mb-12 gap-6">
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight italic">Status de Fluxo de Documentos</h2>
                        <div className="flex flex-wrap gap-6">
                            {statusData.map((s) => (
                                <div key={s.name} className="flex items-center gap-3 text-[10px] font-black text-gray-400 uppercase tracking-widest">
                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: s.color }}></div>
                                    {s.name}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="h-[450px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={statusData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="8 8" vertical={false} stroke="#f1f5f9" />
                                <XAxis
                                    dataKey="name"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#64748b', fontSize: 11, fontWeight: 800 }}
                                    dy={15}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#94a3b8', fontSize: 11 }}
                                />
                                <Tooltip
                                    cursor={{ fill: '#f8fafc' }}
                                    contentStyle={{ borderRadius: '24px', border: 'none', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)', padding: '15px' }}
                                />
                                <Bar dataKey="value" radius={[12, 12, 12, 12]} barSize={80}>
                                    {statusData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};