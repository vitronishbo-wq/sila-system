import type { Order } from '@/types/api';
import { operationsService } from '@/modules/operations/services/operationsService';

export type AttachDocumentsRequest = FormData | Record<string, unknown>;
export type AttachDocumentsResponse = Order;
export type SubmitOrderResponse = Order;
export type ReceiptResponse = Blob;

export const createOrder = async (serviceId: string): Promise<Order> => {
  return operationsService.createOrder({ service_id: serviceId });
};

export const attachDocuments = async (
  orderId: string,
  payload: AttachDocumentsRequest
): Promise<AttachDocumentsResponse> => {
  return operationsService.attachDocuments(orderId, payload);
};

export const submitOrder = async (orderId: string): Promise<SubmitOrderResponse> => {
  return operationsService.submitOrder(orderId);
};

export const getReceipt = async (orderId: string): Promise<ReceiptResponse> => {
  return operationsService.getReceipt(orderId);
};
