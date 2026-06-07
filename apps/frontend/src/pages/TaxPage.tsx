import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Receipt, CreditCard } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const TaxPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string, target: 'request' | 'payment') => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'tax' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    if (target === 'payment') {
      navigate(`/citizen/payments?service=tax${orderParam}`);
      return;
    }
    navigate(`/citizen/requests/new?service=tax&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Contribuinte (AGT)"
      subtitle="Regularize o seu NIF e realize pagamentos fiscais"
      actions={[
        {
          title: 'Emitir ou Regularizar NIF',
          description: 'Envie a documentação necessária para cadastro fiscal.',
          cta: 'Submeter',
          colorClass: 'bg-yellow-500',
          icon: Receipt,
          onClick: () => startRequest('nif', 'request')
        },
        {
          title: 'Pagar Taxas e Impostos',
          description: 'Aceda ao portal de pagamentos para regularizar pendências.',
          cta: 'Pagar agora',
          colorClass: 'bg-slate-900',
          icon: CreditCard,
          onClick: () => startRequest('pagamento', 'payment')
        }
      ]}
      requirements={[
        'Documento de identificação válido',
        'Comprovativo de residência atualizado',
        'Dados de contacto completos',
        'Pagamento das taxas previstas'
      ]}
      timeline={[
        { step: 1, title: 'Submissão', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Validação', days: '1-3 dias', desc: 'AGT' },
        { step: 3, title: 'Pagamento', days: 'Imediato', desc: 'Portal' },
        { step: 4, title: 'Conclusão', days: '1 dia', desc: 'Emitido' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Os pagamentos ficam disponíveis no histórico da sua conta.',
        'Certifique-se de que o NIF está associado ao seu perfil.',
        'Receberá comprovativos digitais após pagamento.',
        'Pendências fiscais bloqueiam alguns serviços.'
      ]}
    />
  );
};

export default TaxPage;
