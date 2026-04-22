import chromadb
from app.core.config import settings

chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)

collection = chroma_client.get_or_create_collection(
    name=settings.chroma_collection_name
)

def search_similar_chunks(query_embedding: list[float], top_k: int = 8):
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    ids = result.get("ids", [[]])[0]

    rows = []
    for i, doc in enumerate(docs):
        rows.append({
            "chunk_id": ids[i],
            "text": doc,
            "metadata": metas[i],
        })

    return rows