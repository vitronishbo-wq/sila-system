import React from 'react';
import { ArrowRight, FileText, RefreshCw, AlertCircle, Clock } from 'lucide-react';

export const IdentityPage: React.FC = () => {
  const handleRequestIdentity = async () => {
    console.log('Requesting new identity document');
  };

  const handleRenewIdentity = async () => {
    console.log('Renewing identity document');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Identidade Civil</h1>
          <p className="text-slate-600">Solicite, renove ou consulte seu bilhete de identidade</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Service Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Request Identity Card */}
          <button
            onClick={handleRequestIdentity}
            className="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 p-8 text-left border border-slate-200 hover:border-blue-400 hover:scale-105"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-4 bg-blue-100 rounded-xl group-hover:bg-blue-200 transition">
                <FileText className="h-8 w-8 text-blue-600" />
              </div>
              <ArrowRight className="h-5 w-5 text-slate-400 group-hover:text-blue-600 transition" />
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Solicitar Bilhete</h2>
            <p className="text-slate-600 text-sm mb-4">Inicie o processo de solicitação de um novo bilhete de identidade</p>
            <div className="flex items-center text-blue-600 text-sm font-semibold">
              Começar <ArrowRight className="h-4 w-4 ml-2" />
            </div>
          </button>

          {/* Renew Identity Card */}
          <button
            onClick={handleRenewIdentity}
            className="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 p-8 text-left border border-slate-200 hover:border-green-400 hover:scale-105"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-4 bg-green-100 rounded-xl group-hover:bg-green-200 transition">
                <RefreshCw className="h-8 w-8 text-green-600" />
              </div>
              <ArrowRight className="h-5 w-5 text-slate-400 group-hover:text-green-600 transition" />
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Renovar Bilhete</h2>
            <p className="text-slate-600 text-sm mb-4">Renove seu bilhete de identidade próximo do vencimento</p>
            <div className="flex items-center text-green-600 text-sm font-semibold">
              Continuar <ArrowRight className="h-4 w-4 ml-2" />
            </div>
          </button>
        </div>

        {/* Requirements Section */}
        <div className="bg-white rounded-2xl shadow-md p-8 border border-slate-200 mb-8">
          <div className="flex gap-4 mb-6">
            <AlertCircle className="h-6 w-6 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-gray-900 text-lg mb-3">Requisitos Importantes</h3>
              <ul className="space-y-2 text-slate-700 text-sm">
                <li className="flex items-center gap-3">
                  <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
                  Ter mais de 18 anos
                </li>
                <li className="flex items-center gap-3">
                  <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
                  Registro civil completo
                </li>
                <li className="flex items-center gap-3">
                  <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
                  Estar inscrito na base de dados biométrica
                </li>
                <li className="flex items-center gap-3">
                  <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
                  Comparecer presencialmente para biometria
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Processing Timeline */}
        <div className="bg-white rounded-2xl shadow-md p-8 border border-slate-200">
          <div className="flex items-center gap-3 mb-6">
            <Clock className="h-6 w-6 text-blue-600" />
            <h3 className="font-bold text-gray-900 text-lg">Processo de Emissão</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { step: 1, title: 'Solicitação', days: '0 dias', desc: 'Online' },
              { step: 2, title: 'Biometria', days: '1-2 dias', desc: 'Presencial' },
              { step: 3, title: 'Processamento', days: '3-5 dias', desc: 'Análise' },
              { step: 4, title: 'Emissão', days: '1 dia', desc: 'Pronto' },
            ].map((item, idx) => (
              <div key={idx} className="text-center p-4 rounded-xl bg-slate-50 hover:bg-blue-50 transition">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-full font-bold mb-3 mx-auto">
                  {item.step}
                </div>
                <p className="font-semibold text-gray-900 text-sm mb-1">{item.title}</p>
                <p className="text-xs text-blue-600 font-semibold mb-1">{item.days}</p>
                <p className="text-xs text-slate-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-2xl p-6">
          <h4 className="font-bold text-blue-900 mb-3">Detalhes Importantes</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div className="flex gap-2">
              <span className="text-lg">📋</span>
              <p>O bilhete de identidade tem validade de 10 anos</p>
            </div>
            <div className="flex gap-2">
              <span className="text-lg">🔄</span>
              <p>Pode renovar até 6 meses antes do vencimento</p>
            </div>
            <div className="flex gap-2">
              <span className="text-lg">💼</span>
              <p>Processamento levará aproximadamente 10 dias úteis</p>
            </div>
            <div className="flex gap-2">
              <span className="text-lg">🔐</span>
              <p>Autenticação biométrica é obrigatória</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IdentityPage;
