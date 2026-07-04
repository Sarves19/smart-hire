from fastapi import FastAPI
from contextlib import asynccontextmanager
from db_models import Base
from database_config import engine
from user_router import router as user_router
from booking_router import router as booking_router



@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")
    yield

app = FastAPI(title="Smart Hire API",lifespan=lifespan)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Hire API"}

