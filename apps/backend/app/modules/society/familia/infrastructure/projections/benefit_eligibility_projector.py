class BenefitEligibilityProjector:

    def project(self, payload: dict) -> dict:
        member_count = int(payload.get('member_count', 0))
        dependents_count = int(payload.get('dependents_count', 0))
        score = dependents_count * 2 + member_count
        return {'family_id': payload.get('family_id'), 'eligibility_score': score, 'eligible_social_support': score >= 5}