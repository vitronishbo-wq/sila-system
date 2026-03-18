/**
 * Identity Service - integrations/frontend
 * RESTful API client for identity operations
 * Digital BI Issuance & Biometric Validation
 */

import http from '../../../api/http';
import type {
  CitizenProfile,
  CitizenListResponse,
  DigitalBIDocument,
  DigitalBIIssueRequest,
  DigitalBIIssueResponse,
  BiometricTemplate,
  BiometricEnrollmentRequest,
  BiometricEnrollmentResponse,
  BiometricValidationRequest,
  BiometricValidationResponse,
  BiometricVerification,
  VerificationRequest,
  VerificationResult,
  BITemplate,
  IdentityStatistics,
  IdentityAuditLog,
} from '../types';

/**
 * Identity Service - Singleton pattern
 * Provides all citizen, digital BI, biometric, and verification operations
 */
class IdentityService {
  private baseUrl = '/civil-identity';

  // ============= CITIZEN MANAGEMENT =============

  /**
   * List all citizens with optional filtering
   */
  async listCitizens(filters?: {
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
      `${this.baseUrl}/citizens`,
      { params: filters }
    );
    return response.data;
  }

  /**
   * Get single citizen by ID
   */
  async getCitizenById(citizen_id: string): Promise<CitizenProfile> {
    const response = await http.get<CitizenProfile>(
      `${this.baseUrl}/citizens/${citizen_id}`
    );
    return response.data;
  }

  /**
   * Get citizen by national ID number
   */
  async getCitizenByNationalId(national_id_number: string): Promise<CitizenProfile> {
    const response = await http.get<CitizenProfile>(
      `${this.baseUrl}/citizens/by-nid/${national_id_number}`
    );
    return response.data;
  }

  /**
   * Update citizen profile
   */
  async updateCitizen(
    citizen_id: string,
    data: Partial<CitizenProfile>
  ): Promise<CitizenProfile> {
    const response = await http.put<CitizenProfile>(
      `${this.baseUrl}/citizens/${citizen_id}`,
      data
    );
    return response.data;
  }

  // ============= DIGITAL BI OPERATIONS =============

  /**
   * Request new digital BI issuance
   */
  async requestDigitalBI(
    request: DigitalBIIssueRequest
  ): Promise<DigitalBIIssueResponse> {
    const response = await http.post<DigitalBIIssueResponse>(
      `${this.baseUrl}/digital-bi/request`,
      request
    );
    return response.data;
  }

  /**
   * Get all digital BI documents for citizen
   */
  async getDigitalBIDocuments(citizen_id: string): Promise<DigitalBIDocument[]> {
    const response = await http.get<DigitalBIDocument[]>(
      `${this.baseUrl}/citizens/${citizen_id}/digital-bi`
    );
    return response.data;
  }

  /**
   * Get single digital BI document
   */
  async getDigitalBIDocument(bi_id: string): Promise<DigitalBIDocument> {
    const response = await http.get<DigitalBIDocument>(
      `${this.baseUrl}/digital-bi/${bi_id}`
    );
    return response.data;
  }

  /**
   * Check status of BI issuance request
   */
  async checkBIRequestStatus(request_id: string): Promise<{
    request_id: string;
    status: string;
    message?: string;
  }> {
    const response = await http.get(
      `${this.baseUrl}/digital-bi/requests/${request_id}/status`
    );
    return response.data;
  }

  /**
   * Download digital BI document (returns Blob)
   */
  async downloadDigitalBI(bi_id: string): Promise<Blob> {
    const response = await http.get(
      `${this.baseUrl}/digital-bi/${bi_id}/download`,
      { responseType: 'blob' as const }
    );
    return response.data;
  }

  /**
   * Revoke digital BI document
   */
  async revokeDigitalBI(bi_id: string, reason: string): Promise<{
    success: boolean;
    message: string;
  }> {
    const response = await http.post(`${this.baseUrl}/digital-bi/${bi_id}/revoke`, {
      reason,
    });
    return response.data;
  }

  // ============= BIOMETRIC ENROLLMENT =============

  /**
   * Enroll new biometric template
   */
  async enrollBiometric(
    request: BiometricEnrollmentRequest
  ): Promise<BiometricEnrollmentResponse> {
    const response = await http.post<BiometricEnrollmentResponse>(
      `${this.baseUrl}/citizens/${request.citizen_id}/biometric/enroll`,
      request
    );
    return response.data;
  }

  /**
   * Get all enrolled biometric templates for citizen
   */
  async getBiometricTemplates(citizen_id: string): Promise<BiometricTemplate[]> {
    const response = await http.get<BiometricTemplate[]>(
      `${this.baseUrl}/citizens/${citizen_id}/biometric/templates`
    );
    return response.data;
  }

