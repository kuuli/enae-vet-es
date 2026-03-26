"""Tests for VETES-1: /public static files and tool-free /askbot conversational chain."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app import create_app, public_root


class EchoContextChatModel(BaseChatModel):
    """Concatenates all human message contents in order (proves history is passed in)."""

    @property
    def _llm_type(self) -> str:
        return "echo-context"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        human_parts = [str(m.content) for m in messages if m.type == "human"]
        text = " | ".join(human_parts)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])

    @property
    def _identifying_params(self) -> dict:
        return {}


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app(EchoContextChatModel()))


def test_get_public_existing_file_returns_200_and_body(client: TestClient) -> None:
    response = client.get("/public/hello.txt")
    assert response.status_code == 200
    assert b"hello from public" in response.content


def test_get_public_path_outside_directory_returns_404(client: TestClient) -> None:
    repo_readme = Path(__file__).resolve().parent.parent / "README.md"
    assert repo_readme.is_file()
    response = client.get("/public/../README.md")
    assert response.status_code == 404


def test_askbot_json_happy_path(client: TestClient) -> None:
    response = client.post(
        "/askbot",
        json={"msg": "Hello", "session_id": "sess-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess-1"
    assert data["msg"] == "Hello"


def test_askbot_form_urlencoded_happy_path(client: TestClient) -> None:
    response = client.post(
        "/askbot",
        content=b"msg=Hi&session_id=s2",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "s2"
    assert data["msg"] == "Hi"


def test_askbot_missing_msg_or_session_returns_422(client: TestClient) -> None:
    r1 = client.post("/askbot", json={"session_id": "x"})
    assert r1.status_code == 422
    r2 = client.post("/askbot", json={"msg": "m"})
    assert r2.status_code == 422
    r3 = client.post("/askbot", json={"msg": "", "session_id": "x"})
    assert r3.status_code == 422


def test_askbot_empty_body_returns_422(client: TestClient) -> None:
    response = client.post(
        "/askbot",
        content=b"",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_askbot_unsupported_content_type_returns_415(client: TestClient) -> None:
    response = client.post(
        "/askbot",
        content=b"msg=a&session_id=b",
        headers={"Content-Type": "multipart/form-data; boundary=----x"},
    )
    assert response.status_code == 415


def test_askbot_same_session_id_carries_conversation_context(client: TestClient) -> None:
    sid = "shared-session"
    first = client.post(
        "/askbot",
        json={"msg": "first-turn", "session_id": sid},
    )
    assert first.status_code == 200
    second = client.post(
        "/askbot",
        json={"msg": "second-turn", "session_id": sid},
    )
    assert second.status_code == 200
    assert "first-turn" in second.json()["msg"]
    assert "second-turn" in second.json()["msg"]


def test_app_source_has_no_tool_agent_executor_patterns() -> None:
    app_src = Path(__file__).resolve().parent.parent / "app.py"
    text = app_src.read_text(encoding="utf-8")
    assert "AgentExecutor" not in text
    assert "bind_tools" not in text
    assert "@tool" not in text


def test_public_root_points_next_to_app() -> None:
    assert (public_root() / "hello.txt").is_file()
