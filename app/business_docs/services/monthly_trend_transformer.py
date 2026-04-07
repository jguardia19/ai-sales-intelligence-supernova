import pandas as pd

def transform_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ventas_totales"] = pd.to_numeric(df["ventas_totales"], errors="coerce")
    df["pedidos"] = pd.to_numeric(df["pedidos"], errors="coerce")

    df = df.sort_values("periodo").reset_index(drop=True)

    # ticket promedio
    df["ticket_promedio"] = df["ventas_totales"] / df["pedidos"]

    # variaciones
    df["ventas_prev"] = df["ventas_totales"].shift(1)
    df["pedidos_prev"] = df["pedidos"].shift(1)

    df["var_ventas_pct"] = ((df["ventas_totales"] - df["ventas_prev"]) / df["ventas_prev"]) * 100
    df["var_pedidos_pct"] = ((df["pedidos"] - df["pedidos_prev"]) / df["pedidos_prev"]) * 100

    # ranking
    df = df.sort_values("ventas_totales", ascending=False).reset_index(drop=True)
    df["ranking_mes"] = df.index + 1

    df["year"] = df["periodo"].str[:4].astype(int)
    df["month"] = df["periodo"].str[5:].astype(int)

    # clasificación tendencia
    def classify_trend(val):
        if pd.isna(val):
            return "SIN REFERENCIA"
        if val >= 10:
            return "CRECIMIENTO FUERTE"
        if val > 0:
            return "CRECIMIENTO MODERADO"
        if val <= -10:
            return "CAIDA FUERTE"
        if val < 0:
            return "CAIDA MODERADA"
        return "ESTABLE"

    df["tendencia"] = df["var_ventas_pct"].apply(classify_trend)

    return df
