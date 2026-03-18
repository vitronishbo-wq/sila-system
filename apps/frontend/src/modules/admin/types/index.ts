export interface AdminStats {
  total_requests: number;
  pending_approvals: number;
  active_users: number;
  system_health: string;
}

export interface RequestItem {
  id: string;
  citizen_name: string;
  service_type: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  created_at: string;
}
