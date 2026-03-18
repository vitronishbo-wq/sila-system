import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Fingerprint, ArrowRight, Lock } from 'lucide-react';
import { BiometricCaptureFlow } from '@/components/Biometrics';
import type { BiometricMetadata } from '@/components/Biometrics';

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

  const handleBiometricSuccess = (_blob: Blob, metadata: BiometricMetadata) => {
    if (metadata.modalityType === 'facial') {
      setBiometricData((prev) => ({ ...prev, face: true }));
    } else if (metadata.modalityType === 'fingerprint') {
      setBiometricData((prev) => ({ ...prev, fingerprints: true }));
    } else if (metadata.modalityType === 'iris') {
      setBiometricData((prev) => ({ ...prev, iris: true }));
    }

    setCompletedModalities((prev) => [...prev, metadata.modalityType]);

    const newProgress = Math.min(100, 20 + completedModalities.length * 30);
    setEnrollmentProgress(newProgress);

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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Inscrição Biométrica</h1>
          <p className="text-slate-600">Registre seus dados biométricos de forma segura para autenticação</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-600 uppercase tracking-wide">Progresso</span>
            <span className="text-xs font-bold text-slate-700">{enrollmentProgress}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${enrollmentProgress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">

        {/* Welcome Step */}
        {currentStep === 'welcome' && (
          <div className="space-y-6">
            {/* Main Service Card */}
            <div className="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
              <div className="relative h-48 bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
                <Fingerprint className="h-24 w-24 text-white opacity-80" />
              </div>
              <div className="p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-3">Proteja Sua Identidade</h2>
                <p className="text-slate-600 mb-6">
                  Configure autenticação biométrica para proteger sua conta com dados únicos e invioláveis.
                  O processo leva apenas 5-10 minutos.
                </p>

                {/* Benefits */}
                <div className="space-y-3 mb-8">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                      <span className="text-xs font-bold text-green-700">✓</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 text-sm">Segurança Máxima</p>
                      <p className="text-xs text-slate-500">Dados processados localmente, nenhuma transmissão</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                      <span className="text-xs font-bold text-green-700">✓</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 text-sm">Autenticação Rápida</p>
                      <p className="text-xs text-slate-500">Acesso em segundos sem senhas</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                      <span className="text-xs font-bold text-green-700">✓</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 text-sm">Conformidade Legal</p>
                      <p className="text-xs text-slate-500">Atende normas internacionais de segurança</p>
                    </div>
                  </div>
                </div>

                {/* Security Notice */}
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
                  <div className="flex gap-3">
                    <Lock className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-semibold text-blue-900">Privacidade Garantida</p>
                      <p className="text-xs text-blue-800 mt-1">
                        Seus dados biométricos são encriptados e armazenados apenas localmente. Nunca solicitamos envio de dados sensíveis.
                      </p>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleStartEnrollment}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition shadow-lg"
                >
                  Iniciar Inscrição <ArrowRight className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Modality Selection Step */}
        {currentStep === 'modality-selection' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {completedModalities.length === 0
                  ? 'Escolha Seu Tipo de Biometria'
                  : 'Adicione Mais Biometrias (Opcional)'}
              </h2>
              <p className="text-slate-600 mb-8">
                {completedModalities.length === 0
                  ? 'Selecione pelo menos um tipo de biometria para proteger sua conta'
                  : `Você já registrou ${completedModalities.length} biometria(s). Adicione mais para maior segurança.`}
              </p>

              {/* Modality Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                {/* Facial Recognition */}
                <button
                  onClick={() => handleSelectModality('facial')}
                  disabled={biometricData.face}
                  className={`group rounded-2xl border-2 transition p-6 text-left ${
                    biometricData.face
                      ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                      : 'border-slate-200 hover:border-blue-400 hover:bg-blue-50 hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-4xl">👤</span>
                    {biometricData.face && (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    )}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">Reconhecimento Facial</h3>
                  <p className="text-xs text-slate-600 mb-3">Usar câmera para capturar rosto</p>
                  <div className="text-xs font-semibold text-blue-600 group-hover:text-blue-700">
                    {biometricData.face ? 'Registado ✓' : 'Registar'}
                  </div>
                </button>

                {/* Fingerprint */}
                <button
                  onClick={() => handleSelectModality('fingerprint')}
                  disabled={biometricData.fingerprints}
                  className={`group rounded-2xl border-2 transition p-6 text-left ${
                    biometricData.fingerprints
                      ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                      : 'border-slate-200 hover:border-purple-400 hover:bg-purple-50 hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-4xl">👆</span>
                    {biometricData.fingerprints && (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    )}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">Impressões Digitais</h3>
                  <p className="text-xs text-slate-600 mb-3">Scanner de dedos ou câmera</p>
                  <div className="text-xs font-semibold text-purple-600 group-hover:text-purple-700">
                    {biometricData.fingerprints ? 'Registados ✓' : 'Registar'}
                  </div>
                </button>

                {/* Iris */}
                <button
                  onClick={() => handleSelectModality('iris')}
                  disabled={biometricData.iris}
                  className={`group rounded-2xl border-2 transition p-6 text-left ${
                    biometricData.iris
                      ? 'bg-green-50 border-green-300 opacity-60 cursor-not-allowed'
                      : 'border-slate-200 hover:border-orange-400 hover:bg-orange-50 hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-4xl">👁️</span>
                    {biometricData.iris && (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    )}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">Scan da Íris</h3>
                  <p className="text-xs text-slate-600 mb-3">Captura do padrão da íris</p>
                  <div className="text-xs font-semibold text-orange-600 group-hover:text-orange-700">
                    {biometricData.iris ? 'Registada ✓' : 'Registar'}
                  </div>
                </button>
              </div>

              {/* Action Buttons */}
              {completedModalities.length > 0 && (
                <div className="space-y-3">
                  <button
                    onClick={handleVerificationComplete}
                    className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-6 py-3 rounded-xl font-bold transition shadow-lg"
                  >
                    ✓ Completar Inscrição
                  </button>
                  <button
                    onClick={() => setCurrentStep('verification')}
                    className="w-full bg-slate-200 hover:bg-slate-300 text-slate-900 px-6 py-3 rounded-xl font-bold transition"
                  >
                    + Adicionar Mais Biometrias
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {currentStep === 'biometric-capture' && selectedModality && (
          <BiometricCaptureFlow
            modalityType={selectedModality}
            onSuccess={handleBiometricSuccess}
            onCancel={handleBiometricCancel}
          />
        )}

        {/* Verification Summary */}
        {currentStep === 'verification' && (
          <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Resumo de Biometrias</h2>

            <div className="space-y-3 mb-8">
              {biometricData.face && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 hover:bg-blue-50 hover:border-blue-300 transition flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">👤</span>
                    <span className="font-semibold text-gray-900">Reconhecimento Facial</span>
                  </div>
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
              )}

              {biometricData.fingerprints && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 hover:bg-purple-50 hover:border-purple-300 transition flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">👆</span>
                    <span className="font-semibold text-gray-900">Impressões Digitais</span>
                  </div>
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
              )}

              {biometricData.iris && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 hover:bg-orange-50 hover:border-orange-300 transition flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">👁️</span>
                    <span className="font-semibold text-gray-900">Scan da Íris</span>
                  </div>
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
              )}
            </div>

            <div className="space-y-3">
              <button
                onClick={handleVerificationComplete}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-6 py-3 rounded-xl font-bold transition shadow-lg"
              >
                Finalizar Inscrição
              </button>
              <button
                onClick={() => {
                  setCurrentStep('modality-selection');
                  setSelectedModality(null);
                }}
                className="w-full bg-slate-200 hover:bg-slate-300 text-slate-900 px-6 py-3 rounded-xl font-bold transition"
              >
                Adicionar Mais Biometrias
              </button>
            </div>
          </div>
        )}

        {/* Completion Step */}
        {currentStep === 'complete' && (
          <div className="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
            <div className="relative h-48 bg-gradient-to-r from-green-600 to-emerald-600 flex items-center justify-center">
              <div className="relative w-24 h-24">
                <div className="absolute inset-0 bg-white opacity-20 rounded-full animate-pulse"></div>
                <CheckCircle className="h-24 w-24 text-white" />
              </div>
            </div>
            <div className="p-8 text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-3">Inscrição Concluída!</h2>
              <p className="text-slate-600 mb-6">
                Suas biometrias foram registadas com sucesso. Você pode agora usar autenticação biométrica em sua conta.
              </p>

              {/* Success Summary */}
              <div className="space-y-2 mb-8 bg-green-50 border border-green-200 rounded-xl p-6">
                {biometricData.face && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold text-sm">👤 Reconhecimento Facial Registado</span>
                  </div>
                )}
                {biometricData.fingerprints && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold text-sm">👆 Impressões Digitais Registadas</span>
                  </div>
                )}
                {biometricData.iris && (
                  <div className="flex items-center gap-3 justify-center">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-green-900 font-semibold text-sm">👁️ Scan da Íris Registado</span>
                  </div>
                )}
              </div>

              <button
                onClick={handleReset}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-bold transition shadow-lg"
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
