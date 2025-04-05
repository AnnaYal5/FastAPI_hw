from pydantic import BaseModel, EmailStr, StringConstraints, Field, field_validator, model_validator
from typing import Annotated
from datetime import *

ShotBioCustomType = Annotated[str, StringConstraints(max_length=125)]

class Author(BaseModel):
    name: str
    email: EmailStr
    bio: ShotBioCustomType | None = None


class Comment(BaseModel):
    author_name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_active: bool = True



"""
5. Модель ArticleRequest - Budko
Атрибути:
    keywords: Список рядків, ключові слова для пошуку статтей.
    date_range: Об'єкт з двох дат (початкова і кінцева дата), для фільтрації статей за періодом.
"""

class DateRange(BaseModel):
    start_date: date
    end_date: date


    @model_validator(mode='after')
    @classmethod
    def validate_date(cls, v):
        if (v.end_date - v.start_date).days < 0:
            raise ValueError
        return v



class ArticleRequest(BaseModel):
    keywords: list[str]
    date_range: DateRange


class Article(BaseModel):
    title: str
    content: str
    author: str
    tags: list[str]
    published_at: datetime = Field(default_factory=datetime.utcnow)