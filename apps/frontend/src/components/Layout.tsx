
import React, { useState, useEffect } from 'react';
import { User, UserRole } from '../types';
import { ASSETS } from '../constants';
import dashboardService from '../services/dashboardService';

interface LayoutProps {
  user: User;
  children: React.ReactNode;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ user, children, onLogout }) => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchCount = async () => {
      const count = await dashboardService.getUnreadCount();
      setUnreadCount(count);
    };
    fetchCount();
    const interval = setInterval(fetchCount, 30_000);
    return () => clearInterval(interval);
  }, []);

  const menuItems = [
    { label: 'Dashboard', icon: 'fa-chart-line', path: '#/admin', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Cidadãos', icon: 'fa-users', path: '#/admin/citizens', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Documentos', icon: 'fa-file-invoice', path: '#/admin/documents', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Pagamentos', icon: 'fa-credit-card', path: '#/admin/payments', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Territórios', icon: 'fa-map-marked-alt', path: '#/admin/territory', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL] },
    { label: 'Observabilidade', icon: 'fa-eye', path: '#/admin/observability', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL] },
  ];

  const filteredItems = menuItems.filter(item => item.roles.includes(user.role));

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Sidebar */}
      <aside className={`bg-slate-900 text-white transition-all duration-300 ${isSidebarOpen ? 'w-64' : 'w-20'} flex flex-col`}>
        <div className="p-4 flex items-center gap-3 border-b border-slate-800">
          <img src={ASSETS.BRASAO} alt="SILA" className="w-8 h-8 object-contain" />
          {isSidebarOpen && <span className="font-bold text-lg tracking-tight">SILA System</span>}
        </div>

        <nav className="flex-1 mt-6 px-2 space-y-1">
          {filteredItems.map((item) => (
            <a
              key={item.label}
              href={item.path}
              className="flex items-center gap-4 px-4 py-3 rounded-lg hover:bg-slate-800 transition-colors"
            >
              <i className={`fa-solid ${item.icon} w-6 text-center text-slate-400`}></i>
              {isSidebarOpen && <span>{item.label}</span>}
            </a>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800">
          <button
            onClick={onLogout}
            className="flex items-center gap-4 px-4 py-3 w-full rounded-lg hover:bg-red-900/30 text-red-400 transition-colors"
          >
            <i className="fa-solid fa-right-from-bracket w-6 text-center"></i>
            {isSidebarOpen && <span>Sair do Sistema</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b flex items-center justify-between px-8 shadow-sm">
          <button onClick={() => setSidebarOpen(!isSidebarOpen)} className="text-gray-500 hover:text-gray-700">
            <i className={`fa-solid ${isSidebarOpen ? 'fa-indent' : 'fa-outdent'} text-xl`}></i>
          </button>

          <div className="flex items-center gap-5">
            {/* Notification Bell */}
            <button
              onClick={() => { window.location.hash = '/admin'; }}
              className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors group"
              title="Notificações"
            >
              <i className="fa-solid fa-bell text-lg text-slate-400 group-hover:text-slate-700 transition-colors" />
              {unreadCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 flex items-center justify-center rounded-full bg-red-500 text-white text-[9px] font-bold ring-2 ring-white">
                  {unreadCount > 99 ? '99+' : unreadCount}
                </span>
              )}
            </button>

            <div className="w-px h-8 bg-gray-200" />

            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-semibold">{user.username}</p>
                <p className="text-xs text-gray-500 uppercase">{(user.role || 'user').replace('admin_', '')}</p>
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center border text-slate-600 font-bold shadow-inner">
                {user.username.charAt(0).toUpperCase()}
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;

