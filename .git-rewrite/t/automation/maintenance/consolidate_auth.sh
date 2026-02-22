#!/bin/bash

# 🔄 CONSOLIDAÇÃO INTELIGENTE DE AUTENTICAÇÃO
# Objetivo: Consolidar as duas implementações de auth em uma única versão otimizada

set -e

echo "🔄 CONSOLIDANDO IMPLEMENTAÇÕES DE AUTENTICAÇÃO"
echo "=============================================="

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Arquivos
WEB_AUTH="frontend/apps/web/src/features/auth/api.ts"
SHARED_AUTH="frontend/packages/shared-api/src/auth.ts"
BACKUP_DIR="backups/auth_consolidation_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"

# Fazer backup
log "📁 Fazendo backup das implementações existentes"
cp "$WEB_AUTH" "$BACKUP_DIR/web_auth_backup.ts"
cp "$SHARED_AUTH" "$BACKUP_DIR/shared_auth_backup.ts"

# Criar implementação consolidada no shared-api
log "🔧 Criando implementação consolidada no shared-api"

cat > "$SHARED_AUTH" << 'EOF'
/**
 * Módulo de API para autenticação - IMPLEMENTAÇÃO CONSOLIDADA
 *
 * @description Gerencia todas as operações de autenticação do usuário,
 * incluindo login, logout, obtenção de dados do usuário atual e
 * renovação de tokens de acesso.
 *
 * Consolidado em: P0 - Centralização Arquitetônica
 * Data: $(date +%Y-%m-%d)
 */

import { api } from './client';

// ========================================
// TIPOS CONSOLIDADOS
// ========================================

export type Role = 'admin' | 'operador' | 'cidadao';

export interface LoginCredentials {
  /** Email ou nome de usuário para autenticação */
  email: string;
  /** Senha do usuário */
  password: string;
}

export interface AuthTokens {
  /** Token de acesso JWT */
  access_token: string;
  /** Token de refresh para renovação */
  refresh_token: string;
  /** Tipo do token (geralmente "Bearer") */
  token_type?: string;
}

export interface User {
  /** ID único do usuário */
  id: string;
  /** Nome do usuário */
  name: string;
  /** Email do usuário */
  email: string;
  /** Lista de papéis/roles do usuário */
  roles: Role[];
  /** Status do usuário */
  status: 'active' | 'inactive';
  /** Lista de permissões específicas */
  permissions?: string[];
}

// ========================================
// API FUNCTIONS CONSOLIDADAS
// ========================================

export const authAPI = {
  /**
   * Realiza login do usuário no sistema
   *
   * @param credentials - Credenciais de login (email/password)
   * @returns Promise com tokens de autenticação
   *
   * @example
   * ```typescript
   * try {
   *   const tokens = await authAPI.login({
   *     email: 'admin@sila.gov.ao',
   *     password: 'senha123'
   *   });
   *
   *   // Salvar tokens no localStorage
   *   localStorage.setItem('accessToken', tokens.access_token);
   *   localStorage.setItem('refreshToken', tokens.refresh_token);
   *
   *   console.log('Login realizado com sucesso!');
   * } catch (error) {
   *   console.error('Erro no login:', error);
   * }
   * ```
   */
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const response = await api.post<AuthTokens>('/auth/login', credentials);
    return response.data;
  },

  /**
   * Realiza logout do usuário atual
   *
   * @description Remove sessão do servidor e limpa tokens locais
   * @returns Promise<void>
   */
  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      // Ignore logout errors - always clear local tokens
    } finally {
      localStorage.removeItem('auth:accessToken');
      localStorage.removeItem('auth:refreshToken');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  },

  /**
   * Obtém dados do usuário atualmente autenticado
   *
   * @returns Promise com dados completos do usuário
   */
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  /**
   * Renova o token de acesso usando o refresh token
   *
   * @param refreshToken - Token de refresh válido (opcional, pega do localStorage)
   * @returns Promise com novos tokens de autenticação
   */
  refreshToken: async (refreshToken?: string): Promise<AuthTokens> => {
    const token = refreshToken || localStorage.getItem('auth:refreshToken') || localStorage.getItem('refreshToken');

    if (!token) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<AuthTokens>('/auth/refresh', {
      refresh_token: token
    });

    return response.data;
  },

  /**
   * Login administrativo (se necessário)
   *
   * @param data - Dados de login administrativo
   * @returns Promise com resposta do login admin
   */
  adminLogin: async (data: any) => {
    const response = await api.post('/admin/auth/login', data);
    return response.data;
  }
};

// ========================================
// UTILITÁRIOS DE TOKEN
// ========================================

