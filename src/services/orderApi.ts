import { api } from "../api/axios"
import {
  AttachDocumentsRequest,
  AttachDocumentsResponse,
  Order,
  ReceiptResponse,
  SubmitOrderResponse
} from "../types/api"

export const createOrder = async (serviceId: string): Promise<Order> => {
  const res = await api.post("/v1/orders", {
    service_id: serviceId
  })

  return res.data
}

export const attachDocuments = async (
  orderId: string,
  payload: AttachDocumentsRequest
): Promise<AttachDocumentsResponse> => {
  const res = await api.post(`/v1/orders/${orderId}/documents`, payload)
  return res.data
}

export const submitOrder = async (
  orderId: string
): Promise<SubmitOrderResponse> => {
  const res = await api.post(`/v1/orders/${orderId}/submit`)
  return res.data
}

export const getReceipt = async (orderId: string): Promise<ReceiptResponse> => {
  const res = await api.get(`/v1/orders/${orderId}/receipt`)
  return res.data
}
