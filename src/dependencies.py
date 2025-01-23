from typing import Any

async def valid_login(login: str) -> dict[str, Any]:
    email = await service.get_by_id(login)['email']
    if not email:
        raise EmailNotFound()
    return email