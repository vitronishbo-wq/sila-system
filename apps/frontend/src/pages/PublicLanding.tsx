
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ESSENTIAL_SERVICES, APP_VERSION } from '@/constants';
import { APP_IMAGES } from '@/constants/images';
import { Search, Star } from 'lucide-react';

const normalizeSearchText = (value: string) =>
  value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();

const PublicLanding: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeService, setActiveService] = useState<string | null>(null);

  const handleServiceClick = (serviceId: string) => {
    setActiveService(serviceId);
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    const parsedUser = storedUser ? JSON.parse(storedUser) : null;
    const role = parsedUser?.role;
    const citizenRoutes: Record<string, string> = {
      identity: '/citizen/services/identity',
      registry: '/citizen/services/registry',
      tax: '/citizen/services/tax',
      water: '/citizen/services/water',
      energy: '/citizen/services/energy',
      educacao: '/citizen/services/educacao',
      employment: '/citizen/services/employment',
      licensing: '/citizen/services/licensing',
      transport: '/citizen/services/transport',
      notaries: '/citizen/services/notaries'
    };
    if (token) {
      if (role === 'CITIZEN') {
        const route = citizenRoutes[serviceId] || `/citizen/portal?service=${serviceId}`;
        navigate(route);
        return;
      }
      if (serviceId === 'identity') navigate('/admin/citizens');
      else if (serviceId === 'registry') navigate('/admin/documents');
      else navigate('/admin');
    } else {
      localStorage.setItem('selected_service', serviceId);
      navigate(`/citizen/login?service=${serviceId}`);
    }
  };

  const normalizedQuery = normalizeSearchText(searchQuery);
  const filteredServices = ESSENTIAL_SERVICES.filter((service) => {
    const haystack = normalizeSearchText(`${service.name} ${service.id}`);
    return haystack.includes(normalizedQuery);
  });

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="min-h-screen grid lg:grid-cols-[1.1fr_1fr]">
        <section className="relative min-h-[60vh] lg:min-h-screen">
          <div className="absolute inset-0">
            <img
              src={APP_IMAGES.LOGIN_HERO}
              alt="SILA System"
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-slate-950/80 via-slate-900/70 to-slate-950/90" />
          </div>

          <div className="relative z-10 h-full flex flex-col p-8 lg:p-12 text-white">
            <div className="flex items-center gap-3">
              <img
                src={APP_IMAGES.LOGO}
                alt="Brasão da República de Angola"
                className="h-10 w-10 object-contain"
              />
              <div>
                <div className="text-lg font-semibold">SILA-System</div>
                <div className="text-xs text-slate-200">Integrated Local Administration System</div>
              </div>
            </div>

            <div className="mt-auto max-w-xl space-y-6">
              <h1 className="text-3xl lg:text-5xl font-bold leading-tight">
                Administração <span className="text-yellow-400">mais próxima de si.</span>
              </h1>
              <p className="text-slate-200 text-base lg:text-lg">
                Aceda aos serviços públicos de forma rápida, segura e sem burocracia.
              </p>

              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="O que deseja tratar hoje?"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 rounded-full border border-white/30 bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-yellow-300/40"
                  title="Pesquisar serviços"
                />

                {searchQuery && filteredServices.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-slate-200 rounded-xl shadow-lg z-10 max-h-64 overflow-y-auto">
                    {filteredServices.map(service => (
                      <button
                        key={service.id}
                        onClick={() => {
                          setSearchQuery('');
                          handleServiceClick(service.id);
                        }}
                        className="w-full text-left px-4 py-3 hover:bg-blue-50 transition-colors flex items-center gap-3 border-b border-slate-100 last:border-b-0 active:bg-blue-100"
                        title={`Aceder a ${service.name}`}
                      >
                        <i className={`fa-solid ${service.icon} text-blue-600`}></i>
                        <span className="font-medium text-slate-700">{service.name}</span>
                      </button>
                    ))}
                  </div>
                )}

                {searchQuery && filteredServices.length === 0 && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-slate-200 rounded-xl shadow-lg p-4 z-10 text-center text-slate-500 text-sm">
                    Nenhum serviço encontrado para "{searchQuery}"
                  </div>
                )}
              </div>
            </div>

            <div className="mt-10 flex items-center gap-6 text-xs text-slate-300">
              <button className="hover:text-white transition-colors" title="Ajuda">
                Ajuda
              </button>
              <button className="hover:text-white transition-colors" title="Contactos">
                Contactos
              </button>
              <span className="text-slate-400">v{APP_VERSION}</span>
            </div>
          </div>
        </section>

        <section className="bg-slate-50 min-h-screen">
          <div className="h-full flex flex-col p-8 lg:p-10">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-yellow-100 text-yellow-600 flex items-center justify-center">
                  <Star className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-lg font-semibold text-slate-800">Serviços Essenciais</div>
                  <div className="text-sm text-slate-500">Cidadão e Administração</div>
                </div>
              </div>

              <div className="flex flex-wrap gap-4 items-start">
                <div className="flex flex-col items-start">
                  <button
                    onClick={() => navigate('/citizen/login')}
                    className="px-4 py-2 rounded-full border border-slate-300 text-slate-700 hover:bg-slate-100 transition-all font-medium active:scale-95"
                    title="Aceder como cidadão"
                  >
                    Entrar como Cidadão
                  </button>
                  <span className="text-xs text-slate-500 mt-1">Portal de Serviços</span>
                </div>
                <div className="flex flex-col items-start">
                  <button
                    onClick={() => navigate('/login')}
                    className="px-4 py-2 rounded-full border border-slate-300 text-slate-700 hover:bg-slate-100 transition-all font-medium active:scale-95"
                    title="Entrar no painel administrativo"
                  >
                    Entrar como Admin
                  </button>
                  <span className="text-xs text-slate-500 mt-1">Painel Administrativo</span>
                </div>
                <button
                  onClick={() => navigate('/register')}
                  className="px-4 py-2 rounded-full bg-slate-900 text-white hover:bg-slate-800 transition-all font-medium active:scale-95"
                  title="Criar uma nova conta"
                >
                  Criar Conta
                </button>
              </div>
            </div>

            <div className="mt-8 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
              {(searchQuery ? filteredServices : ESSENTIAL_SERVICES).map((service) => (
                <button
                  key={service.id}
                  onClick={() => handleServiceClick(service.id)}
                  className={`bg-white border rounded-2xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer group flex flex-col items-center text-center justify-center ${
                    activeService === service.id ? 'ring-2 ring-blue-500 border-blue-400' : 'border-slate-200'
                  }`}
                  title={`Clique para acessar ${service.name}`}
                >
                  <div className={`w-12 h-12 rounded-2xl ${service.color} text-white flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-md`}>
                    <i className={`fa-solid ${service.icon} text-lg`}></i>
                  </div>
                  <h4 className="font-semibold text-slate-700 text-sm leading-tight group-hover:text-blue-600 transition-colors">
                    {service.name}
                  </h4>
                </button>
              ))}
            </div>

            <div className="mt-auto pt-8 text-center text-xs text-slate-400">
              © 2026 Ministério da Administração do Território
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default PublicLanding;
