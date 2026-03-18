import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { useAdminDashboard } from '../hooks/useDashboard';
import { MeteorologyWidget } from '../../meteorologia/components';

export const AdminDashboard: React.FC = () => {
  const { stats, requests, loading } = useAdminDashboard();
  const [showMeteorology, setShowMeteorology] = useState(false);

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
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${req.status === 'APPROVED' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {req.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(req.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Meteorologia Widget - Collapsible */}
      <div className="bg-white rounded-lg shadow">
        <button
          onClick={() => setShowMeteorology(!showMeteorology)}
          className="w-full flex items-center justify-between p-6 hover:bg-gray-50 transition"
        >
          <h2 className="text-xl font-bold text-gray-900">Monitoramento Climático</h2>
          <ChevronDown 
            className={`h-6 w-6 transition-transform ${showMeteorology ? 'rotate-180' : ''}`} 
          />
        </button>
        
        {showMeteorology && (
          <div className="border-t p-6">
            <MeteorologyWidget standalone={false} />
          </div>
        )}
      </div>
    </div>
  );
};
