# Вам необхідно створити чат-сервер використовуючи FastAPI і WebSocket,
# який дозволить користувачам обмінюватися повідомленнями в реальному часі.
# Завдання включає реалізацію автентифікації, обробки повідомлень,
# ведення стану сесій, і впровадження заходів безпеки.
# Реалізувати ендпоінт, який відкриває WebSocket-з'єднання для кожного користувача.
# Користувачі повинні автентифікуватися перед відправкою повідомлень. Можете використовувати JWT або інші токени автентифікації.
# Користувачі повинні мати змогу відправляти та отримувати повідомлення.
# Важливо впровадити санітізацію вхідних даних, щоб запобігти XSS та іншим атакам.
# Сервер повинен відстежувати активні сесії користувачів та коректно обробляти відключення.
# Ваше рішення повинно бути готове до масштабування, здатне обслуговувати велику кількість одночасних з'єднань.
# Забезпечити безпечне шифрування з'єднань та впровадити заходи для захисту від CSRF та інших веб-загроз.
# Написати тести для перевірки функціоналу сервера, зокрема тестування автентифікації,
# відправки/прийому повідомлень, та ведення стану сесій.
#

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from typing import Dict
import html
import uvicorn



app = FastAPI()

bd = {}
active_connections: Dict[str, WebSocket] = {}

SECRET_KEY = ""
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    pass

class Token(BaseModel):
    token: str


@app.post("/register")
def register(user: UserCreate):
    if user.email in bd:
        raise HTTPException(status_code=400, detail="user already register")
    bd[user.email] = user.password
    return {"massage": "user registered" }


@app.post('/token', response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user_email = from_data.username
    password = from_data.password
    if bd.get(user_email) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user_email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    active_connections[email] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            clean = html.escape(data)
            for user, conn in active_connections.items():
                await conn.send_text(f"{email}: {clean}")
    except WebSocketDisconnect:
        del active_connections[email]