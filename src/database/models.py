import enum

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum
from .connection import Base

class UserRole(enum.StrEnum):
    USER = "user"
    HOST = "host"

class SlotState(enum.StrEnum):
    ACTIVE = "active"
    BOOKED = "booked"
    DISABLED = "disabled"

class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.USER
    )

class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    date: Mapped[str] = mapped_column(String)
    start_time: Mapped[str] = mapped_column(String)
    end_time: Mapped[str] = mapped_column(String)
    state: Mapped[SlotState] = mapped_column(
        Enum(SlotState, name="slot_state_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=SlotState.ACTIVE
    )
    client_id: Mapped[int | None] = mapped_column(BigInteger)
