# Створіть власний middleware для FastAPI додатку, який буде виконувати дві основні функції:
# 1. логування деталей запиту
# 2.перевірку наявності спеціального заголовка у запитах.
#
# Розробіть middleware, який для кожного запиту логує таку інформацію:
# 1.HTTP-метод
# 2.URL запиту
# 3.час, коли запит був отриманий.
#
# Виведіть інформацію у консоль сервера.
#
# Ваш middleware повинен перевіряти, чи містить вхідний запит заголовок X-Custom-Header.
#
# Якщо заголовок відсутній, middleware має відправляти відповідь із статус-кодом 400 (Bad Request) і повідомленням про помилку, не передаючи запит далі по ланцюгу обробки.
#
# Створіть кілька тестових маршрутів у вашому FastAPI додатку, які демонструють роботу middleware.
#
# Включіть маршрути, які відповідають звичайним запитам, а також запитам без необхідного заголовка.
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime

app = FastAPI()

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        url = str(request.url)
        time_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{time_received}] {method} {url}")

        if "X-Custom-Header" not in request.headers:
            return JSONResponse(
                status_code=400,
                content={"detail": "Missing X-Custom-Header"}
            )

        response = await call_next(request)
        return response

app.add_middleware(CustomMiddleware)

@app.post("/echo")
async def echo(data: dict):
    return {"received": data}

@app.get("/secure-data")
async def secure_data():
    return {"secret": "Захищені дані"}
