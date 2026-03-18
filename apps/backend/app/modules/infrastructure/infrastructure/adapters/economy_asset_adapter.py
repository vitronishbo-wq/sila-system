from __future__ import annotations
from ...domain.ports.asset_reporting_port import AssetReportingPort

class InfrastructureAssetAdapter(AssetReportingPort):

    def __init__(self, treasury_client: 'TreasuryAPIClient'):
        self.client = treasury_client

    async def report_new_asset(self, asset_data: 'AssetDTO'):
        payload = {'origin': 'INFRASTRUCTURE_CORE', 'asset_class': 'INFRA_HARD_ASSET', 'valuation': asset_data.cost, 'depreciation_start': asset_data.completion_date}
        return await self.client.register_entry(payload)