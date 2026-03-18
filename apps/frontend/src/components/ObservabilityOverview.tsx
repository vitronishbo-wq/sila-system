import React, { useEffect, useState } from 'react';
import http from '../api/http';

type KpiResponse = {
  kpis: {
    users: number;
    territories: number;
    services: number;
    requests: number;
    errors_24h?: number;
    traces?: number;
    otel_metrics?: number;
  };
  meta: {
    scope: string;
    target_id?: string | null;
    health?: string;
  };
  telemetry?: {
    otel_available?: boolean;
    otel_tracing?: boolean;
    otel_metrics?: boolean;
    in_memory_requests?: number;
    in_memory_errors?: number;
    audit_errors_24h?: number;
  };
};

type SlaResponse = {
  avg_issuance_time_seconds?: number | null;
  min_issuance_time_seconds?: number | null;
  max_issuance_time_seconds?: number | null;
  total_processed?: number;
  period_days?: number;
  sla_status?: string | null;
  sla_target_seconds?: number;
};

type SlaBreakdownItem = {
  service_type?: string | null;
  sla_code?: string | null;
  sla_description?: string | null;
  sla_target_seconds?: number | null;
  avg_issuance_time_seconds?: number | null;
  min_issuance_time_seconds?: number | null;
  max_issuance_time_seconds?: number | null;
  total_processed?: number;
  sla_status?: string | null;
};

type SlaBreakdownResponse = {
  items: SlaBreakdownItem[];
  meta?: {
    period_days?: number;
  };
};

const ObservabilityOverview: React.FC = () => {
  const [kpis, setKpis] = useState<KpiResponse | null>(null);
  const [sla, setSla] = useState<SlaResponse | null>(null);
  const [breakdown, setBreakdown] = useState<SlaBreakdownResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [kpiRes, slaRes, breakdownRes] = await Promise.all([
          http.get<KpiResponse>('/admin/observability/kpis'),
          http.get<SlaResponse>('/admin/audit/sla/metrics', { params: { days: 7 } }),
          http.get<SlaBreakdownResponse>('/admin/audit/sla/breakdown', { params: { days: 30 } }),
        ]);

        if (!mounted) return;
        setKpis(kpiRes.data);
        setSla(slaRes.data);
        setBreakdown(breakdownRes.data);
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
    <section className="space-y-8">
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
            <MetricCard label="Erros (24h)" value={kpis?.kpis.errors_24h ?? 0} />
            <MetricCard label="Traces (OTel)" value={kpis?.kpis.traces ?? 0} />
            <MetricCard label="OTel Métricas" value={(kpis?.kpis.otel_metrics ?? 0) ? 'Ativo' : 'Indisponível'} />
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
                <div className="flex justify-between">
                  <dt className="text-slate-500">OTel</dt>
                  <dd className="font-medium text-slate-900">{kpis?.telemetry?.otel_available ? 'Ativo' : 'Indisponível'}</dd>
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

          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">SLA por tipo de serviço</h2>
              <span className="text-xs text-slate-400">Últimos {breakdown?.meta?.period_days ?? 30} dias</span>
            </div>
            {breakdown?.items?.length ? (
              <div className="mt-4 overflow-x-auto">
                <table className="min-w-full text-left text-sm">
                  <thead className="text-xs uppercase tracking-wide text-slate-400">
                    <tr>
                      <th className="py-2 pr-4">Serviço</th>
                      <th className="py-2 pr-4">SLA</th>
                      <th className="py-2 pr-4">Tempo médio</th>
                      <th className="py-2 pr-4">Min / Máx</th>
                      <th className="py-2 pr-4">Meta</th>
                      <th className="py-2 pr-4">Estado</th>
                      <th className="py-2 pr-4 text-right">Processados</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {breakdown.items.map((item) => (
                      <tr key={`${item.service_type}-${item.sla_code}`}>
                        <td className="py-2 pr-4 text-slate-700">
                          <div className="flex flex-wrap items-center gap-2">
                            <span>{formatServiceType(item.service_type)}</span>
                            <DomainBadge domain={resolveDomain(item.service_type)} />
                          </div>
                        </td>
                        <td className="py-2 pr-4 text-slate-500">{item.sla_description || item.sla_code || '-'}</td>
                        <td className="py-2 pr-4 text-slate-700">{formatSeconds(item.avg_issuance_time_seconds)}</td>
                        <td className="py-2 pr-4 text-slate-700">
                          {formatSeconds(item.min_issuance_time_seconds)} / {formatSeconds(item.max_issuance_time_seconds)}
                        </td>
                        <td className="py-2 pr-4">
                          <span className={`font-semibold ${resolveDomain(item.service_type).targetClass}`}>
                            {formatSeconds(item.sla_target_seconds)}
                          </span>
                        </td>
                        <td className="py-2 pr-4">
                          <StatusBadge status={item.sla_status} />
                        </td>
                        <td className="py-2 pr-4 text-right text-slate-700">{item.total_processed ?? 0}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="mt-3 text-sm text-slate-500">Sem dados de SLA no período.</div>
            )}
          </div>
        </>
      )}
    </section>
  );
};

