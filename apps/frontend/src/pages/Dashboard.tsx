
import React, { useState, useEffect, useCallback } from 'react';
import { User, AdminLevel, UserRole } from '../types';
import { ASSETS } from '../constants';
import dashboardService, {
  DashboardData,
  NotificationItem,
  RecentRequest,
} from '../services/dashboardService';

/* ─── helpers ─── */
function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60_000);
  if (mins < 1) return 'agora mesmo';
  if (mins < 60) return `há ${mins}m`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `há ${hrs}h`;
  const days = Math.floor(hrs / 24);
  return `há ${days}d`;
}

const STATUS_MAP: Record<string, { label: string; bg: string; text: string }> = {
  draft: { label: 'Rascunho', bg: 'bg-gray-100', text: 'text-gray-600' },
  pending: { label: 'Pendente', bg: 'bg-amber-50', text: 'text-amber-700' },
  submitted: { label: 'Submetido', bg: 'bg-blue-50', text: 'text-blue-700' },
  under_review: { label: 'Em Revisão', bg: 'bg-indigo-50', text: 'text-indigo-700' },
  in_progress: { label: 'Em Curso', bg: 'bg-sky-50', text: 'text-sky-700' },
  approved: { label: 'Aprovado', bg: 'bg-emerald-50', text: 'text-emerald-700' },
  completed: { label: 'Concluído', bg: 'bg-green-50', text: 'text-green-700' },
  rejected: { label: 'Rejeitado', bg: 'bg-red-50', text: 'text-red-700' },
  cancelled: { label: 'Cancelado', bg: 'bg-rose-50', text: 'text-rose-600' },
  scheduled: { label: 'Agendado', bg: 'bg-violet-50', text: 'text-violet-700' },
};

const NOTIF_ICONS: Record<string, { icon: string; color: string }> = {
  info: { icon: 'fa-circle-info', color: 'text-blue-500' },
  warning: { icon: 'fa-triangle-exclamation', color: 'text-amber-500' },
  success: { icon: 'fa-circle-check', color: 'text-emerald-500' },
  error: { icon: 'fa-circle-xmark', color: 'text-red-500' },
  document_update: { icon: 'fa-file-circle-check', color: 'text-indigo-500' },
  system: { icon: 'fa-gear', color: 'text-slate-500' },
};

/* ─── sub-components ─── */

const KPICard: React.FC<{
  label: string;
  value: string;
  icon: string;
  gradient: string;
  trend: string;
  delay: number;
}> = ({ label, value, icon, gradient, trend, delay }) => {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay);
    return () => clearTimeout(t);
  }, [delay]);

  const isPositive = trend.startsWith('+');
  return (
    <div
      className={`relative overflow-hidden rounded-2xl p-6 shadow-sm border border-gray-100
        hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300
        ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}
      style={{ transitionDelay: `${delay}ms`, background: '#fff' }}
    >
      <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full opacity-10 ${gradient}`} />
      <div className="flex justify-between items-start mb-4 relative z-10">
        <div
          className={`w-12 h-12 rounded-xl flex items-center justify-center text-white shadow-lg ${gradient}`}
        >
          <i className={`fa-solid ${icon} text-lg`} />
        </div>
        <span
          className={`text-xs font-bold px-2.5 py-1 rounded-full ${isPositive
              ? 'bg-emerald-50 text-emerald-600'
              : 'bg-red-50 text-red-600'
            }`}
        >
          {trend}
        </span>
      </div>
      <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider">{label}</p>
      <p className="text-3xl font-extrabold text-slate-900 mt-1 tabular-nums">{value}</p>
    </div>
  );
};

const NotificationBell: React.FC<{
  count: number;
  onClick: () => void;
}> = ({ count, onClick }) => (
  <button
    onClick={onClick}
    className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors group"
    title="Notificações"
  >
    <i className="fa-solid fa-bell text-lg text-slate-500 group-hover:text-slate-800 transition-colors" />
    {count > 0 && (
      <span className="absolute -top-0.5 -right-0.5 min-w-[20px] h-5 px-1.5 flex items-center justify-center rounded-full bg-red-500 text-white text-[10px] font-bold ring-2 ring-white animate-pulse">
        {count > 99 ? '99+' : count}
      </span>
    )}
  </button>
);

/* ─── main dashboard ─── */

interface DashboardProps {
  user: User;
}

