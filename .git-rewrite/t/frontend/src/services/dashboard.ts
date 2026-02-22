import { useEffect, useState } from "react";

export interface ChartDataPoint {
  label: string;
  value: number;
}

export function useDashboardStats() {
  const [documentsByMonth, setDocumentsByMonth] = useState<ChartDataPoint[]>([]);
  const [activeUsers, setActiveUsers] = useState<number>(0);
  const [alerts, setAlerts] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      setLoading(true);
      try {
        const token = localStorage.getItem("access_token");
        const [docsRes, usersRes, alertsRes] = await Promise.all([
          fetch("http://localhost:8000/api/v1/dashboard/documents-by-month", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("http://localhost:8000/api/v1/dashboard/active-users", { headers: { Authorization: `Bearer ${token}` } }),
          fetch("http://localhost:8000/api/v1/dashboard/alerts", { headers: { Authorization: `Bearer ${token}` } })
        ]);
        if (docsRes.ok) setDocumentsByMonth(await docsRes.json());
        if (usersRes.ok) setActiveUsers(await usersRes.json());
        if (alertsRes.ok) setAlerts(await alertsRes.json());
      } catch (e) {
        setAlerts(["Erro ao carregar indicadores críticos"]);
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  return { documentsByMonth, activeUsers, alerts, loading };
}
