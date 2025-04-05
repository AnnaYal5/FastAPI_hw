from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import User
from project.db import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
tokens = {}

def fake_hash_password(password: str):
    return 'hashed-' + password

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    username = tokens.get(token)
    if not username or username not in users_db:
        raise HTTPException(status_code=401, detail='Invalid authentication credentials')
    return users_db[username]


def authenticate_user(username: str, password: str) -> User | None:
    user = users_db.get(username)
    if not user or user.password != fake_hash_password(password):
        return None
    return user
