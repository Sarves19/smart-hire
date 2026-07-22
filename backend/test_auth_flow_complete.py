#!/usr/bin/env python
"""Complete authentication flow test with OTP extraction from DB."""

import requests
import random
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

# Database connection for testing
settings = Settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_latest_otp(email: str, purpose: str = "EMAIL_VERIFICATION") -> str:
    """Extract OTP from database for testing."""
    db = SessionLocal()
    try:
        stmt = text("""
            SELECT otp_code FROM email_verifications 
            WHERE email = :email 
            AND purpose = :purpose 
            AND is_used = false 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        result = db.execute(stmt, {"email": email, "purpose": purpose})
        row = result.fetchone()
        if row:
            return row[0]
        return None
    finally:
        db.close()

# Generate unique test data
timestamp = int(time.time())
test_email = f"flowtest{timestamp}@example.com"
test_phone = f"+947{random.randint(10000000, 99999999)}"
test_password = "ComplexPass123!"

print("=" * 60)
print("COMPLETE AUTHENTICATION FLOW TEST")
print("=" * 60)
print(f"Email: {test_email}")
print(f"Phone: {test_phone}")
print(f"Password: {test_password}\n")

test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_case(name: str, func):
    """Helper to run and track test cases."""
    print(f"\n[TEST] {name}")
    try:
        result = func()
        if result:
            print(f"  ✓ PASS")
            test_results["passed"] += 1
            return True
        else:
            print(f"  ✗ FAIL")
            test_results["failed"] += 1
            return False
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        test_results["failed"] += 1
        test_results["errors"].append((name, str(e)))
        return False

# =====================================================
# TEST 1: Register
# =====================================================

def test_register():
    reg_payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": test_email,
        "phone_number": test_phone,
        "password": test_password,
        "role": "CUSTOMER"
    }
    r = requests.post(f"{API_URL}/auth/register", json=reg_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 201

test_case("1. Register new user", test_register)

# =====================================================
# TEST 2: Verify Email
# =====================================================

def test_verify_email():
    time.sleep(1)  # Wait for DB
    otp = get_latest_otp(test_email, "EMAIL_VERIFICATION")
    if not otp:
        print(f"    Could not find OTP in database")
        return False
    
    print(f"    OTP from DB: {otp}")
    verify_payload = {
        "email": test_email,
        "otp_code": otp
    }
    r = requests.post(f"{API_URL}/auth/verify-otp", json=verify_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 200

test_case("2. Verify email with OTP", test_verify_email)

# =====================================================
# TEST 3: Login Initiate
# =====================================================

def test_login_initiate():
    login_payload = {"email": test_email}
    r = requests.post(f"{API_URL}/auth/login", json=login_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 200

test_case("3. Initiate login (send OTP)", test_login_initiate)

# =====================================================
# TEST 4: Login Verify OTP
# =====================================================

def test_login_verify():
    time.sleep(1)  # Wait for DB
    otp = get_latest_otp(test_email, "LOGIN")
    if not otp:
        print(f"    Could not find login OTP in database")
        return False
    
    print(f"    Login OTP from DB: {otp}")
    verify_payload = {
        "email": test_email,
        "otp_code": otp,
        "device_fingerprint": "test-device-123",
        "device_name": "Test Device",
        "browser": "Chrome",
        "operating_system": "Windows",
        "ip_address": "127.0.0.1",
        "remember_device": False
    }
    r = requests.post(f"{API_URL}/auth/login-verify", json=verify_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    resp = r.json()
    print(f"    Response: {resp}")
    if r.status_code == 200 and "access_token" in resp:
        global access_token, refresh_token
        access_token = resp.get("access_token")
        refresh_token = resp.get("refresh_token")
        return True
    return False

access_token = None
refresh_token = None
test_case("4. Verify login OTP and get tokens", test_login_verify)

# =====================================================
# TEST 5: Refresh Token
# =====================================================

def test_refresh_token():
    if not refresh_token:
        print(f"    No refresh token available")
        return False
    
    refresh_payload = {"refresh_token": refresh_token}
    r = requests.post(f"{API_URL}/auth/refresh", json=refresh_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 200

test_case("5. Refresh token", test_refresh_token)

# =====================================================
# TEST 6: Forgot Password
# =====================================================

def test_forgot_password():
    forgot_payload = {"email": test_email}
    r = requests.post(f"{API_URL}/auth/forgot-password", json=forgot_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 200

test_case("6. Forgot password", test_forgot_password)

# =====================================================
# TEST 7: Reset Password
# =====================================================

def test_reset_password():
    time.sleep(1)  # Wait for DB
    otp = get_latest_otp(test_email, "PASSWORD_RESET")
    if not otp:
        print(f"    Could not find password reset OTP in database")
        return False
    
    print(f"    Password reset OTP from DB: {otp}")
    reset_payload = {
        "email": test_email,
        "otp_code": otp,
        "new_password": "NewPassword456!"
    }
    r = requests.post(f"{API_URL}/auth/reset-password", json=reset_payload, timeout=5)
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    return r.status_code == 200

test_case("7. Reset password", test_reset_password)

# =====================================================
# SUMMARY
# =====================================================

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Passed: {test_results['passed']}")
print(f"Failed: {test_results['failed']}")
if test_results['errors']:
    print("\nErrors:")
    for test_name, error_msg in test_results['errors']:
        print(f"  - {test_name}: {error_msg}")
print("=" * 60)
