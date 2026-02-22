import { useMemo } from 'react';
import ApiClient from '../clients/apiClient';

export const useApi = () => {
  // Memoize the client so it doesn't recreate on each render
  const client = useMemo(() => ApiClient, []);
  return client;
};

export default useApi;
