export interface DashboardStats {
  documentos: number
  usuarios: number
  atividades: number
  pendentes: number
}

export interface ActivityLog {
  id: number
  descricao: string
  data: string
  nivel: 'info' | 'warning' | 'critical'
}
