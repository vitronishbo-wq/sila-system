// Re-export all biometric components from a single entry point
export { BiometricCapture } from './BiometricCapture';
export { BiometricQualityCheck } from './BiometricQualityCheck';
export { BiometricCaptureFlow } from './BiometricCaptureFlow';

export type BiometricModalityType = 'facial' | 'fingerprint' | 'iris';

export interface BiometricMetadata {
  modalityType: string;
  captureTimestamp: string;
  qualityScore: number;
  attemptNumber: number;
}
