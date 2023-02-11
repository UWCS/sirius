import secrets
import string
from datetime import datetime

from passlib.hash import argon2
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    last_login: datetime


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


async def get_user(username: str):
    pass


async def create_user_from_warwick_sso(data: dict[str, list[str]]):
    pass


async def authenticate_user(username: str, password: str):
    pass
