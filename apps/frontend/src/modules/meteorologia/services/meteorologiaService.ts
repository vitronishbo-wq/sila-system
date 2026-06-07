/**
 * Meteorologia Service - API integration layer
 * RESTful client for backend meteorologia endpoints
 */

import axios from 'axios';
import type {
  MeteorologiaEstacao,
  ObservacaoMeteorologica,
  Alert,
  EstacaoListResponse,
  ObservacaoListResponse,
  AlertListResponse,
  MeteorologyFilter,
  PaginationParams,
  MeteorologiaStats,
  RegionWeatherSummary,
  SSEWeatherUpdate,
} from '@/modules/meteorologia/types';
import { API_ORIGIN } from '@/utils/runtime';

const API_BASE = API_ORIGIN || '';

class MeteorologiaService {
  private client = axios.create({
    baseURL: `${API_BASE}/infrastructure-sector/meteorologia`,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // ============= ESTAÇÕES (Stations) =============
  /**
   * Fetch all weather stations with optional filtering
   */
  async getEstacoes(filter?: MeteorologyFilter, pagination?: PaginationParams) {
    const params: Record<string, unknown> = {};
    
    if (filter?.provincia) params.provincia = filter.provincia;
    if (filter?.municipio) params.municipio = filter.municipio;
    if (filter?.statusEstacao) params.status = filter.statusEstacao;
    if (filter?.tipoEstacao) params.tipo = filter.tipoEstacao;
    
    if (pagination) {
      params.page = pagination.page;
      params.limit = pagination.limit;
      if (pagination.sortBy) params.sort_by = pagination.sortBy;
      if (pagination.sortOrder) params.sort_order = pagination.sortOrder;
    }

    const response = await this.client.get<EstacaoListResponse>('/estacoes', { params });
    return response.data;
  }

  /**
   * Get single station by UUID
   */
  async getEstacao(estacaoId: string) {
    const response = await this.client.get<MeteorologiaEstacao>(`/estacoes/${estacaoId}`);
    return response.data;
  }

  /**
   * Get stations grouped by region
   */
  async getEstacoesPorRegiao(provincia: string) {
    const response = await this.client.get<MeteorologiaEstacao[]>(
      `/estacoes/provincia/${encodeURIComponent(provincia)}`
    );
    return response.data;
  }

  /**
   * Get summary stats for all stations
   */
  async getStats() {
    const response = await this.client.get<MeteorologiaStats>('/stats');
    return response.data;
  }

  // ============= OBSERVAÇÕES (Observations) =============
  /**
   * Fetch observations with filtering
   */
  async getObservacoes(
    filter?: MeteorologyFilter & { estacaoId?: string },
    pagination?: PaginationParams
  ) {
    const params: Record<string, unknown> = {};
    
    if (filter?.estacaoId) params.estacao_id = filter.estacaoId;
    if (filter?.dataInicio) params.data_inicio = filter.dataInicio;
    if (filter?.dataFim) params.data_fim = filter.dataFim;
    if (filter?.temAlerta !== undefined) params.tem_alerta = filter.temAlerta;
    
    if (pagination) {
      params.page = pagination.page;
      params.limit = pagination.limit;
    }

    const response = await this.client.get<ObservacaoListResponse>('/observacoes', { params });
    return response.data;
  }

  /**
   * Get latest observation for a station
   */
  async getUltimaObservacao(estacaoId: string) {
    const response = await this.client.get<ObservacaoMeteorologica>(
      `/observacoes/latest/${estacaoId}`
    );
    return response.data;
  }

  /**
   * Get historical data for trend analysis
   */
  async getTrendData(
    estacaoId: string,
    parametro: 'temperatura' | 'humidade' | 'precipitacao' | 'velocidade_vento',
    dataInicio: string,
    dataFim: string
  ) {
    const response = await this.client.get<Array<{ timestamp: string; valor: number }>>(
      `/observacoes/trend/${estacaoId}`,
      {
        params: {
          parametro,
          data_inicio: dataInicio,
          data_fim: dataFim,
        },
      }
    );
    return response.data;
  }

  /**
   * Get forecasted data
   */
  async getPrevisoes(estacaoId: string, horas: number = 48) {
    const response = await this.client.get<ObservacaoMeteorologica[]>(
      `/previsoes/${estacaoId}`,
      { params: { horas } }
    );
    return response.data;
  }

  // ============= ALERTAS (Alerts) =============
  /**
   * Get active alerts
   */
  async getAlertas(filter?: { provincia?: string; tipo?: Alert['tipo'] }, pagination?: PaginationParams) {
    const params: Record<string, unknown> = {};
    
    if (filter?.provincia) params.provincia = filter.provincia;
    if (filter?.tipo) params.tipo = filter.tipo;
    if (pagination) {
      params.page = pagination.page;
      params.limit = pagination.limit;
    }

    const response = await this.client.get<AlertListResponse>('/alertas', { params });
    return response.data;
  }

  /**
   * Get alerts for specific station
   */
  async getAlertasEstacao(estacaoId: string) {
    const response = await this.client.get<Alert[]>(`/alertas/estacao/${estacaoId}`);
    return response.data;
  }

  /**
   * Resolve/dismiss alert
   */
  async resolveAlerta(alertaId: string) {
    const response = await this.client.patch<Alert>(`/alertas/${alertaId}`, {
      resolvido: true,
    });
    return response.data;
  }

  // ============= REGIONAL SUMMARIES =============
  /**
   * Get weather summary for province
   */
  async getResumoRegional(provincia: string) {
    const response = await this.client.get<RegionWeatherSummary>(
      `/resumo-regional/${encodeURIComponent(provincia)}`
    );
    return response.data;
  }

  /**
   * Get all provinces with weather overview
   */
  async getProvincias() {
    const response = await this.client.get<Array<{ nome: string; estacoes: number; alertas: number }>>(
      '/provincias'
    );
    return response.data;
  }

  // ============= REAL-TIME UPDATES =============
  /**
   * Subscribe to SSE updates for station
   * Properly manages EventSource lifecycle to prevent memory leaks and orphaned connections
   */
  subscribeToUpdates(
    estacaoId: string,
    callback: (update: SSEWeatherUpdate) => void
  ): () => void {
    const token = localStorage.getItem('access_token') || localStorage.getItem('admin_token');
    const url = new URL(`${API_BASE}/infrastructure-sector/meteorologia/updates-stream`);
    url.searchParams.set('estacao_id', estacaoId);
    if (token) url.searchParams.set('token', token);

    let eventSource: EventSource | null = new EventSource(url.toString());
    let reconnectTimeout: NodeJS.Timeout | null = null;
    let isClosed = false;

    if (!eventSource) {
      return () => {
        isClosed = true;
      };
    }

    eventSource.onmessage = (event) => {
      if (isClosed) return;

      try {
        const data = JSON.parse(event.data) as SSEWeatherUpdate;
        callback(data);
      } catch (error) {
        console.error('Failed to parse SSE update:', error);
      }
    };

    eventSource.onerror = () => {
      if (isClosed || !eventSource) return;

      console.warn('SSE connection error for station', estacaoId, 'reconnecting in 5s...');
      eventSource.close();
      eventSource = null;

      // Prevent multiple reconnect attempts if already closed
      if (!isClosed) {
        reconnectTimeout = setTimeout(() => {
          if (!isClosed) {
            this.subscribeToUpdates(estacaoId, callback);
          }
        }, 5000);
      }
    };

    // Return cleanup function that prevents reconnection and closes EventSource
    return () => {
      isClosed = true;
      
      // Cancel any pending reconnection
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
      }

      // Properly close the EventSource
      if (eventSource) {
        eventSource.onmessage = null;
        eventSource.onerror = null;
        eventSource.close();
        eventSource = null;
      }
    };
  }

  /**
   * Get historical data via bulk export
   */
  async exportDados(
    format: 'csv' | 'json' | 'excel',
    filter: MeteorologyFilter
  ) {
    const params: Record<string, unknown> = { format };
    
    if (filter.provincia) params.provincia = filter.provincia;
    if (filter.municipio) params.municipio = filter.municipio;
    if (filter.dataInicio) params.data_inicio = filter.dataInicio;
    if (filter.dataFim) params.data_fim = filter.dataFim;

    const response = await this.client.get(`/export`, {
      params,
      responseType: 'blob',
    });
    
    return response.data;
  }
}

export default new MeteorologiaService();
