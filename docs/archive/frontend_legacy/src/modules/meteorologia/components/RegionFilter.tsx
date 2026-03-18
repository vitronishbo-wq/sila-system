/**
 * RegionFilter Component
 * Geographic filtering with province and municipality selection
 */

import { useState } from "react";
import { ChevronDown, X } from "lucide-react";
import { useProvincias } from "../hooks";
import type { MeteorologyFilter } from "../types";

interface RegionFilterProps {
  onFilterChange?: (filter: MeteorologyFilter) => void;
  className?: string;
}

// Mock municipalities by province (replace with API in production)
const municipiosByProvincia: Record<string, string[]> = {
  Luanda: ["Benfica", "Cazenga", "Maianga", "Rangel"],
  Benguela: ["Baía Farta", "Benguela", "Bocoio", "Chongorói"],
  Huílá: ["Caconda", "Chibia", "Humpata", "Lubango"],
  Huambo: ["Bailundo", "Caála", "Huambo", "Kuito"],
  Cabinda: ["Buco Zau", "Cabinda", "Cacongo", "Quinzau"],
};

export function RegionFilter({
  onFilterChange,
  className = "",
}: RegionFilterProps) {
  const { provincias } = useProvincias();
  const [selectedProvincia, setSelectedProvincia] = useState<string | null>(null);
  const [selectedMunicipios, setSelectedMunicipios] = useState<Set<string>>(new Set());
  const [openDropdown, setOpenDropdown] = useState<"provincia" | "municipios" | null>(
    null
  );

  const handleProvinciaChange = (provincia: string | null) => {
    setSelectedProvincia(provincia);
    setSelectedMunicipios(new Set()); // Clear municipalities
    setOpenDropdown(null);

    const filter: MeteorologyFilter = {};
    if (provincia) filter.provincia = provincia;

    onFilterChange?.(filter);
  };

  const handleMunicipioToggle = (municipio: string) => {
    const updated = new Set(selectedMunicipios);
    if (updated.has(municipio)) {
      updated.delete(municipio);
    } else {
      updated.add(municipio);
    }

    setSelectedMunicipios(updated);

    const filter: MeteorologyFilter = {};
    if (selectedProvincia) filter.provincia = selectedProvincia;
    if (updated.size > 0) {
      filter.municipio = Array.from(updated).join(",");
    }

    onFilterChange?.(filter);
  };

  const handleClearAll = () => {
    setSelectedProvincia(null);
    setSelectedMunicipios(new Set());
    setOpenDropdown(null);
    onFilterChange?.({});
  };

  const handleRemoveProvincia = () => {
    handleProvinciaChange(null);
  };

  const handleRemoveMunicipio = (municipio: string) => {
    handleMunicipioToggle(municipio);
  };

  const availableMunicipios = selectedProvincia
    ? municipiosByProvincia[selectedProvincia] || []
    : [];

  return (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 ${className}`}>
      <h3 className="font-bold text-lg text-gray-900 mb-4">Filtros Geográficos</h3>

      {/* Province Selector */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Província
        </label>
        <div className="relative">
          <button
            onClick={() =>
              setOpenDropdown(
                openDropdown === "provincia" ? null : "provincia"
              )
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-left flex items-center justify-between hover:bg-gray-50"
          >
            <span>
              {selectedProvincia || "Selecionar provincia..."}
            </span>
            <ChevronDown
              className={`w-4 h-4 transition-transform ${
                openDropdown === "provincia" ? "rotate-180" : ""
              }`}
            />
          </button>

          {/* Province Dropdown */}
          {openDropdown === "provincia" && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
              <button
                onClick={() => handleProvinciaChange(null)}
                className="w-full text-left px-3 py-2 hover:bg-gray-100 text-sm"
              >
                — Limpar seleção —
              </button>

              {provincias.map((provincia) => (
                <button
                  key={provincia.nome}
                  onClick={() => handleProvinciaChange(provincia.nome)}
                  className={`w-full text-left px-3 py-2 hover:bg-gray-100 text-sm ${
                    selectedProvincia === provincia.nome
                      ? "bg-blue-50 font-semibold"
                      : ""
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span>{provincia.nome}</span>
                    <span className="text-xs text-gray-500">
                      {provincia.estacoes} estações • {provincia.alertas} alertas
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Municipality Selector */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Município
        </label>
        <div className="relative">
          <button
            disabled={!selectedProvincia}
            onClick={() =>
              setOpenDropdown(
                openDropdown === "municipios" ? null : "municipios"
              )
            }
            className={`w-full px-3 py-2 rounded-lg text-left flex items-center justify-between ${
              selectedProvincia
                ? "border border-green-300 hover:bg-green-50"
                : "border border-gray-300 bg-gray-100 cursor-not-allowed text-gray-500"
            }`}
          >
            <span>
              {selectedMunicipios.size > 0
                ? `${selectedMunicipios.size} selecionado(s)`
                : "Selecionar (após provincia)..."}
            </span>
            <ChevronDown
              className={`w-4 h-4 transition-transform ${
                openDropdown === "municipios" ? "rotate-180" : ""
              }`}
            />
          </button>

          {/* Municipality Dropdown */}
          {openDropdown === "municipios" && selectedProvincia && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-green-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
              {availableMunicipios.map((municipio) => (
                <label
                  key={municipio}
                  className="flex items-center px-3 py-2 hover:bg-green-50 text-sm cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={selectedMunicipios.has(municipio)}
                    onChange={() => handleMunicipioToggle(municipio)}
                    className="w-4 h-4 rounded"
                  />
                  <span className="ml-2">{municipio}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Selected Filters Display */}
      {(selectedProvincia || selectedMunicipios.size > 0) && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
          <div className="flex flex-wrap gap-2">
            {selectedProvincia && (
              <div className="flex items-center gap-1 bg-blue-200 text-blue-900 px-3 py-1 rounded-full text-sm">
                <span>{selectedProvincia}</span>
                <button
                  onClick={handleRemoveProvincia}
                  className="hover:font-bold"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {Array.from(selectedMunicipios).map((municipio) => (
              <div
                key={municipio}
                className="flex items-center gap-1 bg-green-200 text-green-900 px-3 py-1 rounded-full text-sm"
              >
                <span>{municipio}</span>
                <button
                  onClick={() => handleRemoveMunicipio(municipio)}
                  className="hover:font-bold"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {(selectedProvincia || selectedMunicipios.size > 0) && (
            <button
              onClick={handleClearAll}
              className="mt-2 w-full px-3 py-1 text-sm font-medium text-blue-700 hover:text-blue-900 border border-blue-300 rounded hover:bg-blue-100 transition-colors"
            >
              Limpar Filtros
            </button>
          )}
        </div>
      )}
    </div>
  );
}
