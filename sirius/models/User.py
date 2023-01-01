from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func

from ..database import metadata

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
    email: str
    first_name: str
    last_name: str
