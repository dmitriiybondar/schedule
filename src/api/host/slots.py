from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_telegram_id
from src.database.connection import get_db
from src.database.crud.slots import create_slot, delete_slot, change_state, get_slots, book_slot, get_slot
from src.database.models import SlotState

router = APIRouter()

class CreateSlotInfo(BaseModel):
    date: str
    start_time: str
    end_time: str

class StateChangeInfo(BaseModel):
    slot_id: int
    state: SlotState


@router.post("/create")
async def create_slot_api(data: CreateSlotInfo, session: AsyncSession = Depends(get_db), host_id: int = Depends(get_telegram_id)):
    slot_id = await create_slot(
        session=session,
        telegram_id=host_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time
    )

    return {"ok": True, "slot_id": slot_id}


@router.delete("/delete/{slot_id}")
async def delete_slot_api(slot_id: int, session: AsyncSession = Depends(get_db), host_id: int = Depends(get_telegram_id)):
    is_deleted = await delete_slot(
        session=session,
        slot_id=slot_id,
        host_id=host_id
    )

    if not is_deleted:
        raise HTTPException(status_code=404, detail="Слот не знайдено або він вам не належить")

    return {"ok": True}


@router.post("/change-state")
async def change_state_api(data: StateChangeInfo, session: AsyncSession = Depends(get_db), host_id: int = Depends(get_telegram_id)):
    await change_state(
        session=session,
        slot_id=data.slot_id,
        new_state=data.state,
        host_id=host_id
    )

    return {"ok": True}


@router.get("/admin-slot-list/{date}")
async def load_slots(date: str, session: AsyncSession = Depends(get_db), host_id: int = Depends(get_telegram_id)):
    result = await get_slots(
        session=session, 
        host_id=host_id, 
        date=date
    )

    return result