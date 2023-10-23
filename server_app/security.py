from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Cookie, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db


SECRET_KEY = "YOUR_SECRET_KEY"  # Change this to a random, secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class NotAuthenticatedException(Exception):
    pass


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    token = token.split("Bearer ")[-1]  # Remove the "Bearer " prefix.
    # print(f"Decoding token: {token}")  # Debug line
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise e


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise NotAuthenticatedException()

    token_data = token.split("Bearer ")[-1]

    try:
        payload = decode_access_token(token_data)
        username: str = payload.get("sub")
        token_role: str = payload.get("role")

        user = db.query(User).filter(User.username == username).first()

        if user is None or user.role != token_role:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

    except Exception as e:
        raise e


def ensure_logged_in(token: str = Cookie(None)):
    if not token:
        return RedirectResponse(url="/login")
    return token
