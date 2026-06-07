/**
 * StationCard - Individual weather station display
 * Shows current conditions with temperature, humidity, wind, pressure
 */

import React, { useEffect, useState } from 'react';
import {
  Cloud,
  CloudRain,
  CloudSnow,
  Wind,
  Droplets,
  Gauge,
  MapPin,
  AlertTriangle,
  TrendingUp,
} from 'lucide-react';
import type { MeteorologiaEstacao, Alert } from '@/modules/meteorologia/types';
import { useEstacao, useAlertas } from '@/modules/meteorologia/hooks';

interface StationCardProps {
  estacaoId: string;
  estacao?: MeteorologiaEstacao;
  className?: string;
}

export const StationCard: React.FC<StationCardProps> = ({ estacaoId, estacao, className = '' }) => {
  const { observation, loading } = useEstacao(estacaoId);
  const { alertas: allAlertas } = useAlertas();

  const [stationAlertas, setStationAlertas] = useState<Alert[]>([]);

  // Filter alerts for this station
  useEffect(() => {
    const filtered = allAlertas.filter((a) => a.parametro === 'estacao_id' && a.valor_observado === parseFloat(estacaoId));
    setStationAlertas(filtered);
  }, [allAlertas, estacaoId]);

  if (!observation) {
    return (
      <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
        <div className="h-64 flex items-center justify-center text-gray-400">
          {loading ? 'Carregando...' : 'Dados indisponíveis'}
        </div>
      </div>
    );
  }

  const getWeatherIcon = (temp: number | undefined, precip: number | undefined) => {
    if (!temp) return null;
    if (precip && precip > 1) return <CloudRain className="h-12 w-12 text-blue-500" />;
    if (temp < 0) return <CloudSnow className="h-12 w-12 text-cyan-500" />;
    return <Cloud className="h-12 w-12 text-gray-400" />;
  };

  const getAlertLevel = () => {
    if (stationAlertas.length === 0) return null;
    const sevLevels = {
      ALERTA_VERMELHO: 3,
      ALERTA_LARANJA: 2,
      ALERTA_AMARELO: 1,
    };
    const highest = stationAlertas.reduce((max, a) => Math.max(max, sevLevels[a.tipo] || 0), 0);
    const colors = { 3: 'red', 2: 'orange', 1: 'yellow' };
    return { level: highest, color: colors[highest as keyof typeof colors] };
  };

  const alertLevel = getAlertLevel();

  return (
    <div className={`relative bg-white rounded-lg shadow hover:shadow-lg transition ${className}`}>
      {/* Alert Badge */}
      {alertLevel && (
        <div
          className={`absolute top-0 right-0 bg-${alertLevel.color}-500 text-white px-3 py-1 rounded-tr-lg rounded-bl-lg flex items-center gap-1`}
        >
          <AlertTriangle className="h-4 w-4" />
          <span className="text-xs font-bold">{stationAlertas.length} Alertas</span>
        </div>
      )}

      <div className="p-4">
        {/* Station Info */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-bold text-lg">{estacao?.nome || 'Estação'}</h3>
            <div className="flex items-center gap-1 text-sm text-gray-600">
              <MapPin className="h-3 w-3" />
              <span>{estacao?.municipio || estacao?.provincia}</span>
            </div>
          </div>
        </div>

        {/* Main Weather Display */}
        <div className="text-center py-4 border-y">
          <div className="flex justify-center mb-2">
            {getWeatherIcon(observation.temperatura, observation.precipitacao)}
          </div>
          <div className="text-4xl font-bold">
            {observation.temperatura ? `${Math.round(observation.temperatura)}°` : '-'}
          </div>
          <div className="text-sm text-gray-600 mt-1">
            {new Date(observation.data_observacao).toLocaleTimeString('pt-PT')}
          </div>
        </div>

        {/* Weather Metrics Grid */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          {/* Humidity */}
          <div className="flex items-center gap-2 p-2 bg-blue-50 rounded">
            <Droplets className="h-4 w-4 text-blue-600" />
            <div>
              <div className="text-xs text-gray-600">Humidade</div>
              <div className="font-semibold">{observation.humidade ? `${Math.round(observation.humidade)}%` : '-'}</div>
            </div>
          </div>

          {/* Wind Speed */}
          <div className="flex items-center gap-2 p-2 bg-green-50 rounded">
            <Wind className="h-4 w-4 text-green-600" />
            <div>
              <div className="text-xs text-gray-600">Vento</div>
              <div className="font-semibold">{observation.velocidade_vento ? `${observation.velocidade_vento.toFixed(1)} m/s` : '-'}</div>
            </div>
          </div>

          {/* Pressure */}
          <div className="flex items-center gap-2 p-2 bg-purple-50 rounded">
            <Gauge className="h-4 w-4 text-purple-600" />
            <div>
              <div className="text-xs text-gray-600">Pressão</div>
              <div className="font-semibold">{observation.pressao ? `${observation.pressao.toFixed(0)} hPa` : '-'}</div>
            </div>
          </div>

          {/* Precipitation */}
          <div className="flex items-center gap-2 p-2 bg-cyan-50 rounded">
            <CloudRain className="h-4 w-4 text-cyan-600" />
            <div>
              <div className="text-xs text-gray-600">Precipitação</div>
              <div className="font-semibold">{observation.precipitacao ? `${observation.precipitacao.toFixed(1)} mm` : '-'}</div>
            </div>
          </div>
        </div>

        {/* Data Quality Badge */}
        <div className="mt-4 p-2 bg-gray-100 rounded text-xs flex items-center justify-between">
          <span className="text-gray-700">Qualidade: {observation.qualidade_dados}</span>
          <TrendingUp className="h-3 w-3 text-gray-600" />
        </div>
      </div>
    </div>
  );
};
