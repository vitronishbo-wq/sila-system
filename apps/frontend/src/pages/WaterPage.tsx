import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Droplet, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const WaterPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string, target: 'request' | 'payment') => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'water' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    if (target === 'payment') {
      navigate(`/citizen/payments?service=water${orderParam}`);
      return;
    }
    navigate(`/citizen/requests/new?service=water&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Água e Saneamento"
      subtitle="Solicite ligações, acompanhe processos e pague faturas"
      actions={[
        {
          title: 'Pagar Fatura',
          description: 'Liquidar consumos pendentes com segurança.',
          cta: 'Pagar agora',
          colorClass: 'bg-cyan-600',
          icon: Droplet,
          onClick: () => startRequest('pagamento', 'payment')
        },
        {
          title: 'Solicitar Ligação',
          description: 'Envie os documentos para iniciar a ligação de água.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => startRequest('ligacao', 'request')
        }
      ]}
      requirements={[
        'Número de cliente ou BI',
        'Comprovativo de residência',
        'Documentação do imóvel',
        'Pagamento de taxas iniciais'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Vistoria', days: '1-3 dias', desc: 'Técnica' },
        { step: 3, title: 'Ativação', days: '1-2 dias', desc: 'Ligação' },
        { step: 4, title: 'Faturação', days: 'Mensal', desc: 'Conta' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Tenha o número de cliente em mãos para pagamentos.',
        'Atualize a morada para evitar atrasos na ligação.',
        'Guarde os comprovativos de pagamento na sua FUC.',
        'Atendimentos presenciais são agendados via portal.'
      ]}
    />
  );
};

export default WaterPage;
