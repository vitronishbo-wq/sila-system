import { StatsCards } from "@/components/Dashboard/StatsCards";
import { FileText, Clock, AlertTriangle, FolderOpen } from "lucide-react";
import { Link } from "react-router-dom";

export default function CitizenDashboard() {
    const recentActivities = [
        { id: 1, title: "Pedido de Bilhete de Identidade", status: "Em processamento", date: "24 Dez 2025", type: "document" },
        { id: 2, title: "Pagamento de Taxa Rodoviária", status: "Concluído", date: "22 Dez 2025", type: "payment" },
        { id: 3, title: "Renovação de Carta de Condução", status: "Pendente de Pagamento", date: "20 Dez 2025", type: "document" },
    ];

    return (
        <div className="min-h-screen bg-gray-50 pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Portal do Cidadão</h1>
                        <p className="text-gray-600 mt-1 font-medium">Bem-vindo de volta! Aqui está um resumo da sua conta.</p>
                    </div>
                    <div className="flex flex-wrap gap-4">
                        <Link to="/citizen/documents" className="bg-white text-gray-700 border border-gray-200 px-6 py-3 rounded-xl font-bold hover:bg-gray-50 transition flex items-center gap-2 shadow-sm">
                            <FolderOpen className="h-5 w-5 text-red-600" />
                            Meus Documentos
                        </Link>
                        <button className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 transition flex items-center gap-2 shadow-lg shadow-red-100">
                            <FileText className="h-5 w-5" />
                            Novo Pedido
                        </button>
                    </div>
                </div>

                <StatsCards />

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Recent Activity */}
                    <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                                <Clock className="h-6 w-6 text-red-600" />
                                Atividade Recente
                            </h2>
                            <button className="text-red-600 text-sm font-bold hover:underline">Ver tudo</button>
                        </div>

                        <div className="space-y-6">
                            {recentActivities.map((activity) => (
                                <div key={activity.id} className="flex items-center justify-between p-4 rounded-xl hover:bg-gray-50 transition border border-transparent hover:border-gray-100">
                                    <div className="flex items-center gap-4">
                                        <div className={`p-3 rounded-lg ${activity.type === 'payment' ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'}`}>
                                            <FileText className="h-6 w-6" />
                                        </div>
                                        <div>
                                            <p className="font-bold text-gray-900">{activity.title}</p>
                                            <p className="text-sm text-gray-500">{activity.date}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className={`px-4 py-1.5 rounded-full text-xs font-bold ${activity.status === 'Concluído' ? 'bg-green-100 text-green-700' :
                                            activity.status === 'Em processamento' ? 'bg-blue-100 text-blue-700' :
                                                'bg-orange-100 text-orange-700'
                                            }`}>
                                            {activity.status}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Quick Support */}
                    <div className="bg-gradient-to-br from-red-600 to-red-800 rounded-2xl shadow-lg p-8 text-white relative overflow-hidden">
                        <div className="relative z-10">
                            <h2 className="text-xl font-bold mb-4">Precisa de Ajuda?</h2>
                            <p className="text-red-50/80 mb-8 leading-relaxed">
                                Nossa equipe de suporte está disponível 24/7 para ajudar com seus documentos e processos.
                            </p>
                            <div className="space-y-4">
                                <button className="w-full bg-white text-red-600 py-3 rounded-xl font-bold hover:bg-red-50 transition">
                                    Falar com Assistente Virtual
                                </button>
                                <button className="w-full bg-red-500/30 text-white border border-red-400/50 py-3 rounded-xl font-bold hover:bg-red-500/40 transition">
                                    Ver Perguntas Frequentes
                                </button>
                            </div>
                        </div>
                        <div className="absolute -bottom-10 -right-10 opacity-10">
                            <AlertTriangle className="h-40 w-40" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
