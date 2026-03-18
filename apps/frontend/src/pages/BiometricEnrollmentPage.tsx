import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Fingerprint } from 'lucide-react';
import { BiometricCaptureFlow, BiometricMetadata } from '@/components/Biometrics';

type EnrollmentStep = 'welcome' | 'modality-selection' | 'biometric-capture' | 'verification' | 'complete';

export const BiometricEnrollmentPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<EnrollmentStep>('welcome');
  const [selectedModality, setSelectedModality] = useState<'facial' | 'fingerprint' | 'iris' | null>(null);
  const [enrollmentProgress, setEnrollmentProgress] = useState(0);
  const [biometricData, setBiometricData] = useState<{
    fingerprints: boolean;
    face: boolean;
    iris: boolean;
  }>({
    fingerprints: false,
    face: false,
    iris: false,
  });
  const [completedModalities, setCompletedModalities] = useState<string[]>([]);

  const handleStartEnrollment = () => {
    setCurrentStep('modality-selection');
    setEnrollmentProgress(20);
  };

  const handleSelectModality = (modality: 'facial' | 'fingerprint' | 'iris') => {
    setSelectedModality(modality);
    setCurrentStep('biometric-capture');
  };

  const handleBiometricSuccess = (blob: Blob, metadata: BiometricMetadata) => {
    // Atualizar estado de dados biométricos
    if (metadata.modalityType === 'facial') {
      setBiometricData((prev) => ({ ...prev, face: true }));
    } else if (metadata.modalityType === 'fingerprint') {
      setBiometricData((prev) => ({ ...prev, fingerprints: true }));
    } else if (metadata.modalityType === 'iris') {
      setBiometricData((prev) => ({ ...prev, iris: true }));
    }

    setCompletedModalities((prev) => [...prev, metadata.modalityType]);

    // Atualizar progresso
    const newProgress = Math.min(100, 20 + completedModalities.length * 30);
    setEnrollmentProgress(newProgress);

    // Se uma biometria foi completada, mostrar opções
    if (completedModalities.length >= 1) {
      setTimeout(() => {
        setCurrentStep('verification');
      }, 1000);
    } else {
      setCurrentStep('modality-selection');
    }
  };

  const handleBiometricCancel = () => {
    setCurrentStep('modality-selection');
    setSelectedModality(null);
  };

  const handleVerificationComplete = () => {
    setEnrollmentProgress(100);
    setCurrentStep('complete');
  };

  const handleReset = () => {
    setCurrentStep('welcome');
    setEnrollmentProgress(0);
    setBiometricData({ fingerprints: false, face: false, iris: false });
    setCompletedModalities([]);
    setSelectedModality(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-8 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Fingerprint className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Inscrição Biométrica</h1>
              <p className="text-gray-600 mt-1">Registre seus dados biométricos de forma segura</p>
            </div>
          </div>
        </div>

        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-semibold text-gray-700">Progresso</span>
            <span className="text-sm font-semibold text-gray-700">{enrollmentProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${enrollmentProgress}%` }}
            ></div>
          </div>
        </div>

        {/* Content */}
        {currentStep === 'welcome' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <div className="text-center mb-8">
              <div className="flex justify-center mb-6">
                <div className="p-6 bg-purple-100 rounded-full">
                  <Fingerprint className="h-12 w-12 text-purple-600" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Bem-vindo à Inscrição Biométrica</h2>
              <p className="text-gray-600 leading-relaxed mb-4">
                Este processo irá registar seus dados biométricos de forma segura para autenticação futura.
              </p>
              <p className="text-sm text-gray-500">
                O processo leva aproximadamente 5-10 minutos e requer câmera e iluminação adequada.
              </p>
            </div>

            <div className="space-y-4 mb-8">
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl flex gap-3">
                <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-blue-900">Segurança Garantida</p>
                  <p className="text-xs text-blue-800">Seus dados são criptografados e processados localmente</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <button
                onClick={handleStartEnrollment}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition"
              >
                <Fingerprint className="h-5 w-5" />
                Iniciar Inscrição
              </button>
            </div>
          </div>
        )}

        {currentStep === 'modality-selection' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {completedModalities.length === 0
                ? 'Selecione o Tipo de Biometria'
                : 'Registar Próxima Biometria (Opcional)'}
            </h2>

            <div className="space-y-4 mb-8">
              {/* Facial Recognition */}
              <button
                onClick={() => handleSelectModality('facial')}
                disabled={biometricData.face}
                className={`w-full p-6 rounded-xl border-2 transition text-left ${
                  biometricData.face
                    ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                    : 'border-gray-300 hover:border-purple-400 hover:bg-purple-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">👤 Reconhecimento Facial</h3>
                    <p className="text-gray-600 text-sm mt-1">Capturar rosto para identificação</p>
                  </div>
                  {biometricData.face && <CheckCircle className="h-6 w-6 text-green-600" />}
                </div>
              </button>

              {/* Fingerprint */}
              <button
                onClick={() => handleSelectModality('fingerprint')}
                disabled={biometricData.fingerprints}
                className={`w-full p-6 rounded-xl border-2 transition text-left ${
                  biometricData.fingerprints
                    ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                    : 'border-gray-300 hover:border-purple-400 hover:bg-purple-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">👆 Impressões Digitais</h3>
                    <p className="text-gray-600 text-sm mt-1">Registar impressões dos dedos</p>
                  </div>
                  {biometricData.fingerprints && <CheckCircle className="h-6 w-6 text-green-600" />}
                </div>
              </button>

              {/* Iris */}
              <button
                onClick={() => handleSelectModality('iris')}
                disabled={biometricData.iris}
                className={`w-full p-6 rounded-xl border-2 transition text-left ${
                  biometricData.iris
                    ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                    : 'border-gray-300 hover:border-purple-400 hover:bg-purple-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">👁️ Íris</h3>
                    <p className="text-gray-600 text-sm mt-1">Scan da íris para autenticação avançada</p>
                  </div>
                  {biometricData.iris && <CheckCircle className="h-6 w-6 text-green-600" />}
                </div>
              </button>
            </div>

            {completedModalities.length > 0 && (
              <div className="space-y-3">
                <button
                  onClick={handleVerificationComplete}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold transition"
                >
                  ✓ Completar Inscrição
                </button>
                <button
                  onClick={() => setEnrollmentProgress(Math.min(100, enrollmentProgress + 10))}
                  className="w-full bg-gray-200 hover:bg-gray-300 text-gray-900 px-6 py-3 rounded-xl font-bold transition"
                >
                  + Adicionar Mais Biometria
                </button>
              </div>
            )}
          </div>
        )}

        {currentStep === 'biometric-capture' && selectedModality && (
          <BiometricCaptureFlow
            modalityType={selectedModality}
            onSuccess={handleBiometricSuccess}
            onCancel={handleBiometricCancel}
          />
        )}

        {currentStep === 'verification' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Resumo de Biometrias Registadas</h2>

            <div className="space-y-4 mb-8">
              {biometricData.face && (
                <div className="p-4 border border-gray-200 rounded-xl">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">👤</span>
                      <span className="font-semibold text-gray-900">Reconhecimento Facial</span>
                    </div>
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  </div>
                </div>
              )}

              {biometricData.fingerprints && (
                <div className="p-4 border border-gray-200 rounded-xl">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">👆</span>
                      <span className="font-semibold text-gray-900">Impressões Digitais</span>
                    </div>
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  </div>
                </div>
              )}

              {biometricData.iris && (
                <div className="p-4 border border-gray-200 rounded-xl">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">👁️</span>
                      <span className="font-semibold text-gray-900">Íris</span>
                    </div>
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-3">
              <button
                onClick={handleVerificationComplete}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold transition"
              >
                Finalizar Inscrição
              </button>
              <button
                onClick={() => {
                  setCurrentStep('modality-selection');
                  setSelectedModality(null);
                }}
                className="w-full bg-gray-200 hover:bg-gray-300 text-gray-900 px-6 py-3 rounded-xl font-bold transition"
              >
                Adicionar Mais Biometrias
              </button>
            </div>
          </div>
        )}

        {currentStep === 'complete' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <div className="text-center">
              <div className="flex justify-center mb-6">
                <div className="p-6 bg-green-100 rounded-full">
                  <CheckCircle className="h-12 w-12 text-green-600" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Inscrição Concluída!</h2>
              <p className="text-gray-600 mb-8">
                Suas biometrias foram registadas com sucesso. Você pode agora usar autenticação biométrica.
              </p>

              <div className="space-y-3 mb-8 bg-green-50 border border-green-200 rounded-xl p-6">
                {biometricData.face && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold">Reconhecimento Facial Registado</span>
                  </div>
                )}
                {biometricData.fingerprints && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold">Impressões Digitais Registadas</span>
                  </div>
                )}
                {biometricData.iris && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold">Íris Registada</span>
                  </div>
                )}
              </div>

              <button
                onClick={handleReset}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold transition"
              >
                Voltar ao Portal
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BiometricEnrollmentPage;
