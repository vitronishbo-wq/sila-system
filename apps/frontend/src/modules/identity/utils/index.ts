/**
 * Identity Utilities
 * Biometric processing, QR code generation, document signing
 */

// ============= BIOMETRIC DATA PROCESSING =============
/**
 * Convert biometric image to base64 for transmission
 */
export function convertBiometricToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      // Extract Base64 content without data URI prefix if present
      const base64Content = base64.includes(',') ? base64.split(',')[1] : base64;
      resolve(base64Content);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * Extract quality score from biometric device response
 */
export function calculateBiometricQuality(
  _templateData: string,
  deviceMetrics?: {
    brightness?: number;
    contrast?: number;
    sharpness?: number;
    completeness?: number;
  }
): number {
  if (!deviceMetrics) {
    // Default: assume good quality if no metrics provided
    return 85;
  }

  const weights = {
    brightness: 0.2,
    contrast: 0.25,
    sharpness: 0.3,
    completeness: 0.25,
  };

  let score = 0;
  let totalWeight = 0;

  if (deviceMetrics.brightness !== undefined) {
    // Normalize brightness to 0-100
    const normalizedBrightness = Math.min(100, Math.max(0, deviceMetrics.brightness));
    score += normalizedBrightness * weights.brightness;
    totalWeight += weights.brightness;
  }

  if (deviceMetrics.contrast !== undefined) {
    const normalizedContrast = Math.min(100, Math.max(0, deviceMetrics.contrast));
    score += normalizedContrast * weights.contrast;
    totalWeight += weights.contrast;
  }

  if (deviceMetrics.sharpness !== undefined) {
    const normalizedSharpness = Math.min(100, Math.max(0, deviceMetrics.sharpness));
    score += normalizedSharpness * weights.sharpness;
    totalWeight += weights.sharpness;
  }

  if (deviceMetrics.completeness !== undefined) {
    const normalizedCompleteness = Math.min(100, Math.max(0, deviceMetrics.completeness));
    score += normalizedCompleteness * weights.completeness;
    totalWeight += weights.completeness;
  }

  return totalWeight > 0 ? Math.round(score / totalWeight) : 85;
}

/**
 * Validate biometric quality meets threshold
 */
export function isBiometricQualityAcceptable(
  qualityScore: number,
  threshold = 70
): { isAcceptable: boolean; message: string } {
  if (qualityScore >= threshold) {
    return { isAcceptable: true, message: `Quality score ${qualityScore} meets requirements` };
  }

  const gap = threshold - qualityScore;
  return {
    isAcceptable: false,
    message: `Quality score ${qualityScore} is below threshold of ${threshold} (${gap} points short)`,
  };
}

// ============= QR CODE GENERATION =============
/**
 * Generate QR code data for Digital BI document
 */
export function generateBIQRCodeData(citizenData: {
  national_id_number: string;
  full_name: string;
  birth_date: string;
  document_id: string;
  expiry_date: string;
  issue_date: string;
  signature?: string;
}): string {
  // Format: Custom structure for Digital BI QR codes
  const qrData = {
    v: 1, // Version
    nid: citizenData.national_id_number,
    n: citizenData.full_name,
    bd: citizenData.birth_date,
    did: citizenData.document_id,
    ied: citizenData.issue_date,
    xed: citizenData.expiry_date,
    ts: new Date().getTime(),
    sig: citizenData.signature,
  };

  return JSON.stringify(qrData);
}

/**
 * Parse QR code data from Digital BI
 */
export function parseBIQRCodeData(qrString: string): {
  version: number;
  nationalIdNumber: string;
  fullName: string;
  birthDate: string;
  documentId: string;
  issueDate: string;
  expiryDate: string;
  timestamp: number;
  signature?: string;
} | null {
  try {
    const data = JSON.parse(qrString);
    return {
      version: data.v,
      nationalIdNumber: data.nid,
      fullName: data.n,
      birthDate: data.bd,
      documentId: data.did,
      issueDate: data.ied,
      expiryDate: data.xed,
      timestamp: data.ts,
      signature: data.sig,
    };
  } catch (error) {
    console.error('Failed to parse QR code data:', error);
    return null;
  }
}

// ============= DOCUMENT STATUS & VERIFICATION =============
/**
 * Check if Digital BI document is valid
 */
export function isDigitalBIValid(document: {
  status: string;
  expiry_date: string;
}): { isValid: boolean; reason?: string } {
  const expiry = new Date(document.expiry_date);
  const now = new Date();

  if (document.status !== 'ISSUED') {
    return { isValid: false, reason: `Document status is ${document.status}` };
  }

  if (expiry < now) {
    return { isValid: false, reason: 'Document has expired' };
  }

  return { isValid: true };
}

