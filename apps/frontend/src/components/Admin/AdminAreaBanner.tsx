import React from 'react';

export const AdminAreaBanner: React.FC = () => {
  const env = typeof import.meta !== 'undefined' ? (import.meta.env?.VITE_APP_ENV as string | undefined) : undefined;
  const demoOverride = typeof window !== 'undefined' ? localStorage.getItem('demo_env') : null;
  const isHomolog = (demoOverride === 'homologacao') || (env === 'homologacao');

  return (
    <div className={`text-xs uppercase tracking-[0.2em] px-6 py-2 ${isHomolog ? 'bg-amber-500 text-black' : 'bg-slate-900 text-white'}`}>
      {isHomolog ? '⚠ Ambiente de Demonstração — Serviços simulados de homologação' : 'Area Administrativa'}
    </div>
  );
};

export default AdminAreaBanner;
