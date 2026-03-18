import http from '../api/http';

export interface AdminDocumentSummary {
  id: string;
  citizen_id: string;
  citizen_name?: string | null;
  citizen_bi?: string | null;
  citizen_email?: string | null;
  document_type: string;
  file_url?: string | null;
  issued_at?: string | null;
  valid_until?: string | null;
  status?: string | null;
}

export interface AdminDocumentListResponse {
  items: AdminDocumentSummary[];
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

export const adminDocumentService = {
  async list(filters: {
    q?: string;
    document_type?: string;
    bi?: string;
    email?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
  }): Promise<AdminDocumentListResponse> {
    const { q, document_type, bi, email, status, date_from, date_to, limit = 20, offset = 0 } = filters;
    const response = await http.get<AdminDocumentListResponse>('admin/documents', {
      params: {
        q: q || undefined,
        document_type: document_type || undefined,
        bi: bi || undefined,
        email: email || undefined,
        status: status || undefined,
        date_from: date_from || undefined,
        date_to: date_to || undefined,
        limit,
        offset,
      },
    });
    return response.data;
  },

  async getById(id: string): Promise<AdminDocumentSummary> {
    const response = await http.get<AdminDocumentSummary>(`admin/documents/${id}`);
    return response.data;
  },

  async listPresets(): Promise<ExportPresetResponse> {
    const response = await http.get<ExportPresetResponse>('admin/exports/presets', {
      params: { module: 'documents' }
    });
    return response.data;
  },

  async savePreset(name: string, columns: string[]): Promise<ExportPresetResponse> {
    const response = await http.post<ExportPresetResponse>('admin/exports/presets', {
      module: 'documents',
      name,
      columns,
    });
    return response.data;
  },

  async deletePreset(name: string): Promise<ExportPresetResponse> {
    const response = await http.delete<ExportPresetResponse>('admin/exports/presets', {
      params: { module: 'documents', name }
    });
    return response.data;
  },

  async startExportJob(filters: {
    q?: string;
    document_type?: string;
    bi?: string;
    email?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    columns?: string[];
    format?: 'csv' | 'xlsx';
  }): Promise<ExportJobStatus> {
    const response = await http.post<ExportJobStatus>('admin/exports/documents', filters);
    return response.data;
  },

  async getExportJob(jobId: string): Promise<ExportJobStatus> {
    const response = await http.get<ExportJobStatus>(`admin/exports/jobs/${jobId}`);
    return response.data;
  },

  async exportCsv(filters: {
    q?: string;
    document_type?: string;
    bi?: string;
    email?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    columns?: string[];
    format?: 'csv' | 'xlsx';
  }): Promise<void> {
    const response = await http.get('admin/documents/export', {
      params: {
        q: filters.q || undefined,
        document_type: filters.document_type || undefined,
        bi: filters.bi || undefined,
        email: filters.email || undefined,
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
    link.download = match?.[1] || `documents_${new Date().toISOString().slice(0, 10)}.${fallbackExt}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};
