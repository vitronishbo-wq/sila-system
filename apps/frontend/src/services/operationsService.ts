import { apiClient } from '@/api/generated/client';
import type { CreateOrderPayload, Order, Payment, Service } from '../types/api';

export const operationsService = {
  async listServices(): Promise<Service[]> {
    const { data, error } = await apiClient.GET('/api/v1/services');
    if (error || !data) {
      throw error ?? new Error('Falha ao listar serviços.');
    }
    return data as Service[];
  },

  async createOrder(payload: CreateOrderPayload): Promise<Order> {
    const { data, error } = await apiClient.POST('/api/v1/orders', { body: payload });
    if (error || !data) {
      throw error ?? new Error('Falha ao criar pedido.');
    }
    return data as Order;
  },

  async submitOrder(orderId: string): Promise<Order> {
    const { data, error } = await apiClient.POST('/api/v1/orders/{order_id}/submit', {
      params: { path: { order_id: orderId } }
    });
    if (error || !data) {
      throw error ?? new Error('Falha ao submeter pedido.');
    }
    return data as Order;
  },

  async completeOrder(orderId: string): Promise<Order> {
    const { data, error } = await apiClient.POST('/api/v1/orders/{order_id}/complete', {
      params: { path: { order_id: orderId } }
    });
    if (error || !data) {
      throw error ?? new Error('Falha ao concluir pedido.');
    }
    return data as Order;
  },

  async attachDocuments(orderId: string, payload: FormData | Record<string, unknown>): Promise<Order> {
    const options: {
      params: { path: { order_id: string } };
      body: FormData | Record<string, unknown>;
      bodySerializer?: (body: FormData | Record<string, unknown>) => BodyInit;
    } = {
      params: { path: { order_id: orderId } },
      body: payload
    };

    if (payload instanceof FormData) {
      options.bodySerializer = (body) => body as BodyInit;
    }

    const { data, error } = await apiClient.POST('/api/v1/orders/{order_id}/documents', options);
    if (error || !data) {
      throw error ?? new Error('Falha ao anexar documentos.');
    }
    return data as Order;
  },

  async getReceipt(orderId: string): Promise<Blob> {
    const { data, error } = await apiClient.GET('/api/v1/orders/{order_id}/receipt', {
      params: { path: { order_id: orderId } },
      parseAs: 'blob'
    });
    if (error || !data) {
      throw error ?? new Error('Falha ao obter recibo.');
    }
    return data as Blob;
  },

  async generatePayment(orderId: string): Promise<Payment> {
    const { data, error } = await apiClient.POST('/api/v1/payments/{order_id}/generate', {
      params: { path: { order_id: orderId } }
    });
    if (error || !data) {
      throw error ?? new Error('Falha ao gerar pagamento.');
    }
    return data as Payment;
  },

  async confirmPayment(reference: string): Promise<Payment> {
    const { data, error } = await apiClient.POST('/api/v1/payments/{reference}/confirm', {
      params: { path: { reference } }
    });
    if (error || !data) {
      throw error ?? new Error('Falha ao confirmar pagamento.');
    }
    return data as Payment;
  }
};
