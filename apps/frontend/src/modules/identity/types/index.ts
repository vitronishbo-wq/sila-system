/**
 * Identity Module - Type Definitions
 * Digital BI Issuance & Biometric Validation
 */

// ============= CITIZEN ENTITIES =============
export interface CitizenProfile {
  id: string;
  national_id_number: string;
  nif: string;
  passport_number?: string | null;
  first_name: string;
  last_name: string;
  full_name: string;
  gender: 'M' | 'F' | 'O';
  birth_date: string;
  marital_status: string;
  nationality: string;
  place_of_birth: string;
  province: string;
  municipality: string;
  phone: string;
  email: string;
  is_verified: boolean;
  verification_level: 'basic' | 'enhanced' | 'biometric';
  status: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED' | 'DECEASED';
  created_at: string;
  updated_at: string;
}

// ============= DIGITAL BI ENTITIES =============
export interface DigitalBIIssueRequest {
  citizen_id: string;
  document_type: 'BI' | 'PASSPORT' | 'RESIDENCE_PERMIT';
  validity_years: number;
  include_mrz: boolean;
  include_nfc: boolean;
  template_version?: string;
}

export interface DigitalBIDocument {
  id: string;
  citizen_id: string;
  document_type: 'BI' | 'PASSPORT' | 'RESIDENCE_PERMIT';
  document_number: string;
  issue_date: string;
  expiry_date: string;
  status: 'PENDING' | 'ISSUED' | 'REVOKED' | 'EXPIRED';
  mrz_data?: string;
  nfc_data?: {
    chip_serial: string;
    chip_status: 'ACTIVE' | 'BLOCKED';
  };
  qr_code_url?: string;
  document_url?: string;
  digital_signature?: {
    signature_hex: string;
    signed_at: string;
    certificate_sn: string;
  };
  created_at: string;
  updated_at: string;
}

// ============= BIOMETRIC VALIDATION =============
export type BiometricType = 'FINGERPRINT' | 'FACE_RECOGNITION' | 'IRIS' | 'VOICE';

export interface BiometricTemplate {
  id: string;
  citizen_id: string;
  biometric_type: BiometricType;
  template_data: string; // Base64 encoded biometric template
  quality_score: number; // 0-100
  capture_date: string;
  device_id?: string;
  location?: string;
  status: 'ACTIVE' | 'INACTIVE' | 'REVOKED';
  created_at: string;
  updated_at: string;
}

export interface BiometricVerification {
  id: string;
  citizen_id: string;
  verification_attempt_id: string;
  biometric_type: BiometricType;
  match_score: number; // 0-100
  is_match: boolean;
  threshold_used: number;
  liveness_detected?: boolean;
  spoof_risk?: 'LOW' | 'MEDIUM' | 'HIGH';
  verified_at: string;
  verifier_notes?: string;
}

export interface BiometricEnrollmentRequest {
  citizen_id: string;
  biometric_type: BiometricType;
  biometric_data: string; // Base64 encoded captured data
  quality_threshold?: number;
  device_id?: string;
  location?: string;
}

export interface BiometricValidationRequest {
  citizen_id: string;
  biometric_type: BiometricType;
  biometric_data: string; // Base64 encoded captured data
  liveness_check?: boolean;
  threshold?: number;
}

// ============= VERIFICATION & VALIDATION =============
export interface VerificationRequest {
  id: string;
  citizen_id: string;
  verification_type: 'DOCUMENT' | 'BIOMETRIC' | 'ADDRESS' | 'COMBINED';
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'REJECTED';
  requested_at: string;
  completed_at?: string;
  verified_by?: string;
  rejection_reason?: string;
  metadata?: Record<string, unknown>;
}

export interface VerificationResult {
  verification_id: string;
  citizen_id: string;
  verification_type: 'DOCUMENT' | 'BIOMETRIC' | 'ADDRESS' | 'COMBINED';
  is_verified: boolean;
  verification_level: 'BASIC' | 'ENHANCED' | 'BIOMETRIC';
  confidence_score: number; // 0-100
  verified_at: string;
  verified_by: string;
  expiry_date?: string;
  audit_trail: AuditEvent[];
}

export interface AuditEvent {
  timestamp: string;
  event_type: string;
  actor_id: string;
  action: string;
  status: 'SUCCESS' | 'FAILURE';
  details?: Record<string, unknown>;
}

// ============= DOCUMENT TEMPLATES =============
export interface BITemplate {
  id: string;
  version: string;
  name: string;
  description: string;
  valid_from: string;
  valid_to?: string;
  fields: TemplateField[];
  security_features: SecurityFeature[];
  is_active: boolean;
}

export interface TemplateField {
  field_name: string;
  display_name: string;
  data_source: string;
  format?: string;
  position: { x: number; y: number; width: number; height: number };
  is_mandatory: boolean;
}

export interface SecurityFeature {
  feature_id: string;
  feature_type: 'HOLOGRAM' | 'WATERMARK' | 'MICROPRINT' | 'UV_INK' | 'BARCODE' | 'QR_CODE' | 'NFC';
  description: string;
  implementation_details?: string;
}

// ============= API RESPONSES =============
export interface DigitalBIIssueResponse {
  request_id: string;
  status: 'ACCEPTED' | 'REJECTED';
  message?: string;
  estimated_ready_date?: string;
  tracking_number?: string;
}

export interface BiometricEnrollmentResponse {
  enrollment_id: string;
  biometric_type: BiometricType;
  status: 'SUCCESS' | 'FAILED';
  quality_score?: number;
  message?: string;
  next_steps?: string[];
}

export interface BiometricValidationResponse {
  verification_id: string;
  is_match: boolean;
  match_score: number;
  liveness_detected?: boolean;
  spoof_risk?: 'LOW' | 'MEDIUM' | 'HIGH';
  message: string;
}

// ============= STATISTICS & REPORTING =============
export interface IdentityAuditLog {
  id: string;
  citizen_id: string;
  action: string;
  resource_type: 'CITIZEN' | 'DIGITAL_BI' | 'BIOMETRIC' | 'VERIFICATION';
  resource_id: string;
  old_value?: unknown;
  new_value?: unknown;
  actor_id: string;
  timestamp: string;
  ip_address?: string;
  user_agent?: string;
}

export interface IdentityStatistics {
  total_citizens: number;
  verified_citizens: number;
  biometric_citizens: number;
  digital_bi_issued: number;
  digital_bi_pending: number;
  verification_pending: number;
  biometric_enrollments_this_month: number;
  verification_success_rate: number; // 0-100
}

export interface CitizenListResponse {
  items: CitizenProfile[];
  total: number;
  limit: number;
  offset: number;
}
