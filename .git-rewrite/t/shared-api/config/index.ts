export const API_BASE_URL = ((): string => {
  // Reads environment variable from the host frontend app.
  // Vite projects expose import.meta.env, but in a built library use process.env at runtime.
  // Set REACT_APP_API_BASE_URL in your application to override.
  const envUrl = (typeof window !== 'undefined' && (window as any)?.__SILA_API_BASE_URL) || process?.env?.REACT_APP_API_BASE_URL || process?.env?.VITE_API_BASE_URL;
  return envUrl || '/api';
})();
