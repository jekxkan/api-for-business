from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import Dependencies
from src.schemas import User
from src.users_info.service import DBService

router = APIRouter()
dependence = Dependencies()
db_service = DBService()


@router.get("/average-age", response_model=int)
async def get_average_age(
    average_age: int = Depends(dependence.get_users_average_age),
):
    return average_age


@router.get("/gender-percentage", response_model=str)
async def get_gender_percentage(
    gender_percentage: tuple[float, float] = Depends(
        dependence.get_users_gender_percentage
    ),
):
    return (
        f"{gender_percentage[0]}% - девушки, {gender_percentage[1]}% - мужчины"
    )


@router.get("/main-cities", response_model=str)
async def get_main_cities(
    main_cities: str = Depends(dependence.get_users_main_cities),
):
    return main_cities


@router.get("/users-without-email", response_model=tuple | str)
async def get_without_email(
    users_without_email: tuple | str = Depends(
        dependence.get_users_without_email
    ),
):
    if type(users_without_email) is tuple:
        answer=f"{users_without_email[0]}, от общей массы составляет {users_without_email[1]}%"
        return answer
    else:
        return users_without_email


@router.get("/users-the-most-popular-day-of-week", response_model=str)
async def get_the_most_popular_day_of_week(
    users_the_most_popular_day_of_week: str = Depends(
        dependence.get_users_the_most_popular_day_of_week
    ),
):
    return users_the_most_popular_day_of_week


@router.post("/regist-user", response_model=User)
async def create_user(user: User):
    try:
        await db_service.create_user_info(
            user.login,
            user.password,
            user.email,
            user.age,
            user.gender,
            user.city,
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=422, detail="Ошибка валидации данных: " + str(e)
        )
