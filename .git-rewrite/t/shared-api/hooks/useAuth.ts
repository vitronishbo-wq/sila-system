import { useState, useEffect, useCallback } from 'react';
import { login, logout as apiLogout, refreshToken as apiRefresh } from '../clients/authClient';
import storage from '../utils/storage';
import type { LoginRequest, Tokens } from '../types/Auth';
import { tokenIsExpired, decodeToken } from '../utils/jwt';
import { getCurrentUser } from '../clients/userClient';

export const useAuth = () => {
  const [tokens, setTokens] = useState<Tokens | null>(() => {
    const token = storage.getToken();
    const refresh = storage.getRefreshToken();
    return token ? { access_token: token, refresh_token: refresh ?? undefined } : null;
  });

  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadUser = useCallback(async () => {
    try {
      const u = await getCurrentUser();
      setUser(u);
    } catch (e) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    (async () => {
      if (tokens?.access_token && !tokenIsExpired(tokens.access_token)) {
        await loadUser();
      }
      setLoading(false);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const performLogin = async (data: LoginRequest) => {
    const res = await login(data);
    storage.saveToken(res.access_token);
    if (res.refresh_token) storage.saveRefreshToken(res.refresh_token);
    setTokens(res);
    await loadUser();
    return res;
  };

  const performLogout = async () => {
    await apiLogout();
    storage.removeTokens();
    setUser(null);
    setTokens(null);
  };

  const doRefresh = async () => {
    const res = await apiRefresh();
    storage.saveToken(res.access_token);
    if (res.refresh_token) storage.saveRefreshToken(res.refresh_token);
    setTokens(res);
    return res;
  };

  return {
    tokens,
    user,
    loading,
    login: performLogin,
    logout: performLogout,
    refresh: doRefresh,
  } as const;
};

export default useAuth;
