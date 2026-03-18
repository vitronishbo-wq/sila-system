
import http from '../api/http';
import type { TerritoryNode } from '../types';

export const territoryService = {
  async getProvinces(): Promise<TerritoryNode[]> {
    const response = await http.get<TerritoryNode[]>('admin/territory/provinces');
    return response.data;
  },

  async getMunicipalities(provinceId: string): Promise<TerritoryNode[]> {
    const response = await http.get<TerritoryNode[]>(`admin/territory/provinces/${provinceId}/municipalities`);
    return response.data;
  },

  async getCommunes(municipalityId: string): Promise<TerritoryNode[]> {
    const response = await http.get<TerritoryNode[]>(`admin/territory/municipalities/${municipalityId}/communes`);
    return response.data;
  },

  async getFullTree(): Promise<TerritoryNode[]> {
    const response = await http.get<TerritoryNode[]>('admin/territory/tree');
    return response.data;
  }
};
