
import http from '../api/http';

export interface CitizenSummary {
  id: string;
  full_name: string;
  bi_number?: string | null;
  birth_date?: string | null;
  email?: string | null;
  phone?: string | null;
  status?: string | null;
  is_active?: boolean | null;
  created_at?: string | null;
}

export interface CitizenListResponse {
  items: CitizenSummary[];
  total: number;
  limit: number;
  offset: number;
}

export interface ExportPresetResponse {
  module: string;
  presets: { name: string; columns: string[] }[];
}

export interface ExportJobStatus {
  job_id: string;
  status: 'pending' | 'running' | 'done' | 'failed';
  download_url?: string;
  filename?: string;
  error?: string;
}

export const citizenService = {
  async list(filters: {
    q?: string;
    name?: string;
    bi?: string;
    email?: string;
    phone?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
  }): Promise<CitizenListResponse> {
    const { q, name, bi, email, phone, status, date_from, date_to, limit = 20, offset = 0 } = filters;
    const response = await http.get<CitizenListResponse>('admin/citizens', {
      params: {
        q: q || undefined,
        name: name || undefined,
        bi: bi || undefined,
        email: email || undefined,
        phone: phone || undefined,
        status: status || undefined,
        date_from: date_from || undefined,
        date_to: date_to || undefined,
        limit,
        offset
      }
    });
    return response.data;
  },

  async getById(id: string): Promise<CitizenSummary> {
    const response = await http.get<CitizenSummary>(`admin/citizens/${id}`);
    return response.data;
  },

  async listPresets(): Promise<ExportPresetResponse> {
    const response = await http.get<ExportPresetResponse>('admin/exports/presets', {
      params: { module: 'citizens' }
    });
    return response.data;
  },

  async savePreset(name: string, columns: string[]): Promise<ExportPresetResponse> {
    const response = await http.post<ExportPresetResponse>('admin/exports/presets', {
      module: 'citizens',
      name,
      columns,
    });
    return response.data;
  },

  async deletePreset(name: string): Promise<ExportPresetResponse> {
    const response = await http.delete<ExportPresetResponse>('admin/exports/presets', {
      params: { module: 'citizens', name }
    });
    return response.data;
  },

  async startExportJob(filters: {
    q?: string;
    name?: string;
    bi?: string;
    email?: string;
    phone?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    columns?: string[];
    format?: 'csv' | 'xlsx';
  }): Promise<ExportJobStatus> {
    const response = await http.post<ExportJobStatus>('admin/exports/citizens', filters);
    return response.data;
  },

  async getExportJob(jobId: string): Promise<ExportJobStatus> {
    const response = await http.get<ExportJobStatus>(`admin/exports/jobs/${jobId}`);
    return response.data;
  },

  async exportCsv(filters: {
    q?: string;
    name?: string;
    bi?: string;
    email?: string;
    phone?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    columns?: string[];
    format?: 'csv' | 'xlsx';
  }): Promise<void> {
    const response = await http.get('admin/citizens/export', {
      params: {
        q: filters.q || undefined,
        name: filters.name || undefined,
        bi: filters.bi || undefined,
        email: filters.email || undefined,
        phone: filters.phone || undefined,
        status: filters.status || undefined,
        date_from: filters.date_from || undefined,
        date_to: filters.date_to || undefined,
        columns: filters.columns?.length ? filters.columns.join(',') : undefined,
        format: filters.format || 'csv',
      },
      responseType: 'blob',
    });
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    const disposition = response.headers['content-disposition'] as string | undefined;
    const match = disposition?.match(/filename=\"?([^\";]+)\"?/i);
    link.href = url;
    const fallbackExt = filters.format === 'xlsx' ? 'xlsx' : 'csv';
    link.download = match?.[1] || `citizens_${new Date().toISOString().slice(0, 10)}.${fallbackExt}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
};
