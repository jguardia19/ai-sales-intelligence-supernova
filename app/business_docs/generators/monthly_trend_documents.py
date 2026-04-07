import pandas as pd

def build_monthly_document(row):
    periodo = row["periodo"]
    pedidos = int(row["pedidos"]) if pd.notna(row["pedidos"]) else 0
    ventas = round(float(row["ventas_totales"]), 2) if pd.notna(row["ventas_totales"]) else 0.0
    year = int(row["year"]) if pd.notna(row["year"]) else 0
    month = int(row["month"]) if pd.notna(row["month"]) else 0
    # Calcular ticket promedio si no existe
    if "ticket_promedio" in row.index:
        ticket = round(float(row["ticket_promedio"]), 2) if pd.notna(row["ticket_promedio"]) else 0.0
    else:
        ticket = round(ventas / pedidos, 2) if pedidos > 0 else 0.0
    
    ranking = int(row["ranking_mes"]) if pd.notna(row["ranking_mes"]) else 0
    tendencia = row["tendencia"] if pd.notna(row["tendencia"]) else "DESCONOCIDO"

    var_ventas = row["var_ventas_pct"]

    if pd.notna(var_ventas):
        var_text = f"{round(var_ventas, 2)}%"
    else:
        var_text = "Sin referencia"

    # insight automático
    if ranking == 1:
        insight = "Este fue el mes con mayor ingreso del periodo analizado."
    elif tendencia == "CRECIMIENTO FUERTE":
        insight = "Se observa un crecimiento importante respecto al mes anterior."
    elif tendencia == "CAIDA FUERTE":
        insight = "Se detecta una caída significativa en ventas respecto al mes anterior."
    else:
        insight = "El comportamiento del mes se mantiene dentro de rangos normales."

    content = f"""
        Periodo: {periodo}.
        Pedidos generados: {pedidos}.
        Ventas totales: {ventas} pesos.
        Ticket promedio: {ticket} pesos.
        Variación de ventas vs mes anterior: {var_text}.
        Tendencia del periodo: {tendencia}.
        Ranking del mes: {ranking}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"monthly_{periodo}",
        "document_type": "monthly_trend",
        "entity_id": periodo,
        "title": f"Tendencia del periodo {periodo}",
        "content": content,
        "metadata": {
            "ranking": ranking,
            "tendencia": tendencia,
            "period": periodo,
            "year": year,
            "month": month,
            "orders_count": pedidos,
            "revenue_amount": ventas,
            "avg_ticket": ticket,
            "sales_variation_pct": var_ventas,
            "trend_type": tendencia,
            "ranking_month": ranking,
            "metric_scope": "monthly",
            "document_group": "monthly_trend"
        }
    }


def generate_monthly_documents(df):
    return [build_monthly_document(row) for _, row in df.iterrows()]
