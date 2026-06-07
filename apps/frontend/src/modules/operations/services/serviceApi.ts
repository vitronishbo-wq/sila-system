import type { Service } from '@/types/api';
import { operationsService } from '@/modules/operations/services/operationsService';

export const getServices = async (): Promise<Service[]> => {
  return operationsService.listServices();
};
