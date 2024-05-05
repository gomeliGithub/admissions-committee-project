from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

Session = async_sessionmaker()

MYSQL_DATABASE_URL: str | URL = 'mysql+aiomysql://root:<password>@localhost/admissionscommitteeprojectdb[?<options>]'

engine: AsyncEngine = create_async_engine(
    MYSQL_DATABASE_URL, echo = True, connect_args = { 'check_same_thread': False }
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(autocommit = False, autoflush = False, bind = engine, expire_on_commit = False)

Base = declarative_base()

def bind_engine ():
    Base.metadata.bind = engine
    Session.configure(bind = engine)

async def get_async_database_session ():
    databaseSession = SessionLocal()

    try:
        yield databaseSession
    finally:
        await databaseSession.close()