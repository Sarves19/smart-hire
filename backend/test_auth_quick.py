#!/usr/bin/env python
"""Quick authentication test with corrected password validation."""

import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

# Generate unique test data
timestamp = int(time.time())
test_email = f"authtest{timestamp}@example.com"
test_phone = f"+947{random.randint(10000000, 99999999)}"
# Password that doesn't contain name or email
test_password = "SmartPassword123!"

print("Testing Authentication Module\n")
print(f"Email: {test_email}")
print(f"Phone: {test_phone}")
print(f"Password: {test_password}\n")

# Test 1: Register
print("[1] Register new user")
reg_payload = {
    "first_name": "John",
    "last_name": "Smith",
    "email": test_email,
    "phone_number": test_phone,
    "password": test_password,
    "role": "CUSTOMER"
}

try:
    r = requests.post(f"{API_URL}/auth/register", json=reg_payload, timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    if r.status_code == 201:
        print("✓ PASS\n")
    else:
        print("✗ FAIL\n")
except Exception as e:
    print(f"✗ FAIL: {e}\n")

print('Waiting 2 seconds before login...')
time.sleep(2)

# Test 2: Try login initiate
print("[2] Initiate login (send OTP)")
login_payload = {
    "email": test_email
}

try:
    r = requests.post(f"{API_URL}/auth/login", json=login_payload, timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    if r.status_code in [200, 401]:
        print("✓ Response received\n")
    else:
        print(f"Status: {r.status_code}\n")
except Exception as e:
    print(f"✗ FAIL: {e}\n")

# Test 3: Forgot password
print("[3] Forgot password")
forgot_payload = {
    "email": test_email
}

try:
    r = requests.post(f"{API_URL}/auth/forgot-password", json=forgot_payload, timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    if r.status_code == 200:
        print("✓ PASS\n")
    else:
        print("✗ FAIL\n")
except Exception as e:
    print(f"✗ FAIL: {e}\n")

print("Tests complete!")
