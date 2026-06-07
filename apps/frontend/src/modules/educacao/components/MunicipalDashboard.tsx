import React from 'react';
import type { DashboardMetrics } from '../types';

export const MunicipalDashboard: React.FC<{ metrics: DashboardMetrics }> = () => (
  <div className="space-y-6">
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">Visão Municipal — Direção Municipal da Educação</h2>
      <p className="text-gray-600">Gestão de escolas e confirmação de matrículas.</p>
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="font-semibold">Total Escolas</p>
          <p className="text-2xl font-bold">—</p>
        </div>
        <div className="p-4 bg-yellow-50 rounded-lg">
          <p className="font-semibold">Confirmações Pendentes</p>
          <p className="text-2xl font-bold">—</p>
        </div>
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="font-semibold">Matrículas Confirmadas</p>
          <p className="text-2xl font-bold">—</p>
        </div>
      </div>
    </div>
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="font-semibold mb-3">Confirmações Pendentes</h3>
      <p className="text-gray-500 text-sm">Nenhuma confirmação pendente.</p>
    </div>
  </div>
);
