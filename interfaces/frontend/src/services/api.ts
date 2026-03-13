import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../store/authStore";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('access_token');

        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        if (config.data instanceof FormData) {
            delete config.headers["Content-Type"];
        }

        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config;
        const { logout } = useAuthStore.getState();

        if (error.response?.status === 401) {
            const isLoginRoute = originalRequest?.url?.includes("/auth/login");

            if (!isLoginRoute) {
                logout();
                if (window.location.pathname !== "/login") {
                    window.location.href = "/login";
                }
            }
        }

        if (import.meta.env.DEV) {
            if (error.code === "ECONNABORTED") {
                console.error("[SILA] Timeout excedido.");
            }
            if (!error.response) {
                console.error("[SILA] Servidor inacessível.");
            }
        }

        return Promise.reject(error);
    }
);

export default api;