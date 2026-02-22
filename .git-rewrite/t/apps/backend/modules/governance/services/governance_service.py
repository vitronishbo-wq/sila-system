"""
Serviço principal de governança - SILA System
Fase 2: Módulos Importantes - Lógica de Negócio Real

Implementa regras complexas de governança:
- Gestão de mandatos e elegibilidade
- Processo de tomada de decisões
- Auditoria e compliance
- Gestão de riscos institucionais
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.auditoria_log import AuditoriaLog
from ..models.council_meeting import CouncilMeeting
from ..models.decision import Decision
from ..models.gestao_risco import GestaoRisco
from ..models.institution import Institution
from ..models.mandate import Mandate
from ..schemas.council_meeting import CouncilMeetingCreate
from ..schemas.decision import DecisionCreate
from ..schemas.institution import InstitutionCreate
from ..schemas.mandate import MandateCreate

logger = logging.getLogger(__name__)


class GovernanceService:
    """Serviço principal para operações de governança"""

    def __init__(self, db: AsyncSession):
        self.db = db

        # Regras de negócio para governança
        self.governance_rules = {
            "mandate_duration": 4,  # 4 anos
            "max_consecutive_mandates": 2,  # Máximo 2 mandatos consecutivos
            "min_decision_quorum": 0.5,  # 50% para decisões simples
            "critical_decision_quorum": 0.67,  # 67% para decisões críticas
            "audit_retention_years": 7,  # Manter auditoria por 7 anos
            "risk_assessment_frequency": 90,  # Avaliação de risco a cada 90 dias
        }

    # ========================================
    # GESTÃO DE INSTITUIÇÕES
    # ========================================

    async def create_institution(
        self, institution_data: InstitutionCreate
    ) -> Institution:
        """Cria nova instituição com validações de hierarquia"""

        # Validar hierarquia se instituição pai foi especificada
        if institution_data.parent_institution_id:
            await self._validate_institution_hierarchy(
                institution_data.parent_institution_id
            )

        # Verificar se já existe instituição com mesmo nome no mesmo nível
        existing = await self._check_institution_name_conflict(
            institution_data.name, institution_data.parent_institution_id
        )

        if existing:
            raise ValueError(
                f"Já existe instituição com nome '{institution_data.name}' neste nível"
            )

        # Criar instituição
        institution = Institution(
            name=institution_data.name,
            description=institution_data.description,
            institution_type=institution_data.institution_type,
            parent_institution_id=institution_data.parent_institution_id,
            status="active",
            created_at=datetime.utcnow(),
        )

        self.db.add(institution)
        await self.db.commit()
        await self.db.refresh(institution)

        # Registrar auditoria
        await self._log_audit_action(
            action="create_institution",
            entity_type="institution",
            entity_id=institution.id,
            details={
                "name": institution_data.name,
                "type": institution_data.institution_type,
            },
        )

        logger.info(f"Instituição criada: {institution_data.name}")

        return institution

    async def get_institution_hierarchy(self) -> Dict[str, Any]:
        """Obtém hierarquia completa de instituições"""

        # Buscar todas as instituições
        result = await self.db.execute(
            select(Institution)
            .where(Institution.status == "active")
            .order_by(Institution.parent_institution_id, Institution.name)
        )
        institutions = result.scalars().all()

        # Construir árvore hierárquica
        hierarchy = self._build_institution_tree(institutions)

        return {
            "hierarchy": hierarchy,
            "total_institutions": len(institutions),
            "levels": self._count_hierarchy_levels(hierarchy),
        }

    # ========================================
    # GESTÃO DE MANDATOS
    # ========================================

    async def create_mandate(
        self, mandate_data: MandateCreate, user_id: int
    ) -> Mandate:
        """Cria novo mandato com validações de elegibilidade"""

        # Verificar elegibilidade do candidato
        eligibility = await self.check_candidate_eligibility(
            user_id, mandate_data.institution_id
        )

        if not eligibility["eligible"]:
            raise ValueError(f"Candidato não elegível: {eligibility['reason']}")

        # Verificar se não há conflito de mandatos
        await self._check_mandate_conflicts(
            user_id, mandate_data.start_date, mandate_data.end_date
        )

        # Criar mandato
        mandate = Mandate(
            user_id=user_id,
            institution_id=mandate_data.institution_id,
            position=mandate_data.position,
            start_date=mandate_data.start_date,
            end_date=mandate_data.end_date,
            status="active",
            created_at=datetime.utcnow(),
        )

        self.db.add(mandate)
        await self.db.commit()
        await self.db.refresh(mandate)

        # Registrar auditoria
        await self._log_audit_action(
            action="create_mandate",
            entity_type="mandate",
            entity_id=mandate.id,
            details={"user_id": user_id, "position": mandate_data.position},
        )

        logger.info(f"Mandato criado: {mandate_data.position} para usuário {user_id}")

        return mandate

    async def check_candidate_eligibility(
        self, user_id: int, institution_id: int
    ) -> Dict[str, Any]:
        """Verifica elegibilidade de candidato para mandato"""

        # Buscar mandatos anteriores
        result = await self.db.execute(
            select(Mandate)
            .where(
                and_(
                    Mandate.user_id == user_id,
                    Mandate.institution_id == institution_id,
                    Mandate.status.in_(["completed", "active"]),
                )
            )
            .order_by(desc(Mandate.end_date))
        )
        previous_mandates = result.scalars().all()

        # Verificar limite de mandatos consecutivos
        consecutive_count = 0
        current_date = datetime.utcnow()

        for mandate in previous_mandates:
            if mandate.end_date and (current_date - mandate.end_date).days <= 365:
                consecutive_count += 1
            else:
                break

        # Regras de elegibilidade
        if consecutive_count >= self.governance_rules["max_consecutive_mandates"]:
            return {
                "eligible": False,
                "reason": f'Limite de {self.governance_rules["max_consecutive_mandates"]} mandatos consecutivos atingido',
            }

        # Verificar se candidato tem mandato ativo em outra instituição
        active_result = await self.db.execute(
            select(Mandate).where(
                and_(
                    Mandate.user_id == user_id,
                    Mandate.status == "active",
                    Mandate.institution_id != institution_id,
                )
            )
        )
        active_mandate = active_result.scalar_one_or_none()

        if active_mandate:
            return {
                "eligible": False,
                "reason": "Candidato já possui mandato ativo em outra instituição",
            }

        # Verificar idade mínima (regra de negócio)
        # Em produção, buscar idade do usuário
        min_age = 21
        user_age = 25  # Mock - em produção buscar do sistema de usuários

        if user_age < min_age:
            return {
                "eligible": False,
                "reason": f"Idade mínima não atingida ({min_age} anos)",
            }

        return {
            "eligible": True,
            "reason": "Candidato elegível",
            "consecutive_mandates": consecutive_count,
            "previous_mandates": len(previous_mandates),
        }

    # ========================================
    # GESTÃO DE DECISÕES
    # ========================================

    async def create_decision(
        self, decision_data: DecisionCreate, user_id: int
    ) -> Decision:
        """Cria nova decisão com validações de autoridade"""

        # Verificar se usuário tem autoridade para tomar esta decisão
        authority = await self._check_decision_authority(
            user_id, decision_data.decision_type
        )

        if not authority["authorized"]:
            raise ValueError(f"Usuário não tem autoridade: {authority['reason']}")

        # Determinar nível de aprovação necessário
        approval_level = self._determine_approval_level(
            decision_data.decision_type, decision_data.impact_level
        )

        # Criar decisão
        decision = Decision(
            title=decision_data.title,
            description=decision_data.description,
            decision_type=decision_data.decision_type,
            impact_level=decision_data.impact_level,
            proposed_by=user_id,
            institution_id=decision_data.institution_id,
            approval_level=approval_level,
            status="pending",
            created_at=datetime.utcnow(),
        )

        self.db.add(decision)
        await self.db.commit()
        await self.db.refresh(decision)

        # Registrar auditoria
        await self._log_audit_action(
            action="create_decision",
            entity_type="decision",
            entity_id=decision.id,
            details={
                "type": decision_data.decision_type,
                "impact": decision_data.impact_level,
            },
        )

        logger.info(f"Decisão criada: {decision_data.title}")

        return decision

    async def approve_decision(
        self, decision_id: int, user_id: int, approval_data: Dict[str, Any]
    ) -> Decision:
        """Aprova decisão com validações de quorum"""

        # Buscar decisão
        result = await self.db.execute(
            select(Decision).where(Decision.id == decision_id)
        )
        decision = result.scalar_one_or_none()

        if not decision:
            raise ValueError("Decisão não encontrada")

        if decision.status != "pending":
            raise ValueError("Decisão não está pendente de aprovação")

        # Verificar se usuário pode aprovar esta decisão
        can_approve = await self._check_approval_authority(
            user_id, decision.approval_level
        )

        if not can_approve:
            raise ValueError("Usuário não tem autoridade para aprovar esta decisão")

        # Registrar aprovação
        approvals = json.loads(decision.approvals or "[]")
        approvals.append(
            {
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "comments": approval_data.get("comments", ""),
                "vote": approval_data.get("vote", "approve"),
            }
        )
        decision.approvals = json.dumps(approvals)

        # Verificar se atingiu quorum necessário
        quorum_met = await self._check_decision_quorum(decision)

        if quorum_met:
            decision.status = "approved"
            decision.approved_at = datetime.utcnow()

            # Aplicar decisão se necessário
            await self._apply_decision(decision)

            logger.info(f"Decisão aprovada: {decision.title}")

        await self.db.commit()

        # Registrar auditoria
        await self._log_audit_action(
            action="approve_decision",
            entity_type="decision",
            entity_id=decision.id,
            details={"user_id": user_id, "status": decision.status},
        )

        return decision

    # ========================================
    # GESTÃO DE REUNIÕES DO CONSELHO
    # ========================================

    async def create_council_meeting(
        self, meeting_data: CouncilMeetingCreate
    ) -> CouncilMeeting:
        """Cria reunião do conselho com validações de agenda"""

        # Validar data da reunião (não pode ser no passado)
        if meeting_data.scheduled_date < datetime.utcnow():
            raise ValueError("Reunião não pode ser agendada para o passado")

        # Verificar conflitos de agenda
        conflicts = await self._check_meeting_conflicts(meeting_data.scheduled_date)

        if conflicts:
            raise ValueError(f"Conflito de agenda: {conflicts}")

        # Validar quorum mínimo
        required_attendees = await self._calculate_required_attendees(
            meeting_data.meeting_type
        )

        if len(meeting_data.invited_members) < required_attendees:
            raise ValueError(
                f"Quorum mínimo não atingido. Necessário: {required_attendees}"
            )

        # Criar reunião
        meeting = CouncilMeeting(
            title=meeting_data.title,
            description=meeting_data.description,
            meeting_type=meeting_data.meeting_type,
            scheduled_date=meeting_data.scheduled_date,
            location=meeting_data.location,
            agenda_items=json.dumps(meeting_data.agenda_items),
            invited_members=json.dumps(meeting_data.invited_members),
            status="scheduled",
            created_at=datetime.utcnow(),
        )

        self.db.add(meeting)
        await self.db.commit()
        await self.db.refresh(meeting)

        # Enviar convites (mock)
        await self._send_meeting_invitations(meeting)

        logger.info(f"Reunião criada: {meeting_data.title}")

        return meeting

    # ========================================
    # GESTÃO DE RISCOS
    # ========================================

    async def assess_institutional_risks(self, institution_id: int) -> Dict[str, Any]:
        """Avalia riscos institucionais baseado em métricas"""

        # Buscar dados históricos para análise
        risk_factors = await self._collect_risk_factors(institution_id)

        # Calcular score de risco
        risk_score = self._calculate_risk_score(risk_factors)

        # Determinar nível de risco
        risk_level = self._determine_risk_level(risk_score)

        # Gerar recomendações
        recommendations = self._generate_risk_recommendations(risk_factors, risk_level)

        # Salvar avaliação
        risk_assessment = GestaoRisco(
            institution_id=institution_id,
            risk_score=risk_score,
            risk_level=risk_level,
            assessment_date=datetime.utcnow(),
            factors=json.dumps(risk_factors),
            recommendations=json.dumps(recommendations),
            status="active",
        )

        self.db.add(risk_assessment)
        await self.db.commit()

        return {
            "institution_id": institution_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": risk_factors,
            "recommendations": recommendations,
            "assessment_date": risk_assessment.assessment_date,
        }

    # ========================================
    # MÉTODOS AUXILIARES PRIVADOS
    # ========================================

    async def _validate_institution_hierarchy(self, parent_id: int) -> bool:
        """Valida hierarquia de instituições"""

        result = await self.db.execute(
            select(Institution).where(Institution.id == parent_id)
        )
        parent = result.scalar_one_or_none()

        if not parent:
            raise ValueError("Instituição pai não encontrada")

        if parent.status != "active":
            raise ValueError("Instituição pai não está ativa")

        return True

    async def _check_institution_name_conflict(
        self, name: str, parent_id: Optional[int]
    ) -> bool:
        """Verifica conflito de nomes de instituições"""

        query = select(Institution).where(Institution.name == name)

        if parent_id:
            query = query.where(Institution.parent_institution_id == parent_id)
        else:
            query = query.where(Institution.parent_institution_id.is_(None))

        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()

        return existing is not None

    def _build_institution_tree(
        self, institutions: List[Institution]
    ) -> List[Dict[str, Any]]:
        """Constrói árvore hierárquica de instituições"""

        # Criar mapa de instituições por ID
        institution_map = {inst.id: inst for inst in institutions}

        # Encontrar raízes (instituições sem pai)
        roots = [inst for inst in institutions if inst.parent_institution_id is None]

        def build_subtree(institution: Institution) -> Dict[str, Any]:
            children = [
                build_subtree(child)
                for child in institutions
                if child.parent_institution_id == institution.id
            ]

            return {
                "id": institution.id,
                "name": institution.name,
                "type": institution.institution_type,
                "children": children,
            }

        return [build_subtree(root) for root in roots]

    def _count_hierarchy_levels(self, hierarchy: List[Dict[str, Any]]) -> int:
        """Conta níveis da hierarquia"""

        def max_depth(node: Dict[str, Any]) -> int:
            if not node["children"]:
                return 1
            return 1 + max(max_depth(child) for child in node["children"])

        return max(max_depth(node) for node in hierarchy) if hierarchy else 0

    async def _check_mandate_conflicts(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> None:
        """Verifica conflitos de mandatos"""

        result = await self.db.execute(
            select(Mandate).where(
                and_(
                    Mandate.user_id == user_id,
                    Mandate.status == "active",
                    or_(
                        and_(
                            Mandate.start_date <= start_date,
                            Mandate.end_date >= start_date,
                        ),
                        and_(
                            Mandate.start_date <= end_date, Mandate.end_date >= end_date
                        ),
                        and_(
                            Mandate.start_date >= start_date,
                            Mandate.end_date <= end_date,
                        ),
                    ),
                )
            )
        )

        conflicts = result.scalars().all()

        if conflicts:
            raise ValueError("Conflito de datas com mandatos existentes")

    async def _check_decision_authority(
        self, user_id: int, decision_type: str
    ) -> Dict[str, Any]:
        """Verifica autoridade para tomar decisão"""

        # Buscar mandato ativo do usuário
        result = await self.db.execute(
            select(Mandate).where(
                and_(Mandate.user_id == user_id, Mandate.status == "active")
            )
        )
        mandate = result.scalar_one_or_none()

        if not mandate:
            return {"authorized": False, "reason": "Usuário não possui mandato ativo"}

        # Verificar se posição permite este tipo de decisão
        authority_levels = {
            "administrative": ["mayor", "secretary", "director"],
            "legislative": ["councilor", "mayor"],
            "executive": ["mayor", "secretary"],
            "financial": ["mayor", "treasurer", "financial_director"],
        }

        if decision_type not in authority_levels:
            return {"authorized": False, "reason": "Tipo de decisão não reconhecido"}

        if mandate.position not in authority_levels[decision_type]:
            return {
                "authorized": False,
                "reason": f"Posição {mandate.position} não tem autoridade para {decision_type}",
            }

        return {"authorized": True, "reason": "Usuário autorizado", "mandate": mandate}

    def _determine_approval_level(self, decision_type: str, impact_level: str) -> str:
        """Determina nível de aprovação necessário"""

        if impact_level == "critical":
            return "council_approval"
        elif impact_level == "high":
            return "executive_approval"
        elif decision_type in ["financial", "budget"]:
            return "financial_committee"
        else:
            return "department_approval"

    async def _check_approval_authority(
        self, user_id: int, approval_level: str
    ) -> bool:
        """Verifica se usuário pode aprovar neste nível"""

        # Buscar mandato ativo
        result = await self.db.execute(
            select(Mandate).where(
                and_(Mandate.user_id == user_id, Mandate.status == "active")
            )
        )
        mandate = result.scalar_one_or_none()

        if not mandate:
            return False

        # Mapear níveis de aprovação para posições
        approval_authorities = {
            "department_approval": ["director", "secretary", "mayor"],
            "executive_approval": ["secretary", "mayor"],
            "financial_committee": ["treasurer", "financial_director", "mayor"],
            "council_approval": ["councilor", "mayor"],
        }

        return mandate.position in approval_authorities.get(approval_level, [])

    async def _check_decision_quorum(self, decision: Decision) -> bool:
        """Verifica se decisão atingiu quorum necessário"""

        approvals = json.loads(decision.approvals or "[]")

        if decision.impact_level == "critical":
            required_quorum = self.governance_rules["critical_decision_quorum"]
        else:
            required_quorum = self.governance_rules["min_decision_quorum"]

        # Buscar total de membros elegíveis para votar
        eligible_members = await self._get_eligible_voters(
            decision.institution_id, decision.approval_level
        )

        # Calcular quorum
        approval_count = len([a for a in approvals if a["vote"] == "approve"])
        current_quorum = (
            approval_count / len(eligible_members) if eligible_members else 0
        )

        return current_quorum >= required_quorum

    async def _get_eligible_voters(
        self, institution_id: int, approval_level: str
    ) -> List[int]:
        """Obtém lista de membros elegíveis para votar"""

        # Em produção, implementar lógica baseada no approval_level
        # Por enquanto, retornar mock
        return [1, 2, 3, 4, 5]  # Mock

    async def _apply_decision(self, decision: Decision) -> None:
        """Aplica decisão aprovada"""

        # Em produção, implementar lógica específica por tipo de decisão
        logger.info(f"Aplicando decisão: {decision.title}")

    async def _check_meeting_conflicts(self, scheduled_date: datetime) -> Optional[str]:
        """Verifica conflitos de agenda"""

        # Verificar se há reuniões no mesmo horário
        result = await self.db.execute(
            select(CouncilMeeting).where(
                and_(
                    CouncilMeeting.status == "scheduled",
                    func.abs(
                        func.extract(
                            "epoch", CouncilMeeting.scheduled_date - scheduled_date
                        )
                    )
                    < 3600,  # 1 hora
                )
            )
        )

        conflicts = result.scalars().all()

        if conflicts:
            return f"Conflito com reunião: {conflicts[0].title}"

        return None

    async def _calculate_required_attendees(self, meeting_type: str) -> int:
        """Calcula número mínimo de participantes"""

        quorum_rules = {"ordinary": 3, "extraordinary": 5, "emergency": 2, "annual": 7}

        return quorum_rules.get(meeting_type, 3)

    async def _send_meeting_invitations(self, meeting: CouncilMeeting) -> None:
        """Envia convites para reunião"""

        # Em produção, integrar com sistema de notificações
        logger.info(f"Convites enviados para reunião: {meeting.title}")

    async def _collect_risk_factors(self, institution_id: int) -> Dict[str, Any]:
        """Coleta fatores de risco"""

        # Buscar dados históricos
        result = await self.db.execute(
            select(func.count(AuditoriaLog.id)).where(
                and_(
                    AuditoriaLog.entity_type == "decision",
                    AuditoriaLog.created_at >= datetime.utcnow() - timedelta(days=365),
                )
            )
        )

        decision_count = result.scalar() or 0

        # Buscar mandatos ativos
        result = await self.db.execute(
            select(func.count(Mandate.id)).where(
                and_(
                    Mandate.institution_id == institution_id, Mandate.status == "active"
                )
            )
        )

        active_mandates = result.scalar() or 0

        return {
            "decision_frequency": decision_count,
            "active_mandates": active_mandates,
            "compliance_score": 85.0,  # Mock
            "financial_health": 78.0,  # Mock
        }

    def _calculate_risk_score(self, factors: Dict[str, Any]) -> float:
        """Calcula score de risco"""

        # Pesos para cada fator
        weights = {
            "decision_frequency": 0.3,
            "active_mandates": 0.2,
            "compliance_score": 0.3,
            "financial_health": 0.2,
        }

        # Normalizar fatores (0-100)
        normalized_factors = {
            "decision_frequency": min(factors["decision_frequency"] * 2, 100),
            "active_mandates": min(factors["active_mandates"] * 10, 100),
            "compliance_score": factors["compliance_score"],
            "financial_health": factors["financial_health"],
        }

        # Calcular score ponderado
        risk_score = sum(
            normalized_factors[factor] * weights[factor] for factor in weights
        )

        return round(risk_score, 2)

    def _determine_risk_level(self, risk_score: float) -> str:
        """Determina nível de risco baseado no score"""

        if risk_score >= 80:
            return "high"
        elif risk_score >= 60:
            return "medium"
        elif risk_score >= 40:
            return "low"
        else:
            return "minimal"

    def _generate_risk_recommendations(
        self, factors: Dict[str, Any], risk_level: str
    ) -> List[str]:
        """Gera recomendações baseadas no nível de risco"""

        recommendations = []

        if risk_level == "high":
            recommendations.extend(
                [
                    "Realizar auditoria completa da instituição",
                    "Implementar controles adicionais de compliance",
                    "Revisar processos de tomada de decisão",
                    "Agendar reunião de emergência do conselho",
                ]
            )
        elif risk_level == "medium":
            recommendations.extend(
                [
                    "Monitorar indicadores de risco semanalmente",
                    "Revisar políticas institucionais",
                    "Capacitar equipe em gestão de riscos",
                ]
            )
        elif risk_level == "low":
            recommendations.extend(
                ["Manter monitoramento regular", "Atualizar documentação de processos"]
            )
        else:
            recommendations.append("Manter monitoramento padrão")

        return recommendations

    async def _log_audit_action(
        self, action: str, entity_type: str, entity_id: int, details: Dict[str, Any]
    ) -> None:
        """Registra ação de auditoria"""

        audit_log = AuditoriaLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=json.dumps(details),
            timestamp=datetime.utcnow(),
        )

        self.db.add(audit_log)
        await self.db.commit()