  /**
   * Delete biometric template
   */
  async deleteBiometricTemplate(template_id: string): Promise<{
    success: boolean;
    message: string;
  }> {
    const response = await http.delete(
      `${this.baseUrl}/biometric/templates/${template_id}`
    );
    return response.data;
  }

  // ============= BIOMETRIC VALIDATION =============

  /**
   * Validate citizen against biometric template
   */
  async validateBiometric(
    request: BiometricValidationRequest
  ): Promise<BiometricValidationResponse> {
    const response = await http.post<BiometricValidationResponse>(
      `${this.baseUrl}/citizens/${request.citizen_id}/biometric/validate`,
      request
    );
    return response.data;
  }

  /**
   * Get biometric verification history for citizen
   */
  async getBiometricVerificationHistory(
    citizen_id: string,
    limit: number = 50
  ): Promise<BiometricVerification[]> {
    const response = await http.get<BiometricVerification[]>(
      `${this.baseUrl}/citizens/${citizen_id}/biometric/history`,
      { params: { limit } }
    );
    return response.data;
  }

  // ============= VERIFICATION WORKFLOWS =============

  /**
   * Request identity verification
   */
  async requestVerification(
    citizen_id: string,
    verification_type: 'DOCUMENT' | 'BIOMETRIC' | 'ADDRESS' | 'COMBINED'
  ): Promise<VerificationRequest> {
    const response = await http.post<VerificationRequest>(
      `${this.baseUrl}/verification/request`,
      { citizen_id, verification_type }
    );
    return response.data;
  }

  /**
   * Get verification request status
   */
  async getVerificationStatus(request_id: string): Promise<VerificationRequest> {
    const response = await http.get<VerificationRequest>(
      `${this.baseUrl}/verification/requests/${request_id}`
    );
    return response.data;
  }

  /**
   * Get all verification results for citizen
   */
  async getVerificationResults(citizen_id: string): Promise<VerificationResult[]> {
    const response = await http.get<VerificationResult[]>(
      `${this.baseUrl}/citizens/${citizen_id}/verifications`
    );
    return response.data;
  }

  /**
   * Get most recent verification result
   */
  async getLatestVerification(citizen_id: string): Promise<VerificationResult | null> {
    const response = await http.get<VerificationResult | null>(
      `${this.baseUrl}/citizens/${citizen_id}/verifications/latest`
    );
    return response.data;
  }

  // ============= TEMPLATES & COMPLIANCE =============

  /**
   * Get available BI document templates
   */
  async getBITemplates(): Promise<BITemplate[]> {
    const response = await http.get<BITemplate[]>(`${this.baseUrl}/bi/templates`);
    return response.data;
  }

  /**
   * Get single BI template
   */
  async getBITemplate(template_id: string): Promise<BITemplate> {
    const response = await http.get<BITemplate>(
      `${this.baseUrl}/bi/templates/${template_id}`
    );
    return response.data;
  }

  /**
   * Get audit log for citizen
   */
  async getAuditLog(
    citizen_id: string,
    filters?: {
      action?: string;
      resource_type?: string;
      start_date?: string;
      end_date?: string;
      limit?: number;
      offset?: number;
    }
  ): Promise<IdentityAuditLog[]> {
    const response = await http.get<IdentityAuditLog[]>(
      `${this.baseUrl}/citizens/${citizen_id}/audit-log`,
      { params: filters }
    );
    return response.data;
  }

  /**
   * Get identity statistics
   */
  async getIdentityStatistics(): Promise<IdentityStatistics> {
    const response = await http.get<IdentityStatistics>(
      `${this.baseUrl}/statistics`
    );
    return response.data;
  }

  // ============= EXPORT & REPORTING =============

  /**
   * Export identity data (CSV/JSON/PDF)
   */
  async exportIdentityData(filters?: {
    format?: 'csv' | 'json' | 'pdf';
    verification_level?: string;
    status?: string;
  }): Promise<Blob> {
    const response = await http.get<Blob>(
      `${this.baseUrl}/export`,
      {
        params: filters,
        responseType: 'blob' as const,
      }
    );
    return response.data;
  }

  /**
   * Generate verification certificate
   */
  async generateVerificationCertificate(
    verification_id: string,
    format: 'pdf' | 'xml' = 'pdf'
  ): Promise<Blob> {
    const response = await http.get<Blob>(
      `${this.baseUrl}/verifications/${verification_id}/certificate`,
      {
        params: { format },
        responseType: 'blob' as const,
      }
    );
    return response.data;
  }
}

export const identityService = new IdentityService();
