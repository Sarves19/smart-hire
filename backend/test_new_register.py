import requests
import json
import random

# Generate valid Sri Lankan phone and random email/password
email = "smartuser" + str(random.randint(100000, 999999)) + "@example.com"
phone = "+947" + str(random.randint(10000000, 99999999))
password = "SecurePass2024!"

payload = {
    "email": email,
    "first_name": "Smart",
    "last_name": "Hire",
    "phone_number": phone,
    "password": password,
    "role": "CUSTOMER"
}

print(f"Registering with email: {payload['email']}")
print(f"Phone: {payload['phone_number']}")
response = requests.post('http://127.0.0.1:8000/api/v1/auth/register', json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    print("\n✓ SUCCESS! Registration created with status 201!")
elif response.status_code == 400:
    print("\n✗ Client error - invalid request")
elif response.status_code == 409:
    print("\n✗ Conflict - email/phone already exists")
elif response.status_code == 422:
    print("\n✗ Validation failed")
else:
    print(f"\n✗ Unexpected status: {response.status_code}")
