from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from server.db.base import AsyncSessionLocal
from functools import wraps

@asynccontextmanager
async def async_session_scope():
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit() # 将数据保存至数据库中
    except Exception as e:
        await session.rollback() # 如果发生异常回滚
        raise e
    finally:
        await session.close() # 释放数据库连接

def with_async_session(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        async with async_session_scope() as session:
            return await f(session, *args, **kwargs)
    return wrapper

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db



