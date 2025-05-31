from celery import Celery
from PIL import Image
import os

celery_app = Celery("tasks", broker="redis://localhost:6379/0")
UPLOAD_DIR = "static/uploads"

@celery_app.task
def optimize_image(name: str):
    path = os.path.join(UPLOAD_DIR, name)
    img = Image.open(path).convert("RGB")
    img.save(path, optimize=True, quality=85)
