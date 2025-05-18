#
# Створіть API для системи повідомлень, яка включає відправлення електронних листів та логування дій користувачів,
# використовуючи фонові завдання для оптимізації продуктивності.
#
# 1. Ендпоінт для Відправлення Електронних Листів:
# Приймає дані користувача та текст листа.
# Використовує фонове завдання для асинхронної відправки листа.
# Повертає відповідь, що запит на відправлення листа прийнято.
#
# 2. Логування Дій Користувачів:
# Під час кожної операції (наприклад, відправлення листа), дії користувача мають бути залоговані.
# Логер має записувати дату, час, тип операції та інформацію про користувача.
#
# 3. Фонові Завдання для Обробки Великих Файлів:
# Розробіть ендпоінт для завантаження файлів.
# Використайте фонові завдання для асинхронної обробки завантажених файлів (зміна розміру зображень).
#
# 4. Організація Черги Фонових Завдань:
# Налаштуйте систему для обробки черги фонових завдань.
# Забезпечте моніторинг стану та відслідковування помилок у фонових процесах.
#
# Напишіть тести для перевірки коректності відправлення електронних листів і логування.


from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from email.message import EmailMessage
import smtplib, os
from dotenv import load_dotenv
from logger_utils import log_action
from PIL import Image

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = FastAPI()

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.post("/send_email/")
async def send_email_endpoint(
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
):
    background_tasks.add_task(send_email, email, subject, message)
    background_tasks.add_task(log_action, "send_email", email)
    return {"status": "Email task accepted"}


def process_image(file_path: str):
    try:
        with open(file_path) as img:
            img = img.resize((250, 250))
            img.save(file_path)
    except Exception as e:
        log_action("image_processing_error", str(e))


@app.post("/upload_image/")
async def upload_img(background_tasks: BackgroundTasks, file: UploadFile = File(...)):#.png or .jpg
    save_path = f"uploaded_{file.filename}"#назва файлу
    with open(save_path, "wb") as f:
        f.write(await file.read())
    background_tasks.add_task(process_image, save_path)
    background_tasks.add_task(log_action, "upload_image", file.filename)
    return {"status": "Image received and processing started"}