from fastapi import FastAPI
from .routers import warwick_sso


app = FastAPI()
app.include_router(warwick_sso.router)


@app.get("/")
async def root():
    return {"Hello": "World"}
