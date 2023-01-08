from fastapi import APIRouter, Form, Request, status
from fastapi.exceptions import HTTPException

from ..database import db
from ..models.Token import Token
from ..models.User import User, authenticate_user, get_user, users

router = APIRouter(prefix="/users")

@router.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    request.session["user"] = user.username
    return user

@router.post("/logout")
async def logout(request: Request):
    del request.session["user"]