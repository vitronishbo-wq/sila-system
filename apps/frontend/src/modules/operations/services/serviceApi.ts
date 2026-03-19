import type { Service } from '@/types/api';
import { operationsService } from './operationsService';

export const getServices = async (): Promise<Service[]> => {
  return operationsService.listServices();
};
