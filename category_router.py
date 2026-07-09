from typing import List

from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import AuthUtils
from database_config import get_db
from db_models import User, Category
from resp_models import CategoryResponse, CategoryCreate

router = APIRouter()

# 1. CREATE CATEGORY (Admin Only)
@router.post("/", response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate, db:AsyncSession = Depends((get_db)), current_user: User = Depends(AuthUtils.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.Only admin can manage categories."
        )
    query = select(Category).where(Category.name == category_data.name)
    result = await db.execute(query)
    existing_category = result.scalar()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    new_category = Category(
        name=category_data.name,
        description=category_data.description
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


# 2. GET ALL CATEGORIES (Public)
@router.get("/",response_model=List[CategoryResponse])
async def get_all_categories(db:AsyncSession = Depends(get_db)):
    query = select(Category).where(Category.status == True)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories