import asyncio

async def stream_token(generators):
    try:
        for event in generators:
                token_text = getattr(event, "text", "")
                print(f"DEBUG: Processing token_text = '{token_text}'") 
                if token_text:
                    for word in token_text.split(" "):
                        yield f"data: {word} \n\n"
                        await asyncio.sleep(0.01)
        yield "data: [DONE]\n\n"
    except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"
