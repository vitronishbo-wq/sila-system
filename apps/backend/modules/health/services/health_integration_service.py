"""
Health Integration Service with comprehensive sanitation integration
Handles health statistics, epidemiological data, and cross-module analysis
"""

import json
import statistics
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from modules.health.models.health_integration import (
    AlertStatus,
    DiseaseCategory,
    EpidemiologicalRecord,
    HealthAlert,
    HealthFacility,
    HealthProfessional,
    SeverityLevel,
)
from modules.health.schemas.health_integration import (
    EpidemiologicalRecordCreate,
    HealthImpactAssessment,
    HealthStatistics,
    SanitationHealthCorrelation,
)


class HealthIntegrationService:

    # ============================================================================
    # HEALTH STATISTICS METHODS
    # ============================================================================

    @staticmethod
    def get_municipality_health_statistics(
        db: Session, municipality_id: int
    ) -> HealthStatistics:
        """Get comprehensive health statistics for a municipality"""

        # Get municipality info
        municipality = db.execute(
            "SELECT name FROM municipalities WHERE id = :id", {"id": municipality_id}
        ).fetchone()
        municipality_name = (
            municipality[0] if municipality else f"Municipality {municipality_id}"
        )

        # Get facilities by type
        facilities = (
            db.query(HealthFacility)
            .filter(
                HealthFacility.municipality_id == municipality_id,
                HealthFacility.active == True,
            )
            .all()
        )

        total_facilities = len(facilities)
        facilities_by_type = {}
        total_capacity = 0
        total_occupancy = 0

        for facility in facilities:
            facility_type = facility.facility_type.value
            if facility_type not in facilities_by_type:
                facilities_by_type[facility_type] = 0
            facilities_by_type[facility_type] += 1
            total_capacity += facility.capacity
            total_occupancy += facility.current_occupancy

        # Get health professionals
        professionals = (
            db.query(HealthProfessional)
            .filter(
                HealthProfessional.municipality_id == municipality_id,
                HealthProfessional.active == True,
            )
            .all()
        )

        total_professionals = len(professionals)
        doctors = len([p for p in professionals if p.profession == "doctor"])
        nurses = len([p for p in professionals if p.profession == "nurse"])
        technicians = len([p for p in professionals if p.profession == "technician"])

        # Get disease statistics (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        disease_records = (
            db.query(EpidemiologicalRecord)
            .filter(
                EpidemiologicalRecord.municipality_id == municipality_id,
                EpidemiologicalRecord.period_start >= thirty_days_ago,
            )
            .all()
        )

        waterborne_cases = sum(
            r.cases_reported
            for r in disease_records
            if r.disease_category == DiseaseCategory.WATERBORNE
        )
        vector_borne_cases = sum(
            r.cases_reported
            for r in disease_records
            if r.disease_category == DiseaseCategory.VECTOR_BORNE
        )
        respiratory_cases = sum(
            r.cases_reported
            for r in disease_records
            if r.disease_category == DiseaseCategory.RESPIRATORY
        )
        total_cases = sum(r.cases_reported for r in disease_records)
        total_deaths = sum(r.deaths for r in disease_records)
        sanitation_related_cases = sum(
            r.cases_reported for r in disease_records if r.related_to_sanitation
        )

        # Calculate population ratios (assuming 100,000 population - would be better to get from municipality data)
        estimated_population = 100000
        population_per_doctor = (
            estimated_population / doctors if doctors > 0 else float("inf")
        )
        population_per_nurse = (
            estimated_population / nurses if nurses > 0 else float("inf")
        )
        population_per_facility = (
            estimated_population / total_facilities
            if total_facilities > 0
            else float("inf")
        )

        # Calculate sanitation correlation score
        sanitation_correlation_score = 0.0
        if total_cases > 0:
            sanitation_correlation_score = (sanitation_related_cases / total_cases) * 10

        bed_occupancy_rate = (
            (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
        )

        return HealthStatistics(
            municipality_id=municipality_id,
            municipality_name=municipality_name,
            snapshot_date=datetime.utcnow(),
            total_facilities=total_facilities,
            facilities_by_type=facilities_by_type,
            total_health_professionals=total_professionals,
            doctors=doctors,
            nurses=nurses,
            technicians=technicians,
            hospital_beds=total_capacity,
            occupied_beds=total_occupancy,
            bed_occupancy_rate=bed_occupancy_rate,
            population_per_doctor=population_per_doctor,
            population_per_nurse=population_per_nurse,
            population_per_facility=population_per_facility,
            waterborne_disease_cases=waterborne_cases,
            vector_borne_disease_cases=vector_borne_cases,
            respiratory_disease_cases=respiratory_cases,
            total_disease_cases=total_cases,
            total_deaths=total_deaths,
            sanitation_related_cases=sanitation_related_cases,
            sanitation_correlation_score=sanitation_correlation_score,
        )

    @staticmethod
    def create_health_alert_from_sanitation(
        db: Session,
        municipality_id: int,
        sanitation_incidents: List[Dict],
        alert_creator: str,
    ) -> Optional[HealthAlert]:
        """Create health alert based on sanitation incidents"""

        if not sanitation_incidents:
            return None

        # Analyze incidents to determine health risk
        critical_incidents = [
            i for i in sanitation_incidents if i.get("severity") == "critical"
        ]
        water_related = [
            i
            for i in sanitation_incidents
            if "water" in i.get("incident_type", "").lower()
        ]
        sewage_related = [
            i
            for i in sanitation_incidents
            if "sewage" in i.get("incident_type", "").lower()
        ]

        # Determine alert severity and type
        if len(critical_incidents) > 2:
            severity = SeverityLevel.CRITICAL
            alert_type = "epidemic"
        elif len(critical_incidents) > 0 or len(water_related) > 1:
            severity = SeverityLevel.HIGH
            alert_type = "outbreak"
        else:
            severity = SeverityLevel.MEDIUM
            alert_type = "emergency"

        # Create alert description
        incident_types = list(
            set([i.get("incident_type", "") for i in sanitation_incidents])
        )
        description = f"Health alert generated due to sanitation incidents: {', '.join(incident_types)}. "
        description += f"Total incidents: {len(sanitation_incidents)}, Critical: {len(critical_incidents)}."

        # Estimate affected population
        affected_population = len(sanitation_incidents) * 1000  # Rough estimate

        # Create recommended actions
        recommended_actions = [
            "Increase surveillance for waterborne diseases",
            "Distribute water purification tablets",
            "Issue public health advisory",
            "Coordinate with sanitation teams for rapid response",
        ]

        if len(critical_incidents) > 0:
            recommended_actions.extend(
                [
                    "Activate emergency health response protocol",
                    "Set up temporary health screening points",
                    "Prepare isolation facilities if needed",
                ]
            )

        alert = HealthAlert(
            municipality_id=municipality_id,
            alert_type=alert_type,
            disease_category=DiseaseCategory.WATERBORNE,
            title=f"Sanitation-Related Health Alert - {municipality_id}",
            description=description,
            severity=severity,
            affected_population=affected_population,
            sanitation_related=True,
            related_sanitation_incidents=json.dumps(
                [i.get("incident_id") for i in sanitation_incidents]
            ),
            recommended_actions=json.dumps(recommended_actions),
            created_by=alert_creator,
            created_at=datetime.utcnow(),
            status=AlertStatus.ACTIVE,
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    # ============================================================================
    # EPIDEMIOLOGICAL METHODS
    # ============================================================================

    @staticmethod
    def create_epidemiological_record(
        db: Session, data: EpidemiologicalRecordCreate
    ) -> EpidemiologicalRecord:
        """Create new epidemiological record"""

        record = EpidemiologicalRecord(
            municipality_id=data.municipality_id,
            reporting_facility_id=data.reporting_facility_id,
            disease_name=data.disease_name,
            disease_category=data.disease_category,
            cases_reported=data.cases_reported,
            deaths=data.deaths,
            period_start=data.period_start,
            period_end=data.period_end,
            population_at_risk=data.population_at_risk,
            related_to_sanitation=data.related_to_sanitation,
            sanitation_incident_ids=json.dumps(data.sanitation_incident_ids),
            notes=data.notes,
            reported_by=data.reported_by,
            reported_at=datetime.utcnow(),
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_waterborne_disease_trends(
        db: Session, municipality_id: int, days: int = 90
    ) -> Dict[str, Any]:
        """Get trends for waterborne diseases (key for sanitation integration)"""

        since_date = datetime.utcnow() - timedelta(days=days)

        records = (
            db.query(EpidemiologicalRecord)
            .filter(
                EpidemiologicalRecord.municipality_id == municipality_id,
                EpidemiologicalRecord.disease_category == DiseaseCategory.WATERBORNE,
                EpidemiologicalRecord.period_start >= since_date,
            )
            .order_by(EpidemiologicalRecord.period_start)
            .all()
        )

        # Group by week
        weekly_data = {}
        for record in records:
            week_key = record.period_start.strftime("%Y-W%U")
            if week_key not in weekly_data:
                weekly_data[week_key] = {
                    "cases": 0,
                    "deaths": 0,
                    "sanitation_related": 0,
                }
            weekly_data[week_key]["cases"] += record.cases_reported
            weekly_data[week_key]["deaths"] += record.deaths
            if record.related_to_sanitation:
                weekly_data[week_key]["sanitation_related"] += record.cases_reported

        # Calculate trends
        weeks = sorted(weekly_data.keys())
        if len(weeks) >= 2:
            recent_avg = statistics.mean(
                [weekly_data[w]["cases"] for w in weeks[-4:]]
            )  # Last 4 weeks
            previous_avg = statistics.mean(
                [weekly_data[w]["cases"] for w in weeks[-8:-4]]
            )  # Previous 4 weeks
            trend = (
                "increasing"
                if recent_avg > previous_avg * 1.1
                else "decreasing" if recent_avg < previous_avg * 0.9 else "stable"
            )
        else:
            trend = "insufficient_data"

        total_cases = sum(r.cases_reported for r in records)
        total_deaths = sum(r.deaths for r in records)
        sanitation_related_cases = sum(
            r.cases_reported for r in records if r.related_to_sanitation
        )

        return {
            "municipality_id": municipality_id,
            "period_days": days,
            "total_cases": total_cases,
            "total_deaths": total_deaths,
            "sanitation_related_cases": sanitation_related_cases,
            "sanitation_correlation_percentage": (
                (sanitation_related_cases / total_cases * 100) if total_cases > 0 else 0
            ),
            "trend": trend,
            "weekly_data": weekly_data,
            "most_common_diseases": self._get_most_common_diseases(records),
            "analysis_date": datetime.utcnow(),
        }

    @staticmethod
    def _get_most_common_diseases(
        records: List[EpidemiologicalRecord],
    ) -> List[Dict[str, Any]]:
        """Helper method to get most common diseases from records"""
        disease_counts = {}
        for record in records:
            disease = record.disease_name
            if disease not in disease_counts:
                disease_counts[disease] = {
                    "cases": 0,
                    "deaths": 0,
                    "sanitation_related": 0,
                }
            disease_counts[disease]["cases"] += record.cases_reported
            disease_counts[disease]["deaths"] += record.deaths
            if record.related_to_sanitation:
                disease_counts[disease]["sanitation_related"] += record.cases_reported

        # Sort by cases and return top 10
        sorted_diseases = sorted(
            disease_counts.items(), key=lambda x: x[1]["cases"], reverse=True
        )
        return [{"disease": disease, **data} for disease, data in sorted_diseases[:10]]

    # ============================================================================
    # CROSS-MODULE INTEGRATION METHODS
    # ============================================================================

    @staticmethod
    def analyze_sanitation_health_correlation(
        db: Session, municipality_id: int, sanitation_data: Dict[str, Any]
    ) -> SanitationHealthCorrelation:
        """Analyze correlation between sanitation indicators and health outcomes"""

        # Get health data
        health_stats = HealthIntegrationService.get_municipality_health_statistics(
            db, municipality_id
        )
        waterborne_trends = HealthIntegrationService.get_waterborne_disease_trends(
            db, municipality_id, 90
        )

        # Extract sanitation indicators
        water_coverage = sanitation_data.get("water_coverage_percentage", 0)
        sewage_coverage = sanitation_data.get("sewage_coverage_percentage", 0)
        active_incidents = sanitation_data.get("total_incidents", 0)
        critical_incidents = sanitation_data.get("critical_incidents", 0)

        # Calculate correlation coefficient (simplified)
        # In a real implementation, you'd use proper statistical correlation
        sanitation_score = (water_coverage + sewage_coverage) / 2 - (
            critical_incidents * 10
        )
        health_score = 100 - (health_stats.waterborne_disease_cases / 10)  # Simplified

        # Normalize and calculate correlation
        correlation_coefficient = max(
            -1, min(1, (sanitation_score - health_score) / 100)
        )

        # Determine correlation strength
        abs_corr = abs(correlation_coefficient)
        if abs_corr < 0.1:
            correlation_strength = "none"
        elif abs_corr < 0.3:
            correlation_strength = "weak"
        elif abs_corr < 0.5:
            correlation_strength = "moderate"
        elif abs_corr < 0.7:
            correlation_strength = "strong"
        else:
            correlation_strength = "very_strong"

        # Risk assessment
        if health_stats.waterborne_disease_cases > 100 and water_coverage < 50:
            risk_assessment = "critical"
        elif health_stats.waterborne_disease_cases > 50 and water_coverage < 70:
            risk_assessment = "high"
        elif health_stats.waterborne_disease_cases > 20 or water_coverage < 80:
            risk_assessment = "medium"
        else:
            risk_assessment = "low"

        # Generate recommendations
        immediate_actions = []
        medium_term_actions = []
        long_term_actions = []

        if critical_incidents > 0:
            immediate_actions.extend(
                [
                    "Address critical sanitation incidents immediately",
                    "Increase health surveillance in affected areas",
                    "Distribute emergency water supplies if needed",
                ]
            )

        if water_coverage < 80:
            medium_term_actions.append("Expand water supply infrastructure")

        if sewage_coverage < 70:
            medium_term_actions.append("Improve sewage treatment capacity")

        if health_stats.waterborne_disease_cases > 50:
            immediate_actions.append("Implement enhanced disease surveillance")
            medium_term_actions.append("Strengthen primary healthcare capacity")

        long_term_actions.extend(
            [
                "Develop integrated sanitation-health monitoring system",
                "Implement community health education programs",
                "Establish early warning system for disease outbreaks",
            ]
        )

        return SanitationHealthCorrelation(
            municipality_id=municipality_id,
            correlation_period_days=90,
            water_coverage_percentage=water_coverage,
            sewage_coverage_percentage=sewage_coverage,
            active_sanitation_incidents=active_incidents,
            critical_sanitation_incidents=critical_incidents,
            waterborne_disease_cases=health_stats.waterborne_disease_cases,
            waterborne_disease_rate_per_100k=(
                health_stats.waterborne_disease_cases / 1000
            ),  # Assuming 100k population
            total_health_alerts=len(
                db.query(HealthAlert)
                .filter(
                    HealthAlert.municipality_id == municipality_id,
                    HealthAlert.status == AlertStatus.ACTIVE,
                )
                .all()
            ),
            sanitation_related_alerts=len(
                db.query(HealthAlert)
                .filter(
                    HealthAlert.municipality_id == municipality_id,
                    HealthAlert.sanitation_related == True,
                    HealthAlert.status == AlertStatus.ACTIVE,
                )
                .all()
            ),
            correlation_coefficient=correlation_coefficient,
            correlation_strength=correlation_strength,
            risk_assessment=risk_assessment,
            immediate_actions=immediate_actions,
            medium_term_actions=medium_term_actions,
            long_term_actions=long_term_actions,
            analysis_date=datetime.utcnow(),
        )

    @staticmethod
    def assess_health_impact_of_sanitation_issues(
        db: Session, municipality_id: int, sanitation_incidents: List[Dict]
    ) -> HealthImpactAssessment:
        """Assess potential health impact of sanitation issues"""

        # Estimate population at risk based on incident locations and severity
        population_at_risk = 0
        high_risk_areas = []

        for incident in sanitation_incidents:
            severity = incident.get("severity", "low")
            location = incident.get("location", "Unknown")

            # Estimate affected population based on incident type and severity
            if severity == "critical":
                affected_pop = 5000
            elif severity == "high":
                affected_pop = 2000
            elif severity == "medium":
                affected_pop = 1000
            else:
                affected_pop = 500

            population_at_risk += affected_pop

            if severity in ["critical", "high"]:
                high_risk_areas.append(location)

        # Get current health capacity
        health_stats = HealthIntegrationService.get_municipality_health_statistics(
            db, municipality_id
        )

        # Estimate additional cases based on historical data and risk factors
        # This is a simplified model - in reality you'd use epidemiological models
        base_attack_rate = 0.05  # 5% of at-risk population may become ill
        severity_multiplier = 1.0

        critical_incidents = len(
            [i for i in sanitation_incidents if i.get("severity") == "critical"]
        )
        if critical_incidents > 2:
            severity_multiplier = 2.0
        elif critical_incidents > 0:
            severity_multiplier = 1.5

        estimated_additional_cases = int(
            population_at_risk * base_attack_rate * severity_multiplier
        )
        estimated_additional_deaths = int(
            estimated_additional_cases * 0.02
        )  # 2% case fatality rate

        # Calculate healthcare capacity strain
        current_occupancy = health_stats.occupied_beds
        total_capacity = health_stats.hospital_beds
        additional_bed_need = (
            estimated_additional_cases * 0.1
        )  # 10% may need hospitalization

        healthcare_strain = (
            min(100, ((current_occupancy + additional_bed_need) / total_capacity * 100))
            if total_capacity > 0
            else 100
        )

        # Generate interventions and recommendations
        health_interventions = [
            "Activate disease surveillance system",
            "Prepare additional hospital beds",
            "Stock oral rehydration salts",
            "Train healthcare workers on outbreak response",
        ]

        sanitation_improvements = [
            "Repair critical water supply issues",
            "Address sewage overflow problems",
            "Improve waste collection in affected areas",
            "Provide temporary clean water sources",
        ]

        if estimated_additional_cases > 100:
            health_interventions.extend(
                [
                    "Set up temporary treatment centers",
                    "Request additional medical supplies",
                    "Coordinate with regional health authorities",
                ]
            )

        if critical_incidents > 1:
            sanitation_improvements.extend(
                [
                    "Deploy emergency sanitation teams",
                    "Implement water quality testing",
                    "Set up emergency latrines if needed",
                ]
            )

        # Estimate intervention cost
        base_cost_per_case = 50  # USD
        sanitation_repair_cost = len(sanitation_incidents) * 1000  # USD per incident
        estimated_cost = (
            estimated_additional_cases * base_cost_per_case
        ) + sanitation_repair_cost

        return HealthImpactAssessment(
            municipality_id=municipality_id,
            assessment_date=datetime.utcnow(),
            population_at_risk=population_at_risk,
            high_risk_areas=list(set(high_risk_areas)),
            vulnerable_populations=[
                "Children under 5",
                "Elderly",
                "Pregnant women",
                "Immunocompromised",
            ],
            estimated_additional_cases_30_days=estimated_additional_cases,
            estimated_additional_deaths_30_days=estimated_additional_deaths,
            healthcare_capacity_strain=healthcare_strain,
            required_health_interventions=health_interventions,
            required_sanitation_improvements=sanitation_improvements,
            estimated_intervention_cost_usd=estimated_cost,
            surveillance_areas=list(set(high_risk_areas)),
            monitoring_frequency="daily" if critical_incidents > 0 else "weekly",
            key_indicators_to_track=[
                "New diarrheal disease cases",
                "Water quality test results",
                "Hospital bed occupancy",
                "Sanitation incident resolution status",
            ],
        )
