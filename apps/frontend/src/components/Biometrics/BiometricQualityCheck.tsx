import React, { useState } from 'react';
import { AlertCircle, CheckCircle, XCircle, RefreshCw } from 'lucide-react';

interface BiometricQualityCheckProps {
  biometricBlob: Blob;
  modalityType: 'facial' | 'fingerprint' | 'iris';
  onApprove: () => void;
  onReject: () => void;
  isValidating?: boolean;
}

interface QualityMetrics {
  sharpness: number;
  contrast: number;
  brightness: number;
  liveness?: number;
  overallScore: number;
}

export const BiometricQualityCheck: React.FC<BiometricQualityCheckProps> = ({
  biometricBlob,
  modalityType,
  onApprove,
  onReject,
  isValidating = false,
}) => {
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  // Carregar e analisar imagem
  React.useEffect(() => {
    const analyzeImage = async () => {
      try {
        // Criar preview URL
        const url = URL.createObjectURL(biometricBlob);
        setPreviewUrl(url);

        // Criar image para análise
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          canvas.width = img.width;
          canvas.height = img.height;
          const ctx = canvas.getContext('2d');

          if (!ctx) return;

          ctx.drawImage(img, 0, 0);
          const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const data = imageData.data;

          // Calcular métricas
          let brightness = 0;
          let variance = 0;
          let minVal = 255;
          let maxVal = 0;

          for (let i = 0; i < data.length; i += 4) {
            const val = (data[i] + data[i + 1] + data[i + 2]) / 3;
            brightness += val;
            minVal = Math.min(minVal, val);
            maxVal = Math.max(maxVal, val);
          }

          const pixelCount = data.length / 4;
          brightness = brightness / pixelCount;

          for (let i = 0; i < data.length; i += 4) {
            const val = (data[i] + data[i + 1] + data[i + 2]) / 3;
            variance += Math.pow(val - brightness, 2);
          }
          variance = variance / pixelCount;

          const sharpness = Math.sqrt(variance); // Proxy para nitidez
          const contrast = maxVal - minVal;

          // Calcular score
          let sharpnessScore = Math.min(100, (sharpness / 50) * 100); // Normalizar
          let contrastScore = Math.min(100, (contrast / 128) * 100);
          let brightnessScore = 100 - Math.abs(brightness - 128) / 1.28; // 0-100

          const overallScore = (sharpnessScore + contrastScore + brightnessScore) / 3;

          setMetrics({
            sharpness: Math.round(sharpnessScore),
            contrast: Math.round(contrastScore),
            brightness: Math.round(brightnessScore),
            overallScore: Math.round(overallScore),
          });

          // Validações
          const validationErrors: string[] = [];

          if (brightness < 40) validationErrors.push('Imagem muito escura');
          if (brightness > 220) validationErrors.push('Imagem muito clara');
          if (sharpness < 15) validationErrors.push('Imagem muito desfocada');
          if (contrast < 30) validationErrors.push('Contraste insuficiente');

          setErrors(validationErrors);
        };

        img.src = url;
      } catch (err) {
        console.error('Erro ao analisar imagem:', err);
      }
    };

    analyzeImage();
  }, [biometricBlob]);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBarColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const isApprovalRecommended = !metrics || (metrics.overallScore >= 70 && errors.length === 0);

  return (
    <div className="space-y-6">
      {/* Preview */}
      {previewUrl && (
        <div className="rounded-xl overflow-hidden bg-gray-100">
          <img src={previewUrl} alt="Biometric preview" className="w-full h-auto max-h-96 object-cover" />
        </div>
      )}

      {/* Métricas de Qualidade */}
      {metrics && (
        <div className="space-y-4">
          <h3 className="font-bold text-gray-900">Métricas de Qualidade</h3>

          {/* Overall Score - Grande */}
          <div className="p-6 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200">
            <div className="flex items-center justify-between mb-3">
              <span className="font-semibold text-gray-700">Score Geral</span>
              <span className={`text-3xl font-bold ${getScoreColor(metrics.overallScore)}`}>
                {metrics.overallScore}%
              </span>
            </div>
            <div className="w-full h-3 bg-gray-300 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${getScoreBarColor(metrics.overallScore)}`}
                style={{ width: `${metrics.overallScore}%` }}
              />
            </div>
          </div>

          {/* Métricas individuais */}
          <div className="grid grid-cols-3 gap-3">
            {/* Sharpness */}
            <div className="p-3 rounded-lg bg-gray-50 border border-gray-200">
              <p className="text-xs text-gray-600 mb-2">Nitidez</p>
              <p className={`text-lg font-bold ${getScoreColor(metrics.sharpness)}`}>
                {metrics.sharpness}%
              </p>
              <div className="w-full h-1 bg-gray-300 rounded mt-2">
                <div
                  className={`h-full ${getScoreBarColor(metrics.sharpness)}`}
                  style={{ width: `${metrics.sharpness}%` }}
                />
              </div>
            </div>

            {/* Contrast */}
            <div className="p-3 rounded-lg bg-gray-50 border border-gray-200">
              <p className="text-xs text-gray-600 mb-2">Contraste</p>
              <p className={`text-lg font-bold ${getScoreColor(metrics.contrast)}`}>
                {metrics.contrast}%
              </p>
              <div className="w-full h-1 bg-gray-300 rounded mt-2">
                <div
                  className={`h-full ${getScoreBarColor(metrics.contrast)}`}
                  style={{ width: `${metrics.contrast}%` }}
                />
              </div>
            </div>

            {/* Brightness */}
            <div className="p-3 rounded-lg bg-gray-50 border border-gray-200">
              <p className="text-xs text-gray-600 mb-2">Luminosidade</p>
              <p className={`text-lg font-bold ${getScoreColor(metrics.brightness)}`}>
                {metrics.brightness}%
              </p>
              <div className="w-full h-1 bg-gray-300 rounded mt-2">
                <div
                  className={`h-full ${getScoreBarColor(metrics.brightness)}`}
                  style={{ width: `${metrics.brightness}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Validações */}
      {errors.length > 0 && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200">
          <div className="flex gap-3">
            <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-red-900 mb-2">Problemas Detectados</h4>
              <ul className="space-y-1">
                {errors.map((error, idx) => (
                  <li key={idx} className="text-sm text-red-700 flex items-center gap-2">
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-red-600" />
                    {error}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Recomendação */}
      {isApprovalRecommended ? (
        <div className="p-4 rounded-xl bg-green-50 border border-green-200">
          <div className="flex gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-green-900">Qualidade Aprovada!</h4>
              <p className="text-sm text-green-700 mt-1">Esta imagem atende aos critérios de qualidade.</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-yellow-50 border border-yellow-200">
          <div className="flex gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-yellow-900">Qualidade Marginal</h4>
              <p className="text-sm text-yellow-700 mt-1">Recomenda-se capturar novamente para melhor qualidade.</p>
            </div>
          </div>
        </div>
      )}

      {/* Botões */}
      <div className="grid grid-cols-2 gap-3">
        <button
          onClick={onReject}
          disabled={isValidating}
          className="px-4 py-3 rounded-xl border-2 border-gray-300 text-gray-900 font-bold hover:bg-gray-50 transition flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <RefreshCw className="w-5 h-5" />
          Recapturar
        </button>
        <button
          onClick={onApprove}
          disabled={isValidating || !isApprovalRecommended}
          className="px-4 py-3 rounded-xl bg-green-600 text-white font-bold hover:bg-green-700 transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <CheckCircle className="w-5 h-5" />
          {isValidating ? 'Validando...' : 'Aprovar'}
        </button>
      </div>

      {/* Dica */}
      <div className="text-xs text-gray-600 text-center p-3 rounded-lg bg-gray-50">
        <p>
          {modalityType === 'facial' && '💡 Para melhor qualidade: iluminação frontal, olhos descansados, sem óculos'}
          {modalityType === 'fingerprint' &&
            '💡 Para melhor qualidade: dedo limpo e seco, pele natural, mantém pressão constante'}
          {modalityType === 'iris' && '💡 Para melhor qualidade: olhos abertos naturalmente, sem maquilhagem excessiva'}
        </p>
      </div>
    </div>
  );
};

export default BiometricQualityCheck;
