import React from 'react';
import { useAdminDashboard } from '../hooks/useDashboard';

const statusStyles: Record<string, string> = {
  APPROVED: "bg-green-100 text-green-800",
  PENDING: "bg-yellow-100 text-yellow-800",
  REJECTED: "bg-red-100 text-red-800",
};

export const AdminDashboard: React.FC = () => {
  const { stats, requests, loading } = useAdminDashboard();

  if (loading) return <div className="p-8 text-center">Carregando painel...</div>;

  return (
    <div className="p-6 space-y-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-900">Painel Central Administrativo</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-sm text-gray-500 uppercase">Total de Pedidos</p>
          <p className="text-2xl font-bold">{stats?.total_requests}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-yellow-500">
          <p className="text-sm text-gray-500 uppercase">Pendentes</p>
          <p className="text-2xl font-bold">{stats?.pending_approvals}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <p className="text-sm text-gray-500 uppercase">Utilizadores Ativos</p>
          <p className="text-2xl font-bold">{stats?.active_users}</p>
        </div>
      </div>

      {/* Requests Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cidadão</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serviço</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {requests.map(req => (
              <tr key={req.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{req.citizen_name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{req.service_type}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusStyles[req.status] ?? "bg-gray-100 text-gray-800"}`}>
                    {req.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(req.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
