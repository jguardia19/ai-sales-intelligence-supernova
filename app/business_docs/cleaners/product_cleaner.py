import pandas as pd
from app.business_docs.cleaners.common_cleaner import (
    normalize_text,
    to_numeric,
    remove_rows_with_nulls,
    remove_duplicates,
)


def clean_product_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # normalizar texto
    df["codigo"] = df["codigo"].apply(normalize_text)
    df["nombre"] = df["nombre"].apply(normalize_text)

    if "categoria" in df.columns:
        df["categoria"] = df["categoria"].apply(normalize_text)

    # numéricos
    df["product_id"] = to_numeric(df["product_id"])
    df["unidades_vendidas"] = to_numeric(df["unidades_vendidas"])
    df["monto_vendido"] = to_numeric(df["monto_vendido"])

    # quitar filas sin identidad
    df = remove_rows_with_nulls(df, ["product_id", "codigo", "nombre"])

    # quitar filas con ventas inválidas
    df = df[
        (df["unidades_vendidas"] > 0) &
        (df["monto_vendido"] > 0)
    ].copy()

    # eliminar duplicados
    df = remove_duplicates(df, ["product_id"])

    # reset
    df = df.reset_index(drop=True)

    return df