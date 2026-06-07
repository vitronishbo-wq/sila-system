// Re-export all biometric components from a single entry point
export { BiometricCapture } from '@/components/Biometrics/BiometricCapture';
export { BiometricQualityCheck } from '@/components/Biometrics/BiometricQualityCheck';
export { BiometricCaptureFlow } from '@/components/Biometrics/BiometricCaptureFlow';

export type BiometricModalityType = 'facial' | 'fingerprint' | 'iris';

export interface BiometricMetadata {
  modalityType: string;
  captureTimestamp: string;
  qualityScore: number;
  attemptNumber: number;
}
