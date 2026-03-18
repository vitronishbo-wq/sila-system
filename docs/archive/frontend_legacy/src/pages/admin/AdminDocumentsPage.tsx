import React, { useCallback, useEffect, useState } from 'react';
import http from '../../api/http';

type DocumentItem = {
  id: string;
  citizen_id: string;
  document_type: string;
  status: string;
  created_at: string;
  updated_at?: string | null;
};

const PAGE_SIZE = 20;

const AdminDocumentsPage: React.FC = () => {
  const [items, setItems] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [skip, setSkip] = useState(0);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await http.get<DocumentItem[]>('v1/identidade-civil/documents', {
        params: { skip, limit: PAGE_SIZE },
      });
      setItems(response.data);
    } catch (err: any) {
      setItems([]);
      setError(err?.response?.data?.detail || 'Falha ao carregar documentos.');
    } finally {
      setLoading(false);
    }
  }, [skip]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const canGoBack = skip > 0;
  const canGoNext = items.length === PAGE_SIZE;

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Documentos</h1>
        <p className="text-sm text-slate-500">Solicitações de emissão e atualização de documentos.</p>
      </header>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr className="text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Cidadão</th>
              <th className="px-4 py-3">Tipo</th>
              <th className="px-4 py-3">Estado</th>
              <th className="px-4 py-3">Criado em</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td className="px-4 py-8 text-sm text-slate-500" colSpan={5}>
                  A carregar documentos...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td className="px-4 py-8 text-sm text-slate-500" colSpan={5}>
                  Nenhum documento encontrado.
                </td>
              </tr>
            ) : (
              items.map((doc) => (
                <tr key={doc.id} className="text-sm text-slate-700">
                  <td className="px-4 py-3 font-mono text-xs">{doc.id}</td>
                  <td className="px-4 py-3 font-mono text-xs">{doc.citizen_id}</td>
                  <td className="px-4 py-3">{doc.document_type}</td>
                  <td className="px-4 py-3">
                    <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold uppercase text-slate-700">
                      {doc.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">{doc.created_at || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <footer className="flex items-center justify-end gap-3">
        <button
          type="button"
          disabled={!canGoBack}
          onClick={() => setSkip((prev) => Math.max(0, prev - PAGE_SIZE))}
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Anterior
        </button>
        <button
          type="button"
          disabled={!canGoNext}
          onClick={() => setSkip((prev) => prev + PAGE_SIZE)}
          className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:cursor-not-allowed disabled:opacity-40"
        >
          Próxima
        </button>
      </footer>
    </section>
  );
};

export default AdminDocumentsPage;
