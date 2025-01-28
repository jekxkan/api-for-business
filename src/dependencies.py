from src.exceptions import AsyncFunctionError, DatabaseError
from src.users_info.service import DBService


class Dependencies:
    """
    Класс для управления зависимостями и выполнения асинхронных
    операций с базой данных
    """

    def __init__(self):
        """
        Инициализация класса с созданием экземпляра для работы с базой данных
        """
        self.service = DBService()

    async def get_users_average_age(self) -> int:
        try:
            average_age = await self.service.get_average_age()
            return average_age
        except DatabaseError:
            raise
        except Exception as e:
            raise AsyncFunctionError(
                f"""Ошибка в асинхронной функции для получения среднего
                возраста: {e}"""
            )

    async def get_users_gender_percentage(self) -> tuple[float, float]:
        try:
            gender_percentage = await self.service.get_gender_percentage()
            return gender_percentage
        except DatabaseError:
            raise
        except Exception as e:
            raise AsyncFunctionError(
                f"""Ошибка в асинхронной функции для получения"
                 соотношения полов: {e}"""
            )

    async def get_users_main_cities(self) -> str:
        try:
            main_cities = await self.service.get_main_cities()
            return ", ".join(main_cities)
        except DatabaseError:
            raise
        except Exception as e:
            raise AsyncFunctionError(
                f"""Ошибка в асинхронной функции для получения
                основных городов проживания: {e}"""
            )

    async def get_users_without_email(self) -> tuple | str:
        try:
            users_without_email = await self.service.get_without_email()
            return users_without_email
        except DatabaseError:
            raise
        except Exception as e:
            raise AsyncFunctionError(
                f"""Ошибка в асинхронной функции для получения 
                количеcтва пользователей без email: {e}"""
            )

    async def get_users_the_most_popular_day_of_week(self) -> str:
        try:
            users_the_most_popular_day_of_week = (
                await self.service.get_the_most_popular_day_of_week()
            )
            return users_the_most_popular_day_of_week
        except DatabaseError:
            raise
        except Exception as e:
            raise AsyncFunctionError(
                f"""Ошибка в асинхронной функции для получения 
                дня недели, в который регистраций больше всего: {e}"""
            )
