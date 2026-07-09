"""
Notification Schemas

Pydantic models for notification management.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE NOTIFICATION
# =====================================================

class NotificationCreate(BaseModel):
    """
    Request schema for creating a notification.
    """

    user_id: int

    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
    )

    message: str = Field(
        ...,
        min_length=5,
        max_length=1000,
    )

    notification_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


# =====================================================
# UPDATE NOTIFICATION
# =====================================================

class NotificationUpdate(BaseModel):
    """
    Update notification.
    """

    is_read: bool


# =====================================================
# NOTIFICATION RESPONSE
# =====================================================

class NotificationResponse(BaseModel):
    """
    Notification response.
    """

    id: int

    user_id: int

    title: str

    message: str

    notification_type: str

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
    