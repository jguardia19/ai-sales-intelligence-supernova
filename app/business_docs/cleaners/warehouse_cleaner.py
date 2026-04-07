import pandas as pd
from app.business_docs.cleaners.common_cleaner import (
    normalize_text,
    to_numeric,
    remove_rows_with_nulls,
    remove_duplicates,
)


def clean_warehouse_dataset(df: pd.DataFrame, allow_zero_stock: bool = False) -> pd.DataFrame:
    df = df.copy()

    df["nombre_almacen"] = df["nombre_almacen"].apply(normalize_text)
    df["id_almacen"] = to_numeric(df["id_almacen"])
    df["productos_distintos"] = to_numeric(df["productos_distintos"])
    df["stock_total"] = to_numeric(df["stock_total"])

    df = remove_rows_with_nulls(df, ["id_almacen", "nombre_almacen"])

    # eliminar stock negativo
    df = df[df["stock_total"] >= 0].copy()

    if not allow_zero_stock:
        df = df[df["stock_total"] > 0].copy()

    df = df[df["productos_distintos"] >= 0].copy()

    df = remove_duplicates(df, ["id_almacen"])
    df = df.reset_index(drop=True)

    return df