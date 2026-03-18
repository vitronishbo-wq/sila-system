import { create } from 'zustand';
import api from '@/api/axios';
import type { User } from '@/types/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,

  login: async (email, password) => {
    set({ isLoading: true });

    // Converte para x-www-form-urlencoded para o OAuth2PasswordRequestForm do FastAPI
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const res = await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    const { access_token, refresh_token } = res as any;

    localStorage.setItem('access_token', access_token);
    if (refresh_token) localStorage.setItem('refresh_token', refresh_token);

    // Busca o perfil do usuário logo após o login
    const meRes = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${access_token}` }
    });
    const user = meRes as any;

    set({ user, isAuthenticated: true, isLoading: false });
  },

  logout: async () => {
    try {
      await api.post('/auth/logout'); // invalida no backend
    } catch {
      // continua mesmo se falhar
    } finally {
      localStorage.clear();
      set({ user: null, isAuthenticated: false });
      window.location.href = '/login';
    }
  },

  fetchUser: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    set({ isLoading: true });
    try {
      const res = await api.get('/auth/me');
      set({ user: res as any, isAuthenticated: true });
    } catch {
      useAuthStore.getState().logout();
    } finally {
      set({ isLoading: false });
    }
  },
}));