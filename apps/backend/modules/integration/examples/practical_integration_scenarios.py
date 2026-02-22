"""
Practical Integration Scenarios - Sanitation + Health + Urbanism
Real-world examples demonstrating cross-module integration workflows
"""


class IntegrationScenarios:
    """
    Practical examples of Sanitation + Health + Urbanism integration
    Based on real municipal challenges in Angola
    """

    @staticmethod
    def scenario_municipality_x_water_crisis():
        """
        Scenario: Municipality X - Water Supply Crisis
        Flow: Sanitation → Health → Urbanism
        """
        return {
            "scenario_name": "Municipality X Water Supply Crisis",
            "municipality_id": 1,
            "scenario_type": "sanitation_health_urbanism",
            "timeline": "7 days",
            "description": "20% water coverage drop leads to disease outbreak requiring urban planning review",
            # Day 1: Sanitation incident reported
            "day_1_sanitation_incident": {
                "incident_type": "water_shortage",
                "location": "Bairro Central",
                "severity": "critical",
                "description": "Main water pump failure affecting 15,000 residents",
                "reported_by": "Municipal Water Department",
                "estimated_population_affected": 15000,
            },
            # Day 2: Health impact detected
            "day_2_health_alert": {
                "alert_type": "outbreak",
                "disease_category": "waterborne",
                "title": "Diarrheal Disease Increase - Bairro Central",
                "cases_reported": 45,
                "severity": "high",
                "sanitation_related": True,
                "recommended_actions": [
                    "Distribute water purification tablets",
                    "Set up temporary water distribution points",
                    "Increase surveillance for cholera/typhoid",
                ],
            },
            # Day 3-5: Cross-module coordination
            "coordination_response": {
                "sanitation_actions": [
                    "Deploy emergency water trucks",
                    "Repair main pump system",
                    "Test water quality in affected areas",
                ],
                "health_actions": [
                    "Establish temporary health screening",
                    "Distribute ORS packets",
                    "Monitor disease trends",
                ],
                "urbanism_actions": [
                    "Review water infrastructure capacity",
                    "Assess backup system adequacy",
                    "Plan redundant water supply routes",
                ],
            },
            # Day 6-7: Long-term planning
            "integration_outcomes": {
                "immediate_resolution": "Water supply restored, outbreak contained",
                "lessons_learned": [
                    "Need backup water systems in high-density areas",
                    "Health surveillance must be linked to infrastructure status",
                    "Urban planning should include infrastructure resilience",
                ],
                "policy_changes": [
                    "Mandatory backup water systems for zones >10k people",
                    "Real-time health-sanitation data sharing protocol",
                    "Infrastructure condition monitoring system",
                ],
                "investment_approved": 250000,  # USD for infrastructure upgrades
            },
        }

    @staticmethod
    def scenario_new_residential_development():
        """
        Scenario: New Residential Development Assessment
        Flow: Urbanism → Sanitation → Health
        """
        return {
            "scenario_name": "Bairro Novo Residential Development",
            "municipality_id": 2,
            "scenario_type": "urbanism_sanitation_health",
            "timeline": "90 days",
            "description": "5,000-person residential development requires integrated infrastructure planning",
            # Week 1: Development permit submitted
            "permit_application": {
                "permit_type": "construction",
                "applicant_name": "Construtora Luanda Lda",
                "project_description": "500-unit residential complex with commercial area",
                "area_affected": 25.5,  # hectares
                "estimated_population_impact": 5000,
                "estimated_cost": 2500000,  # USD
                "requires_sanitation_study": True,
                "requires_health_impact_assessment": True,
            },
            # Week 2-4: Integration assessments
            "sanitation_assessment": {
                "current_water_coverage": 65,  # percentage
                "current_sewage_coverage": 45,  # percentage
                "additional_water_demand": 1000000,  # liters/day
                "additional_sewage_generation": 750000,  # liters/day
                "infrastructure_adequacy": "insufficient",
                "required_investments": [
                    {"type": "water_supply_expansion", "cost_usd": 400000},
                    {"type": "sewage_treatment_plant", "cost_usd": 600000},
                    {"type": "distribution_network", "cost_usd": 200000},
                ],
            },
            "health_assessment": {
                "current_health_facilities": 2,
                "facilities_needed": 1,  # Additional health post
                "estimated_healthcare_demand_increase": 25,  # percentage
                "risk_factors": [
                    "Increased population density",
                    "Potential sanitation system strain",
                    "Limited emergency access routes",
                ],
                "required_health_investments": [
                    {"type": "health_post_construction", "cost_usd": 150000},
                    {"type": "ambulance_service_expansion", "cost_usd": 80000},
                ],
            },
            # Week 5-8: Integrated planning
            "integrated_development_plan": {
                "total_investment_required": 1430000,  # USD
                "phased_implementation": {
                    "phase_1_infrastructure": {
                        "duration_months": 8,
                        "activities": [
                            "Water system upgrade",
                            "Sewage treatment",
                            "Road access",
                        ],
                        "cost": 800000,
                    },
                    "phase_2_development": {
                        "duration_months": 18,
                        "activities": [
                            "Residential construction",
                            "Health post",
                            "Commercial area",
                        ],
                        "cost": 630000,
                    },
                },
                "conditions_for_approval": [
                    "Complete sanitation infrastructure before occupancy",
                    "Health post operational before 50% occupancy",
                    "Emergency access roads completed in Phase 1",
                ],
            },
            # Week 9-12: Approval and monitoring setup
            "approval_outcome": {
                "status": "approved_with_conditions",
                "monitoring_requirements": [
                    "Monthly infrastructure progress reports",
                    "Water quality testing during construction",
                    "Health facility readiness assessments",
                ],
                "success_metrics": [
                    "100% water coverage within 6 months of occupancy",
                    "Health post serving <5000 people ratio",
                    "Zero waterborne disease outbreaks in first year",
                ],
            },
        }

    @staticmethod
    def scenario_cholera_outbreak_response():
        """
        Scenario: Cholera Outbreak Multi-Module Response
        Flow: Health → Sanitation → Urbanism (Emergency Response)
        """
        return {
            "scenario_name": "Cholera Outbreak Emergency Response",
            "municipality_id": 3,
            "scenario_type": "health_sanitation_urbanism_emergency",
            "timeline": "21 days",
            "description": "Cholera outbreak requires coordinated emergency response across all modules",
            # Day 1: Health alert
            "outbreak_detection": {
                "disease_name": "Cholera",
                "cases_reported": 12,
                "deaths": 1,
                "affected_areas": ["Bairro Operário", "Zona Industrial"],
                "case_fatality_rate": 8.3,
                "epidemiological_link": "Contaminated water source suspected",
            },
            # Day 1-3: Immediate response
            "emergency_response": {
                "health_actions": [
                    "Activate cholera treatment centers",
                    "Deploy rapid response teams",
                    "Implement case investigation protocol",
                    "Distribute ORS and antibiotics",
                ],
                "sanitation_actions": [
                    "Emergency water quality testing",
                    "Chlorinate suspected water sources",
                    "Inspect sewage systems in affected areas",
                    "Deploy portable latrines",
                ],
                "urbanism_actions": [
                    "Restrict access to contaminated areas",
                    "Identify alternative water distribution points",
                    "Assess drainage system adequacy",
                    "Plan emergency service access routes",
                ],
            },
            # Day 4-7: Investigation and containment
            "investigation_findings": {
                "contamination_source": "Broken sewage pipe contaminating water well",
                "affected_population": 8500,
                "infrastructure_failures": [
                    "30-year-old sewage pipe with multiple breaks",
                    "Inadequate separation between water and sewage systems",
                    "No backup water source for affected area",
                ],
                "urban_planning_gaps": [
                    "High population density without adequate infrastructure",
                    "Mixed residential-industrial zoning creating risks",
                    "Insufficient emergency response infrastructure",
                ],
            },
            # Day 8-14: Coordinated intervention
            "integrated_intervention": {
                "sanitation_repairs": [
                    "Emergency sewage pipe replacement",
                    "Water system disinfection and testing",
                    "Installation of temporary water treatment",
                    "Waste management system upgrade",
                ],
                "health_surveillance": [
                    "Active case finding in high-risk areas",
                    "Community health education campaigns",
                    "Vaccination campaign preparation",
                    "Contact tracing and monitoring",
                ],
                "urban_modifications": [
                    "Temporary relocation of 200 families",
                    "Emergency access road construction",
                    "Zoning review for industrial-residential separation",
                    "Infrastructure resilience assessment",
                ],
            },
            # Day 15-21: Recovery and prevention
            "recovery_and_prevention": {
                "outbreak_status": "contained",
                "final_case_count": 47,
                "final_death_count": 2,
                "case_fatality_rate": 4.3,
                "lessons_learned": [
                    "Need for integrated infrastructure monitoring",
                    "Importance of emergency response coordination",
                    "Value of community health education",
                ],
                "policy_implementations": [
                    "Mandatory separation distances for water/sewage systems",
                    "Regular infrastructure condition assessments",
                    "Emergency response protocol for all departments",
                    "Community health surveillance network",
                ],
                "long_term_investments": [
                    {"item": "Infrastructure upgrade program", "cost_usd": 1200000},
                    {"item": "Emergency response system", "cost_usd": 300000},
                    {"item": "Community health program", "cost_usd": 150000},
                ],
            },
        }

    @staticmethod
    def get_integration_api_examples():
        """
        API endpoint examples for the integration scenarios
        """
        return {
            "sanitation_endpoints": {
                "GET /sanitation/statistics/{municipality_id}": {
                    "description": "Get comprehensive sanitation statistics",
                    "example_response": {
                        "success": True,
                        "data": {
                            "water_coverage_percentage": 75.5,
                            "sewage_coverage_percentage": 62.3,
                            "waste_collection_volume_tons": 45.2,
                            "total_incidents": 8,
                            "critical_incidents": 2,
                            "technicians_available": 12,
                        },
                    },
                },
                "POST /sanitation/incidents": {
                    "description": "Report new sanitation incident",
                    "example_request": {
                        "municipality_id": 1,
                        "incident_type": "water_shortage",
                        "location": "Bairro Central",
                        "severity": "critical",
                        "description": "Main pump failure",
                        "reported_by": "Water Department",
                    },
                },
            },
            "health_endpoints": {
                "GET /health/statistics/{municipality_id}": {
                    "description": "Get health statistics with sanitation correlation",
                    "example_response": {
                        "success": True,
                        "data": {
                            "total_facilities": 8,
                            "waterborne_disease_cases": 23,
                            "sanitation_related_cases": 15,
                            "sanitation_correlation_score": 6.5,
                            "bed_occupancy_rate": 78.5,
                        },
                    },
                },
                "POST /health/alerts": {
                    "description": "Create health alert with sanitation link",
                    "example_request": {
                        "municipality_id": 1,
                        "alert_type": "outbreak",
                        "disease_category": "waterborne",
                        "sanitation_related": True,
                        "related_sanitation_incidents": [123, 124],
                    },
                },
            },
            "urbanism_endpoints": {
                "GET /urbanism/zones/{municipality_id}": {
                    "description": "Get urban zones with infrastructure status",
                    "example_response": {
                        "success": True,
                        "data": {
                            "zones": [
                                {
                                    "zone_name": "Centro",
                                    "sanitation_infrastructure": True,
                                    "water_coverage_percentage": 95.0,
                                    "health_facilities_count": 3,
                                    "health_facilities_needed": 2,
                                }
                            ]
                        },
                    },
                },
                "POST /urbanism/permits": {
                    "description": "Submit development permit with integration requirements",
                    "example_request": {
                        "municipality_id": 2,
                        "permit_type": "construction",
                        "estimated_population_impact": 5000,
                        "requires_sanitation_study": True,
                        "requires_health_impact_assessment": True,
                    },
                },
            },
            "integration_endpoints": {
                "GET /integration/report/{municipality_id}": {
                    "description": "Comprehensive cross-module integration report",
                    "example_response": {
                        "success": True,
                        "data": {
                            "municipality_name": "Luanda",
                            "sanitation_health_correlations": [
                                {
                                    "correlation_type": "water_coverage_disease_risk",
                                    "strength": "strong",
                                    "recommendation": "Prioritize water infrastructure",
                                }
                            ],
                            "cross_module_recommendations": [
                                "Implement joint monitoring system",
                                "Plan health facilities in new developments",
                            ],
                        },
                    },
                },
                "POST /integration/workflow/sanitation-incident": {
                    "description": "Trigger cross-module workflow for sanitation incident",
                    "example_request": {
                        "municipality_id": 1,
                        "incident_data": {
                            "incident_type": "water_shortage",
                            "severity": "critical",
                        },
                    },
                },
            },
        }


