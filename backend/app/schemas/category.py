"""
Category Schemas

Pydantic models for category management.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Create Category
# =====================================================

class CategoryCreate(BaseModel):
    """
    Request schema for creating a category.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    icon: Optional[str] = None


# =====================================================
# Update Category
# =====================================================

class CategoryUpdate(BaseModel):
    """
    Request schema for updating a category.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    icon: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================================
# Category Response
# =====================================================

class CategoryResponse(BaseModel):
    """
    Category response schema.
    """

    id: int

    name: str

    description: Optional[str]

    icon: Optional[str]

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

    