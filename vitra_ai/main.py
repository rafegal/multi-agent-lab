import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runtime import SessionManager
from vitra_ai.agent import root_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Message(BaseModel):
    content: str

session_manager = SessionManager(
    engine=os.environ.get("DATABASE_URL")
)


@app.post("/sessions")
async def create_session():
    session = session_manager.create_session()
    return {"session_id": session.session_id}

@app.post("/sessions/{session_id}/message")
async def post_message(session_id: str, message: Message):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    response = await session.send_message(root_agent, message.content)
    return {"response": response}
