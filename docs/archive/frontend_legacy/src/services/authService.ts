import http from '../api/http';
import { AdminLevel, UserRole } from '../types';
import type { AuthResponse, User } from '../types';

type RawUserLike = Partial<User> & {
  role?: unknown;
  roles?: unknown;
};

const ROLE_NORMALIZATION_MAP: Record<string, UserRole> = {
  CITIZEN: UserRole.CITIZEN,
  CIDADAO: UserRole.CITIZEN,
  ADMIN: UserRole.ADMIN_CENTRAL,
  SUPERADMIN: UserRole.ADMIN_SUPER,
  MANAGER: UserRole.ADMIN_CENTRAL,
  OFFICER: UserRole.ADMIN_MUNICIPAL,
  ADMIN_SUPER: UserRole.ADMIN_SUPER,
  SUPER_ADMIN: UserRole.ADMIN_SUPER,
  ADMIN_CENTRAL: UserRole.ADMIN_CENTRAL,
  CENTRAL_ADMIN: UserRole.ADMIN_CENTRAL,
  PROVINCE_ADMIN: UserRole.ADMIN_PROVINCIAL,
  ADMIN_PROVINCIAL: UserRole.ADMIN_PROVINCIAL,
  PROVINCIAL_ADMIN: UserRole.ADMIN_PROVINCIAL,
  MUNICIPALITY_ADMIN: UserRole.ADMIN_MUNICIPAL,
  ADMIN_MUNICIPAL: UserRole.ADMIN_MUNICIPAL,
  MUNICIPAL_ADMIN: UserRole.ADMIN_MUNICIPAL,
  COMMUNE_MANAGER: UserRole.ADMIN_COMMUNAL,
  COMMUNE_ADMIN: UserRole.ADMIN_COMMUNAL,
  ADMIN_COMMUNAL: UserRole.ADMIN_COMMUNAL,
  COMMUNAL_ADMIN: UserRole.ADMIN_COMMUNAL,
};

const ROLE_PRIORITY: UserRole[] = [
  UserRole.ADMIN_SUPER,
  UserRole.ADMIN_CENTRAL,
  UserRole.ADMIN_PROVINCIAL,
  UserRole.ADMIN_MUNICIPAL,
  UserRole.ADMIN_COMMUNAL,
  UserRole.CITIZEN,
];

const normalizeRoleToken = (value: unknown): UserRole | null => {
  if (typeof value !== 'string' || !value.trim()) {
    return null;
  }

  const normalized = value
    .trim()
    .toUpperCase()
    .replace(/^ROLE_/, '')
    .replace(/[ -]/g, '_');

  return ROLE_NORMALIZATION_MAP[normalized] ?? null;
};

const normalizeAdminLevel = (value: unknown): AdminLevel => {
  const normalized = String(value || '').trim().toUpperCase().replace(/[ -]/g, '_');

  if (normalized.includes('SUPER')) return AdminLevel.SUPER;
  if (normalized.includes('CENTRAL') || normalized === 'ADMIN' || normalized === 'MANAGER') {
    return AdminLevel.CENTRAL;
  }
  if (normalized.includes('PROVIN')) return AdminLevel.PROVINCIAL;
  if (normalized.includes('MUNIC')) return AdminLevel.MUNICIPAL;
  if (normalized.includes('COMMUN') || normalized.includes('COMUN') || normalized.includes('LOCAL')) {
    return AdminLevel.COMMUNAL;
  }

  return AdminLevel.CENTRAL;
};

const extractRoleFromUser = (user: RawUserLike | null | undefined): UserRole | null => {
  if (!user) {
    return null;
  }

  const resolvedRoles = new Set<UserRole>();

  const directRole = normalizeRoleToken(user.role);
  if (directRole) {
    resolvedRoles.add(directRole);
  }

  if (Array.isArray(user.roles)) {
    for (const rawRole of user.roles) {
      const parsed = normalizeRoleToken(rawRole);
      if (parsed) {
        resolvedRoles.add(parsed);
      }
    }
  }

  for (const role of ROLE_PRIORITY) {
    if (resolvedRoles.has(role)) {
      return role;
    }
  }

  return null;
};

