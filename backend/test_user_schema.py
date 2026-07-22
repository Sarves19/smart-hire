from datetime import datetime

from app.schemas.user import UserResponse

user = UserResponse(
    id=1,
    first_name="Sarves",
    last_name="Suresh",
    email="sarves@example.com",
    phone_number="0771234567",
    role="CUSTOMER",
    is_active=True,
    is_verified=False,
    created_at=datetime.now(),
    updated_at=datetime.now(),
)

print(user)
