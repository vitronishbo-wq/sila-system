import { useAuthStore } from "@/store/authStore";

export const useAuth = () => {
    const { user, logout } = useAuthStore();

    return {
        user,
        logout,
    };
};
