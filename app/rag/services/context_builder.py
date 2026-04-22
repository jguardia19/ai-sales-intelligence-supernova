def build_analytical_context(chunks: list[dict], max_chars: int = 7000) -> str:
    parts = []
    total_chars = 0

    useful_keys = [
        "document_group",
        "metric_scope",
        "ranking",
        "ranking_revenue",
        "ranking_stock",
        "ranking_month",
        "product_name",
        "client_name",
        "category_name",
        "warehouse_name",
        "codigo",
        "nivel",
        "nivel_alerta",
        "participacion",
        "sales_share_pct",
        "revenue_amount",
        "units_sold",
        "orders_count",
        "avg_ticket",
        "stock_total",
        "stock",
        "period",
        "month",
        "year",
        "sales_variation_pct",
        "recommended_action",
    ]

    for i, chunk in enumerate(chunks, start=1):
        chunk_id = chunk.get("chunk_id", "N/A")
        text = chunk.get("text", "")
        metadata = chunk.get("metadata", {}) or {}
        distance = chunk.get("distance", None)

        meta_text = ", ".join(
            f"{key}: {metadata[key]}"
            for key in useful_keys
            if key in metadata and metadata[key] is not None
        )

        section = f"""
    [Chunk {i}]
    chunk_id: {chunk_id}
    distance: {distance}
    metadata: {meta_text}
    text:
    {text}
    """

        if total_chars + len(section) > max_chars:
            break

        parts.append(section.strip())
        total_chars += len(section)

    return "\n\n".join(parts)