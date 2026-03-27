"""Placeholder FastAPI application for the ENAE vet clinic API (VETES-16 / VET-7)."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ENAE Vet Clinic API",
    version="0.1.0",
    description=(
        "Placeholder HTTP API with mock routes and Pydantic models. "
        "Interactive OpenAPI (Swagger UI) is served at `/docs`; ReDoc at `/redoc`."
    ),
)


class HealthResponse(BaseModel):
    """Liveness / readiness style payload for operators."""

    status: str = Field(examples=["ok"])
    service: str = Field(examples=["enae-vet-es-api"])


class EchoRequest(BaseModel):
    """Sample request body; replace with real bot or booking payloads later."""

    text: str = Field(
        min_length=1,
        max_length=500,
        examples=["Hello, clinic"],
    )


class EchoResponse(BaseModel):
    """Echo response marking data as non-production."""

    reply: str
    placeholder: bool = True


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["meta"],
    summary="Service health",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="enae-vet-es-api")


@app.post(
    "/api/v1/echo",
    response_model=EchoResponse,
    tags=["placeholders"],
    summary="Mock echo endpoint",
)
async def echo_placeholder(body: EchoRequest) -> EchoResponse:
    return EchoResponse(reply=f"echo:{body.text}", placeholder=True)
