/**
 * StationCard Component
 * Displays real-time weather data for a single station
 */

import React from "react";
import {
  Cloud,
  CloudRain,
  CloudSnow,
  Droplets,
  Wind,
  Gauge,
  MapPin,
  AlertTriangle,
  TrendingUp,
  AlertCircle,
} from "lucide-react";
import { MeteorologiaEstacao } from "../types";
import { useEstacao, useAlertas } from "../hooks";

interface StationCardProps {
  estacaoId: string;
  estacao?: MeteorologiaEstacao;
  className?: string;
}

export function StationCard({
  estacaoId,
  estacao: initialEstacao,
  className = "",
}: StationCardProps) {
  const { estacao, observacao } = useEstacao(estacaoId);
  const { alertas } = useAlertas();

  const finalEstacao = estacao || initialEstacao;
  const stationAlerts = alertas.filter((a) => a.parametro === estacaoId);
  const highestSeverity = stationAlerts.reduce((max, alert) => {
    const severities = {
      ALERTA_VERMELHO: 3,
      ALERTA_LARANJA: 2,
      ALERTA_AMARELO: 1,
    };
    return Math.max(max, severities[alert.tipo] || 0);
  }, 0);

  const getWeatherIcon = () => {
    const temp = observacao?.temperatura || 0;
    const precip = observacao?.precipitacao || 0;

    if (temp <= 0) return <CloudSnow className="w-12 h-12 text-blue-400" />;
    if (precip > 5) return <CloudRain className="w-12 h-12 text-blue-600" />;
    return <Cloud className="w-12 h-12 text-gray-400" />;
  };

  const getAlertBadgeColor = () => {
    if (highestSeverity === 3)
      return "bg-red-100 text-red-800 border-red-300";
    if (highestSeverity === 2)
      return "bg-orange-100 text-orange-800 border-orange-300";
    if (highestSeverity === 1)
      return "bg-yellow-100 text-yellow-800 border-yellow-300";
    return "bg-gray-100 text-gray-800 border-gray-300";
  };

  return (
    <div
      className={`bg-white rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow relative ${className}`}
    >
      {/* Alert Badge */}
      {stationAlerts.length > 0 && (
        <div
          className={`absolute top-3 right-3 px-2 py-1 rounded text-xs font-semibold border ${getAlertBadgeColor()}`}
        >
          {highestSeverity === 3 && <AlertTriangle className="w-3 h-3 inline mr-1" />}
          {stationAlerts.length} alertas
        </div>
      )}

      {/* Header */}
      <div className="mb-4">
        <h3 className="font-bold text-lg text-gray-900">{finalEstacao?.nome}</h3>
        <div className="flex items-center text-sm text-gray-600 mt-1">
          <MapPin className="w-4 h-4 mr-1" />
          {finalEstacao?.municipio}, {finalEstacao?.provincia}
        </div>
      </div>

      {/* Temperature Display */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-4xl font-bold text-gray-900">
            {observacao?.temperatura?.toFixed(1) || "—"}°C
          </div>
          <p className="text-xs text-gray-500 mt-1">
            {observacao?.data_observacao
              ? new Date(observacao.data_observacao).toLocaleTimeString("pt-PT")
              : "sem dados"}
          </p>
        </div>
        <div>{getWeatherIcon()}</div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-blue-50 rounded p-3">
          <div className="flex items-center mb-1">
            <Droplets className="w-4 h-4 text-blue-600 mr-2" />
            <span className="text-xs text-gray-600">Humidade</span>
          </div>
          <p className="text-lg font-semibold text-blue-900">
            {observacao?.humidade?.toFixed(0) || "—"}%
          </p>
        </div>

        <div className="bg-green-50 rounded p-3">
          <div className="flex items-center mb-1">
            <Wind className="w-4 h-4 text-green-600 mr-2" />
            <span className="text-xs text-gray-600">Vento</span>
          </div>
          <p className="text-lg font-semibold text-green-900">
            {observacao?.velocidade_vento?.toFixed(1) || "—"} m/s
          </p>
        </div>

        <div className="bg-purple-50 rounded p-3">
          <div className="flex items-center mb-1">
            <Gauge className="w-4 h-4 text-purple-600 mr-2" />
            <span className="text-xs text-gray-600">Pressão</span>
          </div>
          <p className="text-lg font-semibold text-purple-900">
            {observacao?.pressao?.toFixed(0) || "—"} hPa
          </p>
        </div>

        <div className="bg-cyan-50 rounded p-3">
          <div className="flex items-center mb-1">
            <CloudRain className="w-4 h-4 text-cyan-600 mr-2" />
            <span className="text-xs text-gray-600">Precipitação</span>
          </div>
          <p className="text-lg font-semibold text-cyan-900">
            {observacao?.precipitacao?.toFixed(1) || "—"} mm
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-gray-600 border-t border-gray-200 pt-3">
        <span className="bg-gray-100 px-2 py-1 rounded">
          {observacao?.qualidade_dados || "PRELIMINAR"}
        </span>
        <TrendingUp className="w-4 h-4 text-green-600" />
      </div>
    </div>
  );
}
