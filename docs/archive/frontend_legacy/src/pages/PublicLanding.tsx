import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IMAGES, ESSENTIAL_SERVICES, APP_VERSION } from '../constants';
import { Search, ArrowRight, Shield, Zap, Users } from 'lucide-react';

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

  const filteredServices = ESSENTIAL_SERVICES.filter((service) =>
    service.name.toLowerCase().includes(searchQuery.toLowerCase()),
  );

  const visibleServices = searchQuery ? filteredServices : ESSENTIAL_SERVICES;

  return (
    <div className="min-h-screen bg-[#eef1f5] text-slate-900">
      <section className="min-h-screen grid lg:grid-cols-[1.02fr_1.28fr]">
        <aside className="relative min-h-[52vh] lg:min-h-screen overflow-hidden">
          <img
            src={IMAGES.DASHBOARD.HERO}
            alt="SILA Hero"
            className="absolute inset-0 w-full h-full object-cover object-[58%_40%] sm:object-[60%_40%] md:object-[62%_41%] lg:object-[64%_42%] xl:object-[66%_42%] scale-[1.08] blur-[0.6px] brightness-[0.84] saturate-[0.82]"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-[#071332]/86 via-[#071332]/80 to-[#050d22]/96" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_24%_27%,rgba(254,202,28,0.1),transparent_34%)]" />
          <div className="absolute inset-0 bg-gradient-to-r from-[#030a1e]/34 via-transparent to-[#030a1e]/8" />

          <div className="relative z-10 h-full p-6 md:p-10 lg:p-12 flex flex-col">
            <div className="flex items-center gap-4">
              <img src={IMAGES.BRAND.LOGO} alt="SILA logo" className="h-10 w-auto rounded" />
              <div>
                <p className="text-white text-3xl font-bold leading-none">SILA-System</p>
                <p className="text-slate-300 text-base">Integrated Local Administration System</p>
              </div>
            </div>

            <div className="mt-auto mb-auto pt-14 md:pt-16 lg:pt-10">
              <h1 className="text-white font-black text-5xl md:text-6xl leading-tight tracking-tight">
                Administração
              </h1>
              <h2 className="text-[#facc15] font-black text-5xl md:text-6xl leading-tight tracking-tight">
                mais próxima de si.
              </h2>
              <p className="mt-6 text-slate-200 text-xl md:text-2xl leading-relaxed max-w-xl">
                Aceda aos serviços públicos de forma rápida, segura e sem burocracia.
              </p>

              <div className="relative mt-8 max-w-2xl">
                <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-400" />
                <input
                  type="text"
                  placeholder="O que deseja tratar hoje?"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-16 rounded-2xl border border-white/20 bg-white text-slate-900 pl-14 pr-4 text-lg md:text-xl placeholder:text-slate-400 focus:outline-none focus:ring-4 focus:ring-yellow-400/20 shadow-xl shadow-black/20"
                  title="Pesquisar serviços"
                />
              </div>
            </div>

            <div className="mt-10 flex flex-wrap items-center gap-5 text-slate-300 text-sm">
              <button className="hover:text-white transition-colors" title="Ver ajuda">
                Ajuda
              </button>
              <button className="hover:text-white transition-colors" title="Ver contactos">
                Contactos
              </button>
              <span className="text-slate-400">v{APP_VERSION}</span>
            </div>
          </div>
        </aside>

        <div className="bg-[#f3f5f8] border-l border-slate-200/70">
          <header className="sticky top-0 z-20 border-b border-slate-200/70 bg-[#f3f5f8]/95 backdrop-blur px-5 md:px-8 py-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-yellow-400 text-yellow-950 flex items-center justify-center font-black">
                  ★
                </div>
                <h3 className="text-3xl md:text-4xl font-extrabold text-slate-800 tracking-tight">Serviços Essenciais</h3>
              </div>

              <div className="flex flex-wrap gap-3">
                <button
                  onClick={() => navigate('/citizen/login')}
                  className="h-11 px-6 rounded-2xl border border-slate-300 bg-white text-slate-700 font-semibold hover:-translate-y-0.5 hover:shadow-md active:translate-y-0 transition-all"
                  title="Aceder como cidadão"
                >
                  FUC do Cidadão
                </button>
                <button
                  onClick={() => navigate('/login')}
                  className="h-11 px-6 rounded-2xl border border-slate-300 bg-white text-slate-700 font-semibold hover:-translate-y-0.5 hover:shadow-md active:translate-y-0 transition-all"
                  title="Entrar como admin"
                >
                  Painel Admin
                </button>
                <button
                  onClick={() => navigate('/register')}
                  className="h-11 px-6 rounded-2xl bg-[#081635] text-white font-semibold shadow-lg shadow-slate-900/25 hover:bg-[#0d1f45] hover:-translate-y-0.5 active:translate-y-0 transition-all"
                  title="Criar uma nova conta"
                >
                  Criar Conta
                </button>
              </div>
            </div>
          </header>

          <main className="px-5 md:px-8 py-7">
            <div id="services" className="grid grid-cols-2 xl:grid-cols-4 gap-5">
              {visibleServices.map((service) => (
                <button
                  key={service.id}
                  onClick={() => handleServiceClick(service.id)}
                  className={`group relative bg-white rounded-3xl border p-6 min-h-[205px] flex flex-col items-center justify-center text-center transition-all duration-300 ${
                    activeService === service.id
                      ? 'border-[#15367a] ring-2 ring-[#15367a]/20 shadow-xl'
                      : 'border-slate-200 hover:border-slate-300 hover:shadow-xl hover:-translate-y-1'
                  }`}
                  title={`Aceder a ${service.name}`}
                >
                  <div className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
                  <div
                    className={`w-14 h-14 rounded-2xl ${service.color} text-white flex items-center justify-center mb-4 shadow-md shadow-slate-300 group-hover:scale-110 transition-transform`}
                  >
                    <i className={`fa-solid ${service.icon} text-xl`} />
                  </div>
                  <h4 className="text-xl md:text-2xl font-semibold text-slate-700 leading-snug group-hover:text-slate-900 transition-colors">
                    {service.name}
                  </h4>
                </button>
              ))}
            </div>

            {searchQuery && visibleServices.length === 0 && (
              <div className="rounded-2xl border border-slate-200 bg-white p-7 text-center mt-5">
                <p className="text-slate-600 text-lg">Nenhum serviço encontrado para "{searchQuery}".</p>
                <button
                  onClick={() => setSearchQuery('')}
                  className="mt-4 h-11 px-5 rounded-xl bg-slate-900 text-white font-semibold hover:bg-slate-800 transition-colors"
                >
                  Limpar pesquisa
                </button>
              </div>
            )}
          </main>
        </div>
      </section>

      <section id="benefits" className="px-5 md:px-8 lg:px-12 py-14 border-t border-slate-800 bg-[#081635]">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] font-bold text-slate-300">Plataforma Nacional</p>
              <h2 className="text-4xl md:text-5xl font-black text-white tracking-tight">Por que usar SILA</h2>
            </div>
            <button
              onClick={() => navigate('/login')}
              className="inline-flex items-center gap-2 h-11 px-6 rounded-2xl bg-white text-[#081635] font-semibold hover:bg-slate-100 transition-colors"
            >
              Entrar no sistema
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-5">
            {[
              {
                icon: Zap,
                title: 'Processo Ágil',
                description: 'Fluxos simplificados para reduzir filas e tempo de resposta.',
              },
              {
                icon: Shield,
                title: 'Confiança Digital',
                description: 'Camadas de segurança e rastreabilidade ponta a ponta.',
              },
              {
                icon: Users,
                title: 'Experiência Humana',
                description: 'Desenho orientado ao cidadão, com acesso claro e direto.',
              },
            ].map((item) => (
              <div key={item.title} className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-sm p-7 hover:bg-white/10 transition-colors">
                <item.icon className="w-11 h-11 text-[#facc15] mb-4" />
                <h3 className="text-2xl font-bold text-white mb-2">{item.title}</h3>
                <p className="text-slate-200 text-lg">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="bg-[#081635] text-slate-300 py-8 px-5 md:px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <p className="text-sm">&copy; 2026 Ministério da Administração do Território. Todos os direitos reservados.</p>
          <div className="flex items-center gap-5 text-sm">
            <button className="hover:text-white transition-colors" title="Ver privacidade">Privacidade</button>
            <button className="hover:text-white transition-colors" title="Ver termos">Termos</button>
            <span className="text-slate-500">v{APP_VERSION}</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PublicLanding;
