"""
FASE 3.2 - Integration Examples
Search Engine & Matching Engine Usage Examples
"""

# ============================================================================
# EXAMPLE 1: Search Endpoint Usage
# ============================================================================

"""
Example 1a: Basic Full-Text Search
-----------------------------------
Search for schools with basic query
"""

import httpx

async def basic_search():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/educacao/marketplace/search",
            params={
                "q": "liceu",  # Full-text search
                "page": 1,
                "page_size": 20,
            }
        )
        results = response.json()
        return results


"""
Example 1b: Advanced Filtering
-------------------------------
Search with multiple filters
"""

async def advanced_search():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/educacao/marketplace/search",
            params={
                "q": "school",
                "city": "Luanda",
                "district": "Maianga",
                "educational_level": "secundario",
                "price_min": 0,
                "price_max": 50000,
                "modality": "presencial",
                "institution_type": "publica",
                "min_slots": 5,
                "has_special_needs_support": True,
                "min_rating": 4.0,
                "page": 1,
                "page_size": 20,
            }
        )
        results = response.json()
        return results


"""
Example 1c: Location-Based Filtering
------------------------------------
Filter only by location
"""

async def location_search():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/educacao/marketplace/search",
            params={
                "city": "Luanda",
                "district": "Kinaxixe",
                "page": 1,
                "page_size": 50,
            }
        )
        results = response.json()
        print(f"Found {results['total']} institutions in Kinaxixe")
        for inst in results['results']:
            print(f"  - {inst['name']}: {inst['rating']}/5.0 ⭐")
        return results


# ============================================================================
# EXAMPLE 2: Matching Engine Usage
# ============================================================================

"""
Example 2a: Find Matches for Student
-------------------------------------
Recommend schools for a student profile
"""

async def find_matches_for_student():
    async with httpx.AsyncClient() as client:
        student_profile = {
            "student_id": "STU-2024-0001",
            "age": 16,
            "academic_performance": 75.5,  # 0-100
            "special_needs": [],
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 30000,
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 0
        }
        
        response = await client.post(
            "http://localhost:8000/marketplace/matching/find-matches",
            json=student_profile,
            params={"limit": 10}
        )
        
        matches = response.json()
        print(f"Found {matches['total']} compatible institutions for {student_profile['student_id']}")
        
        for match in matches['matches']:
            print(f"\n{match['rank']}. {match['name']}")
            print(f"   Score: {match['match_score']:.0f}/100")
            print(f"   Reasons: {', '.join(match['reasons'])}")
        
        return matches


"""
Example 2b: Check Eligibility
------------------------------
Verify if student is eligible for a specific institution
"""

async def check_eligibility():
    async with httpx.AsyncClient() as client:
        student_profile = {
            "student_id": "STU-2024-0001",
            "age": 16,
            "academic_performance": 75.5,
            "special_needs": ["dyslexia"],  # With special needs
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 25000,  # Lower budget
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 2  # Multiple transfers
        }
        
        response = await client.post(
            "http://localhost:8000/marketplace/matching/eligibility/STU-2024-0001/INST-UUID",
            json=student_profile
        )
        
        eligibility = response.json()
        
        print(f"Eligibility for {eligibility['institution_name']}:")
        print(f"  Eligible: {'✓ Yes' if eligibility['eligible'] else '✗ No'}")
        print(f"  Compatibility: {eligibility['compatibility_score']:.0f}/100")
        
        if eligibility['blocking_factors']:
            print(f"  Blocking Factors:")
            for factor in eligibility['blocking_factors']:
                print(f"    - {factor}")
        
        if eligibility['warnings']:
            print(f"  Warnings:")
            for warning in eligibility['warnings']:
                print(f"    ⚠ {warning}")
        
        if eligibility['required_actions']:
            print(f"  Required Actions:")
            for action in eligibility['required_actions']:
                print(f"    → {action}")
        
        return eligibility


"""
Example 2c: Get Personalized Recommendations
--------------------------------------------
Get detailed recommendations for a student
"""

async def get_recommendations():
    async with httpx.AsyncClient() as client:
        student_profile = {
            "student_id": "STU-2024-0001",
            "age": 16,
            "academic_performance": 85.0,  # Strong student
            "special_needs": [],
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 50000,  # Good budget
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 0
        }
        
        response = await client.get(
            f"http://localhost:8000/marketplace/matching/recommendations/STU-2024-0001",
            params={
                **student_profile,
                "limit": 5
            }
        )
        
        recommendations = response.json()
        print(f"Top {len(recommendations['recommendations'])} Recommendations:")
        
        for rec in recommendations['recommendations']:
            print(f"\n🎓 {rec['name']}")
            print(f"   Match Score: {rec['match_score']:.0f}/100")
            print(f"   Compatibility: {rec['compatibility_score']:.0f}/100")
            
        return recommendations


# ============================================================================
# EXAMPLE 3: Advanced Matching Scenarios
# ============================================================================

"""
Example 3a: Student with Special Needs
---------------------------------------
Finding schools that support specific needs
"""

async def find_for_student_with_special_needs():
    async with httpx.AsyncClient() as client:
        student = {
            "student_id": "STU-SPECIAL-001",
            "age": 17,
            "academic_performance": 70.0,
            "special_needs": ["visual_impairment", "mobility_issues"],
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 35000,
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 1
        }
        
        response = await client.post(
            "http://localhost:8000/marketplace/matching/find-matches",
            json=student,
            params={"limit": 5}
        )
        
        matches = response.json()
        return matches


