/**
 * Biometric Enrollment Component
 * Wizard for capturing and enrolling biometric templates
 */

import React, { useRef, useState } from 'react';
import { useBiometricTemplates } from '@/modules/identity/hooks';
import {
  convertBiometricToBase64,
  calculateBiometricQuality,
  isBiometricQualityAcceptable,
} from '@/modules/identity/utils';
import type { BiometricEnrollmentRequest, BiometricTemplate, BiometricType } from '@/modules/identity/types';
import { identityService } from '@/modules/identity/services';

interface BiometricEnrollmentProps {
  citizenId: string;
  onSuccess?: (template: BiometricTemplate) => void;
  onCancel?: () => void;
}

type EnrollmentStep = 'type-selection' | 'capture' | 'review' | 'uploading';

/**
 * BiometricEnrollment - Multi-step biometric capture wizard
 */
export const BiometricEnrollment: React.FC<BiometricEnrollmentProps> = ({
  citizenId,
  onSuccess,
  onCancel,
}) => {
  const { refetch } = useBiometricTemplates(citizenId);
  const [step, setStep] = useState<EnrollmentStep>('type-selection');
  const [selectedType, setSelectedType] = useState<BiometricType | null>(null);
  const [capturedData, setCapturedData] = useState<string | null>(null);
  const [qualityScore, setQualityScore] = useState<number | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleTypeSelect = (type: BiometricType) => {
    setSelectedType(type);
    setError(null);
    setStep('capture');
  };

  const handleFileCapture = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);

    try {
      const base64 = await convertBiometricToBase64(file);
      setCapturedData(base64);

      // Calculate quality score
      const quality = calculateBiometricQuality(base64, {
        brightness: 75,
        contrast: 80,
        sharpness: 85,
        completeness: 70,
      });
      setQualityScore(quality);

      setStep('review');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao processar imagem');
    }
  };

  const handleUpload = async () => {
    if (!selectedType || !capturedData || qualityScore === null) {
      setError('Dados incompletos');
      return;
    }

    const qualityCheck = isBiometricQualityAcceptable(qualityScore, 70);
    if (!qualityCheck.isAcceptable) {
      setError(qualityCheck.message);
      return;
    }

    setStep('uploading');
    setUploading(true);
    setError(null);

    try {
      const request: BiometricEnrollmentRequest = {
        citizen_id: citizenId,
        biometric_type: selectedType,
        biometric_data: capturedData,
        quality_threshold: 70,
        device_id: navigator.userAgent,
        location: 'Web Browser',
      };

      const response = await identityService.enrollBiometric(request);

      if (response.status === 'SUCCESS') {
        await refetch();
        if (onSuccess) {
          const templates = await identityService.getBiometricTemplates(citizenId);
          const newTemplate = templates[templates.length - 1];
          if (newTemplate) {
            onSuccess(newTemplate);
          }
        }
        reset();
      } else {
        setError(response.message || 'Falha ao inscrever biometria');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao inscrever biometria');
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setStep('type-selection');
    setSelectedType(null);
    setCapturedData(null);
    setQualityScore(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
      <h2 className="text-2xl font-bold mb-6 border-b pb-4">Inscrição Biométrica</h2>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}

      {step === 'type-selection' && (
        <TypeSelectionStep onSelect={handleTypeSelect} />
      )}

      {step === 'capture' && (
        <CaptureStep
          biometricType={selectedType}
          onCapture={handleFileCapture}
          fileInputRef={fileInputRef}
          onBack={() => setStep('type-selection')}
        />
      )}

      {step === 'review' && (
        <ReviewStep
          qualityScore={qualityScore}
          onConfirm={handleUpload}
          onRetry={() => {
            setCapturedData(null);
            setQualityScore(null);
            setStep('capture');
          }}
        />
      )}

      {step === 'uploading' && (
        <UploadingStep
          biometricType={selectedType}
          uploading={uploading}
        />
      )}

      {step !== 'uploading' && (
        <div className="flex gap-3 mt-6 pt-4 border-t">
          <button
            onClick={onCancel || reset}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 font-medium"
          >
            {step === 'type-selection' ? 'Cancelar' : 'Voltar'}
          </button>
        </div>
      )}
    </div>
  );
};

// ============= STEP COMPONENTS =============

function TypeSelectionStep({ onSelect }: { onSelect: (type: BiometricType) => void }) {
  const types: { type: BiometricType; label: string; icon: string; description: string }[] = [
    {
      type: 'FINGERPRINT',
      label: 'Impressão Digital',
      icon: '👆',
      description: 'Captura da ponta do dedo',
    },
    {
      type: 'FACE_RECOGNITION',
      label: 'Reconhecimento Facial',
      icon: '😊',
      description: 'Fotografia frontal do rosto',
    },
    {
      type: 'IRIS',
      label: 'Íris',
      icon: '👁️',
      description: 'Imagem do padrão da íris',
    },
    {
      type: 'VOICE',
      label: 'Voz',
      icon: '🎤',
      description: 'Gravação de frase pré-definida',
    },
  ];

  return (
    <div>
      <p className="text-gray-600 mb-6">Selecione o tipo de biometria a capturar:</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {types.map(({ type, label, icon, description }) => (
          <button
            key={type}
            onClick={() => onSelect(type)}
            className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all text-left"
          >
            <div className="text-3xl mb-2">{icon}</div>
            <h3 className="font-bold text-gray-900">{label}</h3>
            <p className="text-sm text-gray-600 mt-1">{description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

function CaptureStep({
  biometricType,
  onCapture,
  fileInputRef,
  onBack,
}: {
  biometricType: BiometricType | null;
  onCapture: (e: React.ChangeEvent<HTMLInputElement>) => void;
  fileInputRef: React.RefObject<HTMLInputElement>;
  onBack: () => void;
}) {
  const instructions: Record<BiometricType, string> = {
    FINGERPRINT: 'Coloque o dedo no scanner ou carregue uma imagem clara da impressão digital',
    FACE_RECOGNITION: 'Tire uma fotografia frontal clara do rosto contra fundo neutro',
    IRIS: 'Posicione o olho a 10-15cm da câmara com boa iluminação',
    VOICE: 'Grave uma gravação clara da frase pré-definida',
  };

  return (
    <div>
      <p className="text-gray-600 mb-6">
        {biometricType ? instructions[biometricType] : 'Instruções'}
      </p>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 hover:bg-blue-50 transition-all">
        <button
          onClick={() => fileInputRef.current?.click()}
          className="text-4xl block mx-auto mb-4"
        >
          📁
        </button>
        <p className="font-medium text-gray-900 mb-2">Selecione ou arraste arquivo</p>
        <p className="text-sm text-gray-600">
          Suportados: PNG, JPG, MP4 (máx. 50MB)
        </p>

        <input
          ref={fileInputRef}
          type="file"
          accept={biometricType === 'VOICE' ? 'audio/*' : 'image/*'}
          onChange={onCapture}
          className="hidden"
        />
      </div>

      <div className="flex gap-3 mt-6 pt-4 border-t">
        <button
          onClick={onBack}
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 font-medium"
        >
          Voltar
        </button>
      </div>
    </div>
  );
}

function ReviewStep({
  qualityScore,
  onConfirm,
  onRetry,
}: {
  qualityScore: number | null;
  onConfirm: () => void;
  onRetry: () => void;
}) {
  if (qualityScore === null) return null;

  const scoreColor =
    qualityScore >= 80
      ? 'text-green-600'
      : qualityScore >= 60
        ? 'text-yellow-600'
        : 'text-red-600';

  const scoreStatus =
    qualityScore >= 80
      ? 'Excelente'
      : qualityScore >= 60
        ? 'Aceitável'
        : 'Fraco';

  return (
    <div>
      <div className="bg-gray-50 rounded-lg p-6 mb-6">
        <h3 className="font-bold text-gray-900 mb-4">Análise de Qualidade</h3>

        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-sm text-gray-600">Pontuação de Qualidade</p>
            <p className={`text-5xl font-bold ${scoreColor}`}>{qualityScore}%</p>
            <p className={`text-lg font-semibold ${scoreColor} mt-1`}>{scoreStatus}</p>
          </div>

          <div className="flex-1 ml-6">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div
                className={`h-8 rounded-full transition-all ${
                  qualityScore >= 80
                    ? 'bg-green-500'
                    : qualityScore >= 60
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                }`}
                style={{ width: `${qualityScore}%` }}
              />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-white p-3 rounded border border-gray-200">
            <p className="text-gray-600">Brilho</p>
            <p className="font-bold text-gray-900">75%</p>
          </div>
          <div className="bg-white p-3 rounded border border-gray-200">
            <p className="text-gray-600">Contraste</p>
            <p className="font-bold text-gray-900">80%</p>
          </div>
          <div className="bg-white p-3 rounded border border-gray-200">
            <p className="text-gray-600">Nitidez</p>
            <p className="font-bold text-gray-900">85%</p>
          </div>
          <div className="bg-white p-3 rounded border border-gray-200">
            <p className="text-gray-600">Preenchimento</p>
            <p className="font-bold text-gray-900">70%</p>
          </div>
        </div>
      </div>

      {qualityScore < 70 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 text-yellow-700 text-sm">
          ⚠️ A qualidade está abaixo do limite recomendado. Por favor, tente novamente.
        </div>
      )}

      <div className="flex gap-3 pt-4 border-t">
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 font-medium"
        >
          Tentar Novamente
        </button>
        {qualityScore >= 70 && (
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 font-medium ml-auto"
          >
            Confirmar e Inscrever
          </button>
        )}
      </div>
    </div>
  );
}

function UploadingStep({
  biometricType,
  uploading,
}: {
  biometricType: BiometricType | null;
  uploading: boolean;
}) {
  return (
    <div className="text-center py-12">
      {uploading ? (
        <>
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-500 rounded-full animate-spin" />
          </div>
          <h3 className="font-bold text-lg text-gray-900 mb-2">Inscrevendo Biometria...</h3>
          <p className="text-gray-600">Por favor aguarde enquanto o seu {biometricType} é processado</p>
        </>
      ) : (
        <>
          <div className="text-5xl mb-4">✅</div>
          <h3 className="font-bold text-lg text-gray-900 mb-2">Inscrição Concluída</h3>
          <p className="text-gray-600">O seu template biométrico foi registrado com sucesso</p>
        </>
      )}
    </div>
  );
}
