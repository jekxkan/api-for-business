from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.routes import router

app = FastAPI()
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
                <input type="text" id="email" name="email"><br><br>
        
                <label for="age">Возраст:</label>
                <input type="number" id="age" name="age" required min="1"><br><br>
        
                <label for="gender">Пол:</label>
                <select id="gender" name="gender" required>
                    <option value="">Выберите пол</option>
                    <option value="male">Мужской</option>
                    <option value="female">Женский</option>
                </select><br><br>
        
                <label for="city">Город проживания:</label>
                <input type="text" id="city" name="city" required><br><br>
        
                <button type="submit">Зарегистрироваться</button>
            </form>
            
            <button id="calculate-age-button">Вычислить средний возраст</button>
            <p>Средний возраст: <span id="average-age"></span></p>
            
            <button id="calculate-gender-percentage-button">Вычислить соотношение полов</button>
            <p>Процентное соотношение полов: <span id="gender-percentage"></span></p>
            
            <button id="find-main-cities-button">Найти основные города</button>
            <p>Основные города проживания пользователей: <span id="main-cities"></span></p>
            
            <button id="calculate-users-without-email-button">Вычислить количество пользователей без почты</button>
            <p>Количество пользователей без почты: <span id="users-without-email"></span></p>
        
            <script>
                document.getElementById('user-form').addEventListener('submit', async function(event) {
                    event.preventDefault();
        
                    const login = document.getElementById('login').value;
                    const password = document.getElementById('password').value;
                    const email = document.getElementById('email').value || null;
                    const age = document.getElementById('age').value;
                    const gender = document.getElementById('gender').value;
                    const city = document.getElementById('city').value;
        
                    const response = await fetch('/regist-user', { 
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ login, password, email, age, gender, city }),
                    });
        
                    if (response.ok) {
                        const result = await response.json();
                        alert(`Пользователь ${result.login} успешно зарегистрирован`);
                    } else {
                        alert('Ошибка регистрации');
                    }
                });
                document.getElementById('calculate-age-button').addEventListener('click', async () => { 
                    const response = await fetch('/average-age'); 
                    if (response.ok) { 
                        const averageAge = await response.text();
                        document.getElementById('average-age').innerText = averageAge; 
                    } else { 
                        alert('Не удалось получить средний возраст.'); 
                    } 
                });
                document.getElementById('calculate-gender-percentage-button').addEventListener('click', async () => { 
                    const response = await fetch('/gender-percentage'); 
                    if (response.ok) { 
                        const genderPercentage = await response.text();
                        document.getElementById('gender-percentage').innerText = genderPercentage; 
                    } else { 
                        alert('Не удалось получить процентное соотношение полов.'); 
                    } 
                });
                document.getElementById('find-main-cities-button').addEventListener('click', async () => { 
                    const response = await fetch('/main-cities'); 
                    if (response.ok) { 
                        const mainCities = await response.text();
                        document.getElementById('main-cities').innerText = mainCities; 
                    } else { 
                        alert('Не удалось получить основные города.'); 
                    } 
                });
                document.getElementById('calculate-users-without-email-button').addEventListener('click', async () => { 
                    const response = await fetch('/users-without-email'); 
                    if (response.ok) { 
                        const usersWithoutEmail = await response.text();
                        document.getElementById('users-without-email').innerText = usersWithoutEmail; 
                    } else { 
                        alert('Не удалось получить количество пользователей без почты.'); 
                    } 
                });
            </script>
        </body>
        </html>
    """