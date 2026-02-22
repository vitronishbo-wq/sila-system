import { useState, useEffect } from 'react';
import storage from '../utils/storage';

export const useSession = () => {
  const [token, setToken] = useState(() => storage.getToken());

  useEffect(() => {
    const onStorage = () => setToken(storage.getToken());
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  return { token, isAuthenticated: !!token } as const;
};

export default useSession;
