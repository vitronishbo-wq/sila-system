/**
 * Identity Hooks - State Management Layer
 * Digital BI & Biometric Validation
 */

import { useState, useCallback, useEffect } from 'react';
import { identityService } from '@/modules/identity/services/identityService';
import type {
  CitizenProfile,
  CitizenListResponse,
  DigitalBIDocument,
  DigitalBIIssueRequest,
  BiometricTemplate,
  BiometricVerification,
  VerificationResult,
  BITemplate,
  IdentityStatistics,
} from '@/modules/identity/types';

// ============= USE CITIZEN =============
export function useCitizen(citizenId: string | null) {
  const [citizen, setCitizen] = useState<CitizenProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!citizenId) return;

    const fetchCitizen = async () => {
      try {
        setLoading(true);
        const data = await identityService.getCitizenById(citizenId);
        setCitizen(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch citizen'));
      } finally {
        setLoading(false);
      }
    };

    fetchCitizen();
  }, [citizenId]);

  return { citizen, loading, error };
}

// ============= USE CITIZENS LIST =============
export function useCitizensList(filters?: {
  q?: string;
  name?: string;
  bi?: string;
  verification_level?: string;
  limit?: number;
  offset?: number;
}) {
  const [data, setData] = useState<CitizenListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchCitizens = useCallback(async () => {
    try {
      setLoading(true);
      const result = await identityService.listCitizens(filters || {});
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch citizens'));
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchCitizens();
  }, [filters]);

  return { data, loading, error, refetch: fetchCitizens };
}

// ============= USE DIGITAL BI =============
export function useDigitalBI(citizenId: string | null) {
  const [documents, setDocuments] = useState<DigitalBIDocument[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchDocuments = useCallback(async () => {
    if (!citizenId) return;

    try {
      setLoading(true);
      const docs = await identityService.getDigitalBIDocuments(citizenId);
      setDocuments(docs);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch BI documents'));
    } finally {
      setLoading(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchDocuments();
  }, [citizenId]);

  const requestDigitalBI = useCallback(
    async (request: DigitalBIIssueRequest) => {
      try {
        const response = await identityService.requestDigitalBI(request);
        // Refresh documents after successful request
        if (response.status === 'ACCEPTED') {
          await fetchDocuments();
        }
        return response;
      } catch (err) {
        throw err instanceof Error ? err : new Error('Failed to request BI');
      }
    },
    [fetchDocuments]
  );

  const revokeDigitalBI = useCallback(
    async (bi_id: string, reason: string) => {
      try {
        const doc = await identityService.revokeDigitalBI(bi_id, reason);
        // Update local state
        setDocuments((prev) =>
          prev.map((d) => (d.id === bi_id ? doc : d))
        );
        return doc;
      } catch (err) {
        throw err instanceof Error ? err : new Error('Failed to revoke BI');
      }
    },
    []
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

// ============= USE BIOMETRIC TEMPLATES =============
export function useBiometricTemplates(citizenId: string | null) {
  const [templates, setTemplates] = useState<BiometricTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchTemplates = useCallback(async () => {
    if (!citizenId) return;

    try {
      setLoading(true);
      const data = await identityService.getBiometricTemplates(citizenId);
      setTemplates(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch biometric templates'));
    } finally {
      setLoading(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchTemplates();
  }, [citizenId]);

  const deleteBiometricTemplate = useCallback(
    async (template_id: string) => {
      try {
        await identityService.deleteBiometricTemplate(template_id);
        // Update local state
        setTemplates((prev) => prev.filter((t) => t.id !== template_id));
      } catch (err) {
        throw err instanceof Error ? err : new Error('Failed to delete biometric template');
      }
    },
    []
  );

  return {
    templates,
    loading,
    error,
    refetch: fetchTemplates,
    deleteTemplate: deleteBiometricTemplate,
  };
}

// ============= USE BIOMETRIC VERIFICATION HISTORY =============
export function useBiometricVerificationHistory(
  citizenId: string | null,
  limit = 50
) {
  const [verifications, setVerifications] = useState<BiometricVerification[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!citizenId) return;

    const fetchHistory = async () => {
      try {
        setLoading(true);
        const data = await identityService.getBiometricVerificationHistory(
          citizenId,
          limit
        );
        setVerifications(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch verification history'));
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [citizenId, limit]);

  return { verifications, loading, error };
}

// ============= USE VERIFICATION RESULTS =============
export function useVerificationResults(citizenId: string | null) {
  const [results, setResults] = useState<VerificationResult[]>([]);
  const [loadingResults, setLoadingResults] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchResults = useCallback(async () => {
    if (!citizenId) return;

    try {
      setLoadingResults(true);
      const data = await identityService.getVerificationResults(citizenId);
      setResults(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch verification results'));
    } finally {
      setLoadingResults(false);
    }
  }, [citizenId]);

  useEffect(() => {
    fetchResults();
  }, [citizenId]);

  const getLatestVerification = useCallback(async () => {
    if (!citizenId) return null;
    try {
      return await identityService.getLatestVerification(citizenId);
    } catch (err) {
      console.error('Failed to fetch latest verification:', err);
      return null;
    }
  }, [citizenId]);

  return {
    results,
    loadingResults,
    error,
    refetch: fetchResults,
    getLatestVerification,
  };
}

// ============= USE BI TEMPLATES =============
export function useBITemplates() {
  const [templates, setTemplates] = useState<BITemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        setLoading(true);
        const data = await identityService.getBITemplates();
        setTemplates(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch BI templates'));
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  return { templates, loading, error };
}

// ============= USE IDENTITY STATISTICS =============
export function useIdentityStatistics(refreshInterval = 300000) {
  const [stats, setStats] = useState<IdentityStatistics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchStatistics = useCallback(async () => {
    try {
      setLoading(true);
      const data = await identityService.getIdentityStatistics();
      setStats(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch statistics'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatistics();

    // Optional: Set up auto-refresh interval
    const interval = setInterval(fetchStatistics, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  return { stats, loading, error, refetch: fetchStatistics };
}
