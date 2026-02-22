"""
Serviço médico principal - SILA System
Fase 2: Módulos Importantes - Lógica de Negócio Real

Implementa lógica médica complexa:
- Gestão de prontuários eletrônicos
- Agendamentos inteligentes
- Protocolos médicos
- Análise de sintomas e diagnósticos
- Gestão de medicamentos e prescrições
"""

import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.appointment import Appointment
from ..models.health_record import HealthRecord
from ..models.medical_service import MedicalService
from ..models.prescription import Prescription
from ..schemas.appointment import AppointmentCreate
from ..schemas.health import HealthCreate
from ..schemas.prescription import PrescriptionCreate

logger = logging.getLogger(__name__)


class UrgencyLevel(str, Enum):
    """Níveis de urgência médica"""

    LOW = "low"  # Baixa - agendamento normal
    MEDIUM = "medium"  # Média - agendamento prioritário
    HIGH = "high"  # Alta - atendimento em 24h
    CRITICAL = "critical"  # Crítica - atendimento imediato


class MedicalService:
    """Serviço principal para operações médicas"""

    def __init__(self, db: AsyncSession):
        self.db = db

        # Protocolos médicos e regras de negócio
        self.medical_protocols = {
            "symptom_analysis": {
                "fever": {"urgency": "high", "priority": 1},
                "chest_pain": {"urgency": "critical", "priority": 1},
                "difficulty_breathing": {"urgency": "critical", "priority": 1},
                "severe_headache": {"urgency": "high", "priority": 2},
                "abdominal_pain": {"urgency": "medium", "priority": 3},
                "cough": {"urgency": "low", "priority": 4},
                "fatigue": {"urgency": "low", "priority": 5},
            },
            "age_groups": {
                "pediatric": {"min_age": 0, "max_age": 17, "specialty": "pediatrics"},
                "adult": {"min_age": 18, "max_age": 64, "specialty": "general"},
                "elderly": {"min_age": 65, "max_age": 120, "specialty": "geriatrics"},
            },
            "appointment_duration": {
                "consultation": 30,  # minutos
                "examination": 45,
                "procedure": 60,
                "emergency": 20,
            },
        }

    # ========================================
    # GESTÃO DE PRONTUÁRIOS ELETRÔNICOS
    # ========================================

    async def create_health_record(
        self, record_data: HealthCreate, doctor_id: int
    ) -> HealthRecord:
        """Cria prontuário médico com análise de sintomas"""

        # Analisar sintomas para determinar urgência
        urgency_analysis = await self._analyze_symptoms(record_data.symptoms)

        # Determinar especialidade necessária
        specialty = await self._determine_specialty(
            record_data.symptoms, record_data.patient_age
        )

        # Criar prontuário
        health_record = HealthRecord(
            patient_id=record_data.patient_id,
            doctor_id=doctor_id,
            symptoms=record_data.symptoms,
            diagnosis=record_data.diagnosis,
            treatment_plan=record_data.treatment_plan,
            urgency_level=urgency_analysis["urgency"],
            specialty=specialty,
            vital_signs=(
                json.dumps(record_data.vital_signs) if record_data.vital_signs else None
            ),
            medical_history=(
                json.dumps(record_data.medical_history)
                if record_data.medical_history
                else None
            ),
            created_at=datetime.utcnow(),
        )

        self.db.add(health_record)
        await self.db.commit()
        await self.db.refresh(health_record)

        # Se urgência crítica, criar alerta
        if urgency_analysis["urgency"] == UrgencyLevel.CRITICAL:
            await self._create_medical_alert(health_record)

        logger.info(
            f"Prontuário criado: ID {health_record.id}, Urgência: {urgency_analysis['urgency']}"
        )

        return health_record

    async def update_diagnosis(
        self, record_id: int, diagnosis: str, doctor_id: int
    ) -> HealthRecord:
        """Atualiza diagnóstico com validações médicas"""

        # Buscar prontuário
        result = await self.db.execute(
            select(HealthRecord).where(HealthRecord.id == record_id)
        )
        record = result.scalar_one_or_none()

        if not record:
            raise ValueError("Prontuário não encontrado")

        # Validar se médico tem acesso ao prontuário
        if record.doctor_id != doctor_id:
            # Verificar se é especialista na área
            has_access = await self._check_doctor_access(doctor_id, record.specialty)
            if not has_access:
                raise ValueError("Médico não tem acesso a este prontuário")

        # Atualizar diagnóstico
        record.diagnosis = diagnosis
        record.updated_at = datetime.utcnow()

        await self.db.commit()

        # Registrar mudança de diagnóstico
        await self._log_diagnosis_change(record_id, diagnosis, doctor_id)

        logger.info(f"Diagnóstico atualizado: Prontuário {record_id}")

        return record

    # ========================================
    # AGENDAMENTOS INTELIGENTES
    # ========================================

    async def create_appointment(
        self, appointment_data: AppointmentCreate
    ) -> Appointment:
        """Cria agendamento com otimização automática"""

        # Analisar urgência do agendamento
        urgency = await self._determine_appointment_urgency(appointment_data.reason)

        # Encontrar horário otimizado
        optimal_slot = await self._find_optimal_appointment_slot(
            appointment_data.specialty, urgency, appointment_data.preferred_date
        )

        if not optimal_slot:
            raise ValueError("Nenhum horário disponível encontrado")

        # Criar agendamento
        appointment = Appointment(
            patient_id=appointment_data.patient_id,
            doctor_id=optimal_slot["doctor_id"],
            specialty=appointment_data.specialty,
            appointment_type=appointment_data.appointment_type,
            scheduled_date=optimal_slot["datetime"],
            duration=self.medical_protocols["appointment_duration"].get(
                appointment_data.appointment_type, 30
            ),
            reason=appointment_data.reason,
            urgency_level=urgency,
            status="scheduled",
            created_at=datetime.utcnow(),
        )

        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)

        # Enviar confirmação (mock)
        await self._send_appointment_confirmation(appointment)

        logger.info(
            f"Agendamento criado: ID {appointment.id}, Data: {optimal_slot['datetime']}"
        )

        return appointment

    async def reschedule_appointment(
        self, appointment_id: int, new_date: datetime, reason: str
    ) -> Appointment:
        """Reagenda consulta com validações"""

        # Buscar agendamento
        result = await self.db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        appointment = result.scalar_one_or_none()

        if not appointment:
            raise ValueError("Agendamento não encontrado")

        # Validar se pode ser reagendado (não pode ser no passado, etc.)
        if new_date < datetime.utcnow():
            raise ValueError("Nova data não pode ser no passado")

        # Verificar disponibilidade do médico
        doctor_available = await self._check_doctor_availability(
            appointment.doctor_id, new_date
        )

        if not doctor_available:
            raise ValueError("Médico não disponível na nova data")

        # Reagendar
        old_date = appointment.scheduled_date
        appointment.scheduled_date = new_date
        appointment.reschedule_reason = reason
        appointment.updated_at = datetime.utcnow()

        await self.db.commit()

        # Registrar histórico de reagendamento
        await self._log_appointment_change(appointment_id, old_date, new_date, reason)

        logger.info(
            f"Agendamento reagendado: ID {appointment_id}, Nova data: {new_date}"
        )

        return appointment

    # ========================================
    # PRESCRIÇÕES E MEDICAMENTOS
    # ========================================

    async def create_prescription(
        self, prescription_data: PrescriptionCreate, doctor_id: int
    ) -> Prescription:
        """Cria prescrição médica com validações de medicamentos"""

        # Validar medicamentos
        for medication in prescription_data.medications:
            validation = await self._validate_medication(
                medication["name"],
                medication["dosage"],
                medication["frequency"],
                prescription_data.patient_id,
            )

            if not validation["valid"]:
                raise ValueError(f"Medicamento inválido: {validation['reason']}")

        # Verificar interações medicamentosas
        interactions = await self._check_drug_interactions(
            prescription_data.medications
        )

        if interactions:
            # Criar alerta de interação
            await self._create_interaction_alert(
                prescription_data.patient_id, interactions
            )

        # Criar prescrição
        prescription = Prescription(
            patient_id=prescription_data.patient_id,
            doctor_id=doctor_id,
            medications=json.dumps(prescription_data.medications),
            instructions=prescription_data.instructions,
            valid_until=prescription_data.valid_until,
            status="active",
            created_at=datetime.utcnow(),
        )

        self.db.add(prescription)
        await self.db.commit()
        await self.db.refresh(prescription)

        logger.info(
            f"Prescrição criada: ID {prescription.id}, Paciente: {prescription_data.patient_id}"
        )

        return prescription

    # ========================================
    # ANÁLISE MÉDICA E DIAGNÓSTICOS
    # ========================================

    async def analyze_patient_symptoms(
        self, symptoms: List[str], patient_age: int
    ) -> Dict[str, Any]:
        """Analisa sintomas do paciente usando protocolos médicos"""

        analysis = {
            "urgency_level": UrgencyLevel.LOW,
            "priority_score": 0,
            "recommended_specialty": "general",
            "suspected_conditions": [],
            "recommended_actions": [],
        }

        # Analisar cada sintoma
        for symptom in symptoms:
            symptom_lower = symptom.lower()

            if symptom_lower in self.medical_protocols["symptom_analysis"]:
                protocol = self.medical_protocols["symptom_analysis"][symptom_lower]

                # Atualizar urgência se mais alta
                if self._is_urgency_higher(
                    protocol["urgency"], analysis["urgency_level"]
                ):
                    analysis["urgency_level"] = protocol["urgency"]

                # Somar score de prioridade
                analysis["priority_score"] += protocol["priority"]

        # Determinar especialidade baseada em idade e sintomas
        analysis["recommended_specialty"] = (
            self._determine_specialty_by_age_and_symptoms(patient_age, symptoms)
        )

        # Gerar condições suspeitas
        analysis["suspected_conditions"] = await self._generate_differential_diagnosis(
            symptoms
        )

        # Gerar ações recomendadas
        analysis["recommended_actions"] = await self._generate_recommended_actions(
            analysis
        )

        return analysis

    async def get_patient_medical_history(self, patient_id: int) -> Dict[str, Any]:
        """Obtém histórico médico completo do paciente"""

        # Buscar prontuários
        result = await self.db.execute(
            select(HealthRecord)
            .where(HealthRecord.patient_id == patient_id)
            .order_by(desc(HealthRecord.created_at))
        )
        records = result.scalars().all()

        # Buscar prescrições ativas
        prescription_result = await self.db.execute(
            select(Prescription).where(
                and_(
                    Prescription.patient_id == patient_id,
                    Prescription.status == "active",
                    Prescription.valid_until >= datetime.utcnow(),
                )
            )
        )
        active_prescriptions = prescription_result.scalars().all()

        # Buscar alergias conhecidas
        allergies = await self._get_patient_allergies(patient_id)

        # Calcular métricas de saúde
        health_metrics = await self._calculate_health_metrics(records)

        return {
            "patient_id": patient_id,
            "records": [self._format_health_record(record) for record in records],
            "active_prescriptions": [
                self._format_prescription(prescription)
                for prescription in active_prescriptions
            ],
            "allergies": allergies,
            "health_metrics": health_metrics,
            "last_consultation": records[0].created_at if records else None,
        }

    # ========================================
    # MÉTODOS AUXILIARES PRIVADOS
    # ========================================

    async def _analyze_symptoms(self, symptoms: str) -> Dict[str, Any]:
        """Analisa sintomas para determinar urgência"""

        symptoms_list = [s.strip().lower() for s in symptoms.split(",")]

        max_urgency = UrgencyLevel.LOW
        priority_score = 0

        for symptom in symptoms_list:
            if symptom in self.medical_protocols["symptom_analysis"]:
                protocol = self.medical_protocols["symptom_analysis"][symptom]

                if self._is_urgency_higher(protocol["urgency"], max_urgency):
                    max_urgency = protocol["urgency"]

                priority_score += protocol["priority"]

        return {
            "urgency": max_urgency,
            "priority_score": priority_score,
            "analyzed_symptoms": symptoms_list,
        }

    async def _determine_specialty(self, symptoms: str, patient_age: int) -> str:
        """Determina especialidade médica necessária"""

        # Determinar por idade primeiro
        for age_group, config in self.medical_protocols["age_groups"].items():
            if config["min_age"] <= patient_age <= config["max_age"]:
                base_specialty = config["specialty"]
                break
        else:
            base_specialty = "general"

        # Ajustar por sintomas específicos
        symptoms_lower = symptoms.lower()

        if any(symptom in symptoms_lower for symptom in ["heart", "chest", "cardiac"]):
            return "cardiology"
        elif any(
            symptom in symptoms_lower for symptom in ["brain", "head", "neurological"]
        ):
            return "neurology"
        elif any(symptom in symptoms_lower for symptom in ["bone", "joint", "muscle"]):
            return "orthopedics"
        elif any(
            symptom in symptoms_lower for symptom in ["skin", "rash", "dermatology"]
        ):
            return "dermatology"
        else:
            return base_specialty

    async def _find_optimal_appointment_slot(
        self, specialty: str, urgency: UrgencyLevel, preferred_date: datetime
    ) -> Optional[Dict[str, Any]]:
        """Encontra horário otimizado para agendamento"""

        # Buscar médicos disponíveis na especialidade
        available_doctors = await self._get_available_doctors(specialty)

        if not available_doctors:
            return None

        # Para urgência crítica, procurar horário mais próximo
        if urgency == UrgencyLevel.CRITICAL:
            return await self._find_emergency_slot(available_doctors)

        # Para outras urgências, procurar próximo à data preferida
        return await self._find_preferred_slot(available_doctors, preferred_date)

    async def _get_available_doctors(self, specialty: str) -> List[Dict[str, Any]]:
        """Obtém lista de médicos disponíveis na especialidade"""

        # Em produção, buscar do banco de dados
        # Mock para demonstração
        return [
            {
                "id": 1,
                "name": "Dr. João Silva",
                "specialty": specialty,
                "schedule": "08:00-17:00",
            },
            {
                "id": 2,
                "name": "Dra. Maria Santos",
                "specialty": specialty,
                "schedule": "09:00-18:00",
            },
            {
                "id": 3,
                "name": "Dr. Pedro Costa",
                "specialty": specialty,
                "schedule": "08:30-16:30",
            },
        ]

    async def _find_emergency_slot(
        self, doctors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Encontra slot de emergência"""

        # Para emergência, usar primeiro médico disponível
        return {
            "doctor_id": doctors[0]["id"],
            "datetime": datetime.utcnow() + timedelta(hours=1),
            "type": "emergency",
        }

    async def _find_preferred_slot(
        self, doctors: List[Dict[str, Any]], preferred_date: datetime
    ) -> Dict[str, Any]:
        """Encontra slot próximo à data preferida"""

        # Simular busca por horário disponível
        return {
            "doctor_id": doctors[0]["id"],
            "datetime": preferred_date,
            "type": "scheduled",
        }

    async def _validate_medication(
        self, name: str, dosage: str, frequency: str, patient_id: int
    ) -> Dict[str, Any]:
        """Valida medicamento e dosagem"""

        # Em produção, integrar com base de dados de medicamentos
        # Verificar se medicamento existe
        valid_medications = [
            "paracetamol",
            "ibuprofeno",
            "amoxicilina",
            "omeprazol",
            "losartana",
            "metformina",
            "atorvastatina",
        ]

        if name.lower() not in valid_medications:
            return {"valid": False, "reason": f"Medicamento {name} não reconhecido"}

        # Verificar alergias do paciente
        allergies = await self._get_patient_allergies(patient_id)
        if name.lower() in allergies:
            return {
                "valid": False,
                "reason": f"Paciente tem alergia ao medicamento {name}",
            }

        return {"valid": True, "reason": "Medicamento válido"}

    async def _check_drug_interactions(
        self, medications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Verifica interações medicamentosas"""

        # Em produção, usar base de dados de interações
        interactions = []

        medication_names = [med["name"].lower() for med in medications]

        # Regras simples de interação (mock)
        if "paracetamol" in medication_names and "ibuprofeno" in medication_names:
            interactions.append(
                {
                    "medication1": "paracetamol",
                    "medication2": "ibuprofeno",
                    "severity": "moderate",
                    "description": "Pode aumentar risco de danos ao fígado",
                }
            )

        return interactions

    async def _get_patient_allergies(self, patient_id: int) -> List[str]:
        """Obtém alergias do paciente"""

        # Em produção, buscar do banco de dados
        # Mock para demonstração
        mock_allergies = {
            1: ["penicilina", "amoxicilina"],
            2: ["aspirina", "ibuprofeno"],
            3: [],
        }

        return mock_allergies.get(patient_id, [])

    async def _calculate_health_metrics(
        self, records: List[HealthRecord]
    ) -> Dict[str, Any]:
        """Calcula métricas de saúde do paciente"""

        if not records:
            return {}

        # Calcular frequência de consultas
        consultation_frequency = len(records) / 12  # por mês (assumindo 1 ano)

        # Calcular especialidades mais visitadas
        specialties = {}
        for record in records:
            specialties[record.specialty] = specialties.get(record.specialty, 0) + 1

        # Determinar condição mais comum
        most_common_condition = (
            max(specialties.items(), key=lambda x: x[1])[0] if specialties else None
        )

        return {
            "consultation_frequency": round(consultation_frequency, 2),
            "most_visited_specialty": most_common_condition,
            "total_consultations": len(records),
            "health_trend": "stable",  # Em produção, calcular baseado em histórico
        }

    def _is_urgency_higher(self, urgency1: str, urgency2: str) -> bool:
        """Compara níveis de urgência"""

        urgency_order = {
            UrgencyLevel.LOW: 1,
            UrgencyLevel.MEDIUM: 2,
            UrgencyLevel.HIGH: 3,
            UrgencyLevel.CRITICAL: 4,
        }

        return urgency_order.get(urgency1, 0) > urgency_order.get(urgency2, 0)

    def _determine_specialty_by_age_and_symptoms(
        self, age: int, symptoms: List[str]
    ) -> str:
        """Determina especialidade baseada em idade e sintomas"""

        # Lógica de determinação de especialidade
        if age < 18:
            return "pediatrics"
        elif age > 65:
            return "geriatrics"
        else:
            # Analisar sintomas para especialidade específica
            symptoms_str = " ".join(symptoms).lower()

            if any(symptom in symptoms_str for symptom in ["heart", "chest"]):
                return "cardiology"
            elif any(symptom in symptoms_str for symptom in ["brain", "head"]):
                return "neurology"
            else:
                return "general"

    async def _generate_differential_diagnosis(self, symptoms: List[str]) -> List[str]:
        """Gera diagnóstico diferencial baseado em sintomas"""

        # Em produção, usar IA ou base de dados médica
        # Mock para demonstração
        symptom_keywords = " ".join(symptoms).lower()

        if "fever" in symptom_keywords and "cough" in symptom_keywords:
            return ["Gripe", "Resfriado comum", "Infecção respiratória"]
        elif "chest pain" in symptom_keywords:
            return ["Angina", "Infarto do miocárdio", "Ansiedade"]
        else:
            return ["Avaliação clínica necessária"]

    async def _generate_recommended_actions(
        self, analysis: Dict[str, Any]
    ) -> List[str]:
        """Gera ações recomendadas baseadas na análise"""

        actions = []

        if analysis["urgency_level"] == UrgencyLevel.CRITICAL:
            actions.extend(
                [
                    "Encaminhamento imediato para emergência",
                    "Monitoramento contínuo de sinais vitais",
                    "Avaliação por especialista em 2 horas",
                ]
            )
        elif analysis["urgency_level"] == UrgencyLevel.HIGH:
            actions.extend(
                [
                    "Agendamento prioritário",
                    "Avaliação em 24 horas",
                    "Monitoramento de sintomas",
                ]
            )
        else:
            actions.extend(
                ["Agendamento regular", "Observação de sintomas", "Retorno se piora"]
            )

        return actions

    def _format_health_record(self, record: HealthRecord) -> Dict[str, Any]:
        """Formata prontuário para resposta"""

        return {
            "id": record.id,
            "symptoms": record.symptoms,
            "diagnosis": record.diagnosis,
            "urgency_level": record.urgency_level,
            "specialty": record.specialty,
            "created_at": record.created_at,
            "doctor_id": record.doctor_id,
        }

    def _format_prescription(self, prescription: Prescription) -> Dict[str, Any]:
        """Formata prescrição para resposta"""

        return {
            "id": prescription.id,
            "medications": json.loads(prescription.medications),
            "instructions": prescription.instructions,
            "valid_until": prescription.valid_until,
            "created_at": prescription.created_at,
        }

    # Métodos de logging e alertas (mock)
    async def _create_medical_alert(self, record: HealthRecord) -> None:
        """Cria alerta médico"""
        logger.warning(f"ALERTA MÉDICO: Prontuário {record.id} - Urgência CRÍTICA")

    async def _send_appointment_confirmation(self, appointment: Appointment) -> None:
        """Envia confirmação de agendamento"""
        logger.info(f"Confirmação enviada para agendamento {appointment.id}")

    async def _log_diagnosis_change(
        self, record_id: int, diagnosis: str, doctor_id: int
    ) -> None:
        """Registra mudança de diagnóstico"""
        logger.info(
            f"Diagnóstico alterado: Prontuário {record_id} por médico {doctor_id}"
        )

    async def _log_appointment_change(
        self, appointment_id: int, old_date: datetime, new_date: datetime, reason: str
    ) -> None:
        """Registra mudança de agendamento"""
        logger.info(
            f"Agendamento {appointment_id} alterado: {old_date} -> {new_date}, Motivo: {reason}"
        )

    async def _create_interaction_alert(
        self, patient_id: int, interactions: List[Dict[str, Any]]
    ) -> None:
        """Cria alerta de interação medicamentosa"""
        logger.warning(
            f"ALERTA: Interações medicamentosas detectadas para paciente {patient_id}"
        )

    async def _check_doctor_access(self, doctor_id: int, specialty: str) -> bool:
        """Verifica se médico tem acesso à especialidade"""
        # Mock - em produção verificar especialização do médico
        return True

    async def _check_doctor_availability(self, doctor_id: int, date: datetime) -> bool:
        """Verifica disponibilidade do médico"""
        # Mock - em produção verificar agenda do médico
        return True
