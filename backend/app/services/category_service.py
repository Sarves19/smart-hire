"""
Category Service

Contains business logic for category management.
"""

from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:
    """
    Handles category business logic.
    """

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    # =====================================================
    # CREATE
    # =====================================================

    def create_category(
        self,
        request: CategoryCreate,
    ) -> Category:
        """
        Create a new category.
        """

        existing_category = self.repository.get_by_name(
            request.name
        )

        if existing_category:
            raise ValueError("Category already exists.")

        category = Category(
            name=request.name,
            description=request.description,
            icon=request.icon,
            is_active=True,
        )

        return self.repository.create(category)

    # =====================================================
    # READ
    # =====================================================

    def get_category(
        self,
        category_id: int,
    ) -> Category:
        """
        Get category by ID.
        """

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Category not found.")

        return category

    def list_categories(self) -> list[Category]:
        """
        Return all categories.
        """

        return self.repository.list_categories()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_category(
        self,
        category_id: int,
        request: CategoryUpdate,
    ) -> Category:
        """
        Update category.
        """

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Category not found.")

        if (
            request.name is not None
            and request.name != category.name
        ):
            existing = self.repository.get_by_name(
                request.name
            )

            if existing:
                raise ValueError(
                    "Category name already exists."
                )

            category.name = request.name

        if request.description is not None:
            category.description = request.description

        if request.icon is not None:
            category.icon = request.icon

        if request.is_active is not None:
            category.is_active = request.is_active

        return self.repository.update(category)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_category(
        self,
        category_id: int,
    ) -> None:
        """
        Delete category.
        """

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Category not found.")

        self.repository.delete(category)

        