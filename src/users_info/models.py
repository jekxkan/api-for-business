from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


class Gender(Enum):
    male = "male"
    female = "female"


Base = declarative_base()


class UserInfo(Base):
    """
    Модель пользователя, представляющая собой запись в таблице users_info
    """

    __tablename__ = "users_info"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    login: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    male: Mapped[Optional[Gender]] = mapped_column(String(20))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    registrated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(tz=timezone.utc), index=True
    )
    __table_args__ = (Index("idx_email", "email", postgresql_using="btree"),)
