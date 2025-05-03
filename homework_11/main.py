# Створить FastAPI додаток із кількома маршрутами, ви можете використовувати домашнє завдання з минулого модуля як приклад додатку.
# Переконайтесь, що Swagger UI був доступний і працював з вашим API.
# Піся цього, додайте детальні описи до кожного маршруту використовуючи Swagger. Зробіть скриншоти, як можна тестувати маршрути API через Swagger UI.
#
# Додайте анотації та коментарі до кожного маршруту у вашому API.
# Додайте описи, теги та сумарі до кожного маршруту.
# Внесіть зміни в OpenAPI специфікацію, запишіть, які зміни були зроблені та чому.

from fastapi import FastAPI, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uuid

app = FastAPI(
    description="Простий FastAPI додаток для автентифікації користувачів.",
)


#база данних
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "full_name": "Admin User",
    },
    "user": {
        "username": "user",
        "password": "user123",
        "full_name": "Normal User",
    },
}

# Назва cookie для збереження сесії
SESSION_COOKIE_NAME = "session_id"


# Модель токену
class Token(BaseModel):
    access_token: str
    token_type: str

# Модель користувача
class User(BaseModel):
    username: str
    full_name: str


def create_session_id():
    """
    Унікальний ID сесії.
    """
    return str(uuid.uuid4())


@app.post("/token", response_model=Token, tags=["Authentication"], summary="Отримати токен доступу")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = fake_users_db.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    session_id = create_session_id()


@app.get("/users/me", response_model=User, tags=["Users"], summary="Отримати інформацію про себе")
async def read_users_me(session_id: str = Cookie(None)) -> User:
    """
    Отримати інформацію про поточного користувача за допомогою сесії.
    Повертає дані користувача.
    """
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid session found.")


    user = None
    for username, user_data in fake_users_db.items():
        if session_id:
            user = user_data
            break

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.")

    return user
