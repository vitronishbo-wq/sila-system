import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const RegistryPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'registry' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=registry&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Registo Civil"
      subtitle="Peça certidões e acompanhe processos do registo civil"
      actions={[
        {
          title: 'Solicitar Certidão',
          description: 'Envie os documentos necessários para emissão de certidões.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-green-600',
          icon: FileText,
          onClick: () => startRequest('certidao')
        },
        {
          title: 'Acompanhar Pedido',
          description: 'Consulte o estado das certidões já solicitadas.',
          cta: 'Ver andamento',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => navigate('/citizen/documents/my?service=registry')
        }
      ]}
      requirements={[
        'Registo civil atualizado',
        'Documentos originais ou digitalizados',
        'Dados pessoais corretos e completos',
        'Pagamento de emolumentos quando aplicável'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Validação', days: '1-2 dias', desc: 'Conferência' },
        { step: 3, title: 'Emissão', days: '2-4 dias', desc: 'Processo' },
        { step: 4, title: 'Entrega', days: '1 dia', desc: 'Disponível' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Certidões podem ser emitidas em formato digital e físico.',
        'Confirme se o nome está exatamente como no registo.',
        'Notificações são enviadas na sua FUC.',
        'Prazos variam conforme a conservatória.'
      ]}
    />
  );
};

export default RegistryPage;
