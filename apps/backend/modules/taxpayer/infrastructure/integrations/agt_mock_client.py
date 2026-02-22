"""AGT Mock Client for Testing"""

from typing import Optional, Dict, Any, List
from datetime import datetime, date, timedelta
import random
import uuid


class AGTMockClient:
    """Mock client for AGT API testing"""
    
    def __init__(self, failure_rate: float = 0.1):
        self.failure_rate = failure_rate
        self._should_fail = lambda: random.random() < self.failure_rate
    
    async def validate_nif(self, nif: str) -> bool:
        """Mock NIF validation"""
        if self._should_fail():
            return False
        return nif and nif[0] in ['1','3','5','7','9']
    
    async def get_taxpayer_data(self, nif: str) -> Optional[Dict[str, Any]]:
        """Mock taxpayer data"""
        if self._should_fail() or not await self.validate_nif(nif):
            return None
        
        return {
            "nif": nif,
            "name": f"Taxpayer {nif[-4:]}",
            "email": f"taxpayer{nif[-4:]}@email.ao",
            "phone": f"+244923{nif[-4:]}",
            "address": f"Street {nif[-4:]}, Luanda",
            "tax_regime": "GENERAL",
            "status": "ACTIVE"
        }
    
    async def get_taxpayer_status(self, nif: str) -> Optional[str]:
        """Mock taxpayer status"""
        if self._should_fail():
            return None
        return "ACTIVE"
    
    async def get_tax_debts(self, nif: str) -> List[Dict[str, Any]]:
        """Mock debts"""
        if self._should_fail():
            return []
        
        debts = []
        for i in range(random.randint(0, 3)):
            amount = random.uniform(10000, 100000)
            days_overdue = random.randint(0, 90)
            debt = {
                "debt_number": f"DEBT-{nif[-4:]}-{i+1}",
                "tax_type": random.choice(["VAT", "IRS", "CIT"]),
                "original_amount": amount,
                "current_amount": amount * (1 + 0.01 * days_overdue/30),
                "created_date": (date.today() - timedelta(days=days_overdue)).isoformat(),
                "due_date": (date.today() - timedelta(days=max(0, days_overdue-30))).isoformat(),
                "status": "PENDING"
            }
            debts.append(debt)
        
        return debts
    
    async def get_declaration_history(self, nif: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Mock declarations"""
        if self._should_fail():
            return []
        
        year = year or date.today().year
        declarations = []
        
        for i in range(random.randint(1, 4)):
            status = random.choice(["PENDING", "APPROVED", "PROCESSING"])
            amount = random.uniform(50000, 500000)
            
            decl = {
                "declaration_number": f"DEC-{year}-{nif[-4:]}-{i+1}",
                "tax_type": random.choice(["VAT", "IRS", "CIT"]),
                "tax_period": f"{year}-{random.randint(1,12):02d}",
                "gross_amount": amount,
                "net_amount": amount * 0.85,
                "status": status,
                "submitted_at": datetime.now().isoformat()
            }
            if status != "PENDING":
                decl["processed_at"] = (datetime.now() + timedelta(days=random.randint(1,10))).isoformat()
            
            declarations.append(decl)
        
        return declarations
    
    async def get_payment_history(self, nif: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Mock payments"""
        if self._should_fail():
            return []
        
        year = year or date.today().year
        payments = []
        
        for i in range(random.randint(0, 5)):
            payment = {
                "payment_number": f"PAY-{year}-{nif[-4:]}-{i+1}",
                "amount": random.uniform(1000, 50000),
                "method": random.choice(["CASH", "TRANSFER", "MOBILE"]),
                "date": (date.today() - timedelta(days=random.randint(1, 365))).isoformat(),
                "status": "COMPLETED"
            }
            payments.append(payment)
        
        return payments
    
    async def submit_declaration(self, nif: str, declaration_data: Dict[str, Any]) -> str:
        """Mock declaration submission"""
        if self._should_fail():
            raise Exception("AGT failure simulated")
        
        return f"PROTOCOL-{uuid.uuid4().hex[:8].upper()}"
    
    async def check_declaration_status(self, protocol: str) -> Dict[str, Any]:
        """Mock status check"""
        if self._should_fail():
            raise Exception("AGT failure simulated")
        
        return {
            "protocol": protocol,
            "status": random.choice(["PROCESSING", "APPROVED", "REJECTED"]),
            "processed_at": datetime.now().isoformat() if random.random() > 0.3 else None
        }
    
    async def request_certificate(self, nif: str, certificate_type: str, year: Optional[int] = None) -> str:
        """Mock certificate request"""
        if self._should_fail():
            raise Exception("AGT failure simulated")
        
        return f"CERT-{uuid.uuid4().hex[:12].upper()}"
    
    async def download_certificate(self, certificate_id: str) -> bytes:
        """Mock certificate download"""
        if self._should_fail():
            raise Exception("AGT failure simulated")
        
        return b"%PDF-1.4 mock certificate content"
    
    async def health_check(self) -> bool:
        """Mock health check"""
        return not self._should_fail()
