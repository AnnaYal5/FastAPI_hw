# Створити додаток FastAPI, який демонструє використання базової автентифікації за допомогою HTTPBasic.
# Реалізувати OAuth2 в додатку FastAPI.
# Створити маршрути для автентифікації через OAuth2, включаючи ендпойнт для отримання токена.

from fastapi import FastAPI, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uuid

app= FastAPI()

#бд
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

SESSION_COOKIE_NAME = "session_id"


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    full_name: str


def create_session_id():
    return str(uuid.uuid4())


d@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    session_id = create_session_id()


    return {"access_token": session_id, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(session_id: str = Cookie(None)):
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
