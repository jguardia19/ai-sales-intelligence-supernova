from typing import List


def build_analytical_context(results: List[dict], max_chars: int = 6000) -> str:
    """
    Construye un contexto legible y analítico a partir de los chunks recuperados.
    """
    sections = []
    total_chars = 0

    for idx, item in enumerate(results, start=1):
        metadata = item.get("metadata", {})
        document_type = item.get("document_type", "unknown")
        title = metadata.get("source_title") or metadata.get("title") or item.get("document_id", "Sin título")
        text = item.get("text", "").strip()

        block = (
            f"[Documento {idx}]\n"
            f"Tipo: {document_type}\n"
            f"Título: {title}\n"
            f"Contenido:\n{text}\n"
        )

        if total_chars + len(block) > max_chars:
            break

        sections.append(block)
        total_chars += len(block)

    return "\n".join(sections).strip()