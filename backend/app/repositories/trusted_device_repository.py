"""
Trusted Device Repository

Data access layer for trusted devices.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.models.trusted_device import TrustedDevice

logger = logging.getLogger("smart_hire.repositories")


class TrustedDeviceRepository:
    """
    Repository for trusted device operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, device: TrustedDevice) -> TrustedDevice:
        """Create a new trusted device."""
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        logger.info(
            "Trusted device created: user_id=%s device_fingerprint=%s",
            device.user_id,
            device.device_fingerprint[:16],
        )
        return device

    def get_by_fingerprint(self, device_fingerprint: str) -> TrustedDevice | None:
        """Get a trusted device by fingerprint."""
        device = self.db.query(TrustedDevice).filter(
            TrustedDevice.device_fingerprint == device_fingerprint
        ).first()
        return device

    def get_by_user_and_fingerprint(
        self,
        user_id: int,
        device_fingerprint: str,
    ) -> TrustedDevice | None:
        """Get a specific trusted device for a user."""
        device = self.db.query(TrustedDevice).filter(
            TrustedDevice.user_id == user_id,
            TrustedDevice.device_fingerprint == device_fingerprint,
        ).first()
        return device

    def get_all_by_user(self, user_id: int) -> list[TrustedDevice]:
        """Get all trusted devices for a user."""
        devices = self.db.query(TrustedDevice).filter(
            TrustedDevice.user_id == user_id,
        ).all()
        return devices

    def get_valid_by_user(self, user_id: int) -> list[TrustedDevice]:
        """Get all valid (active and not expired) trusted devices for a user."""
        devices = self.db.query(TrustedDevice).filter(
            TrustedDevice.user_id == user_id,
            TrustedDevice.is_active == True,
            TrustedDevice.expires_at > datetime.now(timezone.utc),
        ).all()
        return devices

    def update_last_used(self, device: TrustedDevice) -> TrustedDevice:
        """Update the last used timestamp for a device."""
        device.last_used_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(device)
        return device

    def deactivate(self, device: TrustedDevice) -> TrustedDevice:
        """Deactivate a trusted device."""
        device.is_active = False
        self.db.commit()
        self.db.refresh(device)
        logger.info(
            "Trusted device deactivated: user_id=%s device_fingerprint=%s",
            device.user_id,
            device.device_fingerprint[:16],
        )
        return device

    def delete(self, device_id: int) -> bool:
        """Delete a trusted device."""
        result = self.db.execute(
            delete(TrustedDevice).where(TrustedDevice.id == device_id)
        )
        self.db.commit()
        affected = result.rowcount
        if affected > 0:
            logger.info("Trusted device deleted: device_id=%s", device_id)
        return affected > 0

    def delete_all_by_user(self, user_id: int) -> int:
        """Delete all trusted devices for a user."""
        result = self.db.execute(
            delete(TrustedDevice).where(TrustedDevice.user_id == user_id)
        )
        self.db.commit()
        affected = result.rowcount
        logger.info(
            "All trusted devices deleted for user: user_id=%s count=%s",
            user_id,
            affected,
        )
        return affected

    def cleanup_expired(self) -> int:
        """Remove expired trusted devices."""
        result = self.db.execute(
            delete(TrustedDevice).where(
                TrustedDevice.expires_at <= datetime.now(timezone.utc)
            )
        )
        self.db.commit()
        affected = result.rowcount
        if affected > 0:
            logger.info("Expired trusted devices cleaned up: count=%s", affected)
        return affected
