import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpenCheck, GraduationCap } from 'lucide-react';
import ServiceLanding from '@/components/Services/ServiceLanding';
import { operationsService } from '@/modules/operations/services';

export const EducationPage: React.FC = () => {
  const navigate = useNavigate();
  const [isStarting, setIsStarting] = useState(false);

  const startRequest = async (type: string) => {
    if (isStarting) {
      return;
    }
    setIsStarting(true);
    let orderId: string | null = null;
    try {
      const order = await operationsService.createOrder({ service_id: 'educacao' });
      orderId = order.id;
    } catch (err) {
      console.error('Falha ao iniciar pedido:', err);
    } finally {
      setIsStarting(false);
    }
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/requests/new?service=educacao&type=${type}${orderParam}`);
  };

  return (
    <ServiceLanding
      title="Educação"
      subtitle="Trate matrículas, transferências e documentos escolares"
      actions={[
        {
          title: 'Solicitar Matrícula',
          description: 'Inicie um pedido de matrícula ou renovação escolar.',
          cta: 'Iniciar pedido',
          colorClass: 'bg-teal-600',
          icon: GraduationCap,
          onClick: () => startRequest('matricula')
        },
        {
          title: 'Consultar Serviços Escolares',
          description: 'Veja certificados, boletins e transferências disponíveis.',
          cta: 'Ver catálogo',
          colorClass: 'bg-blue-600',
          icon: BookOpenCheck,
          onClick: () => navigate('/citizen/portal?service=educacao')
        }
      ]}
      requirements={[
        'Documento de identificação do estudante ou encarregado',
        'Comprovativo de residência quando aplicável',
        'Boletim ou certificado anterior para continuidade escolar',
        'Contactos atualizados do responsável'
      ]}
      timeline={[
        { step: 1, title: 'Pedido', days: '0 dias', desc: 'Online' },
        { step: 2, title: 'Validação', days: '1-3 dias', desc: 'Escola' },
        { step: 3, title: 'Confirmação', days: '2-5 dias', desc: 'Secretaria' },
        { step: 4, title: 'Resultado', days: 'Até 7 dias', desc: 'FUC' }
      ]}
      infoTitle="Detalhes Importantes"
      infoItems={[
        'A matrícula pode exigir vagas disponíveis na instituição.',
        'Transferências escolares dependem da validação da escola de origem.',
        'Certificados e boletins ficam associados à sua FUC.',
        'Documentos incompletos podem atrasar a análise.'
      ]}
    />
  );
};

export default EducationPage;
