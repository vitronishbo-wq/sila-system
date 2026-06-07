import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bus, Search } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const TransportPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'transport' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=transport&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Transportes"
      subtitle="Licenças, serviços de mobilidade e documentação veicular"
      actions={[
        {
          title: 'Licenças e Viaturas',
          description: 'Submeta documentos para licenciamento e registos.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-emerald-600',
          icon: Bus,
          onClick: () => startRequest('licenciamento')
        },
        {
          title: 'Consultar Registos',
          description: 'Pesquise processos e documentos associados.',
          cta: 'Pesquisar',
          colorClass: 'bg-blue-600',
          icon: Search,
          onClick: () => navigate('/citizen/documents/search?service=transport')
        }
      ]}
      requirements={[
        'Documento de identificação válido',
        'Dados do veículo ou entidade',
        'Comprovativos de propriedade',
        'Taxas de licenciamento em dia'
      ]}
      timeline={[
        { step: 1, title: 'Submissão', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Verificação', days: '2-4 dias', desc: 'Análise' },
        { step: 3, title: 'Pagamento', days: 'Imediato', desc: 'Portal' },
        { step: 4, title: 'Conclusão', days: '1-2 dias', desc: 'Emissão' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Use a busca para encontrar processos anteriores.',
        'Documentos incompletos atrasam o licenciamento.',
        'Acompanhe notificações diretamente na sua FUC.',
        'Guarde comprovativos para fiscalização.'
      ]}
    />
  );
};

export default TransportPage;
