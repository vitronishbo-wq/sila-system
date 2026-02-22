export function formatChartData(data: any[]) {
  return data.map((item) => ({
    ...item,
    documentos: Number(item.documentos) || 0
  }));
}

export function getAlertColor(nivel: string): { bg: string; border: string } {
  switch (nivel) {
    case 'warning':
      return { bg: '#fff7ed', border: '#f97316' };
    case 'critical':
      return { bg: '#fee2e2', border: '#dc2626' };
    case 'info':
    default:
      return { bg: '#ecfeff', border: '#06b6d4' };
  }
}
