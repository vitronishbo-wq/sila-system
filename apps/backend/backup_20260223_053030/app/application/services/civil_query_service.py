from typing import List, Dict, Any, Optional
from datetime import date
from sqlalchemy.orm import Session

from ...domain.models.birth_record import BirthRecord
from ...domain.models.death_record import DeathRecord
from ...domain.models.marriage_record import MarriageRecord
from ...domain.models.certificate_record import CertificateRecord
from ...domain.enums import CivilEventType
from .base_service import BaseService


class CivilQueryService(BaseService):
    """Serviço para consultas integradas do registo civil"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def get_citizen_lifecycle(self, citizen_id: str) -> Dict[str, Any]:
        """Obtém o ciclo de vida completo de um cidadão"""
        result = {
            "citizen_id": citizen_id,
            "birth": None,
            "marriages": [],
            "current_marriage": None,
            "death": None,
            "certificates": []
        }
        
        # 1. Buscar nascimento
        births = self.event_repo.get_by_citizen_id(citizen_id, CivilEventType.BIRTH)
        if births:
            result["birth"] = births[0].to_dict()
        
        # 2. Buscar casamentos
        marriages = self.event_repo.get_by_citizen_id(citizen_id, CivilEventType.MARRIAGE)
        result["marriages"] = [m.to_dict() for m in marriages]
        
        # 3. Identificar casamento atual
        current_marriages = [m for m in marriages if hasattr(m, 'status')]
        if current_marriages:
            result["current_marriage"] = current_marriages[0].to_dict()
        
        # 4. Buscar óbito
        deaths = self.event_repo.get_by_citizen_id(citizen_id, CivilEventType.DEATH)
        if deaths:
            result["death"] = deaths[0].to_dict()
        
        # 5. Buscar certificados
        certificates = self.certificate_repo.get_by_citizen_id(citizen_id)
        result["certificates"] = [c.to_dict() for c in certificates]
        
        return result
    
    def search_events(self, query: str, event_type: Optional[CivilEventType] = None,
                     start_date: Optional[date] = None, end_date: Optional[date] = None,
                     limit: int = 50) -> List[Dict[str, Any]]:
        """Pesquisa eventos por texto livre (nome, número, etc.)"""
        results = []
        
        # Busca simples por período
        if start_date and end_date:
            events = self.event_repo.get_by_date_range(start_date, end_date, event_type)
            results = [e.to_dict() for e in events[:limit]]
        
        return results
    
    def get_statistics(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Obtém estatísticas do período"""
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "births": {
                "total": self.event_repo.count_by_period(start_date, end_date, CivilEventType.BIRTH),
                "late_registrations": 0
            },
            "deaths": {
                "total": self.event_repo.count_by_period(start_date, end_date, CivilEventType.DEATH)
            },
            "marriages": {
                "total": self.event_repo.count_by_period(start_date, end_date, CivilEventType.MARRIAGE)
            },
            "certificates": {
                "issued": len(self.certificate_repo.get_by_date_range(start_date, end_date))
            }
        }
    
    def verify_document_authenticity(self, document_number: str, 
                                     verification_code: str) -> Dict[str, Any]:
        """Verifica autenticidade de um documento (certificado)"""
        from .certificate_service import CertificateService
        cert_service = CertificateService(self.db)
        return cert_service.verify_certificate(document_number, verification_code)
    
    def get_citizen_family_tree(self, citizen_id: str, depth: int = 2) -> Dict[str, Any]:
        """Constrói árvore genealógica básica"""
        # Implementação simplificada
        result = {
            "citizen_id": citizen_id,
            "birth_info": None,
            "parents": [],
            "children": [],
            "spouse": None
        }
        
        # Buscar nascimento para dados dos pais
        births = self.event_repo.get_by_citizen_id(citizen_id, CivilEventType.BIRTH)
        if births and isinstance(births[0], BirthRecord):
            birth = births[0]
            result["birth_info"] = {
                "birth_date": birth.child_birth_date.isoformat() if birth.child_birth_date else None,
                "mother_id": birth.mother_id,
                "mother_name": birth.mother_name,
                "father_id": birth.father_id,
                "father_name": birth.father_name
            }
        
        # Buscar filhos
        children = self.event_repo.get_birth_by_mother(citizen_id)
        result["children"] = [
            {
                "id": c.mother_id if hasattr(c, 'mother_id') else None,
                "name": c.child_first_names + " " + c.child_last_names if hasattr(c, 'child_first_names') else "",
                "birth_date": c.child_birth_date.isoformat() if hasattr(c, 'child_birth_date') else None
            }
            for c in children
        ]
        
        # Buscar cônjuges
        marriages = self.event_repo.get_marriage_by_spouse(citizen_id)
        if marriages and isinstance(marriages[0], MarriageRecord):
            marriage = marriages[0]
            result["spouse"] = {
                "id": marriage.spouse2_id if marriage.spouse1_id == citizen_id else marriage.spouse1_id,
                "name": marriage.spouse2_name if marriage.spouse1_id == citizen_id else marriage.spouse1_name,
                "marriage_date": marriage.marriage_date.isoformat() if marriage.marriage_date else None
            }
        
        return result
