import axios from 'axios';
import { showGlobalToast } from '@/utils/globalToast';
import { API_V1_BASE_URL } from '@/utils/runtime';

export const adminHttp = axios.create({
  baseURL: API_V1_BASE_URL,
});

adminHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

adminHttp.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    if (status === 401 || status === 403) {
      showGlobalToast({ type: 'error', message: 'Sessão expirada. Faça login novamente.' });
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
