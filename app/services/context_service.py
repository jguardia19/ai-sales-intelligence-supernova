def build_context(chunks: list[dict], max_chars: int = 7000) -> str:
    blocks = []
    total = 0

    for i, item in enumerate(chunks, start=1):
        meta = item.get("metadata", {})
        title = meta.get("source_title") or "Sin título"
        doc_type = meta.get("document_type", "unknown")
        text = item.get("text", "").strip()

        block = f"""[Fuente {i}]
Tipo: {doc_type}
Título: {title}
Contenido:
{text}
"""

        if total + len(block) > max_chars:
            break

        blocks.append(block)
        total += len(block)

    return "\n\n".join(blocks)