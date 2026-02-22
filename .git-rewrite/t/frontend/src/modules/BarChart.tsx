import { ChartDataPoint } from "../../services/dashboard";
import { FC } from "react";

interface BarChartProps {
  data: ChartDataPoint[];
  height?: number;
}

const BarChart: FC<BarChartProps> = ({ data, height = 180 }) => {
  const max = Math.max(...data.map((d) => d.value), 1);
  return (
    <svg width="100%" height={height} viewBox={`0 0 ${data.length * 40} ${height}`} style={{ background: "#f9fafb", borderRadius: 8 }}>
      {data.map((d, i) => (
        <g key={d.label}>
          <rect
            x={i * 40 + 10}
            y={height - (d.value / max) * (height - 40) - 20}
            width={20}
            height={(d.value / max) * (height - 40)}
            fill="#3b82f6"
            rx={4}
          />
          <text
            x={i * 40 + 20}
            y={height - 5}
            textAnchor="middle"
            fontSize={12}
            fill="#374151"
          >
            {d.label}
          </text>
          <text
            x={i * 40 + 20}
            y={height - (d.value / max) * (height - 40) - 25}
            textAnchor="middle"
            fontSize={12}
            fill="#111827"
          >
            {d.value}
          </text>
        </g>
      ))}
    </svg>
  );
};

export default BarChart;
