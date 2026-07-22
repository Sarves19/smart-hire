from app.core.config import settings

print("Application :", settings.APP_NAME)
print("Environment :", settings.APP_ENV)
print("Database URL configured:", bool(settings.DATABASE_URL))
print("Host        :", settings.HOST)
