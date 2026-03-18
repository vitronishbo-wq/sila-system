/**
 * TrendsChart Component
 * Visualizes historical weather trends with ASCII bar chart
 */

import React, { useState } from "react";
import {
  Download,
  TrendingUp,
  BarChart3,
} from "lucide-react";
import { useTrendData, getUnidade } from "../hooks";

interface TrendsChartProps {
  estacaoId: string;
  initialDays?: number;
  className?: string;
}

export function TrendsChart({
  estacaoId,
  initialDays = 7,
  className = "",
}: TrendsChartProps) {
  const [selectedParameter, setSelectedParameter] = useState("temperatura");
  const [days, setDays] = useState(initialDays);

  const today = new Date();
  const startDate = new Date(today);
  startDate.setDate(startDate.getDate() - days);

  const { trendData, loading } = useTrendData(
    estacaoId,
    selectedParameter,
    startDate.toISOString().split("T")[0],
    today.toISOString().split("T")[0]
  );

  const parameters = [
    { id: "temperatura", label: "Temperatura", color: "text-red-600" },
    { id: "humidade", label: "Humidade", color: "text-blue-600" },
    { id: "precipitacao", label: "Precipitação", color: "text-cyan-600" },
    { id: "velocidade_vento", label: "Velocidade Vento", color: "text-green-600" },
  ];

  const renderChart = () => {
    if (!trendData || trendData.data.length === 0) {
      return <div className="text-center py-8 text-gray-500">Sem dados</div>;
    }

    const { data, minValue, maxValue } = trendData;
    const range = maxValue - minValue || 1;
    const height = 200;
    const barWidth = Math.max(2, Math.floor(400 / data.length));
    const yTickCount = 5;

    // Generate Y-axis ticks
    const yTicks = Array.from({ length: yTickCount }, (_, i) => {
      const ratio = i / (yTickCount - 1);
      return minValue + ratio * range;
    });

    return (
      <div className="mt-4">
        <div className="flex">
          {/* Y-axis */}
          <div className="flex flex-col justify-between py-2 pr-2 text-xs text-gray-600 font-mono w-16">
            {yTicks.reverse().map((tick) => (
              <div key={tick}>{tick.toFixed(1)}</div>
            ))}
          </div>

          {/* Chart Area */}
          <div className="flex-1 relative" style={{ height: `${height}px` }}>
            <svg
              viewBox={`0 0 400 ${height}`}
              className="w-full h-full"
              preserveAspectRatio="none"
            >
              {/* Grid lines */}
              {yTicks.map((_, i) => {
                const yPos = (i / (yTickCount - 1)) * height;
                return (
                  <line
                    key={`grid-${i}`}
                    x1="0"
                    y1={yPos}
                    x2="400"
                    y2={yPos}
                    stroke="#f0f0f0"
                    strokeWidth="1"
                  />
                );
              })}

              {/* Bars */}
              {data.map((value, i) => {
                const normalized = (value - minValue) / range;
                const barHeight = normalized * (height - 4);
                const yPos = height - barHeight;
                const xPos = (i / data.length) * 400;

                return (
                  <g key={i}>
                    <rect
                      x={xPos}
                      y={yPos}
                      width={barWidth - 1}
                      height={barHeight}
                      fill={
                        selectedParameter === "temperatura"
                          ? "#dc2626"
                          : selectedParameter === "humidade"
                            ? "#2563eb"
                            : selectedParameter === "precipitacao"
                              ? "#06b6d4"
                              : "#16a34a"
                      }
                      opacity="0.8"
                      title={`${value.toFixed(2)}`}
                    />
                  </g>
                );
              })}
            </svg>
          </div>
        </div>

        {/* X-axis labels (every Nth point) */}
        <div className="flex mt-2 pl-16 text-xs text-gray-600 font-mono">
          {trendData.timestamps.slice(0, 5).map((ts, i) => (
            <div
              key={i}
              className="flex-1 text-center"
              style={{
                marginLeft: `${(i * 80) / trendData.timestamps.length}px`,
              }}
            >
              {new Date(ts).toLocaleDateString("pt-PT")}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 ${className}`}>
      {/* Header */}
      <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center">
        <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
        Tendências ({days} dias)
      </h3>

      {/* Parameter Selection */}
      <div className="flex flex-wrap gap-2 mb-4">
        {parameters.map((param) => (
          <button
            key={param.id}
            onClick={() => setSelectedParameter(param.id)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              selectedParameter === param.id
                ? "bg-gray-900 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {param.label}
          </button>
        ))}
      </div>

      {/* Date Range Selector */}
      <div className="flex gap-2 mb-4">
        {[7, 14, 30].map((d) => (
          <button
            key={d}
            onClick={() => setDays(d)}
            className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
              days === d
                ? "bg-blue-600 text-white"
                : "border border-gray-300 text-gray-700 hover:bg-gray-50"
            }`}
          >
            {d}d
          </button>
        ))}
      </div>

      {/* Chart */}
      {loading ? (
        <div className="text-center py-8 text-gray-500">Carregando tendências...</div>
      ) : (
        renderChart()
      )}

      {/* Statistics */}
      {trendData && (
        <div className="grid grid-cols-4 gap-3 mt-4 p-3 bg-gray-50 rounded">
          <div>
            <p className="text-xs text-gray-600">Mínimo</p>
            <p className="font-bold text-gray-900">
              {trendData.minValue.toFixed(2)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Máximo</p>
            <p className="font-bold text-gray-900">
              {trendData.maxValue.toFixed(2)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Média</p>
            <p className="font-bold text-gray-900">
              {trendData.avgValue.toFixed(2)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Unidade</p>
            <p className="font-bold text-gray-900">{trendData.unidade}</p>
          </div>
        </div>
      )}

      {/* Download Button */}
      <button className="mt-4 w-full flex items-center justify-center gap-2 px-3 py-2 rounded border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors">
        <Download className="w-4 h-4" />
        Exportar Dados
      </button>
    </div>
  );
}
