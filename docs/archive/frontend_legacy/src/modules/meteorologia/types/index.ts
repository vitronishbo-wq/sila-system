/**
 * Meteorologia Widget - Type Definitions
 * Central hub for climate monitoring data types
 */

// ============= ENTITIES =============
export interface MeteorologiaEstacao {
  id: string;
  codigo: string;
  nome: string;
  latitude: number;
  longitude: number;
  altitude?: number;
  status: "ACTIVE" | "INACTIVE" | "MAINTENANCE";
  municipio?: string;
  provincia?: string;
  metadata?: Record<string, unknown>;
  created_at?: string;
  updated_at?: string;
}

export interface ObservacaoMeteorologica {
  id: string;
  estacao_id: string;
  data_observacao: string;
  temperatura?: number;
  humidade?: number;
  pressao?: number;
  velocidade_vento?: number;
  direcao_vento?: number;
  precipitacao?: number;
  radiacao_solar?: number;
  tipo: "SURFACE" | "UPPER_AIR" | "MARINE";
  qualidade_dados: "VALIDADO" | "PRELIMINAR" | "SUSPEITO";
  has_alerts: boolean;
  alertas?: Alert[];
  metadata?: Record<string, unknown>;
  created_at?: string;
}

export interface Alert {
  id: string;
  tipo: "ALERTA_AMARELO" | "ALERTA_LARANJA" | "ALERTA_VERMELHO";
  titulo: string;
  descricao: string;
  parametro: string;
  valor_observado: number;
  valor_critico: number;
  timestamp: string;
  resolvido?: boolean;
}

// ============= DASHBOARD STATE =============
export interface MeteorologiaStats {
  total_estacoes: number;
  estacoes_ativas: number;
  observacoes_ultimas_24h: number;
  alertas_ativos: number;
  temperatura_media: number;
  precipitacao_total: number;
}

export interface RegionWeatherSummary {
  provincia: string;
  municipios: number;
  estacoes_ativas: number;
  temperatura_min: number;
  temperatura_max: number;
  precipitacao_acumulada: number;
  alertas_count: number;
  imagem_satelite?: string;
}

// ============= FILTER & QUERY STATE =============
export interface MeteorologyFilter {
  provincia?: string;
  municipio?: string;
  tipoEstacao?: "SURFACE" | "UPPER_AIR" | "MARINE";
  statusEstacao?: "ACTIVE" | "INACTIVE" | "MAINTENANCE";
  dataInicio?: string;
  dataFim?: string;
  temAlerta?: boolean;
}

export interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: "asc" | "desc";
}

// ============= RESPONSE SCHEMAS =============
export interface EstacaoListResponse {
  items: MeteorologiaEstacao[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

export interface ObservacaoListResponse {
  items: ObservacaoMeteorologica[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

export interface AlertListResponse {
  items: Alert[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// ============= CHART DATA =============
export interface TimeseriesPoint {
  timestamp: string;
  temperatura?: number;
  humidade?: number;
  pressao?: number;
  velocidade_vento?: number;
  precipitacao?: number;
}

export interface TrendData {
  label: string;
  data: number[];
  timestamps: string[];
  minValue: number;
  maxValue: number;
  avgValue: number;
  unidade: string;
}

// ============= LIVE UPDATES =============
export interface SSEWeatherUpdate {
  estacao_id: string;
  estacao_nome: string;
  temperatura: number;
  humidade: number;
  pressao: number;
  velocidade_vento: number;
  timestamp: string;
  alerta?: Alert;
}

export interface WebSocketMessage {
  type: "observation_update" | "alert_triggered" | "station_offline" | "forecast_update";
  data: unknown;
  timestamp: string;
}
