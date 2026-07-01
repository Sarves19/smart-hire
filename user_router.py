from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from auth_utils import AuthUtils
from database_config import get_db
from db_models import User
from resp_models import UserResponse, CustomerCreate, ProviderCreate, TokenResponse, LoginRequest
from user_repository import UserRepository

router = APIRouter()
user_repo = UserRepository()

@router.post("/register/customer", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_customer(user: CustomerCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await user_repo.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail="User already exists with this email address!"
        )
    user.role = "customer"
    new_user = await user_repo.create_user(db,user)
    return new_user


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

@router.post("/login", response_model=TokenResponse)
async def login(login_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    db_user = await user_repo.get_user_by_email(db, login_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    is_password_correct = await AuthUtils.verify_password(login_data.password, db_user.password)
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token_data = {"sub": db_user.email, "role": db_user.role}
    access_token = await AuthUtils.create_access_token(data=token_data)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=db_user.role
    )

@router.get("/me",response_model=UserResponse)
async def get_me(current_user: User = Depends(AuthUtils.get_current_user)):
    return current_user
