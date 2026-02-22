import { useState } from "react";
import { UploadZone } from "@/components/Upload/UploadZone";
import { DocumentsView } from "@/pages/DocumentsView";
import { CheckoutCard } from "@/components/Payment/CheckoutCard";

export const UploadDocuments = () => {
    const [refreshKey, setRefreshKey] = useState(0);
    const [pendingPayment, setPendingPayment] = useState<{ amount: number; reference: string; description: string } | null>(null);

    const handleUploadSuccess = (backendResponse: any) => {
        setRefreshKey(prev => prev + 1);

        // Em produção, capturamos os dados reais de faturação retornados pelo backend
        setPendingPayment({
            amount: backendResponse?.fee || 15000,
            reference: backendResponse?.payment_ref || `PAY-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
            description: "Processamento de Documentação Governamental"
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
            <div className="py-12 px-4">
                <h1 className="text-4xl font-black text-center text-gray-800 mb-12 uppercase tracking-tight">
                    Portal de <span className="text-red-600">Documentos</span>
                </h1>

                {pendingPayment ? (
                    <div className="mb-12 animate-in fade-in slide-in-from-top-4 duration-500">
                        <CheckoutCard
                            {...pendingPayment}
                            onPaymentSuccess={() => {
                                setPendingPayment(null);
                                setRefreshKey(prev => prev + 1);
                            }}
                        />
                        <div className="text-center mt-6">
                            <button
                                onClick={() => setPendingPayment(null)}
                                className="text-gray-500 hover:text-red-600 font-medium transition"
                            >
                                ← Enviar mais documentos
                            </button>
                        </div>
                    </div>
                ) : (
                    <UploadZone onUploadSuccess={handleUploadSuccess} />
                )}
            </div>

            <div className="border-t border-gray-200 bg-white">
                <DocumentsView key={refreshKey} />
            </div>
        </div>
    );
};