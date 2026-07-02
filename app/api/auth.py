from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.database import get_db
from app.schemas.auth import UserRegister
from app.schemas.auth import UserResponse
from app.services.auth_service import register_user
from app.core.security import create_access_token
from app.schemas.auth import UserLogin
from app.schemas.auth import TokenResponse
from app.services.auth_service import authenticate_user
from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    user = register_user(
        db,
        user_data
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return TokenResponse(
        access_token=access_token
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def me(
        current_user: User = Depends(
            get_current_user
        )
):
    return current_user