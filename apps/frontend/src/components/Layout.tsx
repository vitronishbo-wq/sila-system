
import React, { useState, useEffect, useRef } from 'react';
import { UserRole } from '../types';
import type { User } from '../types';
import { ASSETS, API_URL } from '../constants';
import dashboardService from '../services/dashboardService';
import { ToastProvider } from '../hooks/useToast';

interface LayoutProps {
  user: User;
  children: React.ReactNode;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ user, children, onLogout }) => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);
  const [exportLog, setExportLog] = useState<{ message: string; module?: string; created_at?: string } | null>(null);
  const [exportPulseAt, setExportPulseAt] = useState<number | null>(null);
  const [showBellPanel, setShowBellPanel] = useState(false);
  const [liveLogs, setLiveLogs] = useState<Array<{ message: string; module?: string; created_at?: string }>>([]);
  const [exportNewCount, setExportNewCount] = useState(0);
  const [panelNewCount, setPanelNewCount] = useState(0);
  const [moduleNewCounts, setModuleNewCounts] = useState<Record<string, number>>(() => {
    const raw = localStorage.getItem('export_logs_module_counts');
    if (!raw) return {};
    try {
      const parsed = JSON.parse(raw) as Record<string, number>;
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch {
      return {};
    }
  });
  const [lastSeenAt, setLastSeenAt] = useState<number>(() => {
    const stored = localStorage.getItem('export_logs_last_seen');
    const parsed = stored ? Number(stored) : NaN;
    return Number.isFinite(parsed) ? parsed : Date.now();
  });
  const [moduleFilter, setModuleFilter] = useState<'all' | string>('all');
  const showBellPanelRef = useRef(showBellPanel);
  const lastSeenAtRef = useRef(lastSeenAt);
  const logListRef = useRef<HTMLDivElement | null>(null);
  const [isAtTop, setIsAtTop] = useState(true);
  const isAtTopRef = useRef(true);
  const moduleFilterRef = useRef<'all' | string>(moduleFilter);
  const [panelPulse, setPanelPulse] = useState(false);
  const [exportPopoverOpen, setExportPopoverOpen] = useState(false);
  const exportPopoverRef = useRef<HTMLDivElement | null>(null);

  const timeAgo = (dateStr?: string) => {
    if (!dateStr) return '';
    const diff = Date.now() - new Date(dateStr).getTime();
    if (Number.isNaN(diff)) return '';
    const mins = Math.floor(diff / 60_000);
    if (mins < 1) return 'agora mesmo';
    if (mins < 60) return `há ${mins}m`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `há ${hrs}h`;
    const days = Math.floor(hrs / 24);
    return `há ${days}d`;
  };

  useEffect(() => {
    const fetchCount = async () => {
      const count = await dashboardService.getUnreadCount();
      setUnreadCount(count);
    };
    fetchCount();
    const interval = setInterval(fetchCount, 30_000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    showBellPanelRef.current = showBellPanel;
    if (showBellPanel) {
      const now = Date.now();
      setLastSeenAt(now);
      lastSeenAtRef.current = now;
      localStorage.setItem('export_logs_last_seen', String(now));
      setExportNewCount(0);
      setModuleFilter('all');
      setPanelNewCount(0);
    }
  }, [showBellPanel]);

  useEffect(() => {
    moduleFilterRef.current = moduleFilter;
    if (isAtTopRef.current) {
      setPanelNewCount(0);
      if (moduleFilter !== 'all') {
        setModuleNewCounts((prev) => {
          if (!prev[moduleFilter]) return prev;
          const next = { ...prev };
          delete next[moduleFilter];
          return next;
        });
      }
    }
  }, [moduleFilter]);

  useEffect(() => {
    if (!panelPulse) return;
    const t = setTimeout(() => setPanelPulse(false), 2200);
    return () => clearTimeout(t);
  }, [panelPulse]);

  useEffect(() => {
    if (!exportPopoverOpen) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (!exportPopoverRef.current) return;
      if (exportPopoverRef.current.contains(event.target as Node)) return;
      setExportPopoverOpen(false);
    };
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [exportPopoverOpen]);

  useEffect(() => {
    const handleRouteChange = () => {
      setExportPopoverOpen(false);
    };
    window.addEventListener('hashchange', handleRouteChange);
    return () => {
      window.removeEventListener('hashchange', handleRouteChange);
    };
  }, []);

  useEffect(() => {
    lastSeenAtRef.current = lastSeenAt;
    localStorage.setItem('export_logs_last_seen', String(lastSeenAt));
  }, [lastSeenAt]);

  useEffect(() => {
    localStorage.setItem('export_logs_module_counts', JSON.stringify(moduleNewCounts));
  }, [moduleNewCounts]);

  useEffect(() => {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token') || localStorage.getItem('admin_token');
    if (!token || !('EventSource' in window)) return;
    const apiRoot = API_URL.replace(/\/api\/?$/, '');
    const stream = new EventSource(`${apiRoot}/api/admin/exports/logs/stream?token=${encodeURIComponent(token)}`);
    stream.onmessage = (event) => {
      if (!event.data) return;
      try {
        const payload = JSON.parse(event.data) as { message?: string; module?: string; created_at?: string };
        if (payload.message) {
          setExportLog({
            message: payload.message || '',
            module: payload.module,
            created_at: payload.created_at,
          });
          setExportPulseAt(Date.now());
          const createdAtMs = payload.created_at ? new Date(payload.created_at).getTime() : Date.now();
          if (!Number.isNaN(createdAtMs) && createdAtMs > lastSeenAtRef.current && !showBellPanelRef.current) {
            setExportNewCount((c) => Math.min(99, c + 1));
          }
          if (!Number.isNaN(createdAtMs) && createdAtMs > lastSeenAtRef.current && payload.module) {
            const filter = moduleFilterRef.current;
            const shouldSkip = showBellPanelRef.current && isAtTopRef.current && filter === payload.module;
            if (!shouldSkip) {
              setModuleNewCounts((prev) => ({
                ...prev,
                [payload.module as string]: Math.min(99, (prev[payload.module as string] || 0) + 1),
              }));
            }
          }
          if (showBellPanelRef.current && !isAtTopRef.current) {
            const filter = moduleFilterRef.current;
            const matchesFilter = filter === 'all' || (!!payload.module && payload.module === filter);
            if (matchesFilter) {
              setPanelNewCount((c) => Math.min(99, c + 1));
              setPanelPulse(true);
            }
          }
          setLiveLogs((prev) => {
            const next = [
              { message: payload.message || '', module: payload.module, created_at: payload.created_at },
              ...prev,
            ];
            const seen = new Set<string>();
            return next.filter((item) => {
              const key = `${item.created_at || ''}-${item.message}-${item.module || ''}`;
              if (seen.has(key)) return false;
              seen.add(key);
              return true;
            }).slice(0, 6);
          });
        }
      } catch {
        // ignore malformed payloads
      }
    };
    stream.onerror = () => {
      stream.close();
    };
    return () => stream.close();
  }, []);

  useEffect(() => {
    if (!showBellPanel) return;
    if (!logListRef.current) return;
    const el = logListRef.current;
    if (el.scrollTop <= 8) {
      el.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [liveLogs, showBellPanel, moduleFilter]);

  useEffect(() => {
    const el = logListRef.current;
    if (!el) return;
    const handleScroll = () => {
      const atTop = el.scrollTop <= 8;
      setIsAtTop(atTop);
      isAtTopRef.current = atTop;
      if (atTop) {
        setPanelNewCount(0);
        const currentFilter = moduleFilterRef.current;
        if (currentFilter && currentFilter !== 'all') {
          setModuleNewCounts((prev) => {
            if (!prev[currentFilter]) return prev;
            const next = { ...prev };
            delete next[currentFilter];
            return next;
          });
        }
      }
    };
    el.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => {
      el.removeEventListener('scroll', handleScroll);
    };
  }, [showBellPanel, moduleFilter]);

  const menuItems = [
    { label: 'Dashboard', icon: 'fa-chart-line', path: '#/admin', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Cidadãos', icon: 'fa-users', path: '#/admin/citizens', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Documentos', icon: 'fa-file-invoice', path: '#/admin/documents', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Exportações', icon: 'fa-file-export', path: '#/admin/exports', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Pagamentos', icon: 'fa-credit-card', path: '#/admin/payments', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL, UserRole.ADMIN_PROVINCIAL, UserRole.ADMIN_MUNICIPAL] },
    { label: 'Territórios', icon: 'fa-map-marked-alt', path: '#/admin/territory', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL] },
    { label: 'Observabilidade', icon: 'fa-eye', path: '#/admin/observability', roles: [UserRole.ADMIN_SUPER, UserRole.ADMIN_CENTRAL] },
  ];

  const filteredItems = menuItems.filter(item => item.roles.includes(user.role));
  const moduleOptions = ['all', ...Array.from(new Set(liveLogs.map((log) => log.module).filter((m): m is string => Boolean(m))))];
  const exportBadgeCount = Object.values(moduleNewCounts).reduce((acc, v) => acc + v, 0);
  const exportBadgeItems = Object.entries(moduleNewCounts)
    .filter(([, count]) => count > 0)
    .sort((a, b) => b[1] - a[1]);

  const readMaxStack = () => {
    const stored = Number(localStorage.getItem('toast_max_stack'));
    if (Number.isFinite(stored) && stored > 0) return stored;
    const envValue = Number(import.meta.env.VITE_TOAST_MAX_STACK ?? 3);
    if (Number.isFinite(envValue) && envValue > 0) return envValue;
    return 3;
  };
  const [toastMaxStack, setToastMaxStack] = useState(readMaxStack);

  useEffect(() => {
    const handler = () => setToastMaxStack(readMaxStack());
    window.addEventListener('toast-config-changed', handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener('toast-config-changed', handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  return (
    <ToastProvider maxStack={toastMaxStack}>
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
              onClick={() => {
                if (item.label === 'Exportações') setExportPopoverOpen(false);
              }}
            >
              <i className={`fa-solid ${item.icon} w-6 text-center text-slate-400`}></i>
              {isSidebarOpen && (
                <span className="flex items-center gap-2">
                  {item.label}
                  {item.label === 'Exportações' && exportBadgeCount > 0 && (
                    <span className="relative" ref={exportPopoverRef}>
                      <button
                        type="button"
                        onClick={(event) => {
                          event.preventDefault();
                          event.stopPropagation();
                          setExportPopoverOpen((prev) => !prev);
                        }}
                        className="inline-flex min-w-[18px] h-[18px] items-center justify-center rounded-full bg-emerald-500 text-white text-[9px] font-bold px-1"
                        aria-label="Novos por módulo"
                      >
                        {exportBadgeCount > 99 ? '99+' : exportBadgeCount}
                      </button>
                      {exportBadgeItems.length > 0 && exportPopoverOpen && (
                        <div className="absolute top-7 right-0 z-50">
                          <div className="min-w-[180px] rounded-lg border border-slate-200 bg-white shadow-xl p-3">
                            <p className="text-[10px] font-semibold uppercase text-slate-400 mb-2">Novos por módulo</p>
                            <div className="space-y-1">
                              {exportBadgeItems.map(([mod, count]) => (
                                <div
                                  key={mod}
                                  className={`flex items-center justify-between text-xs ${
                                    moduleFilter === mod ? 'text-slate-900 font-semibold bg-amber-50 px-2 py-1 rounded-md' : 'text-slate-700'
                                  }`}
                                >
                                  <span className="uppercase flex items-center gap-2">
                                    {mod}
                                    {moduleFilter === mod && (
                                      <span className="inline-flex items-center gap-1 rounded-full bg-amber-200/60 text-amber-800 text-[9px] font-semibold px-2 py-0.5">
                                        <i className="fa-solid fa-filter text-[8px]" />
                                        Filtro ativo
                                      </span>
                                    )}
                                  </span>
                                  <span>{count}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </span>
                  )}
                </span>
              )}
              {!isSidebarOpen && item.label === 'Exportações' && exportBadgeCount > 0 && (
                <span className="absolute ml-8 -mt-5 inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500">
                  <button
                    type="button"
                    onClick={(event) => {
                      event.preventDefault();
                      event.stopPropagation();
                      setExportPopoverOpen((prev) => !prev);
                    }}
                    className="absolute -left-1 -top-1 h-4 w-4 rounded-full"
                    aria-label="Novos por módulo"
                  />
                  {exportBadgeItems.length > 0 && exportPopoverOpen && (
                    <span className="absolute left-3 -top-2 z-50">
                      <span className="min-w-[180px] rounded-lg border border-slate-200 bg-white shadow-xl p-3">
                        <span className="text-[10px] font-semibold uppercase text-slate-400 mb-2 block">Novos por módulo</span>
                        <span className="space-y-1 block">
                          {exportBadgeItems.map(([mod, count]) => (
                            <span
                              key={mod}
                              className={`flex items-center justify-between text-xs ${
                                moduleFilter === mod ? 'text-slate-900 font-semibold bg-amber-50 px-2 py-1 rounded-md' : 'text-slate-700'
                              }`}
                            >
                              <span className="uppercase flex items-center gap-2">
                                {mod}
                                {moduleFilter === mod && (
                                  <span className="inline-flex items-center gap-1 rounded-full bg-amber-200/60 text-amber-800 text-[9px] font-semibold px-2 py-0.5">
                                    <i className="fa-solid fa-filter text-[8px]" />
                                    Filtro ativo
                                  </span>
                                )}
                              </span>
                              <span>{count}</span>
                            </span>
                          ))}
                        </span>
                      </span>
                    </span>
                  )}
                </span>
              )}
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
            <div className="flex items-center gap-3">
              {exportLog && (
                <button
                  onClick={() => { window.location.hash = '/admin/exports'; }}
                  className="hidden lg:flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 hover:bg-slate-100 transition-colors max-w-[360px]"
                  title={exportLog.message}
                >
                  <span className="text-[10px] uppercase tracking-wide font-semibold text-slate-500">Exportações</span>
                  <span className="truncate">{exportLog.message}</span>
                  {exportLog.module && (
                    <span className="px-2 py-0.5 rounded-full bg-slate-200 text-[10px] uppercase text-slate-600">
                      {exportLog.module}
                    </span>
                  )}
                </button>
              )}
              <button
                onClick={() => setShowBellPanel((prev) => !prev)}
                className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors group"
                title="Notificações"
              >
                <i className="fa-solid fa-bell text-lg text-slate-400 group-hover:text-slate-700 transition-colors" />
                {unreadCount > 0 && (
                  <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 flex items-center justify-center rounded-full bg-red-500 text-white text-[9px] font-bold ring-2 ring-white">
                    {unreadCount > 99 ? '99+' : unreadCount}
                  </span>
                )}
                {exportNewCount > 0 && (
                  <span className="absolute -bottom-0.5 -right-0.5 min-w-[16px] h-[16px] px-1 flex items-center justify-center rounded-full bg-emerald-500 text-white text-[9px] font-bold ring-2 ring-white">
                    {exportNewCount > 99 ? '99+' : exportNewCount}
                  </span>
                )}
                {exportPulseAt && Date.now() - exportPulseAt < 5000 && (
                  <span className="absolute -bottom-0.5 -left-0.5 flex h-2.5 w-2.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                  </span>
                )}
              </button>
            </div>

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

      {showBellPanel && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowBellPanel(false)}
          />
          <div className="fixed top-20 right-8 w-96 max-h-[70vh] bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 overflow-hidden animate-in">
            <div className="flex items-center justify-between px-5 py-4 border-b bg-gradient-to-r from-slate-50 to-white">
              <h3 className="font-bold text-slate-900 flex items-center gap-2">
                <i className="fa-solid fa-bell text-yellow-500" />
                Exportações ao vivo
                {unreadCount > 0 && (
                  <span className="px-2 py-0.5 bg-red-500 text-white text-[10px] font-bold rounded-full">
                    {unreadCount}
                  </span>
                )}
                {exportNewCount > 0 && (
                  <span className="px-2 py-0.5 bg-emerald-500 text-white text-[10px] font-bold rounded-full">
                    +{exportNewCount}
                  </span>
                )}
              </h3>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const now = Date.now();
                    setLastSeenAt(now);
                    lastSeenAtRef.current = now;
                    localStorage.setItem('export_logs_last_seen', String(now));
                    setExportNewCount(0);
                    setPanelNewCount(0);
                    setModuleNewCounts({});
                    setPanelPulse(false);
                  }}
                  className="text-xs font-semibold text-slate-500 hover:text-slate-700"
                >
                  Limpar contagens
                </button>
                <button
                  onClick={() => setShowBellPanel(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <i className="fa-solid fa-xmark text-lg" />
                </button>
              </div>
            </div>
            <div className="px-5 py-3 border-b bg-white flex items-center justify-between">
              <button
                onClick={() => { window.location.hash = '/admin/exports'; setShowBellPanel(false); }}
                className="text-xs font-semibold text-slate-700 underline"
              >
                Ver histórico
              </button>
              <button
                onClick={() => { window.location.hash = '/admin'; setShowBellPanel(false); }}
                className="text-xs font-semibold text-slate-500 hover:text-slate-700"
              >
                Notificações gerais
              </button>
            </div>
            <div className="px-5 py-3 border-b bg-white">
              <div className="flex flex-wrap gap-2">
                {moduleOptions.map((mod) => (
                  <button
                    key={mod}
                    onClick={() => setModuleFilter(mod)}
                    className={`rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-wide ${
                      moduleFilter === mod
                        ? 'bg-slate-900 text-white ring-2 ring-amber-200'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    <span className="relative inline-flex items-center gap-1">
                      {moduleFilter === mod && mod !== 'all' && (
                        <i className="fa-solid fa-filter text-[9px] text-amber-300" />
                      )}
                      <span>{mod === 'all' ? 'Todos' : mod}</span>
                      {mod !== 'all' && moduleNewCounts[mod] > 0 && (
                        <span className="ml-1 inline-flex min-w-[16px] h-[16px] items-center justify-center rounded-full bg-emerald-500 text-white text-[9px] font-bold px-1">
                          {moduleNewCounts[mod] > 99 ? '99+' : moduleNewCounts[mod]}
                        </span>
                      )}
                    </span>
                  </button>
                ))}
              </div>
              {exportBadgeItems.length > 0 && (
                <div className="mt-3 rounded-lg border border-slate-200 bg-slate-50 p-2">
                  <p className="text-[10px] font-semibold uppercase text-slate-400 mb-2">Novos por módulo</p>
                  <div className="space-y-1">
                    {exportBadgeItems.map(([mod, count]) => (
                      <div
                        key={mod}
                        className={`flex items-center justify-between text-xs ${
                          moduleFilter === mod ? 'text-slate-900 font-semibold bg-amber-50 px-2 py-1 rounded-md' : 'text-slate-700'
                        }`}
                      >
                        <span className="uppercase flex items-center gap-2">
                          {mod}
                          {moduleFilter === mod && (
                            <span className="inline-flex items-center gap-1 rounded-full bg-amber-200/60 text-amber-800 text-[9px] font-semibold px-2 py-0.5">
                              <i className="fa-solid fa-filter text-[8px]" />
                              Filtro ativo
                            </span>
                          )}
                        </span>
                        <span>{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            <div ref={logListRef} className="relative overflow-y-auto max-h-[calc(70vh-152px)] p-3 space-y-2">
              {liveLogs.length === 0 ? (
                <div className="text-center py-8 text-sm text-gray-400">
                  Sem logs recentes.
                </div>
              ) : (
                liveLogs
                  .filter((log) => moduleFilter === 'all' || log.module === moduleFilter)
                  .map((log, idx) => (
                  <div
                    key={`${log.created_at || ''}-${idx}`}
                    className="flex items-start gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100"
                  >
                    <span className="mt-1 h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-slate-900 truncate">{log.message}</p>
                      <div className="flex items-center gap-2 mt-1">
                        {log.module && (
                          <span className="rounded-full bg-white px-2 py-0.5 text-[10px] uppercase text-slate-500 border border-slate-200">
                            {log.module}
                          </span>
                        )}
                        {log.created_at && (
                          <span className="text-[10px] text-gray-400">{timeAgo(log.created_at)}</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
              {!isAtTop && panelNewCount > 0 && (
                <button
                  type="button"
                  onClick={() => {
                    if (!logListRef.current) return;
                    logListRef.current.scrollTo({ top: 0, behavior: 'smooth' });
                    setPanelNewCount(0);
                  }}
                  className={`sticky bottom-2 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-xs font-semibold px-3 py-2 rounded-full shadow-lg flex items-center gap-2 ${
                    panelPulse ? 'animate-pulse' : ''
                  }`}
                >
                  <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                  Novos logs ({panelNewCount})
                </button>
              )}
            </div>
          </div>
        </>
      )}
      </div>
    </ToastProvider>
  );
};

export default Layout;
