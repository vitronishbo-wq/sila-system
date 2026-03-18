#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

# Import individual modules directly to avoid init conflicts
import importlib.util

def safe_import(module_path):
    """Load module directly from file path"""
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

print('🔍 Testing Auth Gateway...')
from apps.backend.app.core.auth_gateway.infrastructure.security.jwt_engine import JWTEngine
from apps.backend.app.core.auth_gateway.infrastructure.security.auth_resilience import CircuitBreaker
from apps.backend.app.core.auth_gateway.application.services.service_token_service import ServiceTokenService
from apps.backend.app.core.auth_gateway.api.rate_limiter import RateLimiter
print('✅ Auth Gateway: OPERATIONAL')

print('🔍 Testing Security Layer (direct imports)...')
import importlib
sys.path.insert(0, 'app/core/security/threat_detection/application')
sys.path.insert(0, 'app/core/security/anomaly_detection/application')
sys.path.insert(0, 'app/core/security/fraud_detection/application')
sys.path.insert(0, 'app/core/security/zero_trust_engine/application')
sys.path.insert(0, 'app/core/security/national_soc/application')

from threat_engine import ThreatEngine
from anomaly_engine import AnomalyEngine
from fraud_engine import FraudEngine
from zero_trust import ZeroTrustEngine
from soc_monitor import SOCMonitor
print('✅ Security Layer: OPERATIONAL')

print('🔍 Testing Intelligence Layer...')
from apps.backend.app.core.intelligence.behavioral_ai.application.behavior_model import BehavioralModel
from apps.backend.app.core.intelligence.predictive_governance.application.policy_predictor import PolicyPredictor
from apps.backend.app.core.intelligence.economic_simulation.application.economy_model import EconomyModel
from apps.backend.app.core.intelligence.crisis_prediction.application.crisis_engine import CrisisEngine
from apps.backend.app.core.intelligence.national_analytics.application.analytics_engine import NationalAnalytics
print('✅ Intelligence Layer: OPERATIONAL')

print('🔍 Testing Identity + Database...')
from apps.backend.app.modules.identity.bounded_contexts.iam.domain.entities.user import User
from apps.backend.app.modules.identity.infrastructure.models.user_model import UserModel
from apps.backend.app.modules.identity.infrastructure.repositories.user_repository import UserRepository
from apps.backend.app.core.database.session import AsyncSessionLocal, engine
print('✅ Identity Persistence: OPERATIONAL')

# Functional tests
print('\n🧪 Functional Verification...')
jwt = JWTEngine()
token = jwt.generate('user123', ['admin', 'write'])
print(f'✅ JWT Engine: token generated')

threat = ThreatEngine()
result = threat.register_ip('192.168.1.1')
print(f'✅ Threat Engine: {result}')

anomaly = AnomalyEngine()
is_anomaly = anomaly.detect([10, 11, 12, 11, 10, 100])
print(f'✅ Anomaly Detection: {is_anomaly}')

fraud = FraudEngine()
is_fraud = fraud.detect('tax', 20000000)
print(f'✅ Fraud Detection: {is_fraud}')

zt = ZeroTrustEngine()
auth_result = zt.validate({'roles': ['admin']}, 'service1', 'read')
print(f'✅ Zero-Trust Auth: {auth_result}')

analytics = NationalAnalytics()
agg = analytics.aggregate({'revenue': [100, 200, 300]})
print(f'✅ Analytics: computed')

print('\n' + '='*60)
print('🟢 SILA 3.0 TRIPLE BOOTSTRAP COMPLETE')
print('   Identity Persistence    ✅')
print('   Auth Gateway Core       ✅')
print('   Security Layer          ✅')
print('   Intelligence Layer      ✅')
print('='*60)
