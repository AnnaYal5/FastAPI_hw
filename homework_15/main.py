# 	Як розробники мистецького порталу, ваше завдання — створити API для фото-галереї,
# 	яке дозволяє художникам завантажувати, зберігати та обробляти свої твори.
# Ендпоінт має приймати одне або кілька зображень від користувачів.
# Використайте мультипарт-форму для прийому файлів.
# Реалізуйте логіку для перевірки формату (наприклад, JPG, PNG) та розміру зображень.
# Відхиліть файли, які не відповідають визначеним критеріям.
# Розробіть механізм для зберігання завантажених файлів у локальній файловій системі або обраному хмарному сховищі.
# Використайте фонові завдання для оптимізації зображень (наприклад, зменшення розміру, конвертація формату).
# Забезпечте асинхронну обробку, щоб не блокувати основний потік запитів.
# Напишіть тести для перевірки функціоналу завантаження, валідації та зберігання файлів.
# Переконайтеся, що фонові завдання працюють коректно.
# Імплементуйте механізми для санітізації та безпечного оброблення завантажених файлів.
# Застосуйте найкращі практики для захисту збережених файлів та доступу до них.



from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os, aiofiles, imghdr
from uuid import uuid4
from tasks import optimize_image

app = FastAPI()
UPLOAD_DIR = "static/uploads"
ALLOWED = {"jpg", "jpeg", "png"}
MAX_MB = 5

@app.post("/upload/")
async def upload(files: List[UploadFile] = File(...)):
    saved = []
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED:
            raise HTTPException(400, detail="Invalid format")
        content = await file.read()
        if len(content) > MAX_MB * 1024 * 1024:
            raise HTTPException(400, detail="Too large")
        name = f"{uuid4().hex}.{ext}"
        path = os.path.join(UPLOAD_DIR, name)
        async with aiofiles.open(path, "wb") as f:
            await f.write(content)
        if imghdr.what(path) not in ALLOWED:
            os.remove(path)
            raise HTTPException(400, detail="Not a valid image")
        optimize_image.delay(name)
        saved.append(name)

    return {"uploaded": saved}
