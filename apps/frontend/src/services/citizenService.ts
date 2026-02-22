
import http from '../api/http';
import { Citizen } from '../types';

export const citizenService = {
  async list(skip = 0, limit = 20): Promise<Citizen[]> {
    const response = await http.get<Citizen[]>('citizen/citizens/', { params: { skip, limit } });
    return response.data;
  },

  async search(query: string): Promise<Citizen[]> {
    const response = await http.get<Citizen[]>('citizen/citizens/search', { params: { q: query } });
    return response.data;
  },

  async getById(id: string): Promise<Citizen> {
    const response = await http.get<Citizen>(`citizen/citizens/${id}`);
    return response.data;
  },

  async create(data: Partial<Citizen>): Promise<Citizen> {
    const response = await http.post<Citizen>('citizen/citizens/', data);
    return response.data;
  }
};
