export interface Service {
  id: string;
  code: string;
  name: string;
  price: number;
}

export interface Order {
  id: string;
  service_id: string;
  status: 'created' | 'submitted' | 'paid';
}

export interface CreateOrderPayload {
  service_id: string;
}

export interface Payment {
  reference: string;
  order_id: string;
  status: 'PENDING' | 'CONFIRMED';
}
