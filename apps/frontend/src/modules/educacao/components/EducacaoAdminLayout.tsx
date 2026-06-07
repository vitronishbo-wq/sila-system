import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { path: '/educacao/admin/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/educacao/admin/workflows', label: 'Workflows', icon: '🔄' },
  { path: '/educacao/admin/delegacoes', label: 'Delegações', icon: '🔗' },
  { path: '/educacao/admin/scope', label: 'Verificar Âmbito', icon: '🌐' },
];

export const EducacaoAdminLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className={`bg-blue-900 text-white transition-all duration-300 ${collapsed ? 'w-16' : 'w-64'}`}>
        <div className="p-4 border-b border-blue-800 flex items-center justify-between">
          {!collapsed && <h2 className="text-lg font-bold">Educação</h2>}
          <button onClick={() => setCollapsed(!collapsed)} className="text-white hover:text-blue-200 text-xl">
            {collapsed ? '→' : '←'}
          </button>
        </div>
        <nav className="mt-4 space-y-1">
          {NAV_ITEMS.map(item => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                location.pathname === item.path
                  ? 'bg-blue-800 text-white border-r-4 border-blue-300'
                  : 'text-blue-100 hover:bg-blue-800'
              }`}
            >
              <span>{item.icon}</span>
              {!collapsed && <span>{item.label}</span>}
            </button>
          ))}
        </nav>
      </aside>
      <main className="flex-1 overflow-auto">
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
