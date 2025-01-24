from typing import Optional

from fastapi import APIRouter, Depends
from src.dependencies import get_users_average_age, get_users_gender_percentage, get_users_main_cities, \
    get_users_without_email
from src.schemas import User
from src.users_info.service import create_user_info

router = APIRouter()

@router.get("/average-age", response_model=int)
async def get_average_age(average_age: int = Depends(get_users_average_age)):
    return average_age

@router.get("/gender-percentage", response_model=str)
async def get_gender_percentage(gender_percentage: tuple = Depends(get_users_gender_percentage)):
    return f'{gender_percentage[0]}% - девушки, {gender_percentage[1]}% - мужчины'

@router.get("/main-cities", response_model=str)
async def get_main_cities(main_cities: str = Depends(get_users_main_cities)):
    return main_cities

@router.get("/users-without-email", response_model=tuple|str)
async def get_without_email(users_without_email: tuple|str = Depends(get_users_without_email)):
    if type(users_without_email) is tuple:
        return f'{users_without_email[0]}, от общей массы составляет {users_without_email[1]}%'
    else:
        return users_without_email

@router.post("/regist-user", response_model=User)
async def create_user(user: User):
    try:
        await create_user_info(user.login, user.password, user.email, user.age, user.gender, user.city)
        return user
    except Exception as e:
        return {"Error": str(e)}