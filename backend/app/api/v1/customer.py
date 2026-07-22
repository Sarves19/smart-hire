"""
Customer Profile API

Provides endpoints for customer profile management.
"""

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.customer import (
    CustomerProfileCreate,
    CustomerProfileResponse,
    CustomerProfileUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)

ALLOWED_IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_PROFILE_IMAGE_SIZE = 5 * 1024 * 1024


def has_expected_image_signature(content_type: str, content: bytes) -> bool:
    """Reject files that only claim to be images through their MIME header."""
    signatures = {
        "image/jpeg": (b"\xff\xd8\xff",),
        "image/png": (b"\x89PNG\r\n\x1a\n",),
        "image/webp": (b"RIFF",),
    }
    if not content.startswith(signatures[content_type]):
        return False
    return content_type != "image/webp" or len(content) >= 12 and content[8:12] == b"WEBP"


# =====================================================
# CREATE PROFILE
# =====================================================

@router.post(
    "/profile",
    response_model=CustomerProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: CustomerProfileCreate,
    current_user: User = Depends(
        require_role(UserRole.CUSTOMER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Create customer profile.
    """

    service = CustomerService(db)

    try:
        return service.create_profile(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# GET PROFILE
# =====================================================

@router.get(
    "/profile",
    response_model=CustomerProfileResponse,
)
def get_profile(
    current_user: User = Depends(
        require_role(UserRole.CUSTOMER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Get customer profile.
    """

    service = CustomerService(db)

    try:
        return service.get_profile(current_user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# UPDATE PROFILE
# =====================================================

@router.put(
    "/profile",
    response_model=CustomerProfileResponse,
)
def update_profile(
    request: CustomerProfileUpdate,
    current_user: User = Depends(
        require_role(UserRole.CUSTOMER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Update customer profile.
    """

    service = CustomerService(db)

    try:
        return service.update_profile(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/profile/image", response_model=CustomerProfileResponse)
async def upload_profile_image(
    image: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    """Upload a bounded, allow-listed profile image for the current customer."""
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Use a JPEG, PNG, or WebP image.")
    content = await image.read(MAX_PROFILE_IMAGE_SIZE + 1)
    if not content or len(content) > MAX_PROFILE_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image must be between 1 byte and 5 MB.")
    if not has_expected_image_signature(image.content_type, content):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Uploaded file content is not a valid image type.")

    image_name = f"{uuid4()}{ALLOWED_IMAGE_TYPES[image.content_type]}"
    image_directory = Path(__file__).resolve().parents[3] / "uploads" / "profile-images"
    image_directory.mkdir(parents=True, exist_ok=True)
    (image_directory / image_name).write_bytes(content)
    image_url = f"/uploads/profile-images/{image_name}"

    service = CustomerService(db)
    try:
        service.get_profile(current_user)
        return service.update_profile(current_user, CustomerProfileUpdate(profile_image=image_url))
    except ValueError as error:
        if "not found" not in str(error):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
        return service.create_profile(current_user, CustomerProfileCreate(profile_image=image_url))
    
