from google import genai
from src.core.config import settings

if not settings:
    raise RuntimeError("Set GEMINI_API_KEY before using this application")
client = genai.Client(api_key= settings.GEMINI_API_KEY)