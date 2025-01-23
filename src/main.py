from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import HTMLResponse
from src.schemas import User
from typing import List
from src.dependencies import valid_login
from src.users_info.service import create_user_info
from starlette.responses import JSONResponse

app = FastAPI()
router = APIRouter()

# @router.get("/users", response_model=List[User])
# async def get_email_by_login(email: str = Depends(valid_login)):
#     return email
#
@router.post("/regist-user", response_model=User)
async def create_user(user: User):
    try:
        await create_user_info(user.login, user.password, user.email)
        return user
    except Exception as e:
        return {"Error": str(e)}
app.include_router(router)
@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Регистрация пользователя</title>
    </head>
    <body>
        <h1>Регистрация пользователя</h1>
        <form id="user-form">
            <label for="login">Логин:</label>
            <input type="text" id="login" name="login" required><br><br>

            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required><br><br>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>

            <button type="submit">Зарегистрироваться</button>
        </form>

        <script>
            document.getElementById('user-form').addEventListener('submit', async function(event) {
                event.preventDefault(); // Предотвращаем перезагрузку страницы

                const login = document.getElementById('login').value;
                const password = document.getElementById('password').value;
                const email = document.getElementById('email').value;

                const response = await fetch('/regist-user', { // Используйте относительный путь
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ login, password, email }),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(`Пользователь ${result.login} успешно зарегистрирован`);
                } else {
                    alert('Ошибка регистрации');
                }
            });
        </script>
    </body>
    </html>
    """