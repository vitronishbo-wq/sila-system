import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const EnergyPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string, target: 'request' | 'payment') => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'energy' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    if (target === 'payment') {
      navigate(`/citizen/payments?service=energy${orderParam}`);
      return;
    }
    navigate(`/citizen/requests/new?service=energy&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Energia Elétrica"
      subtitle="Pague faturas, solicite ligações e acompanhe pedidos"
      actions={[
        {
          title: 'Pagar Energia',
          description: 'Regularize consumos e evite cortes no fornecimento.',
          cta: 'Pagar agora',
          colorClass: 'bg-orange-600',
          icon: Zap,
          onClick: () => startRequest('pagamento', 'payment')
        },
        {
          title: 'Solicitar Ligação',
          description: 'Submeta documentos para ativar novo fornecimento.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => startRequest('ligacao', 'request')
        }
      ]}
      requirements={[
        'Documento de identificação válido',
        'Comprovativo de residência',
        'Documentos do imóvel',
        'Pagamento de taxas de ligação'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Vistoria', days: '1-3 dias', desc: 'Técnica' },
        { step: 3, title: 'Ativação', days: '1-2 dias', desc: 'Ligação' },
        { step: 4, title: 'Faturação', days: 'Mensal', desc: 'Conta' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Acompanhe a vistoria no histórico da sua conta.',
        'Pagamentos ficam disponíveis para consulta.',
        'Atualize dados de contacto para avisos de consumo.',
        'Faturas vencidas geram restrições de serviço.'
      ]}
    />
  );
};

export default EnergyPage;
