from pydantic import BaseModel, Field
from typing import Any


class RagQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)


class RagChunkResult(BaseModel):
    chunk_id: str
    document_id: str
    document_type: str | None = None
    entity_id: str | None = None
    text: str
    metadata: dict[str, Any] = {}


class RagQueryResponse(BaseModel):
    query: str
    total_results: int
    results: list[RagChunkResult]


class RagAskRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    top_k: int = Field(default=8, ge=1, le=20)


class RagAskResponse(BaseModel):
    query: str
    answer: str
    context: str
    total_sources: int
    sources: list[dict[str, Any]]
