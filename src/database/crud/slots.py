from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Slot, SlotState

async def create_slot(session: AsyncSession, telegram_id: int, date: str, start_time: str, end_time: str):
    new_slot = Slot(
        user_id = telegram_id,
        date = date,
        start_time = start_time,
        end_time = end_time,
    )

    session.add(new_slot)
    await session.commit()

async def delete_slot(session: AsyncSession, slot_id: int):
    stmt = delete(Slot).where(Slot.id == slot_id)

    await session.execute(stmt)
    await session.commit()

async def get_slot(session: AsyncSession, slot_id: int) -> Slot | None:
    stmt = select(Slot).where(Slot.id == slot_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()

async def change_state(session: AsyncSession, slot_id: int, new_state: SlotState):
    stmt = update(Slot).where(Slot.id == slot_id).values(state = new_state)

    await session.execute(stmt)
    await session.commit(stmt)