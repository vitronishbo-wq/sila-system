// apps/frontend/src/components/Dashboard/StatsCards.tsx
import { useEffect, useState } from "react";
import api from "@/api/axios";
import { FileText, CreditCard, AlertCircle, CheckCircle } from "lucide-react";

interface Stats {
    total_documents: number;
    pending_payments: number;
    completed_payments: number;
    pending_requests: number;
}

export const StatsCards = () => {
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        (api.get("/statistics/me") as unknown as Promise<Stats>)
            .then((data) => setStats(data))
            .finally(() => setLoading(false));
    }, []);

    const cards = [
        {
            title: "Meus Documentos",
            value: stats?.total_documents ?? 0,
            icon: FileText,
            color: "text-blue-600",
            bg: "bg-blue-100",
        },
        {
            title: "Pagamentos Pendentes",
            value: stats?.pending_payments ?? 0,
            icon: AlertCircle,
            color: "text-orange-600",
            bg: "bg-orange-100",
        },
        {
            title: "Pagamentos Concluídos",
            value: stats?.completed_payments ?? 0,
            icon: CheckCircle,
            color: "text-green-600",
            bg: "bg-green-100",
        },
        {
            title: "Pedidos em Andamento",
            value: stats?.pending_requests ?? 0,
            icon: CreditCard,
            color: "text-purple-600",
            bg: "bg-purple-100",
        },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
            {cards.map((card) => (
                <div key={card.title} className="bg-white rounded-xl shadow-lg p-8 hover:shadow-2xl transition">
                    <div className="flex items-center justify-between mb-6">
                        <div className={`p-4 rounded-full ${card.bg}`}>
                            <card.icon className={`h-10 w-10 ${card.color}`} />
                        </div>
                        <span className="text-4xl font-extrabold text-gray-800">
                            {loading ? "-" : card.value}
                        </span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-700">{card.title}</h3>
                </div>
            ))}
        </div>
    );
};