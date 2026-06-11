import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { citizenService } from '@/modules/admin/services';
import type { CitizenSummary } from '@/modules/admin/services';

const API_BASE = import.meta.env.VITE_API_URL || '';

interface EducacaoData {
  identidades: Array<{ id: string; nome: string; ns_number: string; status: string }>;
  matriculas: Array<{ id: string; numero_processo: string; escola_nome: string; data: string; status: string }>;
  enrollments: Array<{ id: string; institution_id: string; academic_year: string; grade: string; status: string }>;
  boletins: Array<{ id: string; numero_processo: string; data: string; status: string }>;
  certificados: Array<{ id: string; numero_processo: string; data: string; status: string }>;
}

const formatDate = (value?: string | null) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('pt-PT');
};

const StatusBadge = ({ status }: { status: string }) => {
  const colors: Record<string, string> = {
    ativa: 'bg-green-100 text-green-700',
    activa: 'bg-green-100 text-green-700',
    pendente: 'bg-yellow-100 text-yellow-700',
    concluida: 'bg-blue-100 text-blue-700',
    concluído: 'bg-blue-100 text-blue-700',
    cancelada: 'bg-red-100 text-red-700',
  };
  const cls = colors[status?.toLowerCase()] || 'bg-gray-100 text-gray-600';
  return <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{status}</span>;
};

const AdminCitizenFuc: React.FC = () => {
  const { id } = useParams();
  const [citizen, setCitizen] = useState<CitizenSummary | null>(null);
  const [educacao, setEducacao] = useState<EducacaoData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!id) {
        setError('Cidadão inválido.');
        setLoading(false);
        return;
      }
      try {
        const [citizenData, educData] = await Promise.all([
          citizenService.getById(id),
          fetch(`${API_BASE}/api/educacao/fuc/${id}/educacao`).then(r => r.ok ? r.json() : null),
        ]);
        setCitizen(citizenData);
        setEducacao(educData);
      } catch (err) {
        console.error('Erro ao carregar FUC:', err);
        setError('Não foi possível carregar a FUC.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (loading) {
    return <div className="p-8 text-gray-500">A carregar FUC...</div>;
  }

  if (error || !citizen) {
    return (
      <div className="p-8">
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error || 'FUC indisponível.'}
        </div>
        <a href={`#/admin/citizens/${id}`} className="inline-flex mt-4 text-sm text-slate-700 underline">
          Voltar ao perfil
        </a>
      </div>
    );
  }

  const hasEducacao = educacao && (
    educacao.matriculas.length > 0 ||
    educacao.enrollments.length > 0 ||
    educacao.boletins.length > 0 ||
    educacao.certificados.length > 0 ||
    educacao.identidades.length > 0
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">FUC do Cidadão</h2>
          <p className="text-sm text-gray-500">Vista administrativa da ficha única.</p>
        </div>
        <a href={`#/admin/citizens/${citizen.id}`} className="text-sm text-slate-700 underline">
          Voltar ao perfil
        </a>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <h3 className="text-xl font-semibold text-slate-900 mb-6">Dados pessoais</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Nome completo</p>
            <p className="font-semibold text-slate-900">{citizen.full_name}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">BI</p>
            <p className="text-gray-700">{citizen.bi_number || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Email</p>
            <p className="text-gray-700">{citizen.email || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Telefone</p>
            <p className="text-gray-700">{citizen.phone || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Nascimento</p>
            <p className="text-gray-700">{formatDate(citizen.birth_date)}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Estado</p>
            <p className="text-gray-700">{citizen.is_active ? 'Ativo' : 'Inativo'}</p>
          </div>
        </div>
      </div>

      {hasEducacao && educacao && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <h3 className="text-xl font-semibold text-slate-900 mb-6">Registo Educacional</h3>

          {educacao.identidades.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Identidade Académica</h4>
              <div className="space-y-2">
                {educacao.identidades.map((ident) => (
                  <div key={ident.id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
                    <span className="font-medium text-slate-900">{ident.nome}</span>
                    <span className="text-gray-500">{ident.ns_number}</span>
                    <StatusBadge status={ident.status} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {educacao.matriculas.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Matrículas</h4>
              <div className="space-y-2">
                {educacao.matriculas.map((m) => (
                  <div key={m.id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
                    <span className="text-gray-700">{m.escola_nome}</span>
                    <span className="text-gray-500">{formatDate(m.data)}</span>
                    <StatusBadge status={m.status} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {educacao.enrollments.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Histórico Escolar</h4>
              <div className="space-y-2">
                {educacao.enrollments.map((e) => (
                  <div key={e.id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
                    <span className="text-gray-700">{e.grade} — {e.academic_year}</span>
                    <StatusBadge status={e.status} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {educacao.boletins.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Boletins</h4>
              <div className="space-y-2">
                {educacao.boletins.map((b) => (
                  <div key={b.id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
                    <span className="text-gray-500">{b.numero_processo}</span>
                    <span className="text-gray-500">{formatDate(b.data)}</span>
                    <StatusBadge status={b.status} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {educacao.certificados.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Certificados</h4>
              <div className="space-y-2">
                {educacao.certificados.map((c) => (
                  <div key={c.id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
                    <span className="text-gray-500">{c.numero_processo}</span>
                    <span className="text-gray-500">{formatDate(c.data)}</span>
                    <StatusBadge status={c.status} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminCitizenFuc;
