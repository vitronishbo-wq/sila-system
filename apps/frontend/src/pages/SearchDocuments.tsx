import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import api from "@/services/api";
import { DocumentCard } from "@/components/Documents/DocumentCard";
import { Search, Filter, Loader2, SearchX } from "lucide-react";
import toast from "react-hot-toast";

export const SearchDocuments = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(false);

    const q = searchParams.get("q") || "";
    const status = searchParams.get("status") || "";
    const dateFrom = searchParams.get("date_from") || "";
    const dateTo = searchParams.get("date_to") || "";

    useEffect(() => {
        if (!q && !status && !dateFrom && !dateTo) {
            setDocuments([]);
            return;
        }

        const fetchResults = async () => {
            setLoading(true);
            try {
                const response = await api.get("/documents/search/deep", {
                    params: {
                        q: q || undefined,
                        status: status || undefined,
                        date_from: dateFrom || undefined,
                        date_to: dateTo || undefined
                    }
                });
                setDocuments(response.data);
            } catch (err) {
                console.error("Erro na busca:", err);
                toast.error("Erro ao realizar a busca institucional.");
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, [searchParams]);

    const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const params: any = {};
        formData.forEach((value, key) => {
            if (value) params[key] = value;
        });
        setSearchParams(params);
    };

    return (
        <div className="min-h-screen bg-[#F8FAFC] py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-10">
                    <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
                        Busca Institucional <span className="text-red-600">SILA</span>
                    </h1>
                    <p className="text-lg text-gray-600">
                        Encontre documentos processados e metadados em todo o território nacional.
                    </p>
                </div>

                {/* Filter Bar */}
                <div className="bg-white rounded-3xl shadow-2xl border border-gray-100 p-8 mb-12 transform transition-all">
                    <form onSubmit={handleSearch} className="space-y-6">
                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                            {/* Search Input */}
                            <div className="lg:col-span-7 relative">
                                <Search className="absolute left-5 top-1/2 -translate-y-1/2 h-6 w-6 text-gray-400" />
                                <input
                                    name="q"
                                    type="text"
                                    defaultValue={q}
                                    placeholder="Palavras-chave, número de processo ou conteúdo OCR..."
                                    className="w-full pl-14 pr-4 py-5 bg-gray-50 border-none rounded-2xl focus:ring-4 focus:ring-red-100 transition-all text-lg font-medium placeholder:text-gray-400"
                                />
                            </div>

                            {/* Status Filter */}
                            <div className="lg:col-span-3">
                                <select
                                    name="status"
                                    defaultValue={status}
                                    className="w-full h-full px-6 py-5 bg-gray-50 border-none rounded-2xl focus:ring-4 focus:ring-red-100 transition-all font-semibold text-gray-700 appearance-none cursor-pointer"
                                >
                                    <option value="">Todos os Status</option>
                                    <option value="completed">Concluído</option>
                                    <option value="processing">Processando</option>
                                    <option value="pending">Pendente</option>
                                    <option value="failed">Falhou</option>
                                </select>
                            </div>

                            {/* Submit Button */}
                            <div className="lg:col-span-2">
                                <button
                                    type="submit"
                                    className="w-full h-full bg-red-600 text-white rounded-2xl font-black text-lg hover:bg-black transition-all shadow-lg hover:shadow-red-200/50 flex items-center justify-center gap-3 active:scale-95"
                                >
                                    <Filter className="h-5 w-5" />
                                    BUSCAR
                                </button>
                            </div>
                        </div>

                        {/* Secondary Filters */}
                        <div className="flex flex-wrap gap-4 items-center border-t border-gray-100 pt-6">
                            <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">Período:</span>
                            <div className="flex items-center gap-2">
                                <input
                                    type="date"
                                    name="date_from"
                                    defaultValue={dateFrom}
                                    className="px-4 py-2 bg-gray-50 border-none rounded-xl text-sm font-semibold focus:ring-2 focus:ring-red-100"
                                />
                                <span className="text-gray-300">até</span>
                                <input
                                    type="date"
                                    name="date_to"
                                    defaultValue={dateTo}
                                    className="px-4 py-2 bg-gray-50 border-none rounded-xl text-sm font-semibold focus:ring-2 focus:ring-red-100"
                                />
                            </div>
                        </div>
                    </form>
                </div>

                {/* Results Section */}
                {loading ? (
                    <div className="flex flex-col items-center justify-center py-32 space-y-4">
                        <Loader2 className="h-12 w-12 text-red-600 animate-spin" />
                        <p className="text-xl font-bold text-gray-500 animate-pulse">Consultando base de dados nacional...</p>
                    </div>
                ) : documents.length === 0 ? (
                    (q || status || dateFrom || dateTo) ? (
                        <div className="bg-white rounded-3xl p-20 text-center shadow-sm border border-dashed border-gray-200">
                            <div className="bg-gray-50 h-24 w-24 rounded-full flex items-center justify-center mx-auto mb-6">
                                <SearchX className="h-12 w-12 text-gray-400" />
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-2">Nenhum resultado encontrado</h3>
                            <p className="text-gray-500 max-w-md mx-auto">
                                Verifique a ortografia ou tente remover alguns filtros de status ou data para expandir a busca.
                            </p>
                        </div>
                    ) : (
                        <div className="py-20 text-center">
                            <p className="text-gray-400 text-lg">Digite algo acima para iniciar a busca avançada.</p>
                        </div>
                    )
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {documents.map((doc: any) => (
                            <div key={doc.id} className="transform hover:-translate-y-2 transition-all duration-300">
                                <DocumentCard document={doc} />
                            </div>
                        ))}
                    </div>
                )}

                {/* Counter Footer */}
                {documents.length > 0 && !loading && (
                    <div className="mt-12 text-center text-gray-400 font-medium">
                        Mostrando {documents.length} documento(s) encontrado(s) na consulta.
                    </div>
                )}
            </div>
        </div>
    );
};

export default SearchDocuments;
