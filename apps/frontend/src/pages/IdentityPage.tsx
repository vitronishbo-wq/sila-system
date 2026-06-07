import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, RefreshCw } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const IdentityPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'identity' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=identity&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Identidade Civil"
      subtitle="Solicite, renove ou consulte o seu bilhete de identidade"
      actions={[
        {
          title: 'Solicitar Bilhete',
          description: 'Inicie a inscrição biométrica e abra o pedido do seu bilhete.',
          cta: 'Começar',
          colorClass: 'bg-blue-600',
          icon: FileText,
          onClick: () => startRequest('bilhete')
        },
        {
          title: 'Renovar Bilhete',
          description: 'Atualize dados e envie documentos para renovação.',
          cta: 'Continuar',
          colorClass: 'bg-green-600',
          icon: RefreshCw,
          onClick: () => startRequest('renovacao')
        }
      ]}
      requirements={[
        'Ter mais de 18 anos',
        'Registro civil completo',
        'Estar inscrito na base de dados biométrica',
        'Comparecer presencialmente para biometria'
      ]}
      timeline={[
        { step: 1, title: 'Solicitação', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Biometria', days: '1-2 dias', desc: 'Presencial' },
        { step: 3, title: 'Processamento', days: '3-5 dias', desc: 'Análise' },
        { step: 4, title: 'Emissão', days: '1 dia', desc: 'Pronto' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Comparecer presencialmente no posto de atendimento mais próximo.',
        'Traga documentos originais e cópias legíveis.',
        'A emissão pode variar conforme a província.',
        'Receberá notificações na sua FUC durante o processo.'
      ]}
    />
  );
};

export default IdentityPage;
