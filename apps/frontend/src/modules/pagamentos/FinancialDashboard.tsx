import React, { useState, useEffect, useCallback } from 'react';
import Layout from './components/Layout';
import FinancialAssistant from './components/FinancialAssistant';
import { financeService } from './services/financeService';
import { 
  UserRole, 
  Invoice, 
  InvoiceStatus, 
  FinanceStats 
} from './types';

const App: React.FC = () => {
  const [role, setRole] = useState<UserRole>(UserRole.ADMIN);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [stats, setStats] = useState<FinanceStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showPayModal, setShowPayModal] = useState<Invoice | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const invData = await financeService.getInvoices(role === UserRole.CITIZEN ? 'cit_123' : undefined);
      const statData = await financeService.getStats();
      setInvoices(invData);
      setStats(statData);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  }, [role]);

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [role]);

  const handlePayment = async (inv: Invoice) => {
    try {
      await financeService.processPayment(inv.id, inv.citizen_id, inv.amount);
      setShowPayModal(null);
      fetchData();
      alert("Pagamento processado com sucesso! Fatura atualizada.");
    } catch (error: any) {
      alert(error.message);
    }
  };

  const getStatusStyle = (status: InvoiceStatus) => {
    switch (status) {
      case InvoiceStatus.PAID: return 'bg-emerald-100 text-emerald-700 border-emerald-200';
      case InvoiceStatus.PENDING: return 'bg-amber-100 text-amber-700 border-amber-200';
      case InvoiceStatus.OVERDUE: return 'bg-red-100 text-red-700 border-red-200';
      case InvoiceStatus.CANCELLED: return 'bg-slate-100 text-slate-500 border-slate-200';
      default: return 'bg-slate-100 text-slate-500';
    }
  };

  return (
    <Layout role={role} onRoleChange={setRole}>
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Receita Total" value={`${stats?.total_revenue.toLocaleString()} AOA`} icon="money" color="emerald" />
          <StatCard title="Montante Pendente" value={`${stats?.pending_amount.toLocaleString()} AOA`} icon="clock" color="amber" />
          <StatCard title="Faturas Pagas" value={stats?.paid_count || 0} icon="check" color="blue" />
          <StatCard title="Aguardando Pgto" value={stats?.pending_count || 0} icon="list" color="purple" />
        </div>

        {/* Content Tabs */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="border-b border-slate-200 px-6 py-4 flex items-center justify-between bg-slate-50/50">
            <h2 className="font-bold text-slate-800">Gestão de Faturas</h2>
            <div className="flex gap-2">
              <button className="px-4 py-2 text-sm font-medium bg-white border border-slate-300 rounded-lg hover:bg-slate-50">Exportar</button>
              {role !== UserRole.CITIZEN && (
                <button className="px-4 py-2 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700">Nova Fatura</button>
              )}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-xs font-bold uppercase text-slate-400 bg-slate-50/50">
                  <th className="px-6 py-4 border-b">Referência</th>
                  <th className="px-6 py-4 border-b">Serviço / Classificação</th>
                  <th className="px-6 py-4 border-b">Montante</th>
                  <th className="px-6 py-4 border-b">Data Emissão</th>
                  <th className="px-6 py-4 border-b">Estado</th>
                  <th className="px-6 py-4 border-b text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {loading ? (
                  <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-400 italic">Carregando dados financeiros...</td></tr>
                ) : invoices.length === 0 ? (
                  <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-400 italic">Nenhuma fatura encontrada.</td></tr>
                ) : invoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4 text-sm font-semibold text-slate-900">
                      <div>{inv.reference}</div>
                      <div className="text-[9px] text-slate-400 font-normal">ID: {inv.id.split('_')[1]}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-slate-700">{inv.service_name}</div>
                      <div className="flex gap-2 mt-1">
                        <span className="text-[9px] bg-slate-100 px-1 rounded text-slate-500 font-mono">Rubrica: {inv.revenue_code}</span>
                        <span className="text-[9px] bg-slate-100 px-1 rounded text-slate-500 font-mono">Órgão: {inv.cost_center}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-semibold text-slate-900">{inv.amount.toLocaleString()} {inv.currency}</td>
                    <td className="px-6 py-4 text-sm text-slate-500">{new Date(inv.created_at).toLocaleDateString()}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-[10px] font-bold border ${getStatusStyle(inv.status)}`}>
                        {inv.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex gap-2 justify-end">
                        {inv.status === InvoiceStatus.PENDING ? (
                          <button 
                            onClick={() => setShowPayModal(inv)}
                            className="px-3 py-1.5 text-xs font-bold text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors shadow-sm"
                            title="Proceder com o pagamento"
                          >
                            Pagar
                          </button>
                        ) : (
                          <button className="px-3 py-1.5 text-xs font-bold text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors shadow-sm" title="Ver comprovante de pagamento">
                            Recibo
                          </button>
                        )}
                        <button className="px-3 py-1.5 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors" title="Descarregar fatura">
                          Download
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Payment Modal */}
      {showPayModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-[100] backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h3 className="font-bold text-lg text-slate-900">Finalizar Pagamento</h3>
              <button onClick={() => setShowPayModal(null)} className="text-slate-400 hover:text-slate-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="p-6 space-y-6">
              <div className="bg-slate-50 rounded-xl p-4 border border-slate-100">
                <p className="text-xs text-slate-500 uppercase font-bold mb-1">Total a pagar</p>
                <h4 className="text-2xl font-black text-slate-900">{showPayModal.amount.toLocaleString()} {showPayModal.currency}</h4>
                <div className="flex justify-between items-center mt-2">
                  <p className="text-[10px] text-slate-400 uppercase font-bold">Ref: {showPayModal.reference}</p>
                  <p className="text-[10px] text-slate-400 uppercase font-bold">Org: {showPayModal.cost_center}</p>
                </div>
              </div>
              
              <div className="space-y-3">
                <label className="block text-sm font-bold text-slate-700">Método de Pagamento</label>
                <div className="grid grid-cols-2 gap-3">
                  <button className="border-2 border-red-600 bg-red-50 p-3 rounded-xl flex flex-col items-center gap-1 group">
                    <div className="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center text-white">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                    </div>
                    <span className="text-[10px] font-bold uppercase text-red-600">Multicaixa</span>
                  </button>
                  <button className="border-2 border-slate-100 p-3 rounded-xl flex flex-col items-center gap-1 hover:border-red-200 transition-colors">
                    <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center text-slate-400">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                    </div>
                    <span className="text-[10px] font-bold uppercase text-slate-500">Express</span>
                  </button>
                </div>
              </div>

              <button 
                onClick={() => handlePayment(showPayModal)}
                className="w-full bg-slate-900 text-white font-bold py-4 rounded-xl hover:bg-black transition-colors shadow-lg shadow-slate-200"
              >
                Confirmar Pagamento
              </button>
            </div>
          </div>
        </div>
      )}

      <FinancialAssistant />
    </Layout>
  );
};

const StatCard: React.FC<{ title: string; value: string | number; icon: string; color: string }> = ({ title, value, color }) => {
  const colorMap: any = {
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    blue: 'bg-blue-50 text-blue-600 border-blue-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
  };
  
  return (
    <div className={`p-6 rounded-2xl border ${colorMap[color]} flex flex-col`}>
      <span className="text-xs font-bold uppercase opacity-70 mb-2">{title}</span>
      <span className="text-2xl font-black">{value}</span>
    </div>
  );
};

export default App;