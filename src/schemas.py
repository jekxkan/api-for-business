from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class User(BaseModel):
    """
    Модель пользователя, описывающая его основные атрибуты
    """

    login: str = Field(min_length=1, max_length=20)
    password: str = Field(
        min_length=8, max_length=20, pattern=r"[A-Za-z\d!#$%^&*]"
    )
    email: Optional[str] = Field(
        min_length=8, max_length=20, pattern=r"^[A-Za-z\d._%+-]+@mail\.com$"
    )
    age: int = Field(ge=18)
    gender: str = Field(min_length=1, max_length=10)
    city: str = Field(min_length=1, max_length=50)

    @validator("age")
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Минимальный возраст 18 лет")
        return value
