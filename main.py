from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware
from payment_router import router as payment_router
from service_router import router as service_router
from notification_router import router as notification_router
from auth_utils import AuthUtils
from provider_router import router as provider_router
from dashboard_router import router as dashboard_router
from db_models import Base, Admin
from database_config import engine, async_session
from user_router import router as user_router
from booking_router import router as booking_router
from category_router import router as category_router
from sqlalchemy.future import select
from db_models import User


async def seed_admin_user():
    async with async_session()as db:
        query = select(User).where(User.email == "admin@smarthire.com")
        result = await db.execute(query)
        admin_exists = result.scalar()

        if not admin_exists:
            hashed_password = AuthUtils.hash_password("Admin123")

            super_admin = User(
                username="Super Admin",
                email="admin@smarthire.com",
                password=hashed_password,
                phone="0771234567",
                role="admin",

            )
            db.add(super_admin)
            await db.flush()

            admin_profile = Admin(
                user_id=super_admin.id,
            )
            db.add(admin_profile)
            await db.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")



@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")
    await seed_admin_user()
    yield


app = FastAPI(title="Smart Hire API",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods={"*"},
    allow_headers={"*"},

)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(provider_router, prefix="/provider", tags=["Provider"])
app.include_router(category_router, prefix="/category", tags=["Category"])
app.include_router(service_router, prefix="/service", tags=["Service"])
app.include_router(notification_router, prefix="/notification", tags=["Notification"])
app.include_router(payment_router, prefix="/Payment", tags=["Payment"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Hire API"}

