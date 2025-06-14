# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")

if ENV == "production":
    DATABASE_URL = os.environ["DATABASE_URL"]
else:
    DATABASE_URL = os.getenv("DATABASE_URL_DEV")

    