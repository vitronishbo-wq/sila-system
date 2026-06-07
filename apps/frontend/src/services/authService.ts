import http from '@/api/http';
import { UserRole } from '@/types';
import type { AuthResponse, User } from '@/types';
import { apiClient } from '@/api/generated/client';

export const authService = {
  async login(formData: FormData): Promise<AuthResponse & { navigation?: any }> {
    const response = await http.post<AuthResponse & { navigation?: any }>('auth/login', formData);

    // Auto-redirect if backend provides instruction
    if (response.data.navigation?.should_redirect) {
      window.location.hash = response.data.navigation.redirect_to;
    }

    return response.data;
  },

  async getMe(): Promise<User> {
    const token = localStorage.getItem('token') ?? localStorage.getItem('access_token');
    const headers = token ? { Authorization: `Bearer ${token}` } : undefined;

    let data: unknown;
    let error: unknown;

    try {
      ({ data, error } = await apiClient.GET('/api/auth/me', headers ? { headers } : undefined));
    } catch (err) {
      throw err;
    }

    if (error || !data) {
      throw error ?? new Error('Falha ao obter utilizador.');
    }

    return data as User;
  },

  async logout() {
    localStorage.clear();
    return await http.post('auth/logout');
  },

  async refreshToken(): Promise<AuthResponse> {
    const response = await http.post<AuthResponse>('auth/refresh');
    return response.data;
  },

  async register(data: any): Promise<any> {
    const response = await http.post('auth/register', data);
    return response.data;
  },

  getDashboardForRole(role: string): string {
    const dashboards: Record<string, string> = {
      [UserRole.CITIZEN]: '/citizen/portal',
      [UserRole.ADMIN_SUPER]: '/admin',
      [UserRole.ADMIN_CENTRAL]: '/admin',
      [UserRole.ADMIN_PROVINCIAL]: '/admin',
      [UserRole.ADMIN_MUNICIPAL]: '/admin',
      [UserRole.ADMIN_COMMUNAL]: '/admin',
    };
    return dashboards[role] || '/login';
  },

  canAccessRoute(path: string, user: User | null): boolean {
    if (!user) return false;
    const role = user.role;

    if (path.startsWith('/citizen')) {
      return role === UserRole.CITIZEN;
    }

    if (path.startsWith('/admin')) {
      return role !== UserRole.CITIZEN;
    }

    return true;
  }
};
