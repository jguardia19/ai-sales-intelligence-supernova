import traceback
from flask import Blueprint, request, jsonify

from app.rag.chroma.query import search_similar_chunks
from app.rag.services.rag_answer_service import generate_rag_answer
from app.core.config import settings
from app.services.injection_detector import detect_prompt_injection
from app.services.guard_service import contains_bad_words, is_domain_related
from app.services.advanced_guard_service import comprehensive_validation

rag_bp = Blueprint("rag", __name__, url_prefix="/rag")


def validate_query(query: str, use_advanced: bool = False):
    injection_check = detect_prompt_injection(query)
    if injection_check["is_injection"]:
        return False, "Consulta bloqueada: intento de inyección detectado"

    bad_words_check = contains_bad_words(query)
    if bad_words_check["flagged"]:
        return False, "Consulta bloqueada: lenguaje inapropiado detectado"

    if not is_domain_related(query):
        return False, "Consulta fuera del dominio de negocio permitido"

    if use_advanced:
        advanced_check = comprehensive_validation(query)

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

            return False, f"Consulta bloqueada: {', '.join(reasons)}"

    return True, None


@rag_bp.route("/query", methods=["POST"])
def query_rag():
    data = request.get_json(silent=True) or {}

    query = (data.get("query") or "").strip()
    top_k = data.get("top_k", 5)

    if not query:
        return jsonify({
            "success": False,
            "message": "La consulta es obligatoria"
        }), 400

    # valid, error = validate_query(query, use_advanced=False)
    # if not valid:
    #     return jsonify({
    #         "success": False,
    #         "message": error
    #     }), 400

    try:
        results = search_similar_chunks(
            query=query,
            top_k=top_k,
            collection_name=settings.chroma_collection_name
        )

        parsed = [
            {
                "chunk_id": item["chunk_id"],
                "document_id": item["document_id"],
                "document_type": item.get("document_type"),
                "entity_id": item.get("entity_id"),
                "text": item["text"],
                "metadata": item.get("metadata", {}),
            }
            for item in results
        ]

        return jsonify({
            "success": True,
            "query": query,
            "total_results": len(parsed),
            "results": parsed
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error consultando RAG: {str(e)}"
        }), 500


@rag_bp.route("/ask", methods=["POST"])
def ask_rag():
    data = request.get_json(silent=True) or {}

    query = (data.get("query") or "").strip()
    top_k = data.get("top_k", 5)

    if not query:
        return jsonify({
            "success": False,
            "message": "La consulta es obligatoria"
        }), 400

    try:
        result = generate_rag_answer(
            user_query=query,
            top_k=top_k,
            collection_name=settings.chroma_collection_name
        )

        return jsonify({
            "success": True,
            "query": result["query"],
            "answer": result["answer"],
            "context": result.get("context"),
            "total_sources": len(result["sources"]),
            "sources": result["sources"],
        })

    except Exception as e:
        print("\n========== ERROR EN /rag/ask ==========")
        traceback.print_exc()
        print("ERROR:", str(e))
        print("=======================================\n")

        return jsonify({
            "success": False,
            "message": f"Error generando respuesta RAG: {str(e)}"
        }), 500