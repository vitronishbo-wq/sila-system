/**
 * AlertsPanel Component
 * Displays and manages active weather alerts
 */

import React, { useState } from "react";
import {
  AlertTriangle,
  AlertCircle,
  ChevronDown,
  Clock,
  Zap,
} from "lucide-react";
import { Alert } from "../types";

interface AlertsPanelProps {
  alertas: Alert[];
  loading?: boolean;
  onResolve?: (alertId: string) => void;
  className?: string;
}

export function AlertsPanel({
  alertas,
  loading = false,
  onResolve,
  className = "",
}: AlertsPanelProps) {
  const [activeFilter, setActiveFilter] = useState<string | null>(null);
  const [expandedAlertId, setExpandedAlertId] = useState<string | null>(null);
  const [resolvedAlerts, setResolvedAlerts] = useState<Set<string>>(new Set());

  const getAlertConfig = (tipo: string) => {
    const configs: Record<string, {
      bgColor: string;
      borderColor: string;
      textColor: string;
      icon: React.ReactNode;
      severity: number;
    }> = {
      ALERTA_VERMELHO: {
        bgColor: "bg-red-50",
        borderColor: "border-red-300",
        textColor: "text-red-900",
        icon: <AlertTriangle className="w-4 h-4" />,
        severity: 3,
      },
      ALERTA_LARANJA: {
        bgColor: "bg-orange-50",
        borderColor: "border-orange-300",
        textColor: "text-orange-900",
        icon: <AlertTriangle className="w-4 h-4" />,
        severity: 2,
      },
      ALERTA_AMARELO: {
        bgColor: "bg-yellow-50",
        borderColor: "border-yellow-300",
        textColor: "text-yellow-900",
        icon: <AlertCircle className="w-4 h-4" />,
        severity: 1,
      },
    };
    return configs[tipo] || configs.ALERTA_AMARELO;
  };

  const alertasFiltradas = activeFilter
    ? alertas.filter((a) => a.tipo === activeFilter)
    : alertas;

  const alertasVisibles = alertasFiltradas.filter(
    (a) => !resolvedAlerts.has(a.id)
  );

  const handleResolve = (alertId: string) => {
    setResolvedAlerts((prev) => new Set([...prev, alertId]));
    onResolve?.(alertId);
    setExpandedAlertId(null);
  };

  // Count alerts by type
  const countByType = (tipo: string) => {
    return alertas.filter((a) => a.tipo === tipo).length;
  };

  return (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 ${className}`}>
      {/* Header */}
      <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center">
        <Zap className="w-5 h-5 mr-2 text-yellow-500" />
        Alertas Ativos
      </h3>

      {/* Filter Buttons */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={() => setActiveFilter(null)}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            activeFilter === null
              ? "bg-gray-900 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          Todos ({alertas.length})
        </button>

        <button
          onClick={() => setActiveFilter("ALERTA_VERMELHO")}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            activeFilter === "ALERTA_VERMELHO"
              ? "bg-red-600 text-white"
              : "bg-red-100 text-red-800 hover:bg-red-200"
          }`}
        >
          Vermelho ({countByType("ALERTA_VERMELHO")})
        </button>

        <button
          onClick={() => setActiveFilter("ALERTA_LARANJA")}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            activeFilter === "ALERTA_LARANJA"
              ? "bg-orange-600 text-white"
              : "bg-orange-100 text-orange-800 hover:bg-orange-200"
          }`}
        >
          Laranja ({countByType("ALERTA_LARANJA")})
        </button>

        <button
          onClick={() => setActiveFilter("ALERTA_AMARELO")}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            activeFilter === "ALERTA_AMARELO"
              ? "bg-yellow-600 text-white"
              : "bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
          }`}
        >
          Amarelo ({countByType("ALERTA_AMARELO")})
        </button>
      </div>

      {/* Alerts List */}
      <div className="max-h-96 overflow-y-auto">
        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando alertas...</div>
        ) : alertasVisibles.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            Nenhum alerta neste momento
          </div>
        ) : (
          <div className="space-y-2">
            {alertasVisibles.map((alerta, index) => {
              const config = getAlertConfig(alerta.tipo);
              const isExpanded = expandedAlertId === alerta.id;

              return (
                <div
                  key={alerta.id}
                  className={`${config.bgColor} border ${config.borderColor} rounded p-3 transition-all`}
                >
                  {/* Alert Header (Clickable) */}
                  <button
                    onClick={() =>
                      setExpandedAlertId(isExpanded ? null : alerta.id)
                    }
                    className="w-full text-left flex items-start justify-between hover:opacity-75"
                  >
                    <div className="flex items-start flex-1">
                      <div className={`${config.textColor} mt-1 mr-2`}>
                        {config.icon}
                      </div>
                      <div className="flex-1">
                        <p className={`font-semibold ${config.textColor}`}>
                          {alerta.titulo}
                        </p>
                        <p className={`text-xs ${config.textColor} opacity-75`}>
                          {alerta.parametro}
                        </p>
                      </div>
                    </div>
                    <ChevronDown
                      className={`w-4 h-4 ${config.textColor} transition-transform ${
                        isExpanded ? "rotate-180" : ""
                      }`}
                    />
                  </button>

                  {/* Expanded Details */}
                  {isExpanded && (
                    <div className={`mt-3 pt-3 border-t ${config.borderColor}`}>
                      <p className={`text-sm ${config.textColor} mb-2`}>
                        {alerta.descricao}
                      </p>

                      <div
                        className={`text-xs ${config.textColor} opacity-75 mb-3 space-y-1`}
                      >
                        <p>
                          Valor Observado:{" "}
                          <span className="font-semibold">
                            {alerta.valor_observado.toFixed(2)}
                          </span>
                        </p>
                        <p>
                          Valor Crítico:{" "}
                          <span className="font-semibold">
                            {alerta.valor_critico.toFixed(2)}
                          </span>
                        </p>
                        <div className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {new Date(alerta.timestamp).toLocaleString("pt-PT")}
                        </div>
                      </div>

                      {onResolve && (
                        <button
                          onClick={() => handleResolve(alerta.id)}
                          className={`w-full px-3 py-1 rounded text-xs font-semibold transition-colors text-white ${
                            config.severity === 3
                              ? "bg-red-600 hover:bg-red-700"
                              : config.severity === 2
                                ? "bg-orange-600 hover:bg-orange-700"
                                : "bg-yellow-600 hover:bg-yellow-700"
                          }`}
                        >
                          Marcar como Resolvido
                        </button>
                      )}
                    </div>
                  )}

                  {index < alertasVisibles.length - 1 && (
                    <div className="border-b border-gray-300 mt-2" />
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
