"""Cache key constants and templates"""

from string import Template


class CacheKeys:
    """Central registry of cache keys"""
    
    # Taxpayer cache keys
    TAXPAYER_BY_NIF = Template("taxpayer:nif:$nif")
    TAXPAYER_BY_EMAIL = Template("taxpayer:email:$email")
    TAXPAYER_BY_PHONE = Template("taxpayer:phone:$phone")
    TAXPAYER_ID = Template("taxpayer:id:$id")
    TAXPAYER_SEARCH = Template("taxpayer:search:$query")
    TAXPAYER_STATUS = Template("taxpayer:status:$nif")
    TAXPAYER_ALL = "taxpayer:all"
    
    # Declaration cache keys
    DECLARATION_BY_ID = Template("declaration:id:$id")
    DECLARATION_BY_NUMBER = Template("declaration:number:$number")
    DECLARATION_BY_TAXPAYER = Template("declaration:taxpayer:$nif")
    DECLARATION_BY_PERIOD = Template("declaration:period:$tax_type:$year:$month")
    DECLARATION_PENDING = Template("declaration:pending:$year")
    DECLARATION_BY_TAXPAYER_YEAR = Template("declaration:taxpayer:$nif:$year")
    
    # Debt cache keys
    DEBT_BY_ID = Template("debt:id:$id")
    DEBT_BY_NUMBER = Template("debt:number:$number")
    DEBT_BY_TAXPAYER = Template("debt:taxpayer:$nif")
    DEBT_OVERDUE = Template("debt:overdue:$date")
    DEBT_BY_TAXPAYER_STATUS = Template("debt:taxpayer:$nif:$status")
    DEBT_BY_STATUS = Template("debt:status:$status")
    
    # Payment cache keys
    PAYMENT_BY_ID = Template("payment:id:$id")
    PAYMENT_BY_NUMBER = Template("payment:number:$number")
    PAYMENT_BY_REFERENCE = Template("payment:reference:$reference")
    PAYMENT_BY_TAXPAYER = Template("payment:taxpayer:$nif")
    PAYMENT_BY_DEBT = Template("payment:debt:$debt_id")
    PAYMENT_BY_METHOD = Template("payment:method:$method")
    PAYMENT_RECENT = Template("payment:recent:$days")
    
    # Certificate cache keys
    CERTIFICATE_BY_ID = Template("certificate:id:$id")
    CERTIFICATE_BY_NUMBER = Template("certificate:number:$number")
    CERTIFICATE_BY_TAXPAYER = Template("certificate:taxpayer:$nif")
    CERTIFICATE_BY_TYPE = Template("certificate:type:$cert_type")
    CERTIFICATE_VALID = Template("certificate:valid:$date")
    CERTIFICATE_EXPIRED = Template("certificate:expired:$date")
    
    # Audit cache keys
    AUDIT_BY_ENTITY = Template("audit:entity:$entity_type:$entity_id")
    AUDIT_BY_USER = Template("audit:user:$user_id")
    AUDIT_BY_ACTION = Template("audit:action:$action")
    AUDIT_RECENT = "audit:recent"
    
    # AGT Integration cache keys
    AGT_TAXPAYER_DATA = Template("agt:taxpayer:$nif")
    AGT_TAXPAYER_STATUS = Template("agt:status:$nif")
    AGT_DEBTS = Template("agt:debts:$nif")
    AGT_DECLARATIONS = Template("agt:declarations:$nif:$year")
    AGT_PAYMENTS = Template("agt:payments:$nif:$year")
    AGT_HEALTH = "agt:health"
    
    # Rate limiting cache keys
    RATE_LIMIT_ENDPOINT = Template("ratelimit:endpoint:$endpoint")
    RATE_LIMIT_USER = Template("ratelimit:user:$user_id")
    
    # Session cache keys
    SESSION_USER = Template("session:user:$token")
    SESSION_REFRESH = Template("session:refresh:$token")
    
    # Analytics cache keys
    ANALYTICS_TAXPAYER_COUNT = "analytics:taxpayer:count"
    ANALYTICS_DECLARATION_COUNT = Template("analytics:declaration:count:$year")
    ANALYTICS_DEBT_TOTAL = Template("analytics:debt:total:$date")
    ANALYTICS_PAYMENT_TOTAL = Template("analytics:payment:total:$date")
    
    # Prefix definitions for batch operations
    PREFIX_TAXPAYER = "taxpayer:"
    PREFIX_DECLARATION = "declaration:"
    PREFIX_DEBT = "debt:"
    PREFIX_PAYMENT = "payment:"
    PREFIX_CERTIFICATE = "certificate:"
    PREFIX_AUDIT = "audit:"
    PREFIX_AGT = "agt:"
    PREFIX_RATELIMIT = "ratelimit:"
    PREFIX_SESSION = "session:"
    PREFIX_ANALYTICS = "analytics:"
    
    # Default TTL values (in seconds)
    TTL_TAXPAYER = 3600  # 1 hour
    TTL_DECLARATION = 1800  # 30 minutes
    TTL_DEBT = 1800  # 30 minutes
    TTL_PAYMENT = 1800  # 30 minutes
    TTL_CERTIFICATE = 3600  # 1 hour
    TTL_AGT_DATA = 600  # 10 minutes
    TTL_AGT_HEALTH = 60  # 1 minute
    TTL_RATE_LIMIT = 60  # 1 minute
    TTL_SESSION = 86400  # 24 hours
    TTL_ANALYTICS = 3600  # 1 hour
    
    @staticmethod
    def get_taxpayer_key(nif: str) -> str:
        """Get taxpayer cache key"""
        return CacheKeys.TAXPAYER_BY_NIF.substitute(nif=nif)
    
    @staticmethod
    def get_declaration_key(declaration_id: str) -> str:
        """Get declaration cache key"""
        return CacheKeys.DECLARATION_BY_ID.substitute(id=declaration_id)
    
    @staticmethod
    def get_debt_key(debt_id: str) -> str:
        """Get debt cache key"""
        return CacheKeys.DEBT_BY_ID.substitute(id=debt_id)
    
    @staticmethod
    def get_payment_key(payment_id: str) -> str:
        """Get payment cache key"""
        return CacheKeys.PAYMENT_BY_ID.substitute(id=payment_id)
    
    @staticmethod
    def get_certificate_key(certificate_id: str) -> str:
        """Get certificate cache key"""
        return CacheKeys.CERTIFICATE_BY_ID.substitute(id=certificate_id)
    
    @staticmethod
    def get_audit_key(entity_type: str, entity_id: str) -> str:
        """Get audit cache key"""
        return CacheKeys.AUDIT_BY_ENTITY.substitute(entity_type=entity_type, entity_id=entity_id)
    
    @staticmethod
    def invalidate_taxpayer(nif: str) -> list:
        """Get all taxpayer-related keys to invalidate"""
        return [
            CacheKeys.TAXPAYER_BY_NIF.substitute(nif=nif),
            CacheKeys.DECLARATION_BY_TAXPAYER.substitute(nif=nif),
            CacheKeys.DEBT_BY_TAXPAYER.substitute(nif=nif),
            CacheKeys.PAYMENT_BY_TAXPAYER.substitute(nif=nif),
            CacheKeys.CERTIFICATE_BY_TAXPAYER.substitute(nif=nif),
            CacheKeys.AGT_TAXPAYER_DATA.substitute(nif=nif),
        ]
    
    @staticmethod
    def invalidate_declaration(nif: str, year: int) -> list:
        """Get declaration keys to invalidate"""
        return [
            CacheKeys.DECLARATION_BY_TAXPAYER_YEAR.substitute(nif=nif, year=year),
            CacheKeys.DECLARATION_PENDING.substitute(year=year),
        ]
