from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_embedding(
    text: str,
    model: str = "text-embedding-3-small",
) -> list[float]:
    """Genera embedding para un solo texto."""
    response = client.embeddings.create(
        model=model,
        input=[text]
    )
    return response.data[0].embedding


def generate_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
) -> list[list[float]]:
    """Genera embeddings para múltiples textos."""
    response = client.embeddings.create(
        model=model,
        input=texts
    )
    return [item.embedding for item in response.data]
