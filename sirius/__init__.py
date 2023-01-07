from fastapi import FastAPI

from .database import db
from .routers import auth, warwick_sso

app = FastAPI()
app.include_router(warwick_sso.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"Hello": "World"}


# @app.get("/notes/", response_model=List[Note])
# async def read_notes():
#     query = notes.select()
#     return await database.fetch_all(query)


# @app.post("/notes/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await database.execute(query)
#     return {**note.dict(), "id": last_record_id}
