import asyncio
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google import genai
from google.genai import types

app = FastAPI(title= "Chat API (FastApi plus Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

API_KEY=os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY=",API_KEY)

if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY before running the server")
client = genai.Client(api_key= API_KEY)
MODEL_NAME ="gemini-2.5-flash"

@app.get("/chat")
def chat_get(
    message: str= Query(..., min_length=1, description="user message to send to gemini"),
    temprature: float =Query(0.7, ge=0.0,le=2.0, description="creativity"),
):
    try:
        response = client.models.generate_content(
            model= MODEL_NAME,
            contents=message,
            config= types.GenerateContentConfig(temperature=temprature),
        )
        reply_text = getattr(response,"text","")
        return {"message": message, "reply": reply_text}
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/stream")
async def chat_stream(
    message: str=Query(...,min_length=1,description="user message to get streaming of data"),
    temprature: float=Query(0.7, ge=0.0,le=2.0, description="creativity")
):
    async def event_generator():
        try:
            stream = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=message,
                config=types.GenerateContentConfig(temperature=temprature),
            )

            for event in stream:
                token_text = getattr(event, "text", "")

                if token_text:
                    for word in token_text.split(" "):
                        yield f"data: {word} \n\n"
                        await asyncio.sleep(0.01)
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )