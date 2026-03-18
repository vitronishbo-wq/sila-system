// apps/frontend/src/components/Documents/DocumentCard.tsx
import { useState } from "react";
import { FileText, Download, Loader2, Eye, AlertCircle } from "lucide-react";
import api from "@/services/api";

interface Document {
    id: string; // UUID
    original_filename: string;
    content_type: string;
    file_size: number;
    status: "pending" | "processing" | "completed" | "failed";
    created_at: string;
    thumbnail_url?: string;
    ocr_url?: string;
    download_url: string;
}

export const DocumentCard = ({ document }: { document: Document }) => {
    const [showOcr, setShowOcr] = useState(false);
    const [ocrText, setOcrText] = useState<string | null>(null);
    const [loadingOcr, setLoadingOcr] = useState(false);

    const formatSize = (bytes: number) => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / 1048576).toFixed(1)} MB`;
    };

    const loadOcr = async () => {
        if (ocrText || loadingOcr || !document.id) return;
        setLoadingOcr(true);
        try {
            const res = await api.get(`/documents/${document.id}/ocr`, {
                responseType: 'text'
            });
            setOcrText(res.data);
            setShowOcr(true);
        } catch (err) {
            console.error("Erro ao carregar OCR:", err);
            setOcrText("Erro ao carregar texto OCR. Verifique sua conexão ou se o processamento foi concluído.");
            setShowOcr(true);
        } finally {
            setLoadingOcr(false);
        }
    };

    const statusConfig: Record<string, { color: string; icon: any; label: string; spin?: boolean }> = {
        pending: { color: "bg-gray-100 text-gray-700", icon: Loader2, label: "Pendente" },
        processing: { color: "bg-yellow-100 text-yellow-700", icon: Loader2, label: "Processando...", spin: true },
        completed: { color: "bg-green-100 text-green-700", icon: FileText, label: "Concluído" },
        failed: { color: "bg-red-100 text-red-700", icon: AlertCircle, label: "Falhou" },
    };

    const config = statusConfig[document.status] || statusConfig.pending;

    return (
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-all duration-300">
            <div className="relative h-72 bg-gray-50 flex items-center justify-center">
                {document.status === "completed" ? (
                    <img
                        src={`${import.meta.env.VITE_API_URL}/documents/${document.id}/thumbnail`}
                        alt="Preview"
                        className="max-h-full max-w-full object-contain"
                        loading="lazy"
                    />
                ) : (
                    <div className="flex flex-col items-center text-gray-400">
                        <FileText className="h-24 w-24 mb-4" />
                        <p className="text-xl font-medium">{config.label}</p>
                        {config.spin && <config.icon className="h-10 w-10 mt-4 animate-spin" />}
                    </div>
                )}
            </div>

            <div className="p-6">
                <h3 className="font-bold text-xl text-gray-800 truncate">{document.original_filename}</h3>
                <div className="flex items-center gap-2 mt-2 text-sm text-gray-600">
                    <span>{formatSize(document.file_size)}</span>
                    <span>•</span>
                    <span>{new Date(document.created_at).toLocaleDateString("pt-AO")}</span>
                </div>

                <div className={`inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-full text-sm font-medium ${config.color}`}>
                    <config.icon className={`h-5 w-5 ${config.spin ? "animate-spin" : ""}`} />
                    {config.label}
                </div>

                <div className="flex items-center gap-3 mt-6">
                    <a
                        href={document.download_url}
                        className="flex-1 bg-red-600 text-white py-3 rounded-xl font-bold hover:bg-red-700 transition flex items-center justify-center gap-2"
                    >
                        <Download className="h-5 w-5" />
                        Baixar
                    </a>

                    {document.ocr_url && (
                        <button
                            onClick={loadOcr}
                            disabled={loadingOcr}
                            className="px-6 py-3 bg-gray-100 rounded-xl font-bold hover:bg-gray-200 transition flex items-center gap-2"
                        >
                            {loadingOcr ? <Loader2 className="h-5 w-5 animate-spin" /> : <Eye className="h-5 w-5" />}
                            OCR
                        </button>
                    )}
                </div>

                {showOcr && ocrText && (
                    <div className="mt-6 p-4 bg-gray-50 rounded-xl max-h-80 overflow-y-auto">
                        <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">{ocrText}</pre>
                    </div>
                )}
            </div>
        </div>
    );
};
