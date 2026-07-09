from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import AuthUtils
from database_config import get_db
from db_models import User
from provider_repository import ProviderRepository
from resp_models import UserResponse, ProviderCreate, ReviewResponse, ProviderResponse, ProviderUpdate
from user_repository import ReviewRepository, UserRepository

router = APIRouter()
user_repo = UserRepository()

@router.post("/register/provider", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_provider(user: ProviderCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await user_repo.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email address!"
        )
    user.role = "provider"
    new_user = await user_repo.create_user(db,user)
    return new_user

@router.get("/providers/me/reviews",response_model=list[ReviewResponse])
async def get_my_reviews(db:AsyncSession = Depends(get_db),current_user: User = Depends(AuthUtils.get_current_user)):
    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only providers can access this endpoint."
        )
    if not current_user.provider_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider profile not found for this user."
        )
    reviews = await ReviewRepository.get_reviews_for_provider(db, provider_id=current_user.provider_profile.id)
    return reviews

@router.put("/me/listing", response_model=ProviderResponse, status_code=status.HTTP_200_OK)
async def update_my_listing(update_data: ProviderUpdate, db:AsyncSession = Depends(get_db), current_user: User = Depends(AuthUtils.get_current_user)):
    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only service providers can manage service listings."
        )
    return await ProviderRepository.update_provider_listing(db,current_user.id,update_data)