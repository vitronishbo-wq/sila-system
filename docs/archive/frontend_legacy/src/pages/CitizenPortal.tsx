import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { citizenAuthService } from '../services/citizenAuthService';

interface CitizenProfile {
  id: string;
  full_name: string;
  birth_date?: string | null;
  gender?: string | null;
  vital_status?: string | null;
  id_number?: string | null;
  nif?: string | null;
}

interface ServiceCatalogItem {
  id: string;
  code: string;
  name: string;
  description: string;
  price: number;
  workflow_definition_key: string;
  active: boolean;
}

interface OrderDocument {
  id: string;
  filename: string;
  content_type: string;
  size_bytes: number;
  uri?: string;
  created_at: string;
}

interface Payment {
  id: string;
  order_id: string;
  reference: string;
  amount: number;
  status: string;
  provider: string;
  created_at: string;
  confirmed_at?: string;
}

interface OperationalOrder {
  id: string;
  citizen_id: string;
  service_id: string;
  workflow_instance_id: string;
  total_amount: number;
  status: string;
  status_history: Array<{ from?: string; to: string; reason: string; at: string }>;
  created_at: string;
  submitted_at?: string;
  completed_at?: string;
  receipt_number?: string;
  documents: OrderDocument[];
  payments: Payment[];
}

interface CitizenPortalProps {
  onLogout: () => void;
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const CitizenPortal: React.FC<CitizenPortalProps> = ({ onLogout }) => {
  const [profile, setProfile] = useState<CitizenProfile | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [services, setServices] = useState<ServiceCatalogItem[]>([]);
  const [selectedServiceId, setSelectedServiceId] = useState<string>('');
  const [activeOrder, setActiveOrder] = useState<OperationalOrder | null>(null);
  const [receiptPayload, setReceiptPayload] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isOpsLoading, setIsOpsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [opsMessage, setOpsMessage] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'profile' | 'events' | 'operations'>('profile');
  const hasLoadedRef = useRef(false);

  useEffect(() => {
    if (hasLoadedRef.current) return;
    hasLoadedRef.current = true;
    loadCitizenData();
  }, []);

  const authHeaders = () => {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const loadServices = async () => {
    const response = await axios.get<ServiceCatalogItem[]>(`${API_BASE}/services`, {
      headers: authHeaders(),
    });
    setServices(response.data);
    if (!selectedServiceId && response.data.length > 0) {
      setSelectedServiceId(response.data[0].id);
    }
  };

  const refreshOrder = async (orderId: string) => {
    const response = await axios.get<OperationalOrder>(`${API_BASE}/orders/${orderId}`, {
      headers: authHeaders(),
    });
    setActiveOrder(response.data);
    return response.data;
  };

  const loadCitizenData = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const profileData = await citizenAuthService.getProfile();
      setProfile(profileData);

      try {
        const eventsData = await citizenAuthService.getEvents();
        setEvents(eventsData);
      } catch {
        setEvents([]);
      }

      try {
        await loadServices();
      } catch (error) {
        console.error('Failed to load service catalog:', error);
      }
    } catch (err) {
      console.error('Failed to load citizen data:', err);
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setErrorMessage('Sessão expirada ou sem permissões de cidadão. Inicie sessão novamente.');
      } else {
        setErrorMessage('Não foi possível carregar o perfil do cidadão.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const executeOperation = async (action: () => Promise<void>) => {
    setIsOpsLoading(true);
    setOpsMessage('');
    try {
      await action();
    } catch (error) {
      console.error('Operational flow error:', error);
      if (axios.isAxiosError(error)) {
        setOpsMessage(error.response?.data?.detail || 'Falha ao executar a operação.');
      } else {
        setOpsMessage('Falha ao executar a operação.');
      }
    } finally {
      setIsOpsLoading(false);
    }
  };

  const handleCreateOrder = async () => {
    if (!selectedServiceId) {
      setOpsMessage('Selecione um serviço para criar o pedido.');
      return;
    }
    await executeOperation(async () => {
      const response = await axios.post<OperationalOrder>(
        `${API_BASE}/orders`,
        { service_id: selectedServiceId },
        { headers: authHeaders() }
      );
      setActiveOrder(response.data);
      setReceiptPayload(null);
      setOpsMessage(`Pedido criado com sucesso: ${response.data.id}`);
    });
  };

  const handleSubmitOrder = async () => {
    if (!activeOrder) return;
    await executeOperation(async () => {
      const docsPayload = {
        documents: [
          {
            filename: 'requerimento-assinado.pdf',
            content_type: 'application/pdf',
            size_bytes: 182340,
            uri: `citizen://${activeOrder.id}/requerimento-assinado.pdf`,
          },
          {
            filename: 'bi-frente.jpg',
            content_type: 'image/jpeg',
            size_bytes: 93412,
            uri: `citizen://${activeOrder.id}/bi-frente.jpg`,
          },
        ],
      };

      await axios.post(`${API_BASE}/orders/${activeOrder.id}/documents`, docsPayload, {
        headers: authHeaders(),
      });
      await axios.post(`${API_BASE}/orders/${activeOrder.id}/submit`, {}, { headers: authHeaders() });
      await refreshOrder(activeOrder.id);
      setOpsMessage('Pedido submetido e colocado em revisão.');
    });
  };

  const handleGeneratePayment = async () => {
    if (!activeOrder) return;
    await executeOperation(async () => {
      await axios.post(`${API_BASE}/payments/${activeOrder.id}/generate`, {}, { headers: authHeaders() });
      await refreshOrder(activeOrder.id);
      setOpsMessage('Referência de pagamento gerada.');
    });
  };

  const handleConfirmPayment = async () => {
    const reference = activeOrder?.payments?.find((p) => p.status === 'PENDING')?.reference;
    if (!reference) {
      setOpsMessage('Nenhuma referência pendente para confirmar.');
      return;
    }

    await executeOperation(async () => {
      await axios.post(`${API_BASE}/payments/${reference}/confirm`, {}, { headers: authHeaders() });
      await refreshOrder(activeOrder!.id);
      setOpsMessage(`Pagamento confirmado: ${reference}`);
    });
  };

  const handleCompleteOrder = async () => {
    if (!activeOrder) return;
    await executeOperation(async () => {
      await axios.post(`${API_BASE}/orders/${activeOrder.id}/complete`, {}, { headers: authHeaders() });
      await refreshOrder(activeOrder.id);
      setOpsMessage('Pedido concluído com sucesso.');
    });
  };

  const handleFetchReceipt = async () => {
    if (!activeOrder) return;
    await executeOperation(async () => {
      const response = await axios.get(`${API_BASE}/orders/${activeOrder.id}/receipt`, {
        headers: authHeaders(),
      });
      setReceiptPayload(response.data);
      setOpsMessage('Comprovativo emitido.');
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 mb-4"></div>
          <p className="text-gray-600">A carregar o seu perfil...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <p className="text-red-600 mb-4">{errorMessage || 'Erro ao carregar o perfil'}</p>
          <button onClick={onLogout} className="px-4 py-2 bg-red-600 text-white rounded">
            Voltar
          </button>
        </div>
      </div>
    );
  }

  const selectedService = services.find((s) => s.id === selectedServiceId);
  const pendingPaymentRef = activeOrder?.payments?.find((p) => p.status === 'PENDING')?.reference;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-slate-900">Minha FUC</h1>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold"
            title="Terminar sessão"
          >
            Sair
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex border-b mb-8 bg-white rounded-t-lg">
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'profile'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Perfil
          </button>
          <button
            onClick={() => setActiveTab('events')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'events'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Eventos
          </button>
          <button
            onClick={() => setActiveTab('operations')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'operations'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Pedidos e Pagamentos
          </button>
        </div>

        {activeTab === 'profile' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Dados Pessoais</h2>
            <div className="grid grid-cols-2 gap-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nome Completo</label>
                <p className="text-lg">{profile.full_name || 'Não informado'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data de Nascimento</label>
                <p className="text-lg">
                  {profile.birth_date ? new Date(profile.birth_date).toLocaleDateString('pt-PT') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Género</label>
                <p className="text-lg">
                  {profile.gender ? (profile.gender === 'M' ? 'Masculino' : 'Feminino') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Estado Vital</label>
                <p className="text-lg">
                  {profile.vital_status ? (profile.vital_status === 'ALIVE' ? 'Vivo' : 'Falecido') : 'Não informado'}
                </p>
              </div>
              {profile.id_number && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Número BI</label>
                  <p className="text-lg">{profile.id_number}</p>
                </div>
              )}
              {profile.nif && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">NIF</label>
                  <p className="text-lg">{profile.nif}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'events' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Histórico de Eventos</h2>
            {events.length === 0 ? (
              <p className="text-gray-500">Nenhum evento registado</p>
            ) : (
              <div className="space-y-4">
                {events.map((event: any) => (
                  <div key={event.id} className="border-l-4 border-slate-900 pl-4 py-2">
                    <p className="font-semibold">{event.event_type}</p>
                    <p className="text-sm text-gray-600">{new Date(event.created_at).toLocaleDateString('pt-PT')}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'operations' && (
          <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <h2 className="text-2xl font-bold">Fluxo Operacional do Pedido</h2>

            <div className="grid md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Serviço</label>
                <select
                  value={selectedServiceId}
                  onChange={(e) => setSelectedServiceId(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  {services.map((service) => (
                    <option key={service.id} value={service.id}>
                      {service.name} ({service.price.toLocaleString('pt-PT')} AOA)
                    </option>
                  ))}
                </select>
                {selectedService && (
                  <p className="text-sm text-gray-600 mt-2">{selectedService.description}</p>
                )}
              </div>
              <div className="flex items-end">
                <button
                  onClick={handleCreateOrder}
                  disabled={isOpsLoading || !selectedServiceId}
                  className="w-full px-4 py-2 bg-slate-900 text-white rounded-lg disabled:opacity-50"
                >
                  Pedir Serviço
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <button
                onClick={handleSubmitOrder}
                disabled={isOpsLoading || !activeOrder || activeOrder.status !== 'DRAFT'}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
              >
                Submeter Pedido
              </button>
              <button
                onClick={handleGeneratePayment}
                disabled={
                  isOpsLoading ||
                  !activeOrder ||
                  (activeOrder.status !== 'IN_REVIEW' && activeOrder.status !== 'AWAITING_PAYMENT')
                }
                className="px-4 py-2 bg-amber-600 text-white rounded-lg disabled:opacity-50"
              >
                Gerar Referência de Pagamento
              </button>
              <button
                onClick={handleConfirmPayment}
                disabled={isOpsLoading || !pendingPaymentRef}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg disabled:opacity-50"
              >
                Confirmar Pagamento
              </button>
              <button
                onClick={handleCompleteOrder}
                disabled={isOpsLoading || !activeOrder || activeOrder.status !== 'PAID'}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg disabled:opacity-50"
              >
                Concluir Pedido
              </button>
            </div>

            <button
              onClick={handleFetchReceipt}
              disabled={isOpsLoading || !activeOrder || activeOrder.status !== 'COMPLETED'}
              className="px-4 py-2 bg-slate-700 text-white rounded-lg disabled:opacity-50"
            >
              Emitir Comprovativo
            </button>

            {opsMessage && (
              <div className="p-3 bg-slate-100 rounded border text-sm text-slate-700">{opsMessage}</div>
            )}

            {activeOrder && (
              <div className="border rounded-lg p-4 space-y-2">
                <h3 className="font-semibold text-lg">Pedido Atual</h3>
                <p><strong>ID:</strong> {activeOrder.id}</p>
                <p><strong>Status:</strong> {activeOrder.status}</p>
                <p><strong>Workflow Instance:</strong> {activeOrder.workflow_instance_id}</p>
                <p><strong>Total:</strong> {activeOrder.total_amount.toLocaleString('pt-PT')} AOA</p>
                <p><strong>Referência pendente:</strong> {pendingPaymentRef || '---'}</p>
              </div>
            )}

            {receiptPayload && (
              <div className="border rounded-lg p-4 bg-emerald-50 border-emerald-300">
                <h3 className="font-semibold text-lg mb-2">Comprovativo</h3>
                <pre className="text-xs overflow-auto">{JSON.stringify(receiptPayload, null, 2)}</pre>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default CitizenPortal;
