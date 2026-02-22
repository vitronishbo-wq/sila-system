from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from apps.backend.services.openai_client import generate_text
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from core.db.session import get_async_db as get_db
from .service import create_session, add_message, get_recent_messages

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    model: str | None = None
    session_id: int | None = None


@router.post("/codex")
async def codex(request: PromptRequest):
    try:
        # run blocking client in a thread
        resp = await asyncio.to_thread(
            generate_text,
            request.prompt,
            request.model or "gpt-5-nano",
        )
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None
    model: str | None = None


class ChatResponse(BaseModel):
    session_id: int
    assistant: str


def extract_text_from_response(resp_json: dict) -> str:
    # Generic extractor - adapt to actual API shape
    if not resp_json:
        return ""
    # Try common locations
    if isinstance(resp_json, dict):
        if "output" in resp_json:
            out = resp_json["output"]
            if isinstance(out, list) and out:
                first = out[0]
                if isinstance(first, dict):
                    content = first.get("content")
                    if isinstance(content, list) and content:
                        c0 = content[0]
                        if isinstance(c0, dict) and "text" in c0:
                            return c0["text"]
                    text = first.get("text")
                    if isinstance(text, str):
                        return text
        # fallback: look for top-level 'result' or 'text'
        if "result" in resp_json and isinstance(resp_json["result"], str):
            return resp_json["result"]
        if "text" in resp_json and isinstance(resp_json["text"], str):
            return resp_json["text"]
    # Last resort: stringify
    import json

    return json.dumps(resp_json)[:4000]


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    # Create session if needed
    if req.session_id is None:
        sess = await create_session(db)
        session_id = sess.id
    else:
        session_id = req.session_id

    # Persist user message
    await add_message(db, session_id=session_id, role="user", content=req.message)

    # Get recent history
    history_msgs = await get_recent_messages(db, session_id=session_id, limit=20)
    history = [{"role": m.role, "content": m.content} for m in history_msgs]

    # Call OpenAI client in thread to avoid blocking event loop
    prompt_lines = [f"{h['role']}: {h['content']}" for h in history]
    prompt_lines.append(f"user: {req.message}")
    prompt_text = "\n".join(prompt_lines)

    try:
        resp = await asyncio.to_thread(
            generate_text,
            prompt_text,
            req.model or "gpt-5-nano",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    assistant_text = extract_text_from_response(resp)

    # Persist assistant message
    await add_message(
        db, session_id=session_id, role="assistant", content=assistant_text
    )

    return {"session_id": session_id, "assistant": assistant_text}
