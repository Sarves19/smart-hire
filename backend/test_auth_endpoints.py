#!/usr/bin/env python
"""Simplified authentication flow test - validates endpoints respond correctly."""

import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

# Generate unique test data
timestamp = int(time.time())
test_email = f"flowtest{timestamp}@example.com"
test_phone = f"+947{random.randint(10000000, 99999999)}"
test_password = "ComplexPass123!"

print("=" * 70)
print("SIMPLIFIED AUTHENTICATION FLOW TEST")
print("=" * 70)
print(f"Email: {test_email}")
print(f"Phone: {test_phone}")
print(f"Password: {test_password}\n")

test_results = {"passed": 0, "failed": 0}

def test_case(num: int, name: str, method: str, endpoint: str, payload: dict, expected_status: int):
    """Helper to run and track test cases."""
    print(f"[{num}] {name}")
    print(f"    {method} {endpoint}")
    print(f"    Payload: {payload}")
    
    try:
        if method == "POST":
            r = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=5)
        else:
            r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        
        print(f"    Status: {r.status_code} (expected {expected_status})")
        print(f"    Response: {r.json()}")
        
        if r.status_code == expected_status:
            print(f"    ✓ PASS\n")
            test_results["passed"] += 1
            return True
        else:
            print(f"    ✗ FAIL\n")
            test_results["failed"] += 1
            return False
    except Exception as e:
        print(f"    ✗ ERROR: {e}\n")
        test_results["failed"] += 1
        return False

# =====================================================
# TEST 1: Register
# =====================================================

test_case(
    1,
    "Register new user",
    "POST",
    "/auth/register",
    {
        "first_name": "Test",
        "last_name": "User",
        "email": test_email,
        "phone_number": test_phone,
        "password": test_password,
        "role": "CUSTOMER"
    },
    201
)

# =====================================================
# TEST 2: Try login before email verification (should fail)
# =====================================================

test_case(
    2,
    "Try login before email verification",
    "POST",
    "/auth/login",
    {"email": test_email},
    401  # Should fail because email not verified
)

# =====================================================
# TEST 3: Resend OTP
# =====================================================

test_case(
    3,
    "Resend email verification OTP",
    "POST",
    "/auth/resend-otp",
    {"email": test_email},
    200
)

# =====================================================
# TEST 4: Verify with wrong OTP (should fail)
# =====================================================

test_case(
    4,
    "Verify email with wrong OTP",
    "POST",
    "/auth/verify-otp",
    {
        "email": test_email,
        "otp_code": "000000"  # Wrong OTP
    },
    400  # Should fail with bad request
)

# =====================================================
# TEST 5: Forgot password (should work even without verification)
# =====================================================

test_case(
    5,
    "Request password reset",
    "POST",
    "/auth/forgot-password",
    {"email": test_email},
    200
)

# =====================================================
# TEST 6: Try reset with wrong OTP (should fail)
# =====================================================

test_case(
    6,
    "Reset password with wrong OTP",
    "POST",
    "/auth/reset-password",
    {
        "email": test_email,
        "otp_code": "000000",
        "new_password": "NewPassword456!"
    },
    400  # Should fail with bad request
)

# =====================================================
# TEST 7: Try login verify without OTP (should fail)
# =====================================================

test_case(
    7,
    "Verify login with wrong OTP",
    "POST",
    "/auth/login-verify",
    {
        "email": test_email,
        "otp_code": "000000",
        "device_fingerprint": "test-device",
        "device_name": "Test",
        "browser": "Chrome",
        "operating_system": "Windows",
        "ip_address": "127.0.0.1",
        "remember_device": False
    },
    401  # Should fail - wrong OTP
)

# =====================================================
# TEST 8: Test with non-existent email
# =====================================================

test_case(
    8,
    "Login with non-existent email",
    "POST",
    "/auth/login",
    {"email": "nonexistent@example.com"},
    401  # Should fail - user doesn't exist
)

# =====================================================
# SUMMARY
# =====================================================

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Passed: {test_results['passed']}")
print(f"Failed: {test_results['failed']}")
print(f"Total:  {test_results['passed'] + test_results['failed']}")
print("=" * 70)

if test_results['failed'] == 0:
    print("\n✓ ALL TESTS PASSED!")
else:
    print(f"\n✗ {test_results['failed']} test(s) failed")
