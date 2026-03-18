
import axios from 'axios';
import { API_URL } from '../constants';

const http = axios.create({
  baseURL: API_URL,
  timeout: 30000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  console.log(`[API REQUEST] ${config.method?.toUpperCase()} ${config.url}`, config.data || '');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

http.interceptors.response.use(
  (response) => {
    console.log(`[API RESPONSE] ${response.status} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error(`[API ERROR] ${error.response?.status || 'NETWORK ERROR'} ${error.config?.url}`, error.response?.data || error.message);
    if (error.response?.status === 401) {
      const url = error.config?.url || '';
      const isAdminCall = url.includes('/admin/');
      const hasCitizenSession = !!localStorage.getItem('citizen_token');
      if (isAdminCall && hasCitizenSession) {
        console.warn('[API ERROR] 401 em rota admin com sessão citizen ativa', url);
      } else {
        localStorage.clear();
        window.location.hash = '/login';
      }
    }
    if (error.response?.status === 403) {
      console.error('🚫 Access Denied:', error.config?.url);
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        const user = JSON.parse(savedUser);
        // Dispatch custom event or handle redirect
        if (user.role === 'CITIZEN') {
          window.location.hash = '/citizen/portal';
        } else {
          window.location.hash = '/admin';
        }
      } else {
        localStorage.clear();
        window.location.hash = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default http;
