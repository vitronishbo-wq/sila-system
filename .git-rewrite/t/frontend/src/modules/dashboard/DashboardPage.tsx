import { useDashboardData } from './hooks/useDashboardData';
import DashboardCards from './DashboardCards';
import DashboardCharts from './DashboardCharts';
import DashboardAlerts from './DashboardAlerts';

export default function DashboardPage() {
  const { stats, chart, alerts, loading, error } = useDashboardData();

  if (loading) {
    return <div style={{ padding: 32, textAlign: 'center' }}>Carregando dados...</div>;
  }

  if (error) {
    return <div style={{ padding: 32, color: '#dc2626' }}>Erro: {error}</div>;
  }

  return (
    <>
      <DashboardCards stats={stats} />
      <DashboardCharts data={chart} />
      <DashboardAlerts alerts={alerts} />
    </>
  );
}
