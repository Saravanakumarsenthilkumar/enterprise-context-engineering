import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from src.config import settings
from src.security.guardrails import guardrails
from src.security.pii_redactor import pii_redactor
from src.pipeline.retriever import vector_retriever
from src.pipeline.context_builder import context_builder
from src.pipeline.chunking import text_chunker
from src.utils.telemetry import metrics_collector
from src.utils.logger import get_logger

logger = get_logger("api-main")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Enterprise Context Engineering Engine API for GenAI Landing Zones"
)


class ContextRequest(BaseModel):
    query: str = Field(..., example="What are the database snapshot requirements for production?")
    user_roles: List[str] = Field(default_factory=lambda: ["developer"], example=["developer"])
    system_instruction: Optional[str] = Field(
        default="You are an enterprise AI assistant following strict security guidelines.",
        example="You are an enterprise AI assistant following strict security guidelines."
    )
    max_tokens: Optional[int] = Field(default=4096, example=4096)


class ChunkRequest(BaseModel):
    text: str = Field(..., example="Enterprise Cloud Landing Zone Guidelines state...")
    chunk_size: Optional[int] = Field(default=200, example=200)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


@app.post("/api/v1/context/assemble", status_code=status.HTTP_200_OK)
def assemble_context(request: ContextRequest):
    start_time = time.time()

    # 1. Guardrail Input Validation
    is_valid, error_msg = guardrails.validate_prompt(request.query)
    if not is_valid:
        metrics_collector.record_blocked_request(error_msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security Guardrail Violation: {error_msg}"
        )

    # 2. Vector Document Retrieval (with RBAC)
    retrieved_docs = vector_retriever.retrieve(
        query=request.query,
        user_roles=request.user_roles
    )

    # 3. Context Assembly & PII Redaction
    payload, pii_count = context_builder.assemble_context(
        system_instruction=request.system_instruction,
        user_query=request.query,
        rag_documents=retrieved_docs
    )

    latency_ms = (time.time() - start_time) * 1000
    estimated_tokens = context_builder.estimate_tokens(str(payload))
    metrics_collector.record_context_assembly(estimated_tokens, pii_count, latency_ms)

    return {
        "success": True,
        "assembled_payload": payload,
        "metadata": {
            "estimated_tokens": estimated_tokens,
            "pii_entities_redacted": pii_count,
            "retrieved_documents_count": len(retrieved_docs),
            "latency_ms": round(latency_ms, 2)
        }
    }


@app.post("/api/v1/context/chunk", status_code=status.HTTP_200_OK)
def chunk_text(request: ChunkRequest):
    chunks = text_chunker.split_text(request.text, request.metadata)
    return {
        "success": True,
        "total_chunks": len(chunks),
        "chunks": chunks
    }
