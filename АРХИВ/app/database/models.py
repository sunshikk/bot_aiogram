from sqlalchemy import BigInteger, String, ForeignKey, MetaData, Table, select 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker 
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession 
 
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3') 
 
async_session = async_sessionmaker(engine) 
 
 
metadata = MetaData() 
variables = Table('users', metadata) 
 
class Base(AsyncAttrs, DeclarativeBase): 
    pass 
 
class User(Base): 
    __tablename__ = 'users' 
 
    id: Mapped[int] = mapped_column(primary_key=True) 
    tg_id = mapped_column(BigInteger) 
    moneyy: Mapped[int] = mapped_column() 
 
async def async_main(): 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 
 
async def fetch_value(key): 
    async with async_session() as session: 
        async with session.begin(): 
            # Создание запроса для получения значения по ключу 
            stmt = select(variables.c.values).where(variables.c.key == key) 
            result = await session.execute(stmt) 
            value = result.scalar_one_or_none()  # Получаем одно значение или None 
            return value