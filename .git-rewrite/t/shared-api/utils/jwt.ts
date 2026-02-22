import jwt_decode from 'jwt-decode';

export interface JWTPayload {
  sub?: string | number;
  exp?: number;
  iat?: number;
  [key: string]: any;
}

export const decodeToken = (token: string): JWTPayload | null => {
  try {
    return jwt_decode<JWTPayload>(token);
  } catch (e) {
    return null;
  }
};

export const tokenIsExpired = (token: string | null, offsetSeconds = 30): boolean => {
  if (!token) return true;
  const payload = decodeToken(token);
  if (!payload || !payload.exp) return true;
  const expiry = payload.exp * 1000 - offsetSeconds * 1000;
  return Date.now() >= expiry;
};

export default { decodeToken, tokenIsExpired };
