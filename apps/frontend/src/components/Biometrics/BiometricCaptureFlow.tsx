import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';
import BiometricCapture from './BiometricCapture';
import BiometricQualityCheck from './BiometricQualityCheck';

type BiometricStep = 'instructions' | 'capture' | 'quality-check' | 'processing' | 'success' | 'error';

interface BiometricCaptureFlowProps {
  modalityType: 'facial' | 'fingerprint' | 'iris';
  onSuccess: (biometricData: Blob, metadata: BiometricMetadata) => void;
  onCancel: () => void;
}

interface BiometricMetadata {
  modalityType: string;
  captureTimestamp: string;
  qualityScore: number;
  attemptNumber: number;
}

export const BiometricCaptureFlow: React.FC<BiometricCaptureFlowProps> = ({
  modalityType,
  onSuccess,
  onCancel,
}) => {
  const [currentStep, setCurrentStep] = useState<BiometricStep>('instructions');
  const [capturedBlob, setCapturedBlob] = useState<Blob | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string>('');
  const [attemptCount, setAttemptCount] = useState(1);

  const getModalityLabel = () => {
    switch (modalityType) {
      case 'facial':
        return 'Reconhecimento Facial';
      case 'fingerprint':
        return 'Impressões Digitais';
      case 'iris':
        return 'Íris';
    }
  };

  const getModalityEmoji = () => {
    switch (modalityType) {
      case 'facial':
        return '👤';
      case 'fingerprint':
        return '👆';
      case 'iris':
        return '👁️';
    }
  };

  const handleCapture = (blob: Blob) => {
    setCapturedBlob(blob);
    setCurrentStep('quality-check');
  };

  const handleQualityApprove = async () => {
    if (!capturedBlob) return;

    setCurrentStep('processing');
    setIsProcessing(true);

    try {
      // Simular processamento biométrico
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const metadata: BiometricMetadata = {
        modalityType,
        captureTimestamp: new Date().toISOString(),
        qualityScore: 85,
        attemptNumber: attemptCount,
      };

      setCurrentStep('success');
      setTimeout(() => {
        onSuccess(capturedBlob, metadata);
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao processar biometria');
      setCurrentStep('error');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQualityReject = () => {
    setCapturedBlob(null);
    setAttemptCount((prev) => prev + 1);
    setCurrentStep('capture');
  };

  const handleRetryAfterError = () => {
    setError('');
    setCurrentStep('instructions');
    setAttemptCount((prev) => prev + 1);
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header com progresso */}
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-6">
          <div className="text-4xl">{getModalityEmoji()}</div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{getModalityLabel()}</h2>
            <p className="text-gray-600 text-sm">Tentativa #{attemptCount}</p>
          </div>
        </div>

        {/* Indicador de progresso */}
        <div className="flex items-center gap-2">
          {['instructions', 'capture', 'quality-check', 'processing', 'success'].map((step, idx) => (
            <React.Fragment key={step}>
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition ${
                  ['instructions', 'capture', 'quality-check', 'processing', 'success'].indexOf(
                    currentStep
                  ) >= idx
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {idx + 1}
              </div>
              {idx < 4 && (
                <div
                  className={`flex-1 h-1 transition ${
                    ['instructions', 'capture', 'quality-check', 'processing', 'success'].indexOf(
                      currentStep
                    ) > idx
                      ? 'bg-blue-600'
                      : 'bg-gray-200'
                  }`}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Conteúdo por Step */}
      <div className="bg-white rounded-2xl shadow-lg p-8">
        {currentStep === 'instructions' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">Instruções de Captura</h3>
              <div className="space-y-3">
                {modalityType === 'facial' && (
                  <>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        1
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Iluminação adequada</p>
                        <p className="text-sm text-gray-600">
                          Posicione-se num local com luz frontal, sem sombras no rosto
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        2
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Olhe para a câmera</p>
                        <p className="text-sm text-gray-600">Mantenha o rosto frontal, olhos abertos e naturais</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        3
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Sem obstruções</p>
                        <p className="text-sm text-gray-600">Remova óculos ou qualquer objeto que cubra o rosto</p>
                      </div>
                    </div>
                  </>
                )}

                {modalityType === 'fingerprint' && (
                  <>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        1
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Dedo limpo</p>
                        <p className="text-sm text-gray-600">Certifique-se que o dedo está limpo e seco</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        2
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Posição correta</p>
                        <p className="text-sm text-gray-600">Coloque o dedo no centro da área designada</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                        3
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Pressão firme</p>
                        <p className="text-sm text-gray-600">Mantenha pressão constante sem mover o dedo</p>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex gap-3">
              <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-blue-900">
                Todo o processamento é local na sua máquina. Nenhum dado biométrico é enviado para servidores externos.
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={onCancel}
                className="flex-1 px-4 py-3 rounded-xl border-2 border-gray-300 text-gray-900 font-bold hover:bg-gray-50 transition"
              >
                Cancelar
              </button>
              <button
                onClick={() => setCurrentStep('capture')}
                className="flex-1 px-4 py-3 rounded-xl bg-blue-600 text-white font-bold hover:bg-blue-700 transition"
              >
                Iniciar Captura
              </button>
            </div>
          </div>
        )}

        {currentStep === 'capture' && (
          <BiometricCapture
            modalityType={modalityType}
            onCapture={handleCapture}
            onError={(err) => {
              setError(err);
              setCurrentStep('error');
            }}
            isProcessing={isProcessing}
          />
        )}

        {currentStep === 'quality-check' && capturedBlob && (
          <BiometricQualityCheck
            biometricBlob={capturedBlob}
            modalityType={modalityType}
            onApprove={handleQualityApprove}
            onReject={handleQualityReject}
            isValidating={isProcessing}
          />
        )}

        {currentStep === 'processing' && (
          <div className="text-center space-y-6 py-12">
            <Loader className="w-16 h-16 text-blue-600 animate-spin mx-auto" />
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Processando Biometria...</h3>
              <p className="text-gray-600">Por favor, aguarde enquanto sua biometria é processada e validada</p>
            </div>

            {/* Progresso simulado */}
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-sm text-gray-700">Captura completada</span>
              </div>
              <div className="flex items-center gap-3">
                <Loader className="w-5 h-5 text-blue-600 animate-spin" />
                <span className="text-sm text-gray-700">Validando qualidade...</span>
              </div>
              <div className="flex items-center gap-3 opacity-50">
                <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
                <span className="text-sm text-gray-700">Finalizando inscrição</span>
              </div>
            </div>
          </div>
        )}

        {currentStep === 'success' && (
          <div className="text-center space-y-6 py-12">
            <div className="flex justify-center">
              <div className="p-6 bg-green-100 rounded-full">
                <CheckCircle className="w-16 h-16 text-green-600" />
              </div>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Biometria Registrada!</h3>
              <p className="text-gray-600">
                Sua {getModalityLabel().toLowerCase()} foi registrada com sucesso e pode ser utilizada para autenticação.
              </p>
            </div>
          </div>
        )}

        {currentStep === 'error' && (
          <div className="space-y-6 py-12">
            <div className="p-4 rounded-xl bg-red-50 border border-red-200">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-red-900">Erro ao Processar Biometria</h4>
                  <p className="text-sm text-red-700 mt-2">{error}</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <button
                onClick={handleRetryAfterError}
                className="w-full px-4 py-3 rounded-xl bg-blue-600 text-white font-bold hover:bg-blue-700 transition"
              >
                Tentar Novamente
              </button>
              <button
                onClick={onCancel}
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-300 text-gray-900 font-bold hover:bg-gray-50 transition"
              >
                Cancelar
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer nota de privacidade */}
      <div className="mt-6 text-center text-xs text-gray-600">
        <p>
          🔒 Seus dados biométricos são processados localmente e não são armazenados permanentemente nesta sessão
        </p>
      </div>
    </div>
  );
};

export default BiometricCaptureFlow;
