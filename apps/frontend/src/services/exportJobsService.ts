import http from '../api/http';

export interface ExportJobItem {
  job_id: string;
  module: string;
  status: 'pending' | 'running' | 'done' | 'failed' | 'not_found' | 'forbidden';
  created_at?: string | null;
  updated_at?: string | null;
  result_filename?: string | null;
  error?: string | null;
  duration_seconds?: number | null;
  estimated_seconds?: number | null;
}

export interface ExportJobListResponse {
  items: ExportJobItem[];
  total: number;
  limit: number;
  offset: number;
  averages?: Record<string, number>;
  status_counts?: Record<string, number>;
}

export interface ExportJobStatus {
  job_id: string;
  status: 'pending' | 'running' | 'done' | 'failed' | 'not_found' | 'forbidden';
  download_url?: string;
  filename?: string;
  error?: string;
}

export interface ExportJobDetail {
  job: ExportJobStatus;
  module?: string;
  status?: string;
  created_at?: string | null;
  updated_at?: string | null;
  payload?: Record<string, unknown> | string | null;
  logs?: { level: string; message: string; created_at: string | null }[];
}

export interface ExportTimelineItem {
  day: string | null;
  avg_seconds: number;
  total: number;
}

export interface ExportTimelineCompareResponse {
  series: {
    citizens: ExportTimelineItem[];
    documents: ExportTimelineItem[];
  };
}

export interface ExportPreviewResponse {
  module: string;
  count: number;
  by_status?: Record<string, number>;
}
export const exportJobsService = {
  async list(filters: {
    module?: string;
    status?: string;
    q?: string;
    job_id?: string;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
  }): Promise<ExportJobListResponse> {
    const response = await http.get<ExportJobListResponse>('admin/exports/jobs', {
      params: {
        module: filters.module || undefined,
        status: filters.status || undefined,
        q: filters.q || undefined,
        job_id: filters.job_id || undefined,
        date_from: filters.date_from || undefined,
        date_to: filters.date_to || undefined,
        limit: filters.limit ?? 20,
        offset: filters.offset ?? 0,
      }
    });
    return response.data;
  },

  async get(jobId: string): Promise<ExportJobStatus> {
    const response = await http.get<ExportJobStatus>(`admin/exports/jobs/${jobId}`);
    return response.data;
  },

  async repeat(jobId: string): Promise<ExportJobStatus> {
    const response = await http.post<ExportJobStatus>(`admin/exports/jobs/${jobId}/repeat`);
    return response.data;
  },

  async reprocess(jobId: string, payload: Record<string, unknown>): Promise<ExportJobStatus> {
    const response = await http.post<ExportJobStatus>(`admin/exports/jobs/${jobId}/reprocess`, payload);
    return response.data;
  },

  async detail(jobId: string): Promise<ExportJobDetail> {
    const response = await http.get<ExportJobDetail>(`admin/exports/jobs/${jobId}/detail`);
    return response.data;
  },

  async timeline(filters: { module?: string; days?: number }): Promise<{ items: ExportTimelineItem[] }> {
    const response = await http.get<{ items: ExportTimelineItem[] }>('admin/exports/jobs/timeline', {
      params: {
        module: filters.module || undefined,
        days: filters.days ?? 14,
      }
    });
    return response.data;
  },

  async timelineCompare(days = 14): Promise<ExportTimelineCompareResponse> {
    const response = await http.get<ExportTimelineCompareResponse>('admin/exports/jobs/timeline/compare', {
      params: { days }
    });
    return response.data;
  },

  async preview(module: string, params: Record<string, unknown>): Promise<ExportPreviewResponse> {
    const response = await http.post<ExportPreviewResponse>('admin/exports/preview', {
      module,
      params,
    });
    return response.data;
  },

  async previewDetail(module: string, params: Record<string, unknown>): Promise<ExportPreviewResponse> {
    const response = await http.post<ExportPreviewResponse>('admin/exports/preview/detail', {
      module,
      params,
    });
    return response.data;
  }
};
