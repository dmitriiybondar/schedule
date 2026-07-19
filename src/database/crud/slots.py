from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Slot, SlotState

async def create_slot(session: AsyncSession, telegram_id: int, date: str, start_time: str, end_time: str):
    new_slot = Slot(
        host_id = telegram_id,
        date = date,
        start_time = start_time,
        end_time = end_time,
    )
    session.add(new_slot)

    await session.commit()
    await session.refresh(new_slot)
    
    return new_slot.id


async def delete_slot(session: AsyncSession, slot_id: int, host_id: int):
    stmt = delete(Slot).where(Slot.id == slot_id, Slot.host_id == host_id)
    result = await session.execute(stmt)

    await session.commit()
    return result.rowcount > 0


async def get_slot(session: AsyncSession, slot_id: int) -> Slot | None:
    stmt = select(Slot).where(Slot.id == slot_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def change_state(session: AsyncSession, slot_id: int, new_state: SlotState, host_id: int):
    stmt = update(Slot).where(Slot.id == slot_id, Slot.host_id == host_id).values(state = new_state)

    await session.execute(stmt)
    await session.commit()


async def book_slot(session: AsyncSession, slot_id: int, user_id: int):
    stmt = update(Slot).where(Slot.id == slot_id).values(state = SlotState.BOOKED, client_id = user_id)

    await session.execute(stmt)
    await session.commit()


async def get_by_id(session: AsyncSession, slot_id: int) -> Slot | None:
    stmt = select(Slot).where(Slot.id == slot_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()