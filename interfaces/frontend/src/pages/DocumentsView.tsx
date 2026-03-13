// apps/frontend/src/pages/DocumentsView.tsx
import { useEffect, useState, useCallback } from "react";
import api from "@/services/api";
import { DocumentCard } from "@/components/Documents/DocumentCard";
import { useDocumentStatus, type StatusUpdate } from "@/hooks/useDocumentStatus";

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

export const DocumentsView = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/documents/me")
            .then(res => setDocuments(res.data))
            .finally(() => setLoading(false));
    }, []);

    const handleStatusUpdate = useCallback((updates: StatusUpdate[]) => {
        setDocuments(prev =>
            prev.map(doc => {
                const update = updates.find(u => u.id === doc.id);
                return update ? { ...doc, status: update.status as any } : doc;
            })
        );
    }, []);

    useDocumentStatus(handleStatusUpdate);

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12">
            <div className="max-w-7xl mx-auto px-4">
                <h1 className="text-4xl font-black text-gray-800 mb-12">Meus Documentos</h1>

                {loading ? (
                    <div className="text-center py-20 text-gray-500">Carregando documentos...</div>
                ) : documents.length === 0 ? (
                    <div className="text-center py-20 text-gray-500 text-xl">Nenhum documento encontrado.</div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {documents.map(doc => (
                            <DocumentCard key={doc.id} document={doc as any} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};
