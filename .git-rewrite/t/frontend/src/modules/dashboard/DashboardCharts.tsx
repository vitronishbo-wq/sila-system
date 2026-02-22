import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import { ChartWrapper } from './components';

interface Props {
  data: Array<{ mes: string; documentos: number }>;
}

export default function DashboardCharts({ data }: Props) {
  return (
    <ChartWrapper title="Crescimento de Documentos (2025)">
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <XAxis dataKey="mes" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="documentos"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
}
