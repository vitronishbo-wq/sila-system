/**
 * AlertsPanel - Display active weather alerts
 * Shows severity levels with filtering and dismissal
 */

import React, { useState } from 'react';
import { AlertTriangle, AlertCircle, ChevronDown, X } from 'lucide-react';
import type { Alert } from '../types';

interface AlertsPanelProps {
  alertas: Alert[];
  loading?: boolean;
  onResolve?: (alertaId: string) => void;
  className?: string;
}

export const AlertsPanel: React.FC<AlertsPanelProps> = ({
  alertas,
  loading = false,
  onResolve,
  className = '',
}) => {
  const [expandedAlert, setExpandedAlert] = useState<string | null>(null);
  const [filterTipo, setFilterTipo] = useState<string | 'ALL'>('ALL');

  const getAlertConfig = (tipo: Alert['tipo']) => {
    const config = {
      ALERTA_VERMELHO: {
        bgColor: 'bg-red-50',
        borderColor: 'border-red-300',
        textColor: 'text-red-700',
        icon: AlertTriangle,
        label: 'Alerta Vermelho',
        severity: 3,
      },
      ALERTA_LARANJA: {
        bgColor: 'bg-orange-50',
        borderColor: 'border-orange-300',
        textColor: 'text-orange-700',
        icon: AlertTriangle,
        label: 'Alerta Laranja',
        severity: 2,
      },
      ALERTA_AMARELO: {
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-300',
        textColor: 'text-yellow-700',
        icon: AlertCircle,
        label: 'Alerta Amarelo',
        severity: 1,
      },
    };
    return config[tipo];
  };

  const filterAlerts = () => {
    if (filterTipo === 'ALL') return alertas;
    return alertas.filter((a) => a.tipo === filterTipo);
  };

  const filteredAlertas = filterAlerts();

  const getCountByTipo = (tipo: Alert['tipo']) => {
    return alertas.filter((a) => a.tipo === tipo).length;
  };

  return (
    <div className={`bg-white rounded-lg shadow ${className}`}>
      <div className="p-4 border-b">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-lg flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            Alertas Ativos ({filteredAlertas.length})
          </h3>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setFilterTipo('ALL')}
            className={`px-3 py-1 rounded text-sm font-medium transition ${
              filterTipo === 'ALL' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Todos ({alertas.length})
          </button>
          {['ALERTA_VERMELHO', 'ALERTA_LARANJA', 'ALERTA_AMARELO'].map((tipo) => {
            const count = getCountByTipo(tipo as Alert['tipo']);
            const config = getAlertConfig(tipo as Alert['tipo']);
            return (
              <button
                key={tipo}
                onClick={() => setFilterTipo(tipo)}
                className={`px-3 py-1 rounded text-sm font-medium transition ${
                  filterTipo === tipo
                    ? `${config.bgColor} ${config.textColor} border-2 ${config.borderColor}`
                    : `${config.bgColor} ${config.textColor} hover:opacity-80`
                }`}
              >
                {config.label.split(' ')[1]} ({count})
              </button>
            );
          })}
        </div>
      </div>

      {/* Alerts List */}
      <div className="divide-y max-h-96 overflow-y-auto">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Carregando alertas...</div>
        ) : filteredAlertas.length === 0 ? (
          <div className="p-8 text-center text-gray-500">Nenhum alerta neste momento</div>
        ) : (
          filteredAlertas.map((alerta) => {
            const config = getAlertConfig(alerta.tipo);
            const Icon = config.icon;
            const isExpanded = expandedAlert === alerta.id;

            return (
              <div
                key={alerta.id}
                className={`${config.bgColor} border-l-4 ${config.borderColor} transition`}
              >
                <button
                  onClick={() => setExpandedAlert(isExpanded ? null : alerta.id)}
                  className="w-full p-3 flex items-start justify-between hover:opacity-90 transition"
                >
                  <div className="flex items-start gap-3 flex-1 text-left">
                    <Icon className={`h-5 w-5 ${config.textColor} mt-0.5 flex-shrink-0`} />
                    <div className="flex-1">
                      <h4 className={`font-semibold ${config.textColor}`}>{alerta.titulo}</h4>
                      <p className={`text-sm ${config.textColor} opacity-75`}>
                        {alerta.parametro}: {alerta.valor_observado.toFixed(2)} (crítico: {alerta.valor_critico.toFixed(2)})
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        {new Date(alerta.timestamp).toLocaleString('pt-PT')}
                      </p>
                    </div>
                  </div>
                  <ChevronDown
                    className={`h-5 w-5 ${config.textColor} transition-transform flex-shrink-0 ${
                      isExpanded ? 'rotate-180' : ''
                    }`}
                  />
                </button>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className={`px-3 pb-3 border-t ${config.borderColor} space-y-2`}>
                    <p className={`text-sm ${config.textColor}`}>{alerta.descricao}</p>
                    <div className="flex gap-2">
                      {onResolve && (
                        <button
                          onClick={() => {
                            onResolve(alerta.id);
                            setExpandedAlert(null);
                          }}
                          className={`px-3 py-1 rounded text-xs font-medium ${config.textColor} bg-white border ${config.borderColor} hover:opacity-80 transition flex items-center gap-1`}
                        >
                          <X className="h-3 w-3" />
                          Resolver
                        </button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
