import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Briefcase, ClipboardCheck } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const EmploymentPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'employment' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=employment&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Emprego e Trabalho"
      subtitle="Submeta candidaturas e mantenha o seu perfil laboral atualizado"
      actions={[
        {
          title: 'Submeter Candidatura',
          description: 'Envie documentos e currículo para oportunidades ativas.',
          cta: 'Enviar agora',
          colorClass: 'bg-purple-600',
          icon: Briefcase,
          onClick: () => startRequest('candidatura')
        },
        {
          title: 'Consultar Programas',
          description: 'Veja programas de apoio e vagas disponíveis.',
          cta: 'Ver programas',
          colorClass: 'bg-blue-600',
          icon: ClipboardCheck,
          onClick: () => navigate('/citizen/portal?service=employment')
        }
      ]}
      requirements={[
        'Documento de identificação válido',
        'Currículo atualizado',
        'Comprovativos de formação quando aplicável',
        'Contacto telefónico e email ativos'
      ]}
      timeline={[
        { step: 1, title: 'Submissão', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Triagem', days: '1-3 dias', desc: 'Análise' },
        { step: 3, title: 'Seleção', days: '3-7 dias', desc: 'Avaliação' },
        { step: 4, title: 'Resposta', days: 'Até 10 dias', desc: 'Notificação' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'Mantenha o currículo atualizado para melhores resultados.',
        'Notificações sobre vagas chegam pela sua FUC.',
        'Programas podem exigir entrevistas presenciais.',
        'Documentos incompletos atrasam o processo.'
      ]}
    />
  );
};

export default EmploymentPage;
