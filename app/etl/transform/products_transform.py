import pandas as pd
from app.etl.utils.cleaning import strip_string_columns, drop_duplicates_by_columns


def transform_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = strip_string_columns(df)
    df = drop_duplicates_by_columns(df, ["product_id"])

    numeric_columns = [
        "preciou", "preciom", "precioc",
        "topem", "topec", "visitas",
        "precio_costo", "precio_yuan",
        "subcategoria_id"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    expected_columns = [
        "product_id",
        "nombre",
        "codigo",
        "preciou",
        "preciom",
        "precioc",
        "topem",
        "topec",
        "visitas",
        "estatus",
        "precio_costo",
        "precio_yuan",
        "almacen",
        "subcategoria_id",
        "nombre_subcategoria",
    ]

    df = df[expected_columns]

    return df