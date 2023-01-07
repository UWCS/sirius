from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..database import db
from ..models.User import *

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/token", response_model=User)
async def password_login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await get_user(form_data.username)
