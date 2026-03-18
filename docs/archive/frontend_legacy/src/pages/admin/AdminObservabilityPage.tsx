import React, { useEffect, useState } from 'react';
import http from '../../api/http';

type KpiResponse = {
  kpis: {
    users: number;
    territories: number;
    services: number;
    requests: number;
  };
  meta: {
    scope: string;
    target_id?: string | null;
    health?: string;
  };
};

type SlaResponse = {
  avg_issuance_time_seconds?: number;
  min_issuance_time_seconds?: number;
  max_issuance_time_seconds?: number;
  total_processed?: number;
  period_days?: number;
  sla_status?: string;
  sla_target_seconds?: number;
};

const AdminObservabilityPage: React.FC = () => {
  const [kpis, setKpis] = useState<KpiResponse | null>(null);
  const [sla, setSla] = useState<SlaResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [kpiRes, slaRes] = await Promise.all([
          http.get<KpiResponse>('admin/observability/kpis'),
          http.get<SlaResponse>('admin/audit/sla/metrics', { params: { days: 7 } }),
        ]);

        if (!mounted) return;
        setKpis(kpiRes.data);
        setSla(slaRes.data);
      } catch (err: any) {
        if (!mounted) return;
        setError(err?.response?.data?.detail || 'Falha ao carregar métricas de observabilidade.');
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return <div className="text-sm text-slate-500">A carregar métricas...</div>;
  }

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Observabilidade</h1>
        <p className="text-sm text-slate-500">KPIs operacionais e métricas de SLA/SLO.</p>
      </header>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {!error && (
        <>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Utilizadores" value={kpis?.kpis.users ?? 0} />
            <MetricCard label="Territórios" value={kpis?.kpis.territories ?? 0} />
            <MetricCard label="Serviços" value={kpis?.kpis.services ?? 0} />
            <MetricCard label="Pedidos" value={kpis?.kpis.requests ?? 0} />
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Contexto</h2>
              <dl className="mt-3 space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-slate-500">Escopo</dt>
                  <dd className="font-medium text-slate-900">{kpis?.meta.scope || '-'}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Território alvo</dt>
                  <dd className="font-mono text-xs text-slate-700">{kpis?.meta.target_id || '-'}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Saúde</dt>
                  <dd className="font-medium text-slate-900">{kpis?.meta.health || '-'}</dd>
                </div>
              </dl>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">SLA (7 dias)</h2>
              <dl className="mt-3 space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-slate-500">Tempo médio</dt>
                  <dd className="font-medium text-slate-900">{formatSeconds(sla?.avg_issuance_time_seconds)}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Mín / Máx</dt>
                  <dd className="font-medium text-slate-900">
                    {formatSeconds(sla?.min_issuance_time_seconds)} / {formatSeconds(sla?.max_issuance_time_seconds)}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Meta</dt>
                  <dd className="font-medium text-slate-900">{formatSeconds(sla?.sla_target_seconds)}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Estado</dt>
                  <dd className="font-medium text-slate-900">{sla?.sla_status || '-'}</dd>
                </div>
              </dl>
            </div>
          </div>
        </>
      )}
    </section>
  );
};

const MetricCard: React.FC<{ label: string; value: number }> = ({ label, value }) => (
  <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
    <div className="text-xs uppercase tracking-wide text-slate-500">{label}</div>
    <div className="mt-1 text-2xl font-bold text-slate-900">{value}</div>
  </div>
);

const formatSeconds = (value?: number) => {
  if (typeof value !== 'number' || Number.isNaN(value)) return '-';
  if (value < 60) return `${Math.round(value)}s`;
  const mins = Math.floor(value / 60);
  const secs = Math.round(value % 60);
  return `${mins}m ${secs}s`;
};

export default AdminObservabilityPage;
