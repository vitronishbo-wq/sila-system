
import http from '@/api/http';
import { DocumentStatus } from '@/types';
import type { Document } from '@/types';

export const documentService = {
  async list(status?: DocumentStatus, skip = 0, limit = 20): Promise<Document[]> {
    const response = await http.get<Document[]>('citizen/documents/', {
      params: { status, skip, limit }
    });
    return response.data;
  },

  async create(data: { citizen_id: string; document_type: string; notes?: string }): Promise<Document> {
    const response = await http.post<Document>('citizen/documents/', data);
    return response.data;
  },

  async getById(id: string): Promise<Document> {
    const response = await http.get<Document>(`citizen/documents/${id}`);
    return response.data;
  },

  async updateStatus(id: string, status: DocumentStatus): Promise<Document> {
    const response = await http.patch<Document>(`citizen/documents/${id}/status`, { status });
    return response.data;
  },

  async deepSearch(params: any): Promise<Document[]> {
    const response = await http.get<Document[]>('citizen/documents/search/deep', { params });
    return response.data;
  }
};
