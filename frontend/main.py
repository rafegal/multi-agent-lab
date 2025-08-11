import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for CORS, so the chat can be embedded anywhere.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
templates_path = os.path.join(current_dir, "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


import httpx
from pydantic import BaseModel

class Message(BaseModel):
    content: str

AGENT_API_URL = "http://app:8000"

@app.post("/api/sessions")
async def create_session():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AGENT_API_URL}/sessions")
        response.raise_for_status()
        return response.json()

@app.post("/api/sessions/{session_id}/message")
async def post_message(session_id: str, message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AGENT_API_URL}/sessions/{session_id}/message",
            json={"content": message.content}
        )
        response.raise_for_status()
        return response.json()