"""
Example 3b: Budget-Conscious Student
------------------------------------
Finding affordable options
"""

async def find_affordable_options():
    async with httpx.AsyncClient() as client:
        student = {
            "student_id": "STU-BUDGET-001",
            "age": 16,
            "academic_performance": 72.0,
            "special_needs": [],
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 15000,  # Limited budget
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 0
        }
        
        response = await client.post(
            "http://localhost:8000/marketplace/matching/find-matches",
            json=student,
            params={"limit": 10}
        )
        
        matches = response.json()
        
        # Filter for affordable options
        affordable = [
            m for m in matches['matches']
            if 'orçamento' in ' '.join(m['reasons']).lower()
        ]
        
        return affordable


"""
Example 3c: High Performer
--------------------------
Finding best schools for top student
"""

async def find_for_high_performer():
    async with httpx.AsyncClient() as client:
        student = {
            "student_id": "STU-EXCEL-001",
            "age": 16,
            "academic_performance": 95.0,  # Top student
            "special_needs": [],
            "location": {
                "province": "Luanda",
                "municipality": "Luanda",
                "district": "Maianga"
            },
            "available_budget": 100000,  # High budget
            "preferred_modalities": ["presencial"],
            "educational_level": "secundario",
            "previous_transfers": 0
        }
        
        response = await client.post(
            "http://localhost:8000/marketplace/matching/find-matches",
            json=student,
            params={"limit": 5}
        )
        
        matches = response.json()
        return matches


# ============================================================================
# EXAMPLE 4: Programmatic Usage in Application
# ============================================================================

"""
Example 4a: Integration into Application Service
-------------------------------------------------
Using matching in a service class
"""

from foundation.matching import (
    MatchingEngine,
    MatchingScorer,
    CompatibilityCalculator,
    StudentProfile,
    InstitutionProfile,
)

class StudentAdmissionService:
    def __init__(self):
        self.matching_engine = MatchingEngine(
            scorer=MatchingScorer(),
            compatibility=CompatibilityCalculator()
        )
    
    async def recommend_schools(self, session, student_data: dict):
        """Recommend schools for a student"""
        
        # Convert to domain model
        student = StudentProfile(
            student_id=student_data['id'],
            age=student_data['age'],
            academic_performance=student_data['academic_performance'],
            special_needs=student_data.get('special_needs', []),
            location=student_data['location'],
            available_budget=student_data.get('available_budget', 0),
            preferred_modalities=student_data.get('preferred_modalities', []),
            educational_level=student_data.get('educational_level'),
            previous_transfers=student_data.get('previous_transfers', 0),
        )
        
        # Get institutions from database
        from sqlalchemy import select
        from app.modules.educacao.infrastructure.models.institution_marketplace_projection_model import (
            InstitutionMarketplaceProjectionModel,
        )
        
        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.is_active == True
        )
        result = await session.execute(stmt)
        institution_models = result.scalars().all()
        
        # Convert to domain models
        institutions = [
            InstitutionProfile(
                institution_id=str(m.institution_id),
                name=m.name,
                type=m.type,
                location={
                    "province": m.province,
                    "municipality": m.municipality,
                    "district": m.district,
                },
                available_slots=m.available_slots,
                monthly_fee=m.monthly_fee_avg,
                rating=m.rating,
                approval_rate=m.approval_rate,
                academic_performance=m.average_academic_performance,
                specializations=m.specializations,
                supports_special_needs=m.supports_special_needs,
                special_needs_types=m.special_needs_types,
                teaching_modalities=m.teaching_modalities,
                transfer_acceptance_rate=m.transfer_acceptance_rate,
            )
            for m in institution_models
        ]
        
        # Find matches
        matches = await self.matching_engine.find_matches(
            session=session,
            student=student,
            institutions=institutions,
            max_results=10,
        )
        
        return matches


"""
Example 4b: Batch Processing
-----------------------------
Process multiple students for recommendations
"""

async def batch_recommend_students(session, student_ids: list[str]):
    """Recommend schools for multiple students"""
    
    service = StudentAdmissionService()
    results = {}
    
    for student_id in student_ids:
        # Fetch student data
        student_data = await fetch_student_data(student_id)
        
        # Get recommendations
        recommendations = await service.recommend_schools(session, student_data)
        
        results[student_id] = recommendations
    
    return results


async def fetch_student_data(student_id: str) -> dict:
    """Fetch student data from database"""
    # Implementation would fetch from student service
    pass


# ============================================================================
# EXAMPLE 5: Scripting with Python
# ============================================================================

"""
Example 5: Command-line Usage
-----------------------------
Using these APIs from Python scripts
"""

import asyncio

async def main():
    # Example 1: Search
    print("=" * 50)
    print("Searching for schools...")
    print("=" * 50)
    results = await basic_search()
    print(f"Found {results['total']} results")
    
    # Example 2: Find matches
    print("\n" + "=" * 50)
    print("Finding matches for student...")
    print("=" * 50)
    matches = await find_matches_for_student()
    
    # Example 3: Check eligibility
    print("\n" + "=" * 50)
    print("Checking eligibility...")
    print("=" * 50)
    eligibility = await check_eligibility()

if __name__ == "__main__":
    asyncio.run(main())
