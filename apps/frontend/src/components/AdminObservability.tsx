import React, { useEffect, useMemo, useState } from 'react';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import { getSLAViolations, listSLAServiceBase, predictSLABreach } from '@/services/sla';
import type { SLABreachPrediction, SLAViolation } from '@/services/sla';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Tooltip, Legend);

const AdminObservability: React.FC = () => {
  const [violations, setViolations] = useState<SLAViolation[]>([]);
  const [services, setServices] = useState<{ service_id: string; service_name: string }[]>([]);
  const [selectedService, setSelectedService] = useState('');
  const [slaPrediction, setSlaPrediction] = useState<SLABreachPrediction | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [violationsData, servicesData] = await Promise.all([
        getSLAViolations({ days: 7 }),
        listSLAServiceBase(),
      ]);
      setViolations(violationsData);
      setServices(servicesData.map((service) => ({ service_id: service.service_id, service_name: service.service_name })));
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceSelect = async (serviceId: string) => {
    setSelectedService(serviceId);
    if (serviceId) {
      const prediction = await predictSLABreach(serviceId, 0);
      setSlaPrediction(prediction);
    } else {
      setSlaPrediction(null);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return '#ef4444';
      case 'medium':
        return '#f59e0b';
      default:
        return '#3b82f6';
    }
  };

  const violationsByService = useMemo(() => {
    return violations.reduce((acc, v) => {
      const name = v.service_name || v.service_id;
      acc[name] = (acc[name] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
  }, [violations]);

  const violationSeries = useMemo(() => {
    const buckets: Record<string, number> = {};
    violations.forEach((v) => {
      const date = new Date(v.created_at);
      const key = date.toISOString().slice(0, 10);
      buckets[key] = (buckets[key] || 0) + 1;
    });
    const labels = Object.keys(buckets).sort();
    return {
      labels,
      data: labels.map((label) => buckets[label]),
    };
  }, [violations]);

  const avgDelay = useMemo(() => {
    if (!violations.length) return 0;
    const total = violations.reduce((acc, v) => acc + v.delta_hours, 0);
    return Math.round(total / violations.length);
  }, [violations]);

  const affectedProvinces = useMemo(() => new Set(violations.map((v) => v.province)).size, [violations]);

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Observabilidade de SLAs</h1>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <KpiCard label="Total Violações (7d)" value={violations.length} />
        <KpiCard label="Severidade Alta" value={violations.filter((v) => v.severity === 'high').length} accent="text-red-500" />
        <KpiCard label="Média Atraso" value={`${avgDelay}h`} />
        <KpiCard label="Províncias Afetadas" value={affectedProvinces} />
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <div className="rounded-lg bg-white p-4 shadow">
          <h2 className="mb-4 text-lg font-semibold">Violações por Serviço</h2>
          <Bar
            data={{
              labels: Object.keys(violationsByService),
              datasets: [
                {
                  label: 'Nº de Violações',
                  data: Object.values(violationsByService),
                  backgroundColor: '#3b82f6',
                },
              ],
            }}
          />
        </div>

        <div className="rounded-lg bg-white p-4 shadow">
          <h2 className="mb-4 text-lg font-semibold">Evolução das Violações</h2>
          <Line
            data={{
              labels: violationSeries.labels,
              datasets: [
                {
                  label: 'Ocorrências',
                  data: violationSeries.data,
                  borderColor: '#0ea5e9',
                  backgroundColor: 'rgba(14, 165, 233, 0.2)',
                  tension: 0.3,
                  fill: true,
                },
              ],
            }}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <div className="rounded-lg bg-white p-4 shadow">
          <h2 className="mb-4 text-lg font-semibold">Predicção de SLA</h2>
          <select
            className="mb-4 w-full rounded border p-2"
            value={selectedService}
            onChange={(e) => handleServiceSelect(e.target.value)}
          >
            <option value="">Selecione um serviço</option>
            {services.map((service) => (
              <option key={service.service_id} value={service.service_id}>
                {service.service_name}
              </option>
            ))}
          </select>

          {slaPrediction && (
            <div className="space-y-4">
              <div className="flex justify-between">
                <span>Progresso:</span>
                <span className="font-bold">{slaPrediction.progress_percentage}%</span>
              </div>

              <div className="h-4 w-full rounded-full bg-gray-200">
                <div
                  className="h-4 rounded-full bg-blue-600"
                  style={{ width: `${slaPrediction.progress_percentage}%` }}
                />
              </div>

              <div className="flex justify-between">
                <span>Probabilidade de Violação:</span>
                <span className={`font-bold ${slaPrediction.breach_probability > 0.7 ? 'text-red-500' : 'text-green-500'}`}>
                  {Math.round(slaPrediction.breach_probability * 100)}%
                </span>
              </div>

              {slaPrediction.risk_factors.length > 0 && (
                <div>
                  <span className="font-semibold">Fatores de Risco:</span>
                  <ul className="mt-2 list-disc pl-5">
                    {slaPrediction.risk_factors.map((factor) => (
                      <li key={factor} className="text-red-500">
                        {factor}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="rounded-lg bg-white p-4 shadow">
          <h2 className="mb-4 text-lg font-semibold">Violações Recentes</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="p-3">Serviço</th>
                  <th className="p-3">Província</th>
                  <th className="p-3">SLA Alvo</th>
                  <th className="p-3">Tempo Real</th>
                  <th className="p-3">Atraso</th>
                  <th className="p-3">Severidade</th>
                  <th className="p-3">Data</th>
                </tr>
              </thead>
              <tbody>
                {violations.slice(0, 10).map((violation) => (
                  <tr key={violation.id} className="border-t">
                    <td className="p-3">{violation.service_name || violation.service_id}</td>
                    <td className="p-3">{violation.province}</td>
                    <td className="p-3">{violation.target_hours}h</td>
                    <td className="p-3">{violation.actual_hours}h</td>
                    <td className="p-3 text-red-500">+{violation.delta_hours}h</td>
                    <td className="p-3">
                      <span
                        className="rounded px-2 py-1 text-sm text-white"
                        style={{ backgroundColor: getSeverityColor(violation.severity) }}
                      >
                        {violation.severity}
                      </span>
                    </td>
                    <td className="p-3">{new Date(violation.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

const KpiCard: React.FC<{ label: string; value: string | number; accent?: string }> = ({ label, value, accent }) => (
  <div className="rounded-lg bg-white p-4 shadow">
    <div className="text-sm text-gray-500">{label}</div>
    <div className={`text-3xl font-bold ${accent || ''}`}>{value}</div>
  </div>
);

export default AdminObservability;
