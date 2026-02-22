/**
 * Tipos de Finanças - Sincronizados com Backend
 * Source: apps/backend/app/modules/financas/schemas/
 */

export enum InvoiceStatus {
  PENDING = 'pending',
  PAID = 'paid',
  OVERDUE = 'overdue',
  CANCELLED = 'cancelled'
}

export enum PaymentStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  FAILED = 'failed',
  REVERSED = 'reversed'
}

/**
 * Invoice (Fatura)
 * Alinhada com InvoiceResponse do backend
 */
export interface Invoice {
  id: string;
  citizen_id: string;
  reference: string;
  revenue_code: string;
  cost_center: string;
  service_code: string;
  service_name: string;
  amount: number;
  currency: string;
  status: InvoiceStatus;
  created_at: string;
  updated_at: string;
  due_date: string;
}

/**
 * Payment (Pagamento)
 * Alinhada com PaymentResponse do backend
 */
export interface Payment {
  id: string;
  invoice_id: string;
  citizen_id: string;
  amount: number;
  currency: string;
  gateway_reference: string;
  payment_method: string;
  status: PaymentStatus;
  confirmation_timestamp?: string;
  created_at: string;
}

/**
 * Estatísticas Financeiras
 * Agregação de dados de múltiplas faturas/pagamentos
 */
export interface FinanceStats {
  total_invoices: number;
  total_amount: number;
  paid_amount: number;
  pending_amount: number;
  overdue_amount: number;
  payment_rate: number;
}

/**
 * Request para criar fatura
 */
export interface CreateInvoiceRequest {
  citizen_id: string;
  service_code: string;
  service_name: string;
  revenue_code: string;
  cost_center: string;
  amount: number;
  currency?: string;
  due_date?: string;
}

/**
 * Request para registar pagamento
 */
export interface CreatePaymentRequest {
  invoice_id: string;
  citizen_id: string;
  amount: number;
  gateway_reference: string;
  payment_method: string;
}
