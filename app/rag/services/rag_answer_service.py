from openai import OpenAI
from app.core.config import settings
from app.rag.chroma.query import search_similar_chunks
from app.rag.services.context_builder import build_analytical_context
from app.rag.prompts.analyst_prompt import SYSTEM_ANALYST_PROMPT

client = OpenAI(api_key=settings.openai_api_key)


def generate_rag_answer(
    user_query: str,
    top_k: int = 8,
    collection_name: str = "business_documents",
    model: str = "gpt-4.1-mini",
) -> dict:
    """
    Recupera contexto desde ChromaDB y genera una respuesta analítica.
    """
    retrieved_chunks = search_similar_chunks(
        query=user_query,
        top_k=top_k,
        collection_name=collection_name,
    )

    context = build_analytical_context(retrieved_chunks, max_chars=7000)

    user_prompt = f"""
Pregunta del usuario:
{user_query}

Contexto recuperado:
{context}

Instrucción:
Responde con un análisis útil, claro y ejecutivo basado únicamente en el contexto recuperado.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_ANALYST_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    answer = response.choices[0].message.content

    return {
        "query": user_query,
        "answer": answer,
        "context": context,
        "sources": retrieved_chunks,
    }