import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.host.slots import router as host_slot_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # В продакшні краще вказати конкретний домен
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(host_slot_router, prefix="/api")


# BOT_TOKEN = os.getenv("BOT_TOKEN")
# bot = Bot(token=BOT_TOKEN)

# class BookingRequest(BaseModel):
#     date: str
#     time: str
#     comment: str
#     initData: str


# @app.post("/api/booking")
# async def create_booking(request: BookingRequest):
#     try:
#         web_app_data = safe_parse_webapp_init_data(
#             token=BOT_TOKEN, 
#             init_data=request.initData
#         )
        
#         user_id = web_app_data.user.id
        
#         text = (
#             f"<b>Нове бронювання підтверджено!</b>\n\n"
#             f"📅 Дата: {request.date}\n"
#             f"⏰ Час: {request.time}\n"
#             f"📝 Коментар: {request.comment}"
#         )
        
#         await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
#         logger.info(f"Успішне бронювання для юзера {user_id}")
        
#         return {"ok": True, "message": "Бронювання успішне"}
        
#     except ValueError:
#         logger.error("Помилка валідації initData")
#         raise HTTPException(status_code=403, detail="Недійсні дані авторизації Telegram")
        
#     except Exception as e:
#         logger.error(f"Помилка сервера під час бронювання: {e}")
#         raise HTTPException(status_code=500, detail="Внутрішня помилка сервера")
