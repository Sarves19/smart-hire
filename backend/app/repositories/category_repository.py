"""
Category Repository

Handles all database operations related to categories.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    """
    Repository responsible for Category operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        category: Category,
    ) -> Category:
        """
        Create a category.
        """

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        category_id: int,
    ) -> Optional[Category]:
        """
        Get category by ID.
        """

        stmt = select(Category).where(
            Category.id == category_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_name(
        self,
        name: str,
    ) -> Optional[Category]:
        """
        Get category by name.
        """

        stmt = select(Category).where(
            Category.name == name
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def list_categories(self) -> list[Category]:
        """
        Return all categories.
        """

        stmt = select(Category)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        category: Category,
    ) -> Category:
        """
        Update category.
        """

        self.db.commit()
        self.db.refresh(category)

        return category

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        category: Category,
    ) -> None:
        """
        Delete category.
        """

        self.db.delete(category)
        self.db.commit()