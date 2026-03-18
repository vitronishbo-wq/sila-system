/**
 * Identity Module - Utility Functions
 * interfaces/frontend - Business logic helpers for identity operations
 */

import type {
  DigitalBIDocument,
  VerificationResult,
  AuditEvent,
  CitizenProfile,
} from '../types';

// ============= BIOMETRIC PROCESSING =============

/**
 * Convert captured biometric file to Base64 string for API transmission
 */
export function convertBiometricToBase64(file: File | Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      resolve(base64.split(',')[1] || base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * Calculate biometric template quality score
 * Considers: brightness (20%), contrast (25%), sharpness (30%), completeness (25%)
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
  const metrics = deviceMetrics || {};
  const brightness = metrics.brightness || 50;
  const contrast = metrics.contrast || 50;
  const sharpness = metrics.sharpness || 50;
  const completeness = metrics.completeness || 50;

  const score =
    brightness * 0.2 + contrast * 0.25 + sharpness * 0.3 + completeness * 0.25;

  return Math.min(100, Math.max(0, Math.round(score)));
}

/**
 * Check if biometric quality is acceptable
 */
export function isBiometricQualityAcceptable(
  qualityScore: number,
  threshold: number = 70
): { isAcceptable: boolean; message: string } {
  if (qualityScore >= threshold) {
    return {
      isAcceptable: true,
      message: `Quality score ${qualityScore} meets requirement (${threshold})`,
    };
  }

  const feedback =
    qualityScore < 30
      ? 'Poor quality - try again with better lighting and positioning'
      : qualityScore < 60
        ? 'Quality below threshold - adjust capture and retry'
        : 'Quality slightly below threshold - improve positioning and try again';

  return {
    isAcceptable: false,
    message: `${feedback}. Current: ${qualityScore}, Required: ${threshold}`,
  };
}

// ============= QR CODE GENERATION =============

/**
 * Generate QR code data for digital BI document
 * Format: v1:{nid}:{name}:{birth_date}:{document_id}:{issue_date}:{expiry_date}:{timestamp}
 */
export function generateBIQRCodeData(citizenData: {
  national_id: string;
  name: string;
  birth_date: string;
  document_id: string;
  issue_date: string;
  expiry_date: string;
  signature?: string;
}): string {
  const timestamp = new Date().toISOString();
  return JSON.stringify({
    v: 1,
    nid: citizenData.national_id,
    n: citizenData.name,
    bd: citizenData.birth_date,
    did: citizenData.document_id,
    ied: citizenData.issue_date,
    xed: citizenData.expiry_date,
    ts: timestamp,
    sig: citizenData.signature,
  });
}

/**
 * Parse QR code data string back to structured object
 */
export function parseBIQRCodeData(qrString: string): {
  version: number;
  national_id: string;
  name: string;
  birth_date: string;
  document_id: string;
  issue_date: string;
  expiry_date: string;
  timestamp: string;
  signature?: string;
} {
  const data = JSON.parse(qrString);
  return {
    version: data.v,
    national_id: data.nid,
    name: data.n,
    birth_date: data.bd,
    document_id: data.did,
    issue_date: data.ied,
    expiry_date: data.xed,
    timestamp: data.ts,
    signature: data.sig,
  };
}

// ============= DOCUMENT VALIDATION =============

/**
 * Check if digital BI document is valid
 */
export function isDigitalBIValid(document: DigitalBIDocument): {
  isValid: boolean;
  reason?: string;
} {
  if (document.status !== 'ISSUED') {
    return { isValid: false, reason: `Document status is ${document.status}` };
  }

  const today = new Date();
  const expiryDate = new Date(document.expiry_date);

  if (expiryDate < today) {
    return { isValid: false, reason: 'Document has expired' };
  }

  return { isValid: true };
}

/**
 * Get number of days until BI document expires
 */
export function getDaysUntilExpiry(expiryDate: string): number {
  const today = new Date();
  const expiry = new Date(expiryDate);
  const diffMs = expiry.getTime() - today.getTime();
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
  return diffDays;
}

/**
 * Check if BI document is expiring soon
 */
export function isBIExpiringSoon(expiryDate: string, warningDays: number = 90): boolean {
  const daysUntilExpiry = getDaysUntilExpiry(expiryDate);
  return daysUntilExpiry <= warningDays && daysUntilExpiry > 0;
}

// ============= VERIFICATION MATCHING =============

/**
 * Convert biometric match score to verification decision
 */
export function getVerificationResult(
  matchScore: number,
  threshold: number = 95,
  spoof_risk?: 'LOW' | 'MEDIUM' | 'HIGH'
): { isMatch: boolean; confidence: 'HIGH' | 'MEDIUM' | 'LOW'; message: string } {
  let confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  let message: string;

  if (matchScore >= threshold) {
    confidence = 'HIGH';
    message = 'Match verified successfully';
  } else if (matchScore >= threshold - 15) {
    confidence = 'MEDIUM';
    message = 'Partial match - manual verification recommended';
  } else {
    confidence = 'LOW';
    message = 'No match detected';
  }

  if (spoof_risk === 'HIGH') {
    message += ' (Warning: High spoof risk detected)';
  }

  return {
    isMatch: matchScore >= threshold,
    confidence,
    message,
  };
}

/**
 * Determine verification level from verification methods
 */
export function determineVerificationLevel(
  methods: string[]
): 'BASIC' | 'ENHANCED' | 'BIOMETRIC' {
  if (methods.includes('BIOMETRIC') || methods.includes('FACE_RECOGNITION')) {
    return 'BIOMETRIC';
  }
  if (methods.includes('DOCUMENT') && methods.includes('ADDRESS')) {
    return 'ENHANCED';
  }
  return 'BASIC';
}

// ============= AUDIT & COMPLIANCE =============

/**
 * Create audit event record
 */
export function createAuditEvent(
  eventType: string,
  actorId: string,
  action: string,
  status: 'SUCCESS' | 'FAILURE',
  details?: Record<string, unknown>
): AuditEvent {
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
 * Format audit event for display
 */
export function formatAuditEvent(event: AuditEvent): string {
  const date = new Date(event.timestamp).toLocaleString();
  const statusIcon = event.status === 'SUCCESS' ? '✓' : '✗';
  return `${date} [${statusIcon}] ${event.event_type}: ${event.action}`;
}

// ============= EXPORT & FORMATTING =============

/**
 * Format citizen data for CSV/JSON export
 */
export function formatCitizenDataForExport(
  citizen: CitizenProfile,
  format: 'csv' | 'json'
): string {
  if (format === 'json') {
    return JSON.stringify(citizen, null, 2);
  }

  // CSV format
  const headers = [
    'ID',
    'National ID',
    'NIF',
    'Full Name',
    'Email',
    'Phone',
    'Verification Level',
    'Status',
    'Created At',
  ];

  const values = [
    citizen.id,
    citizen.national_id_number,
    citizen.nif,
    citizen.full_name,
    citizen.email,
    citizen.phone,
    citizen.verification_level,
    citizen.status,
    citizen.created_at,
  ];

  const headerRow = headers.map((h) => `"${h}"`).join(',');
  const valueRow = values.map((v) => `"${v?.toString() || ''}"`).join(',');

  return `${headerRow}\n${valueRow}`;
}

/**
 * Generate verification certificate data for PDF generation
 */
export function generateVerificationCertificateData(
  verification: VerificationResult,
  issuingAuthority: string = 'Republic of Madagascar - Civil Identity Authority'
): {
  certificate_number: string;
  issued_date: string;
  citizen_id: string;
  verification_type: string;
  verification_level: string;
  confidence_score: number;
  valid_until: string;
  issuing_authority: string;
} {
  const certNumber = `CERT-${Date.now()}-${Math.random().toString(36).substring(7).toUpperCase()}`;
  const validUntilDate = new Date();
  validUntilDate.setFullYear(validUntilDate.getFullYear() + 1);

  return {
    certificate_number: certNumber,
    issued_date: new Date().toISOString().split('T')[0],
    citizen_id: verification.citizen_id,
    verification_type: verification.verification_type,
    verification_level: verification.verification_level,
    confidence_score: verification.confidence_score,
    valid_until: validUntilDate.toISOString().split('T')[0],
    issuing_authority: issuingAuthority,
  };
}
