import pandas as pd

def transform_category_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["monto_vendido"] = pd.to_numeric(df["monto_vendido"], errors="coerce")
    df["unidades_vendidas"] = pd.to_numeric(df["unidades_vendidas"], errors="coerce")

    # ordenar por ventas
    df = df.sort_values("monto_vendido", ascending=False).reset_index(drop=True)
    df["ranking"] = df.index + 1

    total_ventas = df["monto_vendido"].sum()

    # participación %
    df["participacion_pct"] = (df["monto_vendido"] / total_ventas) * 100

    # ticket promedio por categoría
    df["ticket_promedio"] = df["monto_vendido"] / df["unidades_vendidas"]

    # clasificación
    def classify(row):
        if row["ranking"] <= 3:
            return "ESTRELLA"
        elif row["ranking"] <= 10:
            return "ALTA"
        elif row["ranking"] <= 20:
            return "MEDIA"
        else:
            return "BAJA"

    df["nivel_categoria"] = df.apply(classify, axis=1)

    return df