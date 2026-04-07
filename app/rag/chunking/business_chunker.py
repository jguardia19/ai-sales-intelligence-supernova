from __future__ import annotations

import math
import re
from typing import Any


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return math.ceil(len(text) / 4)


def build_embedding_text(document: dict[str, Any]) -> str:
    title = normalize_whitespace(document.get("title", "") or "")
    content = normalize_whitespace(document.get("content", "") or "")

    if title and content:
        return f"{title}\n\n{content}"
    return title or content


def split_text_by_lines(
    text: str,
    max_tokens: int = 300,
    overlap_tokens: int = 40,
) -> list[str]:
    text = normalize_whitespace(text)

    if not text:
        return []

    if estimate_tokens(text) <= max_tokens:
        return [text]

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    chunks: list[str] = []
    current_lines: list[str] = []
    current_text = ""

    for line in lines:
        candidate = "\n".join(current_lines + [line]).strip()

        if estimate_tokens(candidate) <= max_tokens:
            current_lines.append(line)
            current_text = candidate
            continue

        if current_text:
            chunks.append(current_text)

        overlap_lines: list[str] = []
        if overlap_tokens > 0 and current_lines:
            tmp_lines: list[str] = []
            for prev_line in reversed(current_lines):
                test = "\n".join([prev_line] + tmp_lines)
                if estimate_tokens(test) <= overlap_tokens:
                    tmp_lines.insert(0, prev_line)
                else:
                    break
            overlap_lines = tmp_lines

        current_lines = overlap_lines + [line]
        current_text = "\n".join(current_lines).strip()

    if current_text:
        chunks.append(current_text)

    return chunks


def chunk_business_documents(
    documents: list[dict[str, Any]],
    max_tokens: int = 300,
    overlap_tokens: int = 40,
) -> list[dict[str, Any]]:
    chunked_docs: list[dict[str, Any]] = []

    for doc in documents:
        embedding_text = build_embedding_text(doc)

        chunks = split_text_by_lines(
            embedding_text,
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens,
        )

        for idx, chunk_text in enumerate(chunks):
            chunked_docs.append(
                {
                    "chunk_id": f"{doc['document_id']}_chunk_{idx}",
                    "document_id": doc["document_id"],
                    "document_type": doc.get("document_type"),
                    "entity_id": doc.get("entity_id"),
                    "chunk_index": idx,
                    "text": chunk_text,
                    "estimated_tokens": estimate_tokens(chunk_text),
                    "metadata": {
                        **doc.get("metadata", {}),
                        "document_id": doc["document_id"],
                        "document_type": doc.get("document_type"),
                        "entity_id": doc.get("entity_id"),
                        "chunk_index": idx,
                        "source_title": doc.get("title"),
                    },
                }
            )

    return chunked_docs