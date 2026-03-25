import pandas as pd


def transform_monthly_trends_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ventas_totales"] = pd.to_numeric(df["ventas_totales"], errors="coerce")
    df["pedidos"] = pd.to_numeric(df["pedidos"], errors="coerce")

    df = df.sort_values("periodo").reset_index(drop=True)

    df["ventas_mes_anterior"] = df["ventas_totales"].shift(1)
    df["pedidos_mes_anterior"] = df["pedidos"].shift(1)

    df["variacion_ventas_pct"] = (
        (df["ventas_totales"] - df["ventas_mes_anterior"]) / df["ventas_mes_anterior"] * 100
    )

    df["variacion_pedidos_pct"] = (
        (df["pedidos"] - df["pedidos_mes_anterior"]) / df["pedidos_mes_anterior"] * 100
    )

    def classify_trend(value):
        if pd.isna(value):
            return "SIN REFERENCIA"
        if value >= 10:
            return "CRECIMIENTO FUERTE"
        if value > 0:
            return "CRECIMIENTO MODERADO"
        if value <= -10:
            return "CAIDA FUERTE"
        if value < 0:
            return "CAIDA MODERADA"
        return "ESTABLE"

    def classify_performance(ventas):
        if pd.isna(ventas):
            return "SIN DATOS"
        if ventas >= 9000000:
            return "MUY ALTO"
        if ventas >= 7000000:
            return "ALTO"
        if ventas >= 5000000:
            return "MEDIO"
        return "BAJO"

    df["tendencia"] = df["variacion_ventas_pct"].apply(classify_trend)
    df["nivel_desempeno"] = df["ventas_totales"].apply(classify_performance)

    def build_insight(row):
        if pd.isna(row["variacion_ventas_pct"]):
            return "Periodo inicial del histórico analizado, sin comparación previa."
        if row["variacion_ventas_pct"] >= 10:
            return "Se observa un crecimiento fuerte en ventas respecto al mes anterior."
        if row["variacion_ventas_pct"] > 0:
            return "Se observa crecimiento moderado en ventas respecto al mes anterior."
        if row["variacion_ventas_pct"] <= -10:
            return "Se detecta una caída fuerte en ventas respecto al mes anterior."
        if row["variacion_ventas_pct"] < 0:
            return "Se detecta una caída moderada en ventas respecto al mes anterior."
        return "El periodo se mantiene estable frente al mes anterior."

    df["insight"] = df.apply(build_insight, axis=1)

    return df