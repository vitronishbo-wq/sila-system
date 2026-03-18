import axios from 'axios';
import { API_URL } from '../constants';

export const citizenHttp = axios.create({
  baseURL: API_URL,
});

citizenHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem('citizen_token') || localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

citizenHttp.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('citizen_token');
    }
    return Promise.reject(error);
  },
);
