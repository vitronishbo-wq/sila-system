/**
 * MeteorologyWidget Component
 * Main composite dashboard combining all meteorologia subcomponents
 */

import React, { useState } from "react";
import {
  Cloud,
  RefreshCw,
  Grid3x3,
  List,
  Download,
  AlertCircle,
} from "lucide-react";
import { MeteorologyFilter } from "../types";
import { useMeteorologia, useEstacoes, useAlertas } from "../hooks";
import { meteorologiaService } from "../services";
import {
  StationCard,
  AlertsPanel,
  TrendsChart,
  RegionFilter,
} from "./index";

interface MeteorologyWidgetProps {
  standalone?: boolean;
  className?: string;
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  trend?: "up" | "down";
  className?: string;
}

function StatCard({
  icon,
  label,
  value,
  trend,
  className = "",
}: StatCardProps) {
  return (
    <div className={`bg-white p-4 rounded-lg border border-gray-200 ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="text-blue-600 opacity-20">{icon}</div>
      </div>
    </div>
  );
}

export function MeteorologyWidget({
  standalone = false,
  className = "",
}: MeteorologyWidgetProps) {
  const { stats, estacoes, alertas, loading, error, refetch } =
    useMeteorologia();
  const [filter, setFilter] = useState<MeteorologyFilter>({});
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [selectedEstacao, setSelectedEstacao] = useState<string | null>(null);

  const { estacoes: estacoesFiltradas } = useEstacoes(
    filter,
    { page: 1, limit: 20 }
  );
  const { alertas: alertasFiltradas } = useAlertas(filter.provincia);

  const displayEstacoes = estacoesFiltradas?.items || estacoes;

  const handleExport = async () => {
    try {
      const blob = await meteorologiaService.exportDados("csv", filter);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `meteorologia-export-${Date.now()}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  return (
    <div className={`${standalone ? "min-h-screen bg-gray-50 p-6" : ""} ${className}`}>
      <div className={standalone ? "max-w-7xl mx-auto" : ""}>
        {/* Header */}
        <div className={`mb-6 ${!standalone ? "mb-4" : ""}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Cloud className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Monitoramento Climático
                </h1>
                <p className="text-gray-600">
                  Acompanhamento em tempo real da rede de estações meteorológicas
                </p>
              </div>
            </div>

            <button
              onClick={refetch}
              disabled={loading}
              className={`p-2 rounded-lg border border-gray-300 hover:bg-gray-100 transition-colors ${
                loading ? "opacity-50 cursor-not-allowed" : ""
              }`}
              title="Atualizar dados"
            >
              <RefreshCw
                className={`w-5 h-5 ${loading ? "animate-spin" : ""}`}
              />
            </button>
          </div>
        </div>

        {/* Statistics Summary */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          <StatCard
            icon={<Cloud className="w-6 h-6" />}
            label="Estações Ativas"
            value={stats?.estacoes_ativas || 0}
          />
          <StatCard
            icon={<Cloud className="w-6 h-6" />}
            label="Obs. 24h"
            value={stats?.observacoes_ultimas_24h || 0}
          />
          <StatCard
            icon={<AlertCircle className="w-6 h-6" />}
            label="Alertas Ativos"
            value={stats?.alertas_ativos || 0}
          />
          <StatCard
            icon={<Cloud className="w-6 h-6" />}
            label="Temp. Média"
            value={`${stats?.temperatura_media?.toFixed(1) || "—"}°C`}
          />
          <StatCard
            icon={<Cloud className="w-6 h-6" />}
            label="Precipitação"
            value={`${stats?.precipitacao_total?.toFixed(1) || "—"}mm`}
          />
          <StatCard
            icon={<Cloud className="w-6 h-6" />}
            label="Total Estações"
            value={stats?.total_estacoes || 0}
          />
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 rounded border transition-colors ${
                viewMode === "grid"
                  ? "bg-blue-600 text-white border-blue-600"
                  : "border-gray-300 text-gray-700 hover:bg-gray-100"
              }`}
              title="Grid view"
            >
              <Grid3x3 className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 rounded border transition-colors ${
                viewMode === "list"
                  ? "bg-blue-600 text-white border-blue-600"
                  : "border-gray-300 text-gray-700 hover:bg-gray-100"
              }`}
              title="List view"
            >
              <List className="w-5 h-5" />
            </button>
          </div>

          {standalone && (
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4" />
              Exportar Dados
            </button>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-300 rounded-lg text-red-900 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Erro ao carregar dados</p>
              <p className="text-sm mt-1">{error.message}</p>
            </div>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Filters */}
          <div className="lg:col-span-3">
            <RegionFilter onFilterChange={setFilter} />
          </div>

          {/* Middle Column - Stations */}
          <div className="lg:col-span-6">
            {loading ? (
              <div className="bg-white rounded-lg border border-gray-200 p-8 text-center text-gray-500">
                Carregando estações...
              </div>
            ) : viewMode === "grid" ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {displayEstacoes.slice(0, 4).map((estacao) => (
                  <div
                    key={estacao.id}
                    onClick={() => setSelectedEstacao(estacao.id)}
                    className={`cursor-pointer ring-2 ring-offset-2 transition-all ${
                      selectedEstacao === estacao.id
                        ? "ring-blue-500"
                        : "ring-transparent hover:ring-gray-300"
                    }`}
                  >
                    <StationCard estacaoId={estacao.id} estacao={estacao} />
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {displayEstacoes.map((estacao) => (
                  <div
                    key={estacao.id}
                    onClick={() => setSelectedEstacao(estacao.id)}
                    className={`cursor-pointer p-4 bg-white rounded-lg border-2 transition-all ${
                      selectedEstacao === estacao.id
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-gray-900">
                          {estacao.nome}
                        </p>
                        <p className="text-sm text-gray-600">
                          {estacao.municipio}, {estacao.provincia}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-gray-500">Status</p>
                        <p className="font-semibold text-gray-900">
                          {estacao.status}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Selected Station Details */}
            {selectedEstacao && (
              <div className="mt-6 pt-6 border-t border-gray-300">
                <h3 className="font-bold text-lg text-gray-900 mb-4">
                  Tendências da Estação
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <TrendsChart
                    estacaoId={selectedEstacao}
                    initialDays={7}
                  />
                  <TrendsChart
                    estacaoId={selectedEstacao}
                    initialDays={30}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Alerts */}
          <div className="lg:col-span-3">
            <AlertsPanel
              alertas={alertasFiltradas}
              loading={loading}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
