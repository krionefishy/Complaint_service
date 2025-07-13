import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = None
    LOGGING_LEVEL: str = "INFO"
    OPEN_AI_KEY: str = None


def setup_config():
    load_dotenv()
    Settings.DATABASE_URL = os.getenv("DATABASE_URL")
    Settings.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
    Settings.OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
    return Settings


