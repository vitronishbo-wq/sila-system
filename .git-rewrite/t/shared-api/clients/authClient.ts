import { ApiClient } from './apiClient';
import type { LoginRequest, Tokens } from '../types/Auth';

const client = new ApiClient();

export const login = async (data: LoginRequest): Promise<Tokens> => {
  const response = await client.post<Tokens>('/auth/login', data);
  return response;
};

export const refreshToken = async (): Promise<Tokens> => {
  const response = await client.post<Tokens>('/auth/refresh');
  return response;
};

export const logout = async () => {
  await client.post('/auth/logout');
};
