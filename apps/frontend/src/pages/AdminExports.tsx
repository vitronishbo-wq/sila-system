import React, { useEffect, useMemo, useRef, useState } from 'react';
import { API_URL } from '../constants';
import { exportJobsService, ExportJobDetail, ExportJobItem, ExportJobStatus, ExportTimelineItem } from '../services/exportJobsService';
import { useToast } from '../hooks/useToast';

const formatDateTime = (value?: string | null) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString('pt-PT');
};

const statusStyles = (status?: string | null) => {
  const normalized = (status || '').toLowerCase();
  if (normalized === 'done') return 'bg-emerald-50 text-emerald-700';
  if (normalized === 'running') return 'bg-blue-50 text-blue-700';
  if (normalized === 'failed') return 'bg-rose-50 text-rose-600';
  return 'bg-amber-50 text-amber-700';
};

const formatDuration = (seconds?: number | null) => {
  if (!seconds && seconds !== 0) return '—';
  const value = Math.max(0, seconds);
  if (value < 60) return `${Math.round(value)}s`;
  if (value < 3600) return `${Math.round(value / 60)}m`;
  return `${(value / 3600).toFixed(1)}h`;
};

const AdminExports: React.FC = () => {
  const [search, setSearch] = useState('');
  const [jobIdFilter, setJobIdFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [moduleFilter, setModuleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [items, setItems] = useState<ExportJobItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [limit, setLimit] = useState(20);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [realtimeMode, setRealtimeMode] = useState<'sse' | 'ws'>('sse');
  const { showToast } = useToast();
  const [detail, setDetail] = useState<ExportJobDetail | null>(null);
  const [timeline, setTimeline] = useState<{ citizens: ExportTimelineItem[]; documents: ExportTimelineItem[] }>({
    citizens: [],
    documents: [],
  });
  const [detailLogs, setDetailLogs] = useState<{ level: string; message: string; created_at: string | null }[]>([]);
  const [liveLogs, setLiveLogs] = useState<Record<string, { level: string; message: string; created_at: string | null }>>({});
  const [showReprocessEditor, setShowReprocessEditor] = useState(false);
  const [reprocessForm, setReprocessForm] = useState({
    format: 'csv',
    columns: '',
    q: '',
    name: '',
    bi: '',
    email: '',
    phone: '',
    status: '',
    document_type: '',
    date_from: '',
    date_to: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [previewCount, setPreviewCount] = useState<number | null>(null);
  const [previewBreakdown, setPreviewBreakdown] = useState<Record<string, number> | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [logLevelFilter, setLogLevelFilter] = useState('');
  const [logSearch, setLogSearch] = useState('');
  const [timelineMode, setTimelineMode] = useState<'compare' | 'citizens' | 'documents'>('compare');
  const [timelineDays, setTimelineDays] = useState(14);
  const [logPulseAt, setLogPulseAt] = useState<number | null>(null);

  const apiRoot = useMemo(() => API_URL.replace(/\/api\/?$/, ''), []);
  const wsRoot = useMemo(() => apiRoot.replace(/^http/, 'ws'), [apiRoot]);
  const mergedTimeline = useMemo(() => {
    const map = new Map<string, { day: string; citizens?: ExportTimelineItem; documents?: ExportTimelineItem }>();
    timeline.citizens.forEach((item) => {
      if (!item.day) return;
      map.set(item.day, { day: item.day, citizens: item, documents: map.get(item.day)?.documents });
    });
    timeline.documents.forEach((item) => {
      if (!item.day) return;
      map.set(item.day, { day: item.day, citizens: map.get(item.day)?.citizens, documents: item });
    });
    return Array.from(map.values()).sort((a, b) => (a.day > b.day ? 1 : -1));
  }, [timeline]);

  const maxTimeline = useMemo(() => {
    const values: number[] = [];
    mergedTimeline.forEach((item) => {
      if (item.citizens?.avg_seconds) values.push(item.citizens.avg_seconds);
      if (item.documents?.avg_seconds) values.push(item.documents.avg_seconds);
    });
    return values.length ? Math.max(...values) : 0;
  }, [mergedTimeline]);
  const subscriptions = useRef(new Map<string, { close: () => void }>());
  const logSubscriptions = useRef(new Map<string, { close: () => void }>());
  const notified = useRef(new Set<string>());

  const page = useMemo(() => Math.floor(offset / limit) + 1, [offset, limit]);

  const showToastMessage = (message: string, type: 'success' | 'error' = 'success', link?: string) => {
    showToast({ message, type, link });
  };

  const getAuthToken = () => (
    localStorage.getItem('token')
    || localStorage.getItem('access_token')
    || localStorage.getItem('admin_token')
  );

  const updateJobFromStatus = (status: ExportJobStatus) => {
    setItems((prev) => prev.map((job) => (
      job.job_id === status.job_id
        ? {
          ...job,
          status: status.status,
          result_filename: status.filename ?? job.result_filename,
          error: status.error ?? job.error,
          updated_at: new Date().toISOString(),
        }
        : job
    )));
    if ((status.status === 'done' || status.status === 'failed') && !notified.current.has(status.job_id)) {
      notified.current.add(status.job_id);
      if (status.status === 'done' && status.download_url) {
        showToastMessage('Exportação concluída.', 'success', `${apiRoot}${status.download_url}`);
      } else if (status.status === 'failed') {
        showToastMessage('Falha na exportação.', 'error');
      }
    }
  };

  const openSse = (jobId: string) => {
    if (!('EventSource' in window)) return null;
    const token = getAuthToken();
    if (!token) return null;
    const url = `${apiRoot}/api/admin/exports/jobs/${jobId}/stream?token=${encodeURIComponent(token)}`;
    return new EventSource(url);
  };

  const openWebSocket = (jobId: string) => {
    const token = getAuthToken();
    if (!token) return null;
    const url = `${wsRoot}/api/admin/exports/jobs/${jobId}/ws?token=${encodeURIComponent(token)}`;
    return new WebSocket(url);
  };

  const subscribeJob = (jobId: string) => {
    if (realtimeMode === 'ws') {
      const socket = openWebSocket(jobId);
      if (!socket) return { close: () => undefined };
      socket.onmessage = (event) => {
        if (!event.data) return;
        try {
          const status = JSON.parse(event.data) as ExportJobStatus;
          updateJobFromStatus(status);
          if (status.status === 'done' || status.status === 'failed') {
            socket.close();
          }
        } catch (err) {
          console.error('Erro ao ler WS de exportação:', err);
        }
      };
      socket.onerror = () => {
        socket.close();
      };
      return { close: () => socket.close() };
    }
    const stream = openSse(jobId);
    if (!stream) return { close: () => undefined };
    stream.onmessage = (event) => {
      if (!event.data) return;
      try {
        const status = JSON.parse(event.data) as ExportJobStatus;
        updateJobFromStatus(status);
        if (status.status === 'done' || status.status === 'failed') {
          stream.close();
        }
      } catch (err) {
        console.error('Erro ao ler SSE de exportação:', err);
      }
    };
    stream.onerror = () => {
      stream.close();
    };
    return { close: () => stream.close() };
  };

  const loadJobs = async (resetOffset = false) => {
    setLoading(true);
    setError(null);
    const effectiveOffset = resetOffset ? 0 : offset;
    try {
      const response = await exportJobsService.list({
        module: moduleFilter || undefined,
        status: statusFilter || undefined,
        q: search.trim() || undefined,
        job_id: jobIdFilter.trim() || undefined,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
        limit,
        offset: effectiveOffset,
      });
      setItems(response.items || []);
      setTotal(response.total || 0);
      setOffset(response.offset ?? effectiveOffset);
    } catch (err) {
      console.error('Erro ao carregar exportações:', err);
      setError('Não foi possível carregar o histórico de exportações.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [limit]);

  useEffect(() => {
    loadJobs(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [moduleFilter, statusFilter, search, jobIdFilter, dateFrom, dateTo]);

  useEffect(() => {
    if (offset === 0 && items.length === 0 && !total) {
      return;
    }
    loadJobs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset]);

  useEffect(() => {
    const active = items.filter((job) => job.status === 'pending' || job.status === 'running');
    const activeIds = new Set(active.map((job) => job.job_id));
    subscriptions.current.forEach((subscription, jobId) => {
      if (!activeIds.has(jobId)) {
        subscription.close();
        subscriptions.current.delete(jobId);
      }
    });
    active.forEach((job) => {
      if (!subscriptions.current.has(job.job_id)) {
        subscriptions.current.set(job.job_id, subscribeJob(job.job_id));
      }
    });
    return () => {
      subscriptions.current.forEach((subscription) => subscription.close());
      subscriptions.current.clear();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [items, realtimeMode]);

  useEffect(() => {
    const interval = setInterval(() => {
      loadJobs();
    }, 30_000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [moduleFilter, statusFilter, search, jobIdFilter, dateFrom, dateTo, limit, offset]);

  useEffect(() => {
    const loadTimeline = async () => {
      try {
        if (timelineMode === 'compare') {
          const response = await exportJobsService.timelineCompare(timelineDays);
          setTimeline(response.series || { citizens: [], documents: [] });
        } else {
          const response = await exportJobsService.timeline({ module: timelineMode, days: timelineDays });
          setTimeline({
            citizens: timelineMode === 'citizens' ? response.items || [] : [],
            documents: timelineMode === 'documents' ? response.items || [] : [],
          });
        }
      } catch (err) {
        console.error('Erro ao carregar timeline de exportações:', err);
        setTimeline({ citizens: [], documents: [] });
      }
    };
    loadTimeline();
  }, [timelineMode, timelineDays]);

  const handleRepeat = async (jobId: string) => {
    try {
      const response = await exportJobsService.repeat(jobId);
      showToastMessage('Exportação repetida com sucesso.');
      setOffset(0);
      await loadJobs(true);
      if (response.job_id) {
        const status = await exportJobsService.get(response.job_id);
        updateJobFromStatus(status);
      }
    } catch (err) {
      console.error('Erro ao repetir exportação:', err);
      showToastMessage('Falha ao repetir exportação.', 'error');
    }
  };

  const handleSelectDetail = async (jobId: string) => {
    try {
      const response = await exportJobsService.detail(jobId);
      setDetail(response);
      setDetailLogs(response.logs || []);
      setLogLevelFilter('');
      setLogSearch('');
      setPreviewCount(null);
      setPreviewBreakdown(null);
      const payload = (response.payload as Record<string, any>) || {};
      const params = payload.params || {};
      const columnsValue = Array.isArray(payload.columns)
        ? payload.columns.join(', ')
        : (typeof payload.columns === 'string' ? payload.columns : '');
      setReprocessForm({
        format: payload.format || 'csv',
        columns: columnsValue || '',
        q: params.q || '',
        name: params.name || '',
        bi: params.bi || '',
        email: params.email || '',
        phone: params.phone || '',
        status: params.status || '',
        document_type: params.document_type || '',
        date_from: params.date_from || '',
        date_to: params.date_to || '',
      });
      setShowReprocessEditor(false);
    } catch (err) {
      console.error('Erro ao carregar detalhe do job:', err);
      showToastMessage('Falha ao carregar detalhe do job.', 'error');
    }
  };

  const handleReprocessCustom = async () => {
    if (!detail?.job?.job_id) return;
    try {
      const validation = validateReprocessForm();
      if (validation) {
        setFormError(validation);
        showToastMessage(validation, 'error');
        return;
      }
      const params: Record<string, string> = {};
      if (reprocessForm.q) params.q = reprocessForm.q;
      if (reprocessForm.name) params.name = reprocessForm.name;
      if (reprocessForm.bi) params.bi = reprocessForm.bi;
      if (reprocessForm.email) params.email = reprocessForm.email;
      if (reprocessForm.phone) params.phone = reprocessForm.phone;
      if (reprocessForm.status) params.status = reprocessForm.status;
      if (reprocessForm.document_type) params.document_type = reprocessForm.document_type;
      if (reprocessForm.date_from) params.date_from = reprocessForm.date_from;
      if (reprocessForm.date_to) params.date_to = reprocessForm.date_to;
      const payload: Record<string, unknown> = {
        params,
        format: reprocessForm.format || 'csv',
      };
      if (columns.length) {
        payload.columns = columns;
      }
      await exportJobsService.reprocess(detail.job.job_id, payload);
      showToastMessage('Reprocessamento iniciado.');
      setShowReprocessEditor(false);
      setFormError(null);
      await loadJobs(true);
    } catch (err) {
      console.error('Erro ao reprocessar com payload custom:', err);
      showToastMessage('Payload inválido ou erro no reprocessamento.', 'error');
    }
  };

  const handlePreview = async () => {
    if (!detail?.job?.job_id) return;
    try {
      const validation = validateReprocessForm();
      if (validation) {
        setFormError(validation);
        showToastMessage(validation, 'error');
        return;
      }
      setPreviewLoading(true);
      const columns = reprocessForm.columns
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean);
      const params: Record<string, string> = {};
      if (reprocessForm.q) params.q = reprocessForm.q;
      if (reprocessForm.name) params.name = reprocessForm.name;
      if (reprocessForm.bi) params.bi = reprocessForm.bi;
      if (reprocessForm.email) params.email = reprocessForm.email;
      if (reprocessForm.phone) params.phone = reprocessForm.phone;
      if (reprocessForm.status) params.status = reprocessForm.status;
      if (reprocessForm.document_type) params.document_type = reprocessForm.document_type;
      if (reprocessForm.date_from) params.date_from = reprocessForm.date_from;
      if (reprocessForm.date_to) params.date_to = reprocessForm.date_to;
      const response = await exportJobsService.previewDetail(moduleType || 'citizens', params);
      setPreviewCount(response.count ?? 0);
      setPreviewBreakdown(response.by_status || null);
    } catch (err) {
      console.error('Erro ao pré-visualizar exportação:', err);
      showToastMessage('Falha ao pré-visualizar exportação.', 'error');
    } finally {
      setPreviewLoading(false);
    }
  };

  const openLogStream = (jobId: string) => {
    const token = getAuthToken();
    if (!token) return null;
    const lastLog = detailLogs[detailLogs.length - 1] || detail?.logs?.[detail.logs.length - 1];
    const since = lastLog?.created_at ? `&since=${encodeURIComponent(lastLog.created_at)}` : '';
    if (realtimeMode === 'ws') {
      const url = `${wsRoot}/api/admin/exports/jobs/${jobId}/logs/ws?token=${encodeURIComponent(token)}${since}`;
      return new WebSocket(url);
    }
    if (!('EventSource' in window)) return null;
    const url = `${apiRoot}/api/admin/exports/jobs/${jobId}/logs/stream?token=${encodeURIComponent(token)}${since}`;
    return new EventSource(url);
  };

  useEffect(() => {
    if (!detail?.job?.job_id) return;
    const jobId = detail.job.job_id;
    const stream = openLogStream(jobId);
    if (!stream) return;
    if (stream instanceof WebSocket) {
      stream.onmessage = (event) => {
        if (!event.data) return;
        try {
          const payload = JSON.parse(event.data) as { level?: string; message?: string; created_at?: string | null; status?: string };
          if (payload.level && payload.message) {
            setDetailLogs((prev) => [...prev, { level: payload.level!, message: payload.message!, created_at: payload.created_at || null }]);
            setLogPulseAt(Date.now());
          }
        } catch (err) {
          console.error('Erro ao ler WS log:', err);
        }
      };
      return () => stream.close();
    }
    stream.onmessage = (event) => {
      if (!event.data) return;
      try {
        const payload = JSON.parse(event.data) as { level?: string; message?: string; created_at?: string | null; status?: string };
        if (payload.level && payload.message) {
          setDetailLogs((prev) => [...prev, { level: payload.level!, message: payload.message!, created_at: payload.created_at || null }]);
          setLogPulseAt(Date.now());
        }
      } catch (err) {
        console.error('Erro ao ler SSE log:', err);
      }
    };
    return () => stream.close();
  }, [detail?.job?.job_id, realtimeMode]);

  const openListLogStream = (jobId: string) => {
    const token = getAuthToken();
    if (!token) return null;
    if (realtimeMode === 'ws') {
      const url = `${wsRoot}/api/admin/exports/jobs/${jobId}/logs/ws?token=${encodeURIComponent(token)}`;
      return new WebSocket(url);
    }
    if (!('EventSource' in window)) return null;
    const url = `${apiRoot}/api/admin/exports/jobs/${jobId}/logs/stream?token=${encodeURIComponent(token)}`;
    return new EventSource(url);
  };

  useEffect(() => {
    const active = items.filter((job) => job.status === 'pending' || job.status === 'running');
    const activeIds = new Set(active.map((job) => job.job_id));
    logSubscriptions.current.forEach((subscription, jobId) => {
      if (!activeIds.has(jobId)) {
        subscription.close();
        logSubscriptions.current.delete(jobId);
      }
    });
    active.forEach((job) => {
      if (logSubscriptions.current.has(job.job_id)) return;
      const stream = openListLogStream(job.job_id);
      if (!stream) return;
      if (stream instanceof WebSocket) {
        stream.onmessage = (event) => {
          if (!event.data) return;
          try {
            const payload = JSON.parse(event.data) as { level?: string; message?: string; created_at?: string | null };
            if (payload.level && payload.message) {
              setLiveLogs((prev) => ({ ...prev, [job.job_id]: { level: payload.level!, message: payload.message!, created_at: payload.created_at || null } }));
              setLogPulseAt(Date.now());
            }
          } catch (err) {
            console.error('Erro ao ler WS log (lista):', err);
          }
        };
        logSubscriptions.current.set(job.job_id, { close: () => stream.close() });
      } else {
        stream.onmessage = (event) => {
          if (!event.data) return;
          try {
            const payload = JSON.parse(event.data) as { level?: string; message?: string; created_at?: string | null };
            if (payload.level && payload.message) {
              setLiveLogs((prev) => ({ ...prev, [job.job_id]: { level: payload.level!, message: payload.message!, created_at: payload.created_at || null } }));
              setLogPulseAt(Date.now());
            }
          } catch (err) {
            console.error('Erro ao ler SSE log (lista):', err);
          }
        };
        logSubscriptions.current.set(job.job_id, { close: () => stream.close() });
      }
    });
    return () => {
      logSubscriptions.current.forEach((subscription) => subscription.close());
      logSubscriptions.current.clear();
    };
  }, [items, realtimeMode]);

  const handleRefresh = () => {
    loadJobs(true);
  };

  const totalPages = Math.max(1, Math.ceil(total / limit));
  const currentPage = Math.min(totalPages, page);
  const pageWindow = 2;
  const startPage = Math.max(1, currentPage - pageWindow);
  const endPage = Math.min(totalPages, currentPage + pageWindow);
  const pageNumbers = Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);

  const filteredDetailLogs = detailLogs.filter((log) => {
    if (logLevelFilter && log.level?.toLowerCase() !== logLevelFilter.toLowerCase()) {
      return false;
    }
    if (logSearch) {
      const needle = logSearch.toLowerCase();
      const hay = `${log.level} ${log.message}`.toLowerCase();
      return hay.includes(needle);
    }
    return true;
  });
  const moduleType = detail?.module?.toLowerCase();
  const isDocumentsModule = moduleType === 'documents';

  const validateReprocessForm = () => {
    if (reprocessForm.date_from && reprocessForm.date_to) {
      const from = new Date(reprocessForm.date_from);
      const to = new Date(reprocessForm.date_to);
      if (!Number.isNaN(from.getTime()) && !Number.isNaN(to.getTime()) && from > to) {
        return 'O intervalo de datas é inválido (início maior que fim).';
      }
    }
    if (reprocessForm.columns) {
      const hasInvalid = reprocessForm.columns.split(',').some((col) => !col.trim());
      if (hasInvalid) {
        return 'Colunas devem ser separadas por vírgula sem campos vazios.';
      }
    }
    return null;
  };
  const canPrev = offset > 0;
  const canNext = offset + limit < total;

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Exportações</h2>
          <p className="text-sm text-gray-500">Histórico real da tabela `export_jobs`.</p>
        </div>

        <div className="flex flex-col gap-3 w-full lg:w-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Pesquisa (módulo, status, ficheiro, erro)"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              value={jobIdFilter}
              onChange={(e) => setJobIdFilter(e.target.value)}
              placeholder="Job ID"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <select
              value={moduleFilter}
              onChange={(e) => setModuleFilter(e.target.value)}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            >
              <option value="">Módulo (todos)</option>
              <option value="citizens">Cidadãos</option>
              <option value="documents">Documentos</option>
            </select>
            <div className="flex items-center gap-2">
              <input
                type="datetime-local"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
              />
              <input
                type="datetime-local"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
              />
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            >
              <option value="">Status (todos)</option>
              <option value="pending">Pendente</option>
              <option value="running">Processando</option>
              <option value="done">Concluído</option>
              <option value="failed">Falhou</option>
            </select>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleRefresh}
                className="rounded-xl border border-gray-200 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50"
              >
                Atualizar
              </button>
              <select
                value={realtimeMode}
                onChange={(e) => setRealtimeMode(e.target.value as 'sse' | 'ws')}
                className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
              >
                <option value="sse">Tempo real: SSE</option>
                <option value="ws">Tempo real: WebSocket</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-slate-900">Timeline de execução</h3>
            <span className="text-xs text-gray-400">Média diária</span>
          </div>
          <div className="flex items-center gap-2">
            <select
              value={timelineMode}
              onChange={(e) => setTimelineMode(e.target.value as 'compare' | 'citizens' | 'documents')}
              className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            >
              <option value="compare">Comparar módulos</option>
              <option value="citizens">Só Cidadãos</option>
              <option value="documents">Só Documentos</option>
            </select>
            <select
              value={timelineDays}
              onChange={(e) => setTimelineDays(Number(e.target.value))}
              className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            >
              {[7, 14, 30].map((value) => (
                <option key={value} value={value}>{value} dias</option>
              ))}
            </select>
          </div>
        </div>
        {mergedTimeline.length === 0 ? (
          <p className="text-sm text-gray-500">Sem dados suficientes para timeline.</p>
        ) : (
          <div className="grid grid-cols-7 gap-3">
            {mergedTimeline.map((item) => {
              const heightCitizens = maxTimeline && item.citizens?.avg_seconds
                ? Math.max(8, (item.citizens.avg_seconds / maxTimeline) * 80)
                : 8;
              const heightDocuments = maxTimeline && item.documents?.avg_seconds
                ? Math.max(8, (item.documents.avg_seconds / maxTimeline) * 80)
                : 8;
              const label = item.day ? new Date(item.day).toLocaleDateString('pt-PT', { day: '2-digit', month: '2-digit' }) : '—';
              const isToday = item.day
                ? new Date(item.day).toDateString() === new Date().toDateString()
                : false;
              const pulseActive = logPulseAt ? (Date.now() - logPulseAt < 5000) : false;
              return (
                <div key={item.day} className="flex flex-col items-center justify-end gap-2">
                  <div className="flex items-end gap-1">
                    {(timelineMode === 'compare' || timelineMode === 'citizens') && (
                      <div
                        className="w-3 rounded-full bg-gradient-to-t from-blue-600 to-blue-300"
                        style={{ height: heightCitizens }}
                        title={`Citizens: ${formatDuration(item.citizens?.avg_seconds)} • ${item.citizens?.total ?? 0} jobs`}
                      />
                    )}
                    {(timelineMode === 'compare' || timelineMode === 'documents') && (
                      <div
                        className="w-3 rounded-full bg-gradient-to-t from-emerald-600 to-emerald-300"
                        style={{ height: heightDocuments }}
                        title={`Documents: ${formatDuration(item.documents?.avg_seconds)} • ${item.documents?.total ?? 0} jobs`}
                      />
                    )}
                    {isToday && pulseActive && (
                      <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-gray-400">{label}</span>
                </div>
              );
            })}
          </div>
        )}
        <div className="mt-4 flex items-center gap-4 text-xs text-gray-500">
          {(timelineMode === 'compare' || timelineMode === 'citizens') && (
            <span className="inline-flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-500"></span>
              Cidadãos
            </span>
          )}
          {(timelineMode === 'compare' || timelineMode === 'documents') && (
            <span className="inline-flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
              Documentos
            </span>
          )}
        </div>
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-gray-500">
          <div className="rounded-xl border border-gray-100 p-3">
            <p className="uppercase text-[10px] text-gray-400 mb-1">Média semanal (Cidadãos)</p>
            <p className="text-sm font-semibold text-slate-900">
              {formatDuration(
                mergedTimeline.slice(-7).reduce((acc, item) => acc + (item.citizens?.avg_seconds || 0), 0)
                / Math.max(1, mergedTimeline.slice(-7).filter((item) => item.citizens?.avg_seconds).length)
              )}
            </p>
          </div>
          <div className="rounded-xl border border-gray-100 p-3">
            <p className="uppercase text-[10px] text-gray-400 mb-1">Média semanal (Documentos)</p>
            <p className="text-sm font-semibold text-slate-900">
              {formatDuration(
                mergedTimeline.slice(-7).reduce((acc, item) => acc + (item.documents?.avg_seconds || 0), 0)
                / Math.max(1, mergedTimeline.slice(-7).filter((item) => item.documents?.avg_seconds).length)
              )}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div className="text-sm text-gray-500">
            {loading ? 'A carregar...' : `Total: ${total} • Página ${currentPage} de ${totalPages}`}
          </div>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span>Por página</span>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="rounded-md border border-gray-200 bg-white px-2 py-1"
            >
              {[10, 20, 30, 50].map((value) => (
                <option key={value} value={value}>{value}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-xs uppercase text-gray-500">
              <tr>
                <th className="px-6 py-3 text-left">Módulo</th>
                <th className="px-6 py-3 text-left">Status</th>
                <th className="px-6 py-3 text-left">Criado em</th>
                <th className="px-6 py-3 text-left">Atualizado</th>
                <th className="px-6 py-3 text-left">Duração / ETA</th>
                <th className="px-6 py-3 text-left">Último log</th>
                <th className="px-6 py-3 text-left">Arquivo</th>
                <th className="px-6 py-3 text-left">Ações</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td colSpan={8} className="px-6 py-6 text-center text-gray-400">
                    A carregar exportações...
                  </td>
                </tr>
              )}
              {!loading && items.length === 0 && (
                <tr>
                  <td colSpan={8} className="px-6 py-6 text-center text-gray-400">
                    Nenhuma exportação encontrada.
                  </td>
                </tr>
              )}
              {!loading && items.map((job) => (
                <tr key={job.job_id} className="border-t border-gray-100">
                  <td className="px-6 py-4 font-semibold text-slate-900 capitalize">{job.module}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold ${statusStyles(job.status)}`}>
                      {job.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{formatDateTime(job.created_at)}</td>
                  <td className="px-6 py-4 text-gray-600">{formatDateTime(job.updated_at)}</td>
                  <td className="px-6 py-4 text-gray-600">
                    {job.status === 'done' || job.status === 'failed'
                      ? formatDuration(job.duration_seconds)
                      : (job.estimated_seconds ? `~${formatDuration(job.estimated_seconds)}` : '—')
                    }
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    {liveLogs[job.job_id]
                      ? `${liveLogs[job.job_id].level}: ${liveLogs[job.job_id].message}`
                      : '—'}
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    {job.result_filename || '—'}
                    {job.error && <div className="text-xs text-rose-500 mt-1">{job.error}</div>}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      {job.status === 'done' && (
                        <a
                          href={`${apiRoot}/api/admin/exports/jobs/${job.job_id}/download`}
                          className="text-xs font-semibold text-slate-900 underline"
                          target="_blank"
                          rel="noreferrer"
                        >
                          Download
                        </a>
                      )}
                      <button
                        type="button"
                        onClick={() => handleRepeat(job.job_id)}
                        className="text-xs font-semibold text-slate-900 underline"
                      >
                        Repetir
                      </button>
                      <button
                        type="button"
                        onClick={() => handleSelectDetail(job.job_id)}
                        className="text-xs font-semibold text-slate-900 underline"
                      >
                        Detalhe
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-100">
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span>Página {currentPage} de {totalPages}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              disabled={!canPrev}
              onClick={() => setOffset(0)}
              className="rounded-lg border border-gray-200 px-3 py-1 text-xs font-semibold disabled:opacity-40"
            >
              Primeira
            </button>
            <button
              disabled={!canPrev}
              onClick={() => setOffset(Math.max(0, offset - limit))}
              className="rounded-lg border border-gray-200 px-3 py-1 text-xs font-semibold disabled:opacity-40"
            >
              Anterior
            </button>
            {pageNumbers.map((pageNumber) => (
              <button
                key={pageNumber}
                onClick={() => setOffset((pageNumber - 1) * limit)}
                className={`rounded-lg border px-3 py-1 text-xs font-semibold ${
                  pageNumber === currentPage
                    ? 'border-slate-900 bg-slate-900 text-white'
                    : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {pageNumber}
              </button>
            ))}
            <button
              disabled={!canNext}
              onClick={() => setOffset(offset + limit)}
              className="rounded-lg border border-gray-200 px-3 py-1 text-xs font-semibold disabled:opacity-40"
            >
              Próxima
            </button>
            <button
              disabled={!canNext}
              onClick={() => setOffset((totalPages - 1) * limit)}
              className="rounded-lg border border-gray-200 px-3 py-1 text-xs font-semibold disabled:opacity-40"
            >
              Última
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Detalhe do job</h3>
        {!detail ? (
          <p className="text-sm text-gray-500">Selecione um job para ver payload e logs.</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 text-sm">
            <div className="space-y-3">
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Job</p>
                <p className="font-semibold text-slate-900">{detail.job?.job_id}</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  disabled={!detail.job?.job_id}
                  onClick={() => handleRepeat(detail.job?.job_id || '')}
                  className="rounded-xl border border-slate-900 px-4 py-2 text-xs font-semibold text-slate-900 hover:bg-slate-900 hover:text-white"
                >
                  Reprocessar
                </button>
                <button
                  type="button"
                  disabled={!detail.job?.job_id}
                  onClick={() => setShowReprocessEditor((prev) => !prev)}
                  className="rounded-xl border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-50"
                >
                  Reprocessar (custom)
                </button>
                {detail.job?.status === 'done' && detail.job?.download_url && (
                  <a
                    href={`${apiRoot}${detail.job.download_url}`}
                    className="text-xs font-semibold text-slate-900 underline"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Download
                  </a>
                )}
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Status</p>
                <p className="text-gray-700">{detail.status}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Criado</p>
                <p className="text-gray-700">{formatDateTime(detail.created_at)}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Atualizado</p>
                <p className="text-gray-700">{formatDateTime(detail.updated_at)}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Payload</p>
                <pre className="rounded-xl bg-slate-900 text-slate-100 p-4 text-xs overflow-auto">
                  {JSON.stringify(detail.payload, null, 2)}
                </pre>
              </div>
              {showReprocessEditor && (
                <div>
                  <p className="text-xs uppercase text-gray-400 mb-2">Reprocessar (custom)</p>
                  <p className="text-xs text-gray-500 mb-2">
                    Campos exibidos conforme o módulo ({isDocumentsModule ? 'Documentos' : 'Cidadãos'}).
                  </p>
                  {formError && (
                    <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 mb-2">
                      {formError}
                    </div>
                  )}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <input
                      value={reprocessForm.q}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, q: e.target.value }))}
                      placeholder="Busca geral"
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    <input
                      value={reprocessForm.columns}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, columns: e.target.value }))}
                      placeholder="Colunas (separadas por vírgula)"
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    <input
                      type="datetime-local"
                      value={reprocessForm.date_from}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, date_from: e.target.value }))}
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    <input
                      type="datetime-local"
                      value={reprocessForm.date_to}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, date_to: e.target.value }))}
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    {moduleType !== 'documents' && (
                      <>
                        <input
                          value={reprocessForm.name}
                          onChange={(e) => setReprocessForm((prev) => ({ ...prev, name: e.target.value }))}
                          placeholder="Nome"
                          className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                        />
                        <input
                          value={reprocessForm.phone}
                          onChange={(e) => setReprocessForm((prev) => ({ ...prev, phone: e.target.value }))}
                          placeholder="Telefone"
                          className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                        />
                      </>
                    )}
                    <input
                      value={reprocessForm.bi}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, bi: e.target.value }))}
                      placeholder="BI"
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    <input
                      value={reprocessForm.email}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, email: e.target.value }))}
                      placeholder="Email"
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    />
                    {moduleType === 'documents' && (
                      <input
                        value={reprocessForm.document_type}
                        onChange={(e) => setReprocessForm((prev) => ({ ...prev, document_type: e.target.value }))}
                        placeholder="Tipo de documento"
                        className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                      />
                    )}
                    <select
                      value={reprocessForm.status}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, status: e.target.value }))}
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    >
                      <option value="">Estado (todos)</option>
                      {isDocumentsModule ? (
                        <>
                          <option value="active">Válido</option>
                          <option value="expired">Expirado</option>
                          <option value="unknown">Indefinido</option>
                        </>
                      ) : (
                        <>
                          <option value="active">Ativo</option>
                          <option value="inactive">Inativo</option>
                        </>
                      )}
                    </select>
                    <select
                      value={reprocessForm.format}
                      onChange={(e) => setReprocessForm((prev) => ({ ...prev, format: e.target.value }))}
                      className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                    >
                      <option value="csv">CSV</option>
                      <option value="xlsx">Excel (.xlsx)</option>
                    </select>
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <button
                      type="button"
                      onClick={handlePreview}
                      disabled={previewLoading}
                      className="rounded-xl border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-50 disabled:opacity-60"
                    >
                      {previewLoading ? 'A calcular...' : 'Pré-visualizar'}
                    </button>
                    <button
                      type="button"
                      onClick={handleReprocessCustom}
                      className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-slate-800"
                    >
                      Executar reprocessamento
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowReprocessEditor(false)}
                      className="rounded-xl border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-50"
                    >
                      Cancelar
                    </button>
                  </div>
                  {previewCount !== null && (
                    <div className="mt-2 text-xs text-gray-500 space-y-1">
                      <p>
                        Estimativa: <span className="font-semibold text-slate-900">{previewCount}</span> registos.
                      </p>
                      {previewBreakdown && (
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(previewBreakdown).map(([key, value]) => (
                            <span key={key} className="rounded-full bg-gray-100 px-2 py-0.5 text-[11px] text-gray-600">
                              {key}: <span className="font-semibold text-slate-900">{value}</span>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
            <div>
              <p className="text-xs uppercase text-gray-400 mb-2">Logs</p>
              <div className="flex flex-wrap gap-2 mb-3">
                <select
                  value={logLevelFilter}
                  onChange={(e) => setLogLevelFilter(e.target.value)}
                  className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                >
                  <option value="">Nível (todos)</option>
                  <option value="info">Info</option>
                  <option value="warning">Warning</option>
                  <option value="error">Error</option>
                </select>
                <input
                  value={logSearch}
                  onChange={(e) => setLogSearch(e.target.value)}
                  placeholder="Filtrar logs"
                  className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-xs shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
                />
              </div>
              <div className="space-y-2">
                {filteredDetailLogs.length > 0 ? filteredDetailLogs.map((log, idx) => (
                  <div key={`${log.created_at}-${idx}`} className="rounded-xl border border-gray-100 p-3">
                    <div className="flex items-center justify-between text-xs text-gray-400">
                      <span className="uppercase">{log.level}</span>
                      <span>{formatDateTime(log.created_at)}</span>
                    </div>
                    <p className="text-sm text-gray-700 mt-1">{log.message}</p>
                  </div>
                )) : (
                  <p className="text-sm text-gray-500">Sem logs para este job.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

    </div>
  );
};

export default AdminExports;
