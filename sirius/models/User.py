import secrets
import string
from datetime import datetime
from typing import Any

from passlib.hash import argon2
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func

from ..database import db, metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(100), unique=True, nullable=False),
    Column("password", String(256), nullable=False),
    Column("email", String(256), nullable=False),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("last_login", DateTime, server_default=func.now()),
)


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
    query = users.select().where(users.c.username == username)
    users_found = await db.fetch_all(query)
    if len(users_found) == 0:
        return None
    user = users_found[0]._mapping
    return User(**user)


async def create_user_from_warwick_sso(data: dict[str, list[str]]):
    username = data["UniversityIDUnscoped"][0]
    email = data["urn:oid:0.9.2342.19200300.100.1.3"][0]
    first_name = data["urn:oid:2.5.4.42"][0]
    last_name = data["urn:oid:2.5.4.4"][0]
    user = await get_user(username)
    if user is not None:
        query = users.update().where(users.c.username == username)
        query = query.values(email=email, first_name=first_name, last_name=last_name, last_login=func.now())
    else:
        password = "".join(
            secrets.choice(string.ascii_letters + string.digits) for i in range(32)
        )
        password_hash = argon2.hash(password)
        query = users.insert().values(
            username=username,
            password=password_hash,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    await db.execute(query)
    return await get_user(username)
