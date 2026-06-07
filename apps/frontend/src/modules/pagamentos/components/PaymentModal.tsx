
import React, { useEffect, useState } from 'react';
import { 
  X, 
  CreditCard, 
  QrCode, 
  Copy, 
  CheckCircle2, 
  Loader2,
  Download,
  ArrowRight,
  Info
} from 'lucide-react';
import { operationsService } from '@/modules/operations/services';
import type { Service as ApiService } from '@/types/api';

interface DisplayService extends ApiService {
  icon: React.ReactNode;
  color: string;
}

interface PaymentModalProps {
  service: DisplayService;
  onClose: () => void;
  initialOrderId?: string;
}

type PaymentStep = 'method' | 'processing' | 'result';
type PaymentMethod = 'reference' | 'qrcode';

const PaymentModal: React.FC<PaymentModalProps> = ({ service, onClose, initialOrderId }) => {
  const [step, setStep] = useState<PaymentStep>('method');
  const [method, setMethod] = useState<PaymentMethod | null>(null);
  const [copied, setCopied] = useState(false);
  const [orderId, setOrderId] = useState<string | null>(initialOrderId ?? null);
  const [paymentReference, setPaymentReference] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isConfirming, setIsConfirming] = useState(false);
  const [confirmMessage, setConfirmMessage] = useState<string | null>(null);
  const [confirmError, setConfirmError] = useState<string | null>(null);

  const amount = service.price;
  const entity = "00001";

  const formatAmount = (value: number) => value.toLocaleString('pt-AO', {
    style: 'currency',
    currency: 'AOA'
  });

  useEffect(() => {
    if (initialOrderId) {
      setOrderId(initialOrderId);
    }
  }, [initialOrderId]);

  const ensurePaymentReference = async (): Promise<string> => {
    if (paymentReference) {
      return paymentReference;
    }

    let currentOrderId = orderId;
    if (!currentOrderId) {
      const order = await operationsService.createOrder({ service_id: service.id });
      currentOrderId = order.id;
      setOrderId(order.id);
    }

    const payment = await operationsService.generatePayment(currentOrderId);
    setPaymentReference(payment.reference);
    return payment.reference;
  };

  const handleSelectMethod = async (m: PaymentMethod) => {
    setMethod(m);
    setStep('processing');
    setError(null);
    setConfirmMessage(null);
    setConfirmError(null);

    try {
      await ensurePaymentReference();
      setStep('result');
    } catch (err) {
      console.error('Falha ao gerar pagamento:', err);
      setError('Não foi possível gerar o pagamento agora. Tente novamente.');
      setStep('method');
    }
  };

  const handleConfirmPayment = async () => {
    if (!paymentReference) {
      setConfirmError('Referência indisponível para confirmação.');
      return;
    }

    setIsConfirming(true);
    setConfirmMessage(null);
    setConfirmError(null);

    try {
      const payment = await operationsService.confirmPayment(paymentReference);
      const status = payment.status?.toUpperCase();

      if (status === 'CONFIRMED' || status === 'PAID') {
        setConfirmMessage('Pagamento confirmado via Multicaixa!');
      } else {
        setConfirmError('Pagamento ainda não detetado. Tente daqui a instantes.');
      }
    } catch (err) {
      console.error('Erro ao confirmar pagamento:', err);
      setConfirmError('Erro ao verificar pagamento.');
    } finally {
      setIsConfirming(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadProof = () => {
    const content = `COMPROVANTE DE PAGAMENTO\n\nServiço: ${service.name}\nValor: ${formatAmount(amount)}\nEntidade: ${entity}\nReferência: ${paymentReference ?? 'N/D'}\nData: ${new Date().toLocaleDateString('pt-PT')}\nMétodo: ${method === 'reference' ? 'Referência' : 'QR Code'}\n\nProcessado via SILA-System v2026.1`;
    const element = document.createElement('a');
    element.setAttribute('href', `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`);
    const safeReference = (paymentReference ?? 'sem-referencia').replace(/\s/g, '');
    element.setAttribute('download', `comprovante-${safeReference}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleShare = (platform: 'whatsapp' | 'email' | 'copy') => {
    const text = `Referência de Pagamento: ${paymentReference ?? 'N/D'}\nEntidade: ${entity}\nValor: ${formatAmount(amount)}`;
    if (platform === 'whatsapp') {
      window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    } else if (platform === 'email') {
      window.open(`mailto:?subject=Referência de Pagamento&body=${encodeURIComponent(text)}`, '_blank');
    } else if (platform === 'copy') {
      copyToClipboard(text);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white w-full max-w-lg rounded-3xl overflow-hidden shadow-2xl animate-in fade-in zoom-in duration-300">
        {/* Header */}
        <div className="bg-[#1a202c] p-6 text-white flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className={`${service.color} p-2 rounded-lg`}>
              {React.cloneElement(service.icon as React.ReactElement, { className: 'w-5 h-5 text-white' })}
            </div>
            <div>
              <h4 className="font-bold text-lg leading-none">{service.name}</h4>
              <p className="text-xs text-gray-400 mt-1">Taxa de Emissão de Documento</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-8">
          {step === 'method' && (
            <div className="space-y-6">
              <div className="text-center">
                <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Valor a Pagar</span>
                <h2 className="text-4xl font-extrabold text-gray-900 mt-1">{formatAmount(amount)}</h2>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-4">
                <button 
                  onClick={() => handleSelectMethod('reference')}
                  className="group flex flex-col items-center gap-4 p-6 border-2 border-gray-100 rounded-2xl hover:border-yellow-500 hover:bg-yellow-50 transition-all"
                >
                  <div className="bg-blue-100 text-blue-600 p-4 rounded-full group-hover:bg-yellow-100 group-hover:text-yellow-600 transition-colors">
                    <CreditCard className="w-8 h-8" />
                  </div>
                  <span className="font-bold text-gray-700">Referência</span>
                </button>

                <button 
                  onClick={() => handleSelectMethod('qrcode')}
                  className="group flex flex-col items-center gap-4 p-6 border-2 border-gray-100 rounded-2xl hover:border-yellow-500 hover:bg-yellow-50 transition-all"
                >
                  <div className="bg-purple-100 text-purple-600 p-4 rounded-full group-hover:bg-yellow-100 group-hover:text-yellow-600 transition-colors">
                    <QrCode className="w-8 h-8" />
                  </div>
                  <span className="font-bold text-gray-700">QR Code</span>
                </button>
              </div>

              <div className="flex items-start gap-3 bg-gray-50 p-4 rounded-xl border border-gray-100">
                <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-600">
                  Os pagamentos são processados via rede Multicaixa. A referência é válida por 48 horas.
                </p>
              </div>
              {error && (
                <div className="bg-red-50 text-red-700 border border-red-200 p-3 rounded-lg text-sm">
                  {error}
                </div>
              )}
            </div>
          )}

          {step === 'processing' && (
            <div className="py-12 flex flex-col items-center text-center">
              <div className="w-16 h-16 border-4 border-gray-100 border-t-yellow-500 rounded-full animate-spin mb-6"></div>
              <h3 className="text-xl font-bold text-gray-900">Gerando sua {method === 'reference' ? 'referência' : 'QR Code'}...</h3>
              <p className="text-gray-500 mt-2">Isso levará apenas alguns segundos.</p>
            </div>
          )}

          {step === 'result' && (
            <div className="space-y-6">
              <div className="flex items-center justify-center gap-2 text-green-600 bg-green-50 py-2 rounded-full w-40 mx-auto">
                <CheckCircle2 className="w-5 h-5" />
                <span className="text-sm font-bold uppercase tracking-tight">Gerado com Sucesso</span>
              </div>

              {method === 'reference' ? (
                <div className="space-y-4">
                  <div className="bg-gray-50 rounded-2xl p-6 border-2 border-dashed border-gray-200">
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-gray-500 text-sm">Entidade</span>
                      <span className="font-mono font-bold text-lg">{entity}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-500 text-sm">Referência</span>
                      <div className="flex items-center gap-3">
                        <span
                          className="font-mono font-bold text-xl tracking-wider cursor-pointer p-2 hover:bg-gray-100 rounded-lg transition-colors"
                          onClick={() => paymentReference && copyToClipboard(paymentReference)}
                          title="Clique para copiar"
                        >
                          {paymentReference ?? '--- --- ---'}
                        </span>
                        <button 
                          onClick={() => paymentReference && copyToClipboard(paymentReference)}
                          className="p-2 hover:bg-gray-200 rounded-lg transition-colors text-blue-600"
                          title="Copiar referência"
                        >
                          {copied ? <CheckCircle2 className="w-5 h-5 text-green-600" /> : <Copy className="w-5 h-5" />}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                   <div
                     className="p-6 bg-white border-2 border-gray-100 rounded-3xl shadow-inner mb-4 hover:border-blue-300 transition-colors cursor-pointer group relative"
                     onClick={() => paymentReference && copyToClipboard(paymentReference)}
                     title="Clique para copiar dados do QR Code"
                   >
                      <img 
                        src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${paymentReference ?? ''}`} 
                        alt="QR Code Pagamento" 
                        className="w-48 h-48 group-hover:opacity-80 transition-opacity"
                      />
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl">
                        <span className="bg-black/60 text-white px-3 py-1 rounded-lg text-xs font-semibold">Copiar dados</span>
                      </div>
                   </div>
                   <p className="text-sm text-gray-500 text-center">Aponte a câmera do seu aplicativo Multicaixa Express para este QR Code</p>
                </div>
              )}

              <div className="bg-blue-600 text-white rounded-2xl p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-blue-200 uppercase font-bold tracking-wider">Total em Kwanza</p>
                    <p className="text-2xl font-black">{formatAmount(amount)}</p>
                  </div>
                  <button onClick={handleDownloadProof} className="bg-white/10 hover:bg-white/20 p-3 rounded-xl transition-all" title="Descarregar comprovante">
                    <Download className="w-6 h-6" />
                  </button>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleShare('whatsapp')} className="flex-1 bg-white/10 hover:bg-white/20 px-3 py-2 rounded-lg transition-all text-xs font-semibold" title="Partilhar via WhatsApp">WhatsApp</button>
                  <button onClick={() => handleShare('email')} className="flex-1 bg-white/10 hover:bg-white/20 px-3 py-2 rounded-lg transition-all text-xs font-semibold" title="Enviar via Email">Email</button>
                  <button onClick={() => handleShare('copy')} className="flex-1 bg-white/10 hover:bg-white/20 px-3 py-2 rounded-lg transition-all text-xs font-semibold" title="Copiar dados">Copiar</button>
                </div>
              </div>

              {(confirmMessage || confirmError) && (
                <div className={`p-4 rounded-xl text-sm font-semibold ${confirmMessage ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}`}>
                  {confirmMessage ?? confirmError}
                </div>
              )}

              <div className="flex gap-3">
                <button
                  onClick={handleConfirmPayment}
                  disabled={isConfirming}
                  className="flex-1 bg-gray-900 text-white font-bold py-4 rounded-2xl hover:bg-gray-800 transition-all flex items-center justify-center gap-2 shadow-lg disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {isConfirming ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      A confirmar...
                    </>
                  ) : (
                    'Já efetuei o Pagamento'
                  )}
                </button>
                <button 
                  onClick={onClose}
                  className="flex-1 bg-gray-200 text-gray-800 font-bold py-4 rounded-2xl hover:bg-gray-300 transition-all flex items-center justify-center gap-2 shadow-lg"
                >
                  Concluir <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaymentModal;
