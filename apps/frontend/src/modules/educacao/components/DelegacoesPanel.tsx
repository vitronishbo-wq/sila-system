import React, { useState } from 'react';
import { educacaoAdminService } from '../services/educacaoAdminService';

export const DelegacoesPanel: React.FC = () => {
  const [delegatorRole, setDelegatorRole] = useState('ROLE_MINISTERIO');
  const [delegatorId, setDelegatorId] = useState('');
  const [delegateRole, setDelegateRole] = useState('ROLE_PROVINCIA');
  const [delegateId, setDelegateId] = useState('');
  const [permission, setPermission] = useState('');
  const [delegateSearchId, setDelegateSearchId] = useState('');
  const [result, setResult] = useState<any>(null);
  const [listResult, setListResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleDelegate = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.delegatePermission(delegatorRole, delegatorId, delegateRole, delegateId, permission);
      setResult(res);
    } catch (e: any) { setError(e.message); }
  };

  const handleList = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.listDelegations(delegateSearchId);
      setListResult(res);
    } catch (e: any) { setError(e.message); }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Gestão de Delegações</h1>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="font-semibold">Nova Delegação</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <select value={delegatorRole} onChange={e => setDelegatorRole(e.target.value)} className="border p-2 rounded">
            <option value="ROLE_MINISTERIO">Ministério</option>
            <option value="ROLE_PROVINCIA">Província</option>
            <option value="ROLE_MUNICIPIO">Município</option>
            <option value="ROLE_ESCOLA">Escola</option>
          </select>
          <input placeholder="Delegator ID" value={delegatorId} onChange={e => setDelegatorId(e.target.value)} className="border p-2 rounded" />
          <input placeholder="Permissão (ex: matricula.validar)" value={permission} onChange={e => setPermission(e.target.value)} className="border p-2 rounded" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <select value={delegateRole} onChange={e => setDelegateRole(e.target.value)} className="border p-2 rounded">
            <option value="ROLE_PROVINCIA">Província</option>
            <option value="ROLE_MUNICIPIO">Município</option>
            <option value="ROLE_ESCOLA">Escola</option>
            <option value="ROLE_OPERADOR">Operador</option>
          </select>
          <input placeholder="Delegate ID" value={delegateId} onChange={e => setDelegateId(e.target.value)} className="border p-2 rounded" />
        </div>
        <button onClick={handleDelegate} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Delegar</button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        {result && (
          <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto max-h-40">{JSON.stringify(result, null, 2)}</pre>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="font-semibold">Listar Delegações Ativas</h2>
        <div className="flex gap-3">
          <input placeholder="Delegate ID" value={delegateSearchId} onChange={e => setDelegateSearchId(e.target.value)} className="border p-2 rounded flex-1" />
          <button onClick={handleList} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Buscar</button>
        </div>
        {listResult && (
          <div>
            <p className="text-sm text-gray-500 mb-2">{listResult.active_delegations?.length || 0} delegações ativas</p>
            <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto max-h-60">{JSON.stringify(listResult, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};
