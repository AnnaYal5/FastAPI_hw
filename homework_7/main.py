# Частина 1
#
# Вам потрібно створити простий REST API для каталогу книг.
# API має дозволяти користувачам отримувати список книг, додавати нові книги та перевіряти деталі окремої книги.
#
# Вимоги до API:
# GET /books: повертає список усіх книг у JSON форматі.
# POST /books: приймає нову книгу як JSON та додає її до списку, повертає статус 201 при успішному додаванні.
# GET /books/{id}: повертає деталі книги за ID у JSON форматі.
#
# Кожна книга має наступну структуру даних:
# ID (ціле число, унікальний ідентифікатор)
# Назва (рядок, обов'язкове поле)
# Автор (рядок, обов'язкове поле)
# Рік видання (ціле число)
# Доступна кількість (ціле число)
#
#
# Частина 2
# Створіть ендпоінт API, який буде реєструвати нових користувачів, виконуючи глибоку валідацію вхідних даних.
# Потрібно переконатися, що всі дані відповідають певним критеріям перед тим, як користувач буде зареєстрований.
#
# Вимоги до валідації даних користувача:
# Ім'я: мінімум 2 символи, лише літери.
# Прізвище: мінімум 2 символи, лише літери.
# Електронна пошта: має бути валідною електронною адресою.
# Пароль: мінімум 8 символів, повинен містити хоча б одну велику літеру, одну маленьку літеру, одну цифру та один спеціальний символ.
# Номер телефону: має відповідати патерну мобільного телефону.
#
# Частина 3
# Існує система управління подіями, яка дозволяє створювати, оновлювати, видаляти та запитувати події.
# Кожна функція API повинна повертати відповідний HTTP статус код залежно від результату операції.
#
# Функціонал та відповідні статус коди:
# POST /events: Створення нової події.
# При успішному створенні повертає 201 (Created).
# Якщо дані не проходять валідацію, повертає 400 (Bad Request).
# Якщо користувач не має дозволу створювати події, повертає 403 (Forbidden).
# GET /events: Отримання списку всіх подій.
# При успіху повертає 200 (OK).
# Якщо події відсутні, повертає 204 (No Content).
# GET /events/{id}: Отримання деталей події за ID.
# При знаходженні події повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# PUT /events/{id}: Оновлення існуючої події.
# При успішному оновленні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо дані не проходять валідацію, повертає 400 (Bad Request).
# Якщо користувач намагається змінити несхвалені поля, повертає 422 (Unprocessable Entity).
# DELETE /events/{id}: Видалення події.
# При успішному видаленні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо користувач не має дозволу видалити подію, повертає 403 (Forbidden).
# PATCH /events/{id}/reschedule: Перенесення часу події.
# При успішному перенесенні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо нова дата недійсна або в минулому, повертає 400 (Bad Request).
# POST /events/{id}/rsvp: Реєстрація на подію.
# При успішній реєстрації повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо користувач вже зареєстрований, повертає 409 (Conflict).


from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
from datetime import datetime
import re

app = FastAPI()

books_db = []
users_db = []
events_db = []
event_rsvps = {}

#Models
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    quantity: int

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str

    @validator("password")
    def password_secure(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])"
        if len(v) < 8 or not re.search(pattern, v):
            raise ValueError("Password must be stronger")
        return v

    @validator("phone")
    def phone_valid(cls, v):
        if not re.match(r"^\+380\d{9}$", v):
            raise ValueError("Phone must be in format +380XXXXXXXXX")
        return v

class Event(BaseModel):
    id: int
    title: str
    date: datetime
    description: str
    created_by: str




@app.get("/books")
async def get_books():
    return books_db
# GET /books: повертає список усіх книг у JSON форматі.

@app.post("/books", status_code=201)
async def add_book(book: Book):
    if any(b.id == book.id for b in books_db):
        raise HTTPException(400, "Book already exists")
    books_db.append(book)
    return {"message": "Book added"}
# POST /books: приймає нову книгу як JSON та додає її до списку, повертає статус 201 при успішному додаванні.

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(404, "Book not found")
# GET /books/{id}: повертає деталі книги за ID у JSON форматі.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.post("/register")
async def register_user(user: User):
    if any(u.email == user.email for u in users_db):
        raise HTTPException(400, "Email already registered")
    users_db.append(user)
    return {"message": "User registered"}


@app.post("/events", status_code=201)
async def create_event(event: Event):
    if any(e.id == event.id for e in events_db):
        raise HTTPException(400, "Event exists")
    events_db.append(event)
    return {"message": "Event created"}
# POST /events: Створення нової події.
# При успішному створенні повертає 201 (Created).
# Якщо дані не проходять валідацію, повертає 400 (Bad Request).
# Якщо користувач не має дозволу створювати події, повертає 403 (Forbidden).


@app.get("/events")
async def get_events():
    if not events_db:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return events_db
# GET /events: Отримання списку всіх подій.
# При успіху повертає 200 (OK).
# Якщо події відсутні, повертає 204 (No Content).


@app.get("/events/{event_id}")
async def get_event(event_id: int):
    for e in events_db:
        if e.id == event_id:
            return e
    raise HTTPException(404, "Event not found")
# GET /events/{id}: Отримання деталей події за ID.
# При знаходженні події повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).


@app.put("/events/{event_id}")
async def update_event(event_id: int, event: Event):
    for i, e in enumerate(events_db):
        if e.id == event_id:
            events_db[i] = event
            return {"message": "Event updated"}
    raise HTTPException(404, "Event not found")
# PUT /events/{id}: Оновлення існуючої події.
# При успішному оновленні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо дані не проходять валідацію, повертає 400 (Bad Request).
# Якщо користувач намагається змінити несхвалені поля, повертає 422 (Unprocessable Entity).


@app.delete("/events/{event_id}")
async def delete_event(event_id: int):
    for i, e in enumerate(events_db):
        if e.id == event_id:
            del events_db[i]
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Event not found")
# DELETE /events/{id}: Видалення події.
# При успішному видаленні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо користувач не має дозволу видалити подію, повертає 403 (Forbidden).


@app.patch("/events/{event_id}/reschedule")
async def reschedule_event(event_id: int, data: dict):
    for e in events_db:
        if e.id == event_id:
            try:
                new_date = datetime.fromisoformat(data["date"])
                if new_date < datetime.now():
                    raise HTTPException(400, "Date must be in the future")
                e.date = new_date
                return {"message": "Rescheduled"}
            except:
                raise HTTPException(400, "Invalid date")
    raise HTTPException(404, "Event not found")
# PATCH /events/{id}/reschedule: Перенесення часу події.
# При успішному перенесенні повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо нова дата недійсна або в минулому, повертає 400 (Bad Request).


@app.post("/events/{event_id}/rsvp")
async def rsvp_event(event_id: int, user: dict):
    if not any(e.id == event_id for e in events_db):
        raise HTTPException(404, "Event not found")
    event_rsvps.setdefault(event_id, [])
    if user["email"] in event_rsvps[event_id]:
        raise HTTPException(409, "Already registered")
    event_rsvps[event_id].append(user["email"])
    return {"message": "RSVP confirmed"}
# POST /events/{id}/rsvp: Реєстрація на подію.
# При успішній реєстрації повертає 200 (OK).
# Якщо подія з вказаним ID не знайдена, повертає 404 (Not Found).
# Якщо користувач вже зареєстрований, повертає 409 (Conflict).
