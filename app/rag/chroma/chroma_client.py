import chromadb
from app.core.config import settings


def get_chroma_client():
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)


def get_or_create_collection(collection_name: str = None):
    client = get_chroma_client()
    name = collection_name or settings.chroma_collection_name
    return client.get_or_create_collection(name=name)
