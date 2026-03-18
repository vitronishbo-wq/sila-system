/**
 * Identity Module - React Hooks
 * interfaces/frontend - State management for identity operations
 */

import { useState, useEffect, useCallback } from 'react';
import {
  CitizenProfile,
  CitizenListResponse,
  DigitalBIDocument,
  DigitalBIIssueRequest,
  BiometricTemplate,
  BiometricVerification,
  VerificationResult,
  BITemplate,
  IdentityStatistics,
} from '../types';
import { identityService } from './identityService';

/**
 * Hook: Fetch single citizen profile
 * Auto-refetches when citizenId changes
 */
export function useCitizen(citizenId: string | null) {
  const [citizen, setCitizen] = useState<CitizenProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!citizenId) return;

    const fetchCitizen = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await identityService.getCitizenById(citizenId);
        setCitizen(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch citizen');
      } finally {
        setLoading(false);
      }
    };

    fetchCitizen();
  }, [citizenId]);

  return { citizen, loading, error };
}

/**
 * Hook: Fetch paginated citizens list
 * Supports filtering by name, verification level, status, etc.
 */
export function useCitizensList(filters?: {
  q?: string;
  name?: string;
  bi?: string;
  email?: string;
  phone?: string;
  verification_level?: string;
  status?: string;
  limit?: number;
  offset?: number;
}) {
  const [data, setData] = useState<CitizenListResponse>({
    items: [],
    total: 0,
    limit: filters?.limit || 50,
    offset: filters?.offset || 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCitizens = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await identityService.listCitizens(filters);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch citizens');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchCitizens();
  }, [fetchCitizens]);

  return { data, loading, error, refetch: fetchCitizens };
}

/**
 * Hook: Manage digital BI documents
 * Fetch, request, revoke BI documents
 */
export function useDigitalBI(citizenId: string | null) {
  const [documents, setDocuments] = useState<DigitalBIDocument[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    if (!citizenId) return;
    setLoading(true);
    setError(null);
    try {
      const docs = await identityService.getDigitalBIDocuments(citizenId);
      setDocuments(docs);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch BI documents');
    } finally {
      setLoading(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchDocuments();
  }, [citizenId, fetchDocuments]);

  const requestDigitalBI = useCallback(
    async (request: DigitalBIIssueRequest) => {
      try {
        const response = await identityService.requestDigitalBI(request);
        await fetchDocuments(); // Refresh list
        return response;
      } catch (err) {
        throw err;
      }
    },
    [fetchDocuments]
  );

  const revokeDigitalBI = useCallback(
    async (bi_id: string, reason: string) => {
      try {
        const response = await identityService.revokeDigitalBI(bi_id, reason);
        await fetchDocuments(); // Refresh list
        return response;
      } catch (err) {
        throw err;
      }
    },
    [fetchDocuments]
  );

  return {
    documents,
    loading,
    error,
    refetch: fetchDocuments,
    requestDigitalBI,
    revokeDigitalBI,
  };
}

/**
 * Hook: Manage enrolled biometric templates
 */
export function useBiometricTemplates(citizenId: string | null) {
  const [templates, setTemplates] = useState<BiometricTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTemplates = useCallback(async () => {
    if (!citizenId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await identityService.getBiometricTemplates(citizenId);
      setTemplates(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch templates');
    } finally {
      setLoading(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchTemplates();
  }, [citizenId, fetchTemplates]);

  const deleteTemplate = useCallback(
    async (template_id: string) => {
      try {
        const response = await identityService.deleteBiometricTemplate(template_id);
        await fetchTemplates(); // Refresh list
        return response;
      } catch (err) {
        throw err;
      }
    },
    [fetchTemplates]
  );

  return { templates, loading, error, refetch: fetchTemplates, deleteTemplate };
}

/**
 * Hook: Get biometric verification history
 * Read-only audit trail of biometric verifications
 */
export function useBiometricVerificationHistory(citizenId: string | null, limit: number = 50) {
  const [verifications, setVerifications] = useState<BiometricVerification[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!citizenId) return;

    const fetchHistory = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await identityService.getBiometricVerificationHistory(
          citizenId,
          limit
        );
        setVerifications(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch history');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [citizenId, limit]);

  return { verifications, loading, error };
}

/**
 * Hook: Get verification results for citizen
 * Track completed verifications and get latest result
 */
export function useVerificationResults(citizenId: string | null) {
  const [results, setResults] = useState<VerificationResult[]>([]);
  const [loadingResults, setLoadingResults] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchResults = useCallback(async () => {
    if (!citizenId) return;
    setLoadingResults(true);
    setError(null);
    try {
      const data = await identityService.getVerificationResults(citizenId);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch results');
    } finally {
      setLoadingResults(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  const getLatestVerification = useCallback(async () => {
    if (!citizenId) return null;
    try {
      return await identityService.getLatestVerification(citizenId);
    } catch (err) {
      throw err;
    }
  }, [citizenId]);

  return { results, loadingResults, error, refetch: fetchResults, getLatestVerification };
}

/**
 * Hook: Get available BI document templates
 * One-time fetch on mount
 */
export function useBITemplates() {
  const [templates, setTemplates] = useState<BITemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTemplates = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await identityService.getBITemplates();
        setTemplates(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch templates');
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  return { templates, loading, error };
}

/**
 * Hook: Get identity system statistics
 * Auto-refreshes every 5 minutes by default
 */
export function useIdentityStatistics(refreshInterval: number = 300000) {
  const [stats, setStats] = useState<IdentityStatistics>({
    total_citizens: 0,
    verified_citizens: 0,
    biometric_citizens: 0,
    digital_bi_issued: 0,
    digital_bi_pending: 0,
    verification_pending: 0,
    biometric_enrollments_this_month: 0,
    verification_success_rate: 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await identityService.getIdentityStatistics();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch statistics');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refetch();
    const interval = setInterval(refetch, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval, refetch]);

  return { stats, loading, error, refetch };
}
