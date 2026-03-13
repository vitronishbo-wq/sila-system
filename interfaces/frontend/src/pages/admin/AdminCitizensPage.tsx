import React, { useCallback, useEffect, useMemo, useState } from 'react';
import http from '../../api/http';

type Citizen = {
  citizen_id: string;
  document_number?: string | null;
  full_name: string;
  birth_date?: string | null;
  gender?: string | null;
  phone?: string | null;
  email?: string | null;
};

const PAGE_SIZE = 20;

const AdminCitizensPage: React.FC = () => {
  const [items, setItems] = useState<Citizen[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [skip, setSkip] = useState(0);

  const fetchCitizens = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      if (search.trim().length >= 2) {
        const response = await http.get<Citizen[]>('v1/identidade-civil/citizens/search', {
          params: { q: search.trim() },
        });
        setItems(response.data);
      } else {
        const response = await http.get<Citizen[]>('v1/identidade-civil/citizens', {
          params: { skip, limit: PAGE_SIZE },
        });
        setItems(response.data);
      }
    } catch (err: any) {
      setItems([]);
      setError(err?.response?.data?.detail || 'Falha ao carregar cidadãos.');
    } finally {
      setLoading(false);
    }
  }, [search, skip]);

  useEffect(() => {
    fetchCitizens();
  }, [fetchCitizens]);

  const isSearching = search.trim().length >= 2;
  const canGoBack = !isSearching && skip > 0;
  const canGoNext = !isSearching && items.length === PAGE_SIZE;

  const subtitle = useMemo(() => {
    if (isSearching) {
      return `Resultado para "${search.trim()}"`;
    }
    return `Registos locais (offset: ${skip})`;
  }, [isSearching, search, skip]);

  return (
    <section className="space-y-6">
      <header className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Cidadãos</h1>
          <p className="text-sm text-slate-500">{subtitle}</p>
        </div>
        <div className="w-full md:w-96">
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setSkip(0);
            }}
            placeholder="Pesquisar por nome (mín. 2 letras)"
            className="h-11 w-full rounded-xl border border-slate-300 bg-white px-4 text-sm text-slate-900 shadow-sm focus:border-slate-500 focus:outline-none"
          />
        </div>
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
              <th className="px-4 py-3">Nome</th>
              <th className="px-4 py-3">Documento</th>
              <th className="px-4 py-3">Contacto</th>
              <th className="px-4 py-3">Nascimento</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td className="px-4 py-8 text-sm text-slate-500" colSpan={4}>
                  A carregar cidadãos...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td className="px-4 py-8 text-sm text-slate-500" colSpan={4}>
                  Nenhum cidadão encontrado.
                </td>
              </tr>
            ) : (
              items.map((citizen) => (
                <tr key={citizen.citizen_id} className="text-sm text-slate-700">
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-900">{citizen.full_name}</div>
                    <div className="text-xs text-slate-500">{citizen.citizen_id}</div>
                  </td>
                  <td className="px-4 py-3">{citizen.document_number || '-'}</td>
                  <td className="px-4 py-3">
                    <div>{citizen.email || '-'}</div>
                    <div className="text-xs text-slate-500">{citizen.phone || '-'}</div>
                  </td>
                  <td className="px-4 py-3">{citizen.birth_date || '-'}</td>
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

export default AdminCitizensPage;
