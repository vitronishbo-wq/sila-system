"""
Constantes Globais - RBAC, Hierarquia Territorial e Tipos de Dados
====================================================================
Define valores válidos para garantir consistência em toda a aplicação.
Sincronizado entre: models, seeds, validações e frontend.
"""

from enum import Enum

# ============================================================================
# 📊 STATUS GLOBAIS - Usado em Models e Validadores
# ============================================================================

class EntityStatus(str, Enum):
    """
    Status padronizados para entidades (Requests, Documents, Payments, etc).
    Evita strings hardcoded como 'pending', 'approved'.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    PAID = "paid"
    DRAFT = "draft"
    SUSPENDED = "suspended"


# ============================================================================
# 🔐 ROLES (Papéis de Utilizador) - RBAC Hierárquico
# ============================================================================

class UserRole(str, Enum):
    """
    Hierarquia de Roles: Super > Central > Provincial > Municipal > Communal > Citizen
    
    Cada role herda permissões do nível anterior (menor).
    Exemplo: admin_provincial pode fazer tudo que municipal faz, e mais.
    Citizen é um role separado com acesso apenas ao portal do munícipe.
    """
    ADMIN_SUPER = "admin_super"          # 👑 Superintendente: Todas as ações, todos os serviços
    ADMIN_CENTRAL = "admin_central"      # 🏛️ Nível Central: Gestão nacional
    ADMIN_PROVINCIAL = "admin_provincial"  # 📍 Nível Provincial: Jurisdição de província
    ADMIN_MUNICIPAL = "admin_municipal"    # 🏢 Nível Municipal: Jurisdição de município
    ADMIN_COMMUNAL = "admin_communal"      # 🏘️ Nível Communal: Jurisdição de comuna
    CITIZEN = "citizen"                  # 👤 Cidadão: Acesso ao portal do munícipe


# Ordenação de roles por hierarquia (0 = menor, 5 = maior)
ROLE_HIERARCHY = {
    UserRole.ADMIN_SUPER: 5,
    UserRole.ADMIN_CENTRAL: 4,
    UserRole.ADMIN_PROVINCIAL: 3,
    UserRole.ADMIN_MUNICIPAL: 2,
    UserRole.ADMIN_COMMUNAL: 1,
    UserRole.CITIZEN: 0,
}

# Roles válidos (lista de strings para validação)
VALID_ROLES = [role.value for role in UserRole]

# ============================================================================
# 🗺️ NÍVEIS ADMINISTRATIVOS - Correlacionados com Roles
# ============================================================================

class AdminLevel(str, Enum):
    """
    Níveis Administrativos: Define a jurisdição territorial do utilizador.
    Deve corresponder à role para validação.
    """
    SUPER = "super"
    CENTRAL = "central"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"
    COMMUNAL = "communal"
    CITIZEN = "citizen"


# Mapeamento Role → Level
ROLE_TO_LEVEL = {
    UserRole.ADMIN_SUPER: AdminLevel.SUPER,
    UserRole.ADMIN_CENTRAL: AdminLevel.CENTRAL,
    UserRole.ADMIN_PROVINCIAL: AdminLevel.PROVINCIAL,
    UserRole.ADMIN_MUNICIPAL: AdminLevel.MUNICIPAL,
    UserRole.ADMIN_COMMUNAL: AdminLevel.COMMUNAL,
    UserRole.CITIZEN: AdminLevel.CITIZEN,
}

VALID_LEVELS = [level.value for level in AdminLevel]

# ============================================================================
# 🗺️ TIPOS TERRITORIAIS - Hierarquia Geográfica
# ============================================================================

class TerritoryType(str, Enum):
    """
    Hierarquia Territorial de Angola:
    Province (topo) → Municipality → Commune (base)
    """
    PROVINCE = "province"
    MUNICIPALITY = "municipality"
    COMMUNE = "commune"


# Hierarquia territorial: qual pode ser parent de qual
TERRITORY_HIERARCHY = {
    TerritoryType.PROVINCE: None,           # Províncias não têm parent
    TerritoryType.MUNICIPALITY: TerritoryType.PROVINCE,
    TerritoryType.COMMUNE: TerritoryType.MUNICIPALITY,
}

VALID_TERRITORY_TYPES = [t.value for t in TerritoryType]

# ============================================================================
# 🔐 PERMISSÕES POR ROLE - RBAC Matrix
# ============================================================================

class PermissionAction(str, Enum):
    """Actions que um role pode ter sobre um serviço"""
    READ = "read"
    WRITE = "write"
    APPROVE = "approve"


# Matriz de permissões: role → serviço → ações permitidas
PERMISSIONS_MATRIX = {
    UserRole.ADMIN_SUPER: {
        # Super Admin tem todas as permissões em todos os serviços
        "all_services": {"read", "write", "approve"},
    },
    UserRole.ADMIN_CENTRAL: {
        # Central: Gestão de validação de documentos e serviços
        "doc_validation": {"read", "write", "approve"},
        "service_mgmt": {"read", "write", "approve"},
    },
    UserRole.ADMIN_PROVINCIAL: {
        # Provincial: Validação SEM aprovação
        "doc_validation": {"read", "write"},  # Sem approve
    },
    UserRole.ADMIN_MUNICIPAL: {
        # Municipal: Leitura apenas
        "doc_validation": {"read"},
    },
    UserRole.ADMIN_COMMUNAL: {
        # Communal: Leitura apenas
        "doc_validation": {"read"},
    },
}

# ============================================================================
# 📦 SERVIÇOS ESSENCIAIS vs CENTRALIZADOS
# ============================================================================

ESSENTIAL_SERVICES = {
    # Público, com ícone, visível na homepage
    "BI": {
        "name": "Bilhete de Identidade",
        "icon_slug": "contact-round",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "RC": {
        "name": "Registo Civil",
        "icon_slug": "file-text",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "SA": {
        "name": "Saúde",
        "icon_slug": "heart-pulse",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "ED": {
        "name": "Educação",
        "icon_slug": "graduation-cap",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "AS": {
        "name": "Água e Saneamento",
        "icon_slug": "droplets",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "EN": {
        "name": "Energia",
        "icon_slug": "zap",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "EM": {
        "name": "Emprego",
        "icon_slug": "briefcase",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "MO": {
        "name": "Moradia",
        "icon_slug": "home",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "TR": {
        "name": "Transportes",
        "icon_slug": "bus",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "NO": {
        "name": "Notariado",
        "icon_slug": "stamp",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "LI": {
        "name": "Licenciamento",
        "icon_slug": "clipboard-check",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
    "NIF": {
        "name": "Cartão de Contribuinte",
        "icon_slug": "credit-card",
        "scope": "public",
        "is_essential": True,
        "is_public": True,
    },
}

CENTRAL_SERVICES = {
    # Centralizados, sem ícone, gestão interna
    "doc_validation": {
        "name": "Validação de Documentos",
        "scope": "central",
        "is_essential": False,
        "is_public": False,
        "icon_slug": None,
    },
    "service_mgmt": {
        "name": "Gestão de Serviços",
        "scope": "central",
        "is_essential": False,
        "is_public": False,
        "icon_slug": None,
    },
}

# Todos os serviços válidos
ALL_SERVICE_CODES = set(ESSENTIAL_SERVICES.keys()) | set(CENTRAL_SERVICES.keys())

# ============================================================================
# 🔗 MAPEAMENTO DE VALIDAÇÃO
# ============================================================================

def validate_role(role: str) -> bool:
    """Valida se um role é válido"""
    return role in VALID_ROLES


def validate_level(level: str) -> bool:
    """Valida se um nível administrativo é válido"""
    return level in VALID_LEVELS


def validate_territory_type(territory_type: str) -> bool:
    """Valida se um tipo territorial é válido"""
    return territory_type in VALID_TERRITORY_TYPES


def validate_service_code(service_code: str) -> bool:
    """Valida se um código de serviço é válido"""
    return service_code in ALL_SERVICE_CODES


def get_role_level(role: str) -> str:
    """Retorna o level correspondente a um role"""
    for user_role, level in ROLE_TO_LEVEL.items():
        if user_role.value == role:
            return level.value
    raise ValueError(f"Role inválido: {role}")


def can_access_territory(user_role: str, user_level: str, territory_type: str) -> bool:
    """
    Valida se um utilizador com um role/level pode acessar um tipo de território.
    
    Exemplo:
    - admin_provincial pode acessar provinces e municipalities
    - admin_municipal pode acessar municipalities e communes
    """
    role_hierarchy = ROLE_HIERARCHY.get(user_role)
    
    if user_level == AdminLevel.SUPER or user_level == AdminLevel.CENTRAL:
        return True  # Super e Central podem acessar tudo
    
    if user_level == AdminLevel.PROVINCIAL:
        return territory_type in [TerritoryType.PROVINCE, TerritoryType.MUNICIPALITY]
    
    if user_level == AdminLevel.MUNICIPAL:
        return territory_type in [TerritoryType.MUNICIPALITY, TerritoryType.COMMUNE]
    
    if user_level == AdminLevel.COMMUNAL:
        return territory_type == TerritoryType.COMMUNE
    
    return False


# ============================================================================
# 🗺️ CÓDIGOS DE PROVÍNCIAS - Angola (DPA 2024/2025)
# ============================================================================

PROVINCE_CODES = {
    "CAB": "Cabinda",
    "ZAI": "Zaire",
    "UIG": "Uíge",
    "BGO": "Bengo",
    "CNO": "Cuanza-Norte",
    "CSU": "Cuanza-Sul",
    "HUA": "Huambo",
    "BGU": "Benguela",
    "HUI": "Huíla",
    "NAM": "Namibe",
    "CNN": "Cunene",
    "CCU": "Cubango",
    "CND": "Cuando",
    "MOX": "Moxico",
    "MXL": "Moxico Leste",
    "MAL": "Malanje",
    "LNO": "Lunda-Norte",
    "LSU": "Lunda-Sul",
    "BIE": "Bié",
    "ICB": "Icolo e Bengo",
    "LUA": "Luanda",
}

if __name__ == "__main__":
    # Teste rápido
    print("✅ Constantes carregadas com sucesso!")
    print(f"Roles válidos: {VALID_ROLES}")
    print(f"Províncias: {len(PROVINCE_CODES)}")
