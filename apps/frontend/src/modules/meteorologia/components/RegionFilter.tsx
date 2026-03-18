/**
 * RegionFilter - Geographic filtering component
 * Filter stations and data by province and municipality
 */

import React, { useState, useEffect } from 'react';
import { MapPin, ChevronDown, X } from 'lucide-react';
import { useProvincias } from '../hooks';
import type { MeteorologyFilter } from '../types';

interface RegionFilterProps {
  onFilterChange?: (filter: MeteorologyFilter) => void;
  className?: string;
}

export const RegionFilter: React.FC<RegionFilterProps> = ({ onFilterChange, className = '' }) => {
  const { provincias, loading } = useProvincias();
  const [selectedProvincia, setSelectedProvincia] = useState<string | null>(null);
  const [showProvincias, setShowProvincias] = useState(false);
  const [showMunicipalities, setShowMunicipalities] = useState(false);
  const [selectedMunicipios, setSelectedMunicipios] = useState<string[]>([]);

  // Mock municipalities data - in real app, fetch from API based on selected province
  const municipiosByProvincia: Record<string, string[]> = {
    'Luanda': ['Luanda', 'Bengo', 'Icolo e Bengo', 'Quissama'],
    'Benguela': ['Benguela', 'Baía Farta', 'Bocoio', 'Catumbela'],
    'Huila': ['Lubango', 'Caconda', 'Chibia', 'Humpata'],
    'Huambo': ['Huambo', 'Bailundo', 'Chinguar', 'Ecunha'],
    'Cabinda': ['Cabinda', 'Belize', 'Buco-Zau', 'Cacongo'],
  };

  useEffect(() => {
    const filter: MeteorologyFilter = {};
    if (selectedProvincia) filter.provincia = selectedProvincia;
    if (selectedMunicipios.length > 0) filter.municipio = selectedMunicipios[0];

    onFilterChange?.(filter);
  }, [selectedProvincia, selectedMunicipios, onFilterChange]);

  const handleClearAll = () => {
    setSelectedProvincia(null);
    setSelectedMunicipios([]);
  };

  const municipios = selectedProvincia ? municipiosByProvincia[selectedProvincia] || [] : [];

  return (
    <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold flex items-center gap-2">
          <MapPin className="h-5 w-5" />
          Filtrar por Região
        </h3>
        {(selectedProvincia || selectedMunicipios.length > 0) && (
          <button
            onClick={handleClearAll}
            className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
          >
            <X className="h-3 w-3" />
            Limpar
          </button>
        )}
      </div>

      {/* Selected Filters Display */}
      <div className="flex flex-wrap gap-2 mb-4">
        {selectedProvincia && (
          <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center gap-2">
            <span>Provence: {selectedProvincia}</span>
            <button
              onClick={() => setSelectedProvincia(null)}
              className="hover:text-blue-900"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        )}
        {selectedMunicipios.map((mun) => (
          <div key={mun} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm flex items-center gap-2">
            <span>{mun}</span>
            <button
              onClick={() => setSelectedMunicipios((prev) => prev.filter((m) => m !== mun))}
              className="hover:text-green-900"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        ))}
      </div>

      {/* Province Selector */}
      <div className="mb-4">
        <button
          onClick={() => setShowProvincias(!showProvincias)}
          className="w-full flex items-center justify-between p-3 border-2 border-gray-300 rounded hover:border-gray-400 transition"
        >
          <span className="text-sm font-medium">
            {selectedProvincia || 'Selecionar Província'}
          </span>
          <ChevronDown className={`h-4 w-4 transition-transform ${showProvincias ? 'rotate-180' : ''}`} />
        </button>

        {showProvincias && (
          <div className="mt-2 border border-gray-300 rounded bg-white shadow-md max-h-64 overflow-y-auto z-10">
            {loading ? (
              <div className="p-4 text-center text-gray-500 text-sm">Carregando...</div>
            ) : provincias.length === 0 ? (
              <div className="p-4 text-center text-gray-500 text-sm">Nenhuma província disponível</div>
            ) : (
              provincias.map((prov) => (
                <button
                  key={prov.nome}
                  onClick={() => {
                    setSelectedProvincia(prov.nome);
                    setShowProvincias(false);
                    setSelectedMunicipios([]);
                  }}
                  className={`w-full text-left px-4 py-2 hover:bg-blue-50 transition flex items-center justify-between ${
                    selectedProvincia === prov.nome ? 'bg-blue-100 font-semibold' : ''
                  }`}
                >
                  <span>{prov.nome}</span>
                  <span className="text-xs text-gray-600">
                    {prov.estacoes} estações · {prov.alertas} alertas
                  </span>
                </button>
              ))
            )}
          </div>
        )}
      </div>

      {/* Municipality Selector */}
      {selectedProvincia && (
        <div>
          <button
            onClick={() => setShowMunicipalities(!showMunicipalities)}
            className="w-full flex items-center justify-between p-3 border-2 border-green-300 rounded hover:border-green-400 transition"
          >
            <span className="text-sm font-medium">
              {selectedMunicipios.length > 0
                ? `${selectedMunicipios.length} Município(s) Selecionado(s)`
                : 'Selecionar Município(s)'}
            </span>
            <ChevronDown className={`h-4 w-4 transition-transform ${showMunicipalities ? 'rotate-180' : ''}`} />
          </button>

          {showMunicipalities && (
            <div className="mt-2 border border-green-300 rounded bg-white shadow-md max-h-64 overflow-y-auto z-10">
              {municipios.length === 0 ? (
                <div className="p-4 text-center text-gray-500 text-sm">Nenhum município disponível</div>
              ) : (
                municipios.map((mun) => (
                  <label
                    key={mun}
                    className="flex items-center px-4 py-2 hover:bg-green-50 transition cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedMunicipios.includes(mun)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedMunicipios((prev) => [...prev, mun]);
                        } else {
                          setSelectedMunicipios((prev) => prev.filter((m) => m !== mun));
                        }
                      }}
                      className="w-4 h-4 rounded cursor-pointer"
                    />
                    <span className="ml-2 text-sm">{mun}</span>
                  </label>
                ))
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
