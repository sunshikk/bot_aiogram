from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete

async def set_user(tg_id) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, moneyy=0))
            await session.commit()

async def update_user(tg_id, moneyy):
    async with async_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(moneyy=moneyy)
        await session.execute(stmt)
        await session.commit()