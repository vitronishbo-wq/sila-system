import axios from 'axios';

export const citizenHttp = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

citizenHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem('citizen_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
