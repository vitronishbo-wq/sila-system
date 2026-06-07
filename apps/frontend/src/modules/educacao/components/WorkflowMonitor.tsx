import React, { useState } from 'react';
import { educacaoAdminService } from '../services/educacaoAdminService';
import type { MatriculaWorkflow, TransferenciaWorkflow } from '../types';

export const WorkflowMonitor: React.FC = () => {
  const [tab, setTab] = useState<'matricula' | 'transferencia'>('matricula');
  const [provider, setProvider] = useState('');
  const [studentId, setStudentId] = useState('');
  const [schoolId, setSchoolId] = useState('');
  const [schoolOrigin, setSchoolOrigin] = useState('');
  const [schoolDest, setSchoolDest] = useState('');
  const [actor, setActor] = useState('escola');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleCriarMatricula = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.criarMatricula(provider, studentId, schoolId);
      setResult(res);
    } catch (e: any) { setError(e.message); }
  };

  const handleAvancarMatricula = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.avancarMatricula(provider, actor);
      setResult(res);
    } catch (e: any) { setError(e.response?.data?.detail || e.message); }
  };

  const handleCriarTransferencia = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.criarTransferencia(provider, studentId, schoolOrigin, schoolDest);
      setResult(res);
    } catch (e: any) { setError(e.message); }
  };

  const handleAvancarTransferencia = async () => {
    setError('');
    try {
      const res = await educacaoAdminService.avancarTransferencia(provider, actor);
      setResult(res);
    } catch (e: any) { setError(e.response?.data?.detail || e.message); }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Workflows Institucionais</h1>

      <div className="flex gap-2 border-b">
        <button onClick={() => setTab('matricula')} className={`px-4 py-2 ${tab === 'matricula' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-500'}`}>
          Matrícula
        </button>
        <button onClick={() => setTab('transferencia')} className={`px-4 py-2 ${tab === 'transferencia' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-500'}`}>
          Transferência
        </button>
      </div>

      {tab === 'matricula' ? (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <h2 className="font-semibold">Workflow de Matrícula</h2>
          <p className="text-sm text-gray-500">Escola → Município → Província</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <input placeholder="Provider ID" value={provider} onChange={e => setProvider(e.target.value)} className="border p-2 rounded" />
            <input placeholder="Student ID" value={studentId} onChange={e => setStudentId(e.target.value)} className="border p-2 rounded" />
            <input placeholder="School ID" value={schoolId} onChange={e => setSchoolId(e.target.value)} className="border p-2 rounded" />
          </div>
          <div className="flex gap-3">
            <button onClick={handleCriarMatricula} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Criar</button>
            <input placeholder="Actor (escola/municipio/provincia)" value={actor} onChange={e => setActor(e.target.value)} className="border p-2 rounded flex-1" />
            <button onClick={handleAvancarMatricula} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Avançar</button>
          </div>
          {error && <p className="text-red-600 text-sm">{error}</p>}
          {result && (
            <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto max-h-60">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          <h2 className="font-semibold">Workflow de Transferência</h2>
          <p className="text-sm text-gray-500">Escola Origem → Escola Destino → Município → Província</p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <input placeholder="Provider ID" value={provider} onChange={e => setProvider(e.target.value)} className="border p-2 rounded" />
            <input placeholder="Student ID" value={studentId} onChange={e => setStudentId(e.target.value)} className="border p-2 rounded" />
            <input placeholder="School Origem" value={schoolOrigin} onChange={e => setSchoolOrigin(e.target.value)} className="border p-2 rounded" />
            <input placeholder="School Destino" value={schoolDest} onChange={e => setSchoolDest(e.target.value)} className="border p-2 rounded" />
          </div>
          <div className="flex gap-3">
            <button onClick={handleCriarTransferencia} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Criar</button>
            <input placeholder="Actor (escola_origem/escola_destino/municipio/provincia)" value={actor} onChange={e => setActor(e.target.value)} className="border p-2 rounded flex-1" />
            <button onClick={handleAvancarTransferencia} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Avançar</button>
          </div>
          {error && <p className="text-red-600 text-sm">{error}</p>}
          {result && (
            <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto max-h-60">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};
