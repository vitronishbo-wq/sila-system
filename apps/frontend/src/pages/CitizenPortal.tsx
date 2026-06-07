import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { citizenAuthService } from '@/services/citizenAuthService';
import { ESSENTIAL_SERVICES, API_URL } from '@/constants';
import { estimateBusinessDays } from '@/utils/businessDays';

const normalizeSearchText = (value: string) =>
  value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();

interface CitizenProfile {
  id: string;
  full_name: string;
  birth_date?: string | null;
  gender?: string | null;
  vital_status?: string | null;
  id_number?: string | null;
  nif?: string | null;
}

interface CitizenPortalProps {
  onLogout: () => void;
}

interface CatalogService {
  id?: string;
  code?: string;
  name: string;
  description?: string;
  price?: number;
  sla_hours?: number | null;
  sla_days?: number | null;
  category?: string;
}

interface CatalogModule {
  module: string;
  name: string;
  description?: string;
  ui?: {
    icon?: string;
    color?: string;
    order?: number;
  };
  services: CatalogService[];
}

const CitizenPortal: React.FC<CitizenPortalProps> = ({ onLogout }) => {
  const [profile, setProfile] = useState<CitizenProfile | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'profile' | 'events' | 'services'>('services');
  const navigate = useNavigate();
  const [catalogModules, setCatalogModules] = useState<CatalogModule[]>([]);
  const [catalogQuery, setCatalogQuery] = useState('');
  const [catalogLoading, setCatalogLoading] = useState(false);
  const [catalogError, setCatalogError] = useState('');
  const [selectedModule, setSelectedModule] = useState<CatalogModule | null>(null);
  const [moduleQuery, setModuleQuery] = useState('');
  const [moduleTypeFilter, setModuleTypeFilter] = useState<string>('all');

  const serviceRoutes: Record<string, string> = {
    identity: '/citizen/services/identity',
    registry: '/citizen/services/registry',
    tax: '/citizen/services/tax',
    water: '/citizen/services/water',
    energy: '/citizen/services/energy',
    educacao: '/citizen/services/educacao',
    education: '/citizen/services/educacao',
    employment: '/citizen/services/employment',
    licensing: '/citizen/services/licensing',
    transport: '/citizen/services/transport',
    notaries: '/citizen/services/notaries'
  };

  useEffect(() => {
    loadCitizenData();
  }, []);

  useEffect(() => {
    const loadCatalog = async () => {
      setCatalogLoading(true);
      setCatalogError('');
      try {
        const token = localStorage.getItem('citizen_token')
          || localStorage.getItem('access_token')
          || localStorage.getItem('token');
        const headers: Record<string, string> = {};
        if (token) headers.Authorization = `Bearer ${token}`;
        const portalResponse = await fetch(`${API_URL}portal/catalog`, { headers });
        if (portalResponse.ok) {
          const data = await portalResponse.json();
          setCatalogModules(Array.isArray(data) ? data : []);
          return;
        }
        const fallbackResponse = await fetch(`${API_URL}service-catalog?limit=1000`, { headers });
        if (!fallbackResponse.ok) {
          throw new Error('Falha ao carregar catalogo');
        }
        const data = await fallbackResponse.json();
        if (Array.isArray(data)) {
          const grouped: Record<string, CatalogModule> = {};
          data.forEach((item: CatalogService) => {
            const moduleKey = (item.category || item.code || 'outros').toLowerCase();
            if (!grouped[moduleKey]) {
              grouped[moduleKey] = {
                module: moduleKey,
                name: moduleKey.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
                services: []
              };
            }
            grouped[moduleKey].services.push(item);
          });
          setCatalogModules(Object.values(grouped));
        } else {
          setCatalogModules([]);
        }
      } catch (err) {
        console.error('Erro ao carregar catalogo:', err);
        setCatalogError('Nao foi possivel carregar o catalogo completo.');
      } finally {
        setCatalogLoading(false);
      }
    };

    loadCatalog();
  }, []);

  const loadCitizenData = async () => {
    setIsLoading(true);
    try {
      const [profileData, eventsData] = await Promise.all([
        citizenAuthService.getProfile(),
        citizenAuthService.getEvents()
      ]);
      setProfile(profileData);
      setEvents(eventsData);
    } catch (err) {
      console.error('Failed to load citizen data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 mb-4"></div>
          <p className="text-gray-600">A carregar o seu perfil...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <p className="text-red-600 mb-4">Erro ao carregar o perfil</p>
          <button onClick={onLogout} className="px-4 py-2 bg-red-600 text-white rounded">
            Voltar
          </button>
        </div>
      </div>
    );
  }

  const fallbackModules: CatalogModule[] = ESSENTIAL_SERVICES.map((service) => ({
    module: service.id,
    name: service.name,
    description: service.name,
    ui: { icon: service.icon, color: service.color },
    services: [
      {
        id: service.id,
        code: service.id,
        name: service.name,
        description: service.name,
        price: 0
      }
    ]
  }));

  const resolvedModules = catalogModules.length ? catalogModules : fallbackModules;

  const queryValue = normalizeSearchText(catalogQuery.trim());
  const visibleModules = resolvedModules.filter((module) => {
    if (!queryValue) return true;
    const matchesModule = normalizeSearchText(module.name).includes(queryValue)
      || normalizeSearchText(module.module).includes(queryValue);
    const matchesService = module.services.some((service) =>
      normalizeSearchText(service.name).includes(queryValue)
        || normalizeSearchText(service.code || service.id || '').includes(queryValue)
    );
    return matchesModule || matchesService;
  });

  const handleServiceSelect = (service: CatalogService) => {
    const serviceCode = service.code || service.id || '';
    const routeKey = (service.category || selectedModule?.module || serviceCode).toLowerCase();
    const route = serviceRoutes[routeKey];
    if (route) {
      navigate(route);
      return;
    }
    navigate(`/citizen/services/catalog/${encodeURIComponent(serviceCode)}`);
  };

  const formatPrice = (price?: number) => {
    if (!price) return 'Gratuito';
    return `${price.toLocaleString('pt-PT')} Kz`;
  };

  const formatSla = (service: CatalogService) => {
    const totalDays = service.sla_days ?? (service.sla_hours ? service.sla_hours / 24 : null);
    if (totalDays) {
      const businessDays = estimateBusinessDays(totalDays);
      return `${businessDays.toLocaleString('pt-PT')} dia${businessDays === 1 ? '' : 's'} úteis`;
    }
    return null;
  };

  const categoryLabels: Record<string, string> = {
    identity: 'Identidade',
    registry: 'Registo Civil',
    justice: 'Justiça',
    tax: 'Finanças',
    economy: 'Finanças',
    water: 'Água',
    energy: 'Energia',
    employment: 'Emprego',
    society: 'Assistência Social',
    licensing: 'Licenciamento',
    transport: 'Transportes',
    logistics: 'Transportes',
    notaries: 'Notariado',
    saude: 'Saúde',
    educacao: 'Educação',
    education: 'Educação'
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Minha FUC</h1>
            <p className="text-xs uppercase tracking-[0.2em] text-slate-500 font-semibold mt-1">Portal de Serviços</p>
          </div>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold"
            title="Terminar sessão"
          >
            Sair
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-4 flex items-center justify-between">
          <button
            onClick={() => setActiveTab('services')}
            className="inline-flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-2 text-sm font-semibold shadow-sm hover:bg-slate-800 transition"
            title="Aceder aos serviços"
          >
            ⭐ Serviços
            <span className="inline-flex items-center rounded-full bg-amber-300 text-slate-900 text-[10px] font-bold px-2 py-0.5 uppercase">
              Novo
            </span>
          </button>
          <span className="text-xs text-slate-500">Escolha um serviço para iniciar o pedido</span>
        </div>

        {/* Navegação de abas */}
        <div className="flex border-b mb-8 bg-white rounded-t-lg">
          <button
            onClick={() => setActiveTab('services')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'services'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-cursor-pointer hover:text-gray-900'
            }`}
            title="Ver serviços disponíveis"
          >
            ⭐ Serviços
          </button>
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'profile'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-cursor-pointer hover:text-gray-900'
            }`}
            title="Ver informações pessoais"
          >
            👤 Perfil
          </button>
          <button
            onClick={() => setActiveTab('events')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'events'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-cursor-pointer hover:text-gray-900'
            }`}
            title="Ver eventos e atividades"
          >
            📋 Eventos
          </button>
        </div>

        {/* Conteúdo */}
        {activeTab === 'services' && (
          <div className="bg-white rounded-lg shadow p-8">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
              <div>
                <h2 className="text-2xl font-bold">Catalogo de Servicos</h2>
                <p className="text-sm text-slate-500">Escolha um servico para iniciar o formulario.</p>
              </div>
              <div className="relative">
                <input
                  value={catalogQuery}
                  onChange={(event) => setCatalogQuery(event.target.value)}
                  placeholder="Pesquisar servicos..."
                  className="w-full lg:w-72 px-4 py-2 rounded-full border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {catalogLoading && (
              <div className="text-sm text-slate-500">A carregar catalogo...</div>
            )}
            {catalogError && (
              <div className="text-sm text-red-600 mb-4">{catalogError}</div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {visibleModules.map((module) => {
                const ui = module.ui ?? {};
                const color = ui.color ?? '#334155';
                const icon = ui.icon ?? 'fa-layer-group';
                const servicesCount = module.services.length;
                return (
                  <button
                    key={module.module}
                    onClick={() => {
                      setSelectedModule(module);
                      setModuleQuery('');
                      setModuleTypeFilter('all');
                    }}
                    className="border border-slate-200 rounded-2xl p-6 text-left hover:shadow-lg hover:-translate-y-1 transition-all bg-slate-50"
                    title={`Abrir ${module.name}`}
                  >
                    <div
                      className="w-12 h-12 rounded-2xl text-white flex items-center justify-center mb-4"
                      style={{ backgroundColor: color }}
                    >
                      <i className={`fa-solid ${icon} text-lg`}></i>
                    </div>
                    <p className="font-semibold text-slate-800">{module.name}</p>
                    <p className="text-xs text-slate-500 mt-2">
                      {module.description || `${servicesCount} servico${servicesCount === 1 ? '' : 's'} disponivel${servicesCount === 1 ? '' : 'is'}`}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {selectedModule && (
          <div className="fixed inset-0 z-50">
            <div
              className="absolute inset-0 bg-slate-900/60"
              onClick={() => setSelectedModule(null)}
            />
            <div className="absolute right-0 top-0 h-full w-full sm:w-[440px] bg-white shadow-2xl flex flex-col">
              <div className="p-6 border-b">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-slate-500 font-semibold">Modulo</p>
                    <h3 className="text-2xl font-bold text-slate-900">{selectedModule.name}</h3>
                    {selectedModule.description && (
                      <p className="text-sm text-slate-500 mt-1">{selectedModule.description}</p>
                    )}
                  </div>
                  <button
                    onClick={() => setSelectedModule(null)}
                    className="text-slate-500 hover:text-slate-900 text-sm font-semibold"
                  >
                    Fechar
                  </button>
                </div>

                <div className="flex flex-col gap-3">
                  <input
                    value={moduleQuery}
                    onChange={(event) => setModuleQuery(event.target.value)}
                    placeholder="Pesquisar servicos..."
                    className="w-full px-4 py-2 rounded-full border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="flex flex-wrap gap-2">
                    {['all', ...Array.from(new Set(selectedModule.services.map((service) => (service.category || selectedModule.module))))].map((type) => (
                      <button
                        key={type}
                        onClick={() => setModuleTypeFilter(type)}
                        className={`px-3 py-1 rounded-full text-xs font-semibold border ${
                          moduleTypeFilter === type
                            ? 'bg-slate-900 text-white border-slate-900'
                            : 'bg-white text-slate-600 border-slate-200'
                        }`}
                      >
                        {type === 'all' ? 'Todos' : (categoryLabels[type] || type)}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {selectedModule.services
                  .filter((service) => {
                    if (moduleTypeFilter !== 'all') {
                      const serviceType = service.category || selectedModule.module;
                      if (serviceType !== moduleTypeFilter) {
                        return false;
                      }
                    }
                    if (!moduleQuery.trim()) return true;
                    const value = moduleQuery.trim().toLowerCase();
                    return service.name.toLowerCase().includes(value)
                      || (service.code || service.id || '').toLowerCase().includes(value);
                  })
                  .map((service) => {
                    const code = service.code || service.id || '';
                    const slaLabel = formatSla(service);
                    return (
                      <button
                        key={code}
                        onClick={() => handleServiceSelect(service)}
                        className="w-full border border-slate-200 rounded-xl p-4 text-left hover:border-blue-500 hover:shadow transition-all"
                      >
                        <div className="flex items-center justify-between">
                          <p className="font-semibold text-slate-800">{service.name}</p>
                          <span className="text-xs font-semibold text-slate-500">{formatPrice(service.price)}</span>
                        </div>
                        {service.description && (
                          <p className="text-xs text-slate-500 mt-1">{service.description}</p>
                        )}
                        {slaLabel && (
                          <p className="text-xs text-blue-600 mt-2">SLA: {slaLabel}</p>
                        )}
                      </button>
                    );
                  })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Dados Pessoais</h2>
            <div className="grid grid-cols-2 gap-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nome Completo</label>
                <p className="text-lg">{profile.full_name || 'Não informado'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data de Nascimento</label>
                <p className="text-lg">
                  {profile.birth_date ? new Date(profile.birth_date).toLocaleDateString('pt-PT') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Género</label>
                <p className="text-lg">
                  {profile.gender ? (profile.gender === 'M' ? 'Masculino' : 'Feminino') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Estado Civil</label>
                <p className="text-lg">
                  {profile.vital_status ? (profile.vital_status === 'ALIVE' ? 'Vivo' : 'Falecido') : 'Não informado'}
                </p>
              </div>
              {profile.id_number && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Número BI</label>
                  <p className="text-lg">{profile.id_number}</p>
                </div>
              )}
              {profile.nif && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">NIF</label>
                  <p className="text-lg">{profile.nif}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'events' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Histórico de Eventos</h2>
            {events.length === 0 ? (
              <p className="text-gray-500">Nenhum evento registado</p>
            ) : (
              <div className="space-y-4">
                {events.map((event: any) => {
                  const dateValue = event?.created_at ? new Date(event.created_at) : null;
                  const dateLabel = dateValue && !Number.isNaN(dateValue.getTime())
                    ? dateValue.toLocaleString('pt-PT')
                    : 'Data não informada';
                  const message = event?.payload?.message;
                  return (
                  <div key={event.id} className="border-l-4 border-slate-900 pl-4 py-2">
                    <p className="font-semibold">{event.event_type}</p>
                    {message && <p className="text-sm text-gray-700">{message}</p>}
                    <p className="text-sm text-gray-600">{dateLabel}</p>
                  </div>
                )})}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default CitizenPortal;
