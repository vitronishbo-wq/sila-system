import { getAlertColor } from './utils/chartHelpers';

interface Alert {
  msg: string;
  nivel: string;
}

interface Props {
  alerts: Alert[];
}

export default function DashboardAlerts({ alerts }: Props) {
  return (
    <div style={{ marginTop: '3rem' }}>
      {alerts.map((a, i) => {
        const colors = getAlertColor(a.nivel);
        return (
          <div key={i} style={{
            background: colors.bg,
            borderLeft: `6px solid ${colors.border}`,
            padding: '1.5rem',
            borderRadius: '12px',
            marginBottom: '1rem'
          }}>
            {a.msg}
          </div>
        );
      })}
    </div>
  )
}
