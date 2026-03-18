import axios from 'axios';

export const adminHttp = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

adminHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
