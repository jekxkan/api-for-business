from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.router import router

app = FastAPI()
app.include_router(router)


def read_html_file(path: str) -> str:
    """
    Функция, получающая html код из папки static как переменную, чтобы потом
    передать ее в app.get

     Args:
         path[str]: путь до html-файла

     Returns:
         html_content[str]: переменная, содержащая html-код в виде строки
    """
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return read_html_file("src/static/index.html")
