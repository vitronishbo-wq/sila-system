import type { Payment } from '@/types/api';
import { operationsService } from './operationsService';

export type ConfirmPaymentResponse = Payment;

export const generatePayment = async (orderId: string): Promise<Payment> => {
  return operationsService.generatePayment(orderId);
};

export const confirmPayment = async (reference: string): Promise<ConfirmPaymentResponse> => {
  return operationsService.confirmPayment(reference);
};