def generate_test_data_municipality_x():
    """Generate realistic test data for Municipality X scenario"""
    return {
        "municipality": {
            "id": 1,
            "name": "Município de Luanda",
            "province": "Luanda",
            "population": 125000,
        },
        "sanitation_baseline": {
            "water_coverage_percentage": 78.5,
            "sewage_coverage_percentage": 65.2,
            "waste_collection_zones": 12,
            "technicians": [
                {
                    "name": "João Silva",
                    "specialization": "Water Systems",
                    "coverage_areas": ["water_supply"],
                },
                {
                    "name": "Maria Santos",
                    "specialization": "Sewage Treatment",
                    "coverage_areas": ["sewage_treatment"],
                },
                {
                    "name": "António Costa",
                    "specialization": "Waste Management",
                    "coverage_areas": ["waste_collection"],
                },
            ],
        },
        "health_baseline": {
            "facilities": [
                {
                    "name": "Hospital Central",
                    "type": "hospital",
                    "capacity": 200,
                    "current_occupancy": 156,
                },
                {
                    "name": "Centro de Saúde Norte",
                    "type": "health_center",
                    "capacity": 50,
                    "current_occupancy": 38,
                },
                {
                    "name": "Posto Médico Sul",
                    "type": "health_post",
                    "capacity": 20,
                    "current_occupancy": 15,
                },
            ],
            "professionals": {"doctors": 25, "nurses": 78, "technicians": 45},
            "recent_diseases": [
                {"disease": "Diarrhea", "cases": 45, "waterborne": True},
                {"disease": "Malaria", "cases": 89, "waterborne": False},
                {"disease": "Typhoid", "cases": 12, "waterborne": True},
            ],
        },
        "urbanism_baseline": {
            "zones": [
                {
                    "name": "Centro",
                    "type": "commercial",
                    "population": 25000,
                    "sanitation_adequate": True,
                },
                {
                    "name": "Bairro Norte",
                    "type": "residential",
                    "population": 45000,
                    "sanitation_adequate": False,
                },
                {
                    "name": "Zona Industrial",
                    "type": "industrial",
                    "population": 8000,
                    "sanitation_adequate": True,
                },
            ],
            "infrastructure": [
                {
                    "name": "Estrada Principal",
                    "type": "roads",
                    "condition": "good",
                    "sanitation_connected": True,
                },
                {
                    "name": "Sistema Drenagem Norte",
                    "type": "drainage",
                    "condition": "poor",
                    "sanitation_connected": True,
                },
                {
                    "name": "Parque Central",
                    "type": "parks",
                    "condition": "excellent",
                    "health_serving": True,
                },
            ],
        },
    }
