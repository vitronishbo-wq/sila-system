import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { UploadZone } from "@/components/Upload/UploadZone";
import { DocumentsView } from "@/pages/DocumentsView";
import { CheckoutCard } from "@/components/Payment/CheckoutCard";
import { operationsService } from "@/modules/operations/services";
import CitizenAreaBanner from "@/components/Services/CitizenAreaBanner";

export const UploadDocuments = () => {
    const [refreshKey, setRefreshKey] = useState(0);
    const [pendingPayment, setPendingPayment] = useState<{ amount: number; reference: string; description: string } | null>(null);
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const orderId = searchParams.get('orderId');
    const serviceParam = searchParams.get('service') ?? '';
    const uploadFields = searchParams.get('uploadFields');
    const uploadFieldList = uploadFields ? uploadFields.split(',').filter(Boolean) : [];

    const guessContentType = (fileName: string) => {
        const ext = fileName.split('.').pop()?.toLowerCase();
        if (ext === 'pdf') return 'application/pdf';
        if (ext === 'png') return 'image/png';
        if (ext === 'jpg' || ext === 'jpeg') return 'image/jpeg';
        return 'application/octet-stream';
    };

    const handleUploadSuccess = (backendResponse: any) => {
        setRefreshKey(prev => prev + 1);

        if (orderId) {
            const fileName = backendResponse?.fileName ?? 'documento.pdf';
            const documentId = backendResponse?.documentId ?? `doc-${Date.now()}`;
            const payload = {
                documents: [
                    {
                        filename: fileName,
                        content_type: guessContentType(fileName),
                        size_bytes: backendResponse?.size_bytes ?? 0,
                        uri: documentId
                    }
                ]
            };

            operationsService.attachDocuments(orderId, payload).then(() => {
                navigate(`/citizen/payments?service=${serviceParam}&orderId=${orderId}`);
            }).catch((err) => {
                console.error('Falha ao anexar documentos ao pedido:', err);
            });
            return;
        }

        // Em produção, capturamos os dados reais de faturação retornados pelo backend
        setPendingPayment({
            amount: backendResponse?.fee || 15000,
            reference: backendResponse?.payment_ref || `PAY-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
            description: "Processamento de Documentação Governamental"
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
            <CitizenAreaBanner />
            <div className="py-12 px-4">
                {uploadFieldList.length > 0 && (
                    <div className="max-w-4xl mx-auto mb-6 bg-blue-50 border border-blue-200 text-blue-800 text-sm rounded-xl px-4 py-3">
                        Anexos solicitados: {uploadFieldList.join(', ')}.
                    </div>
                )}
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

export default UploadDocuments;
