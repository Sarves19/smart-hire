from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, ForeignKey, func, Integer, Float, Boolean, DateTime, Text, text, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__  = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone:Mapped[str] = mapped_column(String(15), nullable=False,unique=True,index=True)
    role: Mapped[str] = mapped_column(String(20), default="customer", nullable=False)

    admin_profile = relationship("Admin", back_populates="user", uselist=False,cascade="all, delete-orphan")

    my_bookings = relationship("Booking", foreign_keys="[Booking.customer_id]",back_populates="customer")
    reviews_given = relationship("Review", foreign_keys="[Review.customer_id]", back_populates="customer")
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

    received_bookings = relationship("Booking", foreign_keys="[Booking.provider_id]", back_populates="provider")
    reviews_received = relationship("Review", foreign_keys="[Review.provider_id]", back_populates="provider")

    user = relationship("User",back_populates="provider_profile")

class Admin(Base):
    __tablename__ = 'admins'

    admin_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),unique=True, nullable=False)

    user = relationship("User",back_populates="admin_profile")




class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Pending")
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    booking_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    customer = relationship("User", foreign_keys=[customer_id], back_populates="my_bookings")
    provider = relationship("Provider", foreign_keys=[provider_id], back_populates="received_bookings")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="booking")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    rating : Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(String(500), nullable=True)
    review_date: Mapped[datetime]= mapped_column(DateTime(timezone=True))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="reviews_given")
    provider = relationship("Provider", foreign_keys=[provider_id], back_populates="reviews_received")


class Category(Base):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status : Mapped[bool] = mapped_column(Boolean, default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    services = relationship("Service",back_populates="category")

class Service(Base):
    __tablename__ = 'services'

    service_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="services")

class Notification(Base):
    __tablename__ = "notifications"
    notification_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(100),nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean,default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    method: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Pending", server_default="Pending")
    payment_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), server_default=func.now())
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="payments")



