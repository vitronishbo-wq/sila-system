import React, { useState } from 'react';
import { educacaoAdminService } from '../services/educacaoAdminService';

export const ScopeChecker: React.FC = () => {
  const [userRole, setUserRole] = useState('ROLE_PROVINCIA');
  const [userProvince, setUserProvince] = useState('');
  const [userMunicipality, setUserMunicipality] = useState('');
  const [userSchool, setUserSchool] = useState('');
  const [resourceNivel, setResourceNivel] = useState('escola');
  const [resourceProvince, setResourceProvince] = useState('');
  const [resourceMunicipality, setResourceMunicipality] = useState('');
  const [resourceSchool, setResourceSchool] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleCheck = async () => {
    const res = await educacaoAdminService.checkScope({
      user_role: userRole,
      user_province: userProvince || undefined,
      user_municipality: userMunicipality || undefined,
      user_school: userSchool || undefined,
      resource_nivel: resourceNivel,
      resource_province: resourceProvince || undefined,
      resource_municipality: resourceMunicipality || undefined,
      resource_school: resourceSchool || undefined,
    });
    setResult(res);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Verificador de Âmbito Territorial</h1>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="font-semibold">Utilizador</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <select value={userRole} onChange={e => setUserRole(e.target.value)} className="border p-2 rounded">
            <option value="ROLE_MINISTERIO">Ministério</option>
            <option value="ROLE_PROVINCIA">Província</option>
            <option value="ROLE_MUNICIPIO">Município</option>
            <option value="ROLE_ESCOLA">Escola</option>
            <option value="ROLE_OPERADOR">Operador</option>
          </select>
          <input placeholder="Province ID" value={userProvince} onChange={e => setUserProvince(e.target.value)} className="border p-2 rounded" />
          <input placeholder="Municipality ID" value={userMunicipality} onChange={e => setUserMunicipality(e.target.value)} className="border p-2 rounded" />
          <input placeholder="School ID" value={userSchool} onChange={e => setUserSchool(e.target.value)} className="border p-2 rounded" />
        </div>

        <h2 className="font-semibold">Recurso</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <select value={resourceNivel} onChange={e => setResourceNivel(e.target.value)} className="border p-2 rounded">
            <option value="nacional">Nacional</option>
            <option value="provincial">Provincial</option>
            <option value="municipal">Municipal</option>
            <option value="escola">Escola</option>
            <option value="operador">Operador</option>
          </select>
          <input placeholder="Province ID" value={resourceProvince} onChange={e => setResourceProvince(e.target.value)} className="border p-2 rounded" />
          <input placeholder="Municipality ID" value={resourceMunicipality} onChange={e => setResourceMunicipality(e.target.value)} className="border p-2 rounded" />
          <input placeholder="School ID" value={resourceSchool} onChange={e => setResourceSchool(e.target.value)} className="border p-2 rounded" />
        </div>

        <button onClick={handleCheck} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Verificar Acesso</button>

        {result && (
          <div className={`p-4 rounded-lg ${result.allowed ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
            <p className={`font-semibold ${result.allowed ? 'text-green-700' : 'text-red-700'}`}>
              {result.allowed ? '✓ Acesso Permitido' : '✗ Acesso Negado'}
            </p>
            {result.reason && <p className="text-sm text-gray-600 mt-1">{result.reason}</p>}
            <pre className="bg-gray-50 p-3 rounded text-sm mt-3 overflow-auto max-h-40">
              {JSON.stringify({ user_scope: result.user_scope, resource_scope: result.resource_scope }, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
