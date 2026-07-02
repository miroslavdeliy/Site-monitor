from pydantic import BaseModel, EmailStr


# Родительский класс регистрации и авторизации
class UserCredentials(BaseModel):
    email: EmailStr
    password: str


#  Регистрация
class UserRegister(UserCredentials):
    pass


# Авторизация
class UserLogin(UserCredentials):
    pass


# Ответ после регистрации
class UserResponse(BaseModel):
    id: int
    email: EmailStr


# Получить токен авторизации
class TokenResponse(BaseModel):
    access_token: str
    token_type: str