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
        average_age = await self.service.get_average_age()
        return average_age

    async def get_users_gender_percentage(self) -> tuple[float, float]:
        gender_percentage = await self.service.get_gender_percentage()
        return gender_percentage

    async def get_users_main_cities(self) -> str:
        main_cities = await self.service.get_main_cities()
        print(main_cities)
        return ", ".join(main_cities)

    async def get_users_without_email(self) -> tuple | str:
        users_without_email = await self.service.get_without_email()
        return users_without_email

    async def get_users_the_most_popular_day_of_week(self) -> str:
        users_the_most_popular_day_of_week = (
            await self.service.get_the_most_popular_day_of_week()
        )
        return users_the_most_popular_day_of_week