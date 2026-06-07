from __future__ import annotations


class JusticeFinesAdapter:
    def __init__(self, justice_service: JusticeInternalService):
        self.justice = justice_service

    async def issue_speeding_fine(self, vehicle_did: str, speed: float, limit: float):
        if speed > limit:
            severity = "HIGH" if speed > limit * 1.2 else "MEDIUM"
            fine_data = {
                "subject_did": vehicle_did,
                "offense_type": "SPEEDING",
                "evidence_speed": speed,
                "severity": severity,
                "automated_judgement": True,
            }
            return await self.justice.open_case(fine_data)
