from fastapi import FASTAPI

app = FASTAPI()

@app.get("/")
def home():
    return {"message": "working for python"}
