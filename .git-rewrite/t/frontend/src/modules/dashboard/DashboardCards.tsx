interface DashboardStats {
  documentos: number
  usuarios: number
  atividades: number
  pendentes: number
}

interface Props {
  stats: DashboardStats
}

export default function DashboardCards({ stats }: Props) {
  const cards = [
    { title: 'Documentos', value: stats.documentos, color: '#2563eb' },
    { title: 'Usuários', value: stats.usuarios, color: '#16a34a' },
    { title: 'Atividades', value: stats.atividades, color: '#7c3aed' },
    { title: 'Pendentes', value: stats.pendentes, color: '#ea580c' }
  ]

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
      gap: '2rem'
    }}>
      {cards.map(c => (
        <div key={c.title} style={{
          background: 'white',
          padding: '2.2rem',
          borderRadius: '18px',
          boxShadow: '0 12px 28px rgba(0,0,0,.1)'
        }}>
          <p style={{ color: '#6b7280' }}>{c.title}</p>
          <p style={{ fontSize: '3.5rem', fontWeight: 'bold', color: c.color }}>
            {c.value}
          </p>
        </div>
      ))}
    </div>
  )
}
