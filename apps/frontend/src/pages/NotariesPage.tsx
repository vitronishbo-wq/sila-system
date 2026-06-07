import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Gavel, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const NotariesPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'notaries' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=notaries&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Cartórios e Notariado"
      subtitle="Solicite atos notariais e acompanhe certidões"
      actions={[
        {
          title: 'Solicitar Certidão',
          description: 'Envie documentos para certidões e reconhecimentos.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-indigo-600',
          icon: Gavel,
          onClick: () => startRequest('certidao')
        },
        {
          title: 'Consultar Atos',
          description: 'Verifique o histórico de atos notariais.',
          cta: 'Ver histórico',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => navigate('/citizen/documents/my?service=notaries')
        }
      ]}
      requirements={[
        'Documento de identificação válido',
        'Dados completos do ato solicitado',
        'Documentação comprovatória',
        'Pagamento dos emolumentos'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Conferência', days: '1-2 dias', desc: 'Validação' },
        { step: 3, title: 'Emissão', days: '2-4 dias', desc: 'Processo' },
        { step: 4, title: 'Entrega', days: '1 dia', desc: 'Disponível' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Certidões podem ser retiradas presencialmente.',
        'Acompanhe notificações pela sua FUC.',
        'Documentos incompletos geram devolução.',
        'Prazos variam conforme a serventia.'
      ]}
    />
  );
};

export default NotariesPage;
