import pandas as pd


def build_dead_stock_document(row: pd.Series) -> dict:
    product_id = row["product_id"]
    codigo = str(row["codigo"]).strip()
    nombre = str(row["nombre"]).strip()
    stock = int(row["stock"]) if pd.notna(row["stock"]) else 0
    ranking_stock = int(row["ranking_stock"]) if pd.notna(row["ranking_stock"]) else None
    nivel_alerta = str(row["nivel_alerta"]).strip()
    tipo_riesgo = str(row["tipo_riesgo"]).strip()
    recomendacion = str(row["recomendacion"]).strip()

    content = f"""
    Producto: {nombre}.
    Código: {codigo}.
    Stock actual: {stock} unidades.
    Estado comercial: activo.
    Situación: el producto no registra ventas en el último año.
    Ranking por stock entre productos sin movimiento: {ranking_stock}.
    Nivel de alerta: {nivel_alerta}.
    Tipo de riesgo: {tipo_riesgo}.
    Recomendación inicial: {recomendacion}
    """.strip()

    return {
        "document_id": f"dead_stock_{product_id}",
        "document_type": "dead_stock_alert",
        "entity_id": int(product_id),
        "title": f"Alerta de stock sin movimiento: {nombre}",
        "content": content,
        "metadata": {
            "product_id": int(product_id),
            "codigo": codigo,
            "stock": stock,
            "nivel_alerta": nivel_alerta,
            "tipo_riesgo": tipo_riesgo,
            "ranking_stock": ranking_stock,
            "product_name": nombre,
            "stock_ranking": ranking_stock,
            "recommended_action": recomendacion,
            "metric_scope": "annual",
            "document_group": "dead_stock_alert"
        }
    }


def generate_dead_stock_documents(df: pd.DataFrame) -> list[dict]:
    return [build_dead_stock_document(row) for _, row in df.iterrows()]