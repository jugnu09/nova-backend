import asyncio

async def stream_token(generators):
    try:
        for token_text in generators:
                print(f"DEBUG: Processing token_text = '{token_text}'") 
                if token_text:
                    for word in token_text.split(" "):
                        yield f"data: {word} \n\n"
                        await asyncio.sleep(0.01)
        yield "data: [DONE]\n\n"
    except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"
