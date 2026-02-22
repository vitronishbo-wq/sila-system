
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ASSETS, ESSENTIAL_SERVICES, APP_VERSION } from '../constants';

const PublicLanding: React.FC = () => {
  const navigate = useNavigate();

  const handleServiceClick = (serviceId: string) => {
    console.log(`Service clicked: ${serviceId}`);
    const token = localStorage.getItem('token');
    if (token) {
      if (serviceId === 'identity') navigate('/admin/citizens');
      else if (serviceId === 'registry') navigate('/admin/documents');
      else navigate('/admin');
    } else {
      // Redirect to login with intent
      navigate(`/login?service=${serviceId}`);
    }
  };

  return (
    <div className="h-screen flex flex-col lg:flex-row bg-slate-50 overflow-hidden font-inter">

      {/* LEFT SIDE: Hero & Search */}
      <div className="w-full lg:w-5/12 bg-slate-900 text-white relative flex flex-col justify-between p-8 lg:p-12 overflow-hidden">
        {/* Background Overlay */}
        <div className="absolute inset-0 z-0 opacity-20">
          <img src={ASSETS.BANDEIRA} alt="Background" className="w-full h-full object-cover" />
        </div>

        {/* Header */}
        <div className="relative z-10 flex items-center gap-3 cursor-pointer" onClick={() => navigate('/')}>
          <img src={ASSETS.BRASAO} alt="Brasão" className="h-10 lg:h-12" />
          <div>
            <h1 className="text-xl font-bold leading-none">SILA-System</h1>
            <p className="text-xs opacity-60">Integrated Local Administration System</p>
          </div>
        </div>

        {/* Hero Content */}
        <div className="relative z-10 my-auto">
          <h2 className="text-3xl lg:text-5xl font-extrabold mb-6 tracking-tight leading-tight">
            Administração <br /> <span className="text-yellow-500">mais próxima de si.</span>
          </h2>
          <p className="text-lg opacity-80 mb-8 max-w-md">
            Aceda aos serviços públicos de forma rápida, segura e sem burocracia.
          </p>

          <div className="relative group max-w-md">
            <input
              type="text"
              placeholder="O que deseja tratar hoje?"
              className="w-full px-6 py-4 rounded-xl text-slate-900 shadow-xl focus:outline-none focus:ring-4 focus:ring-yellow-500/50 transition-all pl-12"
            />
            <i className="fa-solid fa-magnifying-glass absolute left-5 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </div>
        </div>

        {/* Footer info */}
        <div className="relative z-10 text-xs opacity-50 flex gap-4">
          <a href="#" className="hover:text-white transition-colors">Ajuda</a>
          <a href="#" className="hover:text-white transition-colors">Contactos</a>
          <span>v{APP_VERSION}</span>
        </div>
      </div>

      {/* RIGHT SIDE: Services Grid & Login */}
      <div className="w-full lg:w-7/12 flex flex-col h-full bg-slate-50 relative">
        {/* Top Auth Nav */}
        <div className="absolute top-0 right-0 p-6 z-20 flex gap-4">
          <button onClick={() => navigate('/citizen/login')} className="px-5 py-2.5 text-slate-600 font-semibold hover:text-slate-900 transition-colors">FUC do Cidadão</button>
          <button onClick={() => navigate('/login')} className="px-5 py-2.5 text-slate-600 font-semibold hover:text-slate-900 transition-colors">Painel Admin</button>
          <button onClick={() => navigate('/register')} className="px-5 py-2.5 bg-slate-900 text-white rounded-lg font-semibold hover:bg-slate-800 shadow-md transition-all hover:-translate-y-0.5">Criar Conta</button>
        </div>

        {/* Grid Container */}
        <div className="flex-1 overflow-y-auto p-8 lg:p-16 flex flex-col justify-center">
          <div className="max-w-4xl mx-auto w-full">
            <h3 className="text-xl font-bold text-slate-800 mb-8 flex items-center gap-3">
              <span className="w-8 h-8 bg-yellow-400 rounded-lg flex items-center justify-center text-white text-sm shadow-sm">
                <i className="fa-solid fa-star"></i>
              </span>
              Serviços Essenciais
            </h3>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-4 lg:gap-6">
              {ESSENTIAL_SERVICES.map((service) => (
                <div
                  key={service.id}
                  onClick={() => handleServiceClick(service.id)}
                  className="bg-white border border-gray-100 rounded-xl p-4 lg:p-6 shadow-sm hover:shadow-xl hover:border-yellow-400/30 hover:-translate-y-1 transition-all cursor-pointer group flex flex-col items-center text-center aspect-square justify-center"
                >
                  <div className={`w-12 h-12 lg:w-14 lg:h-14 rounded-xl ${service.color} text-white flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-md`}>
                    <i className={`fa-solid ${service.icon} text-xl lg:text-2xl`}></i>
                  </div>
                  <h4 className="font-semibold text-slate-700 text-xs lg:text-sm leading-tight">{service.name}</h4>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Simple Footer */}
        <div className="p-4 text-center text-xs text-gray-400 border-t">
          &copy; 2026 Ministério da Administração do Território
        </div>
      </div>
    </div>
  );
};

export default PublicLanding;