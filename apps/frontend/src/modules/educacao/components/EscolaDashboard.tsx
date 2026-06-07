import React from 'react';
import type { DashboardMetrics } from '../types';

export const EscolaDashboard: React.FC<{ metrics: DashboardMetrics }> = () => (
  <div className="space-y-6">
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">Visão da Escola — Gestão Escolar</h2>
      <p className="text-gray-600">Matrículas, transferências e alunos.</p>
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="font-semibold">Alunos Matriculados</p>
          <p className="text-2xl font-bold">—</p>
        </div>
        <div className="p-4 bg-yellow-50 rounded-lg">
          <p className="font-semibold">Validações Pendentes</p>
          <p className="text-2xl font-bold">—</p>
        </div>
      </div>
    </div>
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="font-semibold mb-3">Ações Rápidas</h3>
      <div className="flex flex-wrap gap-3">
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Nova Matrícula</button>
        <button className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700">Solicitar Transferência</button>
        <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Listar Alunos</button>
      </div>
    </div>
  </div>
);