export const authService = {
  async login(formData: FormData): Promise<AuthResponse & { navigation?: any }> {
    const response = await http.post<AuthResponse & { navigation?: any }>('auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Auto-redirect if backend provides instruction
    if (response.data.navigation?.should_redirect) {
      window.location.hash = response.data.navigation.redirect_to;
    }

    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await http.get<RawUserLike>('auth/me');
    const raw = response.data as Record<string, unknown>;
    const resolvedRole = extractRoleFromUser(response.data);
    const rolesRaw = Array.isArray(raw.roles) ? raw.roles : [];

    const email = typeof raw.email === 'string' ? raw.email : '';
    const usernameCandidate = [raw.username, raw.full_name]
      .find((value): value is string => typeof value === 'string' && value.trim().length > 0);
    const username = usernameCandidate || (email.includes('@') ? email.split('@')[0] : email) || 'utilizador';
    const role = resolvedRole
      || (rolesRaw.map((v) => String(v).toUpperCase()).includes('CITIZEN')
        ? UserRole.CITIZEN
        : UserRole.ADMIN_CENTRAL);

    const idRaw = raw.id ?? raw.user_id ?? '';
    const level = normalizeAdminLevel(raw.level ?? raw.administrative_level ?? raw.role);
    const territory = raw.territory_id ?? raw.region_id ?? null;

    return {
      ...(response.data as User),
      id: String(idRaw),
      email,
      username,
      level,
      role,
      territory_id: territory ? String(territory) : null,
      is_active: typeof raw.is_active === 'boolean' ? raw.is_active : true,
    };
  },

  async logout() {
    localStorage.clear();
    return await http.post('auth/logout');
  },

  async refreshToken(): Promise<AuthResponse> {
    const response = await http.post<AuthResponse>('auth/refresh');
    return response.data;
  },

  async register(data: any): Promise<any> {
    const response = await http.post('auth/register', data);
    return response.data;
  },

  getUserRole(user: RawUserLike | null | undefined): UserRole | null {
    return extractRoleFromUser(user);
  },

  getDashboardForRole(roleOrUser: string | RawUserLike | null | undefined): string {
    const resolvedRole = typeof roleOrUser === 'string'
      ? normalizeRoleToken(roleOrUser)
      : extractRoleFromUser(roleOrUser);

    const dashboards: Record<string, string> = {
      [UserRole.CITIZEN]: '/citizen/portal',
      [UserRole.ADMIN_SUPER]: '/admin',
      [UserRole.ADMIN_CENTRAL]: '/admin',
      [UserRole.ADMIN_PROVINCIAL]: '/admin',
      [UserRole.ADMIN_MUNICIPAL]: '/admin',
      [UserRole.ADMIN_COMMUNAL]: '/admin',
    };

    if (!resolvedRole) {
      if (roleOrUser && typeof roleOrUser !== 'string' && Array.isArray(roleOrUser.roles)) {
        const upperRoles = roleOrUser.roles.map((value) => String(value).toUpperCase());
        if (upperRoles.includes('CITIZEN') || upperRoles.includes('CIDADAO')) {
          return '/citizen/portal';
        }
        if (upperRoles.length > 0) {
          return '/admin';
        }
      }
      return '/login';
    }

    return dashboards[resolvedRole] || '/login';
  },

  canAccessRoute(path: string, user: User | null): boolean {
    if (!user) return false;
    const role = extractRoleFromUser(user);
    if (!role) return false;

    if (path.startsWith('/citizen')) {
      return role === UserRole.CITIZEN;
    }

    if (path.startsWith('/admin')) {
      return role !== UserRole.CITIZEN;
    }

    return true;
  }
};
