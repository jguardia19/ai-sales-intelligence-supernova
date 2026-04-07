import pandas as pd

def transform_warehouse_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["stock_total"] = pd.to_numeric(df["stock_total"], errors="coerce")
    df["productos_distintos"] = pd.to_numeric(df["productos_distintos"], errors="coerce")

    # ordenar por stock
    df = df.sort_values("stock_total", ascending=False).reset_index(drop=True)
    df["ranking"] = df.index + 1

    total_stock = df["stock_total"].sum()

    # participación
    df["participacion_stock_pct"] = (df["stock_total"] / total_stock) * 100

    # densidad (productos vs stock)
    df["densidad_stock"] = df["stock_total"] / df["productos_distintos"]

    # clasificación
    def classify(row):
        if row["ranking"] <= 3:
            return "CENTRAL"
        elif row["ranking"] <= 10:
            return "IMPORTANTE"
        else:
            return "SECUNDARIO"

    df["nivel_almacen"] = df.apply(classify, axis=1)

    return df