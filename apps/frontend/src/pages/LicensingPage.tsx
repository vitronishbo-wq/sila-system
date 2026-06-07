import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileSignature, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const LicensingPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'licensing' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=licensing&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Licenciamento"
      subtitle="Solicite licenças e acompanhe processos regulatórios"
      actions={[
        {
          title: 'Solicitar Licença',
          description: 'Envie a documentação necessária para licenciamento.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-red-600',
          icon: FileSignature,
          onClick: () => startRequest('licenca')
        },
        {
          title: 'Acompanhar Licenças',
          description: 'Verifique o estado e histórico das licenças emitidas.',
          cta: 'Ver andamento',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => navigate('/citizen/documents/my?service=licensing')
        }
      ]}
      requirements={[
        'Documentação técnica do pedido',
        'Comprovativos de pagamento de taxas',
        'Dados da entidade responsável',
        'Declarações e anexos obrigatórios'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Análise', days: '3-5 dias', desc: 'Avaliação' },
        { step: 3, title: 'Pagamento', days: 'Imediato', desc: 'Portal' },
        { step: 4, title: 'Emissão', days: '1-2 dias', desc: 'Conclusão' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Licenças requerem documentação completa para aprovação.',
        'Anexe certificados e plantas quando aplicável.',
        'Acompanhe o progresso pela sua FUC.',
        'Pendências de taxas bloqueiam a emissão.'
      ]}
    />
  );
};

export default LicensingPage;
