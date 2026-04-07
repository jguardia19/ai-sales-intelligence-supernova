from app.rag.chroma.chroma_client import get_or_create_collection
from app.rag.embeddings.openai_embedder import generate_embeddings_batch


def run():
    collection = get_or_create_collection()

    query = "¿Qué categorías generan más ingresos?"
    embedding = generate_embeddings_batch([query])[0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    print(results)


if __name__ == "__main__":
    run()