
export enum UserRole {
  ADMIN_SUPER = 'ADMIN_SUPER',
  ADMIN_CENTRAL = 'ADMIN_CENTRAL',
  ADMIN_PROVINCIAL = 'ADMIN_PROVINCIAL',
  ADMIN_MUNICIPAL = 'ADMIN_MUNICIPAL',
  ADMIN_COMMUNAL = 'ADMIN_COMMUNAL',
  CITIZEN = 'CITIZEN'
}

export enum AdminLevel {
  SUPER = 'super',
  CENTRAL = 'central',
  PROVINCIAL = 'provincial',
  MUNICIPAL = 'municipal',
  COMMUNAL = 'communal'
}

export enum DocumentStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  APPROVED = "approved",
  REJECTED = "rejected",
  ACTIVE = "active",
  CANCELLED = "cancelled"
}

export interface User {
  id: string;
  email: string;
  username: string;
  level: AdminLevel;
  role: UserRole;
  territory_id?: string | null;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Citizen {
  id: string;
  bi_number: string;
  full_name: string;
  birth_date: string;
  gender: string;
  phone: string;
  email: string;
  province_id: string | null;
  municipality_id: string | null;
  created_at: string;
}

export interface Document {
  id: string;
  citizen_id: string;
  citizen_name?: string;
  citizen_bi?: string;
  document_type: string;
  status: DocumentStatus;
  document_number: string;
  request_date: string;
  processing_date?: string;
  completion_date?: string;
  expiry_date?: string;
  notes?: string;
  rejection_reason?: string;
}

export interface TerritoryNode {
  id: string;
  name: string;
  code: string;
  type: "province" | "municipality" | "commune";
  parent_id: string | null;
  children?: TerritoryNode[];
}

export interface KPIStats {
  total_citizens: number;
  total_documents: number;
  pending_requests: number;
  completed_requests: number;
}
