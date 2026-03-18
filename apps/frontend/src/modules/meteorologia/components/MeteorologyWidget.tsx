/**
 * MeteorologyWidget - Main dashboard widget
 * Complete weather monitoring system with real-time updates
 */

import React, { useState, useCallback } from 'react';
import { Cloud, AlertTriangle, MapPin, RefreshCw } from 'lucide-react';
import { useMeteorologia, useAlertas, useEstacoes } from '../hooks';
import { StationCard } from './StationCard';
import { AlertsPanel } from './AlertsPanel';
import { TrendsChart } from './TrendsChart';
import { RegionFilter } from './RegionFilter';
import type { MeteorologyFilter } from '../types';

interface MeteorologyWidgetProps {
  standalone?: boolean;
  className?: string;
}

export const MeteorologyWidget: React.FC<MeteorologyWidgetProps> = ({
  standalone = false,
  className = '',
}) => {
  const [filter, setFilter] = useState<MeteorologyFilter>({});
  const [displayMode, setDisplayMode] = useState<'grid' | 'list' | 'map'>('grid');
  const [selectedEstacaoId, setSelectedEstacaoId] = useState<string | null>(null);

  const { stats, estacoes, alertas, loading, error, refetch } = useMeteorologia();
  const { alertas: filteredAlertas, resolveAlerta } = useAlertas(filter.provincia);
  const { data: estacaoData } = useEstacoes(filter);

  const handleFilterChange = useCallback((newFilter: MeteorologyFilter) => {
    setFilter(newFilter);
    setSelectedEstacaoId(null);
  }, []);

  const displayEstacoes = estacaoData?.items || estacoes;

  const StatCard = ({ icon: Icon, label, value, trend }: any) => (
    <div className="bg-white rounded-lg shadow p-4 flex items-start gap-3">
      <div className="p-3 bg-blue-100 rounded-lg">
        <Icon className="h-6 w-6 text-blue-600" />
      </div>
      <div>
        <div className="text-xs text-gray-600">{label}</div>
        <div className="text-2xl font-bold">{value}</div>
        {trend && <div className="text-xs text-green-600 mt-1">{trend}</div>}
      </div>
    </div>
  );

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold flex items-center gap-2">
            <Cloud className="h-8 w-8" />
            Monitoramento Climático
          </h2>
          <p className="text-gray-600 mt-1">
            Sistema de monitoramento de estações meteorológicas e emissão de alertas climáticos
          </p>
        </div>
        <button
          onClick={() => refetch()}
          disabled={loading}
          className="p-2 hover:bg-gray-100 rounded transition disabled:opacity-50"
        >
          <RefreshCw className={`h-6 w-6 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Summary Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard
            icon={MapPin}
            label="Estações Ativas"
            value={stats.estacoes_ativas}
            trend={`de ${stats.total_estacoes}`}
          />
          <StatCard icon={Cloud} label="Observações 24h" value={stats.observacoes_ultimas_24h} />
          <StatCard icon={AlertTriangle} label="Alertas Ativos" value={stats.alertas_ativos} trend="status" />
          <StatCard
            icon={Cloud}
            label="Temperat. Média"
            value={`${stats.temperatura_media.toFixed(1)}°C`}
          />
          <StatCard icon={Cloud} label="Precipitação" value={`${stats.precipitacao_total.toFixed(1)} mm`} />
          <StatCard icon={Cloud} label="Estações" value={stats.total_estacoes} />
        </div>
      )}

      {/* Filter & View Controls */}
      <div className="flex gap-3 items-center flex-wrap">
        <div className="flex gap-2">
          <button
            onClick={() => setDisplayMode('grid')}
            className={`px-3 py-2 rounded text-sm font-medium transition ${
              displayMode === 'grid'
                ? 'bg-gray-900 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Grade
          </button>
          <button
            onClick={() => setDisplayMode('list')}
            className={`px-3 py-2 rounded text-sm font-medium transition ${
              displayMode === 'list'
                ? 'bg-gray-900 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Lista
          </button>
        </div>
        {standalone && (
          <button className="ml-auto px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition text-sm font-medium">
            Exportar Dados
          </button>
        )}
      </div>

      {/* Main Content Grid */}
      <div className={`grid ${standalone ? 'grid-cols-4' : 'grid-cols-3'} gap-4`}>
        {/* Left: Filter Sidebar */}
        <div className="col-span-1">
          <RegionFilter onFilterChange={handleFilterChange} />
        </div>

        {/* Center: Stations */}
        <div className="col-span-2">
          {displayMode === 'grid' ? (
            <div className="grid grid-cols-2 gap-4">
              {displayEstacoes.slice(0, 4).map((estacao) => (
                <div
                  key={estacao.id}
                  onClick={() => setSelectedEstacaoId(estacao.id)}
                  className={`cursor-pointer transition ${
                    selectedEstacaoId === estacao.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                >
                  <StationCard estacaoId={estacao.id} estacao={estacao} />
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {displayEstacoes.map((estacao) => (
                <div
                  key={estacao.id}
                  onClick={() => setSelectedEstacaoId(estacao.id)}
                  className={`bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-md transition flex items-center justify-between ${
                    selectedEstacaoId === estacao.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                >
                  <div>
                    <h4 className="font-semibold">{estacao.nome}</h4>
                    <p className="text-sm text-gray-600">{estacao.municipio}</p>
                  </div>
                  <span className={`px-3 py-1 rounded text-xs font-medium ${
                    estacao.status === 'ACTIVE'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {estacao.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right: Alerts */}
        <div className="col-span-1">
          <AlertsPanel
            alertas={filteredAlertas}
            loading={loading}
            onResolve={resolveAlerta}
          />
        </div>
      </div>

      {/* Selected Station Details */}
      {selectedEstacaoId && (
        <div className="border-t pt-6">
          <h3 className="font-bold text-lg mb-4">Análise Detalhada</h3>
          <div className="grid grid-cols-2 gap-4">
            <TrendsChart estacaoId={selectedEstacaoId} initialDays={7} />
            <TrendsChart estacaoId={selectedEstacaoId} initialDays={30} />
          </div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-300 rounded p-4 text-red-800">
          <strong>Erro:</strong> {error.message}
        </div>
      )}
    </div>
  );
};
