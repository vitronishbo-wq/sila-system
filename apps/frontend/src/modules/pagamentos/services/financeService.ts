/**
 * Finance Service - Frontend
 * Único ponto de integração com a API de Finanças do Backend
 * 
 * Endpoints:
 * POST   /api/v1/financas/invoices
 * GET    /api/v1/financas/invoices/{id}
 * GET    /api/v1/financas/invoices/citizen/{citizen_id}
 * POST   /api/v1/financas/payments
 * GET    /api/v1/financas/payments/citizen/{citizen_id}
 * POST   /api/v1/financas/payments/confirm (webhook)
 */

import http from '@/api/http';
import { InvoiceStatus } from '@/modules/pagamentos/types';
import type {
  Invoice,
  Payment,
  FinanceStats,
  CreateInvoiceRequest,
  CreatePaymentRequest
} from '@/modules/pagamentos/types';

class FinanceService {
  private readonly apiBase = '/api/v1/financas';

  /**
   * Criar nova fatura
   */
  async createInvoice(data: CreateInvoiceRequest): Promise<Invoice> {
    const response = await http.post<Invoice>(`${this.apiBase}/invoices`, {
      citizen_id: data.citizen_id,
      revenue_code: data.revenue_code,
      cost_center: data.cost_center,
      service_code: data.service_code,
      service_name: data.service_name,
      amount: data.amount,
      currency: data.currency || 'AOA',
      due_date: data.due_date || new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    });
    return response.data;
  }

  /**
   * Obter fatura por ID
   */
  async getInvoice(invoiceId: string): Promise<Invoice> {
    const response = await http.get<Invoice>(`${this.apiBase}/invoices/${invoiceId}`);
    return response.data;
  }

  /**
   * Listar faturas de um cidadão
   */
  async getCitizenInvoices(citizenId: string): Promise<Invoice[]> {
    const response = await http.get<Invoice[]>(`${this.apiBase}/invoices/citizen/${citizenId}`);
    return response.data;
  }

  /**
   * Registar pagamento
   */
  async registerPayment(data: CreatePaymentRequest): Promise<Payment> {
    const response = await http.post<Payment>(`${this.apiBase}/payments`, {
      invoice_id: data.invoice_id,
      citizen_id: data.citizen_id,
      amount: data.amount,
      gateway_reference: data.gateway_reference,
      payment_method: data.payment_method,
    });
    return response.data;
  }

  /**
   * Obter histórico de pagamentos de um cidadão
   */
  async getCitizenPayments(citizenId: string): Promise<Payment[]> {
    const response = await http.get<Payment[]>(`${this.apiBase}/payments/citizen/${citizenId}`);
    return response.data;
  }

  /**
   * Confirmar pagamento via webhook (chamado pelo gateway)
   */
  async confirmPaymentWebhook(payload: Record<string, any>): Promise<{ status: string; message: string }> {
    const response = await http.post<{ status: string; message: string }>(`${this.apiBase}/payments/confirm`, payload);
    return response.data;
  }

  /**
   * Calcular estatísticas financeiras de um cidadão
   */
  async getFinancialStats(citizenId: string): Promise<FinanceStats> {
    const invoices = await this.getCitizenInvoices(citizenId);
    return this.computeStats(invoices);
  }

  /**
   * @deprecated Usar getCitizenInvoices + getCitizenPayments + aggregação
   * Mantido para compatibilidade com componentes legados
   */
  async getInvoices(citizenId?: string): Promise<Invoice[]> {
    if (citizenId) {
      return this.getCitizenInvoices(citizenId);
    }
    const response = await http.get<Invoice[]>(`${this.apiBase}/invoices`);
    return response.data;
  }

  /**
   * @deprecated Usar getFinancialStats
   * Mantido para compatibilidade com componentes legados
   */
  async getStats(): Promise<FinanceStats> {
    const invoices = await this.getInvoices();
    return this.computeStats(invoices);
  }

  /**
   * @deprecated Usar registerPayment
   * Mantido para compatibilidade com componentes legados
   */
  async processPayment(invoiceId: string, citizenId: string, amount: number): Promise<Payment> {
    const gatewayRef = `GW-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    return this.registerPayment({
      invoice_id: invoiceId,
      citizen_id: citizenId,
      amount: amount,
      gateway_reference: gatewayRef,
      payment_method: 'INTERNET_BANKING',
    });
  }

  private computeStats(invoices: Invoice[]): FinanceStats {
    const totalAmount = invoices.reduce((sum, inv) => sum + inv.amount, 0);
    const paidInvoices = invoices.filter(inv => inv.status === InvoiceStatus.PAID);
    const pendingInvoices = invoices.filter(inv => inv.status === InvoiceStatus.PENDING);
    const overdueInvoices = invoices.filter(inv => inv.status === InvoiceStatus.OVERDUE);

    const paidAmount = paidInvoices.reduce((sum, inv) => sum + inv.amount, 0);
    const pendingAmount = pendingInvoices.reduce((sum, inv) => sum + inv.amount, 0);
    const overdueAmount = overdueInvoices.reduce((sum, inv) => sum + inv.amount, 0);

    return {
      total_invoices: invoices.length,
      total_amount: totalAmount,
      paid_amount: paidAmount,
      pending_amount: pendingAmount,
      overdue_amount: overdueAmount,
      payment_rate: totalAmount > 0 ? (paidAmount / totalAmount) * 100 : 0,
      paid_count: paidInvoices.length,
      pending_count: pendingInvoices.length,
    };
  }
}

export const financeService = new FinanceService();
export default financeService;
