import databases
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from config import CONFIG

db = databases.Database(CONFIG.DATABASE_CONNECTION)
metadata = sqlalchemy.MetaData()

engine = create_async_engine(CONFIG.DATABASE_CONNECTION)
