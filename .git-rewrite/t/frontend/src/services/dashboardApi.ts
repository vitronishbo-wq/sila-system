export async function fetchDashboardStats(token: string): Promise<any> {
  const res = await fetch("http://localhost:8000/api/v1/dashboard/stats", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Erro ao buscar estatísticas do dashboard");
  return res.json();
}

export async function fetchDashboardChart(token: string): Promise<Array<{ mes: string; documentos: number }>> {
  const res = await fetch("http://localhost:8000/api/v1/dashboard/chart", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Erro ao buscar dados do gráfico");
  return res.json();
}

export async function fetchDashboardAlerts(token: string): Promise<Array<{ msg: string; nivel: string }>> {
  const res = await fetch("http://localhost:8000/api/v1/dashboard/alerts", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Erro ao buscar alertas");
  return res.json();
}
