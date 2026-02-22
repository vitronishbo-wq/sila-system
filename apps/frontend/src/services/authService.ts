import http from '../api/http';
import { AuthResponse, User, UserRole } from '../types';

export const authService = {
  async login(formData: FormData): Promise<AuthResponse & { navigation?: any }> {
    const response = await http.post<AuthResponse & { navigation?: any }>('auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Auto-redirect if backend provides instruction
    if (response.data.navigation?.should_redirect) {
      window.location.hash = response.data.navigation.redirect_to;
    }

    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await http.get<User>('auth/me');
    return response.data;
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
