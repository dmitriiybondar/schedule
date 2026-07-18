import enum

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.types import Enum
from database.connection import Base

class UserRole(enum.StrEnum):
    USER = "user"
    ADMIN = "admin"

class SlotState(enum.StrEnum):
    ACTIVE = "active"
    BOOKED = "booked"
    DISABLED = "disabled"

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    phone_number = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

class Slot(Base):
    __tablename__ = "slots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    host_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    state = Column(Enum(SlotState), default=SlotState.ACTIVE, nullable=False)
    client_id = Column(BigInteger)
