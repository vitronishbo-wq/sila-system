export type Service = {
  id: string
  code: string
  name: string
  price: number
}

export type ListServicesResponse = Service[]

export type CreateOrderRequest = {
  service_id: string
}

export type CreateOrderResponse = {
  id: string
  service_id: string
  status: "created" | string
}

export type DocumentPayload = {
  filename: string
  content_type: string
  size_bytes: number
  uri: string
}

export type AttachDocumentsRequest = {
  documents: DocumentPayload[]
}

export type AttachDocumentsResponse = Record<string, unknown>

export type SubmitOrderResponse = Record<string, unknown>

export type Order = {
  id: string
  service_id: string
  status: "created" | string
}

export type GeneratePaymentResponse = {
  reference: string
  order_id: string
  status: "PENDING" | string
}

export type ConfirmPaymentResponse = Record<string, unknown>

export type ReceiptResponse = {
  receipt_number: string
  order_id: string
  citizen_id: string
  service_id: string
  amount: number
  status: string
  issued_at: string
}

export type Payment = {
  reference: string
  order_id: string
  status: "PENDING" | string
}
