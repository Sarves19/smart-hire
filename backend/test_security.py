from app.core.security import password_manager

password = "SmartHire@2026"

hashed = password_manager.hash_password(password)

print("Original :", password)
print("Hashed   :", hashed)

print(
    "Verification:",
    password_manager.verify_password(
        password,
        hashed,
    ),
)
