from datetime import datetime

from sqlalchemy import String, ForeignKey, func, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__  = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="customer", nullable=False)

    my_bookings = relationship("Booking", foreign_keys="[Booking.customer_id]",back_populates="customer")
    received_bookings = relationship("Booking", foreign_keys="[Booking.provider_id]", back_populates="provider")


    provider_profile = relationship("Provider", uselist=False, back_populates="user")

class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_type: Mapped[str] = mapped_column(String(255), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hourly_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False)

    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),unique=True, nullable=False)

    user = relationship("User",back_populates="provider_profile")



class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Pending")
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    booking_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    customer = relationship("User", foreign_keys=[customer_id], back_populates="my_bookings")
    provider = relationship("User", foreign_keys=[provider_id], back_populates="received_bookings")

