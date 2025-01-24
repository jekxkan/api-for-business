from typing import Optional

from sqlalchemy import func, select, desc
from src.database import DBSession
from src.users_info.models import UserInfo

async def create_user_info(
    login: str, password: str, email: str, age: int, gender: str, city: str, session = DBSession()
) -> UserInfo:
    """Асинхронная функция, которая создает новую запись в бд

    Args:
        session[DBSession]: экземпляр DBSession
        login[str]: логин пользователя
        password[str]: пароль
        email[str]: почта

    Returns:
        new_record[User]: запись, добавленная в бд
    """
    new_record = UserInfo(login=login, password=password, email=email, age=age, male=gender, city=city)
    session.add(new_record)
    await session.commit()
    return new_record

async def get_average_middle_age(session = DBSession()) -> int:
    stmt = select(func.avg(UserInfo.age))
    result = await session.execute(stmt)
    average_age = int(result.scalar())
    return average_age

async def get_gender_percentage(session = DBSession()) -> tuple:
    stmt = select(func.count(UserInfo.male))
    stmt_female_gender = (select(func.count())
                          .where(UserInfo.male == 'female'))
    result = await session.execute(stmt)
    result_female_gender = await session.execute(stmt_female_gender)
    female_percentage = (result_female_gender.scalar() / result.scalar()) * 100
    male_percentage = 100 - female_percentage
    return (female_percentage, male_percentage)

async def get_main_cities(session = DBSession()) -> list:
    stmt = (
        select(UserInfo.city)
        .group_by(UserInfo.city)
        .order_by(desc(func.count(UserInfo.city)))
        .limit(3)
    )
    result = await session.execute(stmt)
    return list(result.scalars())

async def get_without_email(session = DBSession()) -> tuple|str:
    stmt = (select(func.count())
            .where(UserInfo.email == None))
    count_all_stmt = (select(func.count(UserInfo.login)))
    result = (await session.execute(stmt)).scalar()
    count_all_stmt_result = (await session.execute(count_all_stmt)).scalar()
    if result != 0:
        percentage_users_without_email = (result / count_all_stmt_result) * 100
        return (result, int(percentage_users_without_email))
    else:
        return 'У всех пользователей указана почта'

