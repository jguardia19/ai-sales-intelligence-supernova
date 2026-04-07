import pandas as pd


def build_category_document(row):
    categoria = row["categoria"]
    unidades = int(row["unidades_vendidas"]) if pd.notna(row["unidades_vendidas"]) else 0
    monto = round(float(row["monto_vendido"]), 2) if pd.notna(row["monto_vendido"]) else 0.0
    ranking = int(row["ranking"]) if pd.notna(row["ranking"]) else 0
    participacion = round(float(row["participacion_pct"]), 2) if pd.notna(row["participacion_pct"]) else 0.0
    ticket = round(float(row["ticket_promedio"]), 2) if pd.notna(row["ticket_promedio"]) else 0.0
    nivel = row["nivel_categoria"] if pd.notna(row["nivel_categoria"]) else "DESCONOCIDO"

    # insight automático
    if ranking == 1:
        insight = "Esta es la categoría con mayor generación de ingresos del negocio."
    elif ranking <= 3:
        insight = "Esta categoría forma parte del núcleo principal del negocio."
    elif ranking <= 10:
        insight = "Esta categoría tiene un desempeño comercial sólido."
    else:
        insight = "Esta categoría tiene menor impacto en las ventas generales."

    content = f"""
        Categoría: {categoria}.
        Unidades vendidas en el año: {unidades}.
        Ventas totales: {monto} pesos.
        Participación sobre ventas totales: {participacion}%.
        Ticket promedio por unidad: {ticket} pesos.
        Ranking de categoría: {ranking}.
        Nivel de desempeño: {nivel}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"category_{int(row['subcategoria_id']) if pd.notna(row['subcategoria_id']) else 0}",
        "document_type": "category_performance",
        "entity_id": int(row["subcategoria_id"]) if pd.notna(row["subcategoria_id"]) else 0,
        "title": f"Desempeño de la categoría {categoria}",
        "content": content,
        "metadata": {
            "ranking": ranking,
            "nivel": nivel,
            "participacion": participacion,
            "category_id": int(row["subcategoria_id"]) if pd.notna(row["subcategoria_id"]) else 0,
            "category_name": categoria,
            "ranking_revenue": ranking,
            "performance_level": nivel,
            "sales_share_pct": participacion,
            "units_sold": unidades,
            "revenue_amount": monto,
            "avg_unit_ticket": ticket,
            "metric_scope": "annual",
            "document_group": "category_performance"
        }
    }


def generate_category_documents(df):
    return [build_category_document(row) for _, row in df.iterrows()]
