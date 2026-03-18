import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, CheckCircle, Fingerprint, Loader } from 'lucide-react';

type EnrollmentStep = 'welcome' | 'instructions' | 'capture' | 'verification' | 'complete';

export const BiometricEnrollmentPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<EnrollmentStep>('welcome');
  const [isProcessing, setIsProcessing] = useState(false);
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

  const handleStartEnrollment = () => {
    setCurrentStep('instructions');
  };

  const handleCaptureStart = () => {
    setCurrentStep('capture');
    setIsProcessing(true);
    // Simulate capture process
    const progressInterval = setInterval(() => {
      setEnrollmentProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsProcessing(false);
          setCurrentStep('verification');
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  const handleVerificationComplete = () => {
    setBiometricData({
      fingerprints: true,
      face: true,
      iris: false,
    });
    setCurrentStep('complete');
  };

  const handleRetry = () => {
    setEnrollmentProgress(0);
    setCurrentStep('instructions');
  };

  const handleReset = () => {
    setCurrentStep('welcome');
    setEnrollmentProgress(0);
    setBiometricData({ fingerprints: false, face: false, iris: false });
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-8 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
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

        {/* Welcome Step */}
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
                Este processo irá registrar seus dados biométricos de forma segura para autenticação futura.
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
              <Button
                onClick={handleStartEnrollment}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2"
              >
                <Fingerprint className="h-5 w-5" />
                Iniciar Inscrição
              </Button>
            </div>
          </div>
        )}

        {/* Instructions Step */}
        {currentStep === 'instructions' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Instruções</h2>

            <div className="space-y-6 mb-8">
              <div className="flex gap-4">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-100 flex-shrink-0">
                  <span className="text-purple-600 font-bold">1</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">Ambiente Adequado</h3>
                  <p className="text-gray-600 text-sm">Escolha um local com boa iluminação frontal</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-100 flex-shrink-0">
                  <span className="text-purple-600 font-bold">2</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">Permissões de Câmera</h3>
                  <p className="text-gray-600 text-sm">Você será solicitado a permitir acesso à câmera</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-100 flex-shrink-0">
                  <span className="text-purple-600 font-bold">3</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">Captura de Dados</h3>
                  <p className="text-gray-600 text-sm">Siga as instruções na tela para capturar seus dados</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-100 flex-shrink-0">
                  <span className="text-purple-600 font-bold">4</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">Confirmação</h3>
                  <p className="text-gray-600 text-sm">Revise e confirme seus dados biométricos</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <Button
                onClick={handleCaptureStart}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold"
              >
                Continuar
              </Button>
              <Button
                onClick={handleReset}
                className="w-full bg-gray-200 hover:bg-gray-300 text-gray-900 px-6 py-3 rounded-xl font-bold"
              >
                Cancelar
              </Button>
            </div>
          </div>
        )}

        {/* Capture Step */}
        {currentStep === 'capture' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Captura de Dados Biométricos</h2>

            {isProcessing ? (
              <div className="text-center space-y-6 py-12">
                <div className="flex justify-center">
                  <Loader className="h-12 w-12 text-purple-600 animate-spin" />
                </div>
                <div>
                  <p className="text-gray-909 font-semibold mb-2">Processando dados biométricos...</p>
                  <p className="text-sm text-gray-600">Por favor, mantenha-se imóvel</p>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full">
                      <div className="h-full bg-purple-600 rounded-full" style={{ width: '33%' }}></div>
                    </div>
                    <span className="text-sm text-gray-600">Impressões digitais</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-gray-200 rounded-full">
                      <div className="h-full bg-purple-600 rounded-full" style={{ width: `${enrollmentProgress > 50 ? '100' : '0'}%` }}></div>
                    </div>
                    <span className="text-sm text-gray-600">Reconhecimento facial</span>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        )}

        {/* Verification Step */}
        {currentStep === 'verification' && (
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Verificação de Dados</h2>

            <div className="space-y-4 mb-8">
              <div className="p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Fingerprint className="h-5 w-5 text-purple-600" />
                    <span className="font-semibold text-gray-900">Impressões Digitais</span>
                  </div>
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
              </div>

              <div className="p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Fingerprint className="h-5 w-5 text-purple-600" />
                    <span className="font-semibold text-gray-900">Reconhecimento Facial</span>
                  </div>
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <Button
                onClick={handleVerificationComplete}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold"
              >
                Confirmar e Completar
              </Button>
              <Button
                onClick={handleRetry}
                className="w-full bg-gray-200 hover:bg-gray-300 text-gray-900 px-6 py-3 rounded-xl font-bold"
              >
                Repetir Captura
              </Button>
            </div>
          </div>
        )}

        {/* Complete Step */}
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
                Seus dados biométricos foram registrados com sucesso. Você pode agora usar autenticação biométrica.
              </p>

              <div className="space-y-3 mb-8 bg-green-50 border border-green-200 rounded-xl p-6">
                <div className="flex items-center gap-3 justify-center">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-green-900 font-semibold">Impressões Digitais Registradas</span>
                </div>
                <div className="flex items-center gap-3 justify-center">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="text-green-900 font-semibold">Reconhecimento Facial Registrado</span>
                </div>
              </div>

              <Button
                onClick={handleReset}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold"
              >
                Voltar ao Portal
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BiometricEnrollmentPage;
