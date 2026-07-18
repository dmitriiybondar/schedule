from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_telegram_id
from src.database.connection import get_db
from src.database.crud.slots import create_slot, delete_slot, get_slot, change_state, book_slot

router = APIRouter()

class CreateSlotInfo(BaseModel):
    date: str
    start_time: str
    end_time: str

@router.post("/create")
async def create_slot_api(data: CreateSlotInfo, session: AsyncSession = Depends(get_db), host_id: int = Depends(get_telegram_id)):
    await create_slot(
        session=session,
        telegram_id=host_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time
    )

    return {"ok": True}