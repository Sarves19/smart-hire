#!/usr/bin/env python3
"""
Database Connectivity Test
"""

import sys

try:
    print("Testing database connection and models...")
    
    from app.core.config import settings
    print(f"✓ Config loaded: DATABASE_URL={settings.DATABASE_URL[:50]}...")
    
    from app.core.database import engine, SessionLocal
    print("✓ Database engine created")
    
    from app.models.user import User
    from app.models.email_verification import EmailVerification
    print("✓ Models imported")
    
    # Test connection
    with engine.connect() as conn:
        print("✓ Database connection successful")
    
    # Test session
    session = SessionLocal()
    print("✓ Session created")
    session.close()
    print("✓ Session closed")
    
    # Try to check if tables exist
    from sqlalchemy import text, inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"✓ Available tables: {tables}")
    
    if 'users' not in tables:
        print("✗ FAIL: 'users' table not found!")
        sys.exit(1)
    
    if 'email_verifications' not in tables:
        print("✗ WARN: 'email_verifications' table not found!")
    
    print("\n✓ All database checks passed!")
    sys.exit(0)

except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
