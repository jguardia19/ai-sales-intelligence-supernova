import pandas as pd

def transform_client_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["total_comprado"] = pd.to_numeric(df["total_comprado"], errors="coerce")
    df["total_pedidos"] = pd.to_numeric(df["total_pedidos"], errors="coerce")

    # ranking por monto
    df = df.sort_values("total_comprado", ascending=False).reset_index(drop=True)
    df["ranking"] = df.index + 1

    total_ventas = df["total_comprado"].sum()

    # participación
    df["participacion_pct"] = (df["total_comprado"] / total_ventas) * 100

    # ticket promedio
    df["ticket_promedio"] = df["total_comprado"] / df["total_pedidos"]

    # frecuencia de compra
    def classify_frequency(pedidos):
        if pedidos >= 80:
            return "MUY FRECUENTE"
        elif pedidos >= 40:
            return "FRECUENTE"
        elif pedidos >= 15:
            return "OCASIONAL"
        return "BAJO"

    df["frecuencia"] = df["total_pedidos"].apply(classify_frequency)

    # nivel cliente
    def classify_client(rank):
        if rank <= 10:
            return "TOP"
        elif rank <= 50:
            return "ALTO VALOR"
        elif rank <= 200:
            return "MEDIO"
        return "BAJO"

    df["nivel_cliente"] = df["ranking"].apply(classify_client)

    return df