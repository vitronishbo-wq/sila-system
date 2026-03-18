import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const axiosInstance: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000, // padrão 30s
});

// Request interceptor – Bearer token
axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    // Timeout maior para uploads
    if (config.url?.includes('/documents/upload')) {
        config.timeout = 120000; // 2 minutos
    }
    return config;
});

// Response interceptor – refresh + erros globais
axiosInstance.interceptors.response.use(
    (response) => response.data,
    async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const params = new URLSearchParams();
                    params.append('refresh_token', refreshToken);

                    const res = await axios.post(`${API_BASE_URL}/auth/refresh`, params, {
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                    });

                    const { access_token, refresh_token: newRefreshToken } = res.data;
                    localStorage.setItem('access_token', access_token);
                    if (newRefreshToken) localStorage.setItem('refresh_token', newRefreshToken);

                    originalRequest.headers ??= {};
                    originalRequest.headers.Authorization = `Bearer ${access_token}`;
                    return axiosInstance(originalRequest);
                } catch {
                    localStorage.clear();
                    window.location.href = '/login';
                }
            } else {
                localStorage.clear();
                window.location.href = '/login';
            }
        }

        // 403 → dispatch evento global para UI capturar
        if (error.response?.status === 403) {
            window.dispatchEvent(new CustomEvent('access-denied', {
                detail: {
                    message: (error.response.data as any)?.detail || 'Acesso restrito para esta ação.',
                    status: 403
                }
            }));
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
