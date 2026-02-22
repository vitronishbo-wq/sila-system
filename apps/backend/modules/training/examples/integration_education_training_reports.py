#!/usr/bin/env python3
"""
Exemplo Prático: Integração Education + Training + Reports
Sistema SILA - Fluxo de Dados entre Módulos

Este script demonstra como os dados fluem entre os módulos:
1. Education (dados escolares)
2. Training (cursos técnicos)
3. Reports (relatórios consolidados)

Cenário: João conclui ensino secundário → se inscreve em curso técnico → dados consolidados em relatórios
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


# Simulação de dados dos módulos
class EducationLevel(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    UNIVERSITY = "university"


class TrainingCategory(Enum):
    TECHNICAL = "technical"
    PROFESSIONAL = "professional"
    CIVIC = "civic"


class CourseStatus(Enum):
    ENROLLED = "enrolled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DROPPED = "dropped"


@dataclass
class EducationRecord:
    """Registro educacional do módulo Education"""

    student_id: int
    name: str
    level: EducationLevel
    school_name: str
    municipality: str
    province: str
    final_grade: float  # 0-20
    attendance_rate: float  # 0-100%
    graduation_date: datetime
    has_certificate: bool


@dataclass
class TrainingCourse:
    """Curso de capacitação do módulo Training"""

    course_id: int
    title: str
    category: TrainingCategory
    prerequisites: List[str]
    duration_months: int
    municipality: str
    province: str
    max_participants: int
    current_enrolled: int


@dataclass
class TrainingEnrollment:
    """Inscrição no módulo Training"""

    enrollment_id: int
    student_id: int
    course_id: int
    status: CourseStatus
    enrollment_date: datetime
    completion_date: Optional[datetime]
    final_grade: Optional[float]
    attendance_rate: Optional[float]
    certificate_number: Optional[str]


@dataclass
class ReportKPI:
    """KPIs consolidados do módulo Reports"""

    municipality: str
    province: str
    secondary_graduates: int
    training_enrollments: int
    training_completions: int
    employment_rate: float
    continuity_rate: float  # % que passa de Education para Training


class EducationAPI:
    """Simulação da API do módulo Education"""

    def __init__(self):
        self.students = self._generate_sample_students()

    def _generate_sample_students(self) -> List[EducationRecord]:
        """Gera dados de exemplo de estudantes"""
        students = []
        municipalities = ["Luanda", "Benguela", "Huambo", "Lobito", "Cabinda"]
        provinces = ["Luanda", "Benguela", "Huambo", "Benguela", "Cabinda"]

        for i in range(1, 501):  # 500 estudantes
            students.append(
                EducationRecord(
                    student_id=i,
                    name=f"Estudante {i}",
                    level=EducationLevel.SECONDARY,
                    school_name=f"Escola Secundária {municipalities[i % 5]}",
                    municipality=municipalities[i % 5],
                    province=provinces[i % 5],
                    final_grade=round(10 + (i % 11), 1),  # Notas de 10 a 20
                    attendance_rate=round(75 + (i % 26), 1),  # 75% a 100%
                    graduation_date=datetime.now() - timedelta(days=i % 365),
                    has_certificate=True,
                )
            )
        return students

    async def get_student_by_id(self, student_id: int) -> Optional[EducationRecord]:
        """GET /education/students/{id} - Histórico escolar"""
        return next((s for s in self.students if s.student_id == student_id), None)

    async def get_graduates_by_municipality(
        self, municipality: str, level: EducationLevel
    ) -> List[EducationRecord]:
        """GET /education/graduates - Graduados por município e nível"""
        return [
            s
            for s in self.students
            if s.municipality == municipality and s.level == level
        ]

    async def get_statistics(self) -> Dict[str, Any]:
        """GET /education/statistics - Estatísticas educacionais"""
        by_municipality = {}
        for student in self.students:
            if student.municipality not in by_municipality:
                by_municipality[student.municipality] = {
                    "total_students": 0,
                    "avg_grade": 0,
                    "avg_attendance": 0,
                }
            by_municipality[student.municipality]["total_students"] += 1

        # Calcular médias
        for municipality in by_municipality:
            students_in_mun = [
                s for s in self.students if s.municipality == municipality
            ]
            by_municipality[municipality]["avg_grade"] = round(
                sum(s.final_grade for s in students_in_mun) / len(students_in_mun), 2
            )
            by_municipality[municipality]["avg_attendance"] = round(
                sum(s.attendance_rate for s in students_in_mun) / len(students_in_mun),
                2,
            )

        return {
            "total_students": len(self.students),
            "by_municipality": by_municipality,
            "generated_at": datetime.now().isoformat(),
        }


class TrainingAPI:
    """Simulação da API do módulo Training"""

    def __init__(self, education_api: EducationAPI):
        self.education_api = education_api
        self.courses = self._generate_sample_courses()
        self.enrollments = []

    def _generate_sample_courses(self) -> List[TrainingCourse]:
        """Gera cursos técnicos de exemplo"""
        courses = [
            TrainingCourse(
                1,
                "Técnico em Eletricidade",
                TrainingCategory.TECHNICAL,
                ["Ensino Secundário"],
                6,
                "Luanda",
                "Luanda",
                30,
                0,
            ),
            TrainingCourse(
                2,
                "Soldadura e Serralheria",
                TrainingCategory.TECHNICAL,
                ["Ensino Secundário"],
                4,
                "Benguela",
                "Benguela",
                25,
                0,
            ),
            TrainingCourse(
                3,
                "Informática Básica",
                TrainingCategory.PROFESSIONAL,
                ["Ensino Primário"],
                3,
                "Huambo",
                "Huambo",
                40,
                0,
            ),
            TrainingCourse(
                4,
                "Mecânica Automóvel",
                TrainingCategory.TECHNICAL,
                ["Ensino Secundário"],
                8,
                "Lobito",
                "Benguela",
                20,
                0,
            ),
            TrainingCourse(
                5,
                "Administração Pública",
                TrainingCategory.CIVIC,
                ["Ensino Secundário"],
                5,
                "Cabinda",
                "Cabinda",
                35,
                0,
            ),
        ]
        return courses

    async def validate_prerequisites(self, student_id: int, course_id: int) -> bool:
        """Valida pré-requisitos cruzando com Education"""
        student = await self.education_api.get_student_by_id(student_id)
        course = next((c for c in self.courses if c.course_id == course_id), None)

        if not student or not course:
            return False

        # Validação simples: se tem ensino secundário, pode fazer cursos técnicos
        if "Ensino Secundário" in course.prerequisites:
            return (
                student.level == EducationLevel.SECONDARY and student.final_grade >= 10
            )

        return True

    async def enroll_student(
        self, student_id: int, course_id: int
    ) -> Optional[TrainingEnrollment]:
        """POST /training/enrollments - Inscrever estudante"""
        # Validar pré-requisitos
        if not await self.validate_prerequisites(student_id, course_id):
            return None

        # Verificar capacidade do curso
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if not course or course.current_enrolled >= course.max_participants:
            return None

        # Criar inscrição
        enrollment = TrainingEnrollment(
            enrollment_id=len(self.enrollments) + 1,
            student_id=student_id,
            course_id=course_id,
            status=CourseStatus.ENROLLED,
            enrollment_date=datetime.now(),
            completion_date=None,
            final_grade=None,
            attendance_rate=None,
            certificate_number=None,
        )

        self.enrollments.append(enrollment)
        course.current_enrolled += 1

        return enrollment

    async def complete_course(
        self, enrollment_id: int, grade: float, attendance: float
    ) -> bool:
        """POST /training/enrollments/{id}/complete - Completar curso"""
        enrollment = next(
            (e for e in self.enrollments if e.enrollment_id == enrollment_id), None
        )
        if not enrollment:
            return False

        enrollment.status = CourseStatus.COMPLETED
        enrollment.completion_date = datetime.now()
        enrollment.final_grade = grade
        enrollment.attendance_rate = attendance

        # Gerar certificado se aprovado (nota >= 10 e frequência >= 75%)
        if grade >= 10 and attendance >= 75:
            enrollment.certificate_number = (
                f"CERT-{enrollment_id}-{datetime.now().year}"
            )

        return True

    async def get_statistics(self) -> Dict[str, Any]:
        """GET /training/statistics - Estatísticas de capacitação"""
        by_municipality = {}
        for course in self.courses:
            if course.municipality not in by_municipality:
                by_municipality[course.municipality] = {
                    "total_courses": 0,
                    "total_enrolled": 0,
                    "total_completed": 0,
                    "completion_rate": 0,
                }

            by_municipality[course.municipality]["total_courses"] += 1
            by_municipality[course.municipality][
                "total_enrolled"
            ] += course.current_enrolled

        # Calcular conclusões por município
        for enrollment in self.enrollments:
            course = next(
                (c for c in self.courses if c.course_id == enrollment.course_id), None
            )
            if course and enrollment.status == CourseStatus.COMPLETED:
                by_municipality[course.municipality]["total_completed"] += 1

        # Calcular taxas de conclusão
        for municipality in by_municipality:
            enrolled = by_municipality[municipality]["total_enrolled"]
            completed = by_municipality[municipality]["total_completed"]
            by_municipality[municipality]["completion_rate"] = round(
                (completed / enrolled * 100) if enrolled > 0 else 0, 2
            )

        return {
            "total_courses": len(self.courses),
            "total_enrollments": len(self.enrollments),
            "by_municipality": by_municipality,
            "generated_at": datetime.now().isoformat(),
        }


class ReportsAPI:
    """Simulação da API do módulo Reports"""

    def __init__(self, education_api: EducationAPI, training_api: TrainingAPI):
        self.education_api = education_api
        self.training_api = training_api

    async def generate_education_training_report(self) -> Dict[str, Any]:
        """GET /reports/education-training - Relatório integrado"""
        education_stats = await self.education_api.get_statistics()
        training_stats = await self.training_api.get_statistics()

        # Consolidar dados por município
        municipalities = set(education_stats["by_municipality"].keys())
        municipalities.update(training_stats["by_municipality"].keys())

        consolidated_report = {
            "report_type": "education_training_integration",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_secondary_graduates": education_stats["total_students"],
                "total_training_enrollments": training_stats["total_enrollments"],
                "total_municipalities": len(municipalities),
            },
            "by_municipality": {},
        }

        for municipality in municipalities:
            edu_data = education_stats["by_municipality"].get(municipality, {})
            training_data = training_stats["by_municipality"].get(municipality, {})

            secondary_graduates = edu_data.get("total_students", 0)
            training_enrollments = training_data.get("total_enrolled", 0)
            training_completions = training_data.get("total_completed", 0)

            # Calcular taxa de continuidade (Education → Training)
            continuity_rate = round(
                (
                    (training_enrollments / secondary_graduates * 100)
                    if secondary_graduates > 0
                    else 0
                ),
                2,
            )

            # Simular taxa de empregabilidade (70-90% dos certificados)
            employment_rate = (
                round(training_completions * 0.8, 2) if training_completions > 0 else 0
            )

            consolidated_report["by_municipality"][municipality] = {
                "secondary_graduates": secondary_graduates,
                "training_enrollments": training_enrollments,
                "training_completions": training_completions,
                "continuity_rate": continuity_rate,
                "employment_rate": employment_rate,
                "avg_education_grade": edu_data.get("avg_grade", 0),
                "training_completion_rate": training_data.get("completion_rate", 0),
            }

        return consolidated_report

    async def get_kpis(self) -> Dict[str, Any]:
        """GET /reports/education-training/kpi - KPIs consolidados"""
        report = await self.generate_education_training_report()

        # Calcular KPIs globais
        total_graduates = report["summary"]["total_secondary_graduates"]
        total_enrollments = report["summary"]["total_training_enrollments"]

        total_completions = sum(
            data["training_completions"] for data in report["by_municipality"].values()
        )

        global_continuity_rate = round(
            (total_enrollments / total_graduates * 100) if total_graduates > 0 else 0, 2
        )

        global_completion_rate = round(
            (
                (total_completions / total_enrollments * 100)
                if total_enrollments > 0
                else 0
            ),
            2,
        )

        return {
            "global_kpis": {
                "continuity_rate": global_continuity_rate,
                "completion_rate": global_completion_rate,
                "total_graduates": total_graduates,
                "total_training_participants": total_enrollments,
                "total_certified": total_completions,
            },
            "top_municipalities": {
                "best_continuity": (
                    max(
                        report["by_municipality"].items(),
                        key=lambda x: x[1]["continuity_rate"],
                    )[0]
                    if report["by_municipality"]
                    else None
                ),
                "best_completion": (
                    max(
                        report["by_municipality"].items(),
                        key=lambda x: x[1]["training_completion_rate"],
                    )[0]
                    if report["by_municipality"]
                    else None
                ),
            },
            "generated_at": datetime.now().isoformat(),
        }


async def simulate_joao_journey():
    """
    🧪 Simulação do Cenário Prático: Jornada do João

    1. João conclui ensino secundário (Education)
    2. João se inscreve em curso técnico (Training)
    3. Dados consolidados em relatórios (Reports)
    """
    print("🚀 SIMULAÇÃO: Integração Education + Training + Reports")
    print("=" * 60)

    # Inicializar APIs
    education_api = EducationAPI()
    training_api = TrainingAPI(education_api)
    reports_api = ReportsAPI(education_api, training_api)

    print("\n📚 ETAPA 1: João no módulo Education")
    print("-" * 40)

    # João é o estudante ID 1
    joao = await education_api.get_student_by_id(1)
    print(f"👤 Estudante: {joao.name}")
    print(f"🏫 Escola: {joao.school_name}")
    print(f"📍 Município: {joao.municipality}")
    print(f"📊 Nota Final: {joao.final_grade}/20")
    print(f"📅 Frequência: {joao.attendance_rate}%")
    print(f"🎓 Graduação: {joao.graduation_date.strftime('%d/%m/%Y')}")

    print("\n🔧 ETAPA 2: João se inscreve no Training")
    print("-" * 40)

    # João se inscreve no curso de Eletricidade (ID 1)
    curso_eletricidade = training_api.courses[0]
    print(f"⚡ Curso: {curso_eletricidade.title}")
    print(f"📍 Local: {curso_eletricidade.municipality}")
    print(f"⏱️ Duração: {curso_eletricidade.duration_months} meses")

    # Validar pré-requisitos
    pode_inscrever = await training_api.validate_prerequisites(
        joao.student_id, curso_eletricidade.course_id
    )
    print(f"✅ Pré-requisitos: {'Atende' if pode_inscrever else 'Não atende'}")

    if pode_inscrever:
        # Inscrever João
        inscricao = await training_api.enroll_student(
            joao.student_id, curso_eletricidade.course_id
        )
        print(f"📝 Inscrição ID: {inscricao.enrollment_id}")
        print(f"📅 Data Inscrição: {inscricao.enrollment_date.strftime('%d/%m/%Y')}")

        # Simular conclusão do curso
        await training_api.complete_course(inscricao.enrollment_id, 16.5, 90.0)

        # Buscar inscrição atualizada
        inscricao_atualizada = next(
            (
                e
                for e in training_api.enrollments
                if e.enrollment_id == inscricao.enrollment_id
            ),
            None,
        )

        print(f"🎯 Status: {inscricao_atualizada.status.value}")
        print(f"📊 Nota Final: {inscricao_atualizada.final_grade}/20")
        print(f"📅 Frequência: {inscricao_atualizada.attendance_rate}%")
        print(f"🏆 Certificado: {inscricao_atualizada.certificate_number}")

    print("\n📊 ETAPA 3: Dados consolidados no Reports")
    print("-" * 40)

    # Simular mais inscrições para ter dados significativos
    print("📈 Simulando mais inscrições para análise...")
    for student_id in range(2, 201):  # 200 estudantes se inscrevem
        course_id = ((student_id - 1) % 5) + 1  # Distribuir entre os 5 cursos
        if await training_api.validate_prerequisites(student_id, course_id):
            enrollment = await training_api.enroll_student(student_id, course_id)
            if enrollment:
                # 80% completam o curso
                if student_id % 5 != 0:  # 80% de taxa de conclusão
                    grade = 10 + (student_id % 11)  # Notas variadas
                    attendance = 75 + (student_id % 26)  # Frequência variada
                    await training_api.complete_course(
                        enrollment.enrollment_id, grade, attendance
                    )

    # Gerar relatório consolidado
    relatorio = await reports_api.generate_education_training_report()
    kpis = await reports_api.get_kpis()

    print(f"\n📋 RELATÓRIO CONSOLIDADO")
    print(
        f"🎓 Total Graduados (Education): {relatorio['summary']['total_secondary_graduates']}"
    )
    print(
        f"📚 Total Inscrições (Training): {relatorio['summary']['total_training_enrollments']}"
    )
    print(f"🏆 Taxa Continuidade Global: {kpis['global_kpis']['continuity_rate']}%")
    print(f"✅ Taxa Conclusão Global: {kpis['global_kpis']['completion_rate']}%")

    print(f"\n🏆 TOP MUNICÍPIOS:")
    if kpis["top_municipalities"]["best_continuity"]:
        print(
            f"🥇 Melhor Continuidade: {kpis['top_municipalities']['best_continuity']}"
        )
    if kpis["top_municipalities"]["best_completion"]:
        print(f"🥇 Melhor Conclusão: {kpis['top_municipalities']['best_completion']}")

    print(f"\n📊 DETALHES POR MUNICÍPIO:")
    for municipio, dados in relatorio["by_municipality"].items():
        print(f"\n📍 {municipio}:")
        print(f"  🎓 Graduados: {dados['secondary_graduates']}")
        print(f"  📚 Inscrições Training: {dados['training_enrollments']}")
        print(f"  ✅ Conclusões: {dados['training_completions']}")
        print(f"  📈 Taxa Continuidade: {dados['continuity_rate']}%")
        print(f"  💼 Empregabilidade: {dados['employment_rate']}%")

    # Salvar relatórios em arquivos
    print(f"\n💾 Salvando relatórios...")

    with open("/tmp/sila_education_training_report.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)

    with open("/tmp/sila_kpis_report.json", "w", encoding="utf-8") as f:
        json.dump(kpis, f, indent=2, ensure_ascii=False, default=str)

    print("✅ Relatórios salvos em /tmp/sila_*_report.json")

    print(f"\n🎯 CONCLUSÃO:")
    print("✅ Integração Education → Training → Reports funcionando!")
    print("✅ Dados fluem entre módulos sem duplicação")
    print("✅ Relatórios consolidados gerados com sucesso")
    print("✅ KPIs calculados automaticamente")


if __name__ == "__main__":
    asyncio.run(simulate_joao_journey())
