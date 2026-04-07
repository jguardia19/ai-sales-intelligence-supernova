import pandas as pd


def build_warehouse_document(row):
    nombre = row["nombre_almacen"]
    productos = int(row["productos_distintos"]) if pd.notna(row["productos_distintos"]) else 0
    stock = int(row["stock_total"]) if pd.notna(row["stock_total"]) else 0
    ranking = int(row["ranking"]) if pd.notna(row["ranking"]) else 0
    participacion = round(float(row["participacion_stock_pct"]), 2) if pd.notna(row["participacion_stock_pct"]) else 0.0
    nivel = row["nivel_almacen"] if pd.notna(row["nivel_almacen"]) else "DESCONOCIDO"
    densidad = round(float(row["densidad_stock"]), 2) if pd.notna(row["densidad_stock"]) else 0.0

    # insight automático
    if ranking == 1:
        insight = "Este almacén concentra la mayor parte del inventario del negocio."
    elif participacion >= 20:
        insight = "Este almacén tiene un peso importante en la distribución del inventario."
    elif participacion >= 10:
        insight = "Este almacén tiene una participación media en el inventario."
    else:
        insight = "Este almacén tiene baja participación en el inventario."

    content = f"""
        Almacén: {nombre}.
        Productos distintos almacenados: {productos}.
        Stock total disponible: {stock} unidades.
        Participación en inventario total: {participacion}%.
        Densidad de stock por producto: {densidad}.
        Ranking del almacén: {ranking}.
        Nivel del almacén: {nivel}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"warehouse_{row['id_almacen']}",
        "document_type": "warehouse_inventory",
        "entity_id": int(row["id_almacen"]) if pd.notna(row["id_almacen"]) else 0,
        "title": f"Estado del almacén {nombre}",
        "content": content,
        "metadata": {
            "ranking": ranking,
            "nivel": nivel,
            "participacion": participacion,
            "warehouse_id": int(row["id_almacen"]) if pd.notna(row["id_almacen"]) else 0,
            "warehouse_name": nombre,
            "ranking_stock": ranking,
            "warehouse_level": nivel,
            "inventory_share_pct": participacion,
            "distinct_products":densidad,
            "stock_total": stock,
            "document_group": "warehouse_inventory",
            "metric_scope": "annual"
        }
    }


def generate_warehouse_documents(df):
    return [build_warehouse_document(row) for _, row in df.iterrows()]
