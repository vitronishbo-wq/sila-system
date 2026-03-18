import { useState } from "react";
import { Copy, CheckCircle, Loader2, CreditCard } from "lucide-react";
import { toast } from "react-hot-toast";
import api from "@/services/api";

interface CheckoutProps {
    amount: number;
    reference: string;
    description: string;
    onPaymentSuccess?: () => void;
}

export const CheckoutCard = ({ amount, reference, description, onPaymentSuccess }: CheckoutProps) => {
    const [copied, setCopied] = useState(false);
    const [loading, setLoading] = useState(false);

    const copyReference = () => {
        if (!navigator.clipboard) {
            toast.error("Clipboard não suportado neste navegador");
            return;
        }
        navigator.clipboard.writeText(reference);
        setCopied(true);
        toast.success("Referência copiada!");
        setTimeout(() => setCopied(false), 2000);
    };

    const verifyPayment = async () => {
        setLoading(true);
        try {
            // Chamada real para o backend verificar o status da transação
            const response = await api.get(`/payments/verify/${reference}`);

            if (response.data.status === "PAID") {
                toast.success("Pagamento confirmado via Multicaixa!");
                onPaymentSuccess?.();
            } else {
                toast.error("Pagamento ainda não detetado. Tente daqui a instantes.");
            }
        } catch (err: any) {
            // Se ainda em modo dev, mantemos o fallback de simulação
            if (import.meta.env.DEV) {
                console.warn("API de pagamento real não encontrada, simulando...");
                await new Promise(resolve => setTimeout(resolve, 1500));
                toast.success("Simulação: Pagamento aceite!");
                onPaymentSuccess?.();
            } else {
                toast.error(err.response?.data?.detail || "Erro ao verificar pagamento");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden max-w-md mx-auto border border-gray-100 animate-in zoom-in-95 duration-300">
            {/* Header com Identidade Visual */}
            <div className="bg-gradient-to-br from-red-700 via-red-600 to-red-800 text-white p-8 text-center relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <CreditCard size={120} />
                </div>
                <h2 className="text-2xl font-black uppercase tracking-tight">Pagamento Multicaixa</h2>
                <p className="text-sm mt-1 font-medium text-red-100 uppercase tracking-widest">{description}</p>
            </div>

            <div className="p-8 space-y-8">
                {/* Valor Formatado */}
                <div className="text-center">
                    <p className="text-gray-500 text-sm font-bold uppercase tracking-wider">Total a Liquidar</p>
                    <p className="text-5xl font-black text-gray-900 mt-2">
                        {amount.toLocaleString("pt-AO", { style: "currency", currency: "AOA" })}
                    </p>
                </div>

                {/* Bloco de Referência */}
                <div className="bg-gray-50 border border-gray-100 p-6 rounded-2xl text-center shadow-inner">
                    <p className="text-xs text-gray-400 font-bold uppercase mb-3">Referência (Entidade 00001)</p>
                    <div className="flex items-center justify-center gap-4">
                        <code className="text-3xl font-black text-red-600 tracking-tighter">{reference}</code>
                        <button
                            onClick={copyReference}
                            className="p-3 bg-white hover:bg-gray-100 border border-gray-200 rounded-xl transition-all shadow-sm active:scale-95"
                            title="Copiar Referência"
                        >
                            {copied ? (
                                <CheckCircle className="h-6 w-6 text-green-600" />
                            ) : (
                                <Copy className="h-6 w-6 text-gray-400" />
                            )}
                        </button>
                    </div>
                </div>

                {/* Instruções */}
                <div className="space-y-3 bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                    <div className="flex gap-3 text-sm text-blue-800">
                        <span className="font-bold">1.</span>
                        <p>Vá ao Menu <b>Pagamentos</b> no Multicaixa ou App.</p>
                    </div>
                    <div className="flex gap-3 text-sm text-blue-800">
                        <span className="font-bold">2.</span>
                        <p>Selecione <b>Pagamentos por Referência</b>.</p>
                    </div>
                </div>

                {/* Botão de Verificação */}
                <button
                    onClick={verifyPayment}
                    disabled={loading}
                    className="w-full bg-gray-900 text-white py-5 rounded-2xl font-black text-lg hover:bg-black transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-xl"
                >
                    {loading ? (
                        <>
                            <Loader2 className="h-6 w-6 animate-spin" />
                            A Verificar Transação...
                        </>
                    ) : (
                        "Já efetuei o Pagamento"
                    )}
                </button>
            </div>
        </div>
    );
};