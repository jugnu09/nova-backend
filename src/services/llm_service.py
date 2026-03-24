from google.genai import types
from src.integrations.gemini_client import client
from src.core.config import settings

MODEL_NAME = settings.TEXT_MODEL

def generate_text(prompt: str, temperature: float = 0.7):
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents= prompt,
        config = types.GenerateContentConfig(temperature = temperature)
    )
    return getattr(response,"text","")

def generate_text_stream(prompt: str, temperature: float = 0.7):
    stream = client.models.generate_content_stream(
        model= MODEL_NAME,
        contents= prompt,
        config = types.GenerateContentConfig(temperature= temperature)
    )
    for events in stream:
        yield getattr(events, "text", "")