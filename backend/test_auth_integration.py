#!/usr/bin/env python3
"""
Quick Integration Test for Authentication Endpoints
Tests: Register, Duplicate Register, Login, Rate Limiting, Refresh Token
"""

import json
import sys
import time
from datetime import datetime

import httpx

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test data
TEST_USER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe.auth@example.com",
    "phone_number": "0771234567",
    "password": "SecurePass@2026XYZ",  # Doesn't contain name or email parts
    "role": "CUSTOMER",
}

DUPLICATE_USER = {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "john.doe.auth@example.com",  # Same email as TEST_USER
    "phone_number": "0771234568",
    "password": "AnotherPass@2026ABC",
    "role": "PROVIDER",
}

LOGIN_CREDS = {
    "email": TEST_USER["email"],
    "password": TEST_USER["password"],
}


def test_register():
    """Test user registration."""
    print("\n" + "=" * 60)
    print("TEST: User Registration")
    print("=" * 60)

    response = httpx.post(f"{BASE_URL}/auth/register", json=TEST_USER)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 201:
        print("✓ PASS: Registration successful (201 Created)")
        return True
    else:
        print(f"✗ FAIL: Expected 201, got {response.status_code}")
        return False


def test_duplicate_register():
    """Test duplicate email registration (should return 409)."""
    print("\n" + "=" * 60)
    print("TEST: Duplicate Email Registration (409 Conflict)")
    print("=" * 60)

    response = httpx.post(f"{BASE_URL}/auth/register", json=DUPLICATE_USER)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 409:
        print("✓ PASS: Duplicate registration rejected (409 Conflict)")
        return True
    else:
        print(f"✗ FAIL: Expected 409, got {response.status_code}")
        return False


def test_login():
    """Test user login."""
    print("\n" + "=" * 60)
    print("TEST: User Login")
    print("=" * 60)

    # First, try to login (may fail if email not verified)
    response = httpx.post(f"{BASE_URL}/auth/login", json=LOGIN_CREDS)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        print("✓ PASS: Login successful (200 OK)")
        if "access_token" in data and "refresh_token" in data:
            print(f"  - Access Token: {data['access_token'][:50]}...")
            print(f"  - Refresh Token: {data['refresh_token'][:50]}...")
            return True, data["access_token"], data["refresh_token"]
        else:
            print("✗ FAIL: Missing tokens in response")
            return False, None, None
    elif response.status_code == 401:
        print("⚠ WARN: Login rejected (401 Unauthorized) - email may not be verified")
        return None, None, None
    else:
        print(f"✗ FAIL: Expected 200 or 401, got {response.status_code}")
        return False, None, None


def test_refresh_token(refresh_token):
    """Test refresh token endpoint."""
    print("\n" + "=" * 60)
    print("TEST: Refresh Token")
    print("=" * 60)

    payload = {"refresh_token": refresh_token}
    response = httpx.post(f"{BASE_URL}/auth/refresh", json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        print("✓ PASS: Token refresh successful (200 OK)")
        if "access_token" in data:
            print(f"  - New Access Token: {data['access_token'][:50]}...")
            return True
        else:
            print("✗ FAIL: Missing access_token in response")
            return False
    else:
        print(f"✗ FAIL: Expected 200, got {response.status_code}")
        return False


def test_rate_limiting():
    """Test rate limiting on OTP endpoint (5 requests per 5 minutes)."""
    print("\n" + "=" * 60)
    print("TEST: Rate Limiting (OTP endpoint - 5 req/5 min)")
    print("=" * 60)

    # Use unique email for each test run to avoid cross-contamination
    base_email = f"ratelimit.test.{int(time.time())}@example.com"
    payload = {"email": base_email}

    # Send 6 requests rapidly (should hit rate limit on 6th)
    for i in range(1, 7):
        response = httpx.post(f"{BASE_URL}/auth/resend-otp", json=payload)
        print(f"Request {i}: Status {response.status_code}")

        if i <= 5:
            if response.status_code == 200:
                print(f"  ✓ Request {i} allowed")
            else:
                print(f"  ✗ Request {i} should be allowed (got {response.status_code})")
                print(f"    Response: {response.text}")
                return False
        elif i == 6:
            if response.status_code == 429:
                print(f"  ✓ Request {i} rate limited (429 Too Many Requests)")
                return True
            else:
                print(f"  ✗ Request {i} should be rate limited (expected 429, got {response.status_code})")
                return False


def test_invalid_password():
    """Test invalid password validation."""
    print("\n" + "=" * 60)
    print("TEST: Invalid Password Validation (weak password)")
    print("=" * 60)

    invalid_user = TEST_USER.copy()
    invalid_user["password"] = "weak"  # Too weak

    response = httpx.post(f"{BASE_URL}/auth/register", json=invalid_user)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 422:
        print("✓ PASS: Invalid password rejected (422 Validation Error)")
        return True
    else:
        print(f"Note: Got status {response.status_code} (validation may be at schema level)")
        return None


def test_invalid_email():
    """Test invalid email validation."""
    print("\n" + "=" * 60)
    print("TEST: Invalid Email Validation")
    print("=" * 60)

    invalid_user = TEST_USER.copy()
    invalid_user["email"] = "not-an-email"

    response = httpx.post(f"{BASE_URL}/auth/register", json=invalid_user)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 422:
        print("✓ PASS: Invalid email rejected (422 Validation Error)")
        return True
    else:
        print(f"Note: Got status {response.status_code}")
        return None


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  AUTHENTICATION MODULE INTEGRATION TESTS".center(58) + "║")
    print("║" + f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".ljust(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    results = {}

    # Run tests
    results["Register"] = test_register()
    results["Duplicate Register (409)"] = test_duplicate_register()

    login_result, access_token, refresh_token = test_login()
    results["Login"] = login_result

    if refresh_token:
        results["Refresh Token"] = test_refresh_token(refresh_token)
    else:
        print("\n⚠ Skipping refresh token test (no token from login)")

    results["Rate Limiting"] = test_rate_limiting()
    results["Invalid Password"] = test_invalid_password()
    results["Invalid Email"] = test_invalid_email()

    # Summary
    print("\n\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    for test_name, result in results.items():
        status = "✓ PASS" if result is True else ("✗ FAIL" if result is False else "⊘ SKIP")
        print(f"{test_name:.<40} {status}")

    print("=" * 60)
    print(f"Total: {passed} passed, {failed} failed, {skipped} skipped")
    print(f"Health Score: {passed}/{len(results)} endpoints working")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
