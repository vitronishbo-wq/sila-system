import { FC } from "react";

interface AlertProps {
  alerts: string[];
}

const AlertList: FC<AlertProps> = ({ alerts }) => {
  if (!alerts.length) return null;
  return (
    <div style={{ margin: "1rem 0" }}>
      {alerts.map((alert, i) => (
        <div key={i} style={{ background: "#fee2e2", color: "#991b1b", padding: "0.75rem 1rem", borderRadius: 8, marginBottom: 8 }}>
          {alert}
        </div>
      ))}
    </div>
  );
};

export default AlertList;