const Dashboard: React.FC<DashboardProps> = ({ user }) => {
  // Guard: citizens never see admin dashboard
  if (user.role === UserRole.CITIZEN) return null;

  /* ── state ── */
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [requests, setRequests] = useState<RecentRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNotifPanel, setShowNotifPanel] = useState(false);
  const [activeTab, setActiveTab] = useState<'requests' | 'notifications'>('requests');

  /* ── data fetching ── */
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [dash, notifs, count, reqs] = await Promise.all([
        dashboardService.getDashboard(),
        dashboardService.getNotifications(),
        dashboardService.getUnreadCount(),
        dashboardService.getRecentRequests(),
      ]);
      setDashboard(dash);
      setNotifications(notifs);
      setUnreadCount(count);
      setRequests(reqs);
    } catch (err) {
      console.error('[Dashboard] load error', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    // Auto-refresh every 30s
    const interval = setInterval(loadData, 30_000);
    return () => clearInterval(interval);
  }, [loadData]);

  /* ── actions ── */
  const handleMarkAsRead = async (id: string) => {
    await dashboardService.markAsRead(id);
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
    );
    setUnreadCount((c) => Math.max(0, c - 1));
  };

  const handleMarkAllRead = async () => {
    await dashboardService.markAllAsRead();
    setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
    setUnreadCount(0);
  };

  /* ── derived ── */
  const m = dashboard?.metrics;
  const kpis = [
    {
      label: 'Total de Cidadãos',
      value: m?.total_citizens ?? '—',
      icon: 'fa-users',
      gradient: 'bg-gradient-to-br from-blue-500 to-blue-600',
      trend: m?.trends?.citizens ?? '+0%',
    },
    {
      label: 'Documentos Emitidos',
      value: m?.total_documents ?? '—',
      icon: 'fa-file-invoice',
      gradient: 'bg-gradient-to-br from-emerald-500 to-emerald-600',
      trend: m?.trends?.documents ?? '+0%',
    },
    {
      label: 'Pedidos Pendentes',
      value: m?.pending_requests ?? '—',
      icon: 'fa-clock',
      gradient: 'bg-gradient-to-br from-amber-500 to-orange-500',
      trend: m?.trends?.requests ?? '+0%',
    },
    {
      label: 'Tempo Médio Resposta',
      value: m?.avg_response_time ?? '—',
      icon: 'fa-bolt',
      gradient: 'bg-gradient-to-br from-violet-500 to-purple-600',
      trend: m?.trends?.response_time ?? '+0%',
    },
  ];

  const levelImages: Record<string, string> = {
    [AdminLevel.CENTRAL]: ASSETS.LEVEL_CENTRAL,
    [AdminLevel.PROVINCIAL]: ASSETS.LEVEL_PROVINCIAL,
    [AdminLevel.MUNICIPAL]: ASSETS.LEVEL_MUNICIPAL,
  };

  /* ── render ── */
  return (
    <div className="space-y-8 relative">
      {/* ═══════════════ Welcome Banner ═══════════════ */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-8 text-white shadow-xl">
        <img
          src={levelImages[user.level] || ASSETS.LEVEL_CENTRAL}
          className="absolute right-0 top-0 h-full w-1/2 object-cover opacity-30"
          style={{
            maskImage: 'linear-gradient(to left, transparent 0%, black 60%)',
            WebkitMaskImage: 'linear-gradient(to left, transparent 0%, black 60%)',
          }}
          alt="Level context"
        />
        {/* Animated gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10 animate-pulse pointer-events-none" />

        <div className="relative z-10 flex items-start justify-between">
          <div className="max-w-2xl">
            <p className="text-slate-400 text-sm font-medium mb-1 tracking-wide uppercase">
              Painel Administrativo
            </p>
            <h1 className="text-3xl font-bold mb-2">
              Bom dia, <span className="text-yellow-400">{user.username}</span>
            </h1>
            <p className="text-slate-300 text-base mb-6">
              Visão Geral — Nível{' '}
              <span className="font-semibold text-white">
                {user.level.charAt(0).toUpperCase() + user.level.slice(1)}
              </span>
              {user.territory_id && (
                <span className="ml-2 font-bold text-white">
                  • Localidade: {user.territory_id}
                </span>
              )}
            </p>
            <div className="flex gap-3">
              <button className="px-5 py-2.5 bg-yellow-500 text-slate-900 font-bold rounded-lg hover:bg-yellow-400 transition-all shadow-lg hover:shadow-yellow-500/25 active:scale-95">
                <i className="fa-solid fa-chart-bar mr-2" />
                Gerar Relatório
              </button>
              <button className="px-5 py-2.5 bg-white/10 backdrop-blur text-white font-bold rounded-lg border border-white/20 hover:bg-white/20 transition-all active:scale-95">
                <i className="fa-solid fa-gear mr-2" />
                Configurações
              </button>
            </div>
          </div>

          {/* Notification bell in banner */}
          <div className="flex items-center gap-3">
            <NotificationBell
              count={unreadCount}
              onClick={() => setShowNotifPanel(!showNotifPanel)}
            />
          </div>
        </div>
      </div>

      {/* ═══════════════ KPI Cards ═══════════════ */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi, i) => (
          <KPICard key={kpi.label} {...kpi} delay={100 + i * 80} />
        ))}
      </div>

      {/* ═══════════════ Main Content Grid ═══════════════ */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* ── Left: Requests + Notifications Feed ── */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          {/* Tab bar */}
          <div className="flex border-b border-gray-100">
            <button
              onClick={() => setActiveTab('requests')}
              className={`flex-1 px-6 py-4 text-sm font-bold uppercase tracking-wider transition-colors ${activeTab === 'requests'
                  ? 'text-slate-900 border-b-2 border-yellow-500 bg-yellow-50/50'
                  : 'text-gray-400 hover:text-gray-600'
                }`}
            >
              <i className="fa-solid fa-list-check mr-2" />
              Pedidos Recentes
            </button>
            <button
              onClick={() => setActiveTab('notifications')}
              className={`flex-1 px-6 py-4 text-sm font-bold uppercase tracking-wider transition-colors relative ${activeTab === 'notifications'
                  ? 'text-slate-900 border-b-2 border-yellow-500 bg-yellow-50/50'
                  : 'text-gray-400 hover:text-gray-600'
                }`}
            >
              <i className="fa-solid fa-bell mr-2" />
              Notificações
              {unreadCount > 0 && (
                <span className="ml-2 px-2 py-0.5 bg-red-500 text-white text-[10px] font-bold rounded-full">
                  {unreadCount}
                </span>
              )}
            </button>
          </div>

          <div className="p-6">
            {/* === REQUESTS TAB === */}
            {activeTab === 'requests' && (
              <div className="space-y-3">
                {loading ? (
                  <div className="flex flex-col items-center justify-center py-12 text-gray-400">
                    <i className="fa-solid fa-circle-notch fa-spin text-3xl mb-3" />
                    <p className="text-sm">A carregar pedidos...</p>
                  </div>
                ) : requests.length === 0 ? (
                  <div className="text-center py-12">
                    <i className="fa-solid fa-inbox text-4xl text-gray-200 mb-3" />
                    <p className="text-gray-400 font-medium">Nenhum pedido registado</p>
                    <p className="text-gray-300 text-sm mt-1">
                      Os pedidos aparecerão aqui quando forem criados
                    </p>
                  </div>
                ) : (
                  requests.map((req) => {
                    const st = STATUS_MAP[req.status?.toLowerCase()] || STATUS_MAP.pending;
                    const initials = (req.citizen_name || 'N/A')
                      .split(' ')
                      .slice(0, 2)
                      .map((w) => w[0])
                      .join('')
                      .toUpperCase();

                    return (
                      <div
                        key={req.id}
                        className="flex items-center justify-between p-4 bg-slate-50 rounded-xl
                          hover:bg-white border border-transparent hover:border-slate-200
                          hover:shadow-sm transition-all cursor-pointer group"
                      >
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center font-bold text-slate-600 text-sm shadow-inner">
                            {initials}
                          </div>
                          <div>
                            <p className="font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
                              {req.citizen_name || `Pedido ${req.id.slice(0, 8)}`}
                            </p>
                            <p className="text-xs text-gray-500">
                              {req.request_number && (
                                <span className="font-mono mr-2">{req.request_number}</span>
                              )}
                              {req.service_type?.replace(/_/g, ' ')}
                            </p>
                          </div>
                        </div>
                        <div className="text-right flex flex-col items-end gap-1">
                          <span
                            className={`px-3 py-1 ${st.bg} ${st.text} rounded-full text-[10px] font-bold uppercase tracking-wider`}
                          >
                            {st.label}
                          </span>
                          <p className="text-[10px] text-gray-400">
                            {req.created_at ? timeAgo(req.created_at) : '—'}
                          </p>
                        </div>
                      </div>
                    );
                  })
                )}

                {requests.length > 0 && (
                  <a
                    href="#/admin/documents"
                    className="flex items-center justify-center w-full mt-4 py-3 border-2 border-dashed border-slate-200
                      rounded-xl text-slate-400 font-bold hover:bg-slate-50 hover:border-slate-300
                      hover:text-slate-600 transition-all text-sm"
                  >
                    Ver Todos os Pedidos
                    <i className="fa-solid fa-arrow-right ml-2" />
                  </a>
                )}
              </div>
            )}

            {/* === NOTIFICATIONS TAB === */}
            {activeTab === 'notifications' && (
              <div className="space-y-3">
                {/* Mark all read bar */}
                {notifications.some((n) => !n.is_read) && (
                  <div className="flex justify-end mb-2">
                    <button
                      onClick={handleMarkAllRead}
                      className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1 transition-colors"
                    >
                      <i className="fa-solid fa-check-double" />
                      Marcar todas como lidas
                    </button>
                  </div>
                )}

                {loading ? (
                  <div className="flex flex-col items-center justify-center py-12 text-gray-400">
                    <i className="fa-solid fa-circle-notch fa-spin text-3xl mb-3" />
                    <p className="text-sm">A carregar notificações...</p>
                  </div>
                ) : notifications.length === 0 ? (
                  <div className="text-center py-12">
                    <i className="fa-solid fa-bell-slash text-4xl text-gray-200 mb-3" />
                    <p className="text-gray-400 font-medium">Sem notificações</p>
                    <p className="text-gray-300 text-sm mt-1">Está tudo em dia!</p>
                  </div>
                ) : (
                  notifications.map((notif) => {
                    const ni = NOTIF_ICONS[notif.type] || NOTIF_ICONS.info;
                    return (
                      <div
                        key={notif.id}
                        onClick={() => !notif.is_read && handleMarkAsRead(notif.id)}
                        className={`flex items-start gap-4 p-4 rounded-xl border transition-all cursor-pointer
                          ${notif.is_read
                            ? 'bg-white border-gray-100 opacity-70'
                            : 'bg-blue-50/50 border-blue-100 hover:bg-blue-50 shadow-sm'
                          }`}
                      >
                        <div
                          className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${notif.is_read ? 'bg-gray-100' : 'bg-white shadow-sm'
                            }`}
                        >
                          <i className={`fa-solid ${ni.icon} ${ni.color}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p
                              className={`text-sm font-bold truncate ${notif.is_read ? 'text-gray-500' : 'text-slate-900'
                                }`}
                            >
                              {notif.title}
                            </p>
                            {!notif.is_read && (
                              <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0 ml-2" />
                            )}
                          </div>
                          <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">
                            {notif.message}
                          </p>
                          <p className="text-[10px] text-gray-400 mt-1">
                            {timeAgo(notif.created_at)}
                          </p>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            )}
          </div>
        </div>

        {/* ── Right Column ── */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <h2 className="text-lg font-bold mb-5 flex items-center gap-2">
              <i className="fa-solid fa-rocket text-yellow-500" />
              Ações Rápidas
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: 'Novo Cidadão', icon: 'fa-user-plus', href: '#/admin/citizens' },
                { label: 'Estatísticas', icon: 'fa-chart-pie', href: '#/admin/observability' },
                { label: 'Pedidos', icon: 'fa-file-lines', href: '#/admin/documents' },
                { label: 'Auditoria', icon: 'fa-shield-halved', href: '#/admin/observability' },
                { label: 'Territórios', icon: 'fa-map-location-dot', href: '#/admin/territory' },
                { label: 'Pagamentos', icon: 'fa-credit-card', href: '#/admin/payments' },
              ].map((action) => (
                <a
                  key={action.label}
                  href={action.href}
                  className="p-4 rounded-xl border border-gray-100 bg-slate-50
                    hover:bg-slate-900 hover:text-white hover:border-slate-900
                    transition-all duration-200 group flex flex-col items-center gap-2.5 text-center"
                >
                  <i
                    className={`fa-solid ${action.icon} text-xl text-slate-400 group-hover:text-yellow-400 group-hover:scale-110 transition-all`}
                  />
                  <span className="text-[11px] font-bold uppercase tracking-wide">
                    {action.label}
                  </span>
                </a>
              ))}
            </div>
          </div>

          {/* Attention Card */}
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div className="absolute -right-6 -bottom-6 w-28 h-28 rounded-full bg-yellow-500/10" />
            <div className="absolute -right-3 -bottom-3 w-16 h-16 rounded-full bg-yellow-500/10" />
            <i className="fa-solid fa-flag absolute right-4 bottom-4 text-6xl text-slate-800/50 rotate-12" />

            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <span className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
                <h3 className="font-bold text-base uppercase tracking-wider text-yellow-400">
                  Atenção Crítica
                </h3>
              </div>
              <p className="text-slate-400 text-sm mb-5 leading-relaxed">
                Existem processos aguardando validação há mais de 72 horas. Verifique os pedidos pendentes.
              </p>
              <button className="text-yellow-400 font-bold text-sm flex items-center gap-2 hover:text-yellow-300 hover:translate-x-1 transition-all group">
                Resolver agora
                <i className="fa-solid fa-arrow-right group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>

          {/* Live Events Stream */}
          {dashboard?.recent_events && dashboard.recent_events.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
                </span>
                Eventos em Tempo Real
              </h2>
              <div className="space-y-3 max-h-48 overflow-y-auto pr-1 custom-scrollbar">
                {dashboard.recent_events.slice(0, 8).map((evt: any, i: number) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 text-sm border-l-2 border-slate-200 pl-3 py-1 hover:border-yellow-500 transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-slate-700 font-medium truncate">
                        {evt.action || evt.type || 'Evento'}
                      </p>
                      <p className="text-[10px] text-gray-400">
                        {evt.timestamp ? timeAgo(evt.timestamp) : '—'}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ═══════════════ Floating Notification Panel ═══════════════ */}
      {showNotifPanel && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowNotifPanel(false)}
          />
          <div className="fixed top-20 right-8 w-96 max-h-[70vh] bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 overflow-hidden animate-in">
            <div className="flex items-center justify-between px-5 py-4 border-b bg-gradient-to-r from-slate-50 to-white">
              <h3 className="font-bold text-slate-900 flex items-center gap-2">
                <i className="fa-solid fa-bell text-yellow-500" />
                Notificações
                {unreadCount > 0 && (
                  <span className="px-2 py-0.5 bg-red-500 text-white text-[10px] font-bold rounded-full">
                    {unreadCount}
                  </span>
                )}
              </h3>
              <div className="flex items-center gap-2">
                {unreadCount > 0 && (
                  <button
                    onClick={handleMarkAllRead}
                    className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Ler todas
                  </button>
                )}
                <button
                  onClick={() => setShowNotifPanel(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <i className="fa-solid fa-xmark text-lg" />
                </button>
              </div>
            </div>

            <div className="overflow-y-auto max-h-[calc(70vh-60px)] p-3 space-y-2">
              {notifications.length === 0 ? (
                <div className="text-center py-8">
                  <i className="fa-solid fa-bell-slash text-3xl text-gray-200 mb-2" />
                  <p className="text-gray-400 text-sm">Sem notificações</p>
                </div>
              ) : (
                notifications.slice(0, 15).map((notif) => {
                  const ni = NOTIF_ICONS[notif.type] || NOTIF_ICONS.info;
                  return (
                    <div
                      key={notif.id}
                      onClick={() => !notif.is_read && handleMarkAsRead(notif.id)}
                      className={`flex items-start gap-3 p-3 rounded-xl cursor-pointer transition-all
                        ${notif.is_read
                          ? 'bg-white hover:bg-gray-50 opacity-60'
                          : 'bg-blue-50/60 hover:bg-blue-50'
                        }`}
                    >
                      <i className={`fa-solid ${ni.icon} ${ni.color} mt-0.5`} />
                      <div className="flex-1 min-w-0">
                        <p
                          className={`text-sm font-semibold truncate ${notif.is_read ? 'text-gray-500' : 'text-slate-800'
                            }`}
                        >
                          {notif.title}
                        </p>
                        <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">
                          {notif.message}
                        </p>
                        <p className="text-[10px] text-gray-400 mt-1">
                          {timeAgo(notif.created_at)}
                        </p>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
