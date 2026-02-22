"""
Urbanism Integration Service with comprehensive sanitation and health integration
Handles urban planning, infrastructure management, and cross-module coordination
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from modules.urbanism.models.urbanism_integration import (
    CrossModuleIntegrationLog,
    InfrastructureAsset,
    InfrastructureCondition,
    PermitStatus,
    UrbanPermit,
    UrbanZone,
)
from modules.urbanism.schemas.urbanism_integration import (
    UrbanDevelopmentImpactAnalysis,
    UrbanPermitCreate,
    UrbanPlanningIntegrationSummary,
    UrbanZoneCreate,
)


class UrbanismIntegrationService:

    # ============================================================================
    # URBAN ZONE MANAGEMENT METHODS
    # ============================================================================

    @staticmethod
    def create_urban_zone(db: Session, data: UrbanZoneCreate) -> UrbanZone:
        """Create a new urban zone with integration capabilities"""

        zone = UrbanZone(
            municipality_id=data.municipality_id,
            zone_name=data.zone_name,
            zone_type=data.zone_type,
            area_hectares=data.area_hectares,
            population_density=data.population_density,
            planned_population=data.planned_population,
            current_population=data.current_population,
            coordinates=json.dumps(data.coordinates) if data.coordinates else None,
            zoning_regulations=(
                json.dumps(data.zoning_regulations) if data.zoning_regulations else None
            ),
            environmental_constraints=(
                json.dumps(data.environmental_constraints)
                if data.environmental_constraints
                else None
            ),
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow(),
        )

        db.add(zone)
        db.commit()
        db.refresh(zone)
        return zone

    @staticmethod
    def get_zones_needing_sanitation_assessment(
        db: Session, municipality_id: int
    ) -> List[Dict[str, Any]]:
        """Get urban zones that need sanitation infrastructure assessment"""

        zones = (
            db.query(UrbanZone)
            .filter(
                UrbanZone.municipality_id == municipality_id,
                or_(
                    UrbanZone.sanitation_infrastructure == False,
                    UrbanZone.water_coverage_percentage < 80,
                    UrbanZone.sewage_coverage_percentage < 70,
                ),
            )
            .all()
        )

        assessment_needed = []
        for zone in zones:
            priority_score = 0
            issues = []

            if not zone.sanitation_infrastructure:
                priority_score += 3
                issues.append("No sanitation infrastructure")

            if zone.water_coverage_percentage < 50:
                priority_score += 2
                issues.append("Low water coverage")
            elif zone.water_coverage_percentage < 80:
                priority_score += 1
                issues.append("Moderate water coverage")

            if zone.sewage_coverage_percentage < 50:
                priority_score += 2
                issues.append("Low sewage coverage")
            elif zone.sewage_coverage_percentage < 70:
                priority_score += 1
                issues.append("Moderate sewage coverage")

            if zone.current_population and zone.planned_population:
                growth_rate = (
                    zone.planned_population - zone.current_population
                ) / zone.current_population
                if growth_rate > 0.5:  # 50% growth
                    priority_score += 2
                    issues.append("High population growth expected")

            assessment_needed.append(
                {
                    "zone_id": zone.id,
                    "zone_name": zone.zone_name,
                    "zone_type": zone.zone_type.value,
                    "priority_score": priority_score,
                    "priority_level": (
                        "critical"
                        if priority_score >= 5
                        else "high" if priority_score >= 3 else "medium"
                    ),
                    "issues": issues,
                    "current_population": zone.current_population,
                    "planned_population": zone.planned_population,
                    "area_hectares": zone.area_hectares,
                }
            )

        # Sort by priority score
        assessment_needed.sort(key=lambda x: x["priority_score"], reverse=True)
        return assessment_needed

    @staticmethod
    def get_zones_needing_health_facilities(
        db: Session, municipality_id: int
    ) -> List[Dict[str, Any]]:
        """Get urban zones that need additional health facilities"""

        zones = (
            db.query(UrbanZone)
            .filter(
                UrbanZone.municipality_id == municipality_id,
                or_(
                    UrbanZone.health_facilities_needed
                    > UrbanZone.health_facilities_count,
                    UrbanZone.healthcare_accessibility_score < 5.0,
                ),
            )
            .all()
        )

        health_needs = []
        for zone in zones:
            facilities_deficit = max(
                0, zone.health_facilities_needed - zone.health_facilities_count
            )

            # Calculate urgency based on population and accessibility
            urgency_score = 0
            if facilities_deficit > 2:
                urgency_score += 3
            elif facilities_deficit > 0:
                urgency_score += 2

            if zone.healthcare_accessibility_score < 3:
                urgency_score += 3
            elif zone.healthcare_accessibility_score < 5:
                urgency_score += 2
            elif zone.healthcare_accessibility_score < 7:
                urgency_score += 1

            if zone.current_population and zone.current_population > 10000:
                urgency_score += 1

            health_needs.append(
                {
                    "zone_id": zone.id,
                    "zone_name": zone.zone_name,
                    "zone_type": zone.zone_type.value,
                    "facilities_deficit": facilities_deficit,
                    "accessibility_score": zone.healthcare_accessibility_score,
                    "urgency_score": urgency_score,
                    "urgency_level": (
                        "critical"
                        if urgency_score >= 6
                        else "high" if urgency_score >= 4 else "medium"
                    ),
                    "current_population": zone.current_population,
                    "population_density": zone.population_density,
                }
            )

        health_needs.sort(key=lambda x: x["urgency_score"], reverse=True)
        return health_needs

    # ============================================================================
    # PERMIT MANAGEMENT WITH INTEGRATION
    # ============================================================================

    @staticmethod
    def create_permit_with_integration_assessment(
        db: Session, data: UrbanPermitCreate
    ) -> Dict[str, Any]:
        """Create permit and automatically assess integration requirements"""

        # Generate unique permit number
        permit_number = f"UP-{data.municipality_id}-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

        # Assess integration requirements based on permit details
        integration_requirements = (
            UrbanismIntegrationService._assess_permit_integration_requirements(db, data)
        )

        permit = UrbanPermit(
            municipality_id=data.municipality_id,
            zone_id=data.zone_id,
            permit_type=data.permit_type,
            permit_number=permit_number,
            applicant_name=data.applicant_name,
            applicant_contact=data.applicant_contact,
            project_description=data.project_description,
            location=data.location,
            area_affected=data.area_affected,
            estimated_cost=data.estimated_cost,
            estimated_population_impact=data.estimated_population_impact,
            requires_sanitation_study=integration_requirements[
                "requires_sanitation_study"
            ],
            requires_health_impact_assessment=integration_requirements[
                "requires_health_impact_assessment"
            ],
            requires_environmental_clearance=data.requires_environmental_clearance,
            status=PermitStatus.PENDING,
            submitted_at=datetime.utcnow(),
        )

        db.add(permit)
        db.commit()
        db.refresh(permit)

        # Log integration assessment
        UrbanismIntegrationService._log_integration_event(
            db,
            data.municipality_id,
            "permit_integration_assessment",
            "urbanism",
            ["sanitation", "health"],
            "permit_submitted",
            {"permit_id": permit.id},
            "integration_requirements_assessed",
            integration_requirements,
        )

        return {
            "permit": permit,
            "integration_requirements": integration_requirements,
            "next_steps": integration_requirements["next_steps"],
        }

    @staticmethod
    def _assess_permit_integration_requirements(
        db: Session, data: UrbanPermitCreate
    ) -> Dict[str, Any]:
        """Assess what integration studies are required for a permit"""

        requires_sanitation_study = data.requires_sanitation_study
        requires_health_assessment = data.requires_health_impact_assessment
        next_steps = []

        # Automatic assessment based on project characteristics
        if data.estimated_population_impact and data.estimated_population_impact > 100:
            requires_sanitation_study = True
            requires_health_assessment = True
            next_steps.append("Large population impact requires comprehensive studies")

        if data.area_affected > 10000:  # 1 hectare
            requires_sanitation_study = True
            next_steps.append("Large area development requires sanitation assessment")

        if (
            data.permit_type.value in ["construction", "land_use"]
            and data.estimated_cost
            and data.estimated_cost > 100000
        ):
            requires_sanitation_study = True
            requires_health_assessment = True
            next_steps.append("High-value development requires impact assessments")

        # Check zone-specific requirements
        if data.zone_id:
            zone = db.query(UrbanZone).filter(UrbanZone.id == data.zone_id).first()
            if zone:
                if (
                    not zone.sanitation_infrastructure
                    or zone.water_coverage_percentage < 80
                ):
                    requires_sanitation_study = True
                    next_steps.append("Zone has inadequate sanitation infrastructure")

                if zone.health_facilities_count < zone.health_facilities_needed:
                    requires_health_assessment = True
                    next_steps.append("Zone has insufficient health facilities")

        return {
            "requires_sanitation_study": requires_sanitation_study,
            "requires_health_impact_assessment": requires_health_assessment,
            "assessment_rationale": next_steps,
            "next_steps": (
                next_steps if next_steps else ["Standard permit review process"]
            ),
        }

    # ============================================================================
    # INFRASTRUCTURE MANAGEMENT
    # ============================================================================

    @staticmethod
    def get_infrastructure_integration_status(
        db: Session, municipality_id: int
    ) -> Dict[str, Any]:
        """Get status of infrastructure integration with sanitation and health"""

        infrastructure = (
            db.query(InfrastructureAsset)
            .filter(
                InfrastructureAsset.municipality_id == municipality_id,
                InfrastructureAsset.active == True,
            )
            .all()
        )

        total_assets = len(infrastructure)
        sanitation_connected = len(
            [i for i in infrastructure if i.connects_to_sanitation]
        )
        health_serving = len([i for i in infrastructure if i.serves_health_facilities])
        critical_condition = len(
            [
                i
                for i in infrastructure
                if i.condition == InfrastructureCondition.CRITICAL
            ]
        )
        emergency_critical = len(
            [i for i in infrastructure if i.emergency_access_critical]
        )

        # Group by type
        by_type = {}
        for asset in infrastructure:
            asset_type = asset.infrastructure_type.value
            if asset_type not in by_type:
                by_type[asset_type] = {
                    "total": 0,
                    "sanitation_connected": 0,
                    "health_serving": 0,
                    "critical_condition": 0,
                    "emergency_critical": 0,
                }
            by_type[asset_type]["total"] += 1
            if asset.connects_to_sanitation:
                by_type[asset_type]["sanitation_connected"] += 1
            if asset.serves_health_facilities:
                by_type[asset_type]["health_serving"] += 1
            if asset.condition == InfrastructureCondition.CRITICAL:
                by_type[asset_type]["critical_condition"] += 1
            if asset.emergency_access_critical:
                by_type[asset_type]["emergency_critical"] += 1

        # Calculate integration scores
        sanitation_integration_score = (
            (sanitation_connected / total_assets * 10) if total_assets > 0 else 0
        )
        health_integration_score = (
            (health_serving / total_assets * 10) if total_assets > 0 else 0
        )

        # Identify priority maintenance needs
        priority_maintenance = []
        for asset in infrastructure:
            if asset.condition == InfrastructureCondition.CRITICAL:
                priority_maintenance.append(
                    {
                        "asset_id": asset.id,
                        "asset_name": asset.asset_name,
                        "type": asset.infrastructure_type.value,
                        "location": asset.location,
                        "sanitation_connected": asset.connects_to_sanitation,
                        "health_serving": asset.serves_health_facilities,
                        "emergency_critical": asset.emergency_access_critical,
                    }
                )

        return {
            "municipality_id": municipality_id,
            "total_infrastructure_assets": total_assets,
            "sanitation_connected_assets": sanitation_connected,
            "health_serving_assets": health_serving,
            "critical_condition_assets": critical_condition,
            "emergency_critical_assets": emergency_critical,
            "sanitation_integration_percentage": (
                (sanitation_connected / total_assets * 100) if total_assets > 0 else 0
            ),
            "health_integration_percentage": (
                (health_serving / total_assets * 100) if total_assets > 0 else 0
            ),
            "sanitation_integration_score": sanitation_integration_score,
            "health_integration_score": health_integration_score,
            "by_infrastructure_type": by_type,
            "priority_maintenance_needs": priority_maintenance,
            "assessment_date": datetime.utcnow(),
        }

    # ============================================================================
    # CROSS-MODULE INTEGRATION ANALYSIS
    # ============================================================================

    @staticmethod
    def analyze_development_impact(
        db: Session, municipality_id: int, development_data: Dict[str, Any]
    ) -> UrbanDevelopmentImpactAnalysis:
        """Analyze impact of urban development on sanitation and health systems"""

        # Extract development parameters
        planned_population = development_data.get("planned_population_increase", 0)
        planned_area = development_data.get("planned_area_development", 0)
        timeline_months = development_data.get("development_timeline_months", 24)

        # Calculate sanitation impact
        water_demand_per_person = 200  # liters per day
        sewage_generation_per_person = 150  # liters per day
        waste_generation_per_person = 1.2  # kg per day

        additional_water_demand = planned_population * water_demand_per_person
        additional_sewage = planned_population * sewage_generation_per_person
        additional_waste = (
            planned_population * waste_generation_per_person / 1000
        )  # tons

        # Assess current sanitation capacity
        current_zones = (
            db.query(UrbanZone)
            .filter(UrbanZone.municipality_id == municipality_id)
            .all()
        )

        avg_water_coverage = (
            sum(z.water_coverage_percentage for z in current_zones) / len(current_zones)
            if current_zones
            else 0
        )
        avg_sewage_coverage = (
            sum(z.sewage_coverage_percentage for z in current_zones)
            / len(current_zones)
            if current_zones
            else 0
        )

        if avg_water_coverage < 60 or avg_sewage_coverage < 50:
            sanitation_adequacy = "critical"
        elif avg_water_coverage < 80 or avg_sewage_coverage < 70:
            sanitation_adequacy = "insufficient"
        else:
            sanitation_adequacy = "adequate"

        # Calculate required sanitation investments
        sanitation_investments = []
        if sanitation_adequacy != "adequate":
            water_investment = additional_water_demand * 2  # $2 per liter/day capacity
            sewage_investment = additional_sewage * 3  # $3 per liter/day capacity
            waste_investment = additional_waste * 365 * 500  # $500 per ton/day capacity

            sanitation_investments = [
                {
                    "type": "water_supply_expansion",
                    "cost_usd": water_investment,
                    "priority": "high",
                },
                {
                    "type": "sewage_treatment_expansion",
                    "cost_usd": sewage_investment,
                    "priority": "high",
                },
                {
                    "type": "waste_collection_enhancement",
                    "cost_usd": waste_investment,
                    "priority": "medium",
                },
            ]

        # Calculate health impact
        people_per_health_facility = 5000  # WHO recommendation
        required_facilities = max(1, planned_population // people_per_health_facility)

        # Assess healthcare accessibility impact
        if planned_population > 10000:
            accessibility_impact = "negative"  # Will strain existing services
        elif planned_population > 5000:
            accessibility_impact = "neutral"
        else:
            accessibility_impact = "positive"

        health_facilities_needed = [
            {
                "type": "health_post",
                "quantity": max(1, required_facilities),
                "cost_usd": required_facilities * 50000,
            },
            {
                "type": "ambulance_service",
                "quantity": 1 if planned_population > 5000 else 0,
                "cost_usd": 100000 if planned_population > 5000 else 0,
            },
        ]

        # Public health risk factors
        risk_factors = []
        if sanitation_adequacy == "critical":
            risk_factors.extend(["Waterborne disease risk", "Vector breeding sites"])
        if (
            planned_population > current_zones[0].current_population
            if current_zones
            else 0
        ):
            risk_factors.append("Healthcare system strain")
        if planned_area > 100:  # hectares
            risk_factors.append("Environmental health impacts")

        # Infrastructure impact assessment
        current_infrastructure = (
            db.query(InfrastructureAsset)
            .filter(
                InfrastructureAsset.municipality_id == municipality_id,
                InfrastructureAsset.active == True,
            )
            .all()
        )

        critical_infrastructure = len(
            [
                i
                for i in current_infrastructure
                if i.condition == InfrastructureCondition.CRITICAL
            ]
        )

        road_impact = (
            "inadequate"
            if critical_infrastructure > 5
            else "strained" if critical_infrastructure > 2 else "adequate"
        )
        utility_impact = (
            "inadequate"
            if avg_water_coverage < 60
            else "strained" if avg_water_coverage < 80 else "adequate"
        )

        # Calculate total investment
        sanitation_investment_total = sum(
            inv["cost_usd"] for inv in sanitation_investments
        )
        health_investment_total = sum(
            fac["cost_usd"] for fac in health_facilities_needed
        )
        infrastructure_investment = (
            critical_infrastructure * 100000
        )  # $100k per critical asset
        total_investment = (
            sanitation_investment_total
            + health_investment_total
            + infrastructure_investment
        )

        # Generate recommendations
        recommendations = []
        if sanitation_adequacy != "adequate":
            recommendations.append(
                "Prioritize sanitation infrastructure before development"
            )
        if accessibility_impact == "negative":
            recommendations.append(
                "Plan additional health facilities in development phase"
            )
        if road_impact != "adequate":
            recommendations.append("Upgrade road infrastructure to support development")

        phasing_recommendations = [
            "Phase 1: Infrastructure preparation (sanitation, roads)",
            "Phase 2: Core development with basic services",
            "Phase 3: Community facilities (health, education)",
            "Phase 4: Final development and service optimization",
        ]

        return UrbanDevelopmentImpactAnalysis(
            municipality_id=municipality_id,
            analysis_date=datetime.utcnow(),
            planned_population_increase=planned_population,
            planned_area_development=planned_area,
            development_timeline_months=timeline_months,
            additional_water_demand_liters_per_day=additional_water_demand,
            additional_sewage_generation_liters_per_day=additional_sewage,
            additional_waste_generation_tons_per_day=additional_waste,
            sanitation_infrastructure_adequacy=sanitation_adequacy,
            required_sanitation_investments=sanitation_investments,
            additional_healthcare_demand=required_facilities,
            healthcare_accessibility_impact=accessibility_impact,
            required_health_facilities=health_facilities_needed,
            public_health_risk_factors=risk_factors,
            road_network_impact=road_impact,
            utility_network_impact=utility_impact,
            required_infrastructure_upgrades=[
                {
                    "type": "road_maintenance",
                    "cost_usd": infrastructure_investment * 0.6,
                },
                {
                    "type": "utility_upgrades",
                    "cost_usd": infrastructure_investment * 0.4,
                },
            ],
            total_investment_required_usd=total_investment,
            sanitation_investment_usd=sanitation_investment_total,
            health_investment_usd=health_investment_total,
            infrastructure_investment_usd=infrastructure_investment,
            development_recommendations=recommendations,
            phasing_recommendations=phasing_recommendations,
            risk_mitigation_measures=[
                "Implement phased development approach",
                "Establish health and sanitation monitoring",
                "Create emergency response protocols",
                "Ensure community participation in planning",
            ],
        )

    @staticmethod
    def generate_integration_summary(
        db: Session, municipality_id: int
    ) -> UrbanPlanningIntegrationSummary:
        """Generate comprehensive integration summary for municipality"""

        # Get current status
        zones = (
            db.query(UrbanZone)
            .filter(UrbanZone.municipality_id == municipality_id)
            .all()
        )
        permits = (
            db.query(UrbanPermit)
            .filter(
                UrbanPermit.municipality_id == municipality_id,
                UrbanPermit.status == PermitStatus.PENDING,
            )
            .all()
        )
        infrastructure = (
            db.query(InfrastructureAsset)
            .filter(
                InfrastructureAsset.municipality_id == municipality_id,
                InfrastructureAsset.active == True,
            )
            .all()
        )

        total_zones = len(zones)
        zones_adequate_sanitation = len(
            [
                z
                for z in zones
                if z.sanitation_infrastructure and z.water_coverage_percentage > 80
            ]
        )
        zones_adequate_health = len(
            [
                z
                for z in zones
                if z.health_facilities_count >= z.health_facilities_needed
            ]
        )

        permits_needing_studies = len(
            [
                p
                for p in permits
                if p.requires_sanitation_study or p.requires_health_impact_assessment
            ]
        )

        total_infrastructure = len(infrastructure)
        good_condition_infrastructure = len(
            [
                i
                for i in infrastructure
                if i.condition
                in [InfrastructureCondition.EXCELLENT, InfrastructureCondition.GOOD]
            ]
        )
        maintenance_needed = len(
            [
                i
                for i in infrastructure
                if i.condition
                in [
                    InfrastructureCondition.FAIR,
                    InfrastructureCondition.POOR,
                    InfrastructureCondition.CRITICAL,
                ]
            ]
        )
        sanitation_connected = len(
            [i for i in infrastructure if i.connects_to_sanitation]
        )
        health_serving = len([i for i in infrastructure if i.serves_health_facilities])

        # Development pipeline
        approved_permits = (
            db.query(UrbanPermit)
            .filter(
                UrbanPermit.municipality_id == municipality_id,
                UrbanPermit.status == PermitStatus.APPROVED,
                UrbanPermit.approved_at >= datetime.utcnow() - timedelta(days=365),
            )
            .all()
        )

        estimated_growth = sum(
            p.estimated_population_impact or 0 for p in approved_permits
        )

        # Calculate integration scores
        sanitation_score = (
            (zones_adequate_sanitation / total_zones * 10) if total_zones > 0 else 0
        )
        health_score = (
            (zones_adequate_health / total_zones * 10) if total_zones > 0 else 0
        )
        overall_score = (sanitation_score + health_score) / 2

        # Identify challenges and opportunities
        challenges = []
        opportunities = []

        if zones_adequate_sanitation / total_zones < 0.7 if total_zones > 0 else True:
            challenges.append("Inadequate sanitation coverage in multiple zones")
        if zones_adequate_health / total_zones < 0.8 if total_zones > 0 else True:
            challenges.append("Insufficient health facility coverage")
        if (
            maintenance_needed / total_infrastructure > 0.3
            if total_infrastructure > 0
            else True
        ):
            challenges.append("High infrastructure maintenance backlog")

        if permits_needing_studies > 0:
            opportunities.append("Integration studies can improve planning")
        if estimated_growth > 0:
            opportunities.append("Population growth enables infrastructure investment")

        priority_actions = []
        if sanitation_score < 5:
            priority_actions.append("Accelerate sanitation infrastructure development")
        if health_score < 5:
            priority_actions.append("Expand health facility network")
        if overall_score < 6:
            priority_actions.append("Implement integrated planning approach")

        return UrbanPlanningIntegrationSummary(
            municipality_id=municipality_id,
            summary_date=datetime.utcnow(),
            total_urban_zones=total_zones,
            zones_with_adequate_sanitation=zones_adequate_sanitation,
            zones_with_adequate_health_access=zones_adequate_health,
            pending_permits_requiring_integration_studies=permits_needing_studies,
            infrastructure_assets_total=total_infrastructure,
            infrastructure_assets_good_condition=good_condition_infrastructure,
            infrastructure_assets_needing_maintenance=maintenance_needed,
            sanitation_connected_infrastructure=sanitation_connected,
            health_serving_infrastructure=health_serving,
            approved_developments_next_12_months=len(approved_permits),
            estimated_population_growth_next_5_years=estimated_growth,
            required_sanitation_capacity_increase_percentage=max(
                0, (estimated_growth * 0.2)
            ),  # 20% buffer
            required_health_facilities_increase=max(0, estimated_growth // 5000),
            sanitation_urbanism_integration_score=sanitation_score,
            health_urbanism_integration_score=health_score,
            overall_integration_maturity_score=overall_score,
            main_integration_challenges=challenges,
            integration_opportunities=opportunities,
            priority_actions=priority_actions,
        )

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    @staticmethod
    def _log_integration_event(
        db: Session,
        municipality_id: int,
        integration_type: str,
        source_module: str,
        target_modules: List[str],
        trigger_event: str,
        trigger_data: Dict[str, Any],
        integration_action: str,
        action_result: Dict[str, Any],
    ):
        """Log cross-module integration events for audit and analysis"""

        for target_module in target_modules:
            log_entry = CrossModuleIntegrationLog(
                municipality_id=municipality_id,
                integration_type=integration_type,
                source_module=source_module,
                target_module=target_module,
                trigger_event=trigger_event,
                trigger_data=json.dumps(trigger_data),
                integration_action=integration_action,
                action_result=json.dumps(action_result),
                success=True,
                processing_time_ms=100,  # Would measure actual time
                created_at=datetime.utcnow(),
            )
            db.add(log_entry)

        db.commit()
