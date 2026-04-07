
import json
from pathlib import Path

from app.rag.chunking.business_chunker import chunk_business_documents
from app.rag.chroma.indexer import index_chunks_in_chroma



def load_business_documents(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    file_path = Path("data/business_docs/business_documents.json")

    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    print("[INGEST] Cargando documentos...")
    documents = load_business_documents(str(file_path))
    print(f"[INGEST] Documentos cargados: {len(documents)}")

    print("[INGEST] Generando chunks...")
    chunks = chunk_business_documents(
        documents,
        max_tokens=300,
        overlap_tokens=40,
    )
    print(f"[INGEST] Chunks generados: {len(chunks)}")

    total_estimated_tokens = sum(item["estimated_tokens"] for item in chunks)
    print(f"[INGEST] Tokens estimados totales: {total_estimated_tokens}")

    print("[INGEST] Indexando en ChromaDB...")
    index_chunks_in_chroma(chunks, batch_size=100)

    print("[INGEST] Proceso completado correctamente.")


if __name__ == "__main__":
    run()