import { ApiClient } from './apiClient';
import type { User } from '../types/User';

const client = new ApiClient();

export const getCurrentUser = async (): Promise<User> => {
  return client.get<User>('/users/me');
};

export const getUser = async (id: number): Promise<User> => {
  return client.get<User>(`/users/${id}`);
};

export default { getCurrentUser, getUser };
