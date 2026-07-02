from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserResponse, TokenResponse
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Создаём POST-эндпоинт /register
# response_model говорит FastAPI,
# что ответ должен соответствовать модели UserResponse
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
        # Получаем данные пользователя из JSON тела запроса
        user_data: UserRegister,
        # Получаем сессию подключения к базе данных
        db: Session = Depends(get_db)
):
    # Пытаемся зарегистрировать пользователя
    user = register_user(
        db,
        user_data
    )

    # Если пользователь уже существует
    if user is None:
        raise HTTPException(
            status_code=400,    # Ошибка в запросе клиента
            detail="User already exists"
        )

    # Возвращаем созданного пользователя
    # FastAPI автоматически преобразует объект в JSON
    # и оставит только поля, указанные в UserResponse
    return user


# Создаём POST-эндпоинт /login
# response_model указывает, что ответ должен соответствовать модели TokenResponse
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
        # Получаем username и password из формы
        form_data: OAuth2PasswordRequestForm = Depends(),

        # Получаем объект подключения к базе данных
        db: Session = Depends(get_db)
):
    # Проверяем существование пользователя и правильность пароля
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    # Если пользователь не найден или пароль неверный
    if user is None:
        raise HTTPException(
            status_code=401,    # HTTP статус "Не авторизован"
            detail="Invalid credentials"
        )

    # Создаём JWT-токен
    # В поле "sub" (subject) обычно записывают идентификатор пользователя
    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    # Возвращаем токен клиенту
    # FastAPI автоматически преобразует объект в JSON
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