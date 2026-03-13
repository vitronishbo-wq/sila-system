import asyncio
import sys
import os
import csv

# Add apps/backend to sys.path to allow importing modules
# When running from project root:
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))
# When running inside the backend container:
sys.path.append(os.path.join(os.getcwd()))

try:
    from sqlalchemy import select
    from config.database import AsyncSessionLocal
    from apps.backend.app.modules.identity.models.user import User, AdministrativeLevel
    from apps.backend.app.modules.location.models.region import Region
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)


async def list_administrative_users(export_path=None):
    print("📋 Listing Administrative Users (Provincial, Municipal, Communal)\n")

    async with AsyncSessionLocal() as session:
        try:
            # Join User and Region to get region names
            stmt = (
                select(User, Region.name.label("region_name"), Region.type.label("region_type"))
                .outerjoin(Region, User.region_id == Region.id)
                .where(User.level.in_([
                    AdministrativeLevel.CENTRAL,
                    AdministrativeLevel.PROVINCIAL,
                    AdministrativeLevel.MUNICIPAL,
                    AdministrativeLevel.COMMUNAL
                ]))
                .order_by(User.level, Region.name)
            )

            result = await session.execute(stmt)
            users_with_regions = result.all()

            if not users_with_regions:
                print("⚠️ No administrative users found.")
                return

            # Print Header
            print(f"{'LEVEL':<12} | {'EMAIL':<45} | {'REGION NAME':<30} | {'REGION TYPE'}")
            print("-" * 110)

            export_data = []
            for user_row in users_with_regions:
                user = user_row[0]
                region_name = user_row.region_name or "N/A"
                region_type = user_row.region_type or "N/A"
                print(f"{user.level:<12} | {user.email:<45} | {region_name:<30} | {region_type}")

                export_data.append({
                    "level": user.level,
                    "email": user.email,
                    "region_name": region_name,
                    "region_type": region_type
                })

            print(f"\n✅ Total administrative users listed: {len(users_with_regions)}")

            # Export to CSV if requested
            if export_path:
                try:
                    with open(export_path, mode='w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(
                            f, fieldnames=["level", "email", "region_name", "region_type"])
                        writer.writeheader()
                        writer.writerows(export_data)
                    print(f"📂 Exported to: {export_path}")
                except Exception as export_err:
                    print(f"❌ Error exporting to CSV: {export_err}")

        except Exception as e:
            print(f"❌ Error executing query: {e}")

if __name__ == "__main__":
    # If running inside Docker, /app is the root.
    # We'll save the file in a place that's visible to the host if possible.
    # Since /app is mapped to ./apps/backend, saving to /app/scripts/administrative_users.csv
    # will appear in apps/backend/scripts/administrative_users.csv on the host.

    # Check if we are in Docker or Local
    if os.path.exists("/app/scripts"):
        target_path = "/app/scripts/administrative_users.csv"
    else:
        # Fallback to local execution directory
        target_path = "administrative_users.csv"

    asyncio.run(list_administrative_users(export_path=target_path))
