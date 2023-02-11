from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from settings import Settings

from .routers import auth, warwick_sso

app = FastAPI()

app.include_router(warwick_sso.router)
# app.include_router(auth.router)

app.add_middleware(
    SessionMiddleware, secret_key=Settings().FAST_API_SECRET_KEY  #  type: ignore
)


# @app.on_event("startup")
# async def startup():
#     await db.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await db.disconnect()


@app.get("/")
async def root():
    return {"Hello": "World"}
