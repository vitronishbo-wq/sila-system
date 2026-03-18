import { useEffect, useState } from "react";
import api from "@/services/api";
import { User, Calendar, Search, Loader2, ShieldCheck } from "lucide-react";

interface AuditLog {
    id: string;
    user: {
        full_name: string;
        email: string;
    } | null;
    action: string;
    resource_id: string | null;
    metadata_json: {
        ip?: string;
        user_agent?: string;
        query?: string;
        [key: string]: any;
    } | null;
    created_at: string;
}

export const AdminAuditViewer = () => {
    const [logs, setLogs] = useState<AuditLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [actionFilter, setActionFilter] = useState("all");

    useEffect(() => {
        let isMounted = true;
        api.get("/audit/audit/admin")
            .then(res => {
                if (isMounted) setLogs(res.data);
            })
            .catch(err => console.error("Erro ao carregar auditoria:", err))
            .finally(() => {
                if (isMounted) setLoading(false);
            });
        return () => { isMounted = false; };
    }, []);

    const filteredLogs = logs.filter(log => {
        const searchTerm = search.toLowerCase();
        const matchesSearch =
            !search ||
            log.user?.full_name?.toLowerCase().includes(searchTerm) ||
            log.user?.email?.toLowerCase().includes(searchTerm) ||
            log.action?.toLowerCase().includes(searchTerm) ||
            log.resource_id?.includes(searchTerm) ||
            log.metadata_json?.ip?.includes(searchTerm) ||
            log.metadata_json?.query?.toLowerCase().includes(searchTerm);

        const matchesAction = actionFilter === "all" || log.action === actionFilter;
        return matchesSearch && matchesAction;
    });

    const getActionStyle = (action: string) => {
        const config: Record<string, { bg: string; text: string }> = {
            "SEARCH_DOCUMENT_CONTENT": { bg: "bg-blue-50", text: "text-blue-700 border-blue-100" },
            "DOCUMENT_DOWNLOAD": { bg: "bg-green-50", text: "text-green-700 border-green-100" },
            "DOCUMENT_VIEW": { bg: "bg-purple-50", text: "text-purple-700 border-purple-100" },
            "PAYMENT_SUCCESS": { bg: "bg-emerald-50", text: "text-emerald-700 border-emerald-100" },
            "LOGIN": { bg: "bg-gray-50", text: "text-gray-700 border-gray-100" },
        };
        const cfg = config[action] || { bg: "bg-gray-50", text: "text-gray-600 border-gray-100" };
        return `inline-flex items-center px-3 py-1 rounded-lg text-xs font-bold border ${cfg.bg} ${cfg.text}`;
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] gap-4">
            <Loader2 className="h-10 w-10 animate-spin text-red-600" />
            <p className="text-gray-500 font-medium font-sans">Acedendo aos registos de segurança...</p>
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50/50 py-12 font-sans">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
                    <div>
                        <h1 className="text-4xl font-black text-gray-900 flex items-center gap-3 tracking-tighter">
                            <ShieldCheck className="h-10 w-10 text-red-600" /> Auditoria Geral
                        </h1>
                        <p className="text-gray-500 mt-2 font-medium">Rastreabilidade completa de ações no sistema SILA.</p>
                    </div>
                    <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-2xl border shadow-sm">
                        <span className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></span>
                        <span className="text-sm font-bold text-gray-600">{logs.length} Registos</span>
                    </div>
                </div>

                <div className="bg-white rounded-[2.5rem] shadow-xl shadow-gray-200/50 border border-gray-100 overflow-hidden">
                    <div className="p-8 border-b border-gray-100 bg-gray-50/30">
                        <div className="flex flex-col md:flex-row gap-4">
                            <div className="flex-1 relative">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Buscar usuário, IP, termo ou ID do recurso..."
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    className="w-full pl-12 pr-4 py-4 bg-white border border-gray-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-red-50 transition-all font-medium"
                                />
                            </div>
                            <select
                                value={actionFilter}
                                onChange={(e) => setActionFilter(e.target.value)}
                                className="px-6 py-4 bg-white border border-gray-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-red-50 font-bold text-gray-700 cursor-pointer"
                            >
                                <option value="all">Todas as Ações</option>
                                <option value="SEARCH_DOCUMENT_CONTENT">Busca de Conteúdo</option>
                                <option value="DOCUMENT_DOWNLOAD">Downloads</option>
                                <option value="DOCUMENT_VIEW">Visualizações</option>
                                <option value="PAYMENT_SUCCESS">Pagamentos</option>
                            </select>
                        </div>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="bg-gray-50 text-gray-400 text-[11px] uppercase tracking-widest font-black">
                                    <th className="px-8 py-4">Usuário / Agente</th>
                                    <th className="px-8 py-4">Ação executada</th>
                                    <th className="px-8 py-4">Recurso ID</th>
                                    <th className="px-8 py-4">Metadados</th>
                                    <th className="px-8 py-4">Data e Hora</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {filteredLogs.length === 0 ? (
                                    <tr>
                                        <td colSpan={5} className="py-20 text-center text-gray-400 font-medium">
                                            Nenhum rastro encontrado para estes critérios.
                                        </td>
                                    </tr>
                                ) : (
                                    filteredLogs.map(log => (
                                        <tr key={log.id} className="hover:bg-red-50/30 transition-colors group">
                                            <td className="px-8 py-6">
                                                <div className="flex items-center gap-4">
                                                    <div className="h-10 w-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-400 group-hover:bg-white transition-colors">
                                                        <User className="h-5 w-5" />
                                                    </div>
                                                    <div>
                                                        <p className="font-bold text-gray-900 leading-none">
                                                            {log.user?.full_name || "Sistema / Público"}
                                                        </p>
                                                        <p className="text-xs text-gray-500 mt-1">{log.user?.email || "—"}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-8 py-6">
                                                <span className={getActionStyle(log.action)}>
                                                    {log.action?.replace(/_/g, " ")}
                                                </span>
                                            </td>
                                            <td className="px-8 py-6 font-mono text-[11px] text-gray-400">
                                                {log.resource_id ? `#${log.resource_id.slice(-8)}` : "—"}
                                            </td>
                                            <td className="px-8 py-6">
                                                <div className="space-y-1">
                                                    {log.metadata_json?.ip && (
                                                        <p className="text-xs font-bold text-gray-600">IP: <span className="font-mono text-gray-400 font-normal">{log.metadata_json.ip}</span></p>
                                                    )}
                                                    {log.metadata_json?.query && (
                                                        <p className="text-xs italic text-red-600">Busca: "{log.metadata_json.query}"</p>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="px-8 py-6">
                                                <div className="flex items-center gap-2 text-sm text-gray-600 font-medium">
                                                    <Calendar className="h-4 w-4 text-gray-300" />
                                                    {new Date(log.created_at).toLocaleString("pt-AO")}
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};