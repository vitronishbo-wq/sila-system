import React from 'react';
import type { DashboardMetrics } from '../types';

export const ProvincialDashboard: React.FC<{ metrics: DashboardMetrics }> = () => (
  <div className="space-y-6">
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">Visão Provincial — Direção Provincial da Educação</h2>
      <p className="text-gray-600">Monitoramento de municípios e escolas da província.</p>
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="font-semibold">Total Municípios</p>
          <p className="text-2xl font-bold">—</p>
        </div>
        <div className="p-4 bg-yellow-50 rounded-lg">
          <p className="font-semibold">Auditorias Pendentes</p>
          <p className="text-2xl font-bold">—</p>
        </div>
      </div>
    </div>
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="font-semibold mb-3">Workflows Pendentes de Auditoria</h3>
      <p className="text-gray-500 text-sm">Nenhum workflow pendente de auditoria.</p>
    </div>
  </div>
);
