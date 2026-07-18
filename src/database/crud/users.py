from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, UserRole

async def create_user(session: AsyncSession, telegram_id: int, username: str, full_name: str, phone_number: int,  role: UserRole = None):
    new_user = User(
        telegram_id = telegram_id,
        username = username,
        full_name = full_name,
        phone_number = phone_number,
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

async def get_role(session: AsyncSession, telegram_id: int) -> UserRole | None:
    stmt = select(User.role).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def change_params(session: AsyncSession, telegram_id: int, column: str, value: str | UserRole):
    stmt = update(User).where(User.telegram_id == telegram_id).values({column: value})
    
    await session.execute(stmt)
    await session.commit()
