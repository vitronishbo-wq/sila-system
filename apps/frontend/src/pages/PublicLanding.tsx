
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ASSETS, ESSENTIAL_SERVICES, APP_VERSION } from '../constants';
import { Building2, Search, ArrowRight, Shield, Zap, Users } from 'lucide-react';

const PublicLanding: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeService, setActiveService] = useState<string | null>(null);

  const handleServiceClick = (serviceId: string) => {
    setActiveService(serviceId);
    const token = localStorage.getItem('token');
    if (token) {
      if (serviceId === 'identity') navigate('/admin/citizens');
      else if (serviceId === 'registry') navigate('/admin/documents');
      else navigate('/admin');
    } else {
      navigate(`/login?service=${serviceId}`);
    }
  };

  const filteredServices = ESSENTIAL_SERVICES.filter(s =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Header Navigation */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity hover:-translate-y-0.5"
            title="Voltar ao início"
          >
            <Building2 className="w-8 h-8 text-blue-600" />
            <div>
              <div className="text-xl font-bold text-slate-900">SILA System</div>
              <div className="text-xs text-slate-500">Administração Local Integrada</div>
            </div>
          </button>

          <nav className="hidden md:flex gap-8">
            <button
              onClick={() => document.getElementById('services')?.scrollIntoView({ behavior: 'smooth' })}
              className="text-slate-600 hover:text-blue-600 transition-colors font-medium hover:underline"
              title="Ver serviços disponíveis"
            >
              Serviços
            </button>
            <button
              onClick={() => document.getElementById('benefits')?.scrollIntoView({ behavior: 'smooth' })}
              className="text-slate-600 hover:text-blue-600 transition-colors font-medium hover:underline"
              title="Conhecer os benefícios"
            >
              Benefícios
            </button>
            <button
              onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
              className="text-slate-600 hover:text-blue-600 transition-colors font-medium hover:underline"
              title="Saber mais sobre SILA"
            >
              Sobre
            </button>
          </nav>

          <div className="flex gap-3">
            <button
              onClick={() => navigate('/citizen/login')}
              className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 transition-all font-medium hover:border-slate-400 active:scale-95"
              title="Aceder como cidadão"
            >
              FUC Cidadão
            </button>
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 transition-all font-medium hover:border-slate-400 active:scale-95"
              title="Entrar na sua conta"
            >
              Admin
            </button>
            <button
              onClick={() => navigate('/register')}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-all font-medium active:scale-95 shadow-md hover:shadow-lg hover:-translate-y-0.5"
              title="Criar uma nova conta"
            >
              Registar
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 lg:py-24 px-6">
        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div>
            <h1 className="text-4xl lg:text-6xl font-extrabold text-slate-900 mb-6 leading-tight">
              Administração <span className="text-blue-600">mais próxima</span> de si
            </h1>
            <p className="text-xl text-slate-600 mb-8 leading-relaxed">
              Aceda aos serviços públicos de forma rápida, segura e sem burocracia desnecessária.
              Tudo o que precisa num único lugar.
            </p>

            {/* Search Bar */}
            <div className="relative mb-8">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="O que deseja tratar hoje?"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 rounded-lg border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all focus:outline-none"
                  title="Pesquisar serviços"
                />
              </div>

              {/* Search Results Dropdown */}
              {searchQuery && filteredServices.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-slate-200 rounded-lg shadow-lg z-10 max-h-64 overflow-y-auto">
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
                      <ArrowRight className="w-4 h-4 ml-auto text-slate-400" />
                    </button>
                  ))}
                </div>
              )}

              {searchQuery && filteredServices.length === 0 && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-slate-200 rounded-lg shadow-lg p-4 z-10 text-center text-slate-500 text-sm">
                  Nenhum serviço encontrado para "{searchQuery}"
                </div>
              )}
            </div>

            {/* CTA Buttons */}
            <div className="flex gap-4 flex-wrap">
              <button
                onClick={() => navigate('/citizen/login')}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all active:scale-95 shadow-md hover:shadow-lg hover:-translate-y-0.5 flex items-center gap-2 group"
                title="Aceder como cidadão"
              >
                Aceder como Cidadão
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => document.getElementById('services')?.scrollIntoView({ behavior: 'smooth' })}
                className="px-6 py-3 bg-slate-200 text-slate-900 rounded-lg font-semibold hover:bg-slate-300 transition-all active:scale-95"
                title="Ver todos os serviços"
              >
                Ver Serviços
              </button>
            </div>
          </div>

          {/* Right Image */}
          <div className="hidden lg:block">
            <button
              onClick={() => navigate('/citizen/login')}
              className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-2xl p-8 text-white shadow-xl aspect-square flex flex-col items-center justify-center text-center cursor-pointer hover:shadow-2xl hover:-translate-y-2 transition-all group"
              title="Clique para acessar como cidadão"
            >
              <Building2 className="w-20 h-20 mb-4 group-hover:scale-110 transition-transform" />
              <h3 className="text-2xl font-bold mb-4">Governo Digital</h3>
              <p className="text-blue-100">Transformando a administração pública com tecnologia moderna</p>
            </button>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-16 lg:py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">Serviços Disponíveis</h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Aceda a todos os serviços públicos integrados num único portal
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {(searchQuery ? filteredServices : ESSENTIAL_SERVICES).map((service) => (
              <button
                key={service.id}
                onClick={() => handleServiceClick(service.id)}
                className={`bg-white border-2 rounded-xl p-6 shadow-md hover:shadow-2xl hover:border-blue-400 hover:-translate-y-2 transition-all cursor-pointer group flex flex-col items-center text-center aspect-square justify-center ${
                  activeService === service.id ? 'ring-2 ring-blue-500 border-blue-500' : 'border-slate-200'
                }`}
                title={`Clique para acessar ${service.name}`}
              >
                <div className={`w-12 h-12 rounded-xl ${service.color} text-white flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-md`}>
                  <i className={`fa-solid ${service.icon} text-lg`}></i>
                </div>
                <h4 className="font-semibold text-slate-700 text-sm leading-tight group-hover:text-blue-600 transition-colors">
                  {service.name}
                </h4>
              </button>
            ))}
          </div>

          {searchQuery && filteredServices.length === 0 && (
            <div className="text-center py-12">
              <p className="text-slate-600 text-lg">Nenhum serviço encontrado para "{searchQuery}"</p>
              <button
                onClick={() => setSearchQuery('')}
                className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all active:scale-95"
              >
                Limpar Pesquisa
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-16 lg:py-24 px-6 bg-slate-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-slate-900 mb-12 text-center">Por Que Usar SILA?</h2>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: 'Rápido',
                description: 'Processos ágeis e automatizados para economia de tempo',
              },
              {
                icon: Shield,
                title: 'Seguro',
                description: 'Encriptação de ponta a ponta e conformidade RGPD',
              },
              {
                icon: Users,
                title: 'Acessível',
                description: 'Interface intuitiva para todos os cidadãos',
              },
            ].map((benefit, idx) => (
              <button
                key={idx}
                onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                className="bg-white rounded-xl p-8 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all active:scale-95 cursor-pointer group"
                title={`Clique para saber mais sobre ${benefit.title}`}
              >
                <benefit.icon className="w-12 h-12 text-blue-600 mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-xl font-bold text-slate-900 mb-2">{benefit.title}</h3>
                <p className="text-slate-600">{benefit.description}</p>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 lg:py-24 px-6 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-slate-900 mb-6">Sobre o SILA System</h2>
          <p className="text-xl text-slate-600 mb-8">
            O Sistema de Administração Local Integrada (SILA) é uma plataforma desenvolvida para 
            modernizar a administração pública, trazendo os serviços públicos mais perto dos cidadãos 
            em todo o país.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <button
              onClick={() => navigate('/login')}
              className="bg-blue-600 text-white rounded-lg p-6 hover:bg-blue-700 transition-all active:scale-95 shadow-md hover:shadow-lg cursor-pointer group"
              title="Entrar no painel administrativo"
            >
              <h3 className="font-bold text-lg mb-2 group-hover:text-blue-100">Painel Administrativo</h3>
              <p className="text-blue-100">Gerir serviços e utilizadores</p>
            </button>
            <button
              onClick={() => navigate('/register')}
              className="bg-slate-200 text-slate-900 rounded-lg p-6 hover:bg-slate-300 transition-all active:scale-95 shadow-md hover:shadow-lg cursor-pointer group"
              title="Registar uma nova conta"
            >
              <h3 className="font-bold text-lg mb-2 group-hover:text-blue-600">Criar Conta</h3>
              <p className="text-slate-600">Junte-se à comunidade SILA</p>
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300 py-8 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-bold text-white mb-4 flex items-center gap-2">
                <Building2 className="w-5 h-5" />
                SILA System
              </h4>
              <p className="text-sm text-slate-400">Administração digital para todos</p>
            </div>

            <div>
              <h5 className="font-bold text-white mb-4">Serviços</h5>
              <ul className="space-y-2 text-sm">
                {ESSENTIAL_SERVICES.slice(0, 3).map(s => (
                  <li key={s.id}>
                    <button
                      onClick={() => handleServiceClick(s.id)}
                      className="text-slate-300 hover:text-white transition-colors hover:underline cursor-pointer"
                      title={`Aceder a ${s.name}`}
                    >
                      {s.name}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h5 className="font-bold text-white mb-4">Conta</h5>
              <ul className="space-y-2 text-sm">
                <li>
                  <button
                    onClick={() => navigate('/login')}
                    className="text-slate-300 hover:text-white transition-colors hover:underline cursor-pointer"
                    title="Fazer login"
                  >
                    Entrar
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => navigate('/register')}
                    className="text-slate-300 hover:text-white transition-colors hover:underline cursor-pointer"
                    title="Registar conta nova"
                  >
                    Registar
                  </button>
                </li>
              </ul>
            </div>

            <div>
              <h5 className="font-bold text-white mb-4">Suporte</h5>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="mailto:support@sila.gov.pt" className="text-slate-300 hover:text-white transition-colors hover:underline" title="Enviar email de suporte">
                    support@sila.gov.pt
                  </a>
                </li>
                <li>
                  <a href="tel:+2441407000" className="text-slate-300 hover:text-white transition-colors hover:underline" title="Ligar para suporte">
                    +244 140 7000
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-800 pt-8 flex justify-between items-center text-sm text-slate-400">
            <p>&copy; 2026 Ministério da Administração do Território. Todos os direitos reservados.</p>
            <div className="flex gap-4">
              <button className="hover:text-white transition-colors cursor-pointer" title="Ver privacidade">
                Privacidade
              </button>
              <button className="hover:text-white transition-colors cursor-pointer" title="Ver termos">
                Termos
              </button>
              <span className="text-slate-600">v{APP_VERSION}</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PublicLanding;