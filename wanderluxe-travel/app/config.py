import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "wanderluxe_travel")
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")
SECRET_KEY = os.getenv("SECRET_KEY", "wanderluxe-super-secret-key-2026")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@wanderluxe.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
