/**
 * Meteorologia Service - API Integration Layer
 * Handles all communication with weather monitoring backend
 */

import axios from "axios";
import type {
  MeteorologiaEstacao,
  ObservacaoMeteorologica,
  Alert,
  MeteorologiaStats,
  RegionWeatherSummary,
  MeteorologyFilter,
  PaginationParams,
  EstacaoListResponse,
  ObservacaoListResponse,
  AlertListResponse,
  TrendData,
  TimeseriesPoint,
  SSEWeatherUpdate,
} from "../types";

const API_BASE = "/infrastructure-sector/meteorologia";

interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

class MeteorrologiaService {
  private instance = axios.create({
    baseURL: API_BASE,
    headers: {
      "Content-Type": "application/json",
    },
  });

  constructor() {
    // Inject token from localStorage
    this.instance.interceptors.request.use((config) => {
      const token =
        localStorage.getItem("access_token") || localStorage.getItem("admin_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // ============= ESTAÇÕES =============
  async getEstacoes(
    filter?: MeteorologyFilter,
    pagination?: PaginationParams
  ): Promise<EstacaoListResponse> {
    const params: Record<string, unknown> = {
      ...filter,
      ...(pagination && { page: pagination.page, limit: pagination.limit }),
    };

    const response = await this.instance.get<ApiResponse<EstacaoListResponse>>(
      "/estacoes",
      { params }
    );

    return response.data.data || response.data;
  }

  async getEstacao(id: string): Promise<MeteorologiaEstacao> {
    const response = await this.instance.get<ApiResponse<MeteorologiaEstacao>>(
      `/estacoes/${id}`
    );
    return response.data.data || response.data;
  }

  async getEstacoesPorRegiao(provincia: string): Promise<MeteorologiaEstacao[]> {
    const response = await this.instance.get<
      ApiResponse<MeteorologiaEstacao[]>
    >(`/estacoes/provincia/${provincia}`);
    return response.data.data || response.data || [];
  }

  async getStats(): Promise<MeteorologiaStats> {
    const response = await this.instance.get<ApiResponse<MeteorologiaStats>>(
      "/stats"
    );
    return response.data.data || response.data;
  }

  // ============= OBSERVAÇÕES =============
  async getObservacoes(
    filter?: MeteorologyFilter,
    pagination?: PaginationParams
  ): Promise<ObservacaoListResponse> {
    const params: Record<string, unknown> = {
      ...filter,
      ...(pagination && { page: pagination.page, limit: pagination.limit }),
    };

    const response = await this.instance.get<
      ApiResponse<ObservacaoListResponse>
    >("/observacoes", { params });

    return response.data.data || response.data;
  }

  async getUltimaObservacao(estacaoId: string): Promise<ObservacaoMeteorologica> {
    const response = await this.instance.get<
      ApiResponse<ObservacaoMeteorologica>
    >(`/observacoes/latest/${estacaoId}`);
    return response.data.data || response.data;
  }

  async getTrendData(
    estacaoId: string,
    parametro: string,
    dataInicio: string,
    dataFim: string
  ): Promise<TrendData> {
    const response = await this.instance.get<ApiResponse<TimeseriesPoint[]>>(
      `/observacoes/trend/${estacaoId}`,
      {
        params: { parametro, data_inicio: dataInicio, data_fim: dataFim },
      }
    );

    const data = response.data.data || response.data || [];
    const values = (data as TimeseriesPoint[]).map((p) => {
      switch (parametro) {
        case "temperatura":
          return p.temperatura || 0;
        case "humidade":
          return p.humidade || 0;
        case "pressao":
          return p.pressao || 0;
        case "velocidade_vento":
          return p.velocidade_vento || 0;
        case "precipitacao":
          return p.precipitacao || 0;
        default:
          return 0;
      }
    });

    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    const avgValue = values.reduce((a, b) => a + b, 0) / values.length;

    return {
      label: parametro,
      data: values,
      timestamps: (data as TimeseriesPoint[]).map((p) => p.timestamp),
      minValue,
      maxValue,
      avgValue,
      unidade: this.getUnidade(parametro),
    };
  }

  async getPrevisoes(
    estacaoId: string,
    horas: number = 48
  ): Promise<TimeseriesPoint[]> {
    const response = await this.instance.get<
      ApiResponse<TimeseriesPoint[]>
    >(`/previsoes/${estacaoId}`, { params: { horas } });
    return response.data.data || response.data || [];
  }

  // ============= ALERTAS =============
  async getAlertas(
    filter?: MeteorologyFilter,
    pagination?: PaginationParams
  ): Promise<AlertListResponse> {
    const params: Record<string, unknown> = {
      ...filter,
      ...(pagination && { page: pagination.page, limit: pagination.limit }),
    };

    const response = await this.instance.get<ApiResponse<AlertListResponse>>(
      "/alertas",
      { params }
    );

    return response.data.data || response.data;
  }

  async getAlertasEstacao(estacaoId: string): Promise<Alert[]> {
    const response = await this.instance.get<ApiResponse<Alert[]>>(
      `/alertas/estacao/${estacaoId}`
    );
    return response.data.data || response.data || [];
  }

  async resolveAlerta(id: string): Promise<Alert> {
    const response = await this.instance.patch<ApiResponse<Alert>>(
      `/alertas/${id}`,
      { resolvido: true }
    );
    return response.data.data || response.data;
  }

  // ============= REGIONAL SUMMARIES =============
  async getResumoRegional(provincia: string): Promise<RegionWeatherSummary> {
    const response = await this.instance.get<
      ApiResponse<RegionWeatherSummary>
    >(`/resumo-regional/${provincia}`);
    return response.data.data || response.data;
  }

  async getProvincias(): Promise<
    { nome: string; estacoes: number; alertas: number }[]
  > {
    const response = await this.instance.get<ApiResponse<
      { nome: string; estacoes: number; alertas: number }[]
    >>("/provincias");
    return response.data.data || response.data || [];
  }

  // ============= REAL-TIME UPDATES =============
  subscribeToUpdates(
    estacaoId: string,
    onUpdate: (update: SSEWeatherUpdate) => void
  ): EventSource {
    const token =
      localStorage.getItem("access_token") || localStorage.getItem("admin_token");
    const url = `${API_BASE}/updates-stream?estacao_id=${estacaoId}&token=${token}`;

    const eventSource = new EventSource(url);
    let reconnectTimeout: NodeJS.Timeout | null = null;
    let isClosed = false;

    eventSource.onmessage = (event) => {
      if (isClosed) return;

      try {
        const data = JSON.parse(event.data);
        onUpdate(data);
      } catch (error) {
        console.error("Failed to parse SSE message:", error);
      }
    };

    eventSource.onerror = () => {
      if (isClosed) return;

      console.warn("SSE connection error for station", estacaoId, "reconnecting in 5s...");
      eventSource.close();

      if (!isClosed) {
        reconnectTimeout = setTimeout(() => {
          if (!isClosed) {
            this.subscribeToUpdates(estacaoId, onUpdate);
          }
        }, 5000);
      }
    };

    // Attach cleanup method to EventSource object
    const originalClose = eventSource.close.bind(eventSource);
    eventSource.close = function() {
      isClosed = true;
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
      }
      originalClose();
    };

    return eventSource;
  }

  // ============= EXPORTS =============
  async exportDados(
    format: "csv" | "json" | "excel",
    filter?: MeteorologyFilter
  ): Promise<Blob> {
    const response = await this.instance.get(`/export`, {
      params: { format, ...filter },
      responseType: "blob",
    });
    return response.data;
  }

  // ============= UTILITIES =============
  getUnidade(parametro: string): string {
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
}

export const meteorologiaService = new MeteorrologiaService();
