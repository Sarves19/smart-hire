
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from database_config import get_db
from db_models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "SUPER_SECRET_SMART_HIRE_KEY_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

class AuthUtils:
    @staticmethod
    async def hash_password(password:str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def verify_password(plain_password:str, hashed_password:str) -> bool:
        return pwd_context.verify(plain_password,hashed_password)

    @staticmethod
    async def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
        return encode_jwt

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW_Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception

        from user_repository import UserRepository

        user_repo = UserRepository()
        user = await user_repo.get_user_by_email(db, email=email)
        if user is None:
            raise credentials_exception
        return user
