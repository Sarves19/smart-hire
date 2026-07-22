from app.schemas.auth import RegisterRequest

user = RegisterRequest(
    first_name="Sarves",
    last_name="Suresh",
    email="sarves@example.com",
    phone_number="0771234567",
    password="Password@123",
    role="CUSTOMER",
)

print(user)