import React, { useEffect, useMemo, useState } from 'react';
import { API_URL } from '@/constants';
import { adminDocumentService } from '@/modules/admin/services/adminDocumentService';
import type { AdminDocumentSummary, ExportJobStatus } from '@/modules/admin/services/adminDocumentService';
import { useToast } from '@/hooks/useToast';

const formatDate = (value?: string | null) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('pt-PT');
};

const statusBadge = (status?: string | null) => {
  const normalized = (status || '').toUpperCase();
  if (normalized === 'ACTIVE') return 'bg-emerald-50 text-emerald-700';
  if (normalized === 'EXPIRED') return 'bg-rose-50 text-rose-600';
  return 'bg-gray-100 text-gray-600';
};

const statusLabel = (status?: string | null) => {
  const normalized = (status || '').toUpperCase();
  if (normalized === 'ACTIVE') return 'Válido';
  if (normalized === 'EXPIRED') return 'Expirado';
  return 'Indefinido';
};

const AdminDocuments: React.FC = () => {
  const [query, setQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [biFilter, setBiFilter] = useState('');
  const [emailFilter, setEmailFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [exportFormat, setExportFormat] = useState<'csv' | 'xlsx'>('csv');
  const [csvColumns, setCsvColumns] = useState<string[]>([
    'document_type',
    'citizen_name',
    'citizen_bi',
    'issued_at',
    'valid_until',
    'status',
    'file_url',
  ]);
  const [csvPresets, setCsvPresets] = useState<{ name: string; columns: string[] }[]>([]);
  const [exporting, setExporting] = useState(false);
  const { showToast } = useToast();
  const [items, setItems] = useState<AdminDocumentSummary[]>([]);
  const [selected, setSelected] = useState<AdminDocumentSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [limit, setLimit] = useState(12);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);

  const page = useMemo(() => Math.floor(offset / limit) + 1, [offset, limit]);
  const apiRoot = useMemo(() => API_URL.replace(/\/api\/?$/, ''), []);

  const getAuthToken = () => (
    localStorage.getItem('token')
    || localStorage.getItem('access_token')
    || localStorage.getItem('admin_token')
  );

  const openJobStream = (jobId: string) => {
    if (!('EventSource' in window)) return null;
    const token = getAuthToken();
    if (!token) return null;
    const url = `${apiRoot}/api/admin/exports/jobs/${jobId}/stream?token=${encodeURIComponent(token)}`;
    return new EventSource(url);
  };

  const loadDocuments = async (resetOffset = false) => {
    setLoading(true);
    setError(null);
    const effectiveOffset = resetOffset ? 0 : offset;
    try {
      const response = await adminDocumentService.list({
        q: query.trim(),
        document_type: typeFilter.trim(),
        bi: biFilter.trim(),
        email: emailFilter.trim(),
        status: statusFilter,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
        limit,
        offset: effectiveOffset,
      });
      setItems(response.items || []);
      setTotal(response.total || 0);
      setOffset(response.offset ?? effectiveOffset);
      if (response.items?.length) {
        setSelected(response.items[0]);
      } else {
        setSelected(null);
      }
    } catch (err) {
      console.error('Erro ao carregar documentos:', err);
      setError('Não foi possível carregar a lista de documentos.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [limit]);

  useEffect(() => {
    const loadPresets = async () => {
      try {
        const response = await adminDocumentService.listPresets();
        setCsvPresets(response.presets || []);
      } catch (err) {
        console.error('Erro ao carregar presets:', err);
      }
    };
    loadPresets();
  }, []);

  useEffect(() => {
    if (offset === 0 && items.length === 0 && !total) {
      return;
    }
    loadDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset]);

  const handleSearch = (event?: React.FormEvent) => {
    if (event) event.preventDefault();
    loadDocuments(true);
  };

  const handleClearFilters = () => {
    setQuery('');
    setTypeFilter('');
    setBiFilter('');
    setEmailFilter('');
    setStatusFilter('');
    setDateFrom('');
    setDateTo('');
    setOffset(0);
    loadDocuments(true);
  };

  const showToastMessage = (message: string, type: 'success' | 'error' = 'success', link?: string) => {
    showToast({ message, type, link });
  };

  const handleSavePreset = async () => {
    const name = window.prompt('Nome do preset:');
    if (!name) return;
    try {
      const response = await adminDocumentService.savePreset(name, csvColumns);
      setCsvPresets(response.presets || []);
      showToastMessage('Preset guardado.');
    } catch (err) {
      console.error('Erro ao guardar preset:', err);
      showToastMessage('Falha ao guardar preset.', 'error');
    }
  };

  const handleRemovePreset = async (name: string) => {
    try {
      const response = await adminDocumentService.deletePreset(name);
      setCsvPresets(response.presets || []);
      showToastMessage('Preset removido.');
    } catch (err) {
      console.error('Erro ao remover preset:', err);
      showToastMessage('Falha ao remover preset.', 'error');
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      showToastMessage('Exportação iniciada...');
      const job = await adminDocumentService.startExportJob({
        q: query.trim(),
        document_type: typeFilter.trim(),
        bi: biFilter.trim(),
        email: emailFilter.trim(),
        status: statusFilter,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
        columns: csvColumns,
        format: exportFormat,
      });
      const poll = async (attempt = 0) => {
        if (attempt > 60) {
          setExporting(false);
          showToastMessage('Exportação ainda em processamento.', 'success');
          return;
        }
        let status: ExportJobStatus;
        try {
          status = await adminDocumentService.getExportJob(job.job_id);
        } catch (err) {
          console.error('Erro ao consultar exportação:', err);
          setExporting(false);
          showToastMessage('Falha na exportação.', 'error');
          return;
        }
        if (status.status === 'done' && status.download_url) {
          setExporting(false);
          showToastMessage('Exportação concluída.', 'success', `${apiRoot}${status.download_url}`);
          return;
        }
        if (status.status === 'failed') {
          setExporting(false);
          showToastMessage('Falha na exportação.', 'error');
          return;
        }
        setTimeout(() => poll(attempt + 1), 1000);
      };
      const stream = openJobStream(job.job_id);
      if (stream) {
        stream.onmessage = (event) => {
          if (!event.data) return;
          try {
            const status = JSON.parse(event.data) as ExportJobStatus;
            if (status.status === 'done' && status.download_url) {
              setExporting(false);
              showToastMessage('Exportação concluída.', 'success', `${apiRoot}${status.download_url}`);
              stream.close();
            } else if (status.status === 'failed') {
              setExporting(false);
              showToastMessage('Falha na exportação.', 'error');
              stream.close();
            }
          } catch (err) {
            console.error('Erro ao ler SSE de exportação:', err);
          }
        };
        stream.onerror = () => {
          stream.close();
          poll();
        };
      } else {
        poll();
      }
    } catch (err) {
      console.error('Erro ao exportar CSV:', err);
      showToastMessage('Falha na exportação.', 'error');
      setExporting(false);
    }
  };

  const toggleCsvColumn = (column: string) => {
    setCsvColumns((prev) => (
      prev.includes(column)
        ? prev.filter((item) => item !== column)
        : [...prev, column]
    ));
  };

  const handleSelect = async (document: AdminDocumentSummary) => {
    setSelected(document);
    try {
      const detail = await adminDocumentService.getById(document.id);
      setSelected(detail);
    } catch (err) {
      console.error('Erro ao carregar detalhes:', err);
    }
  };

  const canPrev = offset > 0;
  const canNext = offset + limit < total;
  const totalPages = Math.max(1, Math.ceil(total / limit));
  const currentPage = Math.min(totalPages, page);
  const pageWindow = 2;
  const startPage = Math.max(1, currentPage - pageWindow);
  const endPage = Math.min(totalPages, currentPage + pageWindow);
  const pageNumbers = Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Documentos</h2>
          <p className="text-sm text-gray-500">Lista baseada em `wallet_documents`.</p>
        </div>

        <form onSubmit={handleSearch} className="flex flex-col gap-3 w-full lg:w-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Busca geral (tipo, nome, BI, email)"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              placeholder="Tipo de documento"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              value={biFilter}
              onChange={(e) => setBiFilter(e.target.value)}
              placeholder="BI"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              value={emailFilter}
              onChange={(e) => setEmailFilter(e.target.value)}
              placeholder="Email"
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              type="datetime-local"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <input
              type="datetime-local"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
            >
              <option value="">Estado (todos)</option>
              <option value="active">Válido</option>
              <option value="expired">Expirado</option>
              <option value="unknown">Indefinido</option>
            </select>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="submit"
              className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-slate-800"
            >
              Pesquisar
            </button>
            <button
              type="button"
              onClick={handleClearFilters}
              className="rounded-xl border border-gray-200 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-50"
            >
              Limpar filtros
            </button>
            <div className="flex items-center gap-2">
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value as 'csv' | 'xlsx')}
                className="rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
              >
                <option value="csv">CSV</option>
                <option value="xlsx">Excel (.xlsx)</option>
              </select>
              <button
                type="button"
                onClick={handleExport}
                disabled={exporting}
                className="rounded-xl border border-slate-900 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-slate-900 hover:text-white disabled:opacity-60"
              >
                {exporting ? 'Exportando...' : 'Exportar'}
              </button>
            </div>
          </div>
          <div className="flex flex-wrap gap-3 text-xs text-gray-500">
            <span className="uppercase tracking-wide text-gray-400">Colunas CSV:</span>
            {[
              { label: 'Tipo', value: 'document_type' },
              { label: 'Cidadão', value: 'citizen_name' },
              { label: 'BI', value: 'citizen_bi' },
              { label: 'Email', value: 'citizen_email' },
              { label: 'Emissão', value: 'issued_at' },
              { label: 'Validade', value: 'valid_until' },
              { label: 'Estado', value: 'status' },
              { label: 'Ficheiro', value: 'file_url' },
            ].map((col) => (
              <label key={col.value} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={csvColumns.includes(col.value)}
                  onChange={() => toggleCsvColumn(col.value)}
                  className="accent-slate-900"
                />
                {col.label}
              </label>
            ))}
            <div className="flex items-center gap-2 text-xs text-gray-400">
              <button
                type="button"
                onClick={() => setCsvColumns(['document_type', 'citizen_name', 'citizen_bi', 'issued_at', 'status'])}
                className="underline"
              >
                Preset: Resumo
              </button>
              <button
                type="button"
                onClick={() => setCsvColumns(['id', 'document_type', 'citizen_name', 'citizen_bi', 'citizen_email', 'issued_at', 'valid_until', 'status', 'file_url', 'citizen_id'])}
                className="underline"
              >
                Preset: Completo
              </button>
              <button
                type="button"
                onClick={handleSavePreset}
                className="underline"
              >
                Salvar preset
              </button>
              {csvPresets.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {csvPresets.map((preset) => (
                    <span key={preset.name} className="inline-flex items-center gap-2 rounded-full border border-gray-200 px-2 py-1 text-[11px]">
                      <button type="button" onClick={() => setCsvColumns(preset.columns)} className="underline">
                        {preset.name}
                      </button>
                      <button type="button" onClick={() => handleRemovePreset(preset.name)} className="text-gray-400">
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </form>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-[2.2fr_1fr] gap-6">
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
                {[10, 12, 20, 30].map((value) => (
                  <option key={value} value={value}>{value}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-xs uppercase text-gray-500">
                <tr>
                  <th className="px-6 py-3 text-left">Tipo</th>
                  <th className="px-6 py-3 text-left">Cidadão</th>
                  <th className="px-6 py-3 text-left">BI</th>
                  <th className="px-6 py-3 text-left">Emissão</th>
                  <th className="px-6 py-3 text-left">Estado</th>
                  <th className="px-6 py-3 text-left">Ações</th>
                </tr>
              </thead>
              <tbody>
                {loading && (
                  <tr>
                    <td colSpan={6} className="px-6 py-6 text-center text-gray-400">
                      A carregar documentos...
                    </td>
                  </tr>
                )}
                {!loading && items.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-6 py-6 text-center text-gray-400">
                      Nenhum documento encontrado.
                    </td>
                  </tr>
                )}
                {!loading && items.map((doc) => (
                  <tr
                    key={doc.id}
                    className={`border-t border-gray-100 hover:bg-slate-50 cursor-pointer ${selected?.id === doc.id ? 'bg-slate-50' : ''}`}
                    onClick={() => handleSelect(doc)}
                  >
                    <td className="px-6 py-4 font-semibold text-slate-900">{doc.document_type}</td>
                    <td className="px-6 py-4 text-gray-600">{doc.citizen_name || '—'}</td>
                    <td className="px-6 py-4 text-gray-600">{doc.citizen_bi || '—'}</td>
                    <td className="px-6 py-4 text-gray-600">{formatDate(doc.issued_at)}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold ${statusBadge(doc.status)}`}>
                        {statusLabel(doc.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {doc.file_url ? (
                        <a
                          href={doc.file_url}
                          target="_blank"
                          rel="noreferrer"
                          onClick={(event) => event.stopPropagation()}
                          className="text-xs font-semibold text-slate-900 underline"
                        >
                          Abrir documento
                        </a>
                      ) : (
                        <span className="text-xs text-gray-400">Indisponível</span>
                      )}
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
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Detalhe do documento</h3>
          {!selected ? (
            <p className="text-sm text-gray-500">Selecione um documento para ver o detalhe.</p>
          ) : (
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Tipo</p>
                <p className="font-semibold text-slate-900">{selected.document_type}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Cidadão</p>
                <p className="text-gray-700">{selected.citizen_name || '—'}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">BI</p>
                <p className="text-gray-700">{selected.citizen_bi || '—'}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Email</p>
                <p className="text-gray-700">{selected.citizen_email || '—'}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Emissão</p>
                <p className="text-gray-700">{formatDate(selected.issued_at)}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Validade</p>
                <p className="text-gray-700">{formatDate(selected.valid_until)}</p>
              </div>
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Estado</p>
                <p className="text-gray-700">{statusLabel(selected.status)}</p>
              </div>
              <div className="pt-4">
                <a
                  href={`#/admin/documents/${selected.id}`}
                  className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-slate-800"
                >
                  Abrir detalhe completo
                  <span>→</span>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>

    </div>
  );
};

export default AdminDocuments;
