import { useState, useEffect } from 'react';
import api from '@/api/axios';

interface Document {
    id: number;
    name: string;
    status: string;
    thumbnail_url?: string;
    created_at: string;
    size: number;
    ocr_text?: string;
}

export const useMyDocuments = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    // Lista todos os documentos do utilizador
    const fetchDocuments = async () => {
        try {
            setLoading(true);
            const data = await api.get('/documents/me') as any;
            setDocuments(data.documents || data);
        } catch (err) {
            console.error('Erro ao carregar documentos:', err);
        } finally {
            setLoading(false);
        }
    };

    // Pesquisa profunda por OCR
    const searchDocuments = async (query: string) => {
        if (!query.trim()) {
            fetchDocuments();
            return;
        }

        try {
            setSearching(true);
            const data = await api.get('/documents/search/deep', { params: { q: query } }) as any;
            setDocuments(data.results || data);
        } catch (err) {
            console.error('Erro na pesquisa OCR:', err);
            setDocuments([]);
        } finally {
            setSearching(false);
        }
    };

    // Download
    const downloadDocument = async (id: number) => {
        try {
            const response = await api.get(`/documents/${id}/download`, { responseType: 'blob' }) as any;
            const downloadUrl = window.URL.createObjectURL(new Blob([response]));
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', `documento_${id}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(downloadUrl);
        } catch (err) {
            console.error('Erro no download:', err);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    return {
        documents,
        loading: loading || searching,
        searchTerm,
        setSearchTerm,
        searchDocuments,
        downloadDocument,
        refresh: fetchDocuments,
    };
};
