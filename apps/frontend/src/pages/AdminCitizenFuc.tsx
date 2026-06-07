import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { citizenService } from '@/modules/admin/services';
import type { CitizenSummary } from '@/modules/admin/services';

const formatDate = (value?: string | null) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('pt-PT');
};

const AdminCitizenFuc: React.FC = () => {
  const { id } = useParams();
  const [citizen, setCitizen] = useState<CitizenSummary | null>(null);
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
        const data = await citizenService.getById(id);
        setCitizen(data);
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
    </div>
  );
};

export default AdminCitizenFuc;
