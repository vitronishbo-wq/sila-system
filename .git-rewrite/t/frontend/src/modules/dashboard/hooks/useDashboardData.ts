import { useEffect, useState } from 'react'
import { fetchDashboardStats, fetchDashboardChart, fetchDashboardAlerts } from '../../../services/dashboardApi'

interface DashboardStats {
  documentos: number
  usuarios: number
  atividades: number
  pendentes: number
}

const MOCK_STATS: DashboardStats = {
  documentos: 1247,
  usuarios: 89,
  atividades: 42,
  pendentes: 17
}

const MOCK_CHART = [
  { mes: 'Jan', documentos: 120 },
  { mes: 'Fev', documentos: 210 },
  { mes: 'Mar', documentos: 340 },
  { mes: 'Abr', documentos: 510 },
  { mes: 'Mai', documentos: 780 }
]

const MOCK_ALERTS = [
  { msg: '17 documentos aguardam validação', nivel: 'warning' },
  { msg: 'Backup automático executado com sucesso', nivel: 'info' }
]

export function useDashboardData() {
  const [stats, setStats] = useState<DashboardStats>(MOCK_STATS)
  const [chart, setChart] = useState(MOCK_CHART)
  const [alerts, setAlerts] = useState(MOCK_ALERTS)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token') || ''
    Promise.all([
      fetchDashboardStats(token).catch(() => MOCK_STATS),
      fetchDashboardChart(token).catch(() => MOCK_CHART),
      fetchDashboardAlerts(token).catch(() => MOCK_ALERTS)
    ])
      .then(([stats, chart, alerts]) => {
        setStats(stats)
        setChart(chart)
        setAlerts(alerts)
        setError(null)
      })
      .catch((err) => {
        console.warn('Usando dados mock para dashboard:', err.message)
        setError(null)
      })
      .finally(() => setLoading(false))
  }, [])

  return { stats, chart, alerts, loading, error }
}
