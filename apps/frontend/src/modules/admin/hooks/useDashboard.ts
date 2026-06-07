import { useState, useEffect } from "react";
import { adminService } from "@/modules/admin/services/adminService";
import type { AdminStats, RequestItem } from "@/modules/admin/types";

export const useAdminDashboard = () => {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [requests, setRequests] = useState<RequestItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, reqRes] = await Promise.all([
        adminService.getDashboard(),
        adminService.getRequests()
      ]);
      setStats(statsRes.data);
      setRequests(reqRes.data);
    } catch (error) {
      console.error("Erro no Admin Dashboard", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);
  return { stats, requests, loading, refetch: loadData };
};
