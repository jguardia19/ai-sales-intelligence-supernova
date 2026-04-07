from fastapi import APIRouter, HTTPException
from app.rag.schemas.rag import (
    RagQueryRequest,
    RagQueryResponse,
    RagChunkResult,
    RagAskRequest,
    RagAskResponse,
)
from app.rag.chroma.query import search_similar_chunks
from app.rag.services.rag_answer_service import generate_rag_answer
from app.core.config import settings
from app.services.injection_detector import detect_prompt_injection
from app.services.guard_service import contains_bad_words, is_domain_related
from app.services.advanced_guard_service import comprehensive_validation

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/query", response_model=RagQueryResponse)
def query_rag(payload: RagQueryRequest):
    # Validar inyección de prompts
    injection_check = detect_prompt_injection(payload.query)
    if injection_check["is_injection"]:
        raise HTTPException(
            status_code=400,
            detail="Consulta bloqueada: intento de inyección detectado"
        )
    
    # Validar palabras prohibidas
    bad_words_check = contains_bad_words(payload.query)
    if bad_words_check["flagged"]:
        raise HTTPException(
            status_code=400,
            detail=f"Consulta bloqueada: lenguaje inapropiado detectado"
        )
    
    # Validar relevancia de dominio
    if not is_domain_related(payload.query):
        raise HTTPException(
            status_code=400,
            detail="Consulta fuera del dominio de negocio permitido"
        )
    
    try:
        results = search_similar_chunks(
            query=payload.query,
            top_k=payload.top_k,
            collection_name=settings.chroma_collection_name
        )

        parsed = [
            RagChunkResult(
                chunk_id=item["chunk_id"],
                document_id=item["document_id"],
                document_type=item.get("document_type"),
                entity_id=item.get("entity_id"),
                text=item["text"],
                metadata=item.get("metadata", {}),
            )
            for item in results
        ]

        return RagQueryResponse(
            query=payload.query,
            total_results=len(parsed),
            results=parsed
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando RAG: {str(e)}")


@router.post("/ask", response_model=RagAskResponse)
def ask_rag(payload: RagAskRequest):
    # Validación básica de inyección
    injection_check = detect_prompt_injection(payload.query)
    if injection_check["is_injection"]:
        raise HTTPException(
            status_code=400,
            detail="Consulta bloqueada: intento de inyección detectado"
        )
    
    # Validación de palabras prohibidas
    bad_words_check = contains_bad_words(payload.query)
    if bad_words_check["flagged"]:
        raise HTTPException(
            status_code=400,
            detail="Consulta bloqueada: lenguaje inapropiado detectado"
        )
    
    # Validación avanzada (PII, jailbreak, manipulación)
    advanced_check = comprehensive_validation(payload.query)
    if advanced_check["is_blocked"]:
        reasons = []
        if advanced_check["pii"]["contains_pii"]:
            reasons.append("información personal detectada")
        if advanced_check["jailbreak"]["is_jailbreak"]:
            reasons.append("intento de jailbreak")
        if advanced_check["business_context"]["is_off_topic"]:
            reasons.append("fuera de contexto de negocio")
        if advanced_check["output_manipulation"]["is_manipulation"]:
            reasons.append("intento de manipulación de salida")
        if advanced_check["rate_limit"]["is_suspicious"]:
            reasons.append("patrón sospechoso detectado")
        
        raise HTTPException(
            status_code=400,
            detail=f"Consulta bloqueada: {', '.join(reasons)}"
        )
    
    # Validación de dominio
    if not is_domain_related(payload.query):
        raise HTTPException(
            status_code=400,
            detail="Consulta fuera del dominio de negocio permitido"
        )
    
    try:
        result = generate_rag_answer(
            user_query=payload.query,
            top_k=payload.top_k,
            collection_name=settings.chroma_collection_name
        )

        return RagAskResponse(
            query=result["query"],
            answer=result["answer"],
            context=result["context"],
            total_sources=len(result["sources"]),
            sources=result["sources"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta RAG: {str(e)}")
