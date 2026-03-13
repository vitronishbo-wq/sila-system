#!/usr/bin/env python3
"""
Phase 5 - Password Reset Script
Define senha universal para todos os usuários migrados
"""

import asyncio
import os
import sys
import bcrypt
from datetime import datetime

sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.chdir('/home/dev03wsl/sila-system/apps/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv('/home/dev03wsl/sila-system/.env')

DATABASE_URL = os.getenv('DATABASE_URL')


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


async def reset_iam_passwords(universal_password: str):
    """Reset all iam_users passwords to universal password"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    print("\n" + "="*80)
    print("🔐 PHASE 5 - PASSWORD RESET (UNIVERSAL PASSWORD)")
    print("="*80)
    
    try:
        # Hash the universal password
        print(f"\n🔑 Generating bcrypt hash for: '{universal_password}'")
        password_hash = hash_password(universal_password)
        print(f"✅ Hash generated (length: {len(password_hash)} chars)")
        
        async with SessionLocal() as session:
            # Get all migrated users
            result = await session.execute(text("""
                SELECT id, email FROM iam_users 
                WHERE created_by = 'migration_script'
                ORDER BY email
            """))
            users = result.fetchall()
            
            print(f"\n📝 Found {len(users)} migrated users to update:")
            for user_id, email in users:
                print(f"  • {email}")
            
            # Update passwords
            print(f"\n🔄 Updating passwords...")
            update_result = await session.execute(text("""
                UPDATE iam_users 
                SET password_hash = :password_hash,
                    password_changed_at = :now,
                    updated_at = :now,
                    updated_by = 'password_reset_script'
                WHERE created_by = 'migration_script'
                RETURNING id, email
            """), {
                'password_hash': password_hash,
                'now': datetime.utcnow()
            })
            
            updated_users = update_result.fetchall()
            await session.commit()
            
            print(f"\n✅ Successfully updated {len(updated_users)} users:")
            for user_id, email in updated_users:
                print(f"  ✅ {email}")
            
            # Verify
            print(f"\n🔍 Verification:")
            result = await session.execute(text("""
                SELECT COUNT(*) FROM iam_users 
                WHERE password_hash = :hash AND created_by = 'migration_script'
            """), {'hash': password_hash})
            verified_count = result.scalar()
            print(f"  ✅ {verified_count} users have the new password hash")
            
            if verified_count == len(updated_users):
                print(f"\n🎉 Password reset successful for all users!")
            else:
                print(f"\n⚠️  Warning: Only {verified_count}/{len(updated_users)} users verified")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


async def test_password(username: str, universal_password: str):
    """Test login with the new password"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    try:
        async with SessionLocal() as session:
            result = await session.execute(text("""
                SELECT id, email, password_hash FROM iam_users 
                WHERE email = :email
            """), {'email': username})
            user = result.fetchone()
            
            if not user:
                print(f"❌ User {username} not found")
                return False
            
            user_id, email, stored_hash = user
            
            # Test password
            if bcrypt.checkpw(universal_password.encode('utf-8'), 
                            stored_hash.encode('utf-8')):
                print(f"✅ Password test PASSED for {email}")
                return True
            else:
                print(f"❌ Password test FAILED for {email}")
                return False
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error testing password: {str(e)}")
        return False


async def show_password_status():
    """Show current password status for all migrated users"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    print("\n" + "="*80)
    print("📋 PASSWORD STATUS")
    print("="*80)
    
    try:
        async with SessionLocal() as session:
            result = await session.execute(text("""
                SELECT email, password_changed_at, updated_by 
                FROM iam_users 
                WHERE created_by = 'migration_script'
                ORDER BY email
            """))
            
            print(f"\nMigrated Users Status:")
            for email, changed_at, updated_by in result.fetchall():
                changed_str = changed_at.strftime('%Y-%m-%d %H:%M:%S') if changed_at else 'Never'
                by_str = updated_by or 'System'
                print(f"  {email:<30} Changed: {changed_str}  By: {by_str}")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Phase 5 - Password Reset Script'
    )
    parser.add_argument(
        '--password',
        default='Sila_1983',
        help='Universal password to set (default: Sila_1983)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test password after reset'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show password status'
    )
    parser.add_argument(
        '--test-user',
        help='Test password for specific user'
    )
    
    args = parser.parse_args()
    
    if args.status:
        await show_password_status()
    elif args.test_user:
        print(f"\n🧪 Testing password for {args.test_user}...")
        result = await test_password(args.test_user, args.password)
        if result:
            print(f"\n✅ Login would succeed")
        else:
            print(f"\n❌ Login would fail")
    else:
        await reset_iam_passwords(args.password)
        
        if args.test:
            print(f"\n🧪 Testing with admin@sila.gov.ao...")
            await test_password('admin@sila.gov.ao', args.password)
            print(f"\n🧪 Testing with central@sila.gov.ao...")
            await test_password('central@sila.gov.ao', args.password)


if __name__ == "__main__":
    asyncio.run(main())
