import pandas as pd


def safe_text(value):
    if pd.isna(value):
        return "No disponible"
    return str(value)


def build_monthly_trend_document(row: pd.Series) -> dict:
    periodo = safe_text(row["periodo"])
    pedidos = int(row["pedidos"]) if pd.notna(row["pedidos"]) else 0
    ventas_totales = round(float(row["ventas_totales"]), 2) if pd.notna(row["ventas_totales"]) else 0.0
    tendencia = safe_text(row["tendencia"])
    nivel_desempeno = safe_text(row["nivel_desempeno"])
    insight = safe_text(row["insight"])

    variacion_ventas_pct = row.get("variacion_ventas_pct")
    variacion_pedidos_pct = row.get("variacion_pedidos_pct")

    variacion_ventas_text = (
        f"{round(float(variacion_ventas_pct), 2)}%"
        if pd.notna(variacion_ventas_pct) else "Sin referencia previa"
    )

    variacion_pedidos_text = (
        f"{round(float(variacion_pedidos_pct), 2)}%"
        if pd.notna(variacion_pedidos_pct) else "Sin referencia previa"
    )

    content = f"""
        Periodo: {periodo}.
        Pedidos generados: {pedidos}.
        Ventas totales: {ventas_totales} pesos.
        Variación de ventas vs mes anterior: {variacion_ventas_text}.
        Variación de pedidos vs mes anterior: {variacion_pedidos_text}.
        Tendencia del periodo: {tendencia}.
        Nivel de desempeño comercial: {nivel_desempeno}.
        Observación ejecutiva: {insight}
        """.strip()

    return {
        "document_id": f"monthly_trend_{periodo}",
        "document_type": "monthly_trend",
        "entity_id": periodo,
        "title": f"Tendencia comercial del periodo {periodo}",
        "content": content,
        "metadata": {
            "periodo": periodo,
            "pedidos": pedidos,
            "ventas_totales": ventas_totales,
            "tendencia": tendencia,
            "nivel_desempeno": nivel_desempeno,
        }
    }


def generate_trend_documents(df: pd.DataFrame) -> list[dict]:
    return [build_monthly_trend_document(row) for _, row in df.iterrows()]