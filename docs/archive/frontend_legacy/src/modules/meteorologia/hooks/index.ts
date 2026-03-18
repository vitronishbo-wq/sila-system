/**
 * Meteorologia Hooks - State Management Layer
 * Encapsulates all weather data fetching and real-time subscriptions
 */

import { useEffect, useState } from "react";
import {
  MeteorologiaEstacao,
  ObservacaoMeteorologica,
  Alert,
  MeteorologiaStats,
  MeteorologyFilter,
  PaginationParams,
  EstacaoListResponse,
  AlertListResponse,
  TrendData,
} from "../types";
import { meteorologiaService } from "../services";

// ============= useMeteorologia =============
/**
 * Main dashboard hook - fetches stats, stations, and alerts in parallel
 * Auto-refreshes every 5 minutes
 */
export function useMeteorologia() {
  const [stats, setStats] = useState<MeteorologiaStats | null>(null);
  const [estacoes, setEstacoes] = useState<MeteorologiaEstacao[]>([]);
  const [alertas, setAlertas] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsData, estacoesList, alertasData] = await Promise.all([
        meteorologiaService.getStats(),
        meteorologiaService.getEstacoes(),
        meteorologiaService.getAlertas(),
      ]);

      setStats(statsData);
      setEstacoes(estacoesList.items || []);
      setAlertas(alertasData.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch data"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchData, 300000);

    return () => clearInterval(interval);
  }, []);

  return { stats, estacoes, alertas, loading, error, refetch: fetchData };
}

// ============= useEstacoes =============
/**
 * Fetches filtered and paginated station list
 */
export function useEstacoes(
  filter?: MeteorologyFilter,
  pagination: PaginationParams = { page: 1, limit: 10 }
) {
  const [estacoes, setEstacoes] = useState<EstacaoListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchEstacoes = async () => {
    try {
      setLoading(true);
      const data = await meteorologiaService.getEstacoes(filter, pagination);
      setEstacoes(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch stations"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEstacoes();
  }, [filter?.provincia, filter?.municipio, pagination.page]);

  return { estacoes, loading, error, refetch: fetchEstacoes };
}

// ============= useEstacao =============
/**
 * Fetches single station with real-time SSE updates
 */
export function useEstacao(estacaoId: string) {
  const [estacao, setEstacao] = useState<MeteorologiaEstacao | null>(null);
  const [observacao, setObservacao] = useState<ObservacaoMeteorologica | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [estacao, obs] = await Promise.all([
          meteorologiaService.getEstacao(estacaoId),
          meteorologiaService.getUltimaObservacao(estacaoId),
        ]);

        setEstacao(estacao);
        setObservacao(obs);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error("Failed to fetch station"));
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Subscribe to real-time updates
    const eventSource = meteorologiaService.subscribeToUpdates(
      estacaoId,
      (update) => {
        setObservacao((prev) =>
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
      }
    );

    return () => {
      eventSource.close();
    };
  }, [estacaoId]);

  return { estacao, observacao, loading, error };
}

// ============= useTrendData =============
/**
 * Fetches historical trend data for charting
 */
export function useTrendData(
  estacaoId: string,
  parametro: string,
  dataInicio: string,
  dataFim: string
) {
  const [trendData, setTrendData] = useState<TrendData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const data = await meteorologiaService.getTrendData(
          estacaoId,
          parametro,
          dataInicio,
          dataFim
        );
        setTrendData(data);
      } catch (error) {
        console.error("Failed to fetch trend data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, [estacaoId, parametro, dataInicio, dataFim]);

  return { trendData, loading };
}

// ============= useAlertas =============
/**
 * Fetches active alerts with optional regional filtering
 * Auto-refreshes every minute
 */
export function useAlertas(provincia?: string) {
  const [alertas, setAlertas] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchAlertas = async () => {
    try {
      setLoading(true);
      const filter: MeteorologyFilter = provincia ? { provincia } : undefined;
      const data = await meteorologiaService.getAlertas(filter);
      setAlertas(data.items || []);
    } catch (error) {
      console.error("Failed to fetch alerts:", error);
    } finally {
      setLoading(false);
    }
  };

  const resolveAlerta = async (id: string) => {
    try {
      await meteorologiaService.resolveAlerta(id);
      // Optimistic update: remove from list
      setAlertas((prev) => prev.filter((a) => a.id !== id));
    } catch (error) {
      console.error("Failed to resolve alert:", error);
    }
  };

  useEffect(() => {
    fetchAlertas();

    // Auto-refresh every minute
    const interval = setInterval(fetchAlertas, 60000);

    return () => clearInterval(interval);
  }, [provincia]);

  return { alertas, loading, resolveAlerta, refetch: fetchAlertas };
}

// ============= useProvincias =============
/**
 * Fetches all provinces with metadata counts
 */
export function useProvincias() {
  const [provincias, setProvincias] = useState<
    { nome: string; estacoes: number; alertas: number }[]
  >([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProvincias = async () => {
      try {
        setLoading(true);
        const data = await meteorologiaService.getProvincias();
        setProvincias(data);
      } catch (error) {
        console.error("Failed to fetch provinces:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProvincias();
  }, []);

  return { provincias, loading };
}

// ============= UTILITY FUNCTIONS =============
export function getUnidade(parametro: string): string {
  const unidades: Record<string, string> = {
    temperatura: "°C",
    humidade: "%",
    precipitacao: "mm",
    velocidade_vento: "m/s",
    pressao: "hPa",
    radiacao_solar: "W/m²",
  };
  return unidades[parametro] || "";
}
