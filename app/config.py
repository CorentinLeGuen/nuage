import os
from dotenv import load_dotenv

load_dotenv()

# FastAPI
APP_NAME = os.getenv("APP_NAME", "Nuage")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
DEBUG = os.getenv("DEBUG", "False") == "True"

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 120))

# PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "nuage_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "nuage_db")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://127.0.0.1:9000")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "password")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "nuage-storage")

# Security
ENABLE_2FA = os.getenv("ENABLE_2FA", "False") == "True"
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", 3))
