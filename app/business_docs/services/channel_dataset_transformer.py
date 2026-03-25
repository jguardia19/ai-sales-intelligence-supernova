import pandas as pd


def transform_channel_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ventas_totales"] = pd.to_numeric(df["ventas_totales"], errors="coerce")
    df["pedidos"] = pd.to_numeric(df["pedidos"], errors="coerce")

    total_ventas = df["ventas_totales"].sum()

    # participación %
    df["participacion_pct"] = (df["ventas_totales"] / total_ventas) * 100

    # ticket promedio
    df["ticket_promedio"] = df["ventas_totales"] / df["pedidos"]

    # ranking
    df = df.sort_values("ventas_totales", ascending=False).reset_index(drop=True)
    df["ranking"] = df.index + 1

    # clasificación desempeño
    def classify_performance(pct):
        if pct >= 30:
            return "CRITICO"
        if pct >= 20:
            return "ALTO"
        if pct >= 10:
            return "MEDIO"
        return "BAJO"

    df["nivel_desempeno"] = df["participacion_pct"].apply(classify_performance)

    # insight
    def build_insight(row):
        if row["ranking"] == 1:
            return "Este canal es el principal generador de ingresos."
        if row["participacion_pct"] >= 20:
            return "Este canal tiene un peso importante en las ventas."
        if row["participacion_pct"] >= 10:
            return "Este canal tiene un desempeño medio."
        return "Este canal tiene baja participación en las ventas."

    df["insight"] = df.apply(build_insight, axis=1)

    return df