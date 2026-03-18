import React, { useRef, useEffect, useState } from 'react';
import { Loader, AlertCircle, CheckCircle, Camera } from 'lucide-react';

interface BiometricCaptureProps {
  modalityType: 'facial' | 'fingerprint' | 'iris';
  onCapture: (biometricData: Blob) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
}

export const BiometricCapture: React.FC<BiometricCaptureProps> = ({
  modalityType,
  onCapture,
  onError,
  isProcessing,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [captureReady, setCaptureReady] = useState(false);
  const [quality, setQuality] = useState<'poor' | 'fair' | 'good' | 'excellent'>('poor');
  const [frameCount, setFrameCount] = useState(0);

  // Iniciar câmera
  useEffect(() => {
    const startCamera = async () => {
      try {
        const constraints: MediaStreamConstraints = {
          video: {
            facingMode: 'user',
            width: { ideal: 1280 },
            height: { ideal: 720 },
            ...(modalityType === 'fingerprint' && {
              focusMode: ['continuous', 'auto'],
            }),
          },
          audio: false,
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current?.play();
            setCameraActive(true);
          };
        }
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Erro ao aceder à câmera';
        onError(errorMsg);
      }
    };

    if (!cameraActive) {
      startCamera();
    }

    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [cameraActive, onError]);

  // Monitorar qualidade da imagem
  useEffect(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const analyzeFrame = () => {
      const canvas = canvasRef.current;
      const video = videoRef.current;

      if (!canvas || !video) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);

      // Análise de qualidade (simplicidade - luminosidade)
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      let brightness = 0;
      for (let i = 0; i < data.length; i += 4) {
        brightness += (data[i] + data[i + 1] + data[i + 2]) / 3;
      }
      brightness = brightness / (canvas.width * canvas.height);

      // Score de qualidade (0-100)
      const qualityScore = Math.abs(brightness - 128) * 1.56; // 0-100

      if (qualityScore < 30) {
        setQuality('poor');
        setCaptureReady(false);
      } else if (qualityScore < 50) {
        setQuality('fair');
        setCaptureReady(false);
      } else if (qualityScore < 70) {
        setQuality('good');
        setCaptureReady(true);
      } else {
        setQuality('excellent');
        setCaptureReady(true);
      }

      setFrameCount((prev) => prev + 1);
    };

    const interval = setInterval(analyzeFrame, 100);
    return () => clearInterval(interval);
  }, []);

  // Capturar biometria
  const handleCapture = async () => {
    if (!canvasRef.current || !captureReady) return;

    try {
      canvasRef.current.toBlob((blob) => {
        if (blob) {
          onCapture(blob);
        }
      }, 'image/jpeg', 0.9);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Erro ao capturar dados';
      onError(errorMsg);
    }
  };

  const qualityColors = {
    poor: 'bg-red-100 border-red-300 text-red-700',
    fair: 'bg-yellow-100 border-yellow-300 text-yellow-700',
    good: 'bg-blue-100 border-blue-300 text-blue-700',
    excellent: 'bg-green-100 border-green-300 text-green-700',
  };

  const qualityLabels = {
    poor: 'Fraca',
    fair: 'Aceitável',
    good: 'Boa',
    excellent: 'Excelente',
  };

  return (
    <div className="space-y-6">
      {/* Video preview */}
      <div className="relative rounded-2xl overflow-hidden bg-black aspect-video">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          playsInline
          autoPlay
          muted
        />
        <canvas ref={canvasRef} className="hidden" />

        {/* Overlay guides */}
        {modalityType === 'facial' && (
          <>
            {/* Circular face guide */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="w-64 h-64 border-2 border-green-400 rounded-full opacity-60"></div>
            </div>

            {/* Corner markers */}
            <div className="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-green-400"></div>
            <div className="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-green-400"></div>
            <div className="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-green-400"></div>
            <div className="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-green-400"></div>
          </>
        )}

        {modalityType === 'fingerprint' && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <div className="w-32 h-40 border-2 border-dashed border-green-400 rounded-lg"></div>
              <p className="text-green-400 text-sm mt-4">Coloque o dedo dentro da caixa</p>
            </div>
          </div>
        )}

        {/* Loading indicator */}
        {isProcessing && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <Loader className="w-12 h-12 text-green-400 animate-spin" />
          </div>
        )}
      </div>

      {/* Quality indicator */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm font-semibold text-gray-700">Qualidade da Captura</span>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${qualityColors[quality]}`}>
            {qualityLabels[quality]}
          </span>
        </div>

        {/* Quality bar */}
        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-300 ${
              quality === 'excellent'
                ? 'bg-green-500 w-full'
                : quality === 'good'
                ? 'bg-blue-500 w-3/4'
                : quality === 'fair'
                ? 'bg-yellow-500 w-1/2'
                : 'bg-red-500 w-1/4'
            }`}
          />
        </div>
      </div>

      {/* Instructions */}
      <div className={`p-4 rounded-xl border ${qualityColors[quality]}`}>
        <div className="flex gap-3">
          {quality === 'poor' ? (
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
          ) : (
            <CheckCircle className="w-5 h-5 flex-shrink-0" />
          )}
          <div className="flex-1">
            <p className="font-semibold text-sm">
              {modalityType === 'facial' && 'Olhe diretamente para a câmera'}
              {modalityType === 'fingerprint' && 'Coloque o dedo no centro'}
              {modalityType === 'iris' && 'Abra os olhos naturalmente'}
            </p>
            <p className="text-xs opacity-75 mt-1">
              {quality === 'poor' && 'Melhore a iluminação ou posição'}
              {quality === 'fair' && 'Continue a afinar a posição'}
              {quality === 'good' && 'Qualidade aceitável'}
              {quality === 'excellent' && 'Perfeito! Pronto para capturar'}
            </p>
          </div>
        </div>
      </div>

      {/* Frame counter (debug) */}
      <div className="text-xs text-gray-500 text-center">
        Frames processados: {frameCount}
      </div>

      {/* Capture button */}
      <button
        onClick={handleCapture}
        disabled={!captureReady || isProcessing}
        className={`w-full py-3 rounded-xl font-bold transition flex items-center justify-center gap-2 ${
          captureReady && !isProcessing
            ? 'bg-green-600 hover:bg-green-700 text-white cursor-pointer'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        <Camera className="w-5 h-5" />
        {isProcessing ? 'Processando...' : 'Capturar Biometria'}
      </button>
    </div>
  );
};

export default BiometricCapture;
