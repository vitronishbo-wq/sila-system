import asyncio
import sys
import os
import csv
from sqlalchemy import select

# Add apps/backend to sys.path
if os.path.exists(os.path.join(os.getcwd(), "apps", "backend")):
    sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))
else:
    sys.path.append(os.getcwd())

try:
    from config.database import AsyncSessionLocal
    from modules.identity.models.user import User, AdministrativeLevel
    from modules.location.models.region import Region
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)


async def list_administrative_users(export_path=None):
    print("📋 Listing Administrative Users Hierarchically...\n")

    async with AsyncSessionLocal() as session:
        try:
            # 1. Fetch all regions to build a cache
            res_r = await session.execute(select(Region))
            regions = {r.id: r for r in res_r.scalars().all()}

            # 2. Fetch all admin users
            stmt_u = select(User).where(User.administrative_level.in_([
                AdministrativeLevel.CENTRAL,
                AdministrativeLevel.PROVINCIAL,
                AdministrativeLevel.MUNICIPAL,
                AdministrativeLevel.COMMUNAL
            ]))
            res_u = await session.execute(stmt_u)
            users = res_u.scalars().all()

            # 3. Helper to build hierarchical path for sorting
            def get_path(region_id):
                if not region_id or region_id not in regions:
                    return []
                r = regions[region_id]
                path = [r.name]
                curr = r
                while curr.parent_id and curr.parent_id in regions:
                    curr = regions[curr.parent_id]
                    path.insert(0, curr.name)
                return path

            # 4. Process and sort users
            processed_users = []
            for u in users:
                path = get_path(u.region_id)
                region = regions.get(u.region_id)
                processed_users.append({
                    "level": u.administrative_level.value if hasattr(u.administrative_level, 'value') else str(u.administrative_level),
                    "email": u.email,
                    "region_name": region.name if region else "ANGOLA",
                    "region_type": region.type if region else "PAIS",
                    "path": path,
                    "level_score": {
                        AdministrativeLevel.CENTRAL: 0,
                        AdministrativeLevel.PROVINCIAL: 1,
                        AdministrativeLevel.MUNICIPAL: 2,
                        AdministrativeLevel.COMMUNAL: 3
                    }.get(u.administrative_level, 99)
                })

            # Sort: Central first, then by Top Region (Province), then by Level, then by Region Name
            processed_users.sort(key=lambda x: (x["level_score"], x["path"], x["region_name"]))

            # Print and prepare export
            print(f"{'LEVEL':<12} | {'EMAIL':<45} | {'REGION NAME':<30} | {'REGION TYPE'}")
            print("-" * 110)

            export_data = []
            for pu in processed_users:
                print(
                    f"{pu['level']:<12} | {pu['email']:<45} | {pu['region_name']:<30} | {pu['region_type']}")
                export_data.append({
                    "level": pu["level"],
                    "email": pu["email"],
                    "region_name": pu["region_name"],
                    "region_type": pu["region_type"]
                })

            print(f"\n✅ Total administrative users listed: {len(processed_users)}")

            if export_path:
                with open(export_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(
                        f, fieldnames=["level", "email", "region_name", "region_type"])
                    writer.writeheader()
                    writer.writerows(export_data)
                print(f"📂 Exported to: {export_path}")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    target_path = "/app/scripts/administrative_users.csv" if os.path.exists(
        "/app/scripts") else "administrative_users.csv"
    asyncio.run(list_administrative_users(export_path=target_path))
