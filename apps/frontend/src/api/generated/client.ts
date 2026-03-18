import createClient from 'openapi-fetch';
import type { paths } from './schema';

const rawBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_BASE_URL = rawBaseUrl.replace(/\/api(?:\/v1)?\/?$/, '');

export const apiClient = createClient<paths>({
  baseUrl: API_BASE_URL,
  fetch: async (input, init) => {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    const headers = new Headers(init?.headers);

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    return fetch(input, { ...init, headers });
  }
});