const MetricCard: React.FC<{ label: string; value: string | number }> = ({ label, value }) => (
  <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
    <div className="text-xs uppercase tracking-wide text-slate-500">{label}</div>
    <div className="mt-1 text-2xl font-bold text-slate-900">{value}</div>
  </div>
);

const formatSeconds = (value?: number | null) => {
  if (typeof value !== 'number' || Number.isNaN(value)) return '-';
  if (value < 60) return `${Math.round(value)}s`;
  const mins = Math.floor(value / 60);
  const secs = Math.round(value % 60);
  return `${mins}m ${secs}s`;
};

const formatServiceType = (value?: string | null) => {
  if (!value) return '-';
  return value.replace(/_/g, ' ');
};

const resolveDomain = (serviceType?: string | null) => {
  const normalized = (serviceType || '').toLowerCase();
  if (normalized.startsWith('health_')) {
    return { label: 'Saúde', badgeClass: 'bg-teal-50 text-teal-700', targetClass: 'text-teal-700' };
  }
  if (normalized.startsWith('finance_')) {
    return { label: 'Finanças', badgeClass: 'bg-amber-50 text-amber-700', targetClass: 'text-amber-700' };
  }
  if (normalized.startsWith('education_')) {
    return { label: 'Educação', badgeClass: 'bg-indigo-50 text-indigo-700', targetClass: 'text-indigo-700' };
  }
  if (normalized.startsWith('employment_')) {
    return { label: 'Emprego', badgeClass: 'bg-emerald-50 text-emerald-700', targetClass: 'text-emerald-700' };
  }
  if (normalized.startsWith('social_')) {
    return { label: 'Assistência', badgeClass: 'bg-rose-50 text-rose-700', targetClass: 'text-rose-700' };
  }
  if (normalized.startsWith('youth_')) {
    return { label: 'Juventude', badgeClass: 'bg-fuchsia-50 text-fuchsia-700', targetClass: 'text-fuchsia-700' };
  }
  if (normalized.startsWith('identity_')) {
    return { label: 'Identidade', badgeClass: 'bg-slate-50 text-slate-700', targetClass: 'text-slate-700' };
  }
  if (normalized.startsWith('civil_')) {
    return { label: 'Registo Civil', badgeClass: 'bg-sky-50 text-sky-700', targetClass: 'text-sky-700' };
  }
  return { label: 'Geral', badgeClass: 'bg-gray-50 text-gray-700', targetClass: 'text-gray-700' };
};

const DomainBadge: React.FC<{ domain: { label: string; badgeClass: string } }> = ({ domain }) => (
  <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${domain.badgeClass}`}>
    {domain.label}
  </span>
);

const StatusBadge: React.FC<{ status?: string | null }> = ({ status }) => {
  const normalized = (status || '').toUpperCase();
  if (normalized === 'OK') {
    return <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">OK</span>;
  }
  if (normalized === 'WARNING') {
    return <span className="rounded-full bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700">Atenção</span>;
  }
  if (normalized === 'CRITICAL') {
    return <span className="rounded-full bg-rose-50 px-2 py-0.5 text-xs font-semibold text-rose-700">Crítico</span>;
  }
  if (normalized === 'BREACHED') {
    return <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-semibold text-red-700">Estourado</span>;
  }
  return <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600">-</span>;
};

export default ObservabilityOverview;