export const tokenManager = {
  setTokens: (tokens: AuthTokens) => {
    localStorage.setItem('auth:accessToken', tokens.access_token);
    localStorage.setItem('auth:refreshToken', tokens.refresh_token);

    // Compatibilidade com implementações antigas
    localStorage.setItem('accessToken', tokens.access_token);
    localStorage.setItem('refreshToken', tokens.refresh_token);
  },

  getAccessToken: () => {
    return localStorage.getItem('auth:accessToken') || localStorage.getItem('accessToken');
  },

  getRefreshToken: () => {
    return localStorage.getItem('auth:refreshToken') || localStorage.getItem('refreshToken');
  },

  clearTokens: () => {
    localStorage.removeItem('auth:accessToken');
    localStorage.removeItem('auth:refreshToken');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  isTokenValid: (token: string | null): boolean => {
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }
};

// ========================================
// UTILITÁRIOS DE ROLE
// ========================================

export const roleUtils = {
  hasRole: (user: User | null, roles: Role | Role[]): boolean => {
    if (!user) return false;

    const userRoles = user.roles;
    const requiredRoles = Array.isArray(roles) ? roles : [roles];

    return requiredRoles.some(role => userRoles.includes(role));
  },

  isAdmin: (user: User | null): boolean => {
    return roleUtils.hasRole(user, 'admin');
  },

  isOperador: (user: User | null): boolean => {
    return roleUtils.hasRole(user, 'operador');
  },

  isCidadao: (user: User | null): boolean => {
    return roleUtils.hasRole(user, 'cidadao');
  }
};

// ========================================
// INTERCEPTORS PARA AUTENTICAÇÃO
// ========================================

// Configurar interceptors no cliente HTTP
api.interceptors.request.use(
  (config) => {
    const token = tokenManager.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newTokens = await authAPI.refreshToken();
        tokenManager.setTokens(newTokens);

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        tokenManager.clearTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
EOF

success "✅ Implementação consolidada criada no shared-api"

# Refatorar o arquivo web para usar shared-api
log "🔧 Refatorando web app para usar shared-api"

cat > "$WEB_AUTH" << 'EOF'
/**
 * MÓDULO DE AUTENTICAÇÃO - REFATORADO PARA SHARED-API
 *
 * 🚨 ARQUIVO REFATORADO - P0: Centralização Arquitetônica
 *
 * Este arquivo agora usa a implementação centralizada do shared-api.
 * Toda a lógica de autenticação foi movida para packages/shared-api/src/auth.ts
 *
 * Data da refatoração: $(date +%Y-%m-%d)
 */

// Re-exportar tudo do shared-api para manter compatibilidade
export * from '../../../packages/shared-api/src/auth';

// Importar tipos específicos se necessário
export type {
  LoginCredentials,
  AuthTokens,
  User,
  Role
} from '../../../packages/shared-api/src/auth';

// Importar funções da API
export {
  authAPI,
  tokenManager,
  roleUtils
} from '../../../packages/shared-api/src/auth';

// Manter compatibilidade com imports antigos
export { authAPI as default } from '../../../packages/shared-api/src/auth';
EOF

success "✅ Web app refatorado para usar shared-api"

# Verificar se o cliente HTTP existe no shared-api
SHARED_CLIENT="frontend/packages/shared-api/src/client.ts"
if [ ! -f "$SHARED_CLIENT" ]; then
    log "🔧 Criando cliente HTTP no shared-api"

    cat > "$SHARED_CLIENT" << 'EOF'
/**
 * Cliente HTTP centralizado - SILA System
 * P0: Centralização Arquitetônica
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

class HttpClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.REACT_APP_API_URL || 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }

  // Expor interceptors para configuração externa
  get interceptors() {
    return this.client.interceptors;
  }
}

// Instância singleton
export const api = new HttpClient();

// Exportar também como default
export default api;
EOF

    success "✅ Cliente HTTP criado no shared-api"
fi

# Criar arquivo de índice do shared-api
SHARED_INDEX="frontend/packages/shared-api/src/index.ts"
if [ ! -f "$SHARED_INDEX" ]; then
    log "🔧 Criando arquivo de índice do shared-api"

    cat > "$SHARED_INDEX" << 'EOF'
/**
 * Shared API - Ponto de entrada centralizado
 * P0: Centralização Arquitetônica - SILA System
 */

// Exportar tudo do módulo de autenticação
export * from './auth';

// Exportar cliente HTTP
export * from './client';

// Exportar tipos comuns
export type { ApiResponse } from './client';
EOF

    success "✅ Arquivo de índice criado"
fi

echo ""
echo "✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!"
echo "====================================="
echo ""
echo "📁 Backup salvo em: $BACKUP_DIR"
echo "🔧 Shared API: $SHARED_AUTH"
echo "🔧 Web App: $WEB_AUTH"
echo ""
echo "🎯 Próximos passos:"
echo "1. Testar login/logout no web app"
echo "2. Verificar se não há erros de importação"
echo "3. Continuar com a refatoração dos módulos restantes"
echo ""
