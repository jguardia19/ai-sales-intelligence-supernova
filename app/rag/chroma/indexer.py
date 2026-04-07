from app.rag.chroma.chroma_client import get_or_create_collection
from app.rag.embeddings.openai_embedder import generate_embeddings_batch


def index_chunks_in_chroma(
    chunks: list[dict],
    batch_size: int = 100,
) -> None:
    collection = get_or_create_collection()

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        ids = [item["chunk_id"] for item in batch]
        texts = [item["text"] for item in batch]
        metadatas = [item["metadata"] for item in batch]

        embeddings = generate_embeddings_batch(texts)

        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )

        print(f"[CHROMA] Batch indexado: {i} - {i + len(batch) - 1}")