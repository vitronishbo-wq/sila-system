import createClient from 'openapi-fetch';
import type { paths } from '@/api/generated/schema';
import { API_ORIGIN } from '@/utils/runtime';

const API_BASE_URL = API_ORIGIN || '';

const authFetch: typeof fetch = async (input, init) => {
  const token = localStorage.getItem('access_token')
    || localStorage.getItem('token')
    || localStorage.getItem('citizen_token');
  const headers = new Headers(init?.headers);

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  return fetch(input, { ...init, headers });
};

export const apiClient = createClient<paths>({
  baseUrl: API_BASE_URL,
  fetch: authFetch
});
