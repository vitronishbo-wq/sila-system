// apps/frontend/src/components/Dashboard/DocumentsTable.tsx
import { useEffect, useState } from "react";
import api from "@/services/api"; // Retificado: adicionado chaves para named import
import { FileText, Download, Clock, Eye } from "lucide-react";

interface DocumentVersion {
    version_number: number;
    uploaded_at: string;
    file_size: number;
}

interface Document {
    id: string;
    title: string;
    filename: string;
    file_type: string;
    created_at: string;
    current_version: DocumentVersion;
}

export const DocumentsTable = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/documents/me")
            .then((res: { data: Document[] }) => setDocuments(res.data)) // Retificado: tipagem do parâmetro res
            .catch((err) => console.error("Erro ao carregar documentos:", err))
            .finally(() => setLoading(false));
    }, []);

    const formatSize = (bytes: number) => {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / 1048576).toFixed(1) + " MB";
    };

    if (loading) return <div className="text-center py-12">Carregando documentos...</div>;

    return (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-red-700 to-red-600 text-white p-6">
                <h2 className="text-2xl font-bold flex items-center gap-3">
                    <FileText className="h-8 w-8" />
                    Meus Documentos
                </h2>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead className="bg-gray-50 border-b-2 border-gray-200">
                        <tr>
                            <th className="text-left p-4 font-semibold text-gray-700">Documento</th>
                            <th className="text-left p-4 font-semibold text-gray-700">Versão Atual</th>
                            <th className="text-left p-4 font-semibold text-gray-700">Tamanho</th>
                            <th className="text-left p-4 font-semibold text-gray-700">Emitido em</th>
                            <th className="text-center p-4 font-semibold text-gray-700">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {documents.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="text-center py-12 text-gray-500">
                                    Nenhum documento encontrado.
                                </td>
                            </tr>
                        ) : (
                            documents.map((doc) => (
                                <tr key={doc.id} className="border-b hover:bg-gray-50 transition">
                                    <td className="p-4">
                                        <div className="flex items-center gap-3">
                                            <FileText className="h-10 w-10 text-red-600" />
                                            <div>
                                                <p className="font-medium text-gray-900">{doc.title}</p>
                                                <p className="text-sm text-gray-500">{doc.filename}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="p-4">
                                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                                            v{doc.current_version.version_number}
                                        </span>
                                    </td>
                                    <td className="p-4 text-gray-600">
                                        {formatSize(doc.current_version.file_size)}
                                    </td>
                                    <td className="p-4 text-gray-600">
                                        {new Date(doc.created_at).toLocaleDateString("pt-AO")}
                                    </td>
                                    <td className="p-4">
                                        <div className="flex items-center justify-center gap-3">
                                            <button className="p-2 hover:bg-gray-100 rounded-lg transition" title="Baixar">
                                                <Download className="h-5 w-5 text-green-600" />
                                            </button>
                                            <button className="p-2 hover:bg-gray-100 rounded-lg transition" title="Visualizar">
                                                <Eye className="h-5 w-5 text-blue-600" />
                                            </button>
                                            <button className="p-2 hover:bg-gray-100 rounded-lg transition" title="Histórico">
                                                <Clock className="h-5 w-5 text-gray-600" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};