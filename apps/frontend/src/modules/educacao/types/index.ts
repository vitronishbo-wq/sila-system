export type NivelTerritorial = 'nacional' | 'provincial' | 'municipal' | 'escola' | 'operador';

export type WorkflowStep =
  | 'criada'
  | 'escola_valida'
  | 'municipio_confirma'
  | 'provincia_audita'
  | 'concluido'
  | 'cancelado';

export type TransferenciaStep =
  | 'solicitada'
  | 'escola_origem_valida'
  | 'escola_destino_aceita'
  | 'municipio_confirma'
  | 'provincia_audita'
  | 'concluido'
  | 'cancelado';

export interface TerritorialScope {
  nivel: NivelTerritorial;
  province_id?: string;
  province_name?: string;
  municipality_id?: string;
  municipality_name?: string;
  school_id?: string;
  school_name?: string;
}

export interface RoleInfo {
  role: string;
  permissions: string[];
  superiores: string[];
  inferiores: string[];
}

export interface MatriculaWorkflow {
  provider: string;
  student_id: string;
  school_id: string;
  municipality_id?: string;
  province_id?: string;
  step: WorkflowStep;
  history: { step: string; actor: string; timestamp: string }[];
}

export interface TransferenciaWorkflow {
  provider: string;
  student_id: string;
  school_origin_id: string;
  school_destination_id: string;
  municipality_id?: string;
  province_id?: string;
  step: TransferenciaStep;
  history: { step: string; actor: string; timestamp: string }[];
}

export interface DelegationInfo {
  from: string;
  by: string;
  permissions: string[];
  reason?: string;
}

export interface ScopeCheckResult {
  allowed: boolean;
  reason?: string;
  user_scope: TerritorialScope;
  resource_scope: TerritorialScope;
}

export interface DashboardMetrics {
  total_alunos: number;
  total_escolas: number;
  total_professores: number;
  matriculas_pendentes: number;
  matriculas_concluidas: number;
  transferencias_pendentes: number;
  transferencias_concluidas: number;
  delegacoes_ativas: number;
}
