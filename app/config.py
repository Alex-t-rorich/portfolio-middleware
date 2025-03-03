import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

if DEBUG == True:
  print(f"DB_USER={DB_USER}, DB_PASSWORD={'******' if DB_PASSWORD else None}, DB_HOST={DB_HOST}, DB_PORT={DB_PORT}, DB_NAME={DB_NAME}")
