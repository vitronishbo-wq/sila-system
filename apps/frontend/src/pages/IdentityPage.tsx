import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, CheckCircle, FileText, User } from 'lucide-react';

export const IdentityPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'documents' | 'requests' | 'status'>('documents');
  const [isLoading, setIsLoading] = useState(false);

  const handleRequestIdentity = async () => {
    setIsLoading(true);
    try {
      // TODO: Implement identity request logic
      console.log('Requesting new identity document');
    } catch (error) {
      console.error('Error requesting identity:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRenewIdentity = async () => {
    setIsLoading(true);
    try {
      // TODO: Implement identity renewal logic
      console.log('Renewing identity document');
    } catch (error) {
      console.error('Error renewing identity:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-8 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <User className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Identidade</h1>
              <p className="text-gray-600 mt-1">Gerencie seus documentos de identidade</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <Button
            onClick={handleRequestIdentity}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg"
          >
            <FileText className="h-5 w-5" />
            Solicitar Bilhete de Identidade
          </Button>
          <Button
            onClick={handleRenewIdentity}
            disabled={isLoading}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg"
          >
            <CheckCircle className="h-5 w-5" />
            Renovar Identidade
          </Button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('documents')}
            className={`px-4 py-3 font-semibold text-sm transition ${
              activeTab === 'documents'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Meus Documentos
          </button>
          <button
            onClick={() => setActiveTab('requests')}
            className={`px-4 py-3 font-semibold text-sm transition ${
              activeTab === 'requests'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Solicitações
          </button>
          <button
            onClick={() => setActiveTab('status')}
            className={`px-4 py-3 font-semibold text-sm transition ${
              activeTab === 'status'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Status
          </button>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 min-h-96">
          {activeTab === 'documents' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Documentos de Identidade</h2>
              <div className="p-6 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 text-center">
                <FileText className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                <p className="text-gray-600">Nenhum documento de identidade ativo</p>
                <p className="text-sm text-gray-500 mt-1">Comece solicitando um novo bilhete de identidade</p>
              </div>
            </div>
          )}

          {activeTab === 'requests' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Minhas Solicitações</h2>
              <div className="p-6 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 text-center">
                <AlertCircle className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                <p className="text-gray-600">Nenhuma solicitação em andamento</p>
                <p className="text-sm text-gray-500 mt-1">Suas solicitações aparecerão aqui</p>
              </div>
            </div>
          )}

          {activeTab === 'status' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Status de Processamento</h2>
              <div className="p-6 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 text-center">
                <CheckCircle className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                <p className="text-gray-600">Nenhum processamento ativo</p>
                <p className="text-sm text-gray-500 mt-1">O status de suas solicitações será exibido aqui</p>
              </div>
            </div>
          )}
        </div>

        {/* Information Card */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-2xl p-6">
          <div className="flex gap-4">
            <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-blue-900 mb-2">Informações Importantes</h3>
              <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                <li>O bilhete de identidade tem validade de 10 anos</li>
                <li>Você pode renovar até 6 meses antes do vencimento</li>
                <li>O processamento leva aproximadamente 15 dias úteis</li>
                <li>Para solicitar, você precisa ter autenticação biométrica ativa</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IdentityPage;
