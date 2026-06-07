/**
 * Identity Service - Enhanced Citizen Management
 * Digital BI Issuance & Biometric Validation
 */

import http from '@/api/http';
import type {
  CitizenProfile,
  CitizenListResponse,
  DigitalBIIssueRequest,
  DigitalBIIssueResponse,
  DigitalBIDocument,
  BiometricEnrollmentRequest,
  BiometricEnrollmentResponse,
  BiometricValidationRequest,
  BiometricValidationResponse,
  BiometricTemplate,
  BiometricVerification,
  VerificationRequest,
  VerificationResult,
  BITemplate,
  IdentityAuditLog,
  IdentityStatistics,
} from '@/modules/identity/types';

const IDENTITY_API = '/civil-identity';

class IdentityService {
  // ============= CITIZEN MANAGEMENT =============
  async listCitizens(filters: {
    q?: string;
    name?: string;
    bi?: string;
    email?: string;
    phone?: string;
    verification_level?: string;
    status?: string;
    limit?: number;
    offset?: number;
  }): Promise<CitizenListResponse> {
    const response = await http.get<CitizenListResponse>(
      `${IDENTITY_API}/citizens`,
      { params: filters }
    );
    return response.data;
  }

  async getCitizenById(id: string): Promise<CitizenProfile> {
    const response = await http.get<CitizenProfile>(
      `${IDENTITY_API}/citizens/${id}`
    );
    return response.data;
  }

  async getCitizenByNationalId(national_id_number: string): Promise<CitizenProfile> {
    const response = await http.get<CitizenProfile>(
      `${IDENTITY_API}/citizens/by-national-id/${national_id_number}`
    );
    return response.data;
  }

  async updateCitizen(id: string, data: Partial<CitizenProfile>): Promise<CitizenProfile> {
    const response = await http.patch<CitizenProfile>(
      `${IDENTITY_API}/citizens/${id}`,
      data
    );
    return response.data;
  }

  // ============= DIGITAL BI ISSUANCE =============
  /**
   * Request issuance of a new Digital BI document
   */
  async requestDigitalBI(request: DigitalBIIssueRequest): Promise<DigitalBIIssueResponse> {
    const response = await http.post<DigitalBIIssueResponse>(
      `${IDENTITY_API}/digital-bi/request`,
      request
    );
    return response.data;
  }

  /**
   * Get all Digital BI documents for a citizen
   */
  async getDigitalBIDocuments(citizen_id: string): Promise<DigitalBIDocument[]> {
    const response = await http.get<DigitalBIDocument[]>(
      `${IDENTITY_API}/citizens/${citizen_id}/digital-bi`
    );
    return response.data;
  }

  /**
   * Get specific Digital BI document details
   */
  async getDigitalBIDocument(bi_id: string): Promise<DigitalBIDocument> {
    const response = await http.get<DigitalBIDocument>(
      `${IDENTITY_API}/digital-bi/${bi_id}`
    );
    return response.data;
  }

  /**
   * Check status of Digital BI request
   */
  async checkBIRequestStatus(request_id: string): Promise<{
    request_id: string;
    status: string;
    document_id?: string;
    estimated_ready_date?: string;
  }> {
    const response = await http.get(
      `${IDENTITY_API}/digital-bi/request-status/${request_id}`
    );
    return response.data;
  }

  /**
   * Download digital BI document file
   */
  async downloadDigitalBI(bi_id: string): Promise<Blob> {
    const response = await http.get(
      `${IDENTITY_API}/digital-bi/${bi_id}/download`,
      { responseType: 'blob' }
    );
    return response.data;
  }

  /**
   * Revoke an issued Digital BI
   */
  async revokeDigitalBI(bi_id: string, reason: string): Promise<DigitalBIDocument> {
    const response = await http.patch<DigitalBIDocument>(
      `${IDENTITY_API}/digital-bi/${bi_id}/revoke`,
      { revocation_reason: reason }
    );
    return response.data;
  }

  // ============= BIOMETRIC ENROLLMENT =============
  /**
   * Enroll biometric template for a citizen
   */
  async enrollBiometric(
    request: BiometricEnrollmentRequest
  ): Promise<BiometricEnrollmentResponse> {
    const response = await http.post<BiometricEnrollmentResponse>(
      `${IDENTITY_API}/citizens/${request.citizen_id}/biometric/enroll`,
      request
    );
    return response.data;
  }

  /**
   * Get enrolled biometric templates for citizen
   */
  async getBiometricTemplates(citizen_id: string): Promise<BiometricTemplate[]> {
    const response = await http.get<BiometricTemplate[]>(
      `${IDENTITY_API}/citizens/${citizen_id}/biometric/templates`
    );
    return response.data;
  }

