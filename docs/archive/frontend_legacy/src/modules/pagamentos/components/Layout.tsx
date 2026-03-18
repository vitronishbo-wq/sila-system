
import React from 'react';
import { UserRole } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  role: UserRole;
  onRoleChange: (role: UserRole) => void;
}

const Layout: React.FC<LayoutProps> = ({ children, role, onRoleChange }) => {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-600 rounded flex items-center justify-center font-bold text-xl">S</div>
            <div>
              <h1 className="font-bold text-lg leading-none">SILA System</h1>
              <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Finanças</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1">
          <button className="w-full text-left px-4 py-2 rounded bg-slate-800 text-white flex items-center gap-3">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span>Dashboard</span>
          </button>
          <button className="w-full text-left px-4 py-2 rounded text-slate-400 hover:bg-slate-800 hover:text-white transition-colors flex items-center gap-3">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Faturas</span>
          </button>
          <button className="w-full text-left px-4 py-2 rounded text-slate-400 hover:bg-slate-800 hover:text-white transition-colors flex items-center gap-3">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>Pagamentos</span>
          </button>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <label className="block text-[10px] text-slate-500 uppercase font-bold mb-2">Simular Perfil</label>
          <select 
            value={role} 
            onChange={(e) => onRoleChange(e.target.value as UserRole)}
            className="w-full bg-slate-800 text-xs rounded border-none focus:ring-red-500 py-2"
          >
            <option value={UserRole.CITIZEN}>Cidadão</option>
            <option value={UserRole.ADMIN}>Administrador</option>
            <option value={UserRole.MANAGER}>Gestor</option>
            <option value={UserRole.OFFICER}>Oficial</option>
          </select>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-slate-500 uppercase tracking-wider">Módulo Financeiro</span>
            <div className="h-4 w-px bg-slate-200"></div>
            <span className="text-sm font-semibold text-slate-700">Administração Geral do Estado</span>
          </div>
          <div className="flex items-center gap-4">
            <button className="p-2 text-slate-400 hover:text-slate-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
            </button>
            <div className="w-8 h-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center font-semibold text-slate-600">
              {role[0]}
            </div>
          </div>
        </header>
        
        <div className="flex-1 overflow-y-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
