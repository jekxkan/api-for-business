from typing import Optional

from fastapi import HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from src.database import DBSession
from src.users_info.models import UserInfo


class DBService:
    def __init__(self):
        self.session = DBSession()

    async def create_user_info(
        self,
        login: str,
        password: str,
        email: Optional[str],
        age: int,
        gender: str,
        city: str,
    ) -> UserInfo:
        """
        Асинхронная функция, которая создает новую запись в бд

        Args:
            login[str]: логин пользователя
            password[str]: пароль
            email [Optional[str]]: почта
            age [int]: возраст
            gender [str]: пол
            city [str]: город проживания

        Returns:
            new_record[UserInfo]: запись, добавленная в бд

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            async with self.session.begin():
                new_record = UserInfo(
                    login=login,
                    password=password,
                    email=email,
                    age=age,
                    male=gender,
                    city=city,
                )
                self.session.add(new_record)
                await self.session.commit()
                return new_record
        except SQLAlchemyError as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f'Ошибка добавления'
                                                        f'записи в бд: {e}')

    async def get_average_age(self) -> int:
        """
        Асинхронная функция, которая возвращает средний возраст пользователей

        Returns:
            average_age [int]: средний возраст пользователей

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            stmt = select(func.avg(UserInfo.age))
            average_age = (
                await self.session.execute(stmt)
            ).scalar()
            if average_age is None:
                raise HTTPException(status_code=404, detail="Data not found")
            return int(average_age)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Ошибка бд: {e}')

    async def get_gender_percentage(self) -> tuple[float, float]:
        """
        Асинхронная функция, которая возвращает процентное соотношение
        полов пользователей

        Returns:
            tuple[float, float]: процентное соотношение пользователей женского
            и мужского пола

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            stmt = select(func.count(UserInfo.male))
            stmt_female_gender = select(func.count()).where(
                UserInfo.male == "female"
            )
            result = (
                await self.session.execute(stmt)
            ).scalar()
            users_exist_stmt = select(UserInfo)
            users_exist = (await self.session.execute(users_exist_stmt)).scalar()
            if users_exist is None:
                raise HTTPException(status_code=404, detail="Data not found")
            result_female_gender = (
                await self.session.execute(stmt_female_gender)
            ).scalar()
            female_percentage = (
                result_female_gender / result
            ) * 100
            male_percentage = 100 - female_percentage
            return (round(female_percentage, 1), round(male_percentage, 1))
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Ошибка бд: {e}')

    async def get_main_cities(self) -> list[str]:
        """
        Асинхронная функция, которая возвращает список основных городов
        проживания пользователей

        Returns:
            list[str]: список основных городов проживания пользователей

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            stmt = (
                select(UserInfo.city)
                .group_by(UserInfo.city)
                .order_by(desc(func.count(UserInfo.city)))
                .limit(3)
            )
            result = (
                await self.session.execute(stmt)
            ).scalars()
            users_exist_stmt = select(UserInfo)
            users_exist = (await self.session.execute(users_exist_stmt)).scalar()
            if users_exist is None:
                raise HTTPException(status_code=404, detail="Data not found")
            return list(result)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Ошибка бд: {e}')

    async def get_without_email(self) -> tuple[int, int] | str:
        """
        Асинхронная функция, которая возвращает количество пользователей,
        не оставивших email, и их процентное соотношение

        Returns:
            Tuple[int, int] | str: количество пользователей без email
            и процентное соотношение, или сообщение,
            если все пользователи указали email

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            stmt = select(func.count()).where(UserInfo.email == None)
            count_all_stmt = select(func.count(UserInfo.login))
            result = (await self.session.execute(stmt)).scalar()
            count_all_stmt_result = (
                await self.session.execute(count_all_stmt)
            ).scalar()
            users_exist_stmt = select(UserInfo)
            users_exist = (await self.session.execute(users_exist_stmt)).scalar()
            if users_exist is None:
                raise HTTPException(status_code=404, detail="Data not found")
            if result != 0:
                percentage_users_without_email = (
                    result / count_all_stmt_result
                ) * 100
                return (result, int(percentage_users_without_email))
            else:
                return "У всех пользователей указана почта"
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Ошибка бд: {e}')

    async def get_the_most_popular_day_of_week(self) -> str:
        """
        Асинхронная функция, которая возвращает день недели
        с наибольшим количеством регистраций

        Returns:
            str: день недели с наибольшим количеством регистраций

        Raises:
            - HTTPException(status_code=404): если нет данных
            - HTTPException(status_code=500): если произошла ошибка с бд
        """
        try:
            days_of_week = {
                0: "Воскресенье",
                1: "Понедельник",
                2: "Вторник",
                3: "Среда",
                4: "Четверг",
                5: "Пятница",
                6: "Суббота",
            }
            stmt = select(
                func.extract("dow", UserInfo.registrated_at).label(
                    "day_of_week"
                ),
            )
            result = (
                await self.session.execute(stmt)
            ).scalar()
            if result is None:
                raise HTTPException(status_code=404, detail="Data not found")
            day_of_week = days_of_week[result]
            return day_of_week
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Ошибка бд: {e}')