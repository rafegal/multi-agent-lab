import os
import httpx
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- App Initialization ---
app = FastAPI()

# --- Configuration ---
AGENT_API_URL = "http://app:8000"
AGENT_API_USERNAME = os.environ.get("AGENT_API_USERNAME", "vitra_agent_user")
AGENT_API_PASSWORD = os.environ.get("AGENT_API_PASSWORD", "vitra_agent_password")

# --- In-memory cache for the agent API token ---
agent_api_token: str | None = None
token_lock = asyncio.Lock()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static files and templates ---
current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
templates_path = os.path.join(current_dir, "templates")
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

# --- Pydantic Models ---
class Message(BaseModel):
    content: str

# --- Authentication with Agent App ---
async def force_get_new_agent_api_token() -> str:
    """Fetches a new token from the agent service."""
    global agent_api_token
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AGENT_API_URL}/token",
                data={"username": AGENT_API_USERNAME, "password": AGENT_API_PASSWORD}
            )
            response.raise_for_status()
            token_data = response.json()
            agent_api_token = token_data["access_token"]
            return agent_api_token
    except httpx.HTTPStatusError as e:
        print(f"Error getting token: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail="Could not authenticate with the agent service.")
    except Exception as e:
        print(f"An unexpected error occurred while getting token: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while communicating with the agent service.")

async def get_agent_api_token() -> str:
    """
    Retrieves the agent API token from cache, fetching a new one if necessary.
    This function uses a lock to prevent race conditions.
    """
    global agent_api_token
    async with token_lock:
        if agent_api_token is None:
            return await force_get_new_agent_api_token()
        return agent_api_token

async def invalidate_token():
    """Invalidates the cached token."""
    global agent_api_token
    async with token_lock:
        agent_api_token = None

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def make_agent_request(method: str, url: str, **kwargs):
    """Makes an authenticated request to the agent, with retry logic."""
    token = await get_agent_api_token()
    headers = {"Authorization": f"Bearer {token}", **kwargs.pop("headers", {})}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                await invalidate_token()
                token = await get_agent_api_token()
                headers["Authorization"] = f"Bearer {token}"

                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/api/sessions")
async def create_session():
    return await make_agent_request("POST", f"{AGENT_API_URL}/sessions")

@app.post("/api/sessions/{session_id}/message")
async def post_message(session_id: str, message: Message):
    return await make_agent_request(
        "POST",
        f"{AGENT_API_URL}/sessions/{session_id}/message",
        json={"content": message.content}
    )
