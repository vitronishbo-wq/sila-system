class DependencySummaryProjector:

    def project(self, payload: dict) -> dict:
        records = payload.get('dependencies', [])
        active = [record for record in records if not record.get('end_date')]
        return {'family_id': payload.get('family_id'), 'total_dependencies': len(records), 'active_dependencies': len(active), 'dependency_types': sorted({record.get('dependency_type') for record in active if record.get('dependency_type')})}