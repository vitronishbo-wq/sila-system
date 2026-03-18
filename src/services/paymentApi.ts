import { api } from "../api/axios"
import { ConfirmPaymentResponse, Payment } from "../types/api"

export const generatePayment = async (orderId: string): Promise<Payment> => {
  const res = await api.post(`/v1/payments/${orderId}/generate`)
  return res.data
}

export const confirmPayment = async (
  reference: string
): Promise<ConfirmPaymentResponse> => {
  const res = await api.post(`/v1/payments/${reference}/confirm`)
  return res.data
}
