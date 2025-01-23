from src.database import DBSession
from src.users_info.models import UserInfo

async def create_user_info(
    login: str, password: str, email: str, session = DBSession()
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
    new_record = UserInfo(login=login, password=password, email=email)
    session.add(new_record)
    await session.commit()
    return new_record