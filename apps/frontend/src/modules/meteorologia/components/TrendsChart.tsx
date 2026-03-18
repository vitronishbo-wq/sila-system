/**
 * TrendsChart - Historical weather trends visualization
 * Line charts for temperature, humidity, wind, precipitation
 */

import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Calendar, Download } from 'lucide-react';
import { useTrendData } from '../hooks';
import type { TrendData } from '../types';

interface TrendsChartProps {
  estacaoId: string;
  initialDays?: number;
  className?: string;
}

export const TrendsChart: React.FC<TrendsChartProps> = ({
  estacaoId,
  initialDays = 7,
  className = '',
}) => {
  const [selectedParam, setSelectedParam] = useState<'temperatura' | 'humidade' | 'precipitacao' | 'velocidade_vento'>(
    'temperatura'
  );

  const calculateDateRange = (days: number) => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    return {
      dataInicio: start.toISOString().split('T')[0],
      dataFim: end.toISOString().split('T')[0],
    };
  };

  const { dataInicio, dataFim } = calculateDateRange(initialDays);
  const { trendData, loading, error } = useTrendData(estacaoId, selectedParam, dataInicio, dataFim);

  const paramLabels = {
    temperatura: 'Temperatura (°C)',
    humidade: 'Humidade (%)',
    precipitacao: 'Precipitação (mm)',
    velocidade_vento: 'Velocidade do Vento (m/s)',
  };

  const paramColors = {
    temperatura: '#ef4444',
    humidade: '#3b82f6',
    precipitacao: '#0ea5e9',
    velocidade_vento: '#10b981',
  };

  if (loading) {
    return <div className={`bg-white rounded-lg shadow p-8 text-center text-gray-500 ${className}`}>Carregando tendências...</div>;
  }

  if (error) {
    return <div className={`bg-white rounded-lg shadow p-8 text-center text-red-600 ${className}`}>Erro ao carregar dados</div>;
  }

  if (!trendData) {
    return <div className={`bg-white rounded-lg shadow p-8 text-center text-gray-500 ${className}`}>Sem dados disponíveis</div>;
  }

  // Simple ASCII chart for demonstration
  const renderChart = () => {
    const { data, minValue, maxValue } = trendData;
    const range = maxValue - minValue || 1;
    const chartHeight = 10;

    const normalized = data.map((v) => Math.round(((v - minValue) / range) * (chartHeight - 1)));

    return (
      <div className="space-y-2 mt-4">
        {/* Y-axis labels */}
        <div className="relative h-32">
          {Array.from({ length: 5 }).map((_, i) => {
            const value = minValue + ((4 - i) / 4) * range;
            return (
              <div key={i} className="absolute w-full text-xs text-gray-600" style={{ top: `${i * 25}%` }}>
                <span>{value.toFixed(1)}</span>
                <div className="h-px bg-gray-200 flex-1 -ml-6" />
              </div>
            );
          })}

          {/* Chart bars */}
          <div className="flex items-end justify-between h-full gap-1 mt-2">
            {normalized.slice(0, Math.min(50, normalized.length)).map((val, i) => (
              <div
                key={i}
                className="flex-1 bg-gradient-to-t rounded-t transition hover:opacity-80"
                style={{
                  backgroundColor: paramColors[selectedParam],
                  height: `${(val / (chartHeight - 1)) * 100}%`,
                  minHeight: '2px',
                }}
                title={`${trendData.data[i]?.toFixed(2)} ${trendData.unidade}`}
              />
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-4 gap-2 mt-6 pt-4 border-t">
          <div className="text-center">
            <div className="text-xs text-gray-600">Mínimo</div>
            <div className="font-bold">{minValue.toFixed(1)}</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-600">Máximo</div>
            <div className="font-bold">{maxValue.toFixed(1)}</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-600">Média</div>
            <div className="font-bold">{trendData.avgValue.toFixed(1)}</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-600">Unidade</div>
            <div className="font-bold">{trendData.unidade}</div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg flex items-center gap-2">
          <TrendingUp className="h-5 w-5" />
          Tendências ({initialDays} dias)
        </h3>
        <button className="p-2 hover:bg-gray-100 rounded transition">
          <Download className="h-5 w-5 text-gray-600" />
        </button>
      </div>

      {/* Parameter Selection */}
      <div className="grid grid-cols-4 gap-2 mb-4">
        {Object.entries(paramLabels).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setSelectedParam(key as 'temperatura' | 'humidade' | 'precipitacao' | 'velocidade_vento')}
            className={`px-3 py-2 rounded text-sm font-medium transition ${
              selectedParam === key
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {label.split(' ')[0]}
          </button>
        ))}
      </div>

      {/* Chart */}
      {renderChart()}

      {/* Legend */}
      <div className="mt-4 text-xs text-gray-600 flex items-center gap-2">
        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: paramColors[selectedParam] }} />
        <span>{paramLabels[selectedParam]}</span>
      </div>
    </div>
  );
};
