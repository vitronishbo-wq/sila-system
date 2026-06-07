import { adminHttp } from "@/api/adminHttp";

export const adminService = {
  getDashboard: () => adminHttp.get("/admin/dashboard"),
  getRequests: () => adminHttp.get("/admin/requests"),
};
