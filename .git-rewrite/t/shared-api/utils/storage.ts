const TOKEN_KEY = 'sila_token';
const REFRESH_KEY = 'sila_refresh_token';

export const saveToken = (token: string) => {
  if (typeof window !== 'undefined') localStorage.setItem(TOKEN_KEY, token);
};

export const saveRefreshToken = (token: string) => {
  if (typeof window !== 'undefined') localStorage.setItem(REFRESH_KEY, token);
};

export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
};

export const getRefreshToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_KEY);
};

export const removeTokens = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  }
};

export default { saveToken, getToken, saveRefreshToken, getRefreshToken, removeTokens };
