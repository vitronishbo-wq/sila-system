import React, { useEffect, useMemo, useState } from 'react';
import http from '../../api/http';

type TerritoryNode = {
  id: string;
  name: string;
  code: string;
  type: string;
  parent_id?: string | null;
  children?: TerritoryNode[];
};

const countChildren = (nodes: TerritoryNode[]): number =>
  nodes.reduce((acc, node) => acc + (node.children?.length || 0), 0);

const countGrandChildren = (nodes: TerritoryNode[]): number =>
  nodes.reduce((acc, node) => {
    const municipalities = node.children || [];
    return acc + municipalities.reduce((inner, m) => inner + (m.children?.length || 0), 0);
  }, 0);

const AdminTerritoryPage: React.FC = () => {
  const [tree, setTree] = useState<TerritoryNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  useEffect(() => {
    let mounted = true;
    http
      .get<TerritoryNode[]>('admin/territory/tree')
      .then((response) => {
        if (mounted) {
          setTree(response.data);
          const initial: Record<string, boolean> = {};
          response.data.forEach((node) => {
            initial[node.id] = false;
          });
          setExpanded(initial);
        }
      })
      .catch((err: any) => {
        if (mounted) {
          setError(err?.response?.data?.detail || 'Falha ao carregar árvore territorial.');
        }
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  const totals = useMemo(
    () => ({
      provinces: tree.length,
      municipalities: countChildren(tree),
      communes: countGrandChildren(tree),
    }),
    [tree]
  );

  if (loading) {
    return <div className="text-sm text-slate-500">A carregar hierarquia territorial...</div>;
  }

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Territórios</h1>
        <p className="text-sm text-slate-500">Navegação da hierarquia: províncias, municípios e comunas.</p>
      </header>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {!error && (
        <>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-xs uppercase tracking-wide text-slate-500">Províncias</div>
              <div className="mt-1 text-2xl font-bold text-slate-900">{totals.provinces}</div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-xs uppercase tracking-wide text-slate-500">Municípios</div>
              <div className="mt-1 text-2xl font-bold text-slate-900">{totals.municipalities}</div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="text-xs uppercase tracking-wide text-slate-500">Comunas</div>
              <div className="mt-1 text-2xl font-bold text-slate-900">{totals.communes}</div>
            </div>
          </div>

          <div className="space-y-3">
            {tree.map((province) => {
              const show = expanded[province.id];
              const municipalities = province.children || [];
              return (
                <article key={province.id} className="rounded-xl border border-slate-200 bg-white shadow-sm">
                  <button
                    type="button"
                    onClick={() => setExpanded((prev) => ({ ...prev, [province.id]: !prev[province.id] }))}
                    className="flex w-full items-center justify-between px-4 py-3 text-left"
                  >
                    <div>
                      <div className="font-semibold text-slate-900">{province.name}</div>
                      <div className="text-xs text-slate-500">
                        {province.code} • {municipalities.length} municípios
                      </div>
                    </div>
                    <span className="text-xs font-semibold uppercase text-slate-500">{show ? 'ocultar' : 'ver'}</span>
                  </button>

                  {show && (
                    <div className="border-t border-slate-100 px-4 py-3">
                      {municipalities.length === 0 ? (
                        <p className="text-sm text-slate-500">Sem municípios associados.</p>
                      ) : (
                        <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
                          {municipalities.map((municipality) => (
                            <div key={municipality.id} className="rounded-lg border border-slate-100 bg-slate-50 p-3">
                              <div className="font-medium text-slate-900">{municipality.name}</div>
                              <div className="text-xs text-slate-500">
                                {municipality.code} • {(municipality.children || []).length} comunas
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        </>
      )}
    </section>
  );
};

export default AdminTerritoryPage;
