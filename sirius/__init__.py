from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import CONFIG

from .database import db
from .routers import users, warwick_sso

app = FastAPI()

app.include_router(warwick_sso.router)
app.include_router(users.router)

app.add_middleware(SessionMiddleware, secret_key=CONFIG.FAST_API_SECRET_KEY)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"Hello": "World"}
