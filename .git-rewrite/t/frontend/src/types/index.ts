export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  status?: number;
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
