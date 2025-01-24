from enum import Enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import mapped_column, Mapped, declarative_base
from sqlalchemy import Index

class Gender(Enum):
    male = "male"
    female = "female"

Base = declarative_base()

class UserInfo(Base):

    __tablename__ = "users_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    male: Mapped[Optional[Gender]] = mapped_column(String(20))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    registrated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    __table_args__ = (
        Index(
            "idx_login_and_registrated_at", "login", "registrated_at", postgresql_using="btree"
        ),
    )