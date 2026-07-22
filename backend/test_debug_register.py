"""
Debug test for registration flow.
Simple script to test registration and capture errors.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test data - password does NOT contain name/email
test_user = {
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice.smith@example.com",
    "phone_number": "0771234567",
    "password": "SecurePassword123!@#",
    "role": "CUSTOMER"
}

print("=" * 80)
print("Testing Registration Endpoint")
print("=" * 80)
print(f"\nSending POST {BASE_URL}/api/v1/auth/register")
print(f"Payload: {json.dumps(test_user, indent=2)}")

try:
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code >= 400:
        print("\n❌ REGISTRATION FAILED")
        try:
            print(f"JSON: {json.dumps(response.json(), indent=2)}")
        except:
            pass
    else:
        print("\n✓ REGISTRATION SUCCESSFUL")
        
except Exception as e:
    print(f"\n❌ Request failed: {e}")
    import traceback
    traceback.print_exc()
