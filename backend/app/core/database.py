"""
Database Configuration Module

Configures the SQLAlchemy engine, session management,
and database dependency injection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# =====================================================
# SQLAlchemy Engine
# =====================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# =====================================================
# Session Factory
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# =====================================================
# Database Dependency
# =====================================================

def get_db():
    """
    Provides a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()