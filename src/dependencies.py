from typing import Optional

from src.users_info import service

async def get_users_average_age() -> int:
    average_age = await service.get_average_middle_age()
    # if not average_age:
    #     raise AverageAgeNotFound()
    return average_age

async def get_users_gender_percentage() -> tuple:
    gender_percentage = await service.get_gender_percentage()
    return gender_percentage

async def get_users_main_cities() -> str:
    main_cities = await service.get_main_cities()
    return ', '.join(main_cities)

async def get_users_without_email() -> tuple|str:
    users_without_email = await service.get_without_email()
    return users_without_email