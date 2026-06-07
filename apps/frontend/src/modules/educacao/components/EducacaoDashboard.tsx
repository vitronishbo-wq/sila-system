import React, { useState } from 'react';
import type { DashboardMetrics } from '../types';
import { useAuthStore } from '@/store/authStore';
import { NacionalDashboard } from './NacionalDashboard';
import { ProvincialDashboard } from './ProvincialDashboard';
import { MunicipalDashboard } from './MunicipalDashboard';
import { EscolaDashboard } from './EscolaDashboard';

const DEFAULT_METRICS: DashboardMetrics = {
  total_alunos: 0, total_escolas: 0, total_professores: 0,
  matriculas_pendentes: 0, matriculas_concluidas: 0,
  transferencias_pendentes: 0, transferencias_concluidas: 0,
  delegacoes_ativas: 0,
};

export const EducacaoDashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [metrics] = useState<DashboardMetrics>(DEFAULT_METRICS);

  const roleMap: Record<string, string> = {
    CENTRAL: 'ministerio',
    PROVINCIAL: 'provincial',
    LOCAL: 'municipal',
  };

  const nivelMap: Record<string, React.FC<{ metrics: DashboardMetrics }>> = {
    ministerio: NacionalDashboard,
    provincial: ProvincialDashboard,
    municipal: MunicipalDashboard,
    escola: EscolaDashboard,
  };

  const userLevel = user?.administrative_level || 'CENTRAL';
  const mappedRole = roleMap[userLevel] || 'ministerio';
  const DashboardComponent = nivelMap[mappedRole] || NacionalDashboard;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Painel da Educação</h1>
        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium capitalize">
          {mappedRole}
        </span>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card label="Alunos" value={metrics.total_alunos} color="blue" />
        <Card label="Escolas" value={metrics.total_escolas} color="green" />
        <Card label="Professores" value={metrics.total_professores} color="purple" />
        <Card label="Matrículas Pendentes" value={metrics.matriculas_pendentes} color="yellow" />
      </div>

      <DashboardComponent metrics={metrics} />
    </div>
  );
};

const Card: React.FC<{ label: string; value: number; color: string }> = ({ label, value, color }) => {
  const borderMap: Record<string, string> = {
    blue: 'border-l-blue-500', green: 'border-l-green-500',
    purple: 'border-l-purple-500', yellow: 'border-l-yellow-500',
  };
  return (
    <div className={`bg-white p-6 rounded-lg shadow border-l-4 ${borderMap[color] || 'border-l-gray-500'}`}>
      <p className="text-sm text-gray-500 uppercase">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
};
