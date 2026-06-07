import axios from 'axios';
import { API_URL } from '@/constants';

export const citizenHttp = axios.create({
  baseURL: API_URL,
});

citizenHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem('citizen_token')
    || localStorage.getItem('token')
    || localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
