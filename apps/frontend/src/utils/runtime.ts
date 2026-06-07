const DEFAULT_DEV_API_PORT = (import.meta.env.VITE_API_PORT || '8000').trim();

const trimTrailingSlash = (value: string): string => value.replace(/\/+$/, '');

const normalizeApiV1BaseUrl = (value: string): string => {
  const normalized = trimTrailingSlash(value.trim());

  if (normalized.endsWith('/api/v1')) {
    return normalized;
  }

  if (normalized.endsWith('/api')) {
    return `${normalized}/v1`;
  }

  return normalized;
};

const deriveBrowserApiUrl = (): string => {
  if (typeof window === 'undefined') {
    return `http://127.0.0.1:${DEFAULT_DEV_API_PORT}/api/v1`;
  }

  const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
  const hostname = window.location.hostname || 'localhost';
  return `${protocol}//${hostname}:${DEFAULT_DEV_API_PORT}/api/v1`;
};

const configuredApiUrl = import.meta.env.VITE_API_URL?.trim();

export const API_V1_BASE_URL = normalizeApiV1BaseUrl(
  configuredApiUrl && configuredApiUrl.length > 0 ? configuredApiUrl : deriveBrowserApiUrl()
);

export const API_URL = `${API_V1_BASE_URL.replace(/\/?$/, '/')}`;

export const API_ROOT_URL = API_V1_BASE_URL.replace(/\/api\/v1\/?$/, '/api');

export const API_ORIGIN = (() => {
  const origin = API_V1_BASE_URL.replace(/\/api(?:\/v1)?\/?$/, '');
  return origin === API_V1_BASE_URL ? '' : origin;
})();

export const withApiOrigin = (path: string): string => {
  if (/^https?:\/\//.test(path)) {
    return path;
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return API_ORIGIN ? `${API_ORIGIN}${normalizedPath}` : normalizedPath;
};
