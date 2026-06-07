import React from 'react';
import type { DashboardMetrics } from '../types';

export const NacionalDashboard: React.FC<{ metrics: DashboardMetrics }> = () => (
  <div className="space-y-6">
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">Visão Nacional — Ministério da Educação</h2>
      <p className="text-gray-600">Dashboard consolidado de todas as províncias.</p>
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="font-semibold">Total Províncias</p>
          <p className="text-2xl font-bold">18</p>
        </div>
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="font-semibold">Total Municípios</p>
          <p className="text-2xl font-bold">164</p>
        </div>
        <div className="p-4 bg-purple-50 rounded-lg">
          <p className="font-semibold">Delegações Ativas</p>
          <p className="text-2xl font-bold">—</p>
        </div>
      </div>
    </div>
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="font-semibold mb-3">Ações Rápidas</h3>
      <div className="flex gap-3">
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Nova Delegação</button>
        <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Relatório Nacional</button>
      </div>
    </div>
  </div>
);
