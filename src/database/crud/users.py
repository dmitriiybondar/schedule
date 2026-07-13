from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def create_user(session: AsyncSession, telegram_id: int, username: str, full_name: str, role: str):
    new_user = User(
        telegram_id = telegram_id,
        username = username,
        full_name = full_name,
        role = role
    )

    session.add(new_user)
    await session.commit()


async def delete_user(session: AsyncSession, telegram_id: int):
    stmt = delete(User).where(User.telegram_id == telegram_id)

    await session.execute(stmt)
    await session.commit()

async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()

async def change_role(session: AsyncSession, telegram_id: int, new_role: str):
    stmt = update(User).where(User.telegram_id == telegram_id).values(role = new_role)
    
    await session.execute(stmt)
    await session.commit()