import http from '@/api/http';

export interface SLAViolation {
  id: string;
  service_id: string;
  service_name: string;
  target_hours: number;
  actual_hours: number;
  delta_hours: number;
  breach_percentage: number;
  severity: string;
  province: string;
  created_at: string;
}

export interface SLABreachPrediction {
  service_id: string;
  elapsed_hours: number;
  target_hours: number;
  progress_percentage: number;
  breach_probability: number;
  risk_factors: string[];
  estimated_remaining: number;
  status: string;
}

export interface SLAServiceBase {
  service_id: string;
  service_name: string;
  module: string;
  base_hours: number;
  priority?: string;
  tier?: string;
  version?: string;
}

export const getSLAViolations = async (params?: { days?: number; service_id?: string; province?: string }) => {
  const response = await http.get<SLAViolation[]>('/sla/violations', { params });
  return response.data;
};

export const predictSLABreach = async (serviceId: string, elapsedHours: number, context?: Record<string, any>) => {
  const response = await http.post<SLABreachPrediction>('/sla/predict', {
    service_id: serviceId,
    elapsed_hours: elapsedHours,
    context: context || {},
  });
  return response.data;
};

export const getSLAByService = async (serviceId: string, params?: { province?: string; citizen_type?: string }) => {
  const response = await http.get(`/sla/service/${serviceId}`, { params });
  return response.data;
};

export const listSLAServiceBase = async () => {
  const response = await http.get<SLAServiceBase[]>('/sla/base');
  return response.data;
};
