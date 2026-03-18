import React, { useEffect, useMemo, useState } from 'react';
import type { TerritoryNode } from '../types';
import { territoryService } from '../services/territoryService';
import { useToast } from '../hooks/useToast';

const normalize = (value: string) => value.toLowerCase();

const filterNodes = (nodes: TerritoryNode[], query: string) => {
  if (!query) return nodes;
  const term = normalize(query);
  return nodes.filter((node) => (
    normalize(node.name || '').includes(term)
    || normalize(node.code || '').includes(term)
  ));
};

const AdminTerritory: React.FC = () => {
  const [tree, setTree] = useState<TerritoryNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [selectedProvinceId, setSelectedProvinceId] = useState<string | null>(null);
  const [selectedMunicipalityId, setSelectedMunicipalityId] = useState<string | null>(null);
  const [selectedCommuneId, setSelectedCommuneId] = useState<string | null>(null);
  const { showToast } = useToast({ durationMs: 2500 });

  const loadTree = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await territoryService.getFullTree();
      setTree(data || []);
      if (data && data.length > 0) {
        setSelectedProvinceId(data[0].id);
      } else {
        setSelectedProvinceId(null);
        setSelectedMunicipalityId(null);
      }
    } catch (err) {
      console.error('Erro ao carregar territórios:', err);
      setError('Não foi possível carregar a hierarquia territorial.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTree();
  }, []);

  const selectedProvince = useMemo(
    () => tree.find((province) => province.id === selectedProvinceId) || null,
    [tree, selectedProvinceId],
  );

  const provinceMunicipalities = selectedProvince?.children || [];

  useEffect(() => {
    if (!selectedProvince) {
      setSelectedMunicipalityId(null);
      setSelectedCommuneId(null);
      return;
    }
    const firstMunicipality = selectedProvince.children?.[0];
    setSelectedMunicipalityId(firstMunicipality?.id || null);
  }, [selectedProvince]);

  const selectedMunicipality = useMemo(
    () => provinceMunicipalities.find((item) => item.id === selectedMunicipalityId) || null,
    [provinceMunicipalities, selectedMunicipalityId],
  );

  useEffect(() => {
    if (!selectedMunicipality) {
      setSelectedCommuneId(null);
      return;
    }
    const firstCommune = selectedMunicipality.children?.[0];
    setSelectedCommuneId(firstCommune?.id || null);
  }, [selectedMunicipality]);

  const selectedCommune = useMemo(
    () => selectedMunicipality?.children?.find((item) => item.id === selectedCommuneId) || null,
    [selectedMunicipality, selectedCommuneId],
  );

  const provinces = useMemo(() => filterNodes(tree, query), [tree, query]);
  const municipalities = useMemo(
    () => filterNodes(provinceMunicipalities, query),
    [provinceMunicipalities, query],
  );
  const communes = useMemo(
    () => filterNodes(selectedMunicipality?.children || [], query),
    [selectedMunicipality, query],
  );

  const totals = useMemo(() => {
    const totalProvinces = tree.length;
    const totalMunicipalities = tree.reduce((acc, province) => acc + (province.children?.length || 0), 0);
    const totalCommunes = tree.reduce(
      (acc, province) => acc + (province.children || []).reduce((sum, mun) => sum + (mun.children?.length || 0), 0),
      0,
    );
    return { totalProvinces, totalMunicipalities, totalCommunes };
  }, [tree]);

  const filteredRowsCount = useMemo(() => (
    provinces.length + municipalities.length + communes.length
  ), [provinces, municipalities, communes]);
  const hasActiveFilter = useMemo(() => Boolean(query.trim()), [query]);

  const breadcrumb = useMemo(() => {
    const parts = [];
    if (selectedProvince) parts.push(selectedProvince.name);
    if (selectedMunicipality) parts.push(selectedMunicipality.name);
    if (selectedCommune) parts.push(selectedCommune.name);
    return parts.length ? parts.join(' → ') : 'Selecione um território';
  }, [selectedProvince, selectedMunicipality, selectedCommune]);

  const selectedNode = selectedCommune || selectedMunicipality || selectedProvince;

  const handleCopyId = async () => {
    if (!selectedNode?.id) return;
    try {
      await navigator.clipboard.writeText(selectedNode.id);
      showToast({ message: 'ID copiado.', type: 'success' });
    } catch (err) {
      console.error('Falha ao copiar ID', err);
    }
  };

  const exportCsv = () => {
    const rows: Array<Record<string, string>> = [];
    tree.forEach((province) => {
      rows.push({
        level: 'province',
        id: province.id,
        name: province.name,
        code: province.code || '',
        type: province.type,
        parent_id: province.parent_id || '',
      });
      (province.children || []).forEach((municipality) => {
        rows.push({
          level: 'municipality',
          id: municipality.id,
          name: municipality.name,
          code: municipality.code || '',
          type: municipality.type,
          parent_id: municipality.parent_id || '',
        });
        (municipality.children || []).forEach((commune) => {
          rows.push({
            level: 'commune',
            id: commune.id,
            name: commune.name,
            code: commune.code || '',
            type: commune.type,
            parent_id: commune.parent_id || '',
          });
        });
      });
    });
    const headers = ['level', 'id', 'name', 'code', 'type', 'parent_id'];
    const escape = (value: string) => `"${String(value).replace(/"/g, '""')}"`;
    const content = [
      headers.join(';'),
      ...rows.map((row) => headers.map((key) => escape(row[key] || '')).join(';')),
    ].join('\n');
    const blob = new Blob([`\ufeff${content}`], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `territorios_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  };

  const exportCsvFiltered = () => {
    if (!filteredRowsCount) return;
    const rows: Array<Record<string, string>> = [];
    const addRow = (node: TerritoryNode, level: string) => {
      rows.push({
        level,
        id: node.id,
        name: node.name,
        code: node.code || '',
        type: node.type,
        parent_id: node.parent_id || '',
      });
    };
    const provinceIds = new Set(provinces.map((p) => p.id));
    const municipalityIds = new Set(municipalities.map((m) => m.id));
    provinces.forEach((province) => addRow(province, 'province'));
    municipalities.forEach((municipality) => {
      if (!provinceIds.has(municipality.parent_id || '')) return;
      addRow(municipality, 'municipality');
    });
    communes.forEach((commune) => {
      if (!municipalityIds.has(commune.parent_id || '')) return;
      addRow(commune, 'commune');
    });
    if (!rows.length) return;
    const headers = ['level', 'id', 'name', 'code', 'type', 'parent_id'];
    const escape = (value: string) => `"${String(value).replace(/"/g, '""')}"`;
    const content = [
      headers.join(';'),
      ...rows.map((row) => headers.map((key) => escape(row[key] || '')).join(';')),
    ].join('\n');
    const blob = new Blob([`\ufeff${content}`], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `territorios_filtrados_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Hierarquia de Territórios</h2>
          <p className="text-sm text-gray-500">Estrutura oficial baseada na tabela `locations`.</p>
          <p className="text-xs text-gray-400 mt-1">{breadcrumb}</p>
        </div>

        <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar por nome ou código"
            className="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-900/20"
          />
          <button
            type="button"
            onClick={loadTree}
            className="rounded-xl border border-slate-900 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-slate-900 hover:text-white"
          >
            Atualizar
          </button>
          <button
            type="button"
            onClick={exportCsv}
            className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-slate-800"
          >
            Exportar CSV
          </button>
          <button
            type="button"
            onClick={exportCsvFiltered}
            disabled={!filteredRowsCount}
            className="rounded-xl border border-slate-900 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-slate-900 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Exportar filtrado{hasActiveFilter ? ` (${filteredRowsCount})` : ''}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { label: 'Províncias', value: totals.totalProvinces, color: 'bg-blue-50 text-blue-700' },
          { label: 'Municípios', value: totals.totalMunicipalities, color: 'bg-amber-50 text-amber-700' },
          { label: 'Comunas', value: totals.totalCommunes, color: 'bg-emerald-50 text-emerald-700' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
            <p className="text-xs uppercase text-gray-400">{stat.label}</p>
            <div className="mt-2 flex items-center justify-between">
              <span className="text-3xl font-bold text-slate-900">{stat.value}</span>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${stat.color}`}>Ativo</span>
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 className="text-lg font-semibold text-slate-900">Províncias</h3>
            <span className="text-xs text-gray-400">{provinces.length} resultados</span>
          </div>
          <div className="max-h-[420px] overflow-y-auto">
            {loading && (
              <div className="p-6 text-sm text-gray-400">A carregar províncias...</div>
            )}
            {!loading && provinces.length === 0 && (
              <div className="p-6 text-sm text-gray-400">Sem províncias.</div>
            )}
            {!loading && provinces.map((province) => (
              <button
                key={province.id}
                onClick={() => setSelectedProvinceId(province.id)}
                className={`w-full text-left px-6 py-4 border-b border-gray-100 hover:bg-slate-50 transition ${
                  selectedProvinceId === province.id ? 'bg-slate-50' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-slate-900">{province.name}</p>
                    <p className="text-xs text-gray-400">{province.code || '—'}</p>
                  </div>
                  <span className="rounded-full bg-blue-50 text-blue-700 text-xs font-semibold px-2 py-1">
                    {province.children?.length || 0} municípios
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 className="text-lg font-semibold text-slate-900">Municípios</h3>
            <span className="text-xs text-gray-400">{municipalities.length} resultados</span>
          </div>
          <div className="max-h-[420px] overflow-y-auto">
            {!selectedProvince && (
              <div className="p-6 text-sm text-gray-400">Selecione uma província.</div>
            )}
            {selectedProvince && municipalities.length === 0 && (
              <div className="p-6 text-sm text-gray-400">Sem municípios.</div>
            )}
            {selectedProvince && municipalities.map((municipality) => (
              <button
                key={municipality.id}
                onClick={() => setSelectedMunicipalityId(municipality.id)}
                className={`w-full text-left px-6 py-4 border-b border-gray-100 hover:bg-slate-50 transition ${
                  selectedMunicipalityId === municipality.id ? 'bg-slate-50' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-slate-900">{municipality.name}</p>
                    <p className="text-xs text-gray-400">{municipality.code || '—'}</p>
                  </div>
                  <span className="rounded-full bg-amber-50 text-amber-700 text-xs font-semibold px-2 py-1">
                    {municipality.children?.length || 0} comunas
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100">
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 className="text-lg font-semibold text-slate-900">Comunas</h3>
            <span className="text-xs text-gray-400">{communes.length} resultados</span>
          </div>
          <div className="max-h-[420px] overflow-y-auto">
            {!selectedMunicipality && (
              <div className="p-6 text-sm text-gray-400">Selecione um município.</div>
            )}
            {selectedMunicipality && communes.length === 0 && (
              <div className="p-6 text-sm text-gray-400">Sem comunas.</div>
            )}
            {selectedMunicipality && communes.map((commune) => (
              <button
                key={commune.id}
                onClick={() => setSelectedCommuneId(commune.id)}
                className={`w-full text-left px-6 py-4 border-b border-gray-100 hover:bg-slate-50 transition ${
                  selectedCommuneId === commune.id ? 'bg-slate-50' : ''
                }`}
              >
                <p className="font-semibold text-slate-900">{commune.name}</p>
                <p className="text-xs text-gray-400">{commune.code || '—'}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Detalhe do território</h3>
          {!selectedProvince ? (
            <p className="text-sm text-gray-500">Selecione um território.</p>
          ) : (
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-xs uppercase text-gray-400 mb-1">Província</p>
                <p className="font-semibold text-slate-900">{selectedProvince.name}</p>
                <p className="text-xs text-gray-400">{selectedProvince.id}</p>
              </div>
              {selectedMunicipality && (
                <div>
                  <p className="text-xs uppercase text-gray-400 mb-1">Município</p>
                  <p className="font-semibold text-slate-900">{selectedMunicipality.name}</p>
                  <p className="text-xs text-gray-400">{selectedMunicipality.id}</p>
                </div>
              )}
              {selectedCommune && (
                <div>
                  <p className="text-xs uppercase text-gray-400 mb-1">Comuna</p>
                  <p className="font-semibold text-slate-900">{selectedCommune.name}</p>
                  <p className="text-xs text-gray-400">{selectedCommune.id}</p>
                </div>
              )}
              <div className="pt-2">
                <p className="text-xs uppercase text-gray-400 mb-1">Metadados</p>
                <div className="rounded-lg bg-slate-50 border border-slate-200 p-3 space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-600">
                    <span>Tipo</span>
                    <span className="font-semibold">
                      {selectedCommune?.type || selectedMunicipality?.type || selectedProvince?.type}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-600">
                    <span>Código</span>
                    <span className="font-semibold">
                      {selectedCommune?.code || selectedMunicipality?.code || selectedProvince?.code || '—'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-600">
                    <span>Parent ID</span>
                    <span className="font-semibold truncate">
                      {selectedCommune?.parent_id
                        || selectedMunicipality?.parent_id
                        || selectedProvince?.parent_id
                        || '—'}
                    </span>
                  </div>
                </div>
              </div>
              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleCopyId}
                  className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-slate-800"
                >
                  Copiar ID
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

    </div>
  );
};

export default AdminTerritory;
