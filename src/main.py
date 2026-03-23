from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from src.services.llm_service import generate_text_stream, generate_text
from src.utils.streaming import stream_token
from src.api.router import api_router

app = FastAPI(title= "Chat API (FastApi plus Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)