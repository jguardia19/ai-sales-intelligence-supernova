from datetime import datetime
def build_product_document(row):
    nombre = row["nombre"]
    codigo = row["codigo"]
    categoria = row["categoria"]
    unidades = int(row["unidades_vendidas"])
    monto = round(float(row["monto_vendido"]), 2)
    ranking = int(row["ranking"])
    participacion = round(float(row["participacion_pct"]), 2)
    nivel = row["nivel_producto"]

    # insight automático
    if ranking == 1:
        insight = "Este es el producto más vendido del año."
    elif ranking <= 10:
        insight = "Este producto se encuentra entre los más vendidos del negocio."
    elif ranking <= 50:
        insight = "Este producto presenta un buen nivel de ventas."
    else:
        insight = "Este producto tiene un nivel de ventas moderado o bajo."

    content = f"""
        Producto: {nombre}.
        Código: {codigo}.
        Categoría: {categoria}.
        Unidades vendidas en el año: {unidades}.
        Monto vendido: {monto} pesos.
        Participación sobre ventas totales: {participacion}%.
        Ranking del producto: {ranking}.
        Nivel de desempeño: {nivel}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"product_{row['product_id']}",
        "document_type": "product_performance",
        "entity_id": int(row["product_id"]),
        "title": f"Desempeño del producto {nombre}",
        "content": content,
        "metadata": {
            "entity_type": "product",
            "document_group": "product_performance",
            "metric_scope": "annual",
            "generated_at": datetime.utcnow().isoformat(),
            "quality_flag": "clean",
            "currency": "MXN",
            "country": "MX",
            "codigo": codigo,
            "product_name": nombre,
            "category": categoria,
            "ranking": ranking,
            "nivel": nivel,
            "participacion": participacion
        }
    }


def generate_product_documents(df):
    return [build_product_document(row) for _, row in df.iterrows()]