def build_zone_document(row):
    estado = row["estado"]
    clientes = int(row["clientes_activos"])
    pedidos = int(row["total_pedidos"])
    ventas = round(float(row["ventas_totales"]), 2)
    ticket = round(float(row["ticket_promedio"]), 2)
    participacion = round(float(row["participacion_ventas_pct"]), 2)
    ranking = int(row["ranking_estado"])
    nivel = row["nivel_comercial"]
    ultima = row["ultima_compra_zona"]
    concentracion = row["nivel_concentracion"]

    # insight automático
    if ranking == 1:
        insight = "Este estado es el principal mercado del negocio."
    elif participacion >= 10:
        insight = "Este estado tiene una alta relevancia comercial."
    elif participacion >= 5:
        insight = "Este estado tiene una participación media en el negocio."
    else:
        insight = "Este estado tiene baja participación y potencial de crecimiento."

    content = f"""
        Estado: {estado}.
        Clientes activos: {clientes}.
        Pedidos generados: {pedidos}.
        Ventas totales: {ventas} pesos.
        Ticket promedio: {ticket} pesos.
        Participación en ventas: {participacion}%.
        Última actividad registrada: {ultima}.
        Nivel de concentración: {concentracion}.
        Ranking del estado: {ranking}.
        Nivel comercial: {nivel}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"zone_{estado}",
        "document_type": "zone_performance",
        "entity_id": estado,
        "title": f"Desempeño comercial en {estado}",
        "content": content,
        "metadata": {
            "ranking": ranking,
            "participacion": participacion,
            "nivel": nivel,
            "state_name": estado,
            "commercial_level": nivel,
            "concentration_level": concentracion,
            "active_clients": clientes,
            "orders_count": pedidos,
            "revenue_amount": ventas,
            "avg_ticket": ticket,
            "sales_share_pct": participacion,
            "last_activity_date": ultima,
            "metric_scope": "annual",
            "document_group": "zone_performance"
        }
    }


def generate_zone_documents(df):
    return [build_zone_document(row) for _, row in df.iterrows()]