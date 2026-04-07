def build_client_document(row):
    cliente = row["cliente"]
    pedidos = int(row["total_pedidos"])
    monto = round(float(row["total_comprado"]), 2)
    ranking = int(row["ranking"])
    participacion = round(float(row["participacion_pct"]), 2)
    ticket = round(float(row["ticket_promedio"]), 2)
    nivel = row["nivel_cliente"]
    frecuencia = row["frecuencia"]

    # insight automático
    if ranking == 1:
        insight = "Este cliente es el principal generador de ingresos del negocio."
    elif ranking <= 10:
        insight = "Este cliente se encuentra entre los más importantes del negocio."
    elif ranking <= 50:
        insight = "Este cliente tiene un valor comercial alto."
    else:
        insight = "Este cliente tiene un nivel de compra moderado."

    content = f"""
        Cliente: {cliente}.
        Total de pedidos en el año: {pedidos}.
        Monto total comprado: {monto} pesos.
        Ticket promedio: {ticket} pesos.
        Participación en ventas: {participacion}%.
        Frecuencia de compra: {frecuencia}.
        Ranking del cliente: {ranking}.
        Nivel del cliente: {nivel}.
        Observación: {insight}
        """.strip()

    return {
        "document_id": f"client_{row['client_id']}",
        "document_type": "client_profile",
        "entity_id": int(row["client_id"]),
        "title": f"Perfil comercial del cliente {cliente}",
        "content": content,
        "metadata": {
            "client_id": int(row["client_id"]),
            "ranking": ranking,
            "nivel": nivel,
            "frecuencia": frecuencia,
            "client_name": cliente,
            "ranking_revenue": ranking,
            "client_level": nivel,
            "purchase_frequency": frecuencia,
            "orders_count": pedidos,
            "revenue_amount": monto,
            "avg_ticket": ticket,
            "sales_share_pct": participacion,
            "metric_scope": "annual",
            "document_group": "client_profile"
        }
    }


def generate_client_documents(df):
    return [build_client_document(row) for _, row in df.iterrows()]