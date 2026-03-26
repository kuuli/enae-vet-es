"""Single-file FastAPI clinic bot: static files under /public and tool-free LangChain chat."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


def public_root() -> Path:
    """Directory served by GET /public/{file_path:path}."""
    return Path(__file__).resolve().parent / "public"


def _load_system_prompt() -> str:
    return (
        "You are a veterinary clinic reception assistant. "
        "Use clear, professional language. "
        "You do not diagnose conditions or prescribe treatments; "
        "you help with general information and scheduling topics. "
        "Patient refers to the animal; client refers to the owner."
    )


class _PlaceholderLLM(BaseChatModel):
    """Allows importing the module without ``OPENAI_API_KEY`` (e.g. tests, CI)."""

    @property
    def _llm_type(self) -> str:
        return "placeholder-llm"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(
                        content=(
                            "Configure OPENAI_API_KEY (and optionally OPENAI_MODEL) "
                            "to enable live LLM responses."
                        )
                    )
                )
            ]
        )

    @property
    def _identifying_params(self) -> dict:
        return {}


class ClinicChat:
    """Tool-free conversational chain entry point; HTTP layer stays outside this class."""

    def __init__(self, llm: BaseChatModel) -> None:
        self._store: dict[str, InMemoryChatMessageHistory] = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self._store:
                self._store[session_id] = InMemoryChatMessageHistory()
            return self._store[session_id]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", _load_system_prompt()),
                MessagesPlaceholder("history"),
                ("human", "{input}"),
            ]
        )
        self._runnable = RunnableWithMessageHistory(
            prompt | llm,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def invoke(self, user_input: str, config: dict[str, Any]) -> AIMessage:
        result = self._runnable.invoke({"input": user_input}, config=config)
        if not isinstance(result, AIMessage):
            raise TypeError("Expected AIMessage from conversational chain")
        return result


def _default_llm() -> BaseChatModel:
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
        )
    return _PlaceholderLLM()


def _parse_askbot_payload(request: Request, body_bytes: bytes) -> dict[str, Any]:
    content_type = (request.headers.get("content-type") or "").lower()
    if not body_bytes.strip():
        raise HTTPException(status_code=422, detail="Request body is empty")
    if "application/json" in content_type:
        try:
            data = json.loads(body_bytes.decode())
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=422, detail="Invalid JSON body") from exc
        if not isinstance(data, dict):
            raise HTTPException(status_code=422, detail="JSON body must be an object")
        return data
    if "application/x-www-form-urlencoded" in content_type:
        flat: dict[str, str] = {}
        for key, values in parse_qs(
            body_bytes.decode(),
            keep_blank_values=True,
            strict_parsing=False,
        ).items():
            if values:
                flat[key] = values[-1]
        return {"msg": flat.get("msg"), "session_id": flat.get("session_id")}
    raise HTTPException(
        status_code=415,
        detail=(
            "Unsupported Content-Type; use application/json or "
            "application/x-www-form-urlencoded (no multipart)."
        ),
    )


def _validate_msg_and_session(msg: Any, session_id: Any) -> tuple[str, str]:
    if msg is None or session_id is None:
        raise HTTPException(
            status_code=422,
            detail="msg and session_id are required",
        )
    if not isinstance(msg, str) or not msg.strip():
        raise HTTPException(
            status_code=422,
            detail="msg must be a non-empty string",
        )
    if not isinstance(session_id, str) or not session_id.strip():
        raise HTTPException(
            status_code=422,
            detail="session_id must be a non-empty string",
        )
    return msg.strip(), session_id.strip()


def create_app(llm: BaseChatModel | None = None) -> FastAPI:
    """Build FastAPI app. Pass ``llm`` in tests; production uses ChatOpenAI by default."""
    chat = ClinicChat(llm if llm is not None else _default_llm())

    app = FastAPI(title="ENAE Vet Clinic Bot", version="0.1.0")

    @app.get("/public/{file_path:path}")
    async def serve_public(file_path: str) -> FileResponse:
        root = public_root().resolve()
        candidate = (root / file_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail="Not found") from exc
        if not candidate.is_file():
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(candidate)

    @app.post("/askbot")
    async def askbot(request: Request) -> JSONResponse:
        body_bytes = await request.body()
        payload = _parse_askbot_payload(request, body_bytes)
        msg, session_id = _validate_msg_and_session(
            payload.get("msg"),
            payload.get("session_id"),
        )
        config = {"configurable": {"session_id": session_id}}
        reply = chat.invoke(msg, config=config)
        return JSONResponse({"msg": reply.content, "session_id": session_id})

    return app


app = create_app()
