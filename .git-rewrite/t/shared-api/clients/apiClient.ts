import axios, { AxiosInstance } from 'axios';
import { API_BASE_URL } from '../config';
import { getToken } from '../utils/storage';

const getDefaultHeaders = () => ({
  'Content-Type': 'application/json',
});

export class ApiClient {
  private instance: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL) {
    this.instance = axios.create({
      baseURL,
      headers: getDefaultHeaders(),
      withCredentials: true,
    });

    this.instance.interceptors.request.use((config) => {
      const token = getToken();
      if (token && config.headers) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    });
  }

  get<T = any>(url: string, params?: Record<string, any>) {
    return this.instance.get<T>(url, { params }).then((r) => r.data);
  }

  post<T = any>(url: string, data?: any) {
    return this.instance.post<T>(url, data).then((r) => r.data);
  }

  put<T = any>(url: string, data?: any) {
    return this.instance.put<T>(url, data).then((r) => r.data);
  }

  delete<T = any>(url: string) {
    return this.instance.delete<T>(url).then((r) => r.data);
  }
}

export default new ApiClient();
