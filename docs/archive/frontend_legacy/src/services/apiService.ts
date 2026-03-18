/**
 * API Service Layer - Centralizado
 * 
 * Responsabilidades:
 * - Comunicação HTTP com backend
 * - Tratamento de autenticação
 * - Interceptação de erros
 * - Gerenciamento de estado de loading/erro
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// Configuração base
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Tipos
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface Invoice {
  id: string;
  citizen_id: string;
  service_name: string;
  amount: number;
  currency: string;
  status: 'PENDING' | 'PAID' | 'OVERDUE' | 'CANCELLED';
  due_date: string;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: string;
  invoice_id: string;
  citizen_id: string;
  amount: number;
  currency: string;
  payment_method: string;
  gateway_reference: string;
  status: string;
  proof_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Citizen {
  id: string;
  name: string;
  email: string;
  phone: string;
  status: string;
  created_at: string;
  updated_at: string;
}

// Instância Axios com interceptors
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Request - Adiciona token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de Response - Tratamento de erros
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // 401 - Token expirado, redireciona para login
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    // 403 - Acesso negado
    if (error.response?.status === 403) {
      console.error('Acesso negado:', error.response.data);
    }
    
    return Promise.reject(error);
  }
);

/**
 * SERVIÇOS DE FATURAS (Financeiro)
 */
export const invoiceAPI = {
  /**
   * Lista todas as faturas de um cidadão
   */
  listCitizenInvoices: async (citizenId: string): Promise<Invoice[]> => {
    try {
      const response = await apiClient.get(`/v1/financas/invoices/citizen/${citizenId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao listar faturas:', error);
      throw error;
    }
  },

  /**
   * Lista apenas faturas pendentes
   */
  listPendingInvoices: async (citizenId: string): Promise<Invoice[]> => {
    try {
      const response = await apiClient.get(`/v1/financas/invoices/citizen/${citizenId}/pending`);
      return response.data;
    } catch (error) {
      console.error('Erro ao listar faturas pendentes:', error);
      throw error;
    }
  },

  /**
   * Obter detalhes de uma fatura específica
   */
  getInvoice: async (invoiceId: string): Promise<Invoice> => {
    try {
      const response = await apiClient.get(`/v1/financas/invoices/${invoiceId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter fatura:', error);
      throw error;
    }
  },

  /**
   * Cancelar uma fatura
   */
  cancelInvoice: async (invoiceId: string, reason: string): Promise<Invoice> => {
    try {
      const response = await apiClient.post(`/v1/financas/invoices/${invoiceId}/cancel`, { reason });
      return response.data;
    } catch (error) {
      console.error('Erro ao cancelar fatura:', error);
      throw error;
    }
  },

  /**
   * Download de fatura (PDF/TXT)
   */
  downloadInvoice: async (invoiceId: string, format: 'pdf' | 'txt' = 'pdf'): Promise<Blob> => {
    try {
      const response = await apiClient.get(
        `/v1/financas/invoices/${invoiceId}/download?format=${format}`,
        { responseType: 'blob' }
      );
      return response.data;
    } catch (error) {
      console.error('Erro ao fazer download da fatura:', error);
      throw error;
    }
  },
};

/**
 * SERVIÇOS DE PAGAMENTOS
 */
export const paymentAPI = {
  /**
   * Registar um novo pagamento
   */
  registerPayment: async (paymentData: {
    invoice_id: string;
    amount: number;
    currency: string;
    payment_method: string;
    gateway_reference: string;
  }): Promise<Payment> => {
    try {
      const response = await apiClient.post('/v1/financas/payments', paymentData);
      return response.data;
    } catch (error) {
      console.error('Erro ao registar pagamento:', error);
      throw error;
    }
  },

  /**
   * Lista histórico de pagamentos do cidadão
   */
  getPaymentHistory: async (citizenId: string): Promise<Payment[]> => {
    try {
      const response = await apiClient.get(`/v1/financas/payments/citizen/${citizenId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter histórico de pagamentos:', error);
      throw error;
    }
  },

  /**
   * Obter status de pagamento por referência de gateway
   */
  getPaymentByReference: async (gatewayReference: string): Promise<Payment> => {
    try {
      const response = await apiClient.get(
        `/v1/financas/payments/gateway/${gatewayReference}`
      );
      return response.data;
    } catch (error) {
      console.error('Erro ao obter pagamento:', error);
      throw error;
    }
  },

  /**
   * Download de comprovativo de pagamento
   */
  downloadProof: async (paymentId: string): Promise<Blob> => {
    try {
      const response = await apiClient.get(
        `/v1/financas/payments/${paymentId}/proof`,
        { responseType: 'blob' }
      );
      return response.data;
    } catch (error) {
      console.error('Erro ao fazer download do comprovativo:', error);
      throw error;
    }
  },
};

/**
 * SERVIÇOS DE CIDADÃO (FUC)
 */
export const citizenAPI = {
  /**
   * Obter perfil do cidadão atual
   */
  getCurrentProfile: async (): Promise<Citizen> => {
    try {
      const response = await apiClient.get('/v1/identidade-civil/citizens/me');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter perfil:', error);
      throw error;
    }
  },

  /**
   * Obter cidadão por ID
   */
  getCitizen: async (citizenId: string): Promise<Citizen> => {
    try {
      const response = await apiClient.get(`/v1/identidade-civil/citizens/${citizenId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter cidadão:', error);
      throw error;
    }
  },

  /**
   * Listar eventos/histórico do cidadão
   */
  getEvents: async (citizenId: string): Promise<any[]> => {
    try {
      const response = await apiClient.get(`/v1/identidade-civil/citizens/${citizenId}/events`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter eventos:', error);
      throw error;
    }
  },

  /**
   * Atualizar perfil do cidadão
   */
  updateProfile: async (citizenId: string, data: Partial<Citizen>): Promise<Citizen> => {
    try {
      const response = await apiClient.put(
        `/v1/identidade-civil/citizens/${citizenId}`,
        data
      );
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      throw error;
    }
  },
};

/**
 * SERVIÇOS DE AUTENTICAÇÃO
 */
export const authAPI = {
  /**
   * Login
   */
  login: async (email: string, password: string): Promise<{ token: string; user: any }> => {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      return { token, user };
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }
  },

  /**
   * Logout
   */
  logout: (): void => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  /**
   * Registrar novo utilizador
   */
  register: async (userData: any): Promise<{ token: string; user: any }> => {
    try {
      const response = await apiClient.post('/auth/register', userData);
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      return { token, user };
    } catch (error) {
      console.error('Erro ao registar:', error);
      throw error;
    }
  },

  /**
   * Verificar se está autenticado
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  },

  /**
   * Obter utilizador atual
   */
  getCurrentUser: (): any | null => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

/**
 * SERVIÇOS PÚBLICOS (sem autenticação)
 */
export const publicAPI = {
  /**
   * Listar serviços disponíveis
   */
  listServices: async (): Promise<any[]> => {
    try {
      const response = await apiClient.get('/public/services');
      return response.data;
    } catch (error) {
      console.error('Erro ao listar serviços:', error);
      throw error;
    }
  },

  /**
   * Obter informações públicas
   */
  getInfo: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/public/info');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter informações:', error);
      throw error;
    }
  },
};

export default apiClient;
