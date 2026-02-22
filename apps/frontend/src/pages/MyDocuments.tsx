import { useMyDocuments } from '@/hooks/useMyDocuments';
import { Search, Download, FileText, Loader2, X } from 'lucide-react';
import { useState } from 'react';

export const MyDocuments = () => {
    const { documents, loading, searchTerm, setSearchTerm, searchDocuments, downloadDocument } = useMyDocuments();
    const [previewId, setPreviewId] = useState<number | null>(null);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        searchDocuments(searchTerm);
    };

    return (
        <div className="max-w-7xl mx-auto p-6">
            <div className="mb-10">
                <h1 className="text-3xl font-black text-gray-900 mb-2 tracking-tight">Meus Documentos</h1>
                <p className="text-gray-600 font-medium">Consulte, pesquise e descarregue os seus documentos digitalizados.</p>
            </div>

            {/* Barra de Pesquisa OCR */}
            <form onSubmit={handleSearch} className="mb-8">
                <div className="relative max-w-2xl">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Pesquise por texto dentro do documento (ex: número do BI, nome do pai...)"
                        className="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-300 focus:border-red-600 focus:outline-none text-lg transition-all"
                    />
                    <button
                        type="submit"
                        className="absolute right-2 top-1/2 -translate-y-1/2 bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition font-bold"
                    >
                        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Pesquisar"}
                    </button>
                </div>
            </form>

            {/* Loading / Empty States */}
            {loading && documents.length === 0 && (
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {[...Array(8)].map((_, i) => (
                        <div key={i} className="bg-white rounded-xl shadow-lg overflow-hidden animate-pulse">
                            <div className="h-48 bg-gray-200"></div>
                            <div className="p-4">
                                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {!loading && documents.length === 0 && (
                <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
                    <FileText className="w-24 h-24 mx-auto text-gray-200 mb-6" />
                    <h3 className="text-2xl font-black text-gray-700 mb-2 tracking-tight">
                        {searchTerm ? 'Nenhum documento encontrado' : 'Ainda não tem documentos'}
                    </h3>
                    <p className="text-gray-500 max-w-md mx-auto font-medium">
                        {searchTerm
                            ? 'Tente outra palavra-chave ou verifique a ortografia.'
                            : 'Carregue o seu primeiro documento para começar.'
                        }
                    </p>
                </div>
            )}

            {/* Grid de Documentos */}
            {!loading && documents.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
                    {documents.map((doc) => (
                        <div
                            key={doc.id}
                            className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/40 overflow-hidden hover:shadow-2xl transition-all cursor-pointer glassmorphism border border-transparent hover:border-red-100 group"
                            onClick={() => setPreviewId(doc.id)}
                        >
                            {/* Thumbnail */}
                            <div className="relative overflow-hidden h-56">
                                {doc.thumbnail_url ? (
                                    <img
                                        src={doc.thumbnail_url}
                                        alt={doc.name}
                                        className="w-full h-full object-cover transition-transform group-hover:scale-110"
                                    />
                                ) : (
                                    <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                                        <FileText className="w-16 h-16 text-gray-300" />
                                    </div>
                                )}
                                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors" />
                            </div>

                            {/* Info */}
                            <div className="p-6">
                                <h3 className="font-black text-gray-900 truncate tracking-tight">{doc.name}</h3>
                                <p className="text-xs font-bold text-gray-400 mt-1 uppercase tracking-widest">
                                    {new Date(doc.created_at).toLocaleDateString('pt-AO')}
                                </p>
                                <div className="flex items-center justify-between mt-6">
                                    <span className={`text-[10px] font-black uppercase tracking-tighter px-3 py-1 rounded-full ${doc.status === 'ready' ? 'bg-green-100 text-green-800' :
                                            doc.status === 'processing' ? 'bg-amber-100 text-amber-800' :
                                                'bg-gray-100 text-gray-800'
                                        }`}>
                                        {doc.status === 'ready' ? '✓ Pronto' : doc.status === 'processing' ? '⌛ Em processamento' : doc.status}
                                    </span>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            downloadDocument(doc.id);
                                        }}
                                        className="p-3 bg-gray-50 hover:bg-red-50 text-gray-400 hover:text-red-600 rounded-xl transition-all"
                                        title="Descarregar"
                                    >
                                        <Download className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Preview Modal */}
            {previewId && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setPreviewId(null)}>
                    <div className="bg-white rounded-[2.5rem] max-w-5xl w-full max-h-[90vh] overflow-hidden shadow-2xl animate-in zoom-in-95 duration-200" onClick={e => e.stopPropagation()}>
                        <div className="flex items-center justify-between p-6 border-b border-gray-100">
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-red-50 rounded-2xl">
                                    <FileText className="w-6 h-6 text-red-600" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-black text-gray-900 tracking-tight">Pré-visualização</h3>
                                    <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Documento ID #{previewId}</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setPreviewId(null)}
                                className="p-3 hover:bg-gray-100 rounded-2xl transition-colors text-gray-400 hover:text-gray-900"
                            >
                                <X className="w-8 h-8" />
                            </button>
                        </div>
                        <div className="bg-gray-50 h-[70vh]">
                            <iframe
                                src={`/api/v1/documents/${previewId}/download`}
                                className="w-full h-full border-none"
                                title="Preview"
                            />
                        </div>
                        <div className="p-6 border-t border-gray-100 flex justify-end gap-4">
                            <button
                                onClick={() => setPreviewId(null)}
                                className="px-8 py-3 rounded-xl font-bold text-gray-500 hover:bg-gray-50 transition"
                            >
                                Fechar
                            </button>
                            <button
                                onClick={() => downloadDocument(previewId)}
                                className="px-8 py-3 bg-red-600 text-white rounded-xl font-bold flex items-center gap-2 hover:bg-red-700 transition shadow-lg shadow-red-100"
                            >
                                <Download className="w-5 h-5" />
                                Descarregar PDF
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MyDocuments;
