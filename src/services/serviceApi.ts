import { api } from "../api/axios"
import { Service } from "../types/api"

export const getServices = async (): Promise<Service[]> => {
  const res = await api.get("/v1/services")
  return res.data
}
