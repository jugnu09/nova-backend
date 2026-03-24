from fastapi import APIRouter, HTTPException, Query
from src.services.llm_service import generate_text, generate_text_stream
from src.utils.streaming import stream_token
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/chat/stream")
def chat_stream(
    message: str=Query(...,min_length=1,description="user message to get streaming of data"),
    temperature: float=Query(0.7, ge=0.0,le=2.0, description="creativity")
):
    stream = generate_text_stream(message, temperature)
    return StreamingResponse(
        stream_token(stream),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@router.get("/chat")
def chat_text(
    message: str= Query(..., min_length=1, description="user message to send to gemini"),
    temprature: float =Query(0.7, ge=0.0,le=2.0, description="creativity"),
):
    try:
        response = generate_text(message, temprature)
        reply_text = getattr(response,"text","")
        return {"message": message, "reply": reply_text}
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
