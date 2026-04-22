from app.rag.chroma.chroma_client import get_or_create_collection
from app.rag.embeddings.openai_embedder import generate_embedding


def search_similar_chunks(
    query: str,
    top_k: int = 5,
    collection_name: str = "ai_sales_supernova",
) -> list[dict]:
    collection = get_or_create_collection(collection_name)
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    
    # Parsear resultados
    chunks = []
    for i in range(len(results["ids"][0])):
        entity_id = results["metadatas"][0][i].get("entity_id")
        chunks.append({
            "chunk_id": results["ids"][0][i],
            "document_id": results["metadatas"][0][i].get("document_id", ""),
            "document_type": results["metadatas"][0][i].get("document_type"),
            "entity_id": str(entity_id) if entity_id is not None else None,
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
        })
    
    return chunks
