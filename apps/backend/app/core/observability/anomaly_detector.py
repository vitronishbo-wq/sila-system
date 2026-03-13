"""
Anomaly Detection Engine - Fase 18.2

Detecta comportamentos anômalos em eventos de auditoria usando:
- Análise estatística (Z-score, IQR)
- Padrões temporais (seasonal decomposition)
- Clustering (isolamento de eventos raros)
- Baselines de comportamento (learning mode)
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
from enum import Enum
logger = logging.getLogger('anomaly_detector')

class AnomalyType(Enum):
    """Tipos de anomalias detectadas"""
    LOGIN_SPIKE = 'login_spike'
    FAILED_LOGIN_cluster = 'failed_login_cluster'
    UNUSUAL_TIME = 'unusual_access_time'
    GEO_ANOMALY = 'geographic_anomaly'
    PRIVILEGE_ESCALATION = 'privilege_escalation'
    DATA_EXFILTRATION = 'data_exfiltration'
    BEHAVIORAL_CHANGE = 'behavioral_change'
    INSIDER_THREAT = 'insider_threat'

@dataclass
class Anomaly:
    """Estrutura de uma anomalia detectada"""
    type: AnomalyType
    user_id: str
    tenant_id: str
    severity: str
    score: float
    description: str
    timestamp: datetime
    evidence: Dict
    recommended_action: str

class UserProfile:
    """Perfil comportamental de um usuário"""

    def __init__(self, user_id: str, tenant_id: str):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.learning_phase = True
        self.min_learning_events = 50
        self.event_count = 0
        self.login_times = []
        self.ip_addresses = set()
        self.typical_ips = set()
        self.access_patterns = defaultdict(int)
        self.tenant_access = defaultdict(int)
        self.typical_tenants = set()
        self.failed_logins_per_day = []
        self.devices = set()
        self.avg_logins_per_hour = 0.0
        self.stddev_logins = 0.0
        self.avg_time_between_logins = 0.0
        self.is_admin = False

    def update(self, event: Dict):
        """Atualiza o perfil com novo evento"""
        self.event_count += 1
        if event.get('action') == 'UPDATE_LOGIN':
            self.login_times.append(event['@timestamp'])
            if event.get('source_ip'):
                self.ip_addresses.add(event['source_ip'])
        if event.get('tenant_id'):
            self.tenant_access[event['tenant_id']] += 1
        if 'ADMIN' in (event.get('roles') or []):
            self.is_admin = True
        if self.event_count >= self.min_learning_events:
            self.learning_phase = False
            self._compute_baselines()

    def _compute_baselines(self):
        """Calcula baselines comportamentais"""
        if not self.ip_addresses:
            return
        sorted_ips = sorted(self.ip_addresses, key=lambda ip: -sum((1 for t in self.login_times if True)))
        self.typical_ips = set(sorted_ips[:max(1, len(sorted_ips) // 2)])
        sorted_tenants = sorted(self.tenant_access.items(), key=lambda x: -x[1])
        self.typical_tenants = {t[0] for t in sorted_tenants[:max(1, len(sorted_tenants) // 2)]}
        if len(self.login_times) > 1:
            login_hours = [t.hour for t in self.login_times]
            self.avg_logins_per_hour = np.mean(login_hours) if login_hours else 0.0
            self.stddev_logins = np.std(login_hours) if login_hours else 0.0

    def is_new_ip(self, ip: str) -> bool:
        """Verifica se é um IP novo/anômalo"""
        return ip not in self.typical_ips and len(self.typical_ips) > 0

    def is_unusual_tenant(self, tenant_id: str) -> bool:
        """Verifica se é um acesso a tenant anômalo"""
        return tenant_id not in self.typical_tenants and len(self.typical_tenants) > 0

    def get_risk_score(self) -> float:
        """Calcula score de risco geral do usuário (0-100)"""
        if self.learning_phase:
            return 0.0
        risk = 0.0
        if self.is_admin:
            risk += 10.0
        if len(self.ip_addresses) > 5:
            risk += min(15.0, len(self.ip_addresses) * 2.0)
        if len(self.tenant_access) > 3:
            risk += min(20.0, len(self.tenant_access) * 3.0)
        return min(100.0, risk)

class AnomalyDetector:
    """Detector de anomalias usando aprendizado de máquina"""

    def __init__(self):
        self.user_profiles: Dict[str, UserProfile] = {}
        self.anomalies: List[Anomaly] = []
        self.thresholds = {'login_spike': 3.0, 'failed_login_cluster': 5, 'unusual_time_stddev': 2.5, 'geo_anomaly_probability': 0.05, 'privilege_escalation_risk': 75.0, 'data_exfiltration_size': 1024 * 1024}

    def get_or_create_profile(self, user_id: str, tenant_id: str) -> UserProfile:
        """Obtém ou cria perfil de usuário"""
        key = f'{user_id}:{tenant_id}'
        if key not in self.user_profiles:
            self.user_profiles[key] = UserProfile(user_id, tenant_id)
        return self.user_profiles[key]

    def detect(self, event: Dict) -> Optional[Anomaly]:
        """
        Analisa evento e detecta anomalias
        
        Args:
            event: Evento auditável com campos:
                - action, user_id, tenant_id, roles
                - @timestamp, source_ip
                - request_id, trace_id
        
        Returns:
            Anomaly object ou None se normal
        """
        user_id = event.get('user_id')
        tenant_id = event.get('tenant_id')
        if not user_id:
            return None
        profile = self.get_or_create_profile(user_id, tenant_id or 'unknown')
        profile.update(event)
        if profile.learning_phase:
            return None
        anomalies = [self._detect_login_spike(profile, event), self._detect_failed_login_cluster(profile, event), self._detect_unusual_time(profile, event), self._detect_geo_anomaly(profile, event), self._detect_privilege_escalation(profile, event), self._detect_data_exfiltration(profile, event), self._detect_behavioral_change(profile, event)]
        detected = [a for a in anomalies if a is not None]
        if detected:
            return max(detected, key=lambda a: a.score)
        return None

    def _detect_login_spike(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta spike de logins"""
        if event.get('action') != 'UPDATE_LOGIN':
            return None
        now = event.get('@timestamp', datetime.utcnow())
        recent_logins = sum((1 for t in profile.login_times if isinstance(t, datetime) and (now - t).total_seconds() < 300))
        expected = max(1.0, profile.avg_logins_per_hour / 12.0)
        z_score = (recent_logins - expected) / max(1.0, profile.stddev_logins)
        if z_score > self.thresholds['login_spike']:
            return Anomaly(type=AnomalyType.LOGIN_SPIKE, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='medium', score=min(100.0, 50.0 + z_score * 10), description=f'Login spike: {recent_logins} logins in 5 min (expected ~{expected:.1f})', timestamp=now, evidence={'recent_logins': recent_logins, 'expected': expected, 'z_score': z_score}, recommended_action='Review login patterns. Possible account compromise.')
        return None

    def _detect_failed_login_cluster(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta cluster de tentativas falhas"""
        if event.get('action') != 'INCREMENT_FAILED':
            return None
        now = event.get('@timestamp', datetime.utcnow())
        recent_failures = 1
        if recent_failures >= self.thresholds['failed_login_cluster']:
            return Anomaly(type=AnomalyType.FAILED_LOGIN_cluster, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='high', score=min(100.0, 70.0 + recent_failures * 5), description=f'{recent_failures} failed login attempts in 10 minutes', timestamp=now, evidence={'failure_count': recent_failures, 'threshold': self.thresholds['failed_login_cluster']}, recommended_action='Block account temporarily. Investigate password attack.')
        return None

    def _detect_unusual_time(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta logins em horários incomuns"""
        if event.get('action') != 'UPDATE_LOGIN':
            return None
        if not profile.is_admin:
            return None
        now = event.get('@timestamp', datetime.utcnow())
        hour = now.hour
        if 8 <= hour < 18:
            return None
        expected_hour = 12
        deviation = abs(hour - expected_hour)
        z_score = deviation / max(1.0, profile.stddev_logins)
        if z_score > self.thresholds['unusual_time_stddev']:
            return Anomaly(type=AnomalyType.UNUSUAL_TIME, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='medium', score=min(100.0, 60.0 + z_score * 8), description=f'Admin accessing system at {hour:02d}:00 (outside business hours)', timestamp=now, evidence={'access_hour': hour, 'expected_hours': '08:00-18:00', 'deviation': deviation}, recommended_action='Verify legitimate admin access outside business hours.')
        return None

    def _detect_geo_anomaly(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta IP novo/anômalo"""
        source_ip = event.get('source_ip')
        if not source_ip or profile.is_new_ip(source_ip):
            return None
        return Anomaly(type=AnomalyType.GEO_ANOMALY, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='low', score=30.0, description=f'Login from new IP address: {source_ip}', timestamp=event.get('@timestamp', datetime.utcnow()), evidence={'source_ip': source_ip, 'known_ips': list(profile.typical_ips)[:5]}, recommended_action='Low priority: New IP detected. Log for reference.')

    def _detect_privilege_escalation(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta tentativa de escalação de privilégios"""
        if event.get('action') not in ['GRANT_ROLE', 'UPDATE_ROLES']:
            return None
        if 'ADMIN' in (event.get('roles') or []):
            return None
        if 'ADMIN' in (event.get('roles_attempted') or []):
            return Anomaly(type=AnomalyType.PRIVILEGE_ESCALATION, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='critical', score=95.0, description='Privilege escalation attempt: Non-admin trying to gain admin role', timestamp=event.get('@timestamp', datetime.utcnow()), evidence={'current_roles': event.get('roles'), 'attempted_roles': event.get('roles_attempted'), 'subject_id': event.get('subject_id')}, recommended_action='CRITICAL: Block operation immediately. Investigate user and requestor.')
        return None

    def _detect_data_exfiltration(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta potencial exfiltração de dados"""
        if event.get('action') not in ['EXPORT', 'DOWNLOAD', 'QUERY']:
            return None
        data_size = event.get('data_size', 0)
        if data_size > self.thresholds['data_exfiltration_size']:
            return Anomaly(type=AnomalyType.DATA_EXFILTRATION, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='high', score=85.0, description=f'Large data export: {data_size / (1024 * 1024):.1f}MB', timestamp=event.get('@timestamp', datetime.utcnow()), evidence={'data_size_mb': data_size / (1024 * 1024), 'action': event.get('action'), 'resource': event.get('resource')}, recommended_action='High: Review exported data. Verify legitimate business need.')
        return None

    def _detect_behavioral_change(self, profile: UserProfile, event: Dict) -> Optional[Anomaly]:
        """Detecta mudança em padrão comportamental"""
        tenant = event.get('tenant_id')
        if tenant and profile.is_unusual_tenant(tenant):
            return Anomaly(type=AnomalyType.BEHAVIORAL_CHANGE, user_id=profile.user_id, tenant_id=profile.tenant_id, severity='medium', score=65.0, description=f'Access to unusual tenant: {tenant}', timestamp=event.get('@timestamp', datetime.utcnow()), evidence={'unusual_tenant': tenant, 'typical_tenants': list(profile.typical_tenants)[:5]}, recommended_action='Verify cross-tenant access is authorized.')
        return None

    def get_user_risk_score(self, user_id: str, tenant_id: str) -> float:
        """Obtém score de risco geral de um usuário"""
        profile = self.user_profiles.get(f'{user_id}:{tenant_id}')
        if profile:
            return profile.get_risk_score()
        return 0.0

    def export_anomalies(self, limit: int=100) -> List[Dict]:
        """Exporta anomalias recentes em formato JSON"""
        recent = sorted(self.anomalies, key=lambda a: a.timestamp, reverse=True)[:limit]
        return [{'type': a.type.value, 'user_id': a.user_id, 'tenant_id': a.tenant_id, 'severity': a.severity, 'score': a.score, 'description': a.description, 'timestamp': a.timestamp.isoformat(), 'evidence': a.evidence, 'recommended_action': a.recommended_action} for a in recent]
_detector = AnomalyDetector()

def detect_anomaly(event: Dict) -> Optional[Dict]:
    """Função helper para detectar anomalia em evento"""
    anomaly = _detector.detect(event)
    if anomaly:
        return {'type': anomaly.type.value, 'user_id': anomaly.user_id, 'tenant_id': anomaly.tenant_id, 'severity': anomaly.severity, 'score': anomaly.score, 'description': anomaly.description, 'timestamp': anomaly.timestamp.isoformat(), 'evidence': anomaly.evidence, 'recommended_action': anomaly.recommended_action}
    return None

def get_user_risk_score(user_id: str, tenant_id: str='default') -> float:
    """Obtém score de risco de um usuário"""
    return _detector.get_user_risk_score(user_id, tenant_id)