import os

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TEXT_MODEL = "gemini-2.5-flash"

settings = Settings()