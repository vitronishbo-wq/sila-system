import { useEffect, useRef } from "react";
import { API_V1_BASE_URL } from "@/utils/runtime";

const API_BASE_URL = API_V1_BASE_URL;

export interface StatusUpdate {
    id: string;
    status: string;
}

/**
 * Hook para escutar atualizações de status de documentos em tempo real via SSE.
 * @param onUpdate Callback executado quando novas atualizações chegam.
 */
export const useDocumentStatus = (onUpdate: (updates: StatusUpdate[]) => void) => {
    // Mantemos o timestamp do último update para evitar duplicatas em reconexões
    const lastSeenRef = useRef<number>(Math.floor(Date.now() / 1000));

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (!token) return;

        // Constrói a URL com token para autenticação (SSE não suporta headers customizados)
        // E o timestamp de última visualização para sincronização inteligente
        const streamUrl = `${API_BASE_URL}/documents/status-stream?token=${token}&last_seen=${lastSeenRef.current}`;

        let eventSource: EventSource | null = new EventSource(streamUrl);

        // Ouvinte para o evento customizado 'update' definido no backend
        eventSource.addEventListener("update", (e: MessageEvent) => {
            if (e.data) {
                try {
                    const updates = JSON.parse(e.data) as StatusUpdate[];
                    if (updates && updates.length > 0) {
                        onUpdate(updates);
                        // Atualiza o timestamp de referência
                        lastSeenRef.current = Math.floor(Date.now() / 1000);
                    }
                } catch (err) {
                    console.error("Erro ao processar mensagem SSE:", err);
                }
            }
        });

        eventSource.onopen = () => {
            console.log("Fluxo de status em tempo real conectado.");
        };

        eventSource.onerror = (err) => {
            console.error("Erro na conexão SSE. O navegador tentará reconectar automaticamente.", err);
        };

        // Cleanup ao desmontar o componente
        return () => {
            if (eventSource) {
                eventSource.close();
            }
        };
    }, [onUpdate]);
};
