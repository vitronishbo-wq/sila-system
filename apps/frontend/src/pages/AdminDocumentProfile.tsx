import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { adminDocumentService, AdminDocumentSummary } from '../services/adminDocumentService';

const formatDate = (value?: string | null) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('pt-PT');
};

const AdminDocumentProfile: React.FC = () => {
  const { id } = useParams();
  const [document, setDocument] = useState<AdminDocumentSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!id) {
        setError('Documento inválido.');
        setLoading(false);
        return;
      }
      try {
        const data = await adminDocumentService.getById(id);
        setDocument(data);
      } catch (err) {
        console.error('Erro ao carregar documento:', err);
        setError('Não foi possível carregar o documento.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (loading) {
    return <div className="p-8 text-gray-500">A carregar documento...</div>;
  }

  if (error || !document) {
    return (
      <div className="p-8">
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error || 'Documento indisponível.'}
        </div>
        <a href="#/admin/documents" className="inline-flex mt-4 text-sm text-slate-700 underline">
          Voltar à lista
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Detalhe do Documento</h2>
          <p className="text-sm text-gray-500">Consulta administrativa do documento.</p>
        </div>
        <a href="#/admin/documents" className="text-sm text-slate-700 underline">
          Voltar à lista
        </a>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Tipo</p>
            <p className="font-semibold text-slate-900">{document.document_type}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Cidadão</p>
            <p className="text-gray-700">{document.citizen_name || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">BI</p>
            <p className="text-gray-700">{document.citizen_bi || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Email</p>
            <p className="text-gray-700">{document.citizen_email || '—'}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Emissão</p>
            <p className="text-gray-700">{formatDate(document.issued_at)}</p>
          </div>
          <div>
            <p className="text-xs uppercase text-gray-400 mb-1">Validade</p>
            <p className="text-gray-700">{formatDate(document.valid_until)}</p>
          </div>
        </div>

        <div className="mt-8 flex gap-3">
          {document.file_url ? (
            <a
              href={document.file_url}
              target="_blank"
              rel="noreferrer"
              className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-slate-800"
            >
              Abrir documento
            </a>
          ) : (
            <button
              disabled
              className="rounded-xl border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-400 cursor-not-allowed"
            >
              Documento indisponível
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDocumentProfile;
