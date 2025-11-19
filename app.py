import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_webapi import GeminiClient

app = FastAPI(title="Gemini API Proxy")

client = None


class ChatRequest(BaseModel):
    message: str
    secure_1psid: str | None = None
    secure_1psidts: str | None = None


@app.on_event("startup")
async def startup():
    global client
    client = GeminiClient()
    await client.init()


@app.on_event("shutdown")
async def shutdown():
    if client:
        await client.close()


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await client.generate_content(request.message)
        return {"text": response.text, "images": [img.url for img in response.images]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}