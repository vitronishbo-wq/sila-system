import { useState, useEffect, useRef } from 'react';
import api from '@/api/axios';

interface UploadProgress {
    fileName: string;
    progress: number;
    status: 'pending' | 'uploading' | 'processing' | 'success' | 'error';
    documentId?: number;
    error?: string;
}

export const useDocumentUpload = () => {
    const [uploads, setUploads] = useState<UploadProgress[]>([]);

    // Ref para armazenar todas as conexões SSE ativas – permite limpeza ao desmontar
    const eventSourcesRef = useRef<Map<number, EventSource>>(new Map());

    // Limpeza automática ao desmontar o componente (prevenir memory leaks)
    useEffect(() => {
        return () => {
            eventSourcesRef.current.forEach(es => es.close());
            eventSourcesRef.current.clear();
        };
    }, []);

    const uploadFile = async (file: File) => {
        // 1. Validação client-side (economia de dados + UX imediata)
        const MAX_SIZE = 20 * 1024 * 1024; // 20MB
        const ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/png'];

        if (file.size > MAX_SIZE) {
            setUploads(prev => [...prev, {
                fileName: file.name,
                progress: 0,
                status: 'error',
                error: 'Ficheiro demasiado grande (máximo 20MB)'
            }]);
            return;
        }

        if (!ALLOWED_TYPES.includes(file.type)) {
            setUploads(prev => [...prev, {
                fileName: file.name,
                progress: 0,
                status: 'error',
                error: 'Formato não permitido. Use PDF, JPG ou PNG'
            }]);
            return;
        }

        const newUpload: UploadProgress = {
            fileName: file.name,
            progress: 0,
            status: 'pending',
        };
        setUploads(prev => [...prev, newUpload]);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post('/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                timeout: 120000,
                onUploadProgress: (progressEvent) => {
                    const percent = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
                    setUploads(prev =>
                        prev.map(u =>
                            u.fileName === file.name
                                ? { ...u, progress: percent, status: 'uploading' }
                                : u
                        )
                    );
                },
            }) as any;

            const documentId = response.id;

            setUploads(prev =>
                prev.map(u =>
                    u.fileName === file.name
                        ? { ...u, progress: 100, status: 'processing', documentId }
                        : u
                )
            );

            // Inicia SSE para este documento específico
            listenToDocumentStatus(documentId);
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail ||
                err.message === 'timeout' ? 'Tempo esgotado – tente novamente' :
                'Erro no upload – verifique a ligação';

            setUploads(prev =>
                prev.map(u =>
                    u.fileName === file.name
                        ? { ...u, status: 'error', error: errorMsg }
                        : u
                )
            );
        }
    };

    const listenToDocumentStatus = (documentId: number) => {
        // Evita múltiplas conexões para o mesmo documento
        if (eventSourcesRef.current.has(documentId)) {
            eventSourcesRef.current.get(documentId)!.close();
        }

        const apiUrl = import.meta.env.VITE_API_URL || '';
        const eventSource = new EventSource(`${apiUrl}/documents/status-stream`);

        // Timeout manual: se não houver update em 90s, assume falha
        const timeoutId = setTimeout(() => {
            eventSource.close();
            eventSourcesRef.current.delete(documentId);
            setUploads(prev =>
                prev.map(u =>
                    u.documentId === documentId
                        ? { ...u, status: 'error', error: 'Processamento demorou demais – tente novamente' }
                        : u
                )
            );
        }, 90000);

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.document_id === documentId) {
                    clearTimeout(timeoutId);

                    if (data.status === 'ready' || data.status === 'completed') {
                        setUploads(prev =>
                            prev.map(u =>
                                u.documentId === documentId
                                    ? { ...u, progress: 100, status: 'success' }
                                    : u
                            )
                        );
                        eventSource.close();
                        eventSourcesRef.current.delete(documentId);
                    } else if (data.status === 'failed') {
                        setUploads(prev =>
                            prev.map(u =>
                                u.documentId === documentId
                                    ? { ...u, status: 'error', error: data.message || 'Processamento falhou' }
                                    : u
                            )
                        );
                        eventSource.close();
                        eventSourcesRef.current.delete(documentId);
                    }
                }
            } catch (e) {
                console.error('Erro ao processar SSE:', e);
            }
        };

        eventSource.onerror = () => {
            clearTimeout(timeoutId);
            eventSource.close();
            eventSourcesRef.current.delete(documentId);
            setUploads(prev =>
                prev.map(u =>
                    u.documentId === documentId
                        ? { ...u, status: 'error', error: 'Ligação perdida durante processamento' }
                        : u
                )
            );
        };

        eventSourcesRef.current.set(documentId, eventSource);
    };

    // Função auxiliar para cancelar upload (opcional futuro)
    const cancelUpload = (documentId?: number, fileName?: string) => {
        if (documentId && eventSourcesRef.current.has(documentId)) {
            eventSourcesRef.current.get(documentId)!.close();
            eventSourcesRef.current.delete(documentId);
        }
        setUploads(prev => prev.filter(u => u.documentId !== documentId && u.fileName !== fileName));
    };

    return { uploads, uploadFile, cancelUpload };
};
