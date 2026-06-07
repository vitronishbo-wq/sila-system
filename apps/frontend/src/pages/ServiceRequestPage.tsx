import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  ArrowLeft,
  CheckCircle2,
  ClipboardList,
  CreditCard,
  FileCheck2,
  Fingerprint,
  QrCode,
  School,
  UploadCloud,
  UserRound,
  Users,
  WalletCards
} from 'lucide-react';
import { operationsService } from '@/modules/operations/services';
import CitizenAreaBanner from '@/components/Services/CitizenAreaBanner';

type ServiceConfig = {
  title: string;
  subtitle: string;
  defaultType: string;
  types: string[];
  price: number;
  showBiometrics?: boolean;
};

const SERVICE_CONFIG: Record<string, ServiceConfig> = {
  identity: {
    title: 'Identidade Civil',
    subtitle: 'Pedido de bilhete de identidade',
    defaultType: 'bilhete',
    types: ['bilhete', 'renovacao', 'segunda_via'],
    price: 1000,
    showBiometrics: true
  },
  registry: {
    title: 'Registo Civil',
    subtitle: 'Emissão de certidão',
    defaultType: 'certidao',
    types: ['certidao', 'nascimento', 'casamento', 'obito'],
    price: 500
  },
  tax: {
    title: 'Contribuinte (AGT)',
    subtitle: 'Emissão ou regularização de NIF',
    defaultType: 'nif',
    types: ['nif', 'regularizacao', 'segunda_via'],
    price: 750
  },
  water: {
    title: 'Água e Saneamento',
    subtitle: 'Ligação e serviços de água',
    defaultType: 'ligacao',
    types: ['ligacao', 'reparacao', 'revisao'],
    price: 3500
  },
  energy: {
    title: 'Energia Elétrica',
    subtitle: 'Ligação e serviços de energia',
    defaultType: 'ligacao',
    types: ['ligacao', 'reparacao', 'revisao'],
    price: 3500
  },
  educacao: {
    title: 'Educação',
    subtitle: 'Matrícula, transferência e documentos escolares',
    defaultType: 'matricula',
    types: ['matricula', 'renovacao', 'transferencia', 'certificado', 'boletim'],
    price: 0
  },
  employment: {
    title: 'Emprego e Trabalho',
    subtitle: 'Submissão de candidatura',
    defaultType: 'candidatura',
    types: ['candidatura', 'programa', 'formacao'],
    price: 0
  },
  licensing: {
    title: 'Licenciamento',
    subtitle: 'Solicitação de licença',
    defaultType: 'licenca',
    types: ['licenca', 'renovacao', 'alvara'],
    price: 2500
  },
  transport: {
    title: 'Transportes',
    subtitle: 'Licenciamento e registos',
    defaultType: 'licenciamento',
    types: ['licenciamento', 'vistoria', 'registo'],
    price: 3000
  },
  notaries: {
    title: 'Cartórios e Notariado',
    subtitle: 'Emissão de certidão notarial',
    defaultType: 'certidao',
    types: ['certidao', 'reconhecimento', 'autenticacao'],
    price: 1200
  }
};

const formatCurrency = (value: number) =>
  value.toLocaleString('pt-AO', { style: 'currency', currency: 'AOA' });

const enrollmentSteps = [
  { key: 'student', title: 'Estudante', icon: UserRound },
  { key: 'guardian', title: 'Encarregado', icon: Users },
  { key: 'school', title: 'Escola', icon: School },
  { key: 'documents', title: 'Documentos', icon: FileCheck2 },
  { key: 'validation', title: 'Validação', icon: CheckCircle2 },
  { key: 'payment', title: 'Pagamento', icon: WalletCards },
  { key: 'confirmation', title: 'Confirmação', icon: QrCode }
];

const ServiceRequestPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const serviceId = searchParams.get('service') ?? 'identity';
  const requestedType = searchParams.get('type');
  const initialOrderId = searchParams.get('orderId');
  const config = SERVICE_CONFIG[serviceId] ?? SERVICE_CONFIG.identity;

  const [orderId, setOrderId] = useState<string | null>(initialOrderId);
  const [isCreating, setIsCreating] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [requestType, setRequestType] = useState(requestedType ?? config.defaultType);
  const [notes, setNotes] = useState('');
  const [delivery, setDelivery] = useState('digital');
  const [enrollmentStep, setEnrollmentStep] = useState(0);
  const [enrollmentForm, setEnrollmentForm] = useState<Record<string, string>>({
    paymentMethod: 'referencia',
    shift: 'manha'
  });

  const typeOptions = useMemo(() => config.types, [config.types]);
  const isEnrollmentWizard = serviceId === 'educacao' && requestType === 'matricula';

  useEffect(() => {
    if (requestedType) {
      setRequestType(requestedType);
    }
  }, [requestedType]);

  useEffect(() => {
    if (orderId || isCreating) {
      return;
    }

    const createOrder = async () => {
      setIsCreating(true);
      setError(null);
      try {
        const order = await operationsService.createOrder({ service_id: serviceId });
        setOrderId(order.id);
      } catch (err) {
        console.error('Falha ao criar pedido:', err);
        setError('Não foi possível abrir o pedido agora.');
      } finally {
        setIsCreating(false);
      }
    };

    createOrder();
  }, [orderId, isCreating, serviceId]);

  const handleSubmit = async () => {
    if (!orderId || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      await operationsService.submitOrder(orderId);
      navigate(`/citizen/payments?service=${serviceId}&orderId=${orderId}`);
    } catch (err) {
      console.error('Falha ao submeter pedido:', err);
      setError('Não foi possível submeter o pedido. Tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAttachDocs = () => {
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/documents/upload?service=${serviceId}${orderParam}`);
  };

  const handleBiometrics = () => {
    const orderParam = orderId ? `&orderId=${orderId}` : '';
    navigate(`/citizen/services/identity/biometrics?service=${serviceId}${orderParam}`);
  };

  const updateEnrollmentField = (key: string, value: string) => {
    setEnrollmentForm((current) => ({ ...current, [key]: value }));
  };

  const fieldClass =
    'mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500';

  const renderTextField = (
    key: string,
    label: string,
    type = 'text',
    placeholder?: string,
    required = true
  ) => (
    <label className="text-sm font-semibold text-slate-700">
      {label}
      <input
        value={enrollmentForm[key] ?? ''}
        onChange={(event) => updateEnrollmentField(key, event.target.value)}
        type={type}
        placeholder={placeholder}
        required={required}
        className={fieldClass}
      />
    </label>
  );

  const renderReadOnlyField = (label: string, value: string) => (
    <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
      <span className="block text-xs font-semibold uppercase text-slate-400">{label}</span>
      <span className="text-sm font-semibold text-slate-800">{value}</span>
    </div>
  );

  const renderEnrollmentStepFields = () => {
    switch (enrollmentSteps[enrollmentStep].key) {
      case 'student':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {renderTextField('studentName', 'Nome')}
            {renderTextField('birthDate', 'Data nascimento', 'date')}
            <label className="text-sm font-semibold text-slate-700">
              Sexo
              <select
                value={enrollmentForm.gender ?? ''}
                onChange={(event) => updateEnrollmentField('gender', event.target.value)}
                className={fieldClass}
              >
                <option value="">Selecionar</option>
                <option value="feminino">Feminino</option>
                <option value="masculino">Masculino</option>
              </select>
            </label>
            {renderTextField('studentBi', 'BI', 'text', '000000000AA000')}
            {renderTextField('studentNif', 'NIF', 'text', 'Opcional', false)}
          </div>
        );
      case 'guardian':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {renderTextField('guardianName', 'Nome')}
            <label className="text-sm font-semibold text-slate-700">
              Parentesco
              <select
                value={enrollmentForm.relationship ?? ''}
                onChange={(event) => updateEnrollmentField('relationship', event.target.value)}
                className={fieldClass}
              >
                <option value="">Selecionar</option>
                <option value="mae">Mãe</option>
                <option value="pai">Pai</option>
                <option value="tutor">Tutor</option>
                <option value="outro">Outro</option>
              </select>
            </label>
            {renderTextField('guardianPhone', 'Telefone', 'tel')}
            {renderTextField('guardianEmail', 'Email', 'email', 'Opcional', false)}
            <label className="text-sm font-semibold text-slate-700 md:col-span-2">
              Morada
              <input
                value={enrollmentForm.guardianAddress ?? ''}
                onChange={(event) => updateEnrollmentField('guardianAddress', event.target.value)}
                className={fieldClass}
              />
            </label>
          </div>
        );
      case 'school':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {renderTextField('schoolSearch', 'Pesquisar escola', 'search', 'Nome, bairro ou município')}
            {renderReadOnlyField('Vagas', enrollmentForm.schoolSearch ? 'A validar' : 'Selecione escola')}
            {renderReadOnlyField('Distância', enrollmentForm.schoolSearch ? 'A calcular' : 'Selecione escola')}
            <label className="text-sm font-semibold text-slate-700">
              Turno
              <select
                value={enrollmentForm.shift ?? 'manha'}
                onChange={(event) => updateEnrollmentField('shift', event.target.value)}
                className={fieldClass}
              >
                <option value="manha">Manhã</option>
                <option value="tarde">Tarde</option>
                <option value="noite">Noite</option>
              </select>
            </label>
            {renderReadOnlyField('Propina', 'A confirmar pela escola')}
          </div>
        );
      case 'documents':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {['BI estudante', 'BI encarregado', 'Fotografia', 'Certificado anterior', 'Boletim anterior'].map(
              (label) => (
                <button
                  key={label}
                  type="button"
                  onClick={handleAttachDocs}
                  className="flex min-h-14 items-center justify-between rounded-lg border border-slate-200 px-4 py-3 text-left text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  <span>{label}</span>
                  <UploadCloud className="h-4 w-4 text-slate-500" />
                </button>
              )
            )}
          </div>
        );
      case 'validation':
        return (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {renderReadOnlyField('Elegível', 'Validação interna')}
            {renderReadOnlyField('Há vagas', 'Validação interna')}
            {renderReadOnlyField('Conflitos', 'Validação interna')}
          </div>
        );
      case 'payment':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="text-sm font-semibold text-slate-700">
              Método
              <select
                value={enrollmentForm.paymentMethod ?? 'referencia'}
                onChange={(event) => updateEnrollmentField('paymentMethod', event.target.value)}
                className={fieldClass}
              >
                <option value="referencia">Referência</option>
                <option value="multicaixa">Multicaixa</option>
                <option value="wallet">Wallet</option>
              </select>
            </label>
            {renderReadOnlyField('Referência', 'Gerada na submissão')}
          </div>
        );
      default:
        return (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {renderReadOnlyField('Número matrícula', 'Gerado após aprovação')}
            {renderReadOnlyField('Comprovativo', 'Disponível no FUC')}
            {renderReadOnlyField('QR', 'Gerado no comprovativo')}
          </div>
        );
    }
  };

  const renderEnrollmentWizard = () => (
    <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-6">
      <div className="flex items-start gap-3">
        <div className="p-3 rounded-xl bg-teal-600">
          <School className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Nova Matrícula Escolar</h1>
          <p className="text-slate-500 text-sm">Matrícula híbrida com validação interna</p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
        {enrollmentSteps.map((step, index) => {
          const StepIcon = step.icon;
          const isActive = index === enrollmentStep;
          const isDone = index < enrollmentStep;
          return (
            <button
              key={step.key}
              type="button"
              onClick={() => setEnrollmentStep(index)}
              className={`min-h-16 rounded-lg border px-2 py-2 text-xs font-semibold ${
                isActive
                  ? 'border-teal-600 bg-teal-50 text-teal-800'
                  : isDone
                    ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              <StepIcon className="mx-auto mb-1 h-4 w-4" />
              {step.title}
            </button>
          );
        })}
      </div>

      <div className="mt-6">{renderEnrollmentStepFields()}</div>

      <div className="mt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <button
          type="button"
          onClick={() => setEnrollmentStep((step) => Math.max(0, step - 1))}
          disabled={enrollmentStep === 0}
          className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          Anterior
        </button>
        <button
          type="button"
          onClick={() =>
            setEnrollmentStep((step) => Math.min(enrollmentSteps.length - 1, step + 1))
          }
          disabled={enrollmentStep === enrollmentSteps.length - 1}
          className="rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900"
          >
            <ArrowLeft className="h-4 w-4" />
            Voltar
          </button>
          <span className="text-xs text-slate-400">Pedido #{orderId ?? 'gerando...'}</span>
        </div>
      </div>

      <CitizenAreaBanner />

      <div className="max-w-5xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {isEnrollmentWizard ? (
            renderEnrollmentWizard()
          ) : (
            <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-6">
              <div className="flex items-start gap-3">
                <div className="p-3 rounded-xl bg-blue-600">
                  <ClipboardList className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-slate-900">{config.title}</h1>
                  <p className="text-slate-500 text-sm">{config.subtitle}</p>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                <label className="text-sm font-semibold text-slate-700">
                  Tipo de Pedido
                  <select
                    value={requestType}
                    onChange={(event) => setRequestType(event.target.value)}
                    className={fieldClass}
                  >
                    {typeOptions.map((type) => (
                      <option key={type} value={type}>
                        {type.replace('_', ' ').toUpperCase()}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="text-sm font-semibold text-slate-700">
                  Entrega
                  <select
                    value={delivery}
                    onChange={(event) => setDelivery(event.target.value)}
                    className={fieldClass}
                  >
                    <option value="digital">Digital (FUC)</option>
                    <option value="presencial">Presencial</option>
                    <option value="expresso">Expresso</option>
                  </select>
                </label>
                <label className="text-sm font-semibold text-slate-700 md:col-span-2">
                  Observações
                  <textarea
                    value={notes}
                    onChange={(event) => setNotes(event.target.value)}
                    rows={4}
                    className={fieldClass}
                    placeholder="Indique detalhes adicionais para agilizar o pedido."
                  />
                </label>
              </div>
            </div>
          )}

          <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Próximos Passos</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={handleAttachDocs}
                className="flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              >
                <UploadCloud className="h-4 w-4" />
                Anexar documentos
              </button>
              {config.showBiometrics && (
                <button
                  onClick={handleBiometrics}
                  className="flex items-center justify-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-4 py-3 text-sm font-semibold text-blue-700 hover:bg-blue-100"
                >
                  <Fingerprint className="h-4 w-4" />
                  Iniciar biometria
                </button>
              )}
              <button
                onClick={handleSubmit}
                disabled={!orderId || isSubmitting}
                className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-60"
              >
                {isSubmitting ? 'Submetendo...' : 'Submeter e pagar'}
              </button>
            </div>
            {error && (
              <div className="mt-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {error}
              </div>
            )}
            {isCreating && (
              <div className="mt-4 text-xs text-slate-500">A abrir pedido no sistema...</div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-2xl shadow-md border border-slate-200 p-6">
            <h3 className="text-sm font-semibold text-slate-500 uppercase mb-4">Resumo</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-slate-700">
                <span>Serviço</span>
                <span className="font-semibold">{config.title}</span>
              </div>
              <div className="flex justify-between text-slate-700">
                <span>Tipo</span>
                <span className="font-semibold">
                  {isEnrollmentWizard ? 'NOVA MATRÍCULA' : requestType.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between text-slate-700">
                <span>Entrega</span>
                <span className="font-semibold">{delivery.toUpperCase()}</span>
              </div>
              <div className="flex justify-between text-slate-900 font-bold text-lg">
                <span>Taxa estimada</span>
                <span>{formatCurrency(config.price)}</span>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6">
            <div className="flex items-center gap-2 text-blue-900 font-semibold mb-3">
              <CreditCard className="h-4 w-4" />
              Pagamento pré-selecionado
            </div>
            <p className="text-sm text-blue-800">
              Após submeter o pedido, a referência Multicaixa será gerada automaticamente para este serviço.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceRequestPage;