/**
 * Get days until Digital BI expires
 */
export function getDaysUntilExpiry(expiryDate: string): number {
  const expiry = new Date(expiryDate);
  const now = new Date();
  const diffTime = expiry.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

/**
 * Check if Digital BI is expiring soon
 */
export function isBIExpiringSoon(expiryDate: string, warningDays = 90): boolean {
  return getDaysUntilExpiry(expiryDate) <= warningDays;
}

export const isBIExpiringsoon = isBIExpiringSoon;

// ============= BIOMETRIC MATCHING =============
/**
 * Determine verification result based on match score
 */
export function getVerificationResult(
  matchScore: number,
  threshold = 95,
  spoof_risk?: 'LOW' | 'MEDIUM' | 'HIGH'
): {
  isMatch: boolean;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  message: string;
} {
  // Check spoof risk first
  if (spoof_risk === 'HIGH') {
    return {
      isMatch: false,
      confidence: 'LOW',
      message: 'High spoof risk detected - verification failed',
    };
  }

  if (matchScore >= threshold) {
    return {
      isMatch: true,
      confidence: 'HIGH',
      message: `Match confirmed with ${matchScore}% confidence`,
    };
  }

  if (matchScore >= threshold - 10) {
    return {
      isMatch: false,
      confidence: 'MEDIUM',
      message: `Score ${matchScore}% is below threshold of ${threshold}%`,
    };
  }

  return {
    isMatch: false,
    confidence: 'LOW',
    message: `Score ${matchScore}% indicates no match`,
  };
}

// ============= VERIFICATION LEVEL MAPPING =============
/**
 * Determine verification level based on verification methods
 */
export function determineVerificationLevel(
  methods: Array<'DOCUMENT' | 'BIOMETRIC' | 'ADDRESS'>
): 'BASIC' | 'ENHANCED' | 'BIOMETRIC' {
  if (methods.includes('BIOMETRIC')) {
    return 'BIOMETRIC';
  }

  if (methods.includes('DOCUMENT') && methods.includes('ADDRESS')) {
    return 'ENHANCED';
  }

  if (methods.includes('DOCUMENT')) {
    return 'ENHANCED';
  }

  return 'BASIC';
}

// ============= AUDIT AND COMPLIANCE =============
/**
 * Generate audit event for identity operation
 */
export function createAuditEvent(
  eventType: string,
  actorId: string,
  action: string,
  status: 'SUCCESS' | 'FAILURE',
  details?: Record<string, unknown>
) {
  return {
    timestamp: new Date().toISOString(),
    event_type: eventType,
    actor_id: actorId,
    action,
    status,
    details,
  };
}

/**
 * Format audit log for display
 */
export function formatAuditEvent(event: {
  timestamp: string;
  event_type: string;
  action: string;
  status: string;
}): string {
  const date = new Date(event.timestamp).toLocaleString();
  return `${date} - ${event.event_type}: ${event.action} (${event.status})`;
}

// ============= EXPORT AND FORMATTING =============
/**
 * Format citizen data for export (CSV/JSON)
 */
export function formatCitizenDataForExport(
  citizen: {
    national_id_number: string;
    full_name: string;
    email: string;
    phone: string;
    verification_level: string;
    status: string;
  },
  format: 'csv' | 'json'
): string {
  if (format === 'json') {
    return JSON.stringify(citizen, null, 2);
  }

  // CSV format
  return `"${citizen.national_id_number}","${citizen.full_name}","${citizen.email}","${citizen.phone}","${citizen.verification_level}","${citizen.status}"`;
}

/**
 * Generate verification certificate data (for PDF generation)
 */
export function generateVerificationCertificateData(
  verification: {
    citizen_id: string;
    verification_id: string;
    verification_type: string;
    verified_at: string;
    verification_level: string;
    confidence_score: number;
  },
  issuingAuthority = 'Civil Identity Registry'
) {
  return {
    certificateNumber: `CERT-${verification.verification_id.substring(0, 8).toUpperCase()}`,
    issuedDate: new Date(verification.verified_at).toLocaleDateString(),
    citizenId: verification.citizen_id,
    verificationType: verification.verification_type,
    verificationLevel: verification.verification_level,
    confidenceScore: verification.confidence_score,
    issuingAuthority,
    validUntil: new Date(new Date(verification.verified_at).getTime() + 365 * 24 * 60 * 60 * 1000).toLocaleDateString(),
  };
}
