# Створіть Pydantic модель Movie, яка має наступні поля: id (int), title (str), director (str), release_year (int), і rating (float).
# API Ендпоінти:
# GET /movies: Повертає список всіх фільмів.
# POST /movies: Додає новий фільм до колекції.
# GET /movies/{id}: Повертає інформацію про фільм за ID.
# DELETE /movies/{id}: Видаляє фільм із колекції за ID.
# Переконайтеся, що всі поля при додаванні нового фільму валідуються правильно. Наприклад, рік випуску не може бути у майбутньому.
# Використайте Pydantic моделі для серіалізації даних фільмів у JSON, які будуть відправлені у відповідях.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from datetime import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    director: str
    release_year: int = conint(le=datetime.now().year)
    rating: float

movies_db: list[Movie] = []

@app.get("/movies", response_model=list[Movie])
def return_list_of_movie():
    return movies_db

@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    if any(m.id == movie.id for m in movies_db):
        raise HTTPException(status_code=400, detail="Фільм із таким ID вже існує")

    movies_db.append(movie)
    return movie

@app.get("/movies/{id}", response_model=Movie)
def get_movie(id: int):
    for movie in movies_db:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Фільм не знайдено")

@app.delete("/movies/{id}")
def delete_movie(id: int):
    global movies_db
    movies_db = [movie for movie in movies_db if movie.id != id]
    return {"message": "Фільм видалено"}
