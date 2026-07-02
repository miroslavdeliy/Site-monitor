from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.auth import UserRegister
from app.schemas.auth import UserResponse
from app.services.auth_service import register_user

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