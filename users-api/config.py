from os import environ

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = environ.get("TELEGRAM_BOT_TOKEN")

TELEGRAM_API_URL = environ.get("TELEGRAM_API_URL")

PRODUCTION = environ.get("PRODUCTION") == "true"

WEBAPP_URL = environ.get("WEBAPP_URL")

S3_WORKER_API = environ.get("S3_WORKER_API")

INIT_TABLES = bool(environ.get("INIT_TABLES"))

DATABASE_URL = environ.get("DATABASE_URL")

DB_NAME = environ.get("DB_NAME")

APP_STAGE = environ.get("APP_STAGE")
