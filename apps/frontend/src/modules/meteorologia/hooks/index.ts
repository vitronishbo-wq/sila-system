/**
 * Meteorologia Hooks - State Management
 * React hooks for weather monitoring state
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import meteorologiaService from '../services/meteorologiaService';
import type {
  MeteorologiaEstacao,
  ObservacaoMeteorologica,
  Alert,
  MeteorologyFilter,
  PaginationParams,
  MeteorologiaStats,
  TrendData,
  SSEWeatherUpdate,
  EstacaoListResponse,
} from '../types';

// ============= DASHBOARD HOOK =============
/**
 * useMeteorologia - Main dashboard hook for all weather data
 * Handles parallel fetch of stats, stations, and alerts
 */
export const useMeteorologia = () => {
  const [stats, setStats] = useState<MeteorologiaStats | null>(null);
  const [estacoes, setEstacoes] = useState<MeteorologiaEstacao[]>([]);
  const [alertas, setAlertas] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchAllData = useCallback(async () => {
    try {
      setLoading(true);
      const [statsData, estacResult, alertResult] = await Promise.all([
        meteorologiaService.getStats(),
        meteorologiaService.getEstacoes({}, { page: 1, limit: 50 }),
        meteorologiaService.getAlertas({}, { page: 1, limit: 20 }),
      ]);

      setStats(statsData);
      setEstacoes(estacResult.items);
      setAlertas(alertResult.items);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao carregar dados'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 300000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, [fetchAllData]);

  return { stats, estacoes, alertas, loading, error, refetch: fetchAllData };
};

// ============= ESTAÇÕES HOOK =============
/**
 * useEstacoes - Fetch and manage weather stations
 * Supports filtering and pagination
 */
export const useEstacoes = (filter?: MeteorologyFilter, pagination?: PaginationParams) => {
  const [data, setData] = useState<EstacaoListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      const result = await meteorologiaService.getEstacoes(filter, pagination);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao carregar estações'));
    } finally {
      setLoading(false);
    }
  }, [filter, pagination]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, refetch: fetch };
};

// ============= SINGLE STATION HOOK =============
/**
 * useEstacao - Fetch single station with latest observation
 * Auto-updates via SSE
 */
export const useEstacao = (estacaoId: string | null) => {
  const [estacao, setEstacao] = useState<MeteorologiaEstacao | null>(null);
  const [observation, setObservation] = useState<ObservacaoMeteorologica | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const unsubscribeRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    if (!estacaoId) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        const [estacaoData, obsData] = await Promise.all([
          meteorologiaService.getEstacao(estacaoId),
          meteorologiaService.getUltimaObservacao(estacaoId),
        ]);
        setEstacao(estacaoData);
        setObservation(obsData);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar estação'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Subscribe to real-time updates
    unsubscribeRef.current = meteorologiaService.subscribeToUpdates(estacaoId, (update) => {
      setObservation((prev) =>
        prev
          ? {
              ...prev,
              temperatura: update.temperatura,
              humidade: update.humidade,
              pressao: update.pressao,
              velocidade_vento: update.velocidade_vento,
              data_observacao: update.timestamp,
            }
          : null
      );
    });

    return () => {
      unsubscribeRef.current?.();
    };
  }, [estacaoId]);

  return { estacao, observation, loading, error };
};

// ============= TRENDS HOOK =============
/**
 * useTrendData - Fetch historical data for charts
 */
export const useTrendData = (
  estacaoId: string,
  parametro: 'temperatura' | 'humidade' | 'precipitacao' | 'velocidade_vento',
  dataInicio: string,
  dataFim: string
) => {
  const [trendData, setTrendData] = useState<TrendData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const rawData = await meteorologiaService.getTrendData(
          estacaoId,
          parametro,
          dataInicio,
          dataFim
        );

        const values = rawData.map((d) => d.valor);
        const trendData: TrendData = {
          label: parametro,
          data: values,
          timestamps: rawData.map((d) => d.timestamp),
          minValue: Math.min(...values),
          maxValue: Math.max(...values),
          avgValue: values.reduce((a, b) => a + b, 0) / values.length,
          unidade: getUnidade(parametro),
        };

        setTrendData(trendData);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar tendências'));
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, [estacaoId, parametro, dataInicio, dataFim]);

  return { trendData, loading, error };
};

// ============= ALERTAS HOOK =============
/**
 * useAlertas - Fetch and manage active alerts
 */
export const useAlertas = (provincia?: string) => {
  const [alertas, setAlertas] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      const result = await meteorologiaService.getAlertas(
        provincia ? { provincia } : undefined,
        { page: 1, limit: 100 }
      );
      setAlertas(result.items);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao carregar alertas'));
    } finally {
      setLoading(false);
    }
  }, [provincia]);

  useEffect(() => {
    fetch();
    const interval = setInterval(fetch, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, [fetch]);

  const resolveAlerta = useCallback(
    async (alertaId: string) => {
      try {
        await meteorologiaService.resolveAlerta(alertaId);
        setAlertas((prev) => prev.filter((a) => a.id !== alertaId));
      } catch (err) {
        console.error('Failed to resolve alert:', err);
      }
    },
    []
  );

  return { alertas, loading, error, refetch: fetch, resolveAlerta };
};

// ============= PROVINCIAS HOOK =============
/**
 * useProvincias - Fetch all provinces with weather overview
 */
export const useProvincias = () => {
  const [provincias, setProvincias] = useState<Array<{ nome: string; estacoes: number; alertas: number }>>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const data = await meteorologiaService.getProvincias();
        setProvincias(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar províncias'));
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, []);

  return { provincias, loading, error };
};

// ============= UTILITIES =============
const getUnidade = (parametro: string): string => {
  const unidades: Record<string, string> = {
    temperatura: '°C',
    humidade: '%',
    precipitacao: 'mm',
    velocidade_vento: 'm/s',
    pressao: 'hPa',
    radiacao_solar: 'W/m²',
  };
  return unidades[parametro] || '';
};
