import api from "@/services/api";

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const authService = {
  /**
   * Realiza o login utilizando OAuth2 Password Flow
   * O backend espera application/x-www-form-urlencoded
   */
  async login(params: URLSearchParams): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>("/auth/login", params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  },

  /**
   * Obtém os dados do perfil do utilizador autenticado
   */
  async getCurrentUser() {
    // O token é injetado automaticamente pelo interceptor do api.ts
    const response = await api.get("/auth/me");
    return response.data;
  }
};

/**
 * Persistência manual de tokens para redundância e uso em interceptores
 */
export const saveAuth = (accessToken: string, refreshToken?: string) => {
  localStorage.setItem("access_token", accessToken);
  if (refreshToken) {
    localStorage.setItem("refresh_token", refreshToken);
  }
};

/**
 * Limpeza total de credenciais e estados de persistência
 */
export const clearAuth = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("sila-auth-storage"); // Remove o estado persistido do Zustand
};

export const getAccessToken = () => localStorage.getItem("access_token");
export const isAuthenticated = () => !!localStorage.getItem("access_token");