  /**
   * Delete a biometric template
   */
  async deleteBiometricTemplate(template_id: string): Promise<void> {
    await http.delete(`${IDENTITY_API}/biometric/templates/${template_id}`);
  }

  // ============= BIOMETRIC VALIDATION =============
  /**
   * Verify citizen using biometric data
   */
  async validateBiometric(
    request: BiometricValidationRequest
  ): Promise<BiometricValidationResponse> {
    const response = await http.post<BiometricValidationResponse>(
      `${IDENTITY_API}/citizens/${request.citizen_id}/biometric/validate`,
      request
    );
    return response.data;
  }

  /**
   * Get biometric verification history
   */
  async getBiometricVerificationHistory(
    citizen_id: string,
    limit = 50
  ): Promise<BiometricVerification[]> {
    const response = await http.get<BiometricVerification[]>(
      `${IDENTITY_API}/citizens/${citizen_id}/biometric/verification-history`,
      { params: { limit } }
    );
    return response.data;
  }

  // ============= VERIFICATION MANAGEMENT =============
  /**
   * Start a verification request
   */
  async requestVerification(
    citizen_id: string,
    verification_type: 'DOCUMENT' | 'BIOMETRIC' | 'ADDRESS' | 'COMBINED'
  ): Promise<VerificationRequest> {
    const response = await http.post<VerificationRequest>(
      `${IDENTITY_API}/verification/request`,
      { citizen_id, verification_type }
    );
    return response.data;
  }

  /**
   * Get verification request status
   */
  async getVerificationStatus(request_id: string): Promise<VerificationRequest> {
    const response = await http.get<VerificationRequest>(
      `${IDENTITY_API}/verification/${request_id}`
    );
    return response.data;
  }

  /**
   * Get verification results for citizen
   */
  async getVerificationResults(
    citizen_id: string
  ): Promise<VerificationResult[]> {
    const response = await http.get<VerificationResult[]>(
      `${IDENTITY_API}/citizens/${citizen_id}/verification-results`
    );
    return response.data;
  }

  /**
   * Get latest verification for citizen
   */
  async getLatestVerification(citizen_id: string): Promise<VerificationResult | null> {
    const response = await http.get<VerificationResult | null>(
      `${IDENTITY_API}/citizens/${citizen_id}/latest-verification`
    );
    return response.data;
  }

  // ============= BI TEMPLATES =============
  /**
   * Get available BI document templates
   */
  async getBITemplates(): Promise<BITemplate[]> {
    const response = await http.get<BITemplate[]>(
      `${IDENTITY_API}/templates/bi`
    );
    return response.data;
  }

  /**
   * Get specific BI template
   */
  async getBITemplate(template_id: string): Promise<BITemplate> {
    const response = await http.get<BITemplate>(
      `${IDENTITY_API}/templates/bi/${template_id}`
    );
    return response.data;
  }

  // ============= AUDIT & COMPLIANCE =============
  /**
   * Get audit log for citizen identity operations
   */
  async getAuditLog(
    citizen_id: string,
    filters?: {
      action?: string;
      resource_type?: string;
      date_from?: string;
      date_to?: string;
      limit?: number;
      offset?: number;
    }
  ): Promise<{ items: IdentityAuditLog[]; total: number }> {
    const response = await http.get(
      `${IDENTITY_API}/citizens/${citizen_id}/audit-log`,
      { params: filters }
    );
    return response.data;
  }

  /**
   * Get identity system statistics
   */
  async getIdentityStatistics(): Promise<IdentityStatistics> {
    const response = await http.get<IdentityStatistics>(
      `${IDENTITY_API}/statistics`
    );
    return response.data;
  }

  // ============= EXPORT & REPORTING =============
  /**
   * Export citizen identity data
   */
  async exportIdentityData(filters: {
    citizen_ids?: string[];
    verification_level?: string;
    export_format?: 'csv' | 'json' | 'pdf';
  }): Promise<Blob> {
    const response = await http.get(
      `${IDENTITY_API}/export`,
      {
        params: filters,
        responseType: 'blob',
      }
    );
    return response.data;
  }

  /**
   * Generate verification certificate
   */
  async generateVerificationCertificate(
    verification_id: string,
    format: 'pdf' | 'xml'
  ): Promise<Blob> {
    const response = await http.get(
      `${IDENTITY_API}/verification/${verification_id}/certificate`,
      {
        params: { format },
        responseType: 'blob',
      }
    );
    return response.data;
  }
}

export const identityService = new IdentityService();
