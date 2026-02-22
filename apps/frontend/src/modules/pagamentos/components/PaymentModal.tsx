
import React, { useState } from 'react';
import { 
  X, 
  CreditCard, 
  QrCode, 
  Copy, 
  CheckCircle2, 
  Download,
  ArrowRight,
  Info
} from 'lucide-react';

interface Service {
  id: string;
  name: string;
  icon: React.ReactNode;
  color: string;
}

interface PaymentModalProps {
  service: Service;
  onClose: () => void;
}

type PaymentStep = 'method' | 'processing' | 'result';
type PaymentMethod = 'reference' | 'qrcode';

const PaymentModal: React.FC<PaymentModalProps> = ({ service, onClose }) => {
  const [step, setStep] = useState<PaymentStep>('method');
  const [method, setMethod] = useState<PaymentMethod | null>(null);
  const [copied, setCopied] = useState(false);

  const amount = "12.500,00";
  const entity = "00001";
  const reference = "123 456 789";

  const handleSelectMethod = (m: PaymentMethod) => {
    setMethod(m);
    setStep('processing');
    setTimeout(() => {
      setStep('result');
    }, 1500);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
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
                <h2 className="text-4xl font-extrabold text-gray-900 mt-1">{amount} <span className="text-xl font-normal text-gray-500">AOA</span></h2>
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
                        <span className="font-mono font-bold text-xl tracking-wider">{reference}</span>
                        <button 
                          onClick={() => copyToClipboard(reference)}
                          className="p-2 hover:bg-gray-200 rounded-lg transition-colors text-blue-600"
                        >
                          {copied ? <CheckCircle2 className="w-5 h-5 text-green-600" /> : <Copy className="w-5 h-5" />}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                   <div className="p-6 bg-white border-2 border-gray-100 rounded-3xl shadow-inner mb-4">
                      <img 
                        src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${reference}`} 
                        alt="QR Code Pagamento" 
                        className="w-48 h-48"
                      />
                   </div>
                   <p className="text-sm text-gray-500 text-center">Aponte a câmera do seu aplicativo Multicaixa Express para este QR Code</p>
                </div>
              )}

              <div className="bg-blue-600 text-white rounded-2xl p-6 flex items-center justify-between">
                <div>
                  <p className="text-xs text-blue-200 uppercase font-bold tracking-wider">Total em Kwanza</p>
                  <p className="text-2xl font-black">{amount} AOA</p>
                </div>
                <button className="bg-white/10 hover:bg-white/20 p-3 rounded-xl transition-all">
                  <Download className="w-6 h-6" />
                </button>
              </div>

              <div className="flex gap-3">
                <button 
                  onClick={onClose}
                  className="flex-1 bg-gray-900 text-white font-bold py-4 rounded-2xl hover:bg-gray-800 transition-all flex items-center justify-center gap-2 shadow-lg"
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
