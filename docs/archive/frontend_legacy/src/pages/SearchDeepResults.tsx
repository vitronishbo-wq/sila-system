import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "@/services/api";
import { DocumentCard } from "@/components/Documents/DocumentCard";
import { Search, Loader2, SearchX, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

export const SearchDeepResults = () => {
    const [searchParams] = useSearchParams();
    const q = searchParams.get("q") || "";
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!q) return;
        setLoading(true);
        api.get("/documents/search/deep", { params: { q } })
            .then(res => setDocuments(res.data))
            .catch(err => console.error("Erro na busca profunda:", err))
            .finally(() => setLoading(false));
    }, [q]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Breadcrumb / Back Navigation */}
                <Link to="/documents" className="inline-flex items-center gap-2 text-slate-500 hover:text-red-600 transition-colors font-semibold mb-8 group">
                    <ArrowLeft className="h-5 w-5 group-hover:-translate-x-1 transition-transform" />
                    Voltar para Documentos
                </Link>

                <div className="mb-12">
                    <div className="flex items-center gap-4 mb-2">
                        <div className="bg-red-600 p-2 rounded-xl shadow-lg shadow-red-200">
                            <Search className="h-6 w-6 text-white" />
                        </div>
                        <h1 className="text-4xl font-black text-slate-800 tracking-tight">
                            Resultados para "{q}"
                        </h1>
                    </div>
                    <p className="text-lg text-slate-500 font-medium ml-12">
                        Busca profunda realizada no conteúdo OCR e metadados institucionais.
                    </p>
                </div>

                {loading ? (
                    <div className="flex flex-col items-center justify-center py-32 space-y-6 bg-white rounded-3xl shadow-sm border border-slate-200">
                        <Loader2 className="h-16 w-16 text-red-600 animate-spin" />
                        <div className="text-center">
                            <p className="text-2xl font-bold text-slate-700">Vasculhando bases nacionais...</p>
                            <p className="text-slate-400">Extraindo informações críticas dos documentos processados.</p>
                        </div>
                    </div>
                ) : documents.length === 0 ? (
                    <div className="bg-white rounded-3xl p-24 text-center shadow-xl shadow-slate-200/50 border border-slate-100">
                        <div className="bg-slate-50 h-24 w-24 rounded-full flex items-center justify-center mx-auto mb-8">
                            <SearchX className="h-12 w-12 text-slate-300" />
                        </div>
                        <h3 className="text-3xl font-black text-slate-800 mb-4">Nenhum rastro encontrado</h3>
                        <p className="text-slate-500 text-lg max-w-lg mx-auto leading-relaxed">
                            Não encontramos correspondências exatas para <span className="text-red-600 font-bold">"{q}"</span> no conteúdo interno dos documentos disponíveis.
                        </p>
                        <div className="mt-10 flex justify-center gap-4">
                            <Link to="/documents" className="px-8 py-3 bg-slate-100 text-slate-600 rounded-xl font-bold hover:bg-slate-200 transition-all">
                                Ver meus documentos
                            </Link>
                            <button onClick={() => window.history.back()} className="px-8 py-3 bg-red-600 text-white rounded-xl font-bold hover:bg-red-700 shadow-lg shadow-red-200 transition-all">
                                Tentar outro termo
                            </button>
                        </div>
                    </div>
                ) : (
                    <>
                        <div className="space-y-8 max-w-5xl mx-auto">
                            {documents.map((doc: any) => (
                                <div key={doc.id} className="bg-white rounded-3xl p-8 shadow-xl shadow-slate-200/50 border border-slate-100 transform hover:-translate-y-1 transition-all duration-300 animate-in fade-in slide-in-from-bottom-4">
                                    <DocumentCard document={doc} />

                                    {doc.highlight_snippet && (
                                        <div className="mt-6 p-6 bg-yellow-50 rounded-2xl border border-yellow-100 relative overflow-hidden group">
                                            <div className="absolute top-0 left-0 w-1.5 h-full bg-yellow-400" />
                                            <p className="text-xs font-black text-yellow-700 uppercase tracking-widest mb-3 flex items-center gap-2">
                                                <span className="h-2 w-2 rounded-full bg-yellow-500 animate-pulse" />
                                                Trecho Identificado no Conteúdo
                                            </p>
                                            <div
                                                className="text-slate-800 text-lg leading-relaxed font-medium prose prose-slate max-w-none"
                                                style={{ wordBreak: 'break-word' }}
                                            >
                                                <style dangerouslySetInnerHTML={{
                                                    __html: `
                                                    mark {
                                                        background-color: #fde047; /* bg-yellow-300 */
                                                        color: #1e293b; /* slate-800 */
                                                        padding: 0 2px;
                                                        border-radius: 2px;
                                                        font-weight: 700;
                                                    }
                                                `}} />
                                                <span dangerouslySetInnerHTML={{ __html: `...${doc.highlight_snippet}...` }} />
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                        <div className="mt-16 text-center">
                            <p className="text-slate-400 font-bold uppercase tracking-widest text-sm">
                                {documents.length} documento(s) identificado(s) com alta relevância
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};
