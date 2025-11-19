from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from gemini_webapi import GeminiClient
import os

app = FastAPI(title="Gemini API Proxy")
client = None
chat_sessions = {}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    model: Optional[str] = None


class ChatResponse(BaseModel):
    text: str
    session_id: str
    images: List[str] = []


@app.on_event("startup")
async def startup():
    global client
    Secure_1PSID = os.getenv("SECURE_1PSID")
    Secure_1PSIDTS = os.getenv("SECURE_1PSIDTS")
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxy=None)
    await client.init(timeout=30, auto_close=False, close_delay=300, auto_refresh=True)


@app.on_event("shutdown")
async def shutdown():
    if client:
        await client.close()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if request.session_id and request.session_id in chat_sessions:
            chat = chat_sessions[request.session_id]
            response = await chat.send_message(request.message)
        else:
            if request.session_id:
                chat = client.start_chat(model=request.model)
                chat_sessions[request.session_id] = chat
                response = await chat.send_message(request.message)
            else:
                response = await client.generate_content(request.message, model=request.model)
                session_id = "single"

        session_id = request.session_id or "single"

        return ChatResponse(
            text=response.text,
            session_id=session_id,
            images=[img.url for img in response.images]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